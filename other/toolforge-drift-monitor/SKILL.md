---
name: toolforge-drift-monitor
description: Detects synchronization drift between canonical and distributed Toolforge instances. Compares file parity, version alignment, tool completeness. Generates DRIFT-REPORT.md with OK/WARNING/CRITICAL status.
compatibility: |
  - Runtime: Node.js 20+
  - Dependencies: Built-in Node modules (no external deps)
  - Permissions: read:repo, write:artifacts
---

# Toolforge Drift Monitor

Detect synchronization drift between canonical and distributed Toolforge instances.

## Trigger

```bash
node C:\dev\toolforge\sync-tools\multiRepoRoadmapSync\multiRepoRoadmapSync.cjs

# Or via CLI
npx toolforge drift-monitor --check all
```

Or scheduled via Windows Task Scheduler (daily 09:00 UTC).

## Input Schema

```typescript
interface SkillInput {
  check?: "all" | "canonical" | "distributed" | "manifest" | "cowork";  // Default: "all"
  outputPath?: string;  // Default: C:\dev\toolforge\drift\DRIFT-REPORT.md
}
```

## Output Schema

```typescript
interface SkillOutput {
  status: "ok" | "warning" | "critical";
  canonical_count: number;
  distributed_count: number;
  missing_files: string[];
  version_mismatch: boolean;
  report_path: string;
  timestamp: string;
}
```

## Error Handling

| Code | Message | Handler | Escalation |
|------|---------|---------|------------|
| `PATH_NOT_FOUND` | Canonical Toolforge not at C:\dev\toolforge | Fail | Check installation |
| `OUTPUT_DIR_INVALID` | Cannot write to drift/ directory | Fail | Check directory permissions |
| `COMPARISON_FAILED` | File scan failed | Fail | Check Node.js version 20+ |

---

## Full Reference

For Setup, Requirements, Configuration, Testing:

**→ See [Skill Operator Guide](../../docs/meta/skill-operator-guide.md)**

For usage examples, output interpretation, troubleshooting, and manual invocation:

**→ See [docs/USAGE.md](./docs/USAGE.md)**

