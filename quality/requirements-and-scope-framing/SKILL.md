---
name: requirements-and-scope-framing
description: "Classifies requirements using BABOK's four types (business, stakeholder, functional, non-functional, transition), checks each against the IEEE 830 quality bar (correct, unambiguous, verifiable), and separates in-scope from explicitly out-of-scope items. Use before requirements are locked in, when scope keeps drifting or vague requirements like \"the system should be fast\" are passing unchallenged."
---

# Requirements & Scope Framing

## Purpose

Frames the problem and requirements into a clear, testable whole.

## Anchored in research

- BABOK — requirements
- IEEE 830

## Method

1. **Capture the raw problem statement and classify each candidate
   requirement** using BABOK's four requirement types — business requirements
   (the why: goals and objectives), stakeholder requirements (the needs of a
   specific stakeholder group), solution requirements split into functional
   (what the solution must do) and non-functional (quality attributes:
   performance, security, usability), and transition requirements (what's
   only needed to move from the current state to the future one). Anything
   that doesn't fit cleanly gets flagged for further elicitation before
   scoping continues.
2. **Elicit missing requirement types with structured techniques** (BABOK:
   interviews, workshops, document analysis, observation) rather than
   inferring them silently — any requirement not sourced from a stakeholder
   or document is an assumption and must be marked as one.
3. **Check each requirement against the IEEE 830 SRS quality checklist:** is
   it correct, unambiguous, and verifiable (testable), and is it consistent
   with the other requirements and traceable to its source? A requirement
   that fails "verifiable" (e.g. "the system should be fast") gets rewritten
   with a measurable threshold, or flagged as needing one.
4. **Separate in-scope from explicitly out-of-scope items in a single
   list** — an unscoped boundary is as costly as a wrong requirement, because
   it seeds disagreement later.
5. **Rank requirements on IEEE 830's importance/stability dimension** — which
   are core and stable versus likely to change — so that scope decisions made
   under pressure protect the right things first.
6. **Validate the resulting scope statement with stakeholders explicitly**,
   tracing each requirement back to whoever asked for it (traceability)
   before treating the scope as locked.

## What this skill does NOT do

- Doesn't make the final decision for you — it produces a structured draft to
  support a human decision.
- Doesn't confirm figures, market data, or competitor data from memory — it
  uses the inputs you provide, or marks an assumption clearly
  (`[assumption — verify]`).
- Doesn't finalize a requirements specification without stakeholder
  confirmation.

## Refinement notes

Areas to keep deepening with real practice:

- your own rules of thumb and heuristics for this technique
- concrete templates (into [`../../references/`](../../references/))
- reference cases / your own examples
- what this skill deliberately does *not* do (guardrails, common mistakes) —
  add to the list above

This is an internal working note, not a claim about the skill's current
usability. Track depth privately via the `maturity` field in
`skills_index.json` (see
[`../../../meta/maturity_levels.md`](../../../meta/maturity_levels.md)).
**Don't add new fields to the frontmatter** — `name` and `description` are
the only ones allowed (see
[`../../../meta/frontmatter_schema.md`](../../../meta/frontmatter_schema.md)).

## Continue from here

- Next in this pack: [`../stakeholder-analysis-and-raci/SKILL.md`](../stakeholder-analysis-and-raci/SKILL.md) — Maps stakeholders on a power/interest matrix and assigns responsibilities with RACI.
- A ready-made skill chain for this situation: see [`../../../playbooks/`](../../../playbooks/)
- This pack's shared guardrails: [`../../CLAUDE.md`](../../CLAUDE.md)

## References

- [`../../references/`](../../references/) — the pack's shared background material
- [`../../CLAUDE.md`](../../CLAUDE.md) — the pack's shared guardrails
