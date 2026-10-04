---
name: movemental-pdf
description: Collate a movement leader's docs/voice and docs/themes into one professionally styled PDF deliverable using WeasyPrint. Use when exporting themes+voice for a leader, generating movement leader PDFs, or applying the movemental-pdf workflow.
---

# Movemental PDF

Collate `docs/voice/` + `docs/themes/` for a movement leader and produce a styled PDF. Built on the [[pdf-ebook]] WeasyPrint pipeline.

## Invocation

```
/movemental-pdf {leader-slug} [--output /path/to/file.pdf]
/movemental-pdf --all [--output-dir ~/Desktop]
```

## Prerequisites

A leader is **export-ready** when both exist with at least one `.md` file each:

- `docs/voice/{SLUG}_VOICE.md` (or any `*.md` in `docs/voice/`)
- `docs/themes/CORE_THEMES.md`

Run from the leader repo root or pass `--repo-root`.

## Collation order

1. **Cover** — leader display name, subtitle "Voice & Themes", generation date
2. **Part I — Voice** — `docs/voice/*.md` (single file expected)
3. **Part II — Core Themes** — `docs/themes/CORE_THEMES.md`
4. **Part III — Theme Deep Dives** — every other `docs/themes/*.md`, sorted by YAML `theme_order` (fallback: order in CORE_THEMES table, then filename)

Insert a page-break H1 before each part and each theme deep-dive.

## Process

1. **Discover** — confirm export-ready; list files; extract display name from first H1 or voice filename
2. **Run script** — execute `scripts/build_themes_voice_pdf.py` (do not reinvent inline unless debugging)
3. **Report** — output path, page count, files included

```bash
python3 .cursor/skills/movemental-pdf/scripts/build_themes_voice_pdf.py \
  --repo-root . \
  --output ~/Desktop/{Leader-Name} — Voice & Themes.pdf
```

Batch:

```bash
python3 .cursor/skills/movemental-pdf/scripts/build_themes_voice_pdf.py \
  --scan-root /path/to/movement-leader-websites \
  --output-dir ~/Desktop
```

## Styling

Matches pdf-ebook defaults: US Letter, 1in margins, Georgia 11pt body, sans-serif headings, running header/footer with page numbers. Do not paraphrase or edit source markdown — collation only.

## Dependencies

`weasyprint`, `markdown`, `pyyaml`. Install: `pip3 install weasyprint markdown pyyaml`

## Additional resources

- WeasyPrint/CSS details: [reference.md](reference.md)
