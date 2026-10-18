---
name: autoresearch-wrapper-run
description: Start or resume a dependency-aware autoresearch-wrapper run in Git worktrees. Use when the target and metric are already configured and the user wants to initialize or continue the optimization loop.
---

# Autoresearch Wrapper Run

Use the `run.sh` launcher in this skill's folder (the folder containing this `SKILL.md`). This block finds it in the standard Claude Code and Codex install locations:

```bash
AUTORESEARCH_RUNNER=""
if [ -n "${CLAUDE_SKILL_DIR:-}" ]; then
  AUTORESEARCH_RUNNER="${CLAUDE_SKILL_DIR}/run.sh"
elif [ -n "${CLAUDE_PLUGIN_ROOT:-}" ]; then
  AUTORESEARCH_RUNNER="${CLAUDE_PLUGIN_ROOT}/skills/autoresearch-wrapper-run/run.sh"
else
  for dir in skills/autoresearch-wrapper-run .agents/skills/autoresearch-wrapper-run .claude/skills/autoresearch-wrapper-run "$HOME/.agents/skills/autoresearch-wrapper-run" "$HOME/.claude/skills/autoresearch-wrapper-run" "$HOME/.codex/skills/autoresearch-wrapper-run"; do
    if [ -f "$dir/run.sh" ]; then AUTORESEARCH_RUNNER="$(readlink -f "$dir/run.sh")"; break; fi
  done
fi
[ -n "$AUTORESEARCH_RUNNER" ] || { echo "Could not resolve the autoresearch-wrapper-run launcher" >&2; exit 1; }
```

Use:

```bash
bash "$AUTORESEARCH_RUNNER" run
```

When this skill is invoked:

1. Start or resume the current run.
2. If the run is blocked, explain whether the missing requirement is:
- target selection
- metric configuration
- execution settings
- dependency-aware readiness

3. If the run starts successfully, summarize:
- run id
- target part
- generated `program.md`
- seed worktree
- any preallocated candidates
- execution mode (sequential, parallel, or wild)

4. Remind the user that the underlying loop uses:
- `allocate`
- `evaluate` (commits pending worktree edits before measuring, so kept candidates compound)
- `record`

The run is marked `completed` when the rounds target or stop rule is met (or `early_exit` on stall); its `stop_reason` says why, and `allocate` refuses afterwards. Stop rules are comma-separated clauses, any of which ends the run: `metric<=X` / `metric>=X` / `metric<X` / `metric>X`, `stalled:N`, `minutes:N`.

5. When the run has ended, offer to merge back and clean up:

```bash
bash "$AUTORESEARCH_RUNNER" finalize --run-id <run> --merge
```

Confirm with the user before `--merge` (stages a squash merge of the best branch in their checkout, not committed) or `--prune-branches` (deletes all other run branches). Dirty worktrees are skipped unless `--force`; `--stop` ends a running run first. Without `--merge`, relay the printed `git diff` / `git merge --squash` commands.

6. If early exit is configured, inform the user:
- patience setting (how many rounds without improvement before stopping)
- threshold setting (minimum improvement to count as progress)
- the run will end with status `early_exit` if the patience is exceeded

7. If wild mode is configured, it is your search strategy, not something the CLI automates. Candidates are allocated as in parallel mode; in each one:
- change several parameters at once, up to `wild_max_simultaneous`
- while the metric keeps improving, stay close to the current best (one or two changes)
- when improvement stalls (watch the stalled-round count), widen: change more parameters together or take larger steps

## Example

- `/autoresearch-wrapper-run`
