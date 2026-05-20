#!/usr/bin/env python3
import re
from pathlib import Path

ROOT = Path(__file__).parent

BLOG_COVERS = {
    "titanium-vs-stainless-steel-water-bottles": "g1-thermos-main.jpg",
    "why-titanium-drinkware-is-the-future-of-premium-gifts": "g2-outdoor-main.jpg",
    "top-10-benefits-of-titanium-cups": "g4-kids-main.jpg",
    "how-titanium-drinkware-is-made": "g3-office-main.jpg",
    "b2b-titanium-cup-sourcing-guide": "g1-detail-1.jpg",
    "titanium-eco-friendly-drinkware": "g2-detail-2.jpg",
}

LIST_IMAGES = [
    ("g1-thermos-main.jpg", "Titanium vs stainless steel water bottles comparison"),
    ("g2-outdoor-main.jpg", "Premium titanium drinkware gift collection"),
    ("g4-kids-main.jpg", "Health benefits of pure titanium cups"),
    ("g3-office-main.jpg", "Titanium drinkware manufacturing process"),
    ("g1-detail-1.jpg", "B2B titanium cup wholesale sourcing"),
    ("g2-detail-2.jpg", "Eco-friendly sustainable titanium drinkware"),
]

SVG_BLOCK = re.compile(
    r'<div class="blog-card-image">\s*'
    r'<motion style="width:100%|<motion style="width:100%|'
    r'<div style="width:100%;height:100%;[\s\S]*?</div>\s*</motion>\s*</motion>|'
    r'<motion style="width:100%[\s\S]*?</motion>\s*</motion>',
    re.MULTILINE,
)

# simpler pattern
SVG_BLOCK = re.compile(
    r'<div class="blog-card-image">\s*<div style="width:100%;height:100%;[\s\S]*?</svg>\s*</div>\s*</div>',
    re.MULTILINE,
)


def hero(slug: str) -> str:
    img = BLOG_COVERS[slug]
    alt = slug.replace("-", " ").title()
    return (
        f'      <figure class="article-hero">\n'
        f'        <img src="../images/{img}" alt="{alt}" width="1200" height="630" loading="eager">\n'
        f"      </figure>\n"
    )


def main():
    blog_html = (ROOT / "blog.html").read_text(encoding="utf-8")
    for image, alt in LIST_IMAGES:
        blog_html, n = SVG_BLOCK.subn(
            f'<div class="blog-card-image">\n'
            f'            <img src="images/{image}" alt="{alt}" loading="lazy">\n'
            f"          </div>",
            blog_html,
            count=1,
        )
        if n != 1:
            print("warn: blog list image", image, "replaced", n)
    (ROOT / "blog.html").write_text(blog_html, encoding="utf-8")
    print("✓ blog.html")

    for path in sorted((ROOT / "blog").glob("*.html")):
        slug = path.stem
        if slug not in BLOG_COVERS:
            continue
        text = path.read_text(encoding="utf-8")
        img = BLOG_COVERS[slug]
        og = f'<meta property="og:image" content="https://cixiangift.com/images/{img}">'

        if 'class="article-hero"' not in text:
            text = re.sub(
                r"(      </header>\n)\s*\n(      <div class=\"article-content\">)",
                r"\1\n" + hero(slug) + r"\2",
                text,
                count=1,
            )

        if "og:image" in text:
            text = re.sub(r'<meta property="og:image" content="[^"]+">', og, text)
        else:
            text = text.replace("  <link rel=\"canonical\"", f"  {og}\n  <link rel=\"canonical\"", 1)

        for s, cover in BLOG_COVERS.items():
            text = text.replace(
                f'<a href="{s}.html">',
                f'<a href="{s}.html" data-cover="{cover}">',
            )
        text = re.sub(r' data-cover="[^"]+"', "", text)
        for s, cover in BLOG_COVERS.items():
            text = re.sub(
                rf'(\.\./images/)placeholder\.jpg(" alt="[^"]*" loading="lazy"></div>\s*'
                rf'<div class="blog-card-content">[\s\S]*?<a href="{re.escape(s)}\.html")',
                rf"\1{cover}\2",
                text,
                count=1,
            )

        path.write_text(text, encoding="utf-8")
        print("✓", path.name)

    print("Done.")


if __name__ == "__main__":
    main()
