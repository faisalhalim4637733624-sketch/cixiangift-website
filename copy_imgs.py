import shutil, os

src_base = '/app/data/所有对话/主对话/用户上传/赐贤GIFT_产品图'
dst = '/app/data/所有对话/主对话/用户上传/赐贤GIFT官网/images'

mapping = [
    ('G2_户外探险壶/image26.jpeg', 'outdoor-flask.jpg'),
    ('G3_办公茶咖/image32.jpeg', 'office-tea-coffee.jpg'),
    ('G4_儿童纯钛/image59.jpeg', 'kids-titanium.jpg'),
    ('G5_玻璃钛杯/image8.jpeg', 'titanium-glass.jpg'),
    ('G8_纯钛保鲜盒/image63.jpeg', 'titanium-food-container.jpg'),
]

for rel_src, filename in mapping:
    src_path = os.path.join(src_base, rel_src)
    dst_path = os.path.join(dst, filename)
    if os.path.exists(src_path):
        shutil.copy2(src_path, dst_path)
        print(f'OK: {filename}')
    else:
        print(f'MISSING: {src_path}')

print('Done')
