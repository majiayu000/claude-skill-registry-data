---
name: autoresearch-wrapper-flow
description: Show or plot recorded metric flow for an autoresearch-wrapper run. Use when the user wants the chronological metric sequence, best-so-far progression, or a terminal-friendly plot.
---

# Autoresearch Wrapper Flow

Use the `run.sh` launcher in this skill's folder (the folder containing this `SKILL.md`). This block finds it in the standard Claude Code and Codex install locations:

```bash
AUTORESEARCH_RUNNER=""
if [ -n "${CLAUDE_SKILL_DIR:-}" ]; then
  AUTORESEARCH_RUNNER="${CLAUDE_SKILL_DIR}/run.sh"
elif [ -n "${CLAUDE_PLUGIN_ROOT:-}" ]; then
  AUTORESEARCH_RUNNER="${CLAUDE_PLUGIN_ROOT}/skills/autoresearch-wrapper-flow/run.sh"
else
  for dir in skills/autoresearch-wrapper-flow .agents/skills/autoresearch-wrapper-flow .claude/skills/autoresearch-wrapper-flow "$HOME/.agents/skills/autoresearch-wrapper-flow" "$HOME/.claude/skills/autoresearch-wrapper-flow" "$HOME/.codex/skills/autoresearch-wrapper-flow"; do
    if [ -f "$dir/run.sh" ]; then AUTORESEARCH_RUNNER="$(readlink -f "$dir/run.sh")"; break; fi
  done
fi
[ -n "$AUTORESEARCH_RUNNER" ] || { echo "Could not resolve the autoresearch-wrapper-flow launcher" >&2; exit 1; }
```

Use:

```bash
bash "$AUTORESEARCH_RUNNER" flow
```

When this skill is invoked:

1. Show the recorded metric flow for the active run by default.
2. Summarize:
- metric name
- goal
- chronological sequence
- best-so-far sequence
- latest metric
- best metric

3. Include the ASCII plot when presenting the result.

4. If the user asks for raw structured data, use:

```bash
bash "$AUTORESEARCH_RUNNER" flow --json
```

## Example

- `/autoresearch-wrapper-flow`
