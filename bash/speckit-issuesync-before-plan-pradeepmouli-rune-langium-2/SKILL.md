---
name: speckit-issuesync-before-plan
description: Sync linked issue status for before_plan hook.
compatibility: Requires spec-kit project structure with .specify/ directory
metadata:
  author: github-spec-kit
  source: workflows:commands/issue-sync-before-plan.md
---

Run:

```bash
bash .specify/extensions/workflows/scripts/bash/update-linked-issue.sh --event before_plan
```