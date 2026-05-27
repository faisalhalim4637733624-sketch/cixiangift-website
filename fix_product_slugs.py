#!/usr/bin/env python3
"""Ensure every product has unique slug + id. Fixes empty slug -> all Detail links become products/.html.

Run: python3 fix_product_slugs.py && python3 build.py
"""

import json
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PRODUCTS_JSON = BASE_DIR / "products.json"

# Stable URLs for main catalog lines (match historical site paths)
CANONICAL_SLUG_BY_ID = {
    "g1-thermos": "titanium-thermos",
    "g2-outdoor": "outdoor-flask",
    "g3-office": "office-tea-coffee",
    "g4-kids": "kids-titanium",
    "g5-glass": "titanium-glass",
    "g8-container": "titanium-food-container",
}


def slugify(text: str) -> str:
    s = (text or "").lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = s.strip("-")
    return s or "item"


def main():
    data = json.loads(PRODUCTS_JSON.read_text(encoding="utf-8"))
    products = data.get("products") or []
    used: set[str] = set()

    for i, p in enumerate(products):
        pid = (p.get("id") or "").strip()

        if pid in CANONICAL_SLUG_BY_ID:
            slug = CANONICAL_SLUG_BY_ID[pid]
        else:
            slug = (p.get("slug") or "").strip()
            if not slug:
                mi = p.get("mainImage") or ""
                stem = Path(mi).stem if mi else ""
                slug = slugify(stem) or slugify(p.get("title")) or f"product-line-{i + 1}"

        base = slug
        n = 2
        while slug in used:
            slug = f"{base}-{n}"
            n += 1
        used.add(slug)
        p["slug"] = slug

        if not (p.get("id") or "").strip():
            p["id"] = slug

        if not (p.get("title") or "").strip():
            stem = Path(p.get("mainImage") or "item").stem
            p["title"] = f"Pure titanium drinkware — {stem.replace('-', ' ')}"

        if not (p.get("seriesName") or "").strip():
            if (p.get("series") or "").strip():
                p["seriesName"] = f"{str(p['series']).upper()} product line"
            else:
                p["seriesName"] = (p.get("title") or "Product")[:120]

        if not (p.get("description") or "").strip():
            p["description"] = (
                "Aerospace-grade pure titanium drinkware for wholesale and OEM. "
                "Contact us for FOB pricing, MOQ, and customization."
            )

        if p.get("priceMin") is None or p.get("priceMax") is None:
            p["priceMin"] = 50
            p["priceMax"] = 200
            p["priceDisplay"] = "$50-200"
        elif not (p.get("priceDisplay") or "").strip() or p.get("priceDisplay") == "$-":
            p["priceDisplay"] = f"${p['priceMin']}-{p['priceMax']}"

        if not p.get("specs"):
            p["specs"] = {
                "material": "Pure Titanium (Ti>99.8%)",
                "moq": "50 pieces",
                "certifications": "FDA, LFGB",
            }

    PRODUCTS_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"OK: {len(products)} products, slugs unique.")


if __name__ == "__main__":
    main()
