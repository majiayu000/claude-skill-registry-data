---
name: fire-card-to-epub
description: Convert FIRE analysis cards, Chinese knowledge notes, or project-note JSON into validated EPUB books with directory cards, chapter cards, keyword index cards, backlinks, and GitHub-shareable ebook assets. Use when Codex needs to teach or automate the path from `fire-analysis-card` outputs to `project-note-json-to-epub` style EPUB files, including sample JSON manuscripts and attached `.epub` deliverables.
---

# FIRE Card to EPUB

Turn FIRE analysis cards into a small validated EPUB book.

Use this skill when the user asks:

- `FIRE 卡片變成電子書`
- `把分析卡做成 EPUB`
- `教我怎麼從 FIRE 到電子書`
- `上傳 GitHub 成為技能，附上電子書檔案`
- `把 Obsidian 知識卡整理成 EPUB`

This skill bridges two workflows:

| Source Skill | Role |
|---|---|
| `fire-analysis-card` | Analyze article/note material into Fact, Index, Relation, Encyclopedia |
| `project-note-json-to-epub` | Package structured notes into EPUB with TOC, index, links, and validation |

## Core Workflow

1. Create or collect FIRE cards.
   - Each card should have a stable `code`, `title`, `body`, `keywords`, and optional `fire_card`.
   - Keep each body chunk compact: one concept per card.

2. Build a project-note JSON manuscript.
   - Use `assets/fire-to-epub-tutorial.json` as the starting schema.
   - Required top-level fields: `title`, `creator`, `language`, `chunks`.
   - Optional but recommended fields: `subtitle`, `index`, `orthogonal_check`.

3. Generate EPUB.

```bash
python3 scripts/fire_cards_to_epub.py assets/fire-to-epub-tutorial.json --out assets/fire-to-epub-tutorial.epub --download-copy assets/download.epub
```

4. Verify the output.
   - The script validates XML, href targets, anchors, backlink counts, index links, and file type.
   - Delivery is acceptable only when `errors: 0`.

5. Upload as a GitHub Skill asset.
   - Include `SKILL.md`, `scripts/fire_cards_to_epub.py`, the sample JSON, and the sample EPUB.
   - Keep the EPUB in `assets/` so users can download or inspect it from GitHub.

## JSON Schema

Minimal manuscript:

```json
{
  "title": "FIRE 卡片變成電子書",
  "creator": "Codex",
  "language": "zh-Hant",
  "chunks": [
    {
      "code": "1.1",
      "title": "FIRE 先成卡",
      "body": "正文內容。",
      "keywords": ["FIRE", "知識卡"],
      "fire_card": "可選：固定寬度 FIRE 卡文字"
    }
  ]
}
```

Recommended manuscript:

```json
{
  "title": "FIRE 卡片變成電子書",
  "subtitle": "從分析卡到 EPUB 的最小流程",
  "creator": "Codex",
  "language": "zh-Hant",
  "chunks": [
    {
      "code": "1.1",
      "title": "FIRE 先成卡",
      "body": "先把文章壓成穩定知識卡，再進入電子書結構。",
      "keywords": ["FIRE", "知識卡", "Fact"]
    }
  ],
  "index": [
    {"id": "K001", "keyword": "FIRE", "weight": 100}
  ],
  "orthogonal_check": {
    "ok": true,
    "axes": {
      "analysis_axis": "Fact、Index、Relation、Encyclopedia",
      "book_axis": "TOC、正文、索引、驗證"
    }
  }
}
```

If `index` is missing, the script derives it from `chunks[].keywords`.

## EPUB Output

The generator writes:

| EPUB File | Purpose |
|---|---|
| `mimetype` | EPUB signature, first and uncompressed |
| `META-INF/container.xml` | Rootfile pointer |
| `OEBPS/content.opf` | Metadata, manifest, spine |
| `OEBPS/nav.xhtml` | EPUB navigation |
| `OEBPS/Text/toc.xhtml` | Directory card |
| `OEBPS/Text/part001.xhtml` | Chapter/card pages |
| `OEBPS/Text/index.xhtml` | Keyword index cards |
| `OEBPS/Styles/style.css` | Readable style |

## Validation Contract

Before delivery, report:

```text
errors: 0
title: ...
all_href_count: ...
index_forward_links_tested: ...
body_return_links_tested: ...
index_entries: ...
true_body_cjk_count: ...
file type: EPUB document
```

If `errors` is not `0`, fix the JSON or generator and rebuild.

## Teaching Script

Explain the workflow to the user like this:

1. `fire-analysis-card` 把文章變成穩定知識卡。
2. 把多張 FIRE 卡整理成 `chunks[]`。
3. 從 `keywords` 建立 `K001`、`K002` 等索引卡。
4. EPUB 由三層組成：目錄卡、正文卡、書末索引卡。
5. 每個正文關鍵詞回鏈到索引卡；索引卡再連回正文。
6. 驗證所有 EPUB 連結，確認 `errors: 0`。

## Notes

- Keep EPUB attachments in `assets/`.
- Do not hand-edit generated EPUB internals after validation; fix JSON or script and rebuild.
- Use short Chinese card bodies; EPUB is a sequence of cards, not a long essay dump.
