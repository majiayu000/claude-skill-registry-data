---
name: autoresearch-wrapper-create
description: Create a feature-comparison run where each candidate implementation and a no-change control are tuned with equal budgets. Use when the user wants to add a new feature and compare approaches by their tuned capability ceiling.
---

# Autoresearch Wrapper Create

Use the `run.sh` launcher in this skill's folder (the folder containing this `SKILL.md`). This block finds it in the standard Claude Code and Codex install locations:

```bash
AUTORESEARCH_RUNNER=""
if [ -n "${CLAUDE_SKILL_DIR:-}" ]; then
  AUTORESEARCH_RUNNER="${CLAUDE_SKILL_DIR}/run.sh"
elif [ -n "${CLAUDE_PLUGIN_ROOT:-}" ]; then
  AUTORESEARCH_RUNNER="${CLAUDE_PLUGIN_ROOT}/skills/autoresearch-wrapper-create/run.sh"
else
  for dir in skills/autoresearch-wrapper-create .agents/skills/autoresearch-wrapper-create .claude/skills/autoresearch-wrapper-create "$HOME/.agents/skills/autoresearch-wrapper-create" "$HOME/.claude/skills/autoresearch-wrapper-create" "$HOME/.codex/skills/autoresearch-wrapper-create"; do
    if [ -f "$dir/run.sh" ]; then AUTORESEARCH_RUNNER="$(readlink -f "$dir/run.sh")"; break; fi
  done
fi
[ -n "$AUTORESEARCH_RUNNER" ] || { echo "Could not resolve the autoresearch-wrapper-create launcher" >&2; exit 1; }
```

Use:

```bash
bash "$AUTORESEARCH_RUNNER" create --part <part> --feature "<description>" --candidates <n> --metric <metric> --metric-command "<cmd>" --metric-goal <minimize|maximize>
```

When this skill is invoked:

1. If the user has not scanned yet, run `scan` first. Pass `--no-interactive` when stdin is not a terminal.
2. Identify the target part, the feature, the number of approaches, the metric, and the per-arm budget (`--rounds` and/or `--stop-rule`). Every arm gets the same budget.
3. Run `create`. It sets up arms `control` + `approach-A..N`, each with its own setup worktree. `control` (no change) starts tuning immediately: it exists so gains from tuning are not credited to the feature.
4. Summarize: run id, arms and their setup worktrees, tuning scope, budget, and the generated `program.md`. The tuning scope defaults to the target and its direct dependency neighbours; pass `--tune-scope "a.py,src/models/"` if the user names the knobs to tune (e.g. a config file). Files an arm changes during setup are always added to that arm's scope.
5. Setup phase: implement the feature differently in each `approach-*` setup worktree, then start its tuning run:

```bash
bash "$AUTORESEARCH_RUNNER" arm-ready --run-id <run> --arm approach-A
```

6. Tuning phase, per arm (`control` included): measure the setup score, then run the normal loop, editing only files in the tuning scope. `evaluate` rejects out-of-scope edits before running the metric; revert them rather than reaching for `--allow-out-of-scope`, which is for deliberate exceptions the user approves and is flagged in `compare`:

```bash
bash "$AUTORESEARCH_RUNNER" evaluate --run-id <run> --arm <arm> --candidate seed
bash "$AUTORESEARCH_RUNNER" record --run-id <run> --arm <arm> --candidate seed --status auto --description "setup"
bash "$AUTORESEARCH_RUNNER" allocate --run-id <run> --arm <arm>
```

An arm is done when its rounds target or stop rule is met.

7. Compare. Present the table: setup score, tuned ceiling, tuning gain, delta vs. tuned control, and the winner (ties go to control, i.e. the status quo):

```bash
bash "$AUTORESEARCH_RUNNER" compare --run-id <run>
```

8. Offer to merge the winner and clean up. Confirm with the user before `--merge` or `--prune-branches`. If `control` wins, say plainly that no approach beat the status quo once both were tuned:

```bash
bash "$AUTORESEARCH_RUNNER" finalize --run-id <run> --merge
```

## Example

- `/autoresearch-wrapper-create --part src/api.py --feature "add response caching" --candidates 3 --rounds 10 --metric latency_ms --metric-command "python bench.py" --metric-goal minimize`
