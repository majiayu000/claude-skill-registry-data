---
name: obsidian-ingest-to-wiki
description: Convert one confirmed raw/ or derived/ logical source unit into concise, source-grounded curated notes in a governed Obsidian wiki/. Use when the user asks to turn source material into reusable knowledge pages.
---

# Obsidian Ingest To Wiki

1. Locate the vault root; read `AGENTS.md`, `wiki/index.md`, and the selected source. Treat a matched raw/derived pair as one logical source.
2. Determine source reliability and mark uncertain text, OCR, figures, formulas, or metadata. Use `raw/` for targeted verification when needed.
3. Extract only the claims supported by the selected source. Distinguish source facts, understanding, inference, and open questions.
4. Propose the smallest useful Wiki change: exact paths to create or modify, source anchors, internal links, index impact, and an append-only log entry only if writing succeeds.
5. Ask for independent explicit confirmation. Source selection does not authorize writing.
6. After confirmation, write only the approved `wiki/` files. Never modify `raw/` or `derived/`.
7. Verify links, source references, the exact write scope, index changes, and that the prior `wiki/log.md` content remains a prefix.

## Boundaries

- Process one logical source unit by default; ask the user to prioritize larger batches.
- Do not copy full source text or derived artifacts into Wiki pages.
- Do not promote unsupported inferences to stable facts.
- Stop and request direction when source ownership, identity, or evidence is ambiguous.
