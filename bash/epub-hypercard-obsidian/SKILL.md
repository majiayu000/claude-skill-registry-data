---
name: epub-hypercard-obsidian
description: Convert EPUB card books into Obsidian-ready HyperCard Markdown folders and portable zip files. Use when Codex needs to turn an EPUB with XHTML chapters, table-of-contents cards, keyword index cards, backlinks, Luhmann/Zettelkasten numbers, or cross-links into one Markdown file per card with verified relative links, keyword cards, previous/home/next navigation, and GitHub/shareable zip output.
---

# EPUB HyperCard Obsidian

Create an Obsidian folder from an EPUB card book. Each EPUB正文 card becomes one Markdown file. The output uses the four-table HyperCard format:

1. Luhmann/code + card title
2. Card content
3. Index-card hyperlinks
4. Previous/home/next navigation

Use this skill for EPUBs generated from project notes, Luhmann/Zettelkasten chunks, chapter cards, keyword index cards, or book-check editions that need to become clickable Obsidian Markdown.

## Quick Start

Run the generator:

```bash
python3 scripts/epub_to_hypercard_obsidian.py INPUT.epub --out OUTPUT_DIR --zip
```

Recommended portable mode:

```bash
python3 scripts/epub_to_hypercard_obsidian.py INPUT.epub --out 3.4-centaur-hypercard-obsidian-portable --zip --portable
```

The script writes:

- `index.md`: stack home and chapter directory
- `card-*.md`: one正文 card per EPUB article/chapter
- `keyword-index.md`: keyword directory
- `key-*.md`: one keyword index card per keyword
- `OUTPUT_DIR.zip`: shareable zip, when `--zip` is set

## Workflow

1. Inspect the EPUB before converting.
   - Confirm it has `META-INF/container.xml`, `OEBPS/content.opf`, XHTML text files, and a spine.
   - Treat `Text/toc.xhtml` or the first non-article spine item as the directory card.
   - Treat `Text/index.xhtml` or the XHTML with `.index-card` sections as the keyword index card.
   - Treat XHTML files with `<article>` as正文 HyperCards.

2. Generate Markdown card files.
   - Use `p.code` text for the card code, such as `3.4.1｜113字`.
   - Use `h1` as the visible card title.
   - Put body paragraphs into table 2 as one cell, separated with `<br><br>`.
   - Link keyword occurrences to `key-*.md`.
   - Keep Markdown table links as `[label](file.md)` to avoid Obsidian heading-anchor drift.

3. Generate keyword cards.
   - Parse `index.xhtml` sections into `K001`, keyword, weight, and target cards.
   - Make one `key-*.md` per keyword.
   - Add previous/home/next navigation across keyword cards.

4. Verify all links.
   - Every `[label](target.md)` must resolve to a file in the output folder.
   - Do not rely on `[[#heading]]` same-file anchors for this workflow.
   - Prefer `--portable` for sharing with AI tools, GitHub, macOS Finder, Windows, or zip upload workflows.

5. Deliver the folder and zip.
   - Give the user the output folder path and zip path.
   - Report card count, keyword count, and link verification result.

## Filename Modes

| Mode | Shape | Use |
|---|---|---|
| `--portable` | `card-3-4-1.md`, `key-k001.md` | Default recommendation for zip/GitHub/AI upload |
| no `--portable` | `3.4.1-標題.md`, `K001-關鍵字.md` | More human-readable inside Obsidian, less portable across zip tools |

## Four-Table Card Contract

```markdown
| 魯曼編號 | 卡片標題 |
|---|---|
| `{{code}}` | **{{title}}** |

| 內容 |
|---|
| {{content_with_links}} |

| 索引 |  |  |  |
|---|---|---|---|
| {{keyword_link_1}} | {{keyword_link_2}} | {{keyword_link_3}} | {{keyword_link_4}} |

| ← 上一張 | Card {{n}} / {{total}} | 下一張 → |
|---|---|---|
| {{previous_card}} | [Home](index.md) | {{next_card}} |
```

## Link Rules

- Use relative Markdown file links: `[TARS](key-k001.md)`.
- Do not use Obsidian alias wikilinks inside tables, because `[[target|alias]]` contains `|` and can break table columns.
- Do not use same-file heading anchors for card navigation when the user wants a folder or zip.
- Escape Markdown table pipes in extracted text as `\|`.

## Validation Output

Before finishing, run or report the script validation:

```text
cards: ...
keywords: ...
missing_links: 0
zip: ...
```

If `missing_links` is not zero, fix the generated links or parser before delivery.
