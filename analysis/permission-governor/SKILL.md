---
name: permission-governor
description: Auto-approve whitelisted operations to reduce operator prompts. Analyzes approval cache and identifies bottlenecks.
compatibility: |
  - Runtime: Node.js 18+
  - Dependencies: (see package.json)
---

# Permission Governor

Auto-approve whitelisted operations and analyze bottlenecks.

## Trigger

`/skill permission-governor` — invoke from gstack or CLI

## Input Schema

```typescript
interface Input {
  operation: string;            // operation to check (e.g., "read-repo")
  whitelist?: string[];         // operations to auto-approve (default: built-in)
  analyzeCalls?: boolean;       // analyze approval patterns (default: false)
}
```

## Output Schema

```typescript
interface Output {
  status: "success" | "error";
  approved: boolean;
  reason?: string;
  analysis?: {
    totalCalls: number;
    approved_count: number;
    denied_count: number;
    bottlenecks: string[];
  };
  timestamp: string;
}
```

---

**Full reference:** See [Skill Operator Guide](../../docs/meta/skill-operator-guide.md).
