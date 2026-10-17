---
name: active-work-overview
description: Aggregates active pull requests, recent landings, git worktrees, open backlog items, mobile ingress receipts, and daemon health into a structured report.
compatibility:
  node: ">=20.0.0"
  git: ">=2.40.0"
---

# Active Work Overview

## Trigger
Use this skill when asked to:
- "what items do we have today"
- "give me a status overview"
- "what work is currently in progress"
- "show active PRs and worktrees"
- "run active-work-overview"

## Input Schema
```yaml
workspaceRoot:
  type: string
  required: false
  default: "C:\\dev"
  description: Root development directory to inspect
json:
  type: boolean
  required: false
  default: false
  description: When true, emits structured JSON instead of Markdown
```

## Output Schema
```yaml
markdown:
  type: string
  description: Complete GitHub-Flavored Markdown report with tables and links
data:
  type: object
  properties:
    timestamp: { type: string }
    pullRequests: { type: array }
    recentLandings: { type: array }
    worktrees: { type: array }
    todos: { type: array }
    outboxReceipts: { type: array }
    telemetry: { type: object }
```

## Usage

### 1. Markdown Report (Default)
```bash
node C:\dev\skills\active-work-overview\src\overview.mjs
```

### 2. JSON Mode
```bash
node C:\dev\skills\active-work-overview\src\overview.mjs --json
```

### 3. Verification & Testing
```bash
node --test C:\dev\skills\active-work-overview\tests\overview.test.mjs
```

---

**Reference:** See [Skill Operator Guide](../../docs/meta/skill-operator-guide.md).
