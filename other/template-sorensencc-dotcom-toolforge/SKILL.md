---
name: [skill-id]
description: [1–2 sentence summary of what operator will achieve]
compatibility: |
  - Runtime: Node.js 18+
  - Dependencies: [list key ones]
  - Permissions: read:repo, write:artifacts
---

# [Skill Name] Specification

**ID**: `[skill-id]`
**Version**: 0.1.0
**Status**: [Active|Experimental]
**Owner**: [Team]

---

## Purpose

[Copy "What it does" from README.md or expand slightly]

---

## Trigger

Exact prompt that invokes this skill:

```
[Full user-facing trigger text]
```

---

## Input Schema

```typescript
interface SkillInput {
  input1: string;           // Required. [Description]
  verbose?: boolean;        // Optional. Enable debug output
}
```

---

## Output Schema

```typescript
interface SkillOutput {
  status: "success" | "error";
  message: string;
  data?: Record<string, any>;
  timestamp: string;
}
```

---

## Error Handling

See [Skill Operator Guide — Error Handling](../../docs/meta/skill-operator-guide.md#error-handling) for standard error codes.

Additional errors:

| Code | Message | Handler |
|------|---------|---------|
| `CUSTOM_ERROR` | Description | Action |

---

## Full Reference

For Setup, Requirements, Configuration, Testing, Troubleshooting, and Integration:

**→ See [Skill Operator Guide](../../docs/meta/skill-operator-guide.md)**

For workflow examples and deep integration patterns:

**→ See [docs/USAGE.md](./docs/USAGE.md)**
