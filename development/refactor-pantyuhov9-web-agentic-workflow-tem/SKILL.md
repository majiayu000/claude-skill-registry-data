---
name: refactor
description: Apply a named refactoring pattern to a website codebase (extract templates, centralize analytics, DRY components)
allowed-tools:
  - Bash
  - Read
  - Edit
  - Write
  - Glob
  - Grep
  - TodoWrite
model: opus
argument-hint: <pattern-name> [path to site root]
---

# Site Refactor — named refactoring patterns

You are running the `refactor` skill. Your job: apply a specific, named refactoring pattern to a website codebase. Unlike `site-audit` which diagnoses, `refactor` acts.

## Available patterns

### 1. `extract-template`
Generate a Jinja2 base template + per-page content blocks + build script. The output is still **plain .html files** — Jinja2 is build-time only, no framework migration.

**Steps:**
1. Read all HTML files, identify the shared skeleton (head, nav, analytics, footer)
2. Extract shared parts into `templates/base.html` with `{% block content %}{% endblock %}`
3. Extract analytics into `templates/partials/analytics.html`
4. Extract nav/footer into `templates/partials/nav.html` and `footer.html`
5. Create per-page templates in `templates/pages/` that extend `base.html`
6. Create `site.json` with per-page data (title, description, OG tags, course-specific data)
7. Test that `python3 tools/html_template_engine.py --templates templates/ --out . --data site.json` rebuilds identical HTML

### 2. `centralize-analytics`
Extract all analytics/tracking code (GA4, Meta Pixel, Clarity, CAPI) from individual pages into shared files.

**Steps:**
1. Identify all tracking snippets across pages (use `site-audit` findings)
2. Create `analytics-head.html` (gtag, fbq, clarity — goes in `<head>`)
3. Create `analytics.js` (event handlers, form tracking, CAPI calls)
4. Update all pages to include the shared files
5. Verify tracking IDs are consistent

### 3. `centralize-forms`
Extract form handling (form webhook, server-side event submission) into shared `form-handler.js`.

**Steps:**
1. Identify the form submission pattern duplicated across pages
2. Create `form-handler.js` with configurable data attributes (`data-course`, `data-source`)
3. Update all pages to use the shared script
4. Test form submission still works

### 4. `add-seo-basics`
Generate missing SEO files and tags.

**Steps:**
1. Generate `sitemap.xml` listing all HTML pages with their URLs
2. Generate `robots.txt` with `Sitemap:` directive
3. Add `<link rel="canonical">` to all pages
4. Add JSON-LD `Course` schema to course pages
5. Add JSON-LD `Organization` schema to index page

### 5. `add-cache-busting`
Replace manual version query strings with content-hash based cache busting.

**Steps:**
1. Compute MD5 hash of each CSS/JS file (first 8 chars)
2. Update all `<link>` and `<script>` references to use `?h=<hash>` instead of `?v=N`
3. Document the process so future changes auto-update

### 6. `optimize-images`
Add missing image attributes and flag oversized images.

**Steps:**
1. Scan all `<img>` tags for missing `width`/`height` attributes
2. Add `loading="lazy"` to below-the-fold images
3. Flag images over 200KB for manual WebP conversion
4. Report total image weight savings potential

### 7. `accessibility-fixes`
Fix mechanical accessibility issues.

**Steps:**
1. Add placeholder `alt=""` to decorative images, `alt="[REVIEW]"` to content images
2. Add `<label>` elements for all form inputs
3. Fix heading hierarchy gaps
4. Add `<main>` landmark if missing

## How to use

### Step 0 — Parse arguments
First word of `$ARGUMENTS` is the pattern name. Rest is the site root path.
Default path: current working directory (else ask for the site root).

If the pattern name is not recognized, list available patterns and STOP.

### Step 1 — Pre-flight analysis
Before any changes:
1. Read the files that will be affected (Glob + Read)
2. Count: how many files, estimated lines changed
3. **APPROVAL GATE:** Present the user with:
   - Pattern name and what it does
   - Files that will be modified
   - Preview of the first file's changes (first 20 lines of diff)
   - Estimated scope
4. Wait for explicit "go ahead" before proceeding

### Step 2 — Apply the pattern
Follow the steps listed for the chosen pattern. Make changes with Edit/Write.

### Step 3 — Verify
Run `python3 tools/site_audit.py --root "<site_root>" --mechanical-only --checks <relevant>` to confirm the finding is resolved.

Report: files modified, lines changed, findings before/after.

## Important constraints

1. **Approval gate is mandatory.** Never modify files without showing the plan first.
2. **Preserve existing functionality.** Every refactoring must produce functionally identical output.
3. **One pattern per invocation.** User can chain by re-invoking the skill.
4. **Don't force a framework.** `extract-template` uses Jinja2 as a build tool — output is plain HTML.

## See also

- [tools/site_audit.py](../../../tools/site_audit.py) — diagnostic tool
- [tools/html_template_engine.py](../../../tools/html_template_engine.py) — Jinja2 build tool
- [workflows/site_refactor.md](../../../workflows/site_refactor.md) — the SOP
