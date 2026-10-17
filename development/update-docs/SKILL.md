---
name: update-docs
description: Generate docs/ markdown documentation from real source code; no site generator lock-in
argument-hint: "[scope]"
related:
  - check-should-update
  - follow-single-of-source
  - check-monorepo
  - deep-review-codebase
  - check-reference
  - reframe
  - update-references
  - update-vitepress-docs
  - create-report-in-dot-devin
  - watch-browser

---

## Goal

Create the `docs/` directory in plain markdown — readable on GitHub or any markdown viewer without a site generator, nav config, or complex UX. For a VitePress docs site, use `/update-vitepress-docs`.

## Scope

- Set up `docs/` for a single project and for a monorepo
- Create/update markdown with real content from the source code
- `docs/index.md` is the table of contents linking to every section — no nav/sidebar config
- Supports `update-features-md` (workflow `features-md`) with a separate `project/features` page
- Reuse raw findings that skills persist under `.devin/temp/report/<workspace>/` via `/create-report-in-dot-devin` — e.g. `/deep-test website`, `/watch-browser fix` — as input for updating docs

## Execute

### 1. Prepare

> Goal: Identify the project type, distribution type, and docs scope

1. Run `/check-should-update` if there are git changes
2. Run `/check-monorepo` to detect a monorepo
3. Determine the docs type per the detection in `references/<type>.md` — the file structure varies by project shape:
   - `lib`/`library`: has `exports`/`main`+`types`, no `bin`; users install via a package manager — `references/library.md`
   - `sdk`: client library for a service/API (has a client entry, `*_URL`/`*_KEY` env) — `references/sdk.md`
   - `tool`: dev/internal tool, toolkit, generator, runner (serves developers/CI, not end users) — `references/tool.md`
   - `cli`: has `bin` or a CLI framework in `package.json` — `references/cli.md`
   - `website`: deployable web app (framework + `dev`/`build` output) — `references/website-guide.md`
   - `open-source`: no auth, open license — `references/open-source.md`
   - `opensource-product`: OSS that is an end-user product (app/framework/platform with releases + community) — `references/opensource-product.md`
   - `product`: has auth, `private: true`, commercial license — `references/product.md`
   - `saas-product`: hosted SaaS (dashboard, billing, multi-tenant) — `references/saas-product.md`
   - `monorepo`: layered on the base type — `references/monorepo.md`
4. Read `package.json` to identify the project type (CLI, Library, Web, Product) — if CLI, use the `cli` docs type; if published as a package, use the `library` docs type; if a deployable web app, use the `website` docs type

### 2. Ensure Docs Structure

> Goal: Have a base directory structure for markdown docs

