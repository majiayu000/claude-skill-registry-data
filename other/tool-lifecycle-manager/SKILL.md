---
name: tool-lifecycle-manager
description: Enforce Toolforge governance rules for tool classification, versioning, status transitions, deployment readiness checks.
compatibility: |
  - Runtime: Node.js 18+ or PowerShell
  - Dependencies: manifest.json reader, semantic version parser
---

# Tool Lifecycle Manager

Validates tool registrations and enforces governance rules from GOVERNANCE.md.

## Trigger

```bash
toolforge-validate-tool -Name toolName -Action readiness-check
toolforge-validate-registry -Action full-audit
```

## Input Schema

```typescript
interface LifecycleInput {
  action: "readiness-check" | "full-audit" | "status-transition";
  toolName?: string;
  newStatus?: string;     // For status-transition
}
```

## Output Schema

```typescript
interface LifecycleOutput {
  status: "success" | "error";
  result: "PRODUCTION_READY" | "BLOCKED" | "WARNINGS" | "PASS";
  blockers?: string[];
  warnings?: string[];
  checks: {
    classification: boolean;
    versioning: boolean;
    manifest: boolean;
    documentation: boolean;
    tests: boolean;
  };
  timestamp: string;
}
```

---

**Full reference:** See [Skill Operator Guide](../../docs/meta/skill-operator-guide.md).

**For governance rules, quality gates, status transitions, examples:** See [docs/USAGE.md](docs/USAGE.md).

