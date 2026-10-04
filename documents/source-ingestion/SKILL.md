---
name: source-ingestion
description: "Execute Phase 1.5 of authoring: convert approved source files (PDF, ePUB, DOCX, HTML, Markdown) into canonical Markdown with assets, anchors, metadata, conversion reports, and manifest updates. Use after sources are selected and rights-cleared, before interrogation, to produce the canonical source layer the rest of the pipeline reads."
---

# Skill: source-ingestion

**Purpose:** Execute Phase 1.5 — convert approved source files into canonical Markdown with
assets, anchors, metadata, reports, and manifest updates.

---

## Input

- Source file path or URL
- Target subagent slug
- Optional metadata overrides: title, author, year, rights_status, authority, volatility

---

## Steps (in order)

1. **Preserve original** — copy to `sources/original/<source_id>/original.<ext>`
2. **Compute SHA-256** — via `generate_metadata.py`
3. **Detect file type** — via `detect_file_type.py`
4. **Choose converter** — PDF→Docling/MarkItDown, ePUB→Pandoc/MarkItDown, DOCX→Pandoc/MarkItDown, HTML→readability/Pandoc, Markdown→passthrough
5. **Convert to canonical Markdown** — write to `sources/markdown/<source_id>.md`
6. **Extract assets** — base64 data URIs → `sources/assets/<source_id>/`
7. **Inject source anchors** — headings, tables, figures, code blocks → HTML comments + JSONL
8. **Generate metadata JSON** — `sources/metadata/<source_id>.metadata.json`
9. **Generate conversion report** — `sources/reports/<source_id>.conversion-report.md`
10. **Assign conversion status** — `ok | needs-human-review | needs-ocr | failed`
11. **Update source-pack manifest** — `source-pack.manifest.yaml`
12. **Create human-review queue entry** — when status != ok → append to `sources/reports/human-review-queue.md`

---

## Conversion status rules

| Condition | Status |
|-----------|--------|
| No errors, content extracted | `ok` |
| Scanned/image-only PDF detected | `needs-ocr` |
| URL requires login | `needs-auth` |
| Converter returned errors | `failed` |
| Low content yield, possible quality issue | `needs-human-review` |

---

## Output

All files created under `subagents/<slug>/sources/`.

Returns:
- `source_id`
- `conversion_status`
- `anchor_count`
- `asset_count`
- `markdown_path`
