---
name: cic-repair-pipeline
description: Detect and repair broken stages in the CIC processing pipeline by diagnosing failures and applying automatic or manual remediation.
compatibility: |
  - Runtime: Node.js 18+
  - Dependencies: PostgreSQL client, CIC pipeline orchestrator
  - Permissions: read:pipeline, write:pipeline, write:manifest
---

# cic-repair-pipeline Specification

**ID**: `cic-repair-pipeline`
**Version**: 1.0.0
**Status**: Active
**Owner**: CIC Pipeline Team

---

## Purpose

Detect and repair broken pipeline stages by:
- Scanning stage for failures and diagnostics
- Applying automatic repairs or generating reports
- Restoring stage manifest and validating readiness

---

## Trigger

```
cic repair-pipeline --stage=STAGE --mode=MODE
```

---

## Input Schema

```typescript
interface SkillInput {
  stage: string;              // Required. Pipeline stage identifier (e.g., "INGEST", "EXTRACT")
  mode: "auto" | "manual";    // Required. auto: repair, manual: report only
}
```

---

## Output Schema

```typescript
interface SkillOutput {
  status: "success" | "error" | "warning";
  stage: string;
  diagnostics: string[];
  repairAttempted: boolean;
  repairSucceeded: boolean;
  manifestRestored: boolean;
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
| `STAGE_NOT_FOUND` | Pipeline stage does not exist | Verify stage identifier |
| `REPAIR_FAILED` | Automatic repair could not fix issue | Switch to manual mode for report |
| `MANIFEST_CORRUPTED` | Stage manifest is invalid | Manual intervention required |

---

## Full Reference

For Setup, Requirements, Testing, Configuration, and Troubleshooting:

**→ See [Skill Operator Guide](../../docs/meta/skill-operator-guide.md)**

