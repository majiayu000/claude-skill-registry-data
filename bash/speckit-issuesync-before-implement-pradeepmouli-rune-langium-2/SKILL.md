---
name: speckit-issuesync-before-implement
description: Sync linked issue status for before_implement hook.
compatibility: Requires spec-kit project structure with .specify/ directory
metadata:
  author: github-spec-kit
  source: workflows:commands/issue-sync-before-implement.md
---

Run:

```bash
bash .specify/extensions/workflows/scripts/bash/update-linked-issue.sh --event before_implement
```