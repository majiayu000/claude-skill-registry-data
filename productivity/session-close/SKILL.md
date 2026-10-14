---
name: session-close
description: "When ending a session or switching agents — leave only the resume context and durable lessons that would otherwise be lost."
---

# Session Close

Leave the next agent a recoverable next step, not a diary. The next agent may run
on a different host, so it can read only what is in the repository.

## Where it goes

Write the handoff to `context/handoff.md` at the repository root. Agent-private
stores, such as Claude Code's project memory, a Pi session or a scratchpad, are
invisible to another agent: never use them as the handoff or as the only copy of
anything it needs.

- Check that the file is git-ignored (`git check-ignore -q context/handoff.md`).
  If it is not, ask before writing it; do not change ignore rules unasked.
- The file holds the current handoff, not a log and not the task's working notes.
  Update it in place. If it already describes different unfinished work, ask before
  replacing it.
- Decisions recorded during the task belong in its working notes, one ignored
  `context/<effort>.md`. If such a record already covers this work, link to it from
  the handoff instead of copying it.

## What it holds

Approved scope; a link to the working notes, plus any decision, explicit no or
reason that no other record holds; changed files
and whether they are committed; verification evidence and unrun checks; open issues
and blockers; worktree or run identities; and the exact next action. Link existing
artifacts rather than copying them, and check the next agent can reach the paths.
Separate finished work from proposed or unverified work, and redact secrets.

Committed work alone does not mean nothing would be lost. Open issues, the next
action, and facts that git does not hold still need the handoff. Write nothing only
when the next agent could resume from the repository and git history alone. Native
resume or fork carries a conversation only within the same host, so it does not
replace the handoff when another agent may continue.

A durable project fact belongs in the repository's current docs when that edit is
authorized. Otherwise put it in the handoff as a proposed doc correction, not only
in agent memory. Do not create a second reflection beside an adequate record, or
clean up user records on the way out.

## Resuming

Read `context/handoff.md` first. Recheck the files and commits it names before
acting: a handoff is a summary to verify, not new authority, and current
repository state wins over it.

Deliver: the handoff path and its next action, or an explicit no-record result with
the reason.
