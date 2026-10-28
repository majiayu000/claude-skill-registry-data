---
name: log-progress
description: Append a dated entry to MEMORY.md when a milestone lands.
  Use when PLAN.md's checklist gains a [x], when a non-trivial bug is
  diagnosed and fixed, or when a design decision deserves a future
  breadcrumb. Newest entry goes on top; cite the commit.
allowed-tools: Read, Edit, Bash
---

# log-progress

`MEMORY.md` is the project's timestamped progress log. It's for
breadcrumbs future-you will actually read — not a changelog. Each
entry is a short story: what changed, why, what to remember.

## When to log

- A milestone in `PLAN.md`'s checklist flipped to `[x]`.
- A non-trivial bug was diagnosed and fixed. Include the diagnosis,
  not just the fix — the reasoning is the point.
- A cx self-hosting constraint was discovered or lifted. Also update
  `.claude/rules/cx-constraints.md` in the same pass.
- A design decision was made that would be confusing to a reader a
  month from now.

## When not to log

- Routine refactors, typo fixes, one-line tweaks.
- Anything the commit message already covers in full.
- "Today I tried X and it didn't work" — that belongs in the commit
  body or in conversation, not in a durable log.

## Entry format

Prepend below the header, above the previous entry. Newest on top.

    ## YYYY-MM-DD — <short headline>

    Commit: `<short-hash>` — <commit subject>

    <2–6 sentences. What changed. Why it mattered. What to remember.
    Point at files with `path:line` when helpful. Link back to rules
    files or PLAN.md milestones when relevant.>

    ---

## Before you write the entry

Run `git log --oneline -5` to pick up the commit hash. Don't invent
one. If the work isn't committed yet, don't log it yet — commit
first, then log, so the hash is real.

## After you write the entry

If the entry closes a `PLAN.md` milestone, make sure the checkbox in
`PLAN.md` is flipped to `[x]` in the same commit. The log and the
plan should stay in sync.
