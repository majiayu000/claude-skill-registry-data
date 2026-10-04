---
name: hypothesis-driven-strategy
description: "Structures a strategic question into an initial, provably-wrong hypothesis and a MECE issue tree, then prioritizes testing the branch most likely to kill the hypothesis first. Use when a strategic question needs a defensible, decision-ready point of view quickly, instead of either guessing an answer or trying to analyze everything before forming one."
---

# Hypothesis-Driven Strategy

## Purpose

Structures a strategic problem with MECE and an issue tree, then tests the
resulting hypotheses against data — instead of either guessing an answer or
trying to analyze everything before forming a point of view.

## Anchored in research

- McKinsey — MECE / issue trees / hypothesis-driven problem solving
- Liedtka (1998) — hypothesis-driven
- Conn & McLean (2018), *Bulletproof Problem Solving* — a detailed, published
  account of this exact method: state a hypothesis early, break it into a
  MECE issue tree, and prioritize the branches by how cheaply and decisively
  they can be tested.

## Method

1. **State an initial hypothesis** — your best current answer to the strategic
   question, stated specifically enough to be provably wrong. "We should grow"
   is not a hypothesis; "we should grow by expanding into segment X before
   competitor Y does" is.
2. **Break the question behind the hypothesis into a MECE issue tree.** Each
   branch should be a sub-question that must be true for the hypothesis to
   hold, and the branches together should cover the question completely
   without overlapping (Mutually Exclusive, Collectively Exhaustive).
3. **For each branch, define the minimum evidence that would prove or
   disprove it** — not "more data is better," but the smallest, cheapest,
   most diagnostic piece of evidence that would move your confidence.
4. **Prioritize branches by diagnostic value, not by ease of access.** Test
   the branch most likely to kill the hypothesis first — a hypothesis that
   survives its own strongest challenge is far more useful than one that was
   only ever tested against easy questions.
5. **Update the hypothesis as evidence comes in.** This is iterative, not a
   single pass: a disproven branch should change the hypothesis itself, not
   just get logged as a caveat.
6. **Stop when the hypothesis is decision-ready**, not when the tree is
   exhaustively filled in — the goal is a defensible point of view fast
   enough to act on, not total analysis.

## What this skill does NOT do

- Doesn't make the final decision for you — it produces a structured draft to
  support a human decision.
- Doesn't confirm figures, market data, or competitor data from memory — it
  uses the inputs you provide, or marks an assumption clearly
  (`[assumption — verify]`).
- Doesn't collect or analyze data on your own behalf — it structures the
  questions the data needs to answer.

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

- Next in this pack: [`../scenario-and-foresight/SKILL.md`](../scenario-and-foresight/SKILL.md) — Builds alternative future scenarios and stress-tests a strategy against them.
- A ready-made skill chain for this situation: see [`../../../playbooks/`](../../../playbooks/)
- This pack's shared guardrails: [`../../CLAUDE.md`](../../CLAUDE.md)

## References

- [`../../references/`](../../references/) — the pack's shared background material
- [`../../CLAUDE.md`](../../CLAUDE.md) — the pack's shared guardrails
