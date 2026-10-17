---
name: pre-flight-test-checker
description: Validate test environment before `npm test`. Checks ESLint config, external fixtures, platform compliance, and test assertions.
compatibility: |
  - Runtime: Node.js 18+
  - Dependencies: None (self-contained)
---

# Pre-Flight Test Checker

Validate test environment assumptions before running `npm test`.

## Trigger

```bash
/skill pre-flight-test-checker [options]
```

## Input Schema

```typescript
interface Input {
  repoRoot?: string;           // default: cwd
  verbose?: boolean;           // default: false
  failOnWarning?: boolean;     // default: false (RED on blockers only)
}
```

## Output Schema

```typescript
interface Output {
  status: "success" | "error";
  verdict: "RED" | "YELLOW" | "GREEN";
  checks: Array<{
    name: string;              // e.g., "ESLint Config"
    level: "error" | "warning" | "pass";
    message: string;
    details?: string[];
  }>;
  timestamp: string;
  readyToTest: boolean;
}
```

## Exit Codes

- `0`: GREEN (ready to test)
- `1`: YELLOW (warnings, can proceed with caution)
- `2`: RED (blockers, do not run tests)

---

**Full reference:** See [Skill Operator Guide](../../docs/meta/skill-operator-guide.md).

**For examples and troubleshooting:** See [docs/USAGE.md](docs/USAGE.md).
