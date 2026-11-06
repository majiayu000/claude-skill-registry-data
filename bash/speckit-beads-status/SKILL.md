---
name: speckit-beads-status
description: Show the Beads execution DAG, current readiness, and future waves
compatibility: Requires spec-kit project structure with .specify/ directory
metadata:
  author: Sidekick contributors
  source: beads:commands/speckit.beads.status.md
---

## User Input

```text
$ARGUMENTS
```

Explain what can be completed now and what becomes available afterward, using Beads as the sole execution authority.

1. Resolve the current feature directory with `.specify/scripts/bash/check-prerequisites.sh --json --require-spec`.
2. Run:

   ```bash
   python3 .specify/extensions/beads/scripts/beads_tasks.py status \
     --project-root "$PWD" --feature <feature-directory-name>
   ```

3. Present:
   - the feature epic and completion counts;
   - wave 0 as work that is ready or already in progress;
   - later waves as work unlocked when previous waves complete;
   - tasks blocked by unresolved internal dependencies, external Beads issues, or deferred/blocked state;
   - completed tasks separately.
4. Cross-check with `bd ready --json` and `bd dep cycles`. If they disagree with the projection, report the discrepancy instead of guessing.

Do not modify issue state. The dependency edges in Beads are the authoritative DAG; the planned DAG snapshot on the epic is provenance for the last reconciliation.