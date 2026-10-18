---
name: start
description: The day-one first-run flow and the everyday home screen. On first launch, greet, run setup, then carry the operator into a real first win. On return, give a short briefing and action menu.
trigger: /start
---

# /start: wake the operator

Use this skill on first launch and whenever the operator asks for the home screen, start menu, or orientation.

## State contract

The canonical first-run state is `.aigent/state.json`:

```json
{
  "schemaVersion": 1,
  "status": "uninitialized | setup-in-progress | ready",
  "completedAt": null
}
```

For compatibility with installations before v0.9, `.aigent/first-run-done` is also recognized.

- `status: ready` or a legacy first-run marker means returning operator.
- Missing state, invalid state, or any other status means first run.
- If the legacy marker exists but the JSON state is not ready, migrate the JSON state to `ready` silently.

## First run

1. Write `status: setup-in-progress` before asking questions, so an interrupted setup can resume.
2. Give a two-line, warm, plain greeting:
   > I'm your AIgent operator. Let's get you one real win in the next few minutes.
3. Run `/operator-setup`, one question at a time.
4. When the operator chooses an action from the personal briefing, run `/first-win` and produce a usable artifact.
5. Teach the operating loop once:
   > Later sessions pick up on their own via `/resume`. When you are done, say "close up" or run `/context-capsule` so the work is banked (it also autosaves as you go). Run `/statusline` once in Claude Code to show context usage.
6. Only after setup memory and the first artifact are successfully written:
   - Set `.aigent/state.json` to `status: ready` with an ISO-8601 `completedAt` value.
   - Write `.aigent/first-run-done` for backward compatibility.

Do not mark setup ready before the durable writes succeed.

## Returning operator

1. Read `memory/about-you.md` and recent session memory.
2. Give a short, specific briefing: what matters today, what changed, and what is blocked.
3. Surface the action menu.

## Action menu

Present a short numbered list and accept either the number or a plain-language request:

1. Plan my day
2. Draft content
3. Research something
4. Build an automation
5. Check my numbers
6. Talk it through

On first run, lead with zero-dependency actions so the first win never waits on a connector.

## Rules

- Use plain English and the operator's nouns.
- Ask one setup question at a time.
- Never invent business facts.
- If an operation fails, state what failed, what was attempted, and what durable state was or was not written.
- Do not leave `status: setup-in-progress` indefinitely after a successful setup.
