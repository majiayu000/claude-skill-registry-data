---
name: renderers
description: "Office-document renderers for pursuit deliverables — Markdown to DOCX (Pandoc/OpenXML) and JSON envelopes to styled XLSX (openpyxl). USE WHEN the user asks to export a Studio markdown file to Word, convert compliance matrix JSON to Excel, render proposal outline as DOCX, or run a one-off format conversion on files under pursuits/. Consumer skills (proposal-generator, subcontractor-sow-builder, compliance-auditor) call these scripts internally; users can also run renderers directly from Agent Skills or chat. DO NOT USE FOR drafting content (use proposal-generator), visual decks/PDF/PPTX (use huashu-design), or domain analysis."
license: MIT
metadata:
  title: Renderers
  category: acquisition-deliverables
  status: active
  origin: theseus
  invoke: agent
  runtime: legacy
  supports_llm: false
  upstream: govcon-capture-vibe/.github/skills/renderers
---

# Renderers — DOCX + XLSX utility

## Capture-insights adapter

- **DOCX:** `scripts/render_docx.py` — Pandoc on PATH or OpenXML fallback via `python-docx`
- **XLSX:** `scripts/render_xlsx.py` — requires `openpyxl` in the project venv
- **Run** from Agent Skills, chat ("export executive summary to Word"), or automatically after proposal-generator

PDF / PPTX / MP4 → route to `huashu-design`, not here.

## CLI examples

```bash
python skills/renderers/scripts/render_docx.py --input path/to.md --output path/to.docx --toc
python skills/renderers/scripts/render_xlsx.py --input envelope.json --output matrix.xlsx --title "Compliance"
```