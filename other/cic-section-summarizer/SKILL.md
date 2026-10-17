---
name: cic-section-summarizer
description: Analyze file coverage to estimate phase completion. Identifies coverage gaps and test deficits.
compatibility: |
  - Runtime: Node.js 18+
  - Dependencies: (see package.json)
---

# CIC Section Summarizer

Auto-summarize CIC phase progress and file coverage.

## Trigger

`/skill cic-section-summarizer` — invoke from gstack or CLI

## Input Schema

```typescript
interface Input {
  filePaths: string[];          // files to analyze
  phase?: string;               // optional phase name
  includeTestGaps?: boolean;    // flag files missing tests (default: true)
}
```

## Output Schema

```typescript
interface Output {
  status: "success" | "error";
  estimatedCompletion: number;
  totalFiles: number;
  filesWithTests: number;
  testGaps: string[];
  phaseSummary?: string;
  timestamp: string;
}
```

---

**Full reference:** See [Skill Operator Guide](../../docs/meta/skill-operator-guide.md).