0. `Generated-docs detection`: If `.gitignore` lists `docs/` or `docs/` contains generated markers (`manifest.json`, `sources.json`, build output) — `docs/` is generated output; un-ignore only project-owned paths in `.gitignore` (`docs/*` + `!docs/index.md` + `!docs/<section>/`) and write project docs only to committable paths — never write under generated dirs
1. Create `docs/` at the root (always, not `apps/docs/`)
2. Do not create `docs/.vitepress/` — site config is in the scope of `/update-vitepress-docs`
3. Create the page structure:
   - `docs/index.md`
   - `docs/project/overview.md`
   - `docs/project/features.md`
   - `docs/getting-started/quickstart.md`
   - `docs/getting-started/installation.md`
   - `docs/getting-started/usage.md`
   - `docs/development/setup.md`
   - `docs/development/architecture.md`
   - `docs/development/workflows.md`
   - `docs/development/testing.md`
   - `docs/development/deployment.md`
   - `docs/development/troubleshooting.md`
   - `docs/references/`
   - `docs/roadmap/index.md`
   - extensibility sections (per the project's real content): `docs/guides/index.md` + `docs/guides/<topic>.md`, `docs/examples/index.md` + `docs/examples/<name>.md`, `docs/integrations/index.md`, `docs/plugins/index.md`, `docs/adapters/index.md`, `docs/ecosystem/index.md` — create only sections that have real content, never empty placeholders; a section without a directory must not be linked from index/nav/sidebar
4. For a monorepo, add `docs/project/workspaces.md` and `docs/workspaces/<name>.md`
5. Add type-specific pages from `references/<type>.md`, e.g. `docs/commands/` for `cli`, `docs/references/contributing.md` for `open-source`, `docs/references/auth.md` + `admin.md` + `pricing.md` for `product` (no dedicated template; fall back to `templates/content-page.md`), `references/api.md` + `comparison.md` + `glossary.md` for `library`, `references/endpoints.md` + `errors.md` for `sdk`, `operations/` for `saas-product`, `guides/` for `opensource-product`

### 3. Write Index TOC

> Goal: `docs/index.md` navigates to every section with plain markdown links

1. Use `templates/docs-index.md` — title, short description, link list grouped by section
2. Order sections by the page groups in `references/<type>.md`
3. Use relative links (e.g. `project/overview.md`) — supports direct reading on GitHub

### 4. Write Content Pages

> Goal: Content from real data in the project

1. Every page uses its dedicated template from `templates/index.md` — fall back to `templates/content-page.md` only for pages without a dedicated template
2. `project/overview.md`: use `templates/overview.md` — summarize the project, architecture, tech stack, key concepts
3. `project/features.md`: use `templates/features.md` — list all features from `update-features-md` or analysis
4. `getting-started/quickstart.md`: use `templates/quickstart.md` — the shortest path, <5min
5. `getting-started/installation.md`: use `templates/installation.md` — installation steps, dependency checks
6. `getting-started/usage.md`: use `templates/usage.md` — real usage examples
7. `development/setup.md`: dev environment setup
8. `development/architecture.md`: use `templates/architecture.md` — architecture, conventions, boundaries
9. `development/workflows.md`: use `templates/workflows.md` — slash commands, scripts, CI/CD
10. `development/testing.md`: use `templates/testing.md` — how to run tests, lint, typecheck + `## Latest Results` from real runner artifacts under `.devin/temp/report/<workspace>/` (Vitest `vitest-*.json`/`unit-test-*.md`, Playwright `playwright-*.json`/`e2e-*.md`, `coverage-*`) — never put exploratory results (`browser-test-*`, `e2e-exploratory-*`, `uxui-*`) in Latest Results; if there are no artifacts, write only the commands/runners part
11. `development/deployment.md`: use `templates/deployment.md` — pipeline, secrets, rollback
12. `development/troubleshooting.md`: use `templates/troubleshooting.md` — symptom → fix
13. `references/`: summarize references with their dedicated templates — `api.md`/`configuration.md`/`changelog.md`/`faq.md`/`glossary.md`/`security.md`/`performance.md`/`migration.md`/`comparison.md` use the same-named template; the open-source type adds `contributing.md` with `templates/contributing.md`; the product type adds `auth.md` with `templates/auth.md`; the cli type adds `commands/<name>.md` with `templates/commands.md`
14. `project/decisions/NNNN-*.md`: use `templates/adr.md` — one ADR per decision when architecture choices are non-obvious
15. `roadmap/index.md`: use `templates/roadmap.md` — summarize the roadmap (Now/Next/Later)
16. monorepo: `workspaces/<name>.md` uses `templates/workspace.md`

### 5. Integrate `update-features-md`

> Goal: The existing-features page is accurate

1. If invoked by `/update-features-md`, feature data comes from routes/modules/schemas/API
2. Write `docs/project/features.md` as a markdown table
3. Each row has name, description, module, status
4. Group by domain with headings or sub-sections
5. No dropdowns; use plain headings and bullets

### 6. Content Quality

> Goal: Content is readable, consistent, and non-duplicative

1. Run `/deep-review-codebase`
2. Check heading structure, frontmatter, links
3. Fix duplication or placeholders
4. ≤ ~150 lines per page — if longer, split into sub-pages and link them from index

### 6b. Drift Check

> Goal: Docs do not lag behind the code

1. Compare `project/features.md` + `references/api.md` against the real source — `package.json` exports/scripts, `src/` modules, routes
2. Any row absent from the code → delete or mark `deprecated`; a new module without a row → add one
3. Compare commands in docs with `package.json` scripts — never teach a command that doesn't exist
4. staleness: add `> Last verified: <YYYY-MM-DD>` at the end of pages with frequently changing data (features, api, changelog)

### 7. Update References

> Goal: Links are not broken

1. Run `/update-references`
2. Check internal links between pages in `docs/` and links in `docs/index.md` — verify every link resolves to a real file (e.g. use `Select-String` to find `](` and compare against the file listing; no broken links)
3. Update the README to link to the docs

### Doc Skills

> Goal: Dispatch per-file markdown docs work to the more detailed skill

| Domain | Topic | Skill |
|--------|-------|-------|
| `agents-md` | Create/update root + workspace `AGENTS.md` | `/update-agents-md` |
| `contributing-md` | Create/update `CONTRIBUTING.md` | `/update-contributing` |
| `features-md` | Analyze features and write `FEATURES.md` | `/update-features-md` |
| `readme-md` | Create `README.md` + `LICENSE.md` from a template | `/update-readme-md` |
| `todo-md` | Manage `TODO.md` (add/read/enhance prompt) | `/update-todo-md` |
| `usage-md` | Create/update `USAGE.md` from real code | `/update-usage-md` |

## Rules

### 1. Markdown Only

- Write content in plain markdown
- Never create HTML reports, interactive tables, or complex UX
- Tables may use markdown tables
- No Vue components or generator-specific syntax — pages must render correctly on GitHub

### 2. Docs Index

- `docs/index.md` must link to every real section, ordered per `references/<type>.md`
- Use relative links to `.md` files (e.g. `project/overview.md`) — no site-generator-style paths (`/project/overview`)
- Other pages link back to `index.md` or related pages with relative links when needed

### 3. Frontmatter

- Every markdown file must have frontmatter:
  ```yaml
  ---
  title: Page Title
  description: Short description
  ---
  ```
- title uses Title Case
- description ≤ 120 characters
- optional keys: `since: <version>` (new API), `deprecated: <version>` — use when docs specify the API surface

### 4. Feature Tables

- `docs/project/features.md` uses the table `| Feature | Description | Module | Status |`

### 5. Language

- Markdown content uses the project's language or English
- Never mix languages within the same paragraph

### 6. No Workspace Duplicates

- A monorepo creates a single `docs/` at the root
- Never create `docs/` inside each workspace
- Workspace pages live at `docs/workspaces/<name>.md`

### 7. Real Data

- Content must come from real source code
- Examples must run
- No placeholders or lorem ipsum
- Use /run-docs if needed
- Use /deep-review-codebase if needed
- Use /check-reference if needed
- Use /reframe if needed
- Use `/follow-single-of-source` if needed


## Expected Outcome

- A `docs/` directory at the root with markdown pages for every section
- `docs/index.md` is a TOC linking every page, directly readable on GitHub
- `docs/project/features.md` has a features table from `update-features-md`
- `docs/roadmap/index.md` has Now/Next/Later from `templates/roadmap.md`
- Every file has frontmatter
- No HTML/complex UX or site-generator-specific syntax
- Links are correct and unbroken
- README updated with links to the docs
