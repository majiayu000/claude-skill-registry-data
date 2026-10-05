---
name: page-views
description: Use when updating Cloudflare Web Analytics page-view data, src/_data/pageViews.json, or scripts/update-page-views.mjs.
---

# Page Views

## Files

- `scripts/update-page-views.mjs`
- `src/_data/pageViews.json`
- `.github/workflows/update-page-views.yml`

## Rules

- Never print or commit secrets.
- Prefer `npm run views:update:dry` before writing data.
- Generated page-view data should keep stable JSON formatting.
- Views are optional enhancement data; the site must build without fresh analytics credentials.

## Checks

- `npm run views:update:dry` when credentials are available.
- `npm run build`
- `npm run test:playwright` when notes sorting behavior changes.
