---
name: third-party-repo-auditor
description: Audits third-party Git repositories against upstream remotes for pending commits, tags, and patch status.
compatibility: |
  - Runtime: PowerShell 7+ (pwsh) or Windows PowerShell 5.1+
  - Dependencies: Git CLI on PATH
  - Permissions: read:repo, read:network
---

# Third-Party Repository Auditor

Audits third-party Git repositories across the workspace against upstream remotes for pending updates, release tags, and local dirty state.

## Trigger

```powershell
pwsh -NoProfile -File C:\dev\skills\third-party-repo-auditor\src\audit.ps1

# Or via Toolforge runner
pwsh -NoProfile -File C:\dev\run-tool.ps1 -Tool third-party-repo-auditor
```

## Input Schema

```typescript
interface SkillInput {
  Repositories?: string[]; // Optional repository paths. Default: standard 3rd-party list
  Fetch?: boolean;         // Whether to fetch upstream refs before comparison. Default: true
  Json?: boolean;          // Output structured JSON. Default: false
}
```

## Output Schema

```typescript
interface SkillOutputItem {
  Repository: string;
  Path: string;
  Remote: string;
  Branch: string;
  Commit: string;
  Status: "UP_TO_DATE" | "BEHIND_UPSTREAM" | "AHEAD_OF_UPSTREAM" | "DIRTY";
  Behind: number;
  Ahead: number;
  LatestTag: string;
  DirtyFiles: number;
  LastCommitMessage: string;
}
```

## Error Handling

| Code | Message | Handler | Escalation |
| :--- | :--- | :--- | :--- |
| `GIT_NOT_FOUND` | Git CLI is not on PATH | Fail | Verify Git installation |
| `REMOTE_UNREACHABLE` | Upstream network fetch timed out | Warning | Run with `-Fetch:$false` |
| `REPO_NOT_FOUND` | Target path is missing | Skip | Validate repository path list |

---

## Full Reference

For Setup, Requirements, Configuration, and Testing:

**→ See [Skill Operator Guide](../../docs/meta/skill-operator-guide.md)**
