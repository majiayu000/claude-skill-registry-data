---
name: scaffold
description: One-shot a new product — folders, Next.js starter, product.config.json, CLAUDE.md, scope.md, PRD skeleton, SETUP.md checklist. The Lovable-like ignition.
---

# /scaffold

Usage: `/scaffold "<slug>" "<one-liner>"`

Example: `/scaffold "formpad" "A form builder for indie SaaS founders that auto-generates schema from prompts."`

## What this does

Creates a complete starting point for a new product:

1. **Folder structure** at `products/<slug>/`:
   ```
   products/<slug>/
   ├── product.config.json
   ├── CLAUDE.md
   ├── scope.md
   ├── prd.md
   ├── metrics.md (skeleton, fill in via metric-framework-designer later)
   ├── SETUP.md (the one-time setup checklist)
   ├── README.md
   ├── decisions/
   │   └── 0001-scaffold.md
   ├── interviews/
   │   └── README.md
   ├── launch/
   │   └── README.md
   ├── analytics/
   │   └── README.md
   └── code/ → symlink or new Next.js app (see step 2)
   ```

2. **Next.js starter** — copies `templates/product-starter-nextjs/` to `products/<slug>/code/` with the name, slug, and one-liner substituted into:
   - `package.json` (name)
   - `.env.example` (NEXT_PUBLIC_APP_NAME)
   - `src/app/(marketing)/page.tsx` (hero copy)
   - `src/app/layout.tsx` (default metadata)
   - `next.config.mjs` (if needed)
   - `README.md`

3. **product.config.json** — the dashboard registry entry:
   ```json
   {
     "slug": "<slug>",
     "name": "<Title Case Name>",
     "one_liner": "<one-liner>",
     "created": "<ISO date>",
     "stage": "idea",
     "status": "scaffolded",
     "code_path": "products/<slug>/code",
     "aliases": [],
     "analytics": {
       "stripe_account_id": null,
       "posthog_project_id": null,
       "ga4_measurement_id": null,
       "plausible_domain": null,
       "sentry_org": null,
       "sentry_project": null,
       "gsc_property": null,
       "ahrefs_target": null
     },
     "links": {
       "github": null,
       "prod_url": null,
       "staging_url": null
     }
   }
   ```

4. **CLAUDE.md** in the product folder — uses `templates/claude-md-template.md` with substitutions.

5. **scope.md** — uses `templates/scope-doc-template.md`, with Claude's first-pass fill from the one-liner. User edits in next session.

6. **PRD skeleton** — uses `templates/prd-template.md`, Claude pre-fills sections that can be inferred from the one-liner; rest are clearly marked TODO.

7. **SETUP.md** — the exact 11-step setup checklist from `stack/analytics-stack.md`, with the product's specific URLs for service signups pre-filled.

8. **First decision log entry** in `decisions/0001-scaffold.md`:
   ```
   ## YYYY-MM-DD — Scaffolded
   Created via /scaffold. One-liner: "<one-liner>".
   Stage: idea. Stack: default per stack/tech-stack.md.
   Next: complete SETUP.md, run /validate <slug>.
   ```

## What you do as the assistant when this is invoked

1. Parse `<slug>` and `<one-liner>` from the user's invocation.
2. Validate slug: lowercase, hyphens only, no spaces. If invalid, ask for correction.
3. Validate uniqueness: error if `products/<slug>/` exists.
4. **VALIDATION GATE**: Unless the user said "skip validation" or explicitly the user already has validation evidence (cite the source: e.g. `products/<slug>/validation/snapshot.md` from a prior `/validate` run), ask: "I don't see validation evidence for this product. Are you sure you want to scaffold before validating? (yes / run /validate first)"
5. If user proceeds: create folder structure, copy template, do the substitutions.
6. Generate the doc skeletons by reading the templates and filling from the one-liner.
7. Print the SETUP.md checklist as the final message so the user knows the manual steps remaining.
8. Print "next: run `pnpm install && pnpm dev` in products/<slug>/code/ — landing page should boot at localhost:3000".

## Edge cases
- If `templates/product-starter-nextjs/` doesn't exist yet, scaffold the doc files only and tell the user to wait for the starter (Phase C of this build pass).
- If user provides only `<slug>` without `<one-liner>`, ask for the one-liner once. Don't proceed without it.
