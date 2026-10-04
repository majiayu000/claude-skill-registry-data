---
name: close-issue
description: Close or park this workspace — a retrospective on what changed, what didn't, and what graduates to the persistent background context layer. Use when the user says "I think this is done", or when a review finds the issue has gone quiet for months.
---

# close-issue

Workspaces are meant to end. An issue-bounded workspace that never closes becomes the general
dumping ground it was designed not to be.

## Two endings

- **Closed** — the issue is resolved, or has stopped being live. Final retrospective, graduate
  what's durable, set `status: closed`.
- **Dormant** — not resolved, but not currently worth the attention. Same procedure, lighter, and
  `status: dormant`. It can be woken up. Say so; parking something is not failing at it.

## Procedure

1. **Read everything.** All sessions, all threads, all artefacts, the reviews. This is the one
   time a full read is warranted.

2. **Write `artefacts/retrospective-YYMMDD.md`:**

   ```markdown
   # Retrospective — <issue>

   Open from <date> to <date>. <n> sessions.

   ## What this turned out to be about
   Often not what context/issue.md said on day one. Compare the two honestly.

   ## What changed
   In the situation, and separately, in how they see it. The second is more common
   and counts just as much.

   ## What didn't change
   Plainly. No consolation prize framing.

   ## What helped
   Which of this actually did anything — the writing, the timeline, the appointment
   it fed, the conversation it made possible. Be specific; this is what tells them
   whether to open another workspace.

   ## What I'd do differently next time
   Theirs, in their words, not yours.

   ## Still open
   What is unresolved and deliberately left that way.
   ```

3. **Graduate what's durable.** Run `context-sync`. The test for the background context store is
   what would still be true and useful in a workspace about something else:
   - a person's role, and how that relationship actually works
   - a pattern that showed up here but isn't specific to this issue
   - something learned about how they want to be talked to → `preferences`
   - dated events that belong to their history rather than to this issue
   - what helped and what didn't, when things are hard

   Not: the incidents, the threads, the drafts, the arguments. Those stay here.

4. **Update `context/issue.md`** — `status:`, a closing line in Revisions, and the date.

5. **Tidy.** Move open threads to `archive/` with a status line each. Update `threads/INDEX.md`
   and `artefacts/INDEX.md`. Delete nothing.

6. **Say what happens to the repo.** It stays private, it stays readable, and it can be reopened
   by setting `status: open` and starting a session. If they want it gone, that's their call and
   it's a `git` operation they should run themselves.

## Rules

- **Do not close on your own initiative.** You can observe that a workspace has been quiet for
  three months; the decision is theirs.
- **No graduation ceremony.** No "you've come so far". A retrospective that flatters is a
  retrospective nobody trusts.
- **Nothing graduates without confirmation,** entry by entry.
- If closing surfaces something big — it usually does, right at the end — stop the procedure and
  stay with the conversation. The retrospective can wait a week.
