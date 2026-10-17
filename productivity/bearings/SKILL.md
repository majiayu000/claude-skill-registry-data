---
name: bearings
description: Generate a "pick up where I left off" status report across all active Pi sessions. Use when the user asks for bearings, a status report, morning brief, catch-up, "where did I leave off", or "what's in the works". Reads live session state, composes a scannable 4-section digest, and writes a dated report to ~/.pi/agent/bearings/.
user-invocable: true
---

# Bearings

Generate a complete standalone snapshot from all active Pi sessions, so you can resume in one read after a break, a night, or a context reset.

Inspired by FirstMate's `bearings` skill (kunchenguid/firstmate), adapted for auto-pi's multi-session architecture. Zero dependencies — reads local state files only.

## What it does

1. **Gather live session state.** Read `~/.pi/agent/session-status.jsonl` — each line is a JSON object written by the status extension on every `agent_start`/`agent_end`:

   ```json
   {"sessionId":"abc","project":"/path","phase":"build","task":"add pagination","status":"working","ts":"2026-07-20T..."}
   ```

   Also read `~/.pi/agent/decisions.json` for open decisions.

2. **Compose the 4-section digest.** Every section ALWAYS renders, even when empty:

   - **Your Call** — decisions that need your action now. Open items from `decisions.json` that are unresolved. Empty-state: "Nothing needs your action right now."
   - **Recently Landed** — completed work since last bearings. Check `git log --oneline -5` in each project with active state. Empty-state: "No recent completions."
   - **Underway** — live sessions currently working. One line per session: project, phase, task, status. Empty-state: "Nothing is underway."
   - **Charted Next** — check open issues for what to tackle next. Empty-state: "Nothing is queued."

3. **Write the dated report** to `~/.pi/agent/bearings/<YYYY-MM-DD>.md` and surface the concise digest in chat.

## Rules

- Read-only. Never mutates session state, decisions, or workflow state as a side effect.
- Every section always renders with its empty-state sentence.
- Every report is a complete current snapshot, never a delta against a prior report.
- The 4 buckets are mutually exclusive: needs-your-action = Your Call, done = Recently Landed, self-progressing = Underway, not-yet-started = Charted Next.
- If state suggests an action (PR ready, gate arrived), name it in its section and let the user decide — do not take the action from inside this skill.
