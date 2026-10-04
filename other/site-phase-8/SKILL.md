---
name: site-phase-8
description: >-
  Phase 8 — Final build and deploy to Cloudflare Pages.
  Presents result summary to user.
allowed-tools: Read, Bash
model: sonnet
effort: low
context: fork
user-invocable: false
---

# Phase 8 — Build + Deploy

## Objective

Run the final production build and deploy to Cloudflare Pages. Present the completed site to the user.

## Step 1 — Final build

```bash
cd /Users/felipemoreiralanna/Documents/GitHub/vendedor-de-sites-v2/sites/$LEAD_ID && npm run build
```

Must complete without errors. If it fails, fix and retry.

## Step 2 — Deploy to Cloudflare Pages

```bash
cd /Users/felipemoreiralanna/Documents/GitHub/vendedor-de-sites-v2/sites/$LEAD_ID
wrangler pages deploy dist/ --project-name CLEAN-SLUG
```

Slug: lowercase, hyphens, no accents (e.g., `dra-ariel-cordova`).

## Step 3 — Present result

```
========================================
  SITE READY!
========================================
  Client: [name]
  URL: https://[slug].pages.dev
  Concept: "[phrase]"
  Sections: [list]
  Languages: PT-BR + EN
  Quality score: [X]/10
  Folder: sites/[lead_id]/
  Screenshots: sites/[lead_id]/screenshots/

  Run local: cd sites/[lead_id] && npm run dev
  Re-deploy: cd sites/[lead_id] && npm run build && wrangler pages deploy dist/
========================================
```

## Exit Criteria

- [ ] `npm run build` passed without errors
- [ ] `wrangler pages deploy` executed successfully
- [ ] Site URL shown to user
