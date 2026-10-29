---
name: speckit-workflows-issue-sync-before-specify
description: Sync linked issue status for before_specify hook.
compatibility: Requires spec-kit project structure with .specify/ directory
metadata:
  author: github-spec-kit
  source: workflows:commands/issue-sync-before-specify.md
---

Run:

```bash
bash .specify/extensions/workflows/scripts/bash/update-linked-issue.sh --event before_specify
```