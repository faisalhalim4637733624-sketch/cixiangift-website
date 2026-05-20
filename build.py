#!/usr/bin/env python3
"""
GIFT Titanium Website Generator
Reads products.json and generates all HTML pages
"""

import json
import os
from datetime import datetime

# Base paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = BASE_DIR

# Contact info (must not change)
CONTACT_EMAIL = "faisalhalim4637733624@gmail.com"
CONTACT_PHONE = "+86 13085622387"
CONTACT_WHATSAPP = "8613085622387"
GA_ID = "G-395164520"
SITE_URL = "https://cixiangift.com"


def truncate_meta(text, max_len=155):
    """Truncate meta description at word boundary."""
    text = text.strip()
    if len(text) <= max_len:
        return text.replace('"', '&quot;')
    cut = text[:max_len]
    if ' ' in cut:
        cut = cut.rsplit(' ', 1)[0]
    return cut.rstrip('.,;:') + '...'


def load_products():
    """Load products from JSON file"""
    with open(os.path.join(TEMPLATES_DIR, 'products.json'), 'r', encoding='utf-8') as f:
        return json.load(f)


def generate_product_card(product, is_homepage=False):
    """Generate HTML for a product card"""
    badge_html = f'<span class="product-card-badge">{product["badge"]}</span>' if product.get('badge') else ''
    
    features_html = ''.join([f'<span class="product-feature">{f}</span>' for f in product.get('features', [])])
    
    if is_homepage:
        return f'''
        <!-- Product: {product['title']} -->
        <div class="product-card" data-animate>
          <div class="product-card-image">
            <img src="{product['mainImage']}" alt="{product['title']}" loading="lazy">
            {badge_html}
          </div>
          <div class="product-card-content">
            <span class="product-card-category">{product['series']} Series</span>
            <h3 class="product-card-title">{product['title'].replace('Pure Titanium ', '').replace('Collection', '')}</h3>
            <p class="product-card-description">{product['description'][:120]}...</p>
            <div class="product-card-features">
              {features_html}
            </div>
            <div class="product-card-footer">
              <span class="product-card-price">FOB <strong>{product['priceDisplay']}</strong></span>
              <a href="products/{product['slug']}.html" class="btn btn-ghost btn-sm">View Details</a>
            </div>
          </div>
        </div>'''
    else:
        return f'''
        <!-- Product: {product['title']} -->
        <div class="product-card product-item" data-category="{product['category']}" data-animate>
          <div class="product-card-image">
            <img src="{product['mainImage']}" alt="{product['title']}" loading="lazy">
            {badge_html}
          </div>
          <div class="product-card-content">
            <span class="product-card-category">{product['series']} Series</span>
            <h3 class="product-card-title">{product['title'].replace('Pure Titanium ', '').replace('Collection', '')}</h3>
            <p class="product-card-description">{product['description'][:150]}...</p>
            <div class="product-card-features">
              {features_html}
            </div>
            <div class="product-card-footer">
              <span class="product-card-price">FOB <strong>{product['priceDisplay']}</strong></span>
              <a href="products/{product['slug']}.html" class="btn btn-ghost btn-sm">Details</a>
            </div>
          </div>
        </div>'''


def generate_homepage_products(products):
    """Generate homepage product section"""
    # Homepage shows first 6 products
    homepage_products = products[:6]
    cards_html = ''.join([generate_product_card(p, is_homepage=True) for p in homepage_products])
    
    return f'''
      <!-- Products Section -->
      <section class="section section-dark" id="products">
        <div class="container">
          <div class="section-header">
            <span class="section-label">Our Collection</span>
            <h2>Premium Product Lines</h2>
            <p>From elegant gift collections to rugged outdoor gear—complete pure titanium drinkware solutions.</p>
          </div>
          
          <div class="product-grid">
            {cards_html}
          </div>
          
          <div class="text-center mt-4">
            <a href="products.html" class="btn btn-outline btn-lg">View All Products</a>
          </div>
        </div>
      </section>'''


def generate_products_page_products(products):
    """Generate products.html product grid"""
    cards_html = ''.join([generate_product_card(p, is_homepage=False) for p in products])
    
    return f'''
      <div class="product-grid">
        {cards_html}
      </div>'''


