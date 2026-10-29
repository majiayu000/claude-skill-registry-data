---
name: speckit-workflows-issue-sync-after-specify
description: Sync linked issue status for after_specify hook.
compatibility: Requires spec-kit project structure with .specify/ directory
metadata:
  author: github-spec-kit
  source: workflows:commands/issue-sync-after-specify.md
---

Run:

```bash
bash .specify/extensions/workflows/scripts/bash/update-linked-issue.sh --event after_specify
```