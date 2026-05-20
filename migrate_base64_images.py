#!/usr/bin/env python3
"""Convert base64 mainImage fields in products.json to files under images/."""

import base64
import json
import os
import re
from pathlib import Path

ROOT = Path(__file__).parent
PRODUCTS = ROOT / "products.json"
IMAGES = ROOT / "images"


def save_data_url(data_url: str, prefix: str) -> str:
    if "," in data_url:
        _, b64 = data_url.split(",", 1)
    else:
        b64 = data_url
    raw = base64.b64decode(b64)
    ext = ".jpg"
    if "image/png" in data_url[:80]:
        ext = ".png"
    elif "image/webp" in data_url[:80]:
        ext = ".webp"
    safe = re.sub(r"[^a-zA-Z0-9._-]", "-", prefix).strip("-") or "product"
    name = f"{safe}{ext}"
    dest = IMAGES / name
    n = 1
    while dest.exists():
        dest = IMAGES / f"{safe}-{n}{ext}"
        n += 1
    dest.write_bytes(raw)
    return f"images/{dest.name}"


def main():
    data = json.loads(PRODUCTS.read_text(encoding="utf-8"))
    count = 0
    for p in data.get("products", []):
        img = p.get("mainImage", "")
        if isinstance(img, str) and img.startswith("data:"):
            p["mainImage"] = save_data_url(img, p.get("id", "product"))
            count += 1
        for sub in p.get("subProducts") or []:
            simg = sub.get("image", "")
            if isinstance(simg, str) and simg.startswith("data:"):
                sub["image"] = save_data_url(simg, f"{p.get('id','p')}-{sub.get('id','sub')}")
                count += 1
    PRODUCTS.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"✓ Migrated {count} base64 images to images/")


if __name__ == "__main__":
    main()