def generate_sub_products_section(product):
    """Generate sub-products section for detail pages"""
    if not product.get('subProducts'):
        return ''
    
    sub_cards = []
    for sub in product['subProducts']:
        badge = f'<span class="product-card-badge">{sub["badge"]}</span>' if sub.get('badge') else ''
        features = ''.join([f'<span class="product-feature">{f}</span>' for f in sub.get('features', [])])
        cn = sub.get("nameCn", "")
        name_display = f'{sub["name"]}' + (f' <span style="font-weight:400;color:var(--text-muted);">({cn})</span>' if cn else '')
        
        sub_cards.append(f'''
        <div class="product-card" id="{sub['id']}">
          <div class="product-card-image">
            <img src="../{sub['image']}" alt="{sub['title']}" loading="lazy">
            {badge}
          </div>
          <div class="product-card-content">
            <span class="product-card-category">{name_display}</span>
            <h3 class="product-card-title">{sub['title']}</h3>
            <p class="product-card-description">{sub['description']}</p>
            <div class="product-card-features">
              {features}
            </div>
            <div class="product-card-footer">
              <span class="product-card-price">FOB <strong>{sub['priceDisplay']}</strong></span>
              <button class="btn btn-primary btn-sm" data-get-quote data-product="{sub['title']}">Get Quote</button>
            </div>
          </div>
        </div>''')
    
    return f'''
  <!-- Product Models Section -->
  <section class="section section-bg">
    <div class="container">
      <div class="section-header">
        <h2>Available Models</h2>
        <p>Browse models in this product line — FOB pricing for export orders, MOQ 50 pieces</p>
      </div>
      
      <div class="product-grid">
        {''.join(sub_cards)}
      </div>
    </div>
  </section>'''


def generate_specs_table(specs):
    """Generate specs table rows"""
    rows = []
    for key, value in specs.items():
        key_display = key.replace('_', ' ').title()
        rows.append(f'<tr><th>{key_display}</th><td>{value}</td></tr>')
    return '\n'.join(rows)


def generate_detail_page(product, all_products):
    """Generate a product detail page"""
    specs_rows = generate_specs_table(product.get('specs', {}))
    sub_products_section = generate_sub_products_section(product)
    
    # Find related products (same category, excluding current)
    related = [p for p in all_products if p['category'] == product['category'] and p['id'] != product['id']][:3]
    
    thumbnail_images = [product['mainImage']] + product.get('detailImages', [])[:3]
    thumbnails_html = ''.join([f'''
            <div class="product-thumbnail" data-full-image="../{img}">
              <img src="../{img}" alt="{product['title']} detail">
            </div>''' for img in thumbnail_images[:4]])
    
    features_list = '\n'.join([f'<li>{f}</li>' for f in [
        f'Aerospace-grade Ti>99.8% pure titanium construction',
        'Ultra-lightweight: 40% lighter than stainless steel',
        'Natural antibacterial - keeps drinks fresh',
        'Corrosion-resistant and lifetime durable',
        'FDA & LFGB certified for safety',
        'Premium gift packaging included',
        f'Custom logo and color options available (MOQ 200pcs)'
    ]])
    
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  
  <title>{product['title']} | GIFT Titanium Wholesale</title>
  <meta name="description" content="{truncate_meta(product['description'])} FOB {product['priceDisplay']}. MOQ 50pcs.">
  <meta name="keywords" content="{product['title'].lower()}, titanium cup wholesale, pure titanium manufacturer">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="{SITE_URL}/products/{product['slug']}">
  
  <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🏆</text></svg>">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../css/styles.css">
  
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Product",
    "name": "{product['title']}",
    "description": "{product['description']}",
    "brand": {{"@type": "Brand", "name": "GIFT Titanium"}},
    "category": "Pure Titanium Drinkware"
  }}
  </script>
