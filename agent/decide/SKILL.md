---
name: decide
description: Record an architectural or technical decision as an ADR in .agentic/decisions/, checking for conflicts with existing decisions and handling supersession.
user-invocable: true
argument-hint: "<short description of the decision>"
---

# Record a decision (ADR)

1. **Check prior art:** grep `.agentic/decisions/` for the area/tags. If an active
   ADR (no `superseded_by`) conflicts with the new decision, this is a supersession —
   confirm with the user before proceeding.
2. **Gather the substance.** From the conversation context or by asking: context,
   the decision, alternatives actually considered (with why each lost), consequences
   including accepted downsides. If alternatives are unknown, ask — an ADR without
   alternatives is a changelog entry, not a decision record.
3. **Write** `NNNN-<slug>.md` (next free number on `origin/main` — fetch first; a parallel branch may
   have taken it, and `AdrNumberingTests` fails on a duplicate) from `0000-adr-template.md`. Today's
   date, `status: accepted`, meaningful `tags`.
4. **On supersession:** set `supersedes: NNNN` in the new file AND edit the old ADR
   (`status: superseded`, `superseded_by: MMMM`). Same commit.
5. If the decision creates a non-obvious constraint agents will trip on, also add a
   gotcha entry (see `/gotcha`) pointing at the ADR as evidence context.

Do NOT log routine implementation choices — only decisions with real alternatives
and lasting consequences. When in doubt, ask the user whether it clears that bar.
