---
name: demo-to-business-case-bridge
description: "Translates demo/PoC results into business-case-ready ROI inputs: separates technical performance metrics from business impact metrics, tests whether a PoC-scale result scales responsibly to production scale, and checks whether the assumed ROI mechanism fits the customer's actual organizational structure. Use immediately after a successful demo/PoC, before its results are fed into a business case or ROI calculation."
---

# Demo-to-Business-Case Bridge

## Purpose

Prevent the most common mistake made right after a demo: **extrapolating a
PoC-scale result in a straight line** into a production-scale ROI figure
without anyone checking whether the underlying assumption actually holds.
"Saved 2 hours across 10 test cases" doesn't automatically mean "saves 200
hours a month in production" — an explicit, checked chain of assumptions is
needed in between. This skill is the bridge between the demo evidence
produced by
[`../rapid-prototype-and-vibe-coding-craft/SKILL.md`](../rapid-prototype-and-vibe-coding-craft/SKILL.md)
and
[`../demo-delivery-and-storytelling/SKILL.md`](../demo-delivery-and-storytelling/SKILL.md)
and the structured economic case required by
[`../../../business-case-and-analysis/skills/business-case-builder/SKILL.md`](../../../business-case-and-analysis/skills/business-case-builder/SKILL.md)
and
[`../../../business-case-and-analysis/skills/roi-npv-sensitivity-model/SKILL.md`](../../../business-case-and-analysis/skills/roi-npv-sensitivity-model/SKILL.md).

## Anchored in research

