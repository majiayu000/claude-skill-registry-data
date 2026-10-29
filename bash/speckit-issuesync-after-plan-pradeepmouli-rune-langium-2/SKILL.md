---
name: speckit-issuesync-after-plan
description: Sync linked issue status for after_plan hook.
compatibility: Requires spec-kit project structure with .specify/ directory
metadata:
  author: github-spec-kit
  source: workflows:commands/issue-sync-after-plan.md
---

Run:

```bash
bash .specify/extensions/workflows/scripts/bash/update-linked-issue.sh --event after_plan
```