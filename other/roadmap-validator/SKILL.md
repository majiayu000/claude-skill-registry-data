---
name: roadmap-validator
description: Validate ROADMAP.md files for sync markers, format compliance, and content integrity. Supports permissive and strict modes.
compatibility: |
  - Node.js 18+
  - TypeScript support
---

# Roadmap Validator

Validate ROADMAP.md files for sync markers and content integrity across Toolforge ecosystem.

## Trigger

```
Validate ROADMAP.md file at [path] in strict mode
```

## Input Schema

```typescript
interface SkillInput {
  roadmapPath: string;  // required: path to ROADMAP.md
  verbose?: boolean;    // optional: detailed logging (default: false)
  strict?: boolean;     // optional: fail on warnings (default: false)
}
```

## Output Schema

```typescript
interface SkillOutput {
  status: "success" | "error";
  message: string;
  data: {
    isValid: boolean;
    findings: Array<{ level: string; code: string; message: string }>;
    syncMarkersPresent: boolean;
    contentLength: number;
    validated: string;
  };
}
```

---

**Full reference:** See [Skill Operator Guide](../../docs/meta/skill-operator-guide.md). For error codes and examples: [docs/USAGE.md](docs/USAGE.md).
