---
name: data-monetization-model-selection
description: "Selects and justifies a suitable data monetization model (direct: DaaS/Insight-as-a-Service/data exchange vs. indirect: product enrichment/resource optimization/risk mitigation/Data Flywheel) with a decision tree, and checks the feasibility of a Data Flywheel claim with a four-point checklist. Use once data has been validated as a strategic asset and you need to decide HOW to monetize it."
---

# Data Monetization Model Selection

## Purpose

Once data has been diagnosed as a strategic asset (see
`../data-role-diagnosis/SKILL.md`), the next question isn't "should we
monetize" but "with which model." Direct and indirect monetization require
different capabilities, a different risk profile, and a different
timeline — mixing the two without a deliberate choice typically leads to
an organization trying to sell data externally before internal
productization has even been tested, or, conversely, leaving a clear
external demand unexploited. This skill produces a justified model choice
and separately checks whether a "data flywheel" claim is real or wishful
thinking.

## Anchored in research

- Direct and indirect data monetization models (industry consulting
  practice, a synthesis of multiple sources, 2026): Data-as-a-Service,
  Insight-as-a-Service, data exchange/IP licensing (direct); product
  enrichment, utilization/resource optimization, business-risk mitigation
  (indirect).
- The Data Flywheel mechanism in AI business: unique data → model
  training → better product → more users → more data. As a concept, an
  extension of Collins's (2001) flywheel mechanism (see the anchoring in
  `../data-role-diagnosis/SKILL.md`) applied to the data/AI context.
- Business model innovation patterns from the
  `../../../business-design-frameworks` and
  `../../../specialisation-packs/business-model-canvas` packs (e.g.
  `financial.rev.data_monetization`,
  `operating.resources.leverage_customer_data`) — this skill deepens one
  pattern family with data-specific detail.

## Method

1. **Walk through the direct-monetization decision tree first, since it
   rules out options quickly:**
   - Is selling the data externally legally/contractually permitted
     (customer contracts, GDPR and other privacy law, third-party IP
     rights)? If not, the direct model is ruled out without a separate
     legal review — don't proceed to a direct model before this check.
   - Is there an identified external buyer or market for this
     data/insight TODAY (the resale test, see
     `../data-role-diagnosis/SKILL.md`)? If not, the direct model would
     first require validating the market, not just productizing it.
   - Is the data unique enough that a buyer couldn't acquire the same
     thing more cheaply elsewhere (the defensibility test)? If the data
     is widely available, pricing power in direct sale is weak.
   If all three pass, consider a direct model: DaaS/raw-data sale (the
   lowest processing level, requires the strongest data governance),
   Insight-as-a-Service (analytics/forecasts instead of raw data,
   protects the raw data better), or data exchange/IP licensing (data
   traded for another party's data, technology, or market access — a
   common model in innovation ecosystems).
2. **If the direct model didn't pass point 1, move to an indirect
   model** — this is usually both more profitable and lower-risk:
   - **Product/service enrichment:** data enables a new, paid feature or
     a better user experience within an existing product (e.g.
     hyper-personalization).
   - **Utilization/resource optimization:** data reveals bottlenecks and
     enables dynamic pricing or more efficient resource allocation —
     shows up directly as cost savings or added revenue.
   - **Business-risk mitigation:** data enables proactive detection
     (e.g. customer churn, fraud, equipment failure) before the event —
     "a euro saved is a euro earned."
3. **If a "data flywheel" model is claimed, check it separately with a
   four-point checklist — don't accept a flywheel claim without this:**
   - **Unique collection channel:** is there a genuine, ongoing way to
     collect data that a competitor doesn't have at the same scale?
   - **Measurable model improvement:** does the model/product provably
     (not just presumably) improve as more data accumulates — is there
     already evidence of this, or is it still an assumption?
   - **Observable user-experience improvement:** does the user notice
     the model improving, or is the improvement so small it doesn't
     affect behavior?
   - **The loop closing as growth:** does the observed improvement
     provably attract more users, who generate more data — or does the
     loop break somewhere (e.g. the improvement isn't enough to attract
     new users)?
   If even one of the four points fails the check or is still just an
   assumption, name it explicitly as a risk rather than presenting the
   flywheel as an already-working, self-sustaining mechanism.
4. **Compare the model on speed, risk, and competitive advantage**, not
   just revenue potential: a direct model often produces a faster but
   more easily copied revenue stream (the data itself is no longer your
   exclusive once it's been sold); an indirect model builds more slowly
   but toward more defensible advantage.
5. **Produce a justified recommendation in one sentence per option**,
   naming WHY the model fits or doesn't fit this situation — not just
   the model's name.

## What this skill does NOT do

- Doesn't provide a legal assessment of privacy or contractual obstacles
  to selling data externally — identifies that a check is needed, but
  doesn't replace separate privacy/legal expertise.
- Doesn't calculate exact pricing or ROI for the chosen model — see
  `../../../business-case-and-analysis/skills/roi-npv-sensitivity-model/SKILL.md`.
- Doesn't claim an indirect model is always better than a direct one —
  context decides; the skill produces a structured comparison, not a
  ready-made answer.
- Doesn't confirm figures, market demand, or competitor data from
  memory — uses the inputs you provide, or marks an assumption clearly
  (`[assumption — verify]`).

## Refinement notes

Areas to keep deepening with real practice:

- your own examples of when a direct vs. indirect model turned out to be
  the right choice (and why the wrong choice would have failed)
- a concrete decision-tree template as a visual tool (into
  `../../references/`)
- your own observations on which of the four flywheel checklist points
  most often fails in practice

Once this section is filled in and validated in practice, update the
`maturity` field in `skills_index.json` to `draft`, `validated`, or
`canonical` (see `../../../meta/maturity_levels.md`). **Don't add new
fields to the frontmatter** — `name` and `description` are the only ones
allowed (see `../../../meta/frontmatter_schema.md`).

## Continue from here

- Before this: `../data-role-diagnosis/SKILL.md`
  — first confirm that the data passes the asset tests.
- Before this (prioritization before model selection):
  `../data-ai-strategy-design-and-prioritization/SKILL.md`
- Related skill in another pack: `../../../specialisation-packs/business-model-canvas/skills/bmc-innovation-pattern-matching/SKILL.md`
  — if the chosen monetization model still needs to be fitted into a
  broader business model (Financial Model patterns).
- Related skill in another pack: `../../../business-case-and-analysis/skills/roi-npv-sensitivity-model/SKILL.md`
  — translates the chosen model into a financial calculation.
- A ready-made skill chain for this situation: see `../../../playbooks/`
- This pack's shared guardrails: `../../CLAUDE.md`

## References

- `../../references/data-monetization-frameworks.md` — a broader
  comparison of direct and indirect monetization models
- `../../references/` — the pack's shared background material
- `../../CLAUDE.md` — the pack's shared guardrails
