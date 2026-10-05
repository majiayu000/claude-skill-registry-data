---
name: poke
description: Quick 1-line status check after the user hit esc during a long generation. Report whether work is still progressing or stuck, then continue if fine. NOT a plan or replan — just a heartbeat.
when_to_use: "卡住了吗, 还在动吗, 一切正常吗, are you stuck, still working, heartbeat, esc-confirm — fired after user interrupts a long-running turn to confirm nothing is wrong"
user_invocable: true
---

# Poke Skill

The user hit `esc` during a long generation and wants a heartbeat: are you stuck, still progressing, or done? Answer in ≤3 lines, then continue if fine.

## Behavior

1. **Read the immediate prior context** (not project docs — there's no time).
2. **Classify the state** using the rubric below.
3. **Output ≤3 lines** in the exact format below.
4. **Act** according to state (continue / pause / surface).

## State rubric

| State | Signal | Action |
|---|---|---|
| `progressing` | You were mid-task, tools were returning useful output, no repeat failures | Report + continue same approach |
| `waiting` | Blocked on user confirmation, tool permission, or external process | Report + restate what you're waiting on |
| `stuck` | Same step failed 2+ times, or you've been looping without forward progress | Report + stop; surface the block clearly |
| `done` | Last task finished but reply wasn't closed out | Report result in 1-2 lines |
| `idle` | Nothing active, user probably expected something running | Say so — don't invent work |

## Output format

```
State: {progressing|waiting|stuck|done|idle}
Doing: {one clause — what you were mid-way on, or what just finished}
Next: {continuing → [action] | paused on [blocker] | nothing pending}
```

Then — only if `progressing` — immediately continue with the next tool call for the task. Do NOT re-plan, do NOT summarize the whole session, do NOT ask "should I continue?"

## Rules

- ≤3 lines total. No headers, no markdown fluff, no philosophy.
- Do NOT scan `TODO.md`, `PROGRESS.md`, or docs — this is a heartbeat, not `/next`.
- Do NOT start a new task or change direction — that's what the user will tell you after seeing the heartbeat.
- If `stuck`: say WHY in the "Next" line (e.g. `Next: paused on tests failing 3× with same error — need user guidance`).
- If `idle` and the user seems to expect background work: list recent background handles from this session (agents, `run_in_background` Bash, `/loop`) so they know where to look — see `/status` for the fuller dashboard.

## Completion Status

- ✅ **DONE**: Reported state in ≤3 lines. Resumed work (if progressing) or stopped cleanly.
- ⚠ **DONE_WITH_CONCERNS**: Couldn't classify state confidently — defaulted to surfacing ambiguity.
- ❌ **BLOCKED**: State is `stuck` and root cause needs user input.
