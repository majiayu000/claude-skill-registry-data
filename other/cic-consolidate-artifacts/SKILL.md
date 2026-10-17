---
name: cic-consolidate-artifacts
description: Consolidate artifacts from multiple sources and verify integrity. Supports strict and lenient validation modes.
compatibility: |
  - Node.js 18+
---

# CIC Consolidate Artifacts

Consolidate and verify CIC artifacts across pipeline stages.

## Trigger

```
Consolidate CIC artifacts in [mode] mode
```

## Input Schema

```typescript
interface SkillInput {
  sources: string[];          // artifact source paths
  mode?: "strict" | "lenient"; // default: "strict"
}
```

## Output Schema

```typescript
interface SkillOutput {
  status: "success" | "error";
  manifest: {
    sourceCount: number;
    artifactCount: number;
    validationErrors: Array<{ source: string; error: string }>;
  };
  verified: boolean;
  timestamp: string;
}
```

---

**Full reference:** See [Skill Operator Guide](../../docs/meta/skill-operator-guide.md).
