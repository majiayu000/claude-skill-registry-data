---
name: shipany-page-builder
description: Create new dynamic pages from a short spec (keywords, route/path, reference content).
---

# ShipAny Page Builder (Dynamic Pages)

This skill creates **new pages** using ShipAny’s **evolved dynamic page builder** approach: a page is rendered from a JSON file (per-locale).

**KEY UPDATE**: The system now supports **Automated Routing**.
- **NO** need to register routes in `index.ts`.
- **NO** need to run scripts.
- Just create the JSON file, and it's live!

## v1 edit scope (hard limit)

For v1, you may **only**:

- Add **new** multi-language dynamic page JSON files:
  - `src/config/locale/messages/en/pages/**` (new page JSON files only)
  - `src/config/locale/messages/zh/pages/**` (new page JSON files only)

22: Hard rules:

- Do **not** modify `src/config/locale/index.ts` (it is no longer needed).
- Do **not** modify any existing page JSON files (only create new ones).
- Do **not** touch routing code, layouts, components, or theme blocks.
- Do **not** add or edit any images under `public/`. **Use placeholder images in JSON only.**

## Inputs (normalize first)

Normalize the user request into:

- `route`: string (e.g. `/features/ai-image-generator`)
- `slug`: string (derived from route, e.g. `features/ai-image-generator`)
- `keywords`: string[] (3–10)
- `publishedAt`: optional string (ISO 8601) for **Scheduled Publishing** (pSEO strategies).
- `referenceCopy`: optional raw text snippets, bullets, competitor copy, or notes
- `sectionsWanted`: optional list of section keys (default: `["hero","introduce","benefits","features","faq","cta"]`)

See `references/00-guide.md`.

## Execution order

1. Normalize input + decide route/slug: `references/00-guide.md`
     - **MUST** consult `references/02-block-specs.md` for JSON block schemas.
2. Generate locale files directly:
   - Create `src/config/locale/messages/en/pages/<slug>.json`
   - Create `src/config/locale/messages/zh/pages/<slug>.json`
3. (Optional) Set `publishedAt` in metadata if user requested a scheduled release.
4. Validate build (required):
   - Build: `pnpm build`

## Scheduled Publishing (pSEO)

You can now schedule pages to go live in the future.

```json
{
  "metadata": {
    "title": "Future Page",
    "publishedAt": "2025-12-31T12:00:00Z" // Page returns 404 until this time
  },
  "page": { ... }
}
```
