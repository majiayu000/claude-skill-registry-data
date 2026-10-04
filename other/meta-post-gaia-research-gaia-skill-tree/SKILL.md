---
name: gaia-post
description: Publish a new post (announcement, link, or LaTeX-style meta report) to the Gaia site. Use when you want to add any update to the registry's public feed and landing page.
---

# Gaia Post

Publish a post to the Gaia Skill Tree site. Posts appear in the `path-meta-queue` on the landing page and, for reports, also update the hero notification badge. All post data is tracked in `docs/meta/posts.json` (newest-first) and `docs/index.html` is patched programmatically — no hand-editing HTML.

## Post Types

| Type | When to use | Requires |
|------|-------------|----------|
| `announcement` | Registry news, version releases, policy changes | title, summary |
| `link` | External article, RFC, or resource worth surfacing | title, summary, `--url` |
| `report` | Formal audit or meta-shift (LaTeX-style HTML rendered from Markdown) | title, summary, `--source` |

## Usage

```bash
# Announcement
python scripts/add_post.py announcement "Title" "Short summary." [--label "Release"] [--date YYYY-MM-DD]

# External link
python scripts/add_post.py link "Title" "Short summary." --url https://... [--label "Link"] [--date YYYY-MM-DD]

# Meta report (renders HTML from a Markdown source file)
python scripts/add_post.py report "Title" "Short summary." \
  --source docs/meta/MY_REPORT.md \
  [--author "Name, Role"] \
  [--label "Audit"] \
  [--date YYYY-MM-DD] \
  [--chart reports/YYYY-MM-DD-chart-data.json] \
  [--hero | --no-hero]
```

**`--hero` / `--no-hero`**: controls whether the floating hero notification badge in the landing page is updated to point to this post. Defaults to yes for `report` type, no for others.

## Step-by-Step: Adding a Meta Report

### Step 1 — Write the Markdown source

Create `docs/meta/YYYY-MM-TITLE.md`. Use YAML frontmatter for metadata the script needs:

```markdown
---
title: "Registry Audit Report: Descriptive Title"
author: "Marcus Rafael Tiongson, Auditor"
summary: One sentence for the queue card.
abstract: |
  Optional longer abstract paragraph. If omitted, `summary` is used.
label: Latest Audit
---

## Abstract

Extended abstract text (rendered in the paper body as an indented italic block).

## Executive Summary

Paragraph text here.

### Sub-section

More detail.

## Findings

Tables and lists work:

| Column A | Column B |
|----------|----------|
| value    | value    |

- Bullet one
- Bullet two

## References

[1] Author. (Year). *Title*. Publisher.
[2] Another reference.
```

Supported inline Markdown: `**bold**`, `*italic*`, `` `code` ``, `[text](url)`, fenced code blocks.

### Step 2 — Run the script

```bash
python scripts/add_post.py report "Title" "Queue summary." \
  --source docs/meta/YYYY-MM-TITLE.md
```

The script will:
1. Parse the frontmatter and Markdown body.
2. Render `docs/meta/reports/YYYY-MM-DD-slug.html` using the embedded LaTeX-style academic template.
3. Prepend the new post to `docs/meta/posts.json`.
4. Patch the `<!-- gaia-posts-start / end -->` zone in `docs/index.html` (up to 3 most recent posts shown).
5. Patch the `<!-- gaia-hero-post-start / end -->` zone (hero badge) to point to the new report.

### Step 3 — (Optional) Add Chart.js timeline data

If you have a JSON data file for a timeline chart, pass it:

```bash
python scripts/add_post.py report "Title" "Summary." \
  --source docs/meta/MY_REPORT.md \
  --chart reports/my-chart-data.json
```

The JSON format mirrors `may-2026-timeline.json`:

```json
{
  "labels": ["2026-05-01", "2026-05-15", "2026-05-25"],
  "datasets": [
    { "label": "1★", "color": "#94a3b8", "data": [40, 45, 50] },
    { "label": "6★", "color": "#f59e0b", "data": [1, 1, 1] }
  ]
}
```

### Step 4 — Commit

```bash
git add docs/meta/posts.json docs/meta/reports/ docs/index.html
git commit -m "post: add <type> — <title> [skip-gen]"
```

## Constraints

- Use `Gaia Research` as the default report author unless the user explicitly requests a different byline.
- Avoid banned vocabulary from `CONTEXT.md` (apex tier, Atomic Basics, card, etc.).
- All section headings in report Markdown should use `##` (rendered with auto-numbered LaTeX counter). Use `###` for subsections.
- The `## Abstract` section in the Markdown body is rendered as the indented italic abstract block in the paper; do not repeat it under a different heading.
- The `## References` section receives special `.ref-item` treatment — each `[N] ...` line becomes a hanging-indent reference entry.
- Chart data files live in `docs/meta/reports/` alongside their HTML output.

## Example

```bash
python scripts/add_post.py report \
  "June 2026 Integrity Audit" \
  "DAG validation and evidence liveness sweep across 220 skills." \
  --source docs/meta/JUN_2026_AUDIT.md \
  --label "Audit" \
  --author "Marcus Rafael Tiongson, Auditor"
```
