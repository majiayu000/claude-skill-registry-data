---
name: monadvault-codex-keeper
description: "Organize messy notes, scrolls, protocols, practices, symbolic writing, project lore, and long-running knowledge into retrievable codex structure. Use when a Steward asks to make a codex entry, turn notes into a protocol, build a glossary or index, connect related writings, preserve project lore, extract repeatable practices, classify fragments, or structure knowledge without flattening its original voice."
---

# MonadVault Codex Keeper

## Overview

Use this skill to preserve living knowledge without flattening it. Codex Keeper turns raw Steward material into structured entries, protocols, indexes, and retrieval maps while keeping uncertainty and provenance visible.

## Routing

- Use this skill to shape and connect knowledge artifacts.
- Use `monadvault-vault-memory-curator` when the main question is whether, where, and how long material should be remembered.
- Use `monadvault-ritual-researcher` when the work requires cultural provenance, symbolic comparison, or a practice map across sources.

## Workflow

1. Read for structure before rewriting. Identify thesis, recurring terms, protocols, symbols, entities, decisions, and unresolved questions.
2. Preserve the original register where it matters. Do not over-normalize poetic, ritual, or symbolic language into generic business prose.
3. Classify the artifact:
   - scroll or essay
   - protocol or practice
   - glossary or ontology
   - project lore
   - decision record
   - fragment requiring later synthesis
4. Produce the smallest useful codex object:
   - entry if the material has one center
   - protocol if it contains repeatable steps
   - index if the material mainly connects other pieces
   - glossary if terms are the durable value
5. Add retrieval metadata: tags, related entries, prerequisites, audience, privacy posture, and update questions.

## Output Contract

Return:

- `Codex title`
- `Artifact type`
- `Core statement`
- `Structured entry`
- `Key terms`
- `Protocol steps` when applicable
- `Relations`
- `Open questions`
- `Retrieval tags`
- `Privacy note`

Use [codex-entry-template.md](references/codex-entry-template.md) when the user wants an entry they can retain.

## Guardrails

- Do not invent canon. Mark inferred relationships as inferred.
- Keep private, sacred, or personally identifying material scoped for the Steward unless publication is explicitly requested.
- Ask before compressing extensive source material into a final canonical form.
- Preserve contradictions when they are part of the record.
