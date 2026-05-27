# Deploy to Netlify (cixiangift.com)

This site is a **static** project. Publish directory: **`.`** (project root).

## Prerequisites

- [Node.js](https://nodejs.org/) 18+ (for `npx netlify-cli`)
- A Netlify account with access to the site linked to **cixiangift.com**

## First-time setup

```bash
cd /Users/buaichifan/Desktop/gift_site_fixed

# 1. Log in (opens browser)
npx netlify-cli login

# 2. Link this folder to your existing Netlify site
npx netlify-cli link
# Choose: "Link this directory to an existing project" → select cixiangift site

# 3. Optional: regenerate product pages after editing products.json
python3 build.py
```

## Deploy to production

```bash
cd /Users/buaichifan/Desktop/gift_site_fixed

python3 build.py   # optional, after products.json changes

npx netlify-cli deploy --prod --dir=.
```

When prompted, confirm publish directory is **`.`** (not the old path in `.netlify/netlify.toml`).

## Using a token (CI / no browser)

1. Netlify → User settings → Applications → New access token  
2. Export: `export NETLIFY_AUTH_TOKEN=your_token`  
3. Deploy:

```bash
npx netlify-cli deploy --prod --dir=. --site=YOUR_SITE_ID
```

## After deploy — quick checks

- https://cixiangift.com/
- https://cixiangift.com/products (6 lines, FOB **USD**)
- https://cixiangift.com/products/titanium-thermos (model list + FOB)
- View page source: `canonical` should be `https://cixiangift.com/...` (not gifttitanium.com)
- Submit sitemap in Google Search Console: `https://cixiangift.com/sitemap.xml`

## Regenerate content

| Change | Command |
|--------|---------|
| Products, prices, SKUs | Edit `products.json` → `python3 build.py` |
| Logo / OG image | `python3 generate_brand_assets.py` |
| New blog posts | `python3 generate_blogs.py` |

## Note on admin

`admin.html` is public if deployed. Protect it in Netlify (password) or remove from production if not needed.
