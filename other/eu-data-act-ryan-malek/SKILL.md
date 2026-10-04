---
name: data-act-ryan-malek
description: EU Data Act (Regulation (EU) 2023/2854) skill for lawyers. Use when the user asks about Data Act classification, drafting, lookup, analysis, or audit. Triggers include "Data Act", "Regulation 2023/2854", "connected product", "related service", "data processing service", "DPS switching", "Article 3(2) pre-contract", "Article 25 contract", "trade-secret handbrake", "international government access", "Chapter VI cloud switching", "Article 50 timeline", "FAQ Q22a", "data holder", "exportable data", "functional equivalence", "Art. 4(10) competing product", and similar EU Data Act phrases. The skill produces lawyer-style Word output and cites verbatim from bundled regulation and FAQ source texts.
metadata:
  author: "Ryan Malek"
  license: "agpl-3.0"
  version: "2026-05-12"
---

1. Read `references/method.md`, `references/gotchas.md`, and `references/house-style.md` before answering.
2. When you need facts from the lawyer to proceed (mode, side advised, sector, timing, etc.), use the `AskUserQuestion` tool to present multiple-choice options as a clickable panel. Batch related questions into one call. Only fall back to plain-text A/B/C/D if `AskUserQuestion` is unavailable in the current client.
3. To answer a regulation or FAQ question, search `assets/source/regulation-2023-2854.md` (headings: `## Article N`, `## Recital N`) or `assets/source/faq-v1.4.md` (headings: `## FAQ Q[N|Na]`). Quote verbatim. Never paraphrase from memory; if the provision is not in the source files, report a skill defect.
4. To produce a drafting starter, fill the relevant template in `assets/templates/` (see `assets/templates/README.md`). Do not rewrite templates.
5. For depth on specific topics, read `references/trade-secret-ladder.md`, `references/art-13-unfair-terms.md`, `references/gdpr-overlay.md`, or `references/sectoral-overlays.md` only when relevant.
6. After the chat answer, offer Word export via `scripts/render_docx.py`. The script appends the disclaimer footer.
