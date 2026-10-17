---
name: pre-wrap-audit
description: 12-point blind-spot assessment before session termination. Assesses core + extended fields, returns RED/YELLOW/GREEN verdict.
compatibility: |
  - Runtime: Node.js 18+ or TypeScript
  - Dependencies: None (self-contained audit framework)
---

# pre-wrap-audit — Session Termination Audit Engine

12-point blind-spot assessment before session termination. Returns RED/YELLOW/GREEN verdict for deployment gates.

## Trigger

```bash
/pre-wrap-audit [context-description]
```

## Input Schema

```typescript
interface AuditInput {
  context?: string;           // Project context or phase description
  format?: "json" | "markdown" | "summary";  // Output format
}
```

## Output Schema

```typescript
interface AuditOutput {
  status: "success" | "error";
  verdict: "RED" | "YELLOW" | "GREEN";
  blockers: string[];
  risks: string[];
  ready: string[];
  timestamp: string;
  signedOffBy: string;
}
```

---

**Full reference:** See [Skill Operator Guide](../../docs/meta/skill-operator-guide.md).

**For framework details, examples, verdict rules:** See [docs/USAGE.md](docs/USAGE.md).


