---
name: retro-schema-validator
description: Validate .retro/*.json files against canonical schema v1.0. Catches schema drift and type mismatches.
compatibility: |
  - Runtime: Node.js 18+
  - Dependencies: None (self-contained)
---

# Retro Schema Validator

Validate retro JSON files against canonical schema v1.0.

## Trigger

```bash
/skill retro-schema-validator [path] [options]
```

## Input Schema

```typescript
interface Input {
  filePath?: string;           // path to .retro/*.json (default: auto-detect)
  all?: boolean;               // validate all .retro/*.json (default: false)
  verbose?: boolean;           // default: false
  failOnWarning?: boolean;     // default: false
}
```

## Output Schema

```typescript
interface Output {
  status: "success" | "error";
  verdict: "RED" | "YELLOW" | "GREEN";
  filesValidated: number;
  violations: Array<{
    file: string;
    field: string;
    level: "error" | "warning";
    message: string;
  }>;
  timestamp: string;
}
```

## Exit Codes

- `0`: GREEN (schema compliant)
- `1`: YELLOW (warnings, can proceed)
- `2`: RED (schema violations, do not commit)

---

**Full reference:** See [Skill Operator Guide](../../docs/meta/skill-operator-guide.md).

**For schema definition and examples:** See [docs/USAGE.md](docs/USAGE.md).
