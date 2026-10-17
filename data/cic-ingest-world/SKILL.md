---
name: cic-ingest-world
description: Ingest external data sources into CIC pipeline and register in lineage graph. Supports full re-ingest and delta modes.
compatibility: |
  - Node.js 18+
---

# CIC Ingest World

Ingest worlds/sources into CIC pipeline with lineage tracking.

## Trigger

```
Ingest world from [uri] in [mode] mode
```

## Input Schema

```typescript
interface SkillInput {
  uri: string;               // required: source URI (s3://, file://, etc)
  mode?: "full" | "delta";   // optional: default "full"
}
```

## Output Schema

```typescript
interface SkillOutput {
  status: "success" | "error";
  manifest: {
    uri: string;
    mode: string;
    recordsIngested: number;
    lineageEntry: string;
  };
  timestamp: string;
}
```

---

**Full reference:** See [Skill Operator Guide](../../docs/meta/skill-operator-guide.md).
