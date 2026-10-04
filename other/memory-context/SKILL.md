---
name: memory-context
description: Use when you need reliable context with minimum token load through progressive disclosure.
---

# Memory Context (Progressive Disclosure)

Use this skill when you need reliable context with minimum token load.

## Goal

Fetch memory in two stages:

1. `index` stage: compact source list with stable IDs.
2. `detail` stage: only fetch selected IDs.

Each execution writes an audit record to `.metrics/memory-context-audit.jsonl`.

## Commands

### Stage 1: Index

```bash
npm run memory:context -- -Stage index
```

Optional explicit change:

```bash
npm run memory:context -- -Stage index -Change <change-id>
```

### Stage 2: Detail by IDs

```bash
npm run memory:context -- -Stage detail -Ids S001,S003
```

PowerShell array form (recommended):

```bash
powershell -ExecutionPolicy Bypass -File ./scripts/memory-context.ps1 -Stage detail -Ids S001,S003
```

## Session Evidence Metadata

When you update owner session evidence (`.trellis/workspace/<owner>/`), include:

- `Memory Sources`
- `Disclosure Level`
- `Source IDs`

These markers are required by workflow policy gate.
