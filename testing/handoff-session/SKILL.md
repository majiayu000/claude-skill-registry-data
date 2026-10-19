---
name: handoff-session
description: "User-triggered session handoff. Writes a detailed HANDOFF.md with current state, open items, pending decisions, and recommended resume prompt. Use before switching machines, before long breaks, or when you need to clear context intentionally. Parallel to the automatic pre-compact hook."
tier: task
version: 0.1.0
allowed-tools:
  - Bash
  - Read
  - Write
  - AskUserQuestion
triggers:
  - handoff session
  - pause work
  - save context for later
  - ytstack handoff
---

# handoff-session

Create a `.ytstack/HANDOFF.md` that lets the next session (yours or someone else's) pick up exactly where this one left off. This is the user-triggered equivalent of the automatic `pre-compact` hook -- but richer, because the user decides what matters.

## Anti-Pattern: "I'll remember what I was doing"

You won't. Tomorrow-you, monday-you, and teammate-you all read handoffs cold. The test: write the handoff, read it yourself 30 seconds later, can you pick up without scrolling conversation history? If yes, ship. If no, add detail.

## Checklist

1. **Run preamble** -- detect state
2. **HARD-GATE** -- ytstack initialized
3. **Ask: what's open right now?** -- one sentence on in-flight work
4. **Ask: what's the next action?** -- concrete next step
5. **Ask: any open decisions blocking?** -- things you need the next session to decide
6. **Ask: any warnings / gotchas?** -- things easy to miss
7. **Write `HANDOFF.md`** (overwrites the hook-generated one)
8. **Report + suggest clean exit**

## Preamble

```bash
_PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$PWD}"
cd "$_PROJECT_DIR" 2>/dev/null || true
_PROJECT_SLUG=$(basename "$(git rev-parse --show-toplevel 2>/dev/null)" 2>/dev/null || basename "$(pwd)")
if [ -d "$_PROJECT_DIR/.ytstack" ]; then _YT_DIR="$_PROJECT_DIR/.ytstack";
elif [ -d "$HOME/.ytstack/projects/$_PROJECT_SLUG" ]; then _YT_DIR="$HOME/.ytstack/projects/$_PROJECT_SLUG";
else _YT_DIR=""; fi
_HAS_YTSTACK=$([ -n "$_YT_DIR" ] && echo yes || echo no)

_CURRENT_MILESTONE=none; _ACTIVE_SLICE=none; _ACTIVE_TASK=none; _PROJECT_NAME=unknown
if [ -f "$_YT_DIR/STATE.md" ]; then
  _CURRENT_MILESTONE=$(sed -n 's/^current_milestone: *//p' "$_YT_DIR/STATE.md" | head -1)
  _ACTIVE_SLICE=$(sed -n 's/^active_slice: *//p' "$_YT_DIR/STATE.md" | head -1)
  _ACTIVE_TASK=$(sed -n 's/^active_task: *//p' "$_YT_DIR/STATE.md" | head -1)
fi
[ -f "$_YT_DIR/PROJECT.md" ] && _PROJECT_NAME=$(sed -n 's/^name: *//p' "$_YT_DIR/PROJECT.md" | head -1)
_BRANCH=$(git branch --show-current 2>/dev/null || echo unknown)

echo "HAS_YTSTACK: $_HAS_YTSTACK"
echo "PROJECT_NAME: $_PROJECT_NAME"
echo "CURRENT_MILESTONE: $_CURRENT_MILESTONE / $_ACTIVE_SLICE / $_ACTIVE_TASK"
echo "BRANCH: $_BRANCH"
```

## Procedure

**Step 2 HARD-GATE.** If `HAS_YTSTACK=no`: abort.

**Step 3 -- Open work.** AskUserQuestion:
> Writing a handoff for **{PROJECT_NAME}** on branch `{BRANCH}`. Position: {CURRENT_MILESTONE} / {ACTIVE_SLICE} / {ACTIVE_TASK}.
>
> What's currently in-flight? One sentence. What were you in the middle of when you hit pause?

Remember as `_OPEN_WORK`.

**Step 4 -- Next action.** AskUserQuestion:
> What's the exact next step when you pick this up? Be concrete. Not "continue the task" but "finish the argon2 integration in src/auth/signup.ts, starting at line 47."

Remember as `_NEXT_ACTION`.

**Step 5 -- Open decisions.** AskUserQuestion:
> Any decisions that need to be made before the next session can proceed? These become blockers if forgotten.
>
> Enter "none" if there are no blocking decisions.

Remember as `_OPEN_DECISIONS`.

**Step 6 -- Warnings.** AskUserQuestion:
> Any warnings, gotchas, or easy-to-miss details the next session should know? Examples: "the test suite skips a flaky test on main -- don't be surprised", "env var X must be set before running", "the staging DB is seeded, don't reset it".
>
> Enter "none" if nothing.

Remember as `_WARNINGS`.

**Step 7 -- Write HANDOFF.md.** Use Write tool. Path: `{YT_DIR}/HANDOFF.md`. Overwrites any hook-generated version.

```markdown
---
kind: handoff
event: user-triggered
timestamp: {ISO_TIMESTAMP}
project: {PROJECT_NAME}
branch: {BRANCH}
current_milestone: {CURRENT_MILESTONE}
active_slice: {ACTIVE_SLICE}
active_task: {ACTIVE_TASK}
---

# Session Handoff

Written by the user via `/ytstack:handoff-session` at {ISO_TIMESTAMP}.

## Position

- Project: **{PROJECT_NAME}**
- Branch: `{BRANCH}`
- Milestone / Slice / Task: `{CURRENT_MILESTONE}` / `{ACTIVE_SLICE}` / `{ACTIVE_TASK}`

## In-flight work

{OPEN_WORK}

## Next action

{NEXT_ACTION}

## Open decisions blocking progress

{OPEN_DECISIONS}

## Warnings / gotchas

{WARNINGS}

## How to resume

1. Start a new Claude Code session in this project directory.
2. SessionStart hook will auto-inject state from `STATE.md` -- read that first.
3. Read this file (`HANDOFF.md`) for the in-flight context.
4. Check latest `{CURRENT_MILESTONE}-{ACTIVE_SLICE}-{ACTIVE_TASK}-PLAN.md` and corresponding `-SUMMARY.md` if it exists.
5. Run `/ytstack:resume-session` to get a synthesized briefing.
6. Execute the "Next action" above.

## Related artifacts

- Full dashboard: `{YT_DIR}/STATE.md`
- Milestone roadmap: `{YT_DIR}/{CURRENT_MILESTONE}-ROADMAP.md`
- Deferred items: `{YT_DIR}/REVIEW-NOTES.md`
- Decision log: `{YT_DIR}/DECISIONS.md`
```

**Step 8 -- Report + suggest exit.**

> Handoff written to `{YT_DIR}/HANDOFF.md`. Safe to exit Claude Code now.
>
> To resume later: start a new session in this project, run `/ytstack:resume-session`, then execute the next action.
>
> If you're handing off to another person / machine: make sure `.ytstack/` is committed to git so they have access.

## Terminal State

Return after writing HANDOFF.md. Do NOT invoke any other skill. Do NOT attempt to end the Claude Code session -- that's the user's choice.
