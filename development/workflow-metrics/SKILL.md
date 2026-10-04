---
name: workflow-metrics
description: Measure a workflow change before and after — questions and recommended answers, stops, tokens, long contexts, skill and MCP use — from Claude Code transcripts, deduplicated per model call.
---

# Workflow metrics

Invoke with: `/superpowers-gstack:workflow-metrics [project] [change date]`

```bash
SKILL_DIR='<the base directory the Skill tool printed when this skill loaded>'
WM="$SKILL_DIR/../../scripts/workflow-metrics.py"
[ -f "$WM" ] || WM=$(ls ~/.claude/plugins/cache/*/superpowers-gstack/*/scripts/workflow-metrics.py 2>/dev/null | sort -V | tail -1)
```

## Before and after

Pick the change's date and time (a commit, the moment a contract went into CLAUDE.md),
then run each measurement twice with the same `--project`:

```bash
python3 "$WM" asks   --project <dir substring> --until <change>
python3 "$WM" asks   --project <dir substring> --since <change>
python3 "$WM" tokens --project <dir substring> --until <change>
python3 "$WM" tokens --project <dir substring> --since <change>
```

With `--since` / `--until`, each transcript file (a subagent's included) is filtered by
its own first timestamp, so a subagent file can be in scope while its parent session is not.

| Command | Answers |
|---|---|
| `asks` | How many structured questions, how many answered with the recommended option, how long Claude works between your messages |
| `tokens` | Model calls (main / subagent), output, context reused and written, per project |
| `overhead` | How much context is baseline, and how much is spent above 150k / 200k / 300k / 500k |
| `triggers` | Which builds and test runs happened, how long they took, who asked for them |
| `skills` | Which skills are listed every turn and which were never used |
| `mcp` | MCP calls per server and project (server names only, never their settings; `--claude-json` names the file) |
| `digest --session <file>` / `digest --top N` | A compressed timeline of one session, or the longest sessions |

Every count is one per model call: transcripts write one event per content block, and
counting events inflates the numbers two to three times.

Report the before/after pair as a small table and say what moved. Fewer than about ten
sessions on either side is an anecdote; say so.

**Transcripts are deleted** after `cleanupPeriodDays` (30 by default) in
`~/.claude/settings.json`. For a study longer than that, raise it or copy
`~/.claude/projects` aside and pass `--root <copy>`.
