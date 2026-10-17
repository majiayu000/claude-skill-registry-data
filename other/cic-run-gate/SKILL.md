---
name: cic-run-gate
description: Execute CIC validation gate across pipeline stages. Validates dependencies, generates conformance reports with pass/warn/fail verdicts.
compatibility: |
  - Node.js 18+
  - Python 3.10+ (for adapter)
---

# CIC Run Gate

Run CIC validation gate and generate conformance report.

## Trigger

```
Run CIC gate with [scope] scope
```

## Input Schema

```typescript
interface SkillInput {
  scope?: "full" | "partial" | "single-stage";  // default: "full"
  format?: "verbose" | "summary";               // default: "summary"
}
```

## Output Schema

```typescript
interface SkillOutput {
  status: "success" | "error";
  verdict: "PASS" | "WARN" | "FAIL";
  report: {
    stagesValidated: number;
    failedChecks: Array<{ stage: string; check: string; error: string }>;
    remediationSteps: string[];
  };
  timestamp: string;
}
```

---

**Full reference:** See [Skill Operator Guide](../../docs/meta/skill-operator-guide.md).
