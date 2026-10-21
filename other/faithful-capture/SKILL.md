---
name: faithful-capture
description: |
  Capture what someone actually said without contaminating it with your own inference.
  Invoke when eliciting intent in conversation (design discussion, requirement interview,
  decision surfacing) and when turning a conversation into a durable record (ADR, decision
  node, memory entry, spec `## Decisions` row). Enforces quote-before-critique, keeps
  illustration separate from commitment, and holds interpretation subordinate to verbatim.
  Prevents the failure where unspecified space is filled by the recorder and then evaluated
  as if the speaker had specified it.
---

# faithful-capture — record what was said, not what you inferred

You are capturing intent that lives in someone else's head. The output is either a
turn of conversation or a durable record. In both cases the failure mode is identical:
**you fill space the speaker left unspecified, then treat your filling as theirs.**

In conversation this costs the speaker a turn of reclaiming ground they never conceded.
In a durable record it costs far more — a fabricated node gets cited later, defended by a
future session as established fact, and outlives the context needed to detect it.

This skill is a discipline, not a phase. It runs inside whatever is doing the capturing.

## Consumers

| Caller | What it is capturing | Where it lands |
|---|---|---|
| Interview / design dialogue | The speaker's intent, mid-formation | Conversation, then a brief or spec |
| ADR authoring | A fork that was taken, and why | Decision node / ADR |
| Decision extraction from `_pending` | Forks detected in prior conversation | Curated decision record |
| Memory promotion | A rule or lesson the user stated | Canonical memory entry |

## The eight rules

Each rule names the tell that detects a violation and the repair. The tells are mechanical —
apply them to your own draft before it ships.

### R1 — Quote before you critique

Before evaluating any element, locate the speaker's actual words for it.

- **Tell:** you are about to criticize something you cannot quote from what they wrote.
- **Repair:** you have no target. Convert the criticism into a question, or delete it.

An unquotable critique is always self-critique wearing someone else's name. This is the
parent rule; R2, R3 and R4 are the three ways it gets violated.

### R2 — Illustration is not commitment

`for example`, `like`, `e.g.`, `etc`, `say`, `something such as` mark an item as
illustrative. Illustrations show the *shape* of a category. They are not proposals.

- **Tell:** you are evaluating a list item that arrived under an example marker.
- **Repair:** treat the category as proposed and the item as disposable. If the item
  matters, ask whether it was meant as a commitment.

### R3 — Unspecified is not maximal

When a speaker states a mechanism without stating its bound, the bound is *open*, not
*maximal*. Do not assume the extreme reading and then argue against it.

- **Tell:** your objection contains a quantifier (`everywhere`, `always`, `every`, `all`,
  `never`) that does not appear in their text.
- **Repair:** ask for the bound. "Where would these go — all call sites, or specific ones?"

### R4 — An open shape is not a defect

A speaker who deliberately leaves structure, ordering, or sequencing undecided has not
created a problem. Deriving a hazard from a shape they have not chosen is fabrication
dressed as risk analysis.

- **Tell:** your hazard depends on an ordering, boundary, or structure you supplied.
- **Repair:** name the fork instead of the hazard. "Ordering matters here — if X runs
  before Y you get one set of constraints, after Y you get another. Which way were you
  leaning?"

### R5 — Completion is the speaker's to declare

You have no reliable signal for whether an exposition is finished. A pause is not
completion. Never infer it.

- **Tell:** you are about to summarize, audit, or identify gaps in something the speaker
  is still laying out.
- **Repair:** ask. "More to lay out, or do you want reactions?" One line removes this
  entire class of error.

### R6 — Contributing and evaluating are different acts

Contribution offers something adjacent the speaker may not have weighed. Evaluation
judges what they have. Contribution is legal at any point. **Evaluation requires a target
that both exists and has been declared complete.**

- **Tell:** your contribution is framed as a deficiency — "the risk none of this
  addresses", "what's missing here", "this doesn't account for".
- **Repair:** state the consideration as a consideration. The information is identical;
  the framing is the entire difference between something usable and something the speaker
  has to defend against.

### R7 — Propose anyway

The defect is unearned certainty and adversarial framing. It is **not** having views.
Do not overcorrect into pure elicitation.

