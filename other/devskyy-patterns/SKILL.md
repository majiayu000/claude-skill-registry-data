---
name: devskyy-patterns
description: Coding patterns extracted from DevSkyy git history (200 commits analyzed 2026-06-10). Commit conventions, hot-surface workflows, co-change rules (CSS→.min rebuild, source→.wolf docs), and testing layout. Use when committing, editing theme assets, or onboarding a session to this repo's actual practices.
version: 1.0.0
source: local-git-analysis
analyzed_commits: 200
---

# DevSkyy Patterns

Extracted from the last 200 commits on `main`/feature branches (analyzed 2026-06-10).
These are *observed* practices — what the repo actually does, not aspirations.

## Commit Conventions

**Conventional commits, near-100% adherence.** Distribution over 200 commits:

| Type | Count | Usage |
|------|-------|-------|
| `feat` | 70 | New features, templates, pipelines |
| `fix` | 43 | Bug fixes, security findings, CI repair |
| `chore` | 27 | Deps, cleanup, .wolf/openwolf metadata |
| `docs` | 26 | Specs, brand docs, CLAUDE.md learnings |
| `refactor` | 14 | Template consolidation, DI inversions |
| `perf` | 12 | Theme asset/loading optimization |
| `style` / `test` / `ci` / `build` | rare | Used precisely, not as dumping grounds |

**Scopes are used ~50% of the time** and name the subsystem, not the file:
`(theme)` `(elite-studio)` `(v2-mockup)` `(specs)` `(deps)` `(phase0)` `(hooks)`
`(openwolf)` `(uploader)` `(plugin)` `(security)` `(render)` `(pipeline3d)`.

Pattern: `<type>(<subsystem>): <imperative description>`. Example from history:
`fix(security): resolve 7 bandit HIGH/HIGH findings blocking security CI gate`.

## Hot Surfaces (where work concentrates)

Most-changed files — treat edits here as high-blast-radius, read before writing:

1. `wordpress-theme/skyyrose-flagship/functions.php` (33 commits) — theme constants,
   includes array, bootstrap order. Almost every theme feature touches it.
2. `wordpress-theme/skyyrose-flagship/inc/enqueue.php` (17) — all CSS/JS loading,
   template-slug detection. New page CSS/JS lands here, never inline.
3. `wordpress-theme/skyyrose-flagship/style.css` (10) — version bumps ride along
   with asset changes (cache-bust via `SKYYROSE_VERSION`).
4. `assets/images/products/**` (255 directory touches) — product imagery batches;
   per-SKU folders named `<product-name>/<product-name>-<view>.<ext>`.
5. `.wolf/anatomy.md` + `.wolf/memory.md` (15 commits co-change with source) —
   OpenWolf metadata is committed WITH the change it documents, not after.

## Co-Change Rules (files that move together)

- **Theme CSS/JS source ⇄ `.min` build**: 14 of the analyzed commits change a
  source asset and its `.min` together. Production loads `.min` only — an edit
  without `node scripts/build-css.js` / `build-js.js` is inert. Never commit
  one without the other.
- **`functions.php` ⇄ `inc/<module>.php`**: new `inc/` modules are registered in
  the same commit that creates them (includes array, bootstrap order matters:
  `detection.php` → `shared.php` → builder files).
- **Fix ⇄ learning**: corrective commits carry their CLAUDE.md "Learnings" entry
  or `.wolf/cerebrum.md` entry in the same commit (project Self-Correction rule,
  visible in history as `docs+fix:` style commits).
- **Theme version bump ⇄ asset change**: `SKYYROSE_VERSION` in `functions.php` /
  `style.css` bumps alongside CSS/JS changes so the CDN cache busts.

## Workflows

### Adding a theme page/template
1. Create `template-<kind>-<slug>.php` in theme root
2. Register slug in `inc/enqueue.php` template-slug map (filename must match exactly)
3. Add page CSS to `assets/css/`, JS to `assets/js/`
4. Rebuild minified assets (`scripts/build-css.js`, `scripts/build-js.js`)
5. Bump `SKYYROSE_VERSION`; commit all of it together as one `feat(theme):`

### Adding an `inc/` module
1. Create `inc/<module>.php` with ABSPATH guard
2. Add to includes array in `functions.php` (respect bootstrap order)
3. Same commit

### Product imagery batch
- One commit per batch under `assets/images/products/<sku-folder>/`
- Reference images live in `products/_references/`, ghost-mannequin in `products/ghost/`
- Catalog truth = `data/skyyrose-catalog.csv` + per-SKU dossiers in `data/dossiers/`

### Python pipeline work
- Pipelines live in `scripts/` (e.g. `scripts/oai_render/`) and `skyyrose/elite_studio/`
- Every top-level package dir needs `__init__.py` (mypy `namespace_packages = False`)
- Format gate before commit: `isort . && ruff check --fix && black .` (line length 100)

## Testing Patterns

- Framework: **pytest**; tests mirror source domains: `tests/elite_studio/platform/`
  (19 commit-touches), `tests/pipelines/`, `tests/integration/` (integration tests
  go here, NOT `tests/api/`)
- Naming: `test_<area>_<behavior>.py` (e.g. `tests/test_p0_ssrf_replicate.py`
  shipped 20 regression tests alongside its fix — tests land in the fix commit)
- Run `pytest tests/ -v` after every change; coverage target 85%
- Use `rtk proxy pytest` for true pass/fail (bare rtk pytest output can mislead)

## Anti-Patterns (observed and corrected in history)

- Committing source CSS/JS without rebuilding `.min` → fix shipped but inert in prod
- Creating `agents/base_super_agent.py` flat file → silently shadowed by the package
- Staging auto-injected `<claude-mem-context>` CLAUDE.md churn → session noise, exclude
- Editing WC core templates instead of hooks → all WC changes via theme overrides + hooks
