---
name: speckit-issuesync.after-tasks
description: Sync linked issue status for after_tasks hook.
compatibility: Requires spec-kit project structure with .specify/ directory
metadata:
  author: github-spec-kit
  source: templates/commands/issuesync.after-tasks.md
---

# Speckit Issuesync.After-Tasks Skill

<!-- Extension: workflows -->
<!-- Config: .specify/extensions/workflows/ -->
Run:

```bash
bash .specify/extensions/workflows/scripts/bash/update-linked-issue.sh --event after_tasks
```
