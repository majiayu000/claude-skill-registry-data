---
name: roi-npv-sensitivity-model
description: "Calculates ROI, NPV, IRR, and payback period against a credible do-nothing baseline, then runs a one-at-a-time sensitivity analysis to rank which two or three assumptions actually drive the result, plus upside/downside scenarios. Use when a business case's financial numbers need to survive scrutiny, not just look attractive under the base case."
---

# ROI / NPV Sensitivity Model

## Purpose

Calculates ROI, NPV, and IRR plus a sensitivity analysis across scenarios.

## Anchored in research

- w95 business-case-builder
- aj-geddes — business-case-development

## Method

1. **Establish the cash-flow baseline** — incremental costs and benefits by
   period, compared against a credible do-nothing baseline, not against
   zero. ROI and NPV overstate the case if they're compared to nothing
   happening instead of to what would happen anyway.
2. **Select and justify a discount rate** (e.g. WACC, an internal hurdle
   rate, or the organization's standard rate) — never invent this figure;
   ask for it, use a marked placeholder, or use a clearly flagged
   conservative default.
3. **Compute NPV (the sum of discounted net cash flows), IRR (the discount
   rate at which NPV = 0), payback period, and ROI (net benefit ÷ cost) side
   by side** — a single metric can look attractive while another flags a
   problem, e.g. a fast payback period paired with a negative NPV at the
   real discount rate.
4. **Run a one-at-a-time sensitivity analysis:** vary each key input
   (adoption rate, unit cost, benefit-realization timing, discount rate) by a
   defined range (e.g. ±20%) while holding the others constant, and rank the
   inputs by how much they move NPV. This produces a tornado chart that
   identifies which two or three assumptions actually drive the result.
5. **Build at least a downside (pessimistic) and an upside (optimistic)
   scenario, not only the base case** — a sensitivity analysis whose worst
   case still looks comfortable isn't a real stress test.
6. **Report the breakeven point for the most sensitive variable** (e.g.
   "adoption has to exceed X% for NPV to stay positive") so the
   decision-maker sees exactly which assumption they're betting on.

## Available scripts

- **`scripts/roi_npv_model.py`** -- calculates NPV, IRR (bisection search),
  payback period, and ROI from a list of incremental net cash flows
  (already vs. the do-nothing baseline, per Method step 1), then runs the
  one-at-a-time sensitivity analysis from step 4, an upside/downside
  scenario pair from step 5, and the breakeven estimate from step 6. Run it
  once cash flows and a discount rate are known, instead of computing NPV/
  IRR by hand -- it also catches the sign-flip cases (no IRR in a sane
  range) that are easy to get wrong manually.

  ```bash
  python3 scripts/roi_npv_model.py --example > input.json   # see the input shape
  python3 scripts/roi_npv_model.py input.json                # or: ... - <<< '{...}'
  ```

  Stdlib only (json, argparse, math) -- no install needed. Exit code 1 on
  invalid input (missing discount_rate, fewer than 2 cash-flow periods),
  with a specific error on stderr.

## What this skill does NOT do

- Doesn't make the final decision for you — it produces a structured draft to
  support a human decision.
- Doesn't confirm figures, market data, or competitor data from memory — it
  uses the inputs you provide, or marks an assumption clearly
  (`[assumption — verify]`).
- Doesn't invent precise currency amounts — it calculates from the baseline
  values you provide and makes every assumption visible.

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

- Next in this pack: [`../risk-matrix-and-mitigation/SKILL.md`](../risk-matrix-and-mitigation/SKILL.md) — Identifies and scores risks (probability × impact) and designs mitigations.
- Before this (if the inputs come from a demo/PoC):
  [`../../../prototyping-and-demonstration/skills/demo-to-business-case-bridge/SKILL.md`](../../../prototyping-and-demonstration/skills/demo-to-business-case-bridge/SKILL.md)
  — run the sensitivity analysis especially on the assumptions that skill
  flagged as weakest in the assumption chain.
- A ready-made skill chain for this situation: see [`../../../playbooks/`](../../../playbooks/)
- This pack's shared guardrails: [`../../CLAUDE.md`](../../CLAUDE.md)

## References

- [`../../references/`](../../references/) — the pack's shared background material
- [`../../CLAUDE.md`](../../CLAUDE.md) — the pack's shared guardrails
