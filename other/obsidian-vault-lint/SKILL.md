---
name: obsidian-vault-lint
description: Audit a governed Obsidian raw/derived/wiki vault read-only for structure, links, source mapping, index coverage, maintenance logs, isolated notes, duplicate concepts, and unresolved claims. Use when the user requests a vault health check or repair suggestions.
---

# Obsidian Vault Lint

1. Locate the vault root and read `AGENTS.md` and `wiki/index.md`. Let stricter local rules override this skill.
2. Scan `raw/` and `derived/` shallowly for structure and source-mapping risks. Inspect `wiki/` for broken links, index coverage, source anchors, isolated pages, duplicate concepts, and contradictory maturity labels.
3. Report findings with stable IDs, severity, evidence, impact, and a suggested repair. Clearly label ambiguous items as requiring human confirmation.
4. Do not create reports or modify vault files during lint unless the user explicitly asks to save a report.
5. Wait for the user to select repair IDs. Then inspect only the affected files, show an exact repair allowlist, and wait for confirmation before changing anything.
6. Keep raw/derived repairs out of the lint repair flow; route them to the matching import workflow.

## Boundaries

- Lint is read-only by default.
- Do not run OCR, conversions, simulations, or exports.
- Do not append to `wiki/log.md` unless a confirmed repair actually succeeds.
- Do not claim a semantic inconsistency when the available evidence only establishes a possible issue.
