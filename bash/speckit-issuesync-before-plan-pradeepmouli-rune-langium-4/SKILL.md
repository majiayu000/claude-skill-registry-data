---
name: speckit-issuesync.before-plan
description: Sync linked issue status for before_plan hook.
compatibility: Requires spec-kit project structure with .specify/ directory
metadata:
  author: github-spec-kit
  source: templates/commands/issuesync.before-plan.md
---

# Speckit Issuesync.Before-Plan Skill

<!-- Extension: workflows -->
<!-- Config: .specify/extensions/workflows/ -->
Run:

```bash
bash .specify/extensions/workflows/scripts/bash/update-linked-issue.sh --event before_plan
```
