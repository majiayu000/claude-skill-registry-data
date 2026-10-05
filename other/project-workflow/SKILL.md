---
name: project-workflow
description: Runs multi step work the way a careful senior engineer would. Triage before code, a short PRD in prds/, task.md kept current, docs synced after, and lessons recorded when a mistake repeats. Use when a task spans several files or steps, changes architecture, needs a plan the user can review, or when the user says "write a PRD", "plan this", "track this in task.md", or "what did we learn".
---

# Project workflow

One loop for any task bigger than a typo. Plan in a PRD, track in `task.md`, sync docs when done, write down what went wrong so it does not repeat.

Skip this for one file fixes. A typo, a copy change, a single obvious bug. Just fix those.

## The loop

1. Triage. Read the request and the code before touching anything.
2. PRD. Write `prds/<slug>.md` from the template. Share it if the plan has a real choice in it.
3. Track. Add the work to `task.md` under `## To Do`. Move items as they land.
4. Build. Small commits worth of change at a time. Verify each step.
5. Sync docs. Hand off to the `project-docs` skill to update `task.md`, `changelog.md`, `files.md`.
6. Learn. If the user corrected the same thing twice, add a line to `prds/lessons.md`.

## Triage

Before writing code, answer these in a few lines:

- What is missing, broken, or incomplete?
- What are two or three likely causes or approaches?
- Which one is most likely, and why?
- What is still unclear enough to ask about?

If the last answer is not empty, ask. One question, not five. Then wait.

For bugs, name the root cause before proposing the fix. A fix without a root cause is a guess.

## PRD

Create `prds/<feature-or-problem-slug>.md` before non trivial work. Use the layout in [references/prd-template.md](references/prd-template.md).

Required sections:

- Problem (one paragraph)
- Root cause (bugs only)
- Proposed solution
- Files to change
- Edge cases
- Verification steps
- Task completion log

Metadata at the top, always in UTC:

```
Created: YYYY-MM-DD HH:mm UTC
Last Updated: YYYY-MM-DD HH:mm UTC
Status: Draft | In Progress | Done
```

Keep it short. A PRD that takes longer to write than the change did is too long. Two screens is plenty for most work.

PRDs are `.md` files and live in `prds/`. Old or sensitive PRDs move to `prds/archive/`.

## Task tracking

`task.md` has three sections: `## To Do`, `## In Progress`, `## Completed`.

- New work goes under To Do with a link to its PRD.
- Only one item In Progress at a time when possible.
- An item moves to Completed after verification, not after the edit.
- Completed entries carry a `YYYY-MM-DD HH:mm UTC` timestamp, the files touched, and the verification command or outcome.

Good entry:

```
- [x] 2026-09-15 18:40 UTC Fix duplicate heartbeat writes. prds/heartbeat-dedup.md. convex/stats.ts, src/hooks/usePageTracking.ts. Verified: npx convex dev clean, no OCC retries in dashboard for 10 min.
```

Bad entry:

```
- [x] fixed heartbeat
```

## Docs sync

After each feature or fix, `task.md`, `changelog.md`, and `files.md` have to agree with the code. Load the `project-docs` skill for the rules. In short:

- `changelog.md` follows Keep a Changelog. Dates come from `git log --date=short`, never from memory.
- `files.md` gets new files added and stale descriptions fixed.
- Claims about what shipped come from the diff, not from the plan.

## Execution style

- Keep the change set tight. The request sets the scope. Extra ideas go in the summary, not the diff. Load `avoid-feature-creep` if scope starts to drift.
- One subagent per research question when the task is large enough to benefit. Do not parallelize edits to the same file.
- Stop and re plan if the work stops making sense. Update the PRD, then continue.
- Before calling it done, ask: would a staff engineer approve this diff as is?

## Learning loop

`prds/lessons.md` is a flat list. One line per lesson, newest at the bottom:

```
- 2026-09-15 Do not add `returns` validators that duplicate the schema doc shape; use a shared validator constant instead.
```

Add a lesson when:

- the user corrects the same pattern a second time
- a verification step catches something the plan missed
- a tool or API behaved differently from the docs

Read `prds/lessons.md` at the start of any session in that repo.

## Never

- Deploy, publish, commit, or push. The user does those.
- Mark a task done without running the verification step written in the PRD.
- Invent a date. Run `git log` or use the current UTC time.
- Write a PRD for a one line change.
