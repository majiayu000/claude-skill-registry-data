---
name: design
description: "When intent or consequential choices are unclear — resolve goals, boundaries, contracts, and an approved direction before building."
---

# Design

Find the real need before committing to a solution. A clear bounded request can
already supply approved intent; do not turn it into another interview.

- Read what the repository can answer. Separate discoverable facts, user-owned
  choices, and knowledge held by an absent stakeholder. Research and delegated
  evidence inform decisions; they do not authorize them.
- Ask about consequential uncertainty: outcome, audience, non-goals, constraints,
  data and failure behavior, acceptance, and hard-to-reverse choices. Use concrete
  scenarios to expose ambiguous terms or contradictions; check claimed behavior
  against the code before treating it as a fact. Challenge a fashionable solution
  when a simpler one solves the actual problem.
- Bundle dependency-ready questions into a short round. Include a grounded
  recommendation, worded so a plain yes accepts it, and meaningful alternatives;
  ask separately when one answer would reframe the rest. Do not demand arbitrary
  option counts or explore every hypothetical branch. Block only work that depends on an unresolved answer.
- If someone else holds the answer, establish the recipient and needed outcome,
  then prepare a focused questionnaire. Each question should stand alone, lead
  with what matters most, and welcome partial answers or uncertainty. Do not
  invent the absent person's preference.
- State the proposed outcome, exclusions, contracts, test seams (what each
  catches and misses), assumptions and consequential trade-offs clearly enough
  to approve. Approval means the user
  agreed to this direction in context; no magic word is needed, and silence is
  not approval. A material expansion needs fresh approval. If no decision-maker
  is available, report the blocked choice rather than guessing through it.
- Prefer small verifiable, reversible outcomes. Probe load-bearing assumptions
  before designing around them; name what would invalidate the direction.
  Compare architecture or build an authorized prototype when evidence would
  settle the choice more cheaply than discussion.

For dependent choices spanning sessions, use [Decision frontier](references/DECISIONS.md)
inside the task's existing working notes (one ignored `context/<effort>.md`),
never the handoff file. When continuity needs it and writing is authorized,
capture settled constraints, explicit no-s, ordering/numeric requirements and their
reasons as they land, not only in a final summary. Put agreed terms beside the
contract they clarify; a glossary is not a spec. No per-question record, glossary,
or planning artifact is required merely to finish an interview.

Deliver: approved intent and boundaries, acceptance/contract decisions, unresolved
prerequisites and their owners. Proceed within clear implementation authority;
use a plan when risk, dependencies or handoff need one. `plan` and `implement`
defer to these approval rules.
