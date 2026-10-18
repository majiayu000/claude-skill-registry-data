---
name: autoresearch-wrapper-monitor
description: Report or keep an eye on an autoresearch-wrapper run's progress (status, rounds, best metric, stalls). Use when the user asks how a run is going or wants to be told when it finishes.
---

# Autoresearch Wrapper Monitor

Use the `run.sh` launcher in this skill's folder (the folder containing this `SKILL.md`). This block finds it in the standard Claude Code and Codex install locations:

```bash
AUTORESEARCH_RUNNER=""
if [ -n "${CLAUDE_SKILL_DIR:-}" ]; then
  AUTORESEARCH_RUNNER="${CLAUDE_SKILL_DIR}/run.sh"
elif [ -n "${CLAUDE_PLUGIN_ROOT:-}" ]; then
  AUTORESEARCH_RUNNER="${CLAUDE_PLUGIN_ROOT}/skills/autoresearch-wrapper-monitor/run.sh"
else
  for dir in skills/autoresearch-wrapper-monitor .agents/skills/autoresearch-wrapper-monitor .claude/skills/autoresearch-wrapper-monitor "$HOME/.agents/skills/autoresearch-wrapper-monitor" "$HOME/.claude/skills/autoresearch-wrapper-monitor" "$HOME/.codex/skills/autoresearch-wrapper-monitor"; do
    if [ -f "$dir/run.sh" ]; then AUTORESEARCH_RUNNER="$(readlink -f "$dir/run.sh")"; break; fi
  done
fi
[ -n "$AUTORESEARCH_RUNNER" ] || { echo "Could not resolve the autoresearch-wrapper-monitor launcher" >&2; exit 1; }
```

Do not run a blocking polling loop yourself: it ties up your tool call and can hit tool timeouts. Take snapshots instead.

When this skill is invoked:

1. Take a snapshot of the run (the active run by default; pass `--run-id <run>` for another, or `--arm <arm>` for an arm of a comparison run):

```bash
bash "$AUTORESEARCH_RUNNER" status --json
bash "$AUTORESEARCH_RUNNER" flow --run-id <run>
```

2. Report in a few lines:
- run status, and `stop_reason` once it has ended
- rounds completed vs the rounds target, and progress toward any stop rule
- best metric and which candidate holds it; the latest result
- stalled rounds vs early-exit patience, if configured
- candidates that crashed or are still unevaluated
- for comparison runs: each arm's phase (also try `compare --run-id <run>`)

3. If the user wants ongoing updates, re-check on a schedule using your tool's own scheduling (for example Claude Code's `/loop`) rather than sleeping in a shell. Pick an interval that matches how long one evaluation takes (no faster than every few minutes for long metric commands). Stop when the run reaches `completed` or `early_exit`, and then offer `finalize`.

4. If the user wants to watch it themselves in a terminal, give them the CLI's live poller to run (it blocks until the run ends):

```bash
bash "$AUTORESEARCH_RUNNER" monitor --interval 60
```

5. If no run exists, say so and suggest starting one with the `autoresearch-wrapper-run` skill.

## Example

- `/autoresearch-wrapper-monitor how is the latency run doing?`
