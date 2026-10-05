---
name: vault-governance
description: Use when working inside a governed Obsidian vault, before reading or editing notes, topic folders, registries, workflow docs, or canonical knowledge. Applies when the vault uses RULES.md, registry files, layered knowledge zones, or multiple agents and models that must share one operating protocol.
---

# Vault Governance

## Overview

Use this as the entry skill for any governed vault. Its job is to align the agent before work starts: find the rule source, determine the target layer, check write authority, and decide whether the task is intake, curation, promotion, audit, or archive.

If your agent supports MCP, 优先 connect the vault governance MCP server.
Use this skill as the compatibility layer when MCP is unavailable.

## First Pass

1. Read `RULES.md`
2. Read the nearest adapter file if present: `CLAUDE.md`, `AGENTS.md`, or `GEMINI.md`
3. Read `.knowledge-registry/vault-registry.json`
4. Identify the target `topic_id`
5. Identify the target `kb_layer`
6. Check whether your role can write there

## Layer Decision

| Layer | Typical content | Default action |
|------|------------------|----------------|
| `system` | rules, schemas, workflows, registries | edit rarely, log always |
| `intake` | raw sources, imported data, NotebookLM outputs | capture or normalize |
| `curation` | reorganized notes, draft synthesis, topic indexes | curate or propose |
| `canonical` | long-lived knowledge, stable topic summaries | propose unless Hermes/human |
| `archive` | frozen or retired material | archive only with authority |

Read `references/layer-model.md` when the folder layout is ambiguous.

## Routing

- Raw inputs, source landing, imported artifacts -> use `$vault-intake-curation`
- Candidate stable knowledge or canonical update -> use `$vault-canonical-promotion`
- Drift, duplicates, missing metadata, registry mismatch -> use `$vault-audit-repair`
- Merge, canonical decision, archive decision under Hermes -> use `$hermes-coordination`

## Required Behavior

- Do not treat `ProjectRaw/` or other intake zones as canonical by default.
- Do not write directly to canonical knowledge unless your role explicitly allows it.
- Do not skip registry lookup when topic identity matters.
- Record important changes in `change-ledger.jsonl`.

## Red Flags

- "This is just a simple note edit"
- "I probably know the right folder"
- "I can update canonical and skip proposal"
- "Registry updates can wait until later"

All of these mean: stop and re-run the first pass.

## Common Mistakes

- Reading `CLAUDE.md` but not `RULES.md`
- Choosing folder by intuition instead of `topic_id`
- Updating content without logging the change
- Promoting working notes straight into canonical
