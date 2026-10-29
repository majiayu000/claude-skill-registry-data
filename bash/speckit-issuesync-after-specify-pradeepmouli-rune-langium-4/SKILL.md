---
name: speckit-issuesync.after-specify
description: Sync linked issue status for after_specify hook.
compatibility: Requires spec-kit project structure with .specify/ directory
metadata:
  author: github-spec-kit
  source: templates/commands/issuesync.after-specify.md
---

# Speckit Issuesync.After-Specify Skill

<!-- Extension: workflows -->
<!-- Config: .specify/extensions/workflows/ -->
Run:

```bash
bash .specify/extensions/workflows/scripts/bash/update-linked-issue.sh --event after_specify
```
