---
name: plan-extractor-integration
description: Unified entry point for CodeFlow extraction into CIC stores. Extracts metadata from CodeFlow analyzers into the central CIC store.
compatibility: |
  - Runtime: Node.js 18+
  - Dependencies: CodeFlow SDK, CIC store client
---

# Plan Extractor Integration

Extracts node, edge, pattern, security, and impact metadata from CodeFlow analyzers into the central CIC store.

## Trigger

```bash
npm run extract -- [analysis-path]
```

## Input Schema

```typescript
interface ExtractionInput {
  analysisPath: string;      // Path to CodeFlow analysis output
  storeConfig?: {
    endpoint?: string;
    authToken?: string;
  };
}
```

## Output Schema

```typescript
interface ExtractionOutput {
  status: "success" | "error";
  factsWritten: number;
  store: {
    nodes: number;
    edges: number;
    patterns: number;
  };
  timestamp: string;
}
```

---

**Full reference:** See [Skill Operator Guide](../../docs/meta/skill-operator-guide.md).
