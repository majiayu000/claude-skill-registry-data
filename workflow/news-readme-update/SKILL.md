---
name: news-readme-update
description: Use when updating src/content/*/news.md, README.md, public changelog-like notes, or site-facing update summaries.
---

# News And README Updates

## Rules

- News rows are public-facing and should be short.
- By default, News announces newly published pages only. Do not add a row for updates, additions, corrections, or new workflows on an existing page unless the owner explicitly requests an exception.
- Keep localized news entries aligned only when the owner requested localization.
- Update `updated` frontmatter when the news page changes.
- README should describe the site, not operational internals.
- Do not add promotional claims that are not reflected by the site content.

## Checks

- `npm run check:content`
- `npm run build`

## Pipeline

Part of the article pipeline in [article-authoring](../article-authoring/SKILL.md).

For a newly published page, add one row per language whose page actually exists — check the files, not whether [localization](../localization/SKILL.md) ran. Existing-page updates do not enter this step by default.

Next: [release-check](../release-check/SKILL.md).
