---
name: speckit-progress-implement
description: 'Hook: mark the implement phase active on the dashboard card'
compatibility: Requires spec-kit project structure with .specify/ directory
metadata:
  author: imosquera
  source: extension:progress
user-invocable: true
disable-model-invocation: false
---

# Progress Implement Skill

## Dashboard — enter `implement` (lifecycle hook)

The `before_implement` hook invoked this command, so it runs regardless of which preset
owns the `/speckit-implement` body. Its only job is to mark the `implement` phase active
on the branch-status card — the writer marks all prior phases done and later phases
pending, so this single call advances the card correctly.

The writer lives in the progress-report **preset**; this extension ships no copy of
it. Resolve it and skip cleanly if the preset isn't installed (the writer itself
already no-ops when the dashboard repo is absent, so a present writer is safe to call):

```bash
PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel)}"
REPORT="$PROJECT_DIR/.specify/presets/progress-report/scripts/ts/progress_report.ts"
if [ ! -f "$REPORT" ]; then
  echo "progress-report preset not installed (or installed before the bun port — refresh with ./install.ts --force) — skipping dashboard update (not an error)"
elif ! command -v bun >/dev/null; then
  echo "WARNING: progress-report is installed but bun is not on PATH — the dashboard card was NOT updated. Install bun (https://bun.sh)." >&2
else
  bun "$REPORT" enter implement
fi
```

Do not run implementation here; the core `/speckit-implement` command does that. This
touches only the dashboard card.
