---
name: hugo-notion-publish
description: Convert Notion pages or drafts into Hugo content for this repo, including front matter, shortcodes, glossary terms, and asset placement, and publish/preview with the Hugo CLI. Use when asked to import from Notion, format content to match FORMATTING.md, or create/update posts in content/.
---

# Hugo Notion Publish

## Overview
Turn Notion content into Hugo-ready Markdown and publish it in this site with the correct front matter, shortcodes, and assets.

## Workflow
1. Identify the target section and slug.
2. Gather metadata (title, date, tags, summary, series, author, glossary terms).
3. Pull the source content:
   - Use Notion MCP `notion-search` to locate the page if only keywords are provided.
   - Use `notion-fetch` with the page URL to retrieve properties, blocks, and assets.
   - If Notion MCP is unavailable, ask for a Markdown or HTML export.
4. Build front matter using `references/hugo-frontmatter.md`.
5. Convert Notion blocks to Hugo Markdown per `references/notion-to-hugo.md` and `FORMATTING.md`.
6. Write the file and place assets.
7. Preview or build with the Hugo CLI if requested.

## Target locations
- Blog posts: `content/posts/<slug>.md`
- Images: `static/images/<slug>/...` referenced as `/images/<slug>/file.ext`
- Other sections: `content/<section>/` (mirror front matter fields from existing entries).

## Publishing with Hugo CLI
- Preview locally: `hugo server -D`
- Production build: `hugo --gc --minify`
- Use `hugo new <section>/slug.md` only to scaffold; replace front matter with the site template and remove `draft`.

## Notion MCP helpers
- Use `scripts/notion_fetch_plan.py <notion-url>` to generate a minimal tool-call payload for `notion-fetch`.

## Formatting rules
- Shift headings down one level (Notion H1 -> `##`) so the H1 is only in front matter.
- Use `{{< term >}}`, `{{< highlight-box >}}`, `{{< collapse >}}`, and `{{< app >}}` as defined in `FORMATTING.md`.
- Keep tags lower-case and hyphenated; keep summaries to 1-2 sentences.
- When updating an existing post, preserve the filename/slug and `date`, and set `lastmod`.

## Quality checks
- Remove Notion artifacts (export headers, "Untitled", orphaned URLs).
- Ensure image paths resolve under `/images/<slug>/`.
- Summary matches the lead and is not duplicated verbatim in the first paragraph.
- Glossary terms appear in front matter or `data/glossary.yaml` when reused across posts.

## Resources
- `scripts/notion_fetch_plan.py`
- `references/hugo-frontmatter.md`
- `references/notion-to-hugo.md`
- `FORMATTING.md`
- `CLAUDE.md`
