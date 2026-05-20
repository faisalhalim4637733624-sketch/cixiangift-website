import os
import re

html_files = ['about.html', 'blog.html', 'products.html']

product_to_image = {
    'Jiaren Pure Titanium Thermos Cup': 'titanium-thermos.jpg',
    'Nvshen Pure Titanium Thermos': 'titanium-thermos.jpg',
    'Letu Pure Titanium Thermos': 'titanium-thermos.jpg',
    'Daphne Pure Titanium Thermos': 'titanium-thermos.jpg',
    'GIFT Pure Titanium Double Wall Thermos': 'titanium-thermos.jpg',
    'Huazhai Pure Titanium Thermos': 'titanium-thermos.jpg',
    'Explorer Pure Titanium Outdoor Flask': 'outdoor-flask.jpg',
    'Chuanshi Pure Titanium Tea Cup': 'office-tea-coffee.jpg',
    'Jueshi Pure Titanium Office Coffee Cup': 'office-tea-coffee.jpg',
    'Mofei Pure Titanium Coffee Cup': 'office-tea-coffee.jpg',
    'Nannan Kids Pure Titanium Water Bottle': 'kids-titanium.jpg',
    'Yundun Pure Titanium Glass Cup': 'titanium-glass.jpg',
    'Ruyi Stainless Steel Thermos': 'titanium-thermos.jpg',
    'Gaoshan Borosilicate Glass Cup Set': 'titanium-glass.jpg',
    'Lexiang Pure Titanium Food Container': 'titanium-food-container.jpg',
    'GIFT Titanium Manufacturing Facility': 'titanium-thermos.jpg',
    'GIFT Titanium Company': 'office-tea-coffee.jpg',
    'Titanium vs Stainless Steel Water Bottles': 'titanium-thermos.jpg',
    'Titanium Drinkware for Premium Gifts': 'outdoor-flask.jpg',
    'Top 10 Benefits of Titanium Cups': 'office-tea-coffee.jpg',
}

total = 0
for html_file in html_files:
    if os.path.exists(html_file):
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        replaced = 0
        for alt_text, new_image in product_to_image.items():
            pattern = r'<img src="images/placeholder\.jpg" alt="' + re.escape(alt_text) + r'" loading="lazy">'
            replacement = f'<img src="images/{new_image}" alt="{alt_text}" loading="lazy">'
            new_content, count = re.subn(pattern, replacement, content)
            if count > 0:
                content = new_content
                replaced += count
        if replaced > 0:
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f'Updated {html_file}: {replaced} replacements')
        total += replaced

print(f'Total: {total}')
