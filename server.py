#!/usr/bin/env python3
"""
GIFT Titanium Local Server with API
Provides static file serving and REST API for product management
"""

import http.server
import socketserver
import json
import os
import re
import subprocess
import base64
import urllib.parse
from pathlib import Path

# Configuration
PORT = 8899
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PRODUCTS_FILE = os.path.join(BASE_DIR, 'products.json')


class GIFTRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Custom request handler with API support"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)
    
    def do_GET(self):
        """Handle GET requests"""
        if self.path.startswith('/api/'):
            self.handle_api_get()
        else:
            super().do_GET()
    
    def do_OPTIONS(self):
        """CORS preflight for API"""
        if self.path.startswith('/api/'):
            self.send_response(204)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
        else:
            self.send_error(404, 'Not Found')

    def do_POST(self):
        """Handle POST requests"""
        if self.path.startswith('/api/'):
            self.handle_api_post()
        else:
            self.send_error(404, 'Not Found')
    
    def handle_api_get(self):
        """Handle GET API requests"""
        if self.path == '/api/products':
            self.send_json_response(self.load_products())
        else:
            self.send_error(404, 'API endpoint not found')
    
    def handle_api_post(self):
        """Handle POST API requests"""
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')
        
        if self.path == '/api/products':
            try:
                data = json.loads(body)
                self.save_products(data)
                self.send_json_response({'success': True, 'message': 'Products saved successfully'})
            except json.JSONDecodeError:
                self.send_error(400, 'Invalid JSON')
            except Exception as e:
                self.send_error(500, str(e))
        
        elif self.path == '/api/build':
            try:
                result = self.run_build()
                self.send_json_response({'success': True, 'message': 'Build completed', 'output': result})
            except Exception as e:
                self.send_json_response({'success': False, 'message': str(e)}, status=500)

        elif self.path == '/api/upload-image':
            try:
                payload = json.loads(body)
                path = self.save_uploaded_image(
                    payload.get('filename', 'upload.jpg'),
                    payload.get('data', ''),
                )
                self.send_json_response({'success': True, 'path': path})
            except Exception as e:
                self.send_json_response({'success': False, 'message': str(e)}, status=400)
        
        else:
            self.send_error(404, 'API endpoint not found')
    
    def load_products(self):
        """Load products from JSON file"""
        try:
            with open(PRODUCTS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {'products': [], 'siteInfo': {}}
        except json.JSONDecodeError:
            return {'products': [], 'siteInfo': {}}
    
    def save_products(self, data):
        """Save products to JSON file"""
        with open(PRODUCTS_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def save_uploaded_image(self, filename, data_url):
        """Save base64 image data to images/ and return web path."""
        if not data_url:
            raise ValueError('No image data')
        if ',' in data_url:
            header, b64 = data_url.split(',', 1)
        else:
            b64 = data_url
        raw = base64.b64decode(b64)
        if len(raw) > 5 * 1024 * 1024:
            raise ValueError('Image too large (max 5MB)')

        safe = re.sub(r'[^a-zA-Z0-9._-]', '-', filename or 'upload.jpg').strip('-')
        if not safe.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.gif')):
            safe += '.jpg'

        images_dir = os.path.join(BASE_DIR, 'images')
        os.makedirs(images_dir, exist_ok=True)
        dest = os.path.join(images_dir, safe)
        base, ext = os.path.splitext(safe)
        n = 1
        while os.path.exists(dest):
            dest = os.path.join(images_dir, f'{base}-{n}{ext}')
            n += 1

        with open(dest, 'wb') as f:
            f.write(raw)
        return 'images/' + os.path.basename(dest)
    
    def run_build(self):
        """Run the build script"""
        build_script = os.path.join(BASE_DIR, 'build.py')
        result = subprocess.run(
            ['python3', build_script],
            capture_output=True,
            text=True,
            cwd=BASE_DIR
        )
        
        if result.returncode != 0:
            raise Exception(result.stderr or 'Build failed')
        
        return result.stdout
    
    def send_json_response(self, data, status=200):
        """Send JSON response"""
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        response = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.wfile.write(response)
    
    def log_message(self, format, *args):
        """Custom log format"""
        print(f"[{self.log_date_time_string()}] {args[0]}")


def main():
    """Main entry point"""
    print("\n" + "="*60)
    print("  GIFT Titanium Product Management Server")
    print("="*60)
    print()
    print(f"  Local URL:    http://localhost:{PORT}")
    print(f"  Admin Panel:  http://localhost:{PORT}/admin.html")
    print()
    print("  API Endpoints:")
    print(f"    GET  /api/products - Get all products")
    print(f"    POST /api/products - Save products")
    print(f"    POST /api/build        - Generate HTML pages")
    print(f"    POST /api/upload-image - Save image to images/")
    print()
    print("  Press Ctrl+C to stop the server")
    print("="*60 + "\n")
    
    # Change to the website directory
    os.chdir(BASE_DIR)
    
    with socketserver.TCPServer(("", PORT), GIFTRequestHandler) as httpd:
        print(f"Server running on port {PORT}...")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\nServer stopped.")
            httpd.shutdown()


if __name__ == '__main__':
    main()
