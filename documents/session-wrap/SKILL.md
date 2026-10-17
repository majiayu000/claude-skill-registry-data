---
name: session-wrap
description: Atomic session wrap-up engine. Writes doc updates, stages scoped files, creates prefixed commits, generates summary reports.
compatibility: |
  - Runtime: Node.js 18+
  - Dependencies: Node.js fs, child_process (git)
---

# Session Wrap — Session Termination Commit Engine

Orchestrate four session-end tasks: write doc updates, stage relevant changes, create prefixed atomic commit, generate summary report.

## Trigger

```bash
npm run wrap -- --commitMessage "[claude] Session complete" --summary "Documentation updated"
```

## Input Schema

```typescript
interface WrapInput {
  commitMessage: string;    // Must start with [claude]|[copilot]|[gemini]|[human]
  summary?: string;         // Session summary for report
  docUpdates?: Array<{ path: string; content: string }>;
  stageFiles?: string[];    // Additional paths to stage (beyond docUpdates)
  stageAll?: boolean;       // Default false; true = git add -A
  dryRun?: boolean;         // Preview without modifying git
}
```

## Output Schema

```typescript
interface WrapOutput {
  status: "success" | "error";
  commitHash: string | null;
  docUpdates: Array<{ path: string; status: string }>;
  stagedFiles: string[];
  skippedCommit: boolean;
  report: { summary: string; checklistItems: string[]; nextSteps: string[] };
  timestamp: string;
}
```

---

**Full reference:** See [Skill Operator Guide](../../docs/meta/skill-operator-guide.md).

**For v1.1.0 changes, collision fixes, worked examples:** See [docs/USAGE.md](docs/USAGE.md).
