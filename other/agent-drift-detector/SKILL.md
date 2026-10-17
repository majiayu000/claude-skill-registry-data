---
name: agent-drift-detector
description: Detect schema drift in agent messages and APIs by comparing top-level field names.
compatibility: |
  - Runtime: Node.js 18+
  - Dependencies: (see package.json)
---

# Agent Drift Detector

Detect schema drift in agent messages and APIs.

## Trigger

`/skill agent-drift-detector` — invoke from gstack or CLI

## Input Schema

```typescript
interface Input {
  agentName: string;
  expectedSchema: Record<string, unknown>;
  actualSchema: Record<string, unknown>;
}
```

## Output Schema

```typescript
interface Output {
  agentName: string;
  driftDetected: boolean;
  missingFields: string[];
  extraFields: string[];
  recommendations: string[];
}
```

---

Export: `detectDrift(input)`. Compare top-level keys only; values and nested
types do not affect drift. Empty schema objects are valid. Pilot invocation
trims agentName and rejects blank names, arrays, and unknown input fields.

**Full reference:** See [Skill Operator Guide](../../docs/meta/skill-operator-guide.md).
