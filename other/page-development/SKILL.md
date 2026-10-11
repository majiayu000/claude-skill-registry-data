---
name: page-development
description: Generate and remove route pages in `app/routes` using the template `sample-page.tsx` and automatic route wiring in `app/routes.ts`.
metadata:
  short-description: Page scaffolding workflow
---

# Page Development

## When to use
- Creating a new route page from `_template/page/sample-page.tsx`.
- Registering the new page in `app/routes.ts` without manual edits.
- Removing a previously generated page and its route entry.

## Quick start
0) Generate page:
   - `ill addPage sample-page`
   - or `ill addPage --name sample-page`
1) CLI creates `app/routes/sample-page.tsx` (name is normalized to kebab-case for file and route path).
2) CLI ensures route config supports `route(...)` helper and injects:
   - `route('sample-page', 'routes/sample-page.tsx')`
3) Remove page when needed:
   - `ill removePage sample-page`
   - or `ill removePage --name sample-page`

## What CLI edits
- `app/routes.ts`
  - Adds/removes `route('<name-kebab>', 'routes/<name-kebab>.tsx')`.
  - Adds `route` import when needed.
  - Returns import back to `index`-only if no dynamic page routes remain.
- `app/routes/<name-kebab>.tsx`
  - File is created from `_template/page/sample-page.tsx`.
  - Placeholders are renamed with case-aware replacements:
    - `SamplePage` -> `${NamePascal}`
    - `sample-page` -> `${nameKebab}`
    - `Sample Page` -> `${NamePascal}`

## Naming rules
- Recommended input: kebab-case (`faq-page`) or PascalCase (`FaqPage`).
- Result path is always kebab-case (`app/routes/faq-page.tsx`).
- Component name inside file is PascalCase (`FaqPage`).

## Final checks
- `app/routes.ts` contains exactly one route line per generated page.
- `app/routes/<name-kebab>.tsx` exists and exports a default component.
- After removal, route line and page file are both deleted.
