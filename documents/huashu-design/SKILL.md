---
name: huashu-design
description: "HTML-as-medium design for hi-fi prototypes, pitch decks, and motion exports (PPTX/PDF). USE WHEN the user asks for a one-pager, pitch deck, visual deck, capture deck, export deck to PDF or PowerPoint, or HTML visuals from pursuit intel. Builds numbered slide HTML under pursuits/{slug}/05_visuals/ and exports via vendored Node scripts (export_deck_pdf.mjs, export_deck_pptx.mjs). DO NOT USE FOR Word/Excel office docs (use renderers) or proposal prose (use proposal-generator)."
metadata:
  title: Huashu Design
  category: visuals-decks
  status: active
  origin: huashu-design
  invoke: agent
  runtime: tools
  supports_llm: true
  max_turns: 20
  upstream: alchaincyf/huashu-design
compatibility: Node, Chromium/Playwright for export scripts when active
---

# Huashu Design

## Capture-insights adapter (no KG)

- **Run** from Agent Skills — builds `05_visuals/one_pager.html` from pursuit artifacts.
- Writes `one_pager.html` + numbered `01_title.html` … deck slides from proposal-generator templates.
- PDF via `export_deck_pdf.mjs`; editable PPTX via `export_deck_pptx.mjs` + `html2pptx.js`.
- **Toolchain:** `cd skills/huashu-design && npm install` (playwright, pptxgenjs, sharp).

Visual output skill — consumer skills hand off content; this skill owns HTML + export.