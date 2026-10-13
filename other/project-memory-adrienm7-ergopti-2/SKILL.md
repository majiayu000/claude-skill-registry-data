---
name: project-memory
description: Consult or maintain routed project memory without loading unrelated topics. Use for unfamiliar work or durable repository discoveries.
---

# Project memory

`docs/memory/README.md` is the routing index for hard-won knowledge. The actual
entries live beside it in focused files under `docs/memory/`.
`docs/PROJECT_MEMORY.md` is only a compatibility pointer for older clients.
This catalog is shared by every developer, agent and reviewer and replaces
agent-private memory stores.

## Consult it first

Read `docs/memory/README.md`, then only the topic files covering the area you
will touch. Do not load every topic by default. A meaningful share of "new"
bugs in this repo are documented recurrences.

## What belongs here

Something **non-obvious**, **durable**, and written in **English**: a foot-gun that cost real debugging
time, an invariant that is not visible from the code, a decision whose rationale
would otherwise evaporate, an intentional asymmetry that looks like a bug.

What does **not** belong: anything the repo already records — code structure, the
content of a fix (that is the commit), git history, or universal rules already
written in `AGENTS.md`. Do not restate; link instead.

## Entry format

Add the entry to the narrowest existing topic file.

```markdown
### slug-with-dashes

One concise paragraph naming the mechanism and the action future work must take.
```

Use dash-separated slug headings. Keep entries short enough to scan and link
directly to code/tests when that is more useful than restating them.

## Writing well

- **Be concrete.** "Guard the map access" is useless; name the file, the key, the
  failure mode, and what the symptom looked like.
- **Convert relative dates to absolute.** "Last week" is meaningless in six months.
- **Record the symptom, not just the cause** — that is the string a future reader
  searches for when they hit it again.
- **Check for an existing entry first** and extend it rather than adding a near
  duplicate. Delete entries that turn out to be wrong.
- **Delete stale history.** Completed audit transcripts, branch narratives,
  commit summaries, temporary measurements, and TODO snapshots belong in Git,
  not project memory.
- **Verify before trusting.** Entries reflect what was true when written. If one
  names a file, function or flag, confirm it still exists before acting on it —
  and correct it if not.

## Cadence

Add or update entries proactively at the end of a task, without being asked.
Prune obsolete material at the same time. Put measured rejected ideas in
`docs/memory/rejected_proposals.md`, not among implementation invariants. Then
commit without pushing, per the `commit-and-push` skill.
