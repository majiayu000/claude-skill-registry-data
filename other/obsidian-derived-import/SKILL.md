---
name: obsidian-derived-import
description: Import readable, processed, OCR, extracted, or preview artifacts into a governed Obsidian vault derived/ area after they are matched to one raw/ source. Use when the user provides artifacts prepared outside the vault.
---

# Obsidian Derived Import

1. Locate the vault root and read `AGENTS.md`, `wiki/index.md`, and the relevant `raw/` layout.
2. Match every candidate artifact to exactly one raw source using paths, names, metadata, or content identifiers. Mark uncertain matches for manual confirmation.
3. Mirror the raw source's relative category under `derived/` when practical. Treat derived content as rebuildable, not authoritative.
4. Show the exact source-artifact mapping, targets, collision policy, and expected package files. Do not copy yet.
5. Ask for explicit confirmation.
6. After confirmation, copy only the approved artifacts. Verify the reported scope and preserve the raw source unchanged.
7. Report what was imported, what remained uncertain, and any limitations of the readable representation.

## Boundaries

- Never modify `raw/`.
- Do not create Wiki notes or update `wiki/index.md` or `wiki/log.md`.
- Do not fabricate missing metadata or infer a source mapping as certain.
- Do not generate conversions, OCR, or exports unless that was separately requested and approved.
