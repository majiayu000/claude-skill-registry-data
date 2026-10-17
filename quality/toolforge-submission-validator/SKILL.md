---
name: toolforge-submission-validator
description: Validates skill submissions against conformance gate (manifest, tests, docs, governance). Returns report and recommendation.
compatibility: |
  - Runtime: Node.js 18+
  - Dependencies: None
---

# Toolforge Submission Validator

Validates skill submissions before caveman review / Tier 1 approval.

## Trigger

```bash
npm run validate -- <skill-path>
```

## Input Schema

```typescript
interface ValidatorInput {
  skillPath: string;  // Absolute path to skill directory
}
```

## Output Schema

```typescript
interface ConformanceReport {
  status: "success" | "error";
  submissionId: string;
  skillId: string;
  skillVersion: string;
  checks: {
    manifestValid: boolean;
    testPass: boolean | null;
    docsComplete: boolean;
    governanceAligned: boolean;
    cavemanReview: "pending";
  };
  blockers: string[];
  recommendation: "approve" | "hold" | "reject";
  timestamp: string;
}
```

---

**Full reference:** See [Skill Operator Guide](../../docs/meta/skill-operator-guide.md).

**For check definitions, recommendation logic, examples:** See [docs/USAGE.md](docs/USAGE.md).
