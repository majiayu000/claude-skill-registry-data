---
name: speckit-issuesync-before-tasks
description: Sync linked issue status for before_tasks hook.
compatibility: Requires spec-kit project structure with .specify/ directory
metadata:
  author: github-spec-kit
  source: workflows:commands/issue-sync-before-tasks.md
---

Run:

```bash
bash .specify/extensions/workflows/scripts/bash/update-linked-issue.sh --event before_tasks
```