---
name: speckit-issuesync.before-specify
description: Sync linked issue status for before_specify hook.
compatibility: Requires spec-kit project structure with .specify/ directory
metadata:
  author: github-spec-kit
  source: templates/commands/issuesync.before-specify.md
---

# Speckit Issuesync.Before-Specify Skill

<!-- Extension: workflows -->
<!-- Config: .specify/extensions/workflows/ -->
Run:

```bash
bash .specify/extensions/workflows/scripts/bash/update-linked-issue.sh --event before_specify
```
