---
name: documenting
description: >-
  Writes project docs in the right place. Use when the user asks to document something, record a decision, write an ADR, or update the README or docs. Not for code comments, commit messages or reviews.
license: Apache-2.0
metadata:
  level: "atomic"
  uses: ""
  agents: ""
  tokens: "548"
---

Put each fact in its one home, in the project's existing format, sized to the change.

## Steps
1. Find the homes: read CLAUDE.md `## Where things live` for the docs home and decision log (fallback: `docs/`, `docs/decisions.md`). Read the target file's tail and copy its format, numbering and tone.
2. Pick the home for the fact, then size it:
   - One-line fact: one line in the right existing place.
   - New subsystem or feature: a short doc in the docs home, linked from where readers start (README or CLAUDE.md `## Where things live`).
   - Changed command: update CLAUDE.md `## Commands`. User-facing change: README.
   - Decision: only if it passes all three gates below.
3. Update an existing doc instead of adding one; replace stale text rather than appending a contradiction.
4. Grep for other places that state the same fact and fix or link them. Check that each path and command you wrote exists or runs.

## Decision gates
When you decide on your own whether to log a decision, write an entry only when all three hold, otherwise skip it. When the user asks to record one, record it.
1. Hard to reverse: changing your mind later costs real work.
2. Surprising without context: a reader would ask "why this way?".
3. A real trade-off: genuine alternatives existed and one was chosen for stated reasons.

Entry: date, decision, alternatives, reason, status `proposed`, `accepted` or `superseded by <id>`. A superseded entry stays; mark it and link the new one. A decision that changes how code is written also gets one line in CLAUDE.md.

## Rules
- One home per fact: link to it, never copy it.
- No new `*.md` outside the docs home (README, CLAUDE.md, AGENTS.md, CHANGELOG, DESIGN.md excepted).
- Never put trees, dependency lists, overviews or generic advice into CLAUDE.md; only what code cannot show.
- README changes only for what users see; internals go to the docs home.
- Say which size you took (line, edit or new doc) in one line.

If you create a new doc, a decision log or a glossary, or the project has no docs yet, read `references/formats.md`.

## Report
- Files changed and what was recorded (or which gate failed and why nothing was written).
- Not checked: <…>
