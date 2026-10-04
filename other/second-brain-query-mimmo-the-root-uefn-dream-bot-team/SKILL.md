---
name: second-brain-query
description: How to query second-brain-librarian efficiently — ask for exactly what you need, not "everything about X." Read before invoking it in query mode (coder checking for a reusable pattern, project-bootstrap checking retention track record) to keep the round-trip and its answer short.
---

# Querying the second brain efficiently

`second-brain-librarian` reads the vault's own `CLAUDE.md` and can produce a thorough answer —
but a vague, broad question makes it read more of the vault and write a longer answer than the
task needs. Ask narrowly.

## Rules
- **Ask for the specific thing, not the topic.** "What's the current Verse snippet and
  Visto/testato su list for the Elimination Manager pattern?" — not "tell me everything about
  Elimination Manager."
- **Prefer a `type: synthesis` article when one might exist.** If you're about to ask about two
  or three related concepts together, ask first whether a synthesis article already combines
  them — one citation instead of stitching together several component articles yourself.
- **State what you'll do with the answer**, briefly — it helps the librarian judge how much
  detail actually matters (a snippet to adapt needs the code; a track-record check just needs
  the outcome, not the full article).
- **Don't re-query for the same thing twice in one session** — if you already asked and got "no
  match," don't ask again a different way hoping for a different answer; proceed as if the
  pattern doesn't exist yet.
- **Never ask it to summarize the whole vault** or a whole thematic wiki "just in case" — that's
  exactly the kind of broad request this skill exists to avoid.
