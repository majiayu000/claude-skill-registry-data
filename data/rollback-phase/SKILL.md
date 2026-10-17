---
name: rollback-phase
description: Revert CIC pipeline execution to a prior phase checkpoint by restoring PostgreSQL state and clearing partial vectors.
compatibility: |
  - Runtime: Node.js 18+
  - Dependencies: PostgreSQL client, Qdrant client
  - Permissions: read:checkpoints, write:database, write:vector-store
---

# rollback-phase Specification

**ID**: `rollback-phase`
**Version**: 1.0.0
**Status**: Active
**Owner**: CIC Pipeline Team

---

## Purpose

Revert CIC pipeline execution to a prior phase checkpoint by:
- Verifying checkpoint exists and is valid
- Stopping current pipeline execution
- Restoring PostgreSQL state from snapshot
- Clearing partial vectors from Qdrant
- Resuming from target phase

---

## Trigger

```
rollback-phase [target-phase]
```

---

## Input Schema

```typescript
interface SkillInput {
  targetPhase: string;      // Phase number or name (e.g., "18", "18-harvest-validation")
}
```

---

## Output Schema

```typescript
interface SkillOutput {
  status: "success" | "error";
  currentPhase: number;
  targetPhase: number;
  checkpointId: string;
  checkpointSize: string;
  checkpointTimestamp: string;
  nextAction: string;
  timestamp: string;
}
```

---

## Error Handling

See [Skill Operator Guide — Error Handling](../../docs/meta/skill-operator-guide.md#error-handling) for standard error codes.

Additional errors:

| Code | Message | Handler |
|------|---------|---------|
| `CHECKPOINT_NOT_FOUND` | Checkpoint does not exist | Verify phase number and retry |
| `CHECKPOINT_CORRUPTED` | State hash mismatch | Restore from backup checkpoint |
| `DB_RESTORE_FAILED` | PostgreSQL restore failed | Manual intervention required |

---

## Full Reference

For Setup, Requirements, Testing, Configuration, and Troubleshooting:

**→ See [Skill Operator Guide](../../docs/meta/skill-operator-guide.md)**

