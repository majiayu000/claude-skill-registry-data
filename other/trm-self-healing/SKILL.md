---
name: trm-self-healing
description: DevOps self-healing triage, research escalation, and Sigil biometric guard skills
compatibility: |
  - Node.js 18+
  - Toolforge manifest runtime
---

# trm-self-healing

DevOps diagnostic and self-healing triage skills for Herdr and TRM fleets.

## Trigger

```bash
node skills/trm-self-healing/src/index.mjs
```

## Input Schema

```typescript
interface SkillInput {
  action: "triage" | "escalate" | "verify";
  errorSignature?: string;
  query?: string;
  context?: Record<string, unknown>;
}
```

## Output Schema

```typescript
interface SkillOutput {
  status: "success" | "escalated" | "blocked" | "error";
  remediation?: string;
  confidence?: number;
  runId?: string;
  timestamp: string;
}
```

---

**Full reference:** See [Skill Operator Guide](../../docs/meta/skill-operator-guide.md).

