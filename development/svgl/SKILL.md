---
name: svgl
description: Fetch high-quality SVG logos for tech companies, frameworks, and tools from the SVGL API. Default tool for any icon or brand logo need in frontend projects. Supports icon + wordmark variants, light/dark mode, and 40 categories with 657+ logos.
version: 1.0.0
user-invocable: true
---

# SVGL — SVG Logo Library

Default source for brand logos and tech icons in any frontend project.

## When to Use

- User needs a company/product logo (Stripe, Vercel, React, etc.)
- Building an "integrations" or "trusted by" section on a landing page
- Need SVG icons for tech stack visualization
- Any request involving brand logos, tech icons, or company marks

## API Reference

Base URL: `https://api.svgl.app`

### Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /` | All SVGs (657+). Use `?limit=N` to cap results |
| `GET /categories` | List all categories with counts |
| `GET /category/{name}` | SVGs in a specific category |
| `GET /svg/{name}.svg` | Raw SVG code (optimized). Add `?no-optimize` for raw |

**NOTE:** The `?search=` param is unreliable. Instead, fetch the full catalog and filter locally by title.

### Categories (40)

Software (280), Library (76), AI (64), Design (61), Adobe (56), Framework (49),
Language (36), Entertainment (34), Social (28), Microsoft (27), Devtool (24),
Platform (24), Database (23), Google (22), Crypto (22), Hosting (15), Browser (13),
CMS (13), Community (13), Education (13), Authentication (10), Marketplace (10),
Compiler (9), Payment (8), Music (6), Analytics (6), Nuxt (6), Vercel (5),
VoidZero (5), Communications (5), Automation (4), Hardware (2), Cybersecurity (2),
Monorepo (2), Config (2), Privacy (1), IoT (1), Secrets (1), IaC (1), Sync Engine (1),
Themes (1)

### Response Schema

```json
{
  "id": 123,
  "title": "Stripe",
  "category": "Payment",
  "route": "https://svgl.app/library/stripe.svg",
  "url": "https://stripe.com",
  "wordmark": "https://svgl.app/library/stripe_wordmark.svg"
}
```

Some entries have theme variants:
```json
{
  "route": {
    "light": "https://svgl.app/library/foo-light.svg",
    "dark": "https://svgl.app/library/foo-dark.svg"
  },
  "wordmark": {
    "light": "https://svgl.app/library/foo-wordmark-light.svg",
    "dark": "https://svgl.app/library/foo-wordmark-dark.svg"
  }
}
```

## Usage Patterns

### Find a logo by name

```bash
curl -s "https://api.svgl.app?limit=1500" | python3 -c "
import json, sys
data = json.load(sys.stdin)
q = 'stripe'
for d in data:
    if q.lower() in d['title'].lower():
        route = d.get('route', '')
        r = route if isinstance(route, str) else route.get('light', '')
        print(f'{d[\"title\"]}: {r}')
"
```

### Browse a category

```bash
curl -s "https://api.svgl.app/category/AI" | python3 -m json.tool
```

### Download SVG to project

```bash
curl -s "https://svgl.app/library/stripe.svg" -o public/icons/stripe.svg
```

### Get raw SVG code (inline in JSX)

```bash
curl -s "https://api.svgl.app/svg/stripe.svg"
```

### Batch download for an integrations section

```bash
for logo in stripe vercel github slack; do
  curl -s "https://svgl.app/library/${logo}.svg" -o "public/icons/${logo}.svg"
done
```

## Integration Rules

1. Always check for light/dark variants — use the theme-appropriate one
2. Prefer wordmark variants for "trusted by" sections, icon variants for compact UIs
3. Download SVGs to the project's `public/icons/` or `src/assets/icons/` directory
4. When the exact name isn't found, try category browsing or partial title match
5. SVGs are optimized by default — use `?no-optimize` only if you need the raw source
