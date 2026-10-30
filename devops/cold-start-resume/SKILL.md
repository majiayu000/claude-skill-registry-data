---
name: cold-start-resume
description: >-
  Survey what changed before resuming work after a literal interruption: an app restart, a context cap, a
  machine sleep, a crash, or "resume" / "continue from where we left off" after the session went quiet while
  other sessions, the user, or automated jobs could have touched the repository. Trigger phrases include
  "cold start", "resume", "I had to restart", "continue from where we left off", "we may have changed files
  during the pause", "verify before writing". Do NOT use on the first turn of a brand-new session, or for a
  plain status question ("what's the state of X"), which is answered directly.
license: Apache-2.0
metadata:
  author: Marc Taccolini
  version: 1.1.0
---

# Cold-Start Resume: survey before you write

**A note is history. The system is state.** Whatever this session remembers, and whatever any resume
note, job file, or summary says, describes the repository as it was. Other sessions, the user, and
scheduled jobs kept working while this one was offline. Resume from what is true now.

Resuming without checking produces three failures: redoing work a parallel session finished, overwriting
edits made during the pause, and telling the user something is pending when it shipped an hour ago.

## The survey (read-only: write nothing until it is done)

Run it in one batch. Breadth first, depth only where something moved.

1. **Your own artifacts.** For each file or object this session was building, read it back by name. If
   it changed after your last edit, someone else touched it: read the new state, then confirm the
   markers your edit introduced are still there.
2. **What moved since you left.** `git log --since=<when you paused>` and `git status`. New commits and
   uncommitted changes from other sessions are the map of parallel work.
3. **The live record.** The tracker, decision log, and changelog the repository uses. A row you were about
   to fill may be done. **A decision made elsewhere may have retired your task entirely.** Check for that
   before checking progress.
4. **Outside the repository.** Files on disk do not capture what happened in other systems: a merged or
   closed PR, a CI result, an issue comment, a deploy, a reply in a message thread. Re-query every
   external system the work touched. This is the step most often skipped and the one that produces the
   most confident wrong claims.
5. **Other sessions' notes.** Recent session records or drafts dated inside your pause window are
   parallel work. Read enough to know whether they overlap yours. Never silently continue another
   session's work.

**An empty result is a finding to check, not a clean bill.** A glob that is not recursive, a search run in
the wrong directory, or a query against a source that does not hold the answer all return nothing, and
nothing reads as "no changes". Before you report "no parallel work", confirm the probe could have found
some.

## Report, then continue

Give the user five short lines before the first write:

- **Intact:** your work that survived unchanged.
- **Changed:** what others moved, with where you saw it.
- **Still open:** items from before the pause that are still open now.
- **No longer open:** items that finished, or were retired by a decision, during the pause.
- **Needs you:** only what you cannot settle yourself.

Then resume on the current state, not the remembered one.

## Anti-patterns

- Continuing "where we left off" by writing before the survey.
- Assuming a background agent from before the pause is still alive. It is not; treat its last output as
  final.
- Appending a second changelog entry for work a parallel session already logged.
- Treating another session's draft as authoritative. It may be unapplied or superseded.
- Trusting a state line in a note without re-running the check that produced it.
