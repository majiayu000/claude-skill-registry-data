---
name: underwrite-preflight
description: Verify changes in the underwrite repository locally before reporting completion, committing, or pushing. Use for code, tests, contracts, packaging, CI, and documentation changes in this project.
---

# Underwrite preflight

Run from the repository root. The shared runner owns the checks used locally and
in GitHub CI; do not reconstruct its command list or substitute a prior CI pass.

1. Run focused regression tests while editing. Before finishing a change, run:

   ```sh
   uv run --frozen --no-sync python scripts/preflight.py
   ```

   The runner synchronizes frozen development dependencies. Its default compares
   against `origin/main` and includes staged, unstaged, and untracked changes.
   If the task has a different reviewed base, supply `--base <ref>` explicitly.
   A missing base, unknown path, or uncertain change set selects the full suite.
   Only the runner's narrow documentation allowlist can select the shorter lane.

2. For release preparation or an explicitly requested complete audit, use
   `--mode full`. To inspect selection without running checks, use `--plan`;
   a plan is not validation. Do not force a smaller change set to get a pass.

3. Read the exit status and `output/preflight.json`. Fix failures, rerun affected
   tests, and rerun preflight after the final edit. A failed, interrupted, or
   partial run is not a pass. Reports are local diagnostics, not signed evidence
   or permission to skip GitHub checks. Do not commit the report or upload logs
   automatically. If a prerequisite cannot be recovered locally, report exactly
   what was not checked; do not silently downgrade to a lighter lane.

4. Report the selected lane, actual outcomes, and any remaining limitation.
   A successful run can cover completion and a subsequent commit/push of those
   unchanged files; do not repeat it solely because the commit ID changed.
   This skill does not authorize a push, merge, release, or deployment.

The full lane preserves strict typing, lint, import/dependency boundaries, tests,
both distribution builds, installed-wheel CLI behavior, and pure-only execution.
No Docker, hosted service, or new testing dependency is required. Keep source
claims and `not_measured`, `indeterminate`, and `abstained` distinct.
