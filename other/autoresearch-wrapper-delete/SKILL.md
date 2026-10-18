---
name: autoresearch-wrapper-delete
description: Create a deletion-comparison run that tunes the codebase with and without a part using equal budgets. Use when the user wants to remove a module or file and know whether it is worth it once dependents are re-tuned.
---

# Autoresearch Wrapper Delete

Use the `run.sh` launcher in this skill's folder (the folder containing this `SKILL.md`). This block finds it in the standard Claude Code and Codex install locations:

```bash
AUTORESEARCH_RUNNER=""
if [ -n "${CLAUDE_SKILL_DIR:-}" ]; then
  AUTORESEARCH_RUNNER="${CLAUDE_SKILL_DIR}/run.sh"
elif [ -n "${CLAUDE_PLUGIN_ROOT:-}" ]; then
  AUTORESEARCH_RUNNER="${CLAUDE_PLUGIN_ROOT}/skills/autoresearch-wrapper-delete/run.sh"
else
  for dir in skills/autoresearch-wrapper-delete .agents/skills/autoresearch-wrapper-delete .claude/skills/autoresearch-wrapper-delete "$HOME/.agents/skills/autoresearch-wrapper-delete" "$HOME/.claude/skills/autoresearch-wrapper-delete" "$HOME/.codex/skills/autoresearch-wrapper-delete"; do
    if [ -f "$dir/run.sh" ]; then AUTORESEARCH_RUNNER="$(readlink -f "$dir/run.sh")"; break; fi
  done
fi
[ -n "$AUTORESEARCH_RUNNER" ] || { echo "Could not resolve the autoresearch-wrapper-delete launcher" >&2; exit 1; }
```

Use:

```bash
bash "$AUTORESEARCH_RUNNER" delete --part <part> --metric <metric> --metric-command "<cmd>" --metric-goal <minimize|maximize>
```

When this skill is invoked:

1. If the user has not scanned yet, run `scan` first. Pass `--no-interactive` when stdin is not a terminal.
2. Identify the part to delete, the metric, and the per-arm budget (`--rounds` and/or `--stop-rule`).
3. Run `delete`. It sets up two arms: `control` (part kept, starts tuning immediately; it is the tuned pre-deletion baseline) and `deleted` (part removed and committed in its setup worktree).
4. Summarize: run id, transitive dependents of the deleted part, tuning scope, budget, and the generated `program.md`. The tuning scope defaults to the deleted part's direct dependents (override with `--tune-scope`); files changed while repairing the `deleted` arm are added to its scope. `evaluate` rejects out-of-scope edits; `--allow-out-of-scope` is for user-approved exceptions and is flagged in `compare`.
5. Setup phase: fix broken imports and references in the `deleted` setup worktree, then start its tuning run:

```bash
bash "$AUTORESEARCH_RUNNER" arm-ready --run-id <run> --arm deleted
```

6. Tuning phase, for both arms: `evaluate`/`record` the `seed` with `--arm <arm>` to get the setup score, then `allocate`/`evaluate`/`record` with `--arm <arm>` until the budget is spent.
7. Compare and report whether removing the part costs or gains once dependents are re-tuned:

```bash
bash "$AUTORESEARCH_RUNNER" compare --run-id <run>
```

8. Offer `finalize --run-id <run> --merge` to merge the winner and clean up. Confirm with the user before `--merge` or `--prune-branches`.

## Example

- `/autoresearch-wrapper-delete --part src/legacy_cache.py --rounds 10 --metric throughput --metric-command "python bench.py" --metric-goal maximize`
