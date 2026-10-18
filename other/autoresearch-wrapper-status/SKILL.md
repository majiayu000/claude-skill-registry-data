---
name: autoresearch-wrapper-status
description: Show dependency-aware autoresearch-wrapper state for the current repo. Use when the user wants the selected part, readiness, runs, candidates, or current status summary.
---

# Autoresearch Wrapper Status

Use the `run.sh` launcher in this skill's folder (the folder containing this `SKILL.md`). This block finds it in the standard Claude Code and Codex install locations:

```bash
AUTORESEARCH_RUNNER=""
if [ -n "${CLAUDE_SKILL_DIR:-}" ]; then
  AUTORESEARCH_RUNNER="${CLAUDE_SKILL_DIR}/run.sh"
elif [ -n "${CLAUDE_PLUGIN_ROOT:-}" ]; then
  AUTORESEARCH_RUNNER="${CLAUDE_PLUGIN_ROOT}/skills/autoresearch-wrapper-status/run.sh"
else
  for dir in skills/autoresearch-wrapper-status .agents/skills/autoresearch-wrapper-status .claude/skills/autoresearch-wrapper-status "$HOME/.agents/skills/autoresearch-wrapper-status" "$HOME/.claude/skills/autoresearch-wrapper-status" "$HOME/.codex/skills/autoresearch-wrapper-status"; do
    if [ -f "$dir/run.sh" ]; then AUTORESEARCH_RUNNER="$(readlink -f "$dir/run.sh")"; break; fi
  done
fi
[ -n "$AUTORESEARCH_RUNNER" ] || { echo "Could not resolve the autoresearch-wrapper-status launcher" >&2; exit 1; }
```

Use:

```bash
bash "$AUTORESEARCH_RUNNER" status
```

When this skill is invoked:

1. Run the status command for the current repo.
2. Summarize:
- selected part
- readiness
- dependency blockers
- active run
- candidate lifecycle
- compact metric-flow summary if present

3. If the user asks for raw machine-readable output, use:

```bash
bash "$AUTORESEARCH_RUNNER" status --json
```

## Example

- `/autoresearch-wrapper-status`