- Research synthesis (2026) on translating demo/PoC results into business
  language: two distinct metric classes (technical performance and
  business impact), returning to the original hypothesis and to the
  baseline/success criteria, bringing finance in early to validate the
  measurement approach, and a warning that the ROI mechanism (e.g. "saves
  headcount hours") has to match the customer's actual organizational
  structure — if the organization can't or won't reduce headcount, an
  ROI based on labor savings won't materialize even if technical
  performance has been proven.

## Method

1. **Return to the original hypothesis and success criteria** (see
   [`../rapid-prototype-and-vibe-coding-craft/SKILL.md`](../rapid-prototype-and-vibe-coding-craft/SKILL.md)
   step 1 and
   [`../../../ai-strategy-and-governance/skills/ai-use-case-feasibility-and-poc-scoping/SKILL.md`](../../../ai-strategy-and-governance/skills/ai-use-case-feasibility-and-poc-scoping/SKILL.md)).
   Compare the demo's actual result to the original criterion as stated —
   don't let excitement (or disappointment) generated during the demo
   distort the assessment of whether the original criterion was met.
2. **Separate two metric classes clearly:**
   - **Technical performance** — accuracy, coverage, error rate, speed,
     measured under demo/PoC conditions. These are *leading indicators*,
     not business value yet.
   - **Business impact** — time savings, cost savings, new revenue,
     reduced risk, better decision-making. These MUST be derived from the
     technical results through an explicit chain of assumptions, not
     stated directly.
3. **Make the assumption chain visible for every business-impact figure:**
   "In the PoC, X happened with a sample of N → we assume the same holds
   at production scale, because [justification] → this implies Y in
   business value, assuming Z [e.g. usage rate, adoption rate]." If you
   can't fill in the justification convincingly, don't present the
   business figure as confirmed — mark it `[assumption — verify]` (see
   the pack's [`../../CLAUDE.md`](../../CLAUDE.md)).
4. **Check that the assumed ROI mechanism matches the customer's actual
   organizational structure and culture.** The most common pitfall: ROI is
   based on an assumed reduction in headcount, but the customer's
   organization doesn't intend or isn't able to reduce headcount (union
   agreements, a strategic decision to keep staff and redirect them to
   other tasks, etc.) — in that case the ROI needs to be recalculated as
   freed-up capacity or improved quality, not as a direct cost saving. Ask
   this explicitly of the customer before locking in the ROI mechanism.
5. **Bring in finance or an equivalent function as early as possible** to
   validate the measurement approach and the baseline — an ROI figure the
   customer's own finance department has approved is far more convincing
   than the consultant's own calculation.
6. **Feed the validated assumptions and business-impact figures**
   into [`../../../business-case-and-analysis/skills/business-case-builder/SKILL.md`](../../../business-case-and-analysis/skills/business-case-builder/SKILL.md)
   for a full business case (problem, solution, economics, risks,
   timeline, recommendation) and into
   [`../../../business-case-and-analysis/skills/roi-npv-sensitivity-model/SKILL.md`](../../../business-case-and-analysis/skills/roi-npv-sensitivity-model/SKILL.md)
   for ROI/NPV/IRR calculation and sensitivity analysis — run the
   sensitivity analysis especially on the assumptions you flagged as
   weakest in step 3.
7. **Also record what the demo/PoC did NOT prove** regarding business
   impact (e.g. adoption rate, change-management cost, integration work)
   in the business case's risk section — these are typically exactly the
   things that lead to "pilot purgatory" if they aren't accounted for in
   advance.

## What this skill does NOT do

- Doesn't calculate ROI, NPV, or IRR itself — produces validated,
  transparent inputs for
  [`../../../business-case-and-analysis/skills/roi-npv-sensitivity-model/SKILL.md`](../../../business-case-and-analysis/skills/roi-npv-sensitivity-model/SKILL.md).
- Doesn't write a full business case — that's the job of
  [`../../../business-case-and-analysis/skills/business-case-builder/SKILL.md`](../../../business-case-and-analysis/skills/business-case-builder/SKILL.md).
- Doesn't guarantee that a PoC-scale result scales to production — on the
  contrary, its core job is to force into the open the assumptions the
  scale-up claim rests on.
- Doesn't assess technical feasibility at production scale — see
  [`../../../ai-strategy-and-governance/skills/ai-use-case-feasibility-and-poc-scoping/SKILL.md`](../../../ai-strategy-and-governance/skills/ai-use-case-feasibility-and-poc-scoping/SKILL.md)
  and
  [`../../../ai-strategy-and-governance/skills/build-vs-buy-vs-partner-ai/SKILL.md`](../../../ai-strategy-and-governance/skills/build-vs-buy-vs-partner-ai/SKILL.md).

## Refinement notes

Areas to keep deepening with real practice:

- your own examples of assumption chains that turned out wrong when
  scaling from PoC to production — and what you learned from that
- your own template for documenting an assumption chain (into
  [`../../references/`](../../references/))
- rules of thumb for which types of ROI mechanism most often collide with
  a customer's organizational structure

This is an internal working note, not a claim about the skill's current
usability. Track depth privately via the `maturity` field in
`skills_index.json` (see
[`../../../meta/maturity_levels.md`](../../../meta/maturity_levels.md)).
**Don't add new fields to the frontmatter** — `name` and `description` are
the only ones allowed (see
[`../../../meta/frontmatter_schema.md`](../../../meta/frontmatter_schema.md)).

## Continue from here

- Before this: [`../demo-delivery-and-storytelling/SKILL.md`](../demo-delivery-and-storytelling/SKILL.md)
- In this pack (if the frame was set before the demo, go back to check the
  success criteria): [`../demo-framing-and-expectation-setting/SKILL.md`](../demo-framing-and-expectation-setting/SKILL.md)
- Next: [`../../../business-case-and-analysis/skills/business-case-builder/SKILL.md`](../../../business-case-and-analysis/skills/business-case-builder/SKILL.md)
  and [`../../../business-case-and-analysis/skills/roi-npv-sensitivity-model/SKILL.md`](../../../business-case-and-analysis/skills/roi-npv-sensitivity-model/SKILL.md)
- Testing assumptions before locking them in: [`../../../business-case-and-analysis/skills/assumption-and-evidence-audit/SKILL.md`](../../../business-case-and-analysis/skills/assumption-and-evidence-audit/SKILL.md)
- A ready-made skill chain for this situation: see [`../../../playbooks/`](../../../playbooks/)
- This pack's shared guardrails: [`../../CLAUDE.md`](../../CLAUDE.md)

## References

- Research synthesis (2026) on translating demo/PoC ROI — two metric
  classes, baseline/hypothesis comparison, early involvement of finance,
  fit between the ROI mechanism and organizational structure
- [`../../references/`](../../references/) — the pack's shared background material
- [`../../CLAUDE.md`](../../CLAUDE.md) — the pack's shared guardrails
