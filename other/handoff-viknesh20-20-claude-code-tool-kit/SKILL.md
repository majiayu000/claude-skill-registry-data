---
name: handoff
description: "End-of-session summary written to .claude/memory/handoffs/<date>.md so the next session can pick up cleanly. Captures what was done, what's pending, what's blocked, what to verify, and any decisions awaiting the user."
---

# /handoff

Write an end-of-session handoff summary so the next session — yours, your teammate's, or a future-you's — can resume work without losing context.

## When to use

- End of a working session, even a short one, if work is left unfinished.
- Before stepping away from a long-running task (deploy in progress, migration mid-flight, large refactor in progress).
- Before switching contexts to a different project.
- After a meaningful milestone (feature shipped, decision made, blocker hit).

## Operating method

Read the current session transcript and produce a structured summary. Save it to `.claude/memory/handoffs/<YYYY-MM-DD>.md`. If a handoff already exists for today, append to it (don't overwrite — sessions can resume mid-day).

### Sections to populate

```markdown
---
name: handoff-<YYYY-MM-DD>-<HH-MM>
type: handoff
description: <one-line: what was the focus today?>
created: <YYYY-MM-DD HH:MM TZ>
---

# Handoff — <date>

## Focus today
<2–3 sentences. The actual goal, not the title.>

## What we did
- <specific change, with file paths or commit refs>
- <…>

## What's left for next session
- [ ] <task 1, with enough detail to start cold>
- [ ] <task 2>

## Blocked / waiting
- <blocker, who/what we're waiting on, when expected>

## Decisions made
- <decision> — chosen because <reason>. Reversible if <condition>.

## Decisions awaiting the user
- <question> — needs answer before <next step>.

## To verify before continuing
- <test that should still pass>
- <metric that should still be in budget>
- <thing the user said they'd check>

## Surprises / things I learned
- <non-obvious fact about the codebase or domain>
  (if it'll matter beyond this week, also save as a project memory)

## Open files / branches
- Branch: <name>
- Uncommitted files: <list>
- Stash entries: <list>

## Next concrete action
<the single first thing to do next session — small enough to not need re-thinking>
```

### Update the index

Append to `.claude/memory/MEMORY.md`:

```
## Handoffs
- [<YYYY-MM-DD>](memory/handoffs/<YYYY-MM-DD>.md) — <focus from description>
```

Newest at the top of the section.

## Behavior rules

- **Don't summarize what's already in git.** A handoff is for state that *isn't* in code: ambiguity, awaiting decisions, surprises, things to verify.
- **Promote to long-term memory if appropriate.** Surprises that'll matter in a month should also be saved to `project/`. Handoffs decay; project memory is curated.
- **Be specific about the next action.** "Continue working on auth" is useless. "Open `src/auth/sign-in.ts:42`, replace the bcrypt call with `argon2.hash` and update the test" is useful.
- **Surface decisions awaiting the user prominently.** This is the highest-value section — questions the user needs to answer to unblock progress.
- **Don't include secrets** — same redaction rules as other memory.

## Output format

Show the handoff before writing. Confirm. Write. Print a one-line "Handoff saved" + the path.

```
## Handoff preview
[…full content…]

Save? [Y/n]
```

After save:

```
✓ Handoff saved: .claude/memory/handoffs/2026-05-02-15-45.md
✓ Indexed in .claude/memory/MEMORY.md

Next session start: read this handoff and pick up at "Next concrete action".
```

## Calibration

A good handoff is roughly the length of a Slack message, not a status report. Three to ten lines per section. If you're padding, drop the section.

If nothing is pending and the session was clean: skip the handoff. Don't write empty stubs.
