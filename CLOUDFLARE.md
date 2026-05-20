# Deploy cixiangift.com on Cloudflare Pages

Static site — no build step. Publish the **repository root** (where `index.html` lives).

## 1. Connect GitHub (fix “keeps asking to link”)

1. GitHub → **Settings** → **Applications** → **Cloudflare Workers and Pages** → **Configure**
2. Grant access to **`cixiangift-website`** (or all repos)
3. Cloudflare Dashboard → **Workers & Pages** → **Create** → **Pages** → **Connect to Git**
4. Pick repo: `faisalhalim4637733624-sketch/cixiangift-website`

## 2. Build settings

| Setting | Value |
|---------|--------|
| Production branch | `main` |
| Build command | *(leave empty)* |
| Build output directory | `/` |

Click **Save and Deploy**.  
Root must contain `index.html`, `_redirects`, `netlify.toml` (optional on CF), `images/`, etc.

## 3. Custom domain (move from Netlify)

1. In Netlify: remove **cixiangift.com** from the old site (or pause site) so DNS does not conflict.
2. Cloudflare Pages → your project → **Custom domains** → **Set up a custom domain**
3. Add `cixiangift.com` and `www.cixiangift.com`

### If the domain uses Cloudflare DNS

- Pages will suggest a **CNAME** to `your-project.pages.dev`
- For apex `@`, use CNAME flattening (Cloudflare does this automatically) or follow the wizard

### If the domain DNS is elsewhere

- Point **CNAME** `www` → `your-project.pages.dev`
- For apex, use registrar ALIAS/ANAME to `your-project.pages.dev`, or move nameservers to Cloudflare

Wait 5–30 minutes for SSL (HTTPS) to become active.

## 4. Push site files

```bash
git add _redirects CLOUDFLARE.md
git commit -m "Add Cloudflare Pages redirects and deploy guide"
git push origin main
```

Each push to `main` triggers a new deployment.

## 5. After deploy — check

- `https://your-project.pages.dev`
- `https://cixiangift.com`
- `https://cixiangift.com/products`
- `https://cixiangift.com/products/titanium-thermos`
- `https://cixiangift.com/blog`

## Admin / images

- **Production admin** (`/admin`) is static only — use **local** `python3 server.py` + `http://localhost:8899/admin.html` to edit and upload images, then push to GitHub.
- Product images live in `images/` — commit and push so Cloudflare serves them.

## Netlify note

If Netlify shows **usage_exceeded**, the domain may still point there until DNS is updated. After Cloudflare is live, you can leave or delete the Netlify project.
