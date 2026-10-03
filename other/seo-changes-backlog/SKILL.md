---
name: seo-changes-backlog
description: Maintain docs/SEO/maintenance/seo-changes-backlog.md whenever SEO-facing code, content, metadata, sitemap, schema, canonical, hreflang, redirects, IndexNow, GSC, GA4 attribution, pSEO, or blog SEO changes are made.
---

# SEO Changes Backlog

Use this skill whenever a task touches SEO-facing behavior or assets.

## File

Primary backlog:

- `docs/SEO/maintenance/seo-changes-backlog.md`

Related operational backlog:

- `docs/SEO/maintenance/gsc-request-indexing-backlog.md`

## Workflow

1. Before editing SEO surfaces, skim the latest entries in `seo-changes-backlog.md`.
2. Make the requested change and run the relevant SEO tests.
3. Add a short dated entry to `seo-changes-backlog.md` with:
   - changed surface or URLs
   - why it changed
   - files, database records, or external actions touched
   - validation performed
   - follow-up or GSC/IndexNow actions
4. If request-indexing is needed after deploy, add or update `gsc-request-indexing-backlog.md`.
5. If the backlog is getting long, summarize older detailed entries into a monthly rollup and keep recent entries detailed.

## Entry Template

```markdown
## YYYY-MM-DD

### Short Title

Source: optional report/PRD/backlog link

Changes:

- ...

Validation:

- ...

Follow-up:

- ...
```

## Keep It Useful

- Prefer concise summaries over raw commit lists.
- Link reports and PRDs instead of duplicating long analysis.
- Mention external actions explicitly: IndexNow, GSC sitemap submission, URL inspection, request-indexing backlog, GA4 admin follow-up.
- Do not mark manual GSC work complete unless the user confirms it was done.
