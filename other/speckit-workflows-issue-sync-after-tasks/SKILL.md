---
name: speckit-workflows-issue-sync-after-tasks
description: Sync linked issue status for after_tasks hook.
compatibility: Requires spec-kit project structure with .specify/ directory
metadata:
  author: github-spec-kit
  source: workflows:commands/issue-sync-after-tasks.md
---

Run:

```bash
bash .specify/extensions/workflows/scripts/bash/update-linked-issue.sh --event after_tasks
```