Anchor-and-correct converges faster than open probing whenever the speaker has taste and
correction is cheap: proposing gives them something concrete to push against, where open
questions make them generate the whole answer unaided. A capture skill that refuses to
propose is slower and produces thinner records.

- **Tell:** three or more consecutive turns containing no substantive contribution.
- **Repair:** propose, with the uncertainty marked and the frame set to contribution.

### R8 — Verbatim outranks interpretation

The speaker's words are canonical. Your reconstruction of their reasoning is subordinate,
and must be visibly marked as yours. On conflict, verbatim wins and you surface the
conflict rather than resolving it silently.

- **Tell:** a record contains rationale with no traceable source in what was said.
- **Repair:** either attribute it to the speaker with a quote, or label it as
  reconstruction. Never let the two blur.

This extends CLAUDE.md Article IX clause 6 (verbatim canonical for `user-instruction` /
`user-feedback`) to decision capture, where the stakes are the same and the record is
longer-lived.

## Pre-output gate

Run this against your own draft before it ships. It is mechanical.

1. **Scan for evaluative statements.** For each, can you quote its target from the
   speaker's text? No quote → convert to a question or cut it. (R1)
2. **Scan for example markers** in what you are treating as proposed. Anything under
   `for example` / `etc` is illustration, not schema. (R2)
3. **Scan your own quantifiers.** Every `everywhere` / `always` / `never` that is not in
   their text is an invented bound. (R3)
4. **Scan hazards for supplied structure.** If the hazard needs an ordering they did not
   choose, it is a fork to name, not a risk to raise. (R4)
5. **Check completion.** Are you auditing something still being laid out? Ask instead. (R5)
6. **Check framing.** Rewrite any contribution currently shaped as a deficiency. (R6)
7. **Check substance.** If the last few turns were all questions, contribute. (R7)

## Interview leg

Applies to design dialogue, requirement elicitation, and decision surfacing.

- Open by asking whether the speaker is laying out or wants reactions. Re-ask when the
  topic shifts. (R5)
- Propose freely, with uncertainty marked. Anchor-and-correct is the point. (R7)
- Track two lists as you go: **stated** (quotable) and **inferred** (yours). Only the
  first is available as a critique target. Surface the second explicitly when it starts
  carrying weight — "I've been assuming X; is that right?"
- When the speaker corrects you, absorb without defending. A correction is data about the
  target, which is the thing you are here to capture.
- Never convert an open fork into a settled one by proceeding as if it were decided.

## ADR / decision-record leg

Applies when a conversation becomes a durable node.

- **The fork must be quotable.** Record a decision only where the speaker actually chose.
  A choice you inferred from their code, silence, or adjacent statements is at best a
  candidate, and is marked as one.
- **Rejected alternatives must have been considered.** An option nobody raised is not a
  rejected alternative. Unexplored space is unexplored, and saying so is more honest than
  a fabricated rejection with an invented reason.
- **Rationale carries provenance.** Split the record: what the speaker said, and what you
  reconstructed. Both are useful; conflating them is what makes a node undefendable later.
- **Absence is not a decision.** Scope that was never discussed is not scope that was cut.
  Only record a cut where there is a cut to quote.
- **Uncertain capture stays a candidate.** When a fork is real but the rationale is thin,
  record the fork and mark the rationale open. A node flagged incomplete is recoverable;
  a node confidently wrong is not.

## Constraints

- Runs in main context (CLAUDE.md Article II). It informs a written record or a spoken
  turn, both of which are binding judgment — never delegate it to a subagent.
- Advisory to the caller's own output discipline. It writes no artifact of its own.
- Does not gate or slow a conversation. R7 exists specifically so that applying this
  skill does not degrade into interrogation.
- Where this skill and Article IX clause 6 both apply, Article IX governs — this skill
  extends its reach, never relaxes it.

## Provenance

Derived from an observed failure in a live design conversation about decision-trail
architecture (2026-07-31), where four distinct objections from the user all reduced to a
single mechanism: unspecified space filled by the recorder, then evaluated as the
speaker's own. R1–R6 are the taxonomy of that mechanism. R7 guards the overcorrection.
R8 connects it to existing constitutional doctrine.
