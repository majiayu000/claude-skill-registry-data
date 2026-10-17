---
name: automation-audit
description: Read-only repo scan for automation opportunities. Identifies oversized logs, backup/archive dirs needing retention policy, and manual-step markers.
compatibility: |
  - Runtime: Node.js 18+
  - Dependencies: (see package.json)
---

# Automation Audit

Read-only repo scan for automation opportunities.

## Trigger

`/skill automation-audit` — invoke from gstack or CLI

## Input Schema

```typescript
interface Input {
  repoRoot?: string;              // default: cwd
  logSizeMB?: number;             // default: 10
  backupItemThreshold?: number;   // default: 10
  manualMarkerPattern?: string;   // regex, default: /\b(TODO|manual)\b/i
  excludeDirs?: string[];         // default: [node_modules, .git, dist, build]
}
```

## Output Schema

```typescript
interface Output {
  status: "success" | "error";
  scanTimestamp: string;
  repoRoot: string;
  totalOpportunities: number;
  byPriority: { high: number; medium: number; low: number };
  byCategory: Record<string, number>;
  opportunities: Array<{
    category: string;
    priority: string;
    path: string;
    details: string;
  }>;
}
```

---

**Full reference:** See [Skill Operator Guide](../../docs/meta/skill-operator-guide.md).

**For detailed workflow:** See [docs/USAGE.md](docs/USAGE.md).
