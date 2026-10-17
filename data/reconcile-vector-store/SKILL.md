---
name: reconcile-vector-store
description: Verify Qdrant vector store is in sync with PostgreSQL extraction state by comparing counts and optionally re-indexing missing vectors.
compatibility: |
  - Runtime: Node.js 18+
  - Dependencies: PostgreSQL client, Qdrant client
  - Permissions: read:database, read:vector-store, write:vector-store
---

# reconcile-vector-store Specification

**ID**: `reconcile-vector-store`
**Version**: 1.0.0
**Status**: Active
**Owner**: CIC Pipeline Team

---

## Purpose

Compare vector store with PostgreSQL extraction state:
- Check mode: Detect drift and report status
- Repair mode: Re-index missing vectors from PostgreSQL

---

## Trigger

```
reconcile-vector-store [check | repair]
```

---

## Input Schema

```typescript
interface SkillInput {
  mode: "check" | "repair";  // Required. check (default) or repair
}
```

---

## Output Schema

```typescript
interface SkillOutput {
  status: "success" | "error";
  mode: string;
  postgresRecords: number;
  qdrantVectors: number;
  driftCount: number;
  driftPercentage: number;
  syncTimestamp: string;
  operationDuration: string;
  timestamp: string;
}
```

---

## Error Handling

See [Skill Operator Guide — Error Handling](../../docs/meta/skill-operator-guide.md#error-handling) for standard error codes.

Additional errors:

| Code | Message | Handler |
|------|---------|---------|
| `DRIFT_DETECTED` | Vector store out of sync (check mode only) | Run repair mode or investigate |
| `REPAIR_FAILED` | Re-indexing failed | Check PostgreSQL availability |

---

## Full Reference

For Setup, Requirements, Testing, Configuration, and Troubleshooting:

**→ See [Skill Operator Guide](../../docs/meta/skill-operator-guide.md)**

