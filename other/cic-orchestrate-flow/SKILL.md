---
name: cic-orchestrate-flow
description: Compose CIC ingest, gate, repair, and consolidation stages into one deterministic pipeline call.
compatibility: Node.js 18+
---

# cic-orchestrate-flow Specification

## Trigger

`cic orchestrate-flow`

## Input Schema

```typescript
interface SkillInput { inputPath?: string; dryRun?: boolean; }
```

## Output Schema

```typescript
interface SkillOutput { status: "success" | "error" | "warning"; stages: string[]; errors: string[]; }
```

See the Skill Operator Guide for standard setup, errors, and testing guidance.
