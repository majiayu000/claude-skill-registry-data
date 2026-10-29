---
name: speckit-issuesync.after-implement
description: Sync linked issue status for after_implement hook.
compatibility: Requires spec-kit project structure with .specify/ directory
metadata:
  author: github-spec-kit
  source: templates/commands/issuesync.after-implement.md
---

# Speckit Issuesync.After-Implement Skill

<!-- Extension: workflows -->
<!-- Config: .specify/extensions/workflows/ -->
Run:

```bash
bash .specify/extensions/workflows/scripts/bash/update-linked-issue.sh --event after_implement
```
