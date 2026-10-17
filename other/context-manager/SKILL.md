---
name: context-manager
description: Detect autonomous execution context via env var and JSON file. Prevents operator prompts during non-interactive sessions.
compatibility: |
  - Runtime: Node.js 18+
  - Dependencies: (see package.json)
---

# Context Manager

Detect and manage autonomous execution context.

## Trigger

`/skill context-manager` — invoke from gstack or CLI

## Input Schema

```typescript
interface Input {
  checkEnv?: boolean;           // check AUTONOMOUS_EXECUTION env (default: true)
  contextFile?: string;         // path to .autonomous-context.json (default: cwd)
  validate?: boolean;           // validate context freshness (default: true)
}
```

## Output Schema

```typescript
interface Output {
  status: "success" | "error";
  isAutonomous: boolean;
  context?: {
    mode: string;
    initiator: string;
    startTime: string;
    timeout?: number;
  };
  timestamp: string;
}
```

---

**Full reference:** See [Skill Operator Guide](../../docs/meta/skill-operator-guide.md).
