---
name: speckit-issuesync.after-plan
description: Sync linked issue status for after_plan hook.
compatibility: Requires spec-kit project structure with .specify/ directory
metadata:
  author: github-spec-kit
  source: templates/commands/issuesync.after-plan.md
---

# Speckit Issuesync.After-Plan Skill

<!-- Extension: workflows -->
<!-- Config: .specify/extensions/workflows/ -->
Run:

```bash
bash .specify/extensions/workflows/scripts/bash/update-linked-issue.sh --event after_plan
```
