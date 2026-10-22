---
name: meeting
description: Tidy a meeting note by filling its frontmatter and adding a summary, decisions and per-person action items around my raw notes. Use when asked to clean up, summarize or process a meeting note.
argument-hint: "[note]"
---

# Meeting cleanup

The target is the note I name, else the newest note in `Meetings/`. An Inbox note
that is clearly a meeting moves to `Meetings/YYYY-MM-DD Topic.md` first (see /inbox).

1. Read it. Everything I wrote stays, word for word apart from unmistakable typos.
2. Frontmatter: `date` (from the file name or the content), `attendees` (the people
   and teams in it, plain text), `project` (`"[[Project]]"` only if that note
   exists), and a one-line `summary`.
3. Add `## Summary` (2–4 sentences) directly after the frontmatter, then
   `## Decisions` (bullets; leave it out if there were none).
4. In `## Actions`, add an item for every action the notes support, as
   `- [ ] Name: task`, grouped by person, with `Nickolaj` for mine. Put an owner
   prefix on existing items only where the owner is clear, and use `?` where it
   isn't. Never invent decisions or actions.
5. Finish with `git diff` of the note.
