---
name: workflow-status
description: Show who has returned, who is still working and how much output a background Workflow run produced. Use when the user asks about workflow progress, says "/workflows doesn't work", asks "is the workflow done", "how's the workflow going", "check the workflow", or wants to inspect a multi-agent orchestration run.
---

# Workflow status

For harness-owned isolated role workers, run `citizen role status` or
`citizen role status <worker-id>`. Report status, runtime, role and result path from those records.
They are separate CLI processes and do not appear as native subagent threads.

This reader inspects local Claude workflow journals from any client with filesystem access.
It does not inspect Codex native agent threads or hosted runs. For those, use the client's native
agent view; an empty local journal search does not mean no agents are running.

## Run it

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/status.py"            # most recent run
python3 "${CLAUDE_SKILL_DIR}/scripts/status.py" --all      # every run, newest first
python3 "${CLAUDE_SKILL_DIR}/scripts/status.py" --limit 3  # the last three
python3 "${CLAUDE_SKILL_DIR}/scripts/status.py" --run wf_eed4141a   # one specific run
```

Claude Code expands `CLAUDE_SKILL_DIR` to this skill's installed directory. In another client,
resolve this SKILL.md's absolute parent directory before invoking the script. Never execute an
unexpanded placeholder. Pass `--terminal-status completed|failed|cancelled` only with an exact
`--run` and an explicit terminal notification from the runtime; omit it when unknown.

Report the output to the user in prose — the counts, what is still in flight, and roughly how
far along the run is. Do not paste the raw table unless they ask for it.

## What it reads, and what it must not

The script reads:

- `~/.claude/projects/*/*/subagents/workflows/wf_*/journal.jsonl` — one line per agent start and
  one per agent result. This is the authoritative record of what has returned.
- the **first line only** of each `agent-*.jsonl`, to recover a human-readable identity (the
  workflow's `label` option is not persisted, so the agent's opening prompt is the best available
  name).
- the persisted script under `workflows/scripts/`, for the declared phase titles.

🛑 **Never read a full `agent-*.jsonl` transcript.** They routinely run to megabytes and will
overflow the context window. The journal plus first lines is always enough for status. If the user
wants an agent's actual findings, wait for the workflow to complete and read its returned result,
or read the file the workflow wrote — not the transcript.

## Interpreting it

- **`returned`, `pending`, `failed`, `unknown`** come from journal records joined by `agentId`
  and key. Transcript age describes activity only; it never proves that an agent returned.
- **`UNKNOWN (no terminal signal)`** means the journal cannot establish run completion, even
  when every currently known agent has returned. More phases may still launch.
- Missing or malformed journal records leave status unknown; they are not evidence of success.

## When a run has finished

The workflow's own completion notification carries the returned value, which is the thing to
report. This skill is for the interval before that arrives — or for checking on a run from a
different session, since the journal persists on disk.
