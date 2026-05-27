#!/bin/bash
# Start admin server (kills old process on port 8899 first)
set -e
cd "$(dirname "$0")"

echo "=== GIFT Admin Server ==="

if lsof -ti :8899 >/dev/null 2>&1; then
  echo "Stopping old server on port 8899..."
  lsof -ti :8899 | xargs kill -9 2>/dev/null || true
  sleep 1
fi

if grep -q '"data:image' products.json 2>/dev/null; then
  echo "Converting base64 images in products.json to files..."
  python3 migrate_base64_images.py
fi

echo ""
echo "Open: http://localhost:8899/admin.html"
echo "Press Ctrl+C to stop"
echo ""
python3 server.py
