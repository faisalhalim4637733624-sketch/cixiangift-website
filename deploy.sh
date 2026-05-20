#!/bin/bash
# Deploy GIFT / cixiangift.com site to Netlify
set -e
cd "$(dirname "$0")"

echo "=== GIFT Titanium → Netlify Deploy ==="
echo ""

if ! npx --yes netlify-cli@latest status 2>/dev/null | grep -q "Current project"; then
  echo "Step 1: Log in to Netlify (browser will open)..."
  npx --yes netlify-cli@latest login
fi

echo ""
echo "Step 2: Link to your cixiangift site (if not linked yet)..."
echo "  → Choose your team, then select the site that uses cixiangift.com"
npx --yes netlify-cli@latest link || true

echo ""
echo "Step 3: Deploy to production..."
npx --yes netlify-cli@latest deploy --prod --dir=. --message "Update: cixiangift.com domain, products, blogs"

echo ""
echo "Done! Visit https://cixiangift.com"