</head>
<body>
  <!-- Header -->
  <header class="header">
    <div class="container">
      <div class="header-inner">
        <a href="../index.html" class="logo">
          <span class="logo-text">GIFT</span>
          <span class="logo-tagline">Pure Titanium Drinkware</span>
        </a>
        <nav class="nav">
          <ul class="nav-list">
            <li><a href="../index.html" class="nav-link">Home</a></li>
            <li><a href="../products.html" class="nav-link active">Products</a></li>
            <li><a href="../about.html" class="nav-link">About</a></li>
            <li><a href="../blog.html" class="nav-link">Blog</a></li>
            <li><a href="../contact.html" class="nav-link">Contact</a></li>
            <li><a href="#quote" class="btn btn-primary btn-sm" onclick="openQuoteModal()">Get Quote</a></li>
          </ul>
        </nav>
        <button class="menu-toggle" aria-label="Toggle menu"><span></span><span></span><span></span></button>
      </div>
    </div>
    <nav class="mobile-nav">
      <ul class="mobile-nav-list">
        <li><a href="../index.html" class="mobile-nav-link">Home</a></li>
        <li><a href="../products.html" class="mobile-nav-link">Products</a></li>
        <li><a href="../about.html" class="mobile-nav-link">About Us</a></li>
        <li><a href="../blog.html" class="mobile-nav-link">Blog</a></li>
        <li><a href="../contact.html" class="mobile-nav-link">Contact</a></li>
      </ul>
    </nav>
  </header>

  <!-- Product Detail -->
  <section class="product-detail">
    <div class="container">
      <div class="product-detail-grid">
        <div class="product-gallery">
          <div class="product-main-image">
            <img src="../{product['mainImage']}" alt="{product['title']}" id="mainImage">
          </div>
          <div class="product-thumbnails">
            <div class="product-thumbnail active" data-full-image="../{product['mainImage']}">
              <img src="../{product['mainImage']}" alt="{product['title']}">
            </div>
            {thumbnails_html}
          </div>
        </div>
        
        <div class="product-info">
          <nav class="product-breadcrumb">
            <a href="../index.html">Home</a> / <a href="../products.html">Products</a> / <span>{product['series']} Series</span>
          </nav>
          
          <span class="product-category-tag">{product['series']} Series - {product['seriesName']}</span>
          <h1 class="product-title">{product['title']}</h1>
          <p class="product-subtitle">
            {product['description']}
          </p>
          
          <div class="product-price-section">
            <span class="product-price-label">Wholesale Price Range (FOB)</span>
            <div class="product-price">{product['priceDisplay']}</div>
            <span class="product-moq">MOQ: <strong>50 pieces</strong> | Volume discounts available</span>
          </div>
          
          <div class="product-specs">
            <h3>Specifications</h3>
            <table class="specs-table">
              {specs_rows}
            </table>
          </div>
          
          <div class="product-features-list">
            <h3>Key Features</h3>
            <ul>
              {features_list}
            </ul>
          </div>
          
          <div class="product-cta">
            <h3>Interested in This Product?</h3>
            <p>Contact us for detailed FOB pricing, sample availability, and customization options.</p>
            <button class="btn btn-primary btn-lg" data-get-quote data-product="{product['title']}">Get Quote Now</button>
            <p class="product-cta-note">Response within 24 hours | Sample orders welcome</p>
          </div>
        </div>
      </div>
    </div>
  </section>

{sub_products_section}

  <!-- CTA Section -->
  <section class="cta-section" id="quote">
    <div class="container">
      <h2>Ready to Source {product['seriesName']}?</h2>
      <p>Get our wholesale catalog with FOB pricing for bulk orders. MOQ starts at 50 pieces.</p>
      <div class="cta-buttons">
        <a href="../contact.html" class="btn btn-white btn-lg">Contact Us Now</a>
        <a href="../products.html" class="btn btn-outline btn-lg" style="border-color: white; color: white;">View All Products</a>
      </div>
    </div>
  </section>

  <!-- Footer -->
  <footer class="footer">
    <div class="container">
      <div class="footer-grid">
        <div class="footer-brand"><div class="logo-text">GIFT</div><p>Premium pure titanium drinkware manufacturer from China.</p></div>
        <div class="footer-column"><h4>Products</h4><ul class="footer-links"><li><a href="../products/titanium-thermos.html">Titanium Thermos</a></li><li><a href="../products/outdoor-flask.html">Outdoor Flask</a></li><li><a href="../products/office-tea-coffee.html">Office Tea & Coffee</a></li><li><a href="../products.html">All Products</a></li></ul></div>
        <div class="footer-column"><h4>Company</h4><ul class="footer-links"><li><a href="../about.html">About Us</a></li><li><a href="../blog.html">Blog</a></li><li><a href="../contact.html">Contact</a></li></ul></div>
        <div class="footer-column"><h4>Contact</h4><ul class="footer-links"><li>📧 {CONTACT_EMAIL}</li><li>📱 {CONTACT_PHONE}</li><li>📍 Hangzhou, Zhejiang, China</li></ul></div>
      </div>
      <div class="footer-bottom"><p class="footer-copyright">© 2025 GIFT Titanium. All rights reserved.</p></div>
    </div>
  </footer>

  <button class="scroll-top" aria-label="Scroll to top">↑</button>
  
  <div id="quote-modal" class="quote-modal">
    <div class="quote-modal-content">
      <div class="quote-modal-header">
        <div>
          <span class="quote-modal-label">Get Your Quote</span>
          <h2>Request a Quote</h2>
        </div>
        <button class="quote-modal-close" onclick="closeQuoteModal()" type="button">×</button>
      </div>
      <form id="quote-form" action="https://formsubmit.co/{CONTACT_EMAIL}" method="POST">
        <input type="hidden" name="_subject" value="GIFT Titanium Product Inquiry">
        <input type="hidden" name="_captcha" value="false">
        <input type="hidden" name="_template" value="table">
        <input type="hidden" name="_next" value="{SITE_URL}/products/{product['slug']}">
        <input type="hidden" name="product" id="quote-product">
        <div class="form-group"><label class="form-label">Full Name <span class="required">*</span></label><input type="text" name="name" class="form-input" required></div>
        <div class="form-group"><label class="form-label">Business Email <span class="required">*</span></label><input type="email" name="email" class="form-input" required></div>
        <div class="form-group"><label class="form-label">Company Name <span class="required">*</span></label><input type="text" name="company" class="form-input" required></div>
        <div class="form-group"><label class="form-label">Quantity Needed</label><input type="text" name="quantity" class="form-input" placeholder="e.g., 200 pieces"></div>
        <div class="form-group"><label class="form-label">Message</label><textarea name="message" class="form-textarea" placeholder="Tell us about your requirements..."></textarea></div>
        <button type="submit" class="btn btn-primary btn-full">Send Inquiry</button>
      </form>
    </div>
  </div>

  <script src="../js/main.js"></script>
