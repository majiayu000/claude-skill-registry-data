---
name: scaffold
disable-model-invocation: true
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
   ├── validation/
   │   └── README.md (the validation ledger — gates `bun run check-validation`)
   ├── interviews/
   │   └── README.md
   ├── launch/
   │   └── README.md
   ├── analytics/
   │   └── README.md
   └── (NO code/ here — see step 2: product code lives in its OWN sibling repo)
   ```

   **Layout rule (hard):** `products/<slug>/` in Hamzaish is **metadata only**
   (markdown + `product.config.json` + the folders above). A product's actual code
   lives in its **own repo outside Hamzaish**, registered in gitignored
   `code-paths.local.json`. Never create `products/<slug>/code/` (or `src/`, `app/`,
   `dist/`…) with real source — Hamzaish is always public and nothing excludes it from
   commits. `bun run check-product-layout` enforces this; see
   `brain/anti-patterns/product-code-inside-factory-repo.md`.

2. **Code repo — a SIBLING repo, NOT inside Hamzaish.** Create the product's code in
   its own directory outside this repo (e.g. `~/Claude/<Name>`), `git init` it there
   (no remote yet if held local → add a `.no-auto-push` marker), then register it:
   add `"<slug>": "/abs/path/to/<Name>"` to `code-paths.local.json` (gitignored) and
   keep `code_path: null` in `product.config.json` (path-portability rule). For a web
   product, seed that sibling repo from `templates/product-starter-nextjs/` with the
   name, slug, and one-liner substituted into:
   - `package.json` (name)
   - `.env.example` (NEXT_PUBLIC_APP_NAME)
   - `src/app/(marketing)/page.tsx` (hero copy)
   - `src/app/layout.tsx` (default metadata)
   - `next.config.mjs` (if needed)
   - `README.md`
   - `.gitleaks.toml`, `SETUP.md` ({{PRODUCT_NAME}} / {{PRODUCT_SLUG}} placeholders)
   - `.devcontainer/devcontainer.json` ({{PRODUCT_NAME}} placeholder)

   The starter is **secure-by-default** — the copy already brings `.gitignore`
   (`.env*` ignored, `!.env.example` tracked), the committed `.env.example`
   placeholder, the `secret-scan.yml` gitleaks workflow, `.gitleaks.toml`, the
   `.githooks/pre-commit` hook, and a `.devcontainer/` (Node + Bun) so builds run
   in an isolated container instead of on the bare host. See "Secure-by-default"
   below for the scaffold-time steps the template can't carry on its own.

3. **product.config.json** — the dashboard registry entry:
   ```json
   {
     "slug": "<slug>",
     "name": "<Title Case Name>",
     "one_liner": "<one-liner>",
     "created": "<ISO date>",
     "stage": "idea",
     "status": "scaffolded",
     "code_path": null,
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
4. **VALIDATION GATE**: Seed `products/<slug>/validation/README.md` from `products/_template/validation/README.md`, then run `bun run check-validation <slug>`. If it exits non-zero (state `unvalidated`), tell the user: "No validation evidence for this product. Run `/validate <slug>` first, or — if you're choosing to build first — I'll set the ledger to `debt-accepted` and record why." Building first is allowed; building first **silently** is not. Only proceed once the ledger reflects reality (`validated`, `in-progress`, or `debt-accepted`).
5. If user proceeds: create folder structure, copy template, do the substitutions.
6. Generate the doc skeletons by reading the templates and filling from the one-liner.
7. **Apply the secure-by-default steps** (section below).
8. Print the **local-first promise**: the scaffold runs with ZERO config — no accounts, no env vars. `bun install && bun dev` boots it in local mode (dev-auth stub, SQLite-ready, integrations off). SETUP.md is the *go-live* checklist for later, not a prerequisite — surface it as "when you're ready to ship," never as "do this first."
9. Print "next: **open the product's code repo (the path you registered in `code-paths.local.json`) in its devcontainer** — VS Code → 'Reopen in Container' (or `devcontainer up`). The container installs deps and runs the dev server in isolation; the landing page boots at localhost:3000 (port-forwarded out of the container) **with zero accounts** — build first, wire your stack when you deploy. Building on the bare host instead is at your own risk."

## Secure-by-default

Every scaffolded product ships secure from commit zero. Most of this rides in via
the template copy; a few steps must run at scaffold time.

- **Secrets gitignored** — verify the copied `.gitignore` ignores `.env`, `.env.*`,
  `*.env.local` and re-includes `!.env.example`. Only the placeholder
  `.env.example` is tracked; real secrets go in `.env.local` (local) or Vercel
  project settings (prod), never the repo.
- **Conversations gitignored** — verify the copied `.gitignore` carries the
  "Conversations / chat transcripts / strategy & discussion notes" block (prose
  `.md`/`.txt` patterns). Our conversations/strategy/discussion **never** belong in a
  product repo — that context lives in local memory. The block is a backstop; the
  guarantee is discipline. (A machine-wide `~/.config/git/ignore` net mirrors it.)
- **Secret-scan CI included** — `.github/workflows/secret-scan.yml` (gitleaks,
  pinned action, `permissions: contents: read`) + `.gitleaks.toml` come with the
  template. Confirm they landed in the product's code repo.
- **Devcontainer ships in the template** — `.devcontainer/devcontainer.json` +
  `Dockerfile` (Node + Bun, non-root, workspace-only mount, no host secret/SSH
  passthrough) ride in via the copy. Confirm they landed, and **tell the user to
  open the product in the container** ("Reopen in Container" in VS Code, or
  `devcontainer up`) so the agent and all build/install commands run isolated from
  the host. Running on the bare host is at the operator's own risk.
- **`.no-auto-push` marker** — create it at scaffold time so wip auto-commits stay
  local until `/ship`: `touch <code-repo>/.no-auto-push` (in the sibling code repo). (It's gitignored
  by design — operator-local discipline — so the template can't carry it across a
  fresh clone; the scaffold step must add it.)
- **Production-branch deploy** — note in the product's `SETUP.md` / decision log:
  Vercel **Production Branch must be set to `production`** (Project → Settings →
  Git). Deploys happen only via `/ship` (promote reviewed commits to `production`).
  `main`/working-branch pushes should be Preview, not Production.
- **RLS-on reminder** — surface it: every Supabase table holding user data needs
  `enable row level security` + a policy in `supabase/migrations/`. The starter
  migration is the place to set the habit; flag it in the final message.
- Tell the user they can run `/security-check <slug>` any time to audit all of the
  above, and that `/ship` runs it as a gate before every deploy.

## Edge cases
- If `templates/product-starter-nextjs/` doesn't exist yet, scaffold the doc files only and tell the user to wait for the starter (Phase C of this build pass).
- If user provides only `<slug>` without `<one-liner>`, ask for the one-liner once. Don't proceed without it.
