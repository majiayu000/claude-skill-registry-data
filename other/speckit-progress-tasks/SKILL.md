---
name: speckit-progress-tasks
description: 'Hook: mark the tasks phase active on the dashboard card'
compatibility: Requires spec-kit project structure with .specify/ directory
metadata:
  author: github-spec-kit
  source: progress:commands/tasks.md
---

## Dashboard — enter `tasks` (lifecycle hook)

The `before_tasks` hook invoked this command, so it runs regardless of which preset
owns the `/speckit-tasks` body. Its only job is to mark the `tasks` phase active on the
branch-status card — the writer marks all prior phases done and later phases pending,
so this single call advances the card correctly.

The writer lives in the progress-report **preset**; this extension ships no copy of
it. Resolve it and skip cleanly if the preset isn't installed (the writer itself
already no-ops when the dashboard repo is absent, so a present writer is safe to call):

```bash
ROOT="${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel)}"
REPORT="$ROOT/.specify/presets/progress-report/scripts/python/progress_report.py"
if [ -f "$REPORT" ]; then
  python3 "$REPORT" enter tasks
else
  echo "progress-report preset not installed — skipping dashboard update (not an error)"
fi
```

Do not run task generation here; the core `/speckit-tasks` command does that. This
touches only the dashboard card.