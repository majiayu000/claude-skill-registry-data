---
name: site-audit
description: Full site crawl and audit using existing site-audit scripts. Checks every public and authenticated route for errors, broken links, missing content, accessibility. Use when user says /site-audit, "crawl the site", "check all pages", "find broken pages", or before a major release.
---

# SITE-AUDIT (Full Site Crawl)

## Purpose

Systematically visit every route and check for problems. Uses existing scripts.

## Procedure

### Phase 1: Generate Manifest

```bash
node scripts/site-audit-manifest.mjs
```

This produces a list of all routes to check.

### Phase 2: Run Audit

```bash
node scripts/site-audit-runner.mjs
```

If scripts are broken/outdated, fall back to Playwright crawl:

1. Start from homepage
2. Follow every link
3. For each page, check:
   - HTTP status (200, not 404/500)
   - No console errors
   - No layout breaks (viewport overflow)
   - Key content renders (not blank pages)
   - Images load (no broken img)
   - Forms have labels
   - Buttons are clickable

### Phase 3: Categorize Findings

| Severity | Meaning                                        | Action           |
| -------- | ---------------------------------------------- | ---------------- |
| CRITICAL | 500 errors, auth bypass, data exposure         | Fix immediately  |
| HIGH     | Broken features, dead buttons, missing content | Fix before ship  |
| MEDIUM   | Layout issues, missing labels, slow loads      | Queue for polish |
| LOW      | Minor visual, nice-to-have improvements        | Note and move on |

### Phase 4: Report

```
## Site Audit [date]

Pages crawled: X
- Clean: Y
- Issues: Z

### Critical
| Page | Issue | Details |
|------|-------|---------|

### High
| Page | Issue | Details |
|------|-------|---------|

### Summary
- Auth routes: X/Y working
- Public routes: X/Y working
- API routes: X/Y responding
```

### Phase 5: Quick Fixes

- Fix all CRITICAL issues immediately
- Fix HIGH issues if < 30 min total work
- Queue MEDIUM/LOW to build queue

## Constraints

- Never modify page content during audit (read-only pass)
- Use agent account for authenticated routes
- Don't audit external links (only internal routes)
- Max crawl time: 10 minutes (skip remainder if exceeded)
