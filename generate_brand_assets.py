#!/usr/bin/env python3
"""Generate GIFT Titanium logo and Open Graph images."""

from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    raise SystemExit("Install Pillow: pip install Pillow")

BASE = Path(__file__).parent / "images"
GOLD = (192, 160, 98)
DARK = (10, 10, 10)
MID = (26, 26, 26)
LIGHT = (220, 220, 220)


def draw_logo_png(size=512):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    pad = size // 8
    d.rounded_rectangle([pad, pad, size - pad, size - pad], radius=size // 12, fill=DARK + (255,))
    d.rounded_rectangle([pad + 4, pad + 4, size - pad - 4, size - pad - 4], radius=size // 14, outline=GOLD, width=max(2, size // 80))
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Georgia.ttf", size // 4)
        sub = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", size // 14)
    except OSError:
        font = ImageFont.load_default()
        sub = font
    text = "GIFT"
    bbox = d.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    d.text(((size - tw) / 2, size * 0.32 - th / 2), text, fill=GOLD, font=font)
    tag = "Ti"
    bbox2 = d.textbbox((0, 0), tag, font=sub)
    tw2 = bbox2[2] - bbox2[0]
    d.text(((size - tw2) / 2, size * 0.58), tag, fill=LIGHT, font=sub)
    return img


def draw_og_image():
    w, h = 1200, 630
    img = Image.new("RGB", (w, h), DARK)
    d = ImageDraw.Draw(img)
    for i in range(h):
        t = i / h
        c = tuple(int(DARK[j] * (1 - t * 0.35) + MID[j] * t * 0.35) for j in range(3))
        d.line([(0, i), (w, i)], fill=c)
    d.rounded_rectangle([60, 60, w - 60, h - 60], radius=24, outline=GOLD, width=3)
    try:
        title_f = ImageFont.truetype("/System/Library/Fonts/Supplemental/Georgia.ttf", 72)
        sub_f = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 32)
        small_f = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 24)
    except OSError:
        title_f = sub_f = small_f = ImageFont.load_default()
    d.text((100, 140), "GIFT Titanium", fill=GOLD, font=title_f)
    d.text((100, 240), "Premium Pure Titanium Drinkware", fill=LIGHT, font=sub_f)
    d.text((100, 310), "B2B Wholesale  ·  OEM/ODM  ·  MOQ 50pcs", fill=(160, 160, 160), font=small_f)
    d.text((100, 480), "www.cixiangift.com", fill=GOLD, font=small_f)
  # decorative ring
    cx, cy, r = w - 220, h // 2, 140
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=GOLD, width=4)
    d.ellipse([cx - r + 30, cy - r + 30, cx + r - 30, cy + r - 30], outline=(100, 100, 100), width=2)
    return img


def write_logo_svg():
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" role="img" aria-label="GIFT Titanium">
  <rect width="200" height="200" rx="24" fill="#0A0A0A"/>
  <rect x="6" y="6" width="188" height="188" rx="20" fill="none" stroke="#C0A062" stroke-width="3"/>
  <text x="100" y="95" text-anchor="middle" fill="#C0A062" font-family="Georgia, serif" font-size="52" font-weight="600">GIFT</text>
  <text x="100" y="130" text-anchor="middle" fill="#DCDCDC" font-family="system-ui, sans-serif" font-size="18" letter-spacing="4">PURE TITANIUM</text>
</svg>'''
    (BASE / "logo.svg").write_text(svg, encoding="utf-8")


def main():
    BASE.mkdir(exist_ok=True)
    write_logo_svg()
    draw_logo_png(512).save(BASE / "logo.png", "PNG")
    draw_logo_png(256).save(BASE / "logo-256.png", "PNG")
    draw_og_image().save(BASE / "og-image.jpg", "JPEG", quality=92)
    print("✓ images/logo.svg")
    print("✓ images/logo.png")
    print("✓ images/og-image.jpg")


if __name__ == "__main__":
    main()