</body>
</html>'''


def update_index_html(data):
    """Update index.html with new products"""
    products_html = generate_homepage_products(data['products'])
    
    # Read existing index.html
    with open(os.path.join(TEMPLATES_DIR, 'index.html'), 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find and replace products section
    start_marker = '<!-- Products Section -->'
    end_marker = '<!-- Testimonials Section -->'
    
    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)
    
    if start_idx != -1 and end_idx != -1:
        new_content = content[:start_idx] + products_html + '\n\n  ' + content[end_idx:]
        
        with open(os.path.join(TEMPLATES_DIR, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("✓ Updated index.html")
    else:
        print("⚠ Could not find products section markers in index.html")


def update_products_html(data):
    """Update products.html with new products"""
    products_html = generate_products_page_products(data['products'])
    
    # Read existing products.html
    with open(os.path.join(TEMPLATES_DIR, 'products.html'), 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find and replace product grid - look for the grid with first product card
    start_marker = '<div class="product-grid">'
    
    # Find the end: look for the closing div before CTA section
    cta_marker = '<!-- CTA Section -->'
    
    start_idx = content.find(start_marker)
    cta_idx = content.find(cta_marker)
    
    if start_idx != -1 and cta_idx != -1:
        # Find the </div> just before CTA section
        end_idx = content.rfind('</div>', 0, cta_idx)
        
        if end_idx != -1:
            # Find the opening <div> for product-grid container
            container_start = content.rfind('<div', 0, start_idx + 30)
            new_content = content[:container_start] + products_html + '\n      ' + content[end_idx + 6:]
            
            with open(os.path.join(TEMPLATES_DIR, 'products.html'), 'w', encoding='utf-8') as f:
                f.write(new_content)
            print("✓ Updated products.html")
        else:
            print("⚠ Could not find closing div for product grid")
    else:
        print("⚠ Could not find product grid markers in products.html, regenerating...")
        # Fallback: just note that products.html needs manual update
        pass


def generate_all_detail_pages(data):
    """Generate all product detail pages"""
    products_dir = os.path.join(TEMPLATES_DIR, 'products')
    os.makedirs(products_dir, exist_ok=True)
    
    for product in data['products']:
        html_content = generate_detail_page(product, data['products'])
        filename = os.path.join(products_dir, f"{product['slug']}.html")
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✓ Generated {product['slug']}.html")


def main():
    """Main build function"""
    print("\n" + "="*50)
    print("GIFT Titanium Website Generator")
    print("="*50 + "\n")
    
    print("Loading products from products.json...")
    data = load_products()
    print(f"✓ Loaded {len(data['products'])} products\n")
    
    print("Generating HTML pages...")
    update_index_html(data)
    update_products_html(data)
    generate_all_detail_pages(data)
    
    print("\n" + "="*50)
    print("Build complete!")
    print("="*50 + "\n")
    
    print("Generated files:")
    print("  - index.html (products section)")
    print("  - products.html (product grid)")
    for p in data['products']:
        print(f"  - products/{p['slug']}.html")
    print()


if __name__ == '__main__':
    main()
