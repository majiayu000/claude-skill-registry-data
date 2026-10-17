---
name: rewrite-labs-orchestrator
description: Orchestrates multi-stage development pipelines. Analyzes stage statuses, calculates completion %, identifies blockers, suggests next steps.
compatibility: |
  - Runtime: Node.js 18+
  - Dependencies: None
---

# Rewrite Labs Orchestrator

Analyzes pipeline stage statuses, calculates completion percent, identifies blockers, and suggests next execution steps.

## Trigger

```bash
npm run orchestrate -- pipeline.json
```

## Input Schema

```typescript
interface PipelineInput {
  stages: Array<{
    id: string;
    status: "pending" | "in-progress" | "completed" | "blocked";
    blocker?: string;
  }>;
}
```

## Output Schema

```typescript
interface PipelineOutput {
  status: "success" | "error";
  completionPercent: number;
  blockedStages: string[];
  nextSteps: string[];
  timestamp: string;
}
```

---

**Full reference:** See [Skill Operator Guide](../../docs/meta/skill-operator-guide.md).
