---
name: hook-validator
description: Audit pre-commit hook chain for completeness, order-independence, and sequencing. Prevents installer race conditions.
compatibility: |
  - Runtime: Node.js 18+ or PowerShell 7+
  - Dependencies: None (self-contained)
---

# Hook Validator

Audit pre-commit hook shim for completeness and order-independence.

## Trigger

```bash
/skill hook-validator [options]
```

## Input Schema

```typescript
interface Input {
  hookPath?: string;           // default: .git/hooks/pre-commit
  verbose?: boolean;           // default: false
  strict?: boolean;            // default: false (warn on partial, fail on missing)
}
```

## Output Schema

```typescript
interface Output {
  status: "success" | "error";
  verdict: "RED" | "YELLOW" | "GREEN";
  checks: Array<{
    name: string;              // e.g., "Shim Completeness"
    level: "error" | "warning" | "pass";
    message: string;
    details?: string[];
  }>;
  expectedHooks: string[];
  foundHooks: string[];
  timestamp: string;
}
```

## Exit Codes

- `0`: GREEN (hook chain healthy)
- `1`: YELLOW (partial/warnings)
- `2`: RED (broken chain, cannot commit safely)

---

**Full reference:** See [Skill Operator Guide](../../docs/meta/skill-operator-guide.md).

**For examples and incident history:** See [docs/USAGE.md](docs/USAGE.md).
