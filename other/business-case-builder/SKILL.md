---
name: business-case-builder
description: "Builds a full business case — problem, options considered (including \"do nothing\"), economics (ROI/NPV/IRR), risk, stakeholders, milestone-level timeline, and recommendation — following BABOK/PMI structure. Use when a proposal needs to reach a decision-maker as a structured business case, not a pitch with only one option on the table."
---

# Business Case Builder

## Purpose

Builds a full business case: problem, solution, economics (ROI/NPV/IRR), risks, timeline, stakeholders, recommendation.

## Anchored in research

- IIBA BABOK
- PMI Business Analysis
- w95/awesome-claude-corporate-skills — business-case-builder structure

## Method

1. **State the problem or opportunity in business terms first** — the gap
   between the current and the desired state — before any solution is named.
   A business case that opens with the solution has already skipped the
   justification step BABOK requires.
2. **Lay out the options actually considered, including "do nothing" as a
   baseline** — a business case with only one option isn't a comparison,
   it's a pitch. The cost of inaction (of the status quo continuing) is what
   the recommended option has to beat.
3. **Build the economic case using this pack's
   [`roi-npv-sensitivity-model`](../roi-npv-sensitivity-model/SKILL.md) skill**
   for the cost/benefit analysis (ROI/NPV/IRR, sensitivity) — don't compute
   the financials inline here; reference the dedicated skill so the numbers
   stay in one place and follow one method.
4. **Bring in risk (via
   [`risk-matrix-and-mitigation`](../risk-matrix-and-mitigation/SKILL.md)) and
   stakeholder mapping (via
   [`stakeholder-analysis-and-raci`](../stakeholder-analysis-and-raci/SKILL.md))
   as sections of the case rather than afterthoughts** — PMI's business
   analysis practice treats these as integral to the recommendation, not an
   appendix.
5. **Sequence the implementation at a milestone level (not a detailed
   project plan)** — enough to show the case is achievable in the proposed
   timeframe, with dependencies flowing from the other sections (e.g. a
   resourcing risk flagged in the risk matrix should show up here too).
6. **Close with an explicit recommendation and the decision being asked of
   the reader** — what they're being asked to approve, by when, and what
   happens if they don't decide.

## What this skill does NOT do

- Doesn't make the final decision for you — it produces a structured draft to
  support a human decision.
- Doesn't confirm figures, market data, or competitor data from memory — it
  uses the inputs you provide, or marks an assumption clearly
  (`[assumption — verify]`).
- Doesn't approve a budget or make the investment decision — it produces
  decision-ready material for whoever does approve it.

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

- Next in this pack: [`../roi-npv-sensitivity-model/SKILL.md`](../roi-npv-sensitivity-model/SKILL.md) — Calculates ROI, NPV, and IRR plus a sensitivity analysis across scenarios.
- Before this (if there's a demo or PoC behind it whose results feed in as
  input): [`../../../prototyping-and-demonstration/skills/demo-to-business-case-bridge/SKILL.md`](../../../prototyping-and-demonstration/skills/demo-to-business-case-bridge/SKILL.md)
  — translates the demo's results into validated ROI inputs with a
  transparent assumption chain before they're used here.
- A ready-made skill chain for this situation: see [`../../../playbooks/`](../../../playbooks/)
- If the case is for a public-sector, municipal, or non-profit client:
  frame the value case first with
  [`../../../specialisation-packs/public-sector-ai-service-design/skills/ps-public-value-business-case-framing/SKILL.md`](../../../specialisation-packs/public-sector-ai-service-design/skills/ps-public-value-business-case-framing/SKILL.md)
  — public value (efficiency, service quality, equity, trust) often
  doesn't reduce to a pure ROI story the way this skill's default
  economics section assumes.
- This pack's shared guardrails: [`../../CLAUDE.md`](../../CLAUDE.md)

## References

- [`../../references/`](../../references/) — the pack's shared background material
- [`../../CLAUDE.md`](../../CLAUDE.md) — the pack's shared guardrails
