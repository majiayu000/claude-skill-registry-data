---
name: speckit-workflows-issue-sync-before-specify
description: Sync linked issue status for before_specify hook.
compatibility: Requires spec-kit project structure with .specify/ directory
metadata:
  author: github-spec-kit
  source: extension:workflows
---

# Workflows Issue Sync Before Specify Skill

Run:

```bash
bash .specify/extensions/workflows/scripts/bash/update-linked-issue.sh --event before_specify
```
