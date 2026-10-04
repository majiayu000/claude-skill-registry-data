---
name: data-role-diagnosis
description: "Diagnoses and justifies whether data functions in the organization as an enabler (cost, operational efficiency) or as a strategic asset (revenue-generating, monetizable, defensible) — using heuristic tests (resale, flywheel, defensibility, relevance) and the Offense/Defense framework. Use before designing a data strategy or an AI business model, when you need to determine what role data plays in the organization TODAY and what role it SHOULD play."
---

# Data Role Diagnosis

## Purpose

Prevents the most common confusion in data strategy discussions: talking
about "data strategy" while meaning two different things at once. Part of
the organization means data **governance** (governance, quality,
integrations — a cost that keeps the machinery running). Part means
**exploiting** data as a source of new value (monetization, defensible
competitive advantage, new business models). Neither is wrong, but they
require different tools, different metrics, and different language with
leadership. This skill produces a diagnosis: what role data plays TODAY in
each area, and whether a shift from enabler to asset is even worth pursuing
right now.

## Anchored in research

- The enabler vs. strategic asset distinction (industry consulting
  practice, a synthesis of multiple sources, 2026): data as a commodity
  that enables operations vs. data as an asset whose value grows and
  produces measurable returns.
- Davenport, Thomas H. & Bean, Randy — the "offense vs. defense" framework
  for data strategy (Harvard Business Review / MIT Sloan Management Review
  writing): data governance is a defensive game (risk management,
  compliance, quality); exploiting data as a source of new business is an
  offensive game (growth, competitive advantage, new revenue streams).
- Collins, Jim — the flywheel concept (*Good to Great*, 2001) as a general
  business mechanism, applied here to data's self-reinforcing value loop
  (see point 3 below and
  `../data-monetization-model-selection/SKILL.md`).
- The relevance test (added later) is not tied to a verified named
  source — see
  `../../../ai-strategy-and-governance/references/ai-native-reshuffle-heuristics-research.md`
  for why its original attribution couldn't be confirmed and was
  deliberately dropped, while the underlying test was kept because the
  point stands on its own.

## Method

1. **Ask the enabler question for every significant data source:** *"Does
   this data help us do what we already do faster, cheaper, or better?"*
   If the answer is yes but nothing more, the data functions today as an
   enabler — it's a commodity, not the core of the business. A typical
   sign: the data enables breaking down an operational silo (e.g.
   reporting, integrations) but doesn't itself produce sellable value.
2. **Ask the asset question about the same data source:** *"Could we sell
   this data directly, or use it to train a model a competitor couldn't
   replicate with capital alone?"* If yes, the data is a potential
   strategic asset — but potential alone isn't enough; it needs to be
   validated with the tests in point 3.
3. **Validate the asset claim with four tests before you believe it:**
   - **Resale test:** is there a party that would pay for this data or an
     insight derived from it TODAY, without you first having to build
     anything new? If not, this is potential, not a present-day asset.
   - **Flywheel test:** does the product/model measurably improve as more
     data accumulates, and does the better product attract more users
     (who generate more data)? If the loop doesn't close somewhere (e.g.
     more data doesn't noticeably improve the model), "flywheel" is
     wishful thinking — see the more detailed checklist in
     `../data-monetization-model-selection/SKILL.md`.
   - **Defensibility test:** could a competitor replicate this
     competitive advantage by buying the same amount of compute/capital,
     or does it require this specific data, unavailable elsewhere? If a
     competitor could reach the same outcome with money alone without
     this data, the asset isn't as defensible as assumed.
   - **Relevance test:** is this specifically the data type with genuine
     predictive power for the target outcome, or just the data the
     organization happens to already have, for a different reason? This
     catches a common and easy-to-miss mistake: owning ADJACENT data
     (e.g. purchase-behavior data) doesn't mean the organization is
     positioned for an AI use case that actually needs a DIFFERENT kind
     of data (e.g. health or biometric data for genuinely personalized
     recommendations) — the two can look similar enough in a slide to
     pass unquestioned, but only one of them has real predictive value
     for the stated goal. Ask directly: if a well-resourced competitor
     started from zero but had access to the RIGHT data type instead of
     ours, would they out-predict us despite the head start we think we
     have? This illustrative failure mode (owning consumer purchase
     data while believing it substitutes for health/microbiome data in
     a personalization use case) is a plausible, cautionary example, not
     an independently verified case — treat it as illustrative rather
     than a confirmed citation.
4. **Place the diagnosis on an Offense/Defense matrix** with two axes:
   current maturity (low/high data governance) and targeted role
   (enabler/asset). This exposes a common trap: the organization tries to
   build asset-level business (e.g. data monetization) on top of a weak
   governance foundation — in that case, the first investment isn't
   monetization, it's governance.
5. **Communicate the role diagnosis to leadership as a one-sentence claim
   per data source**, e.g. "Customer purchase-behavior data today
   functions purely as a reporting enabler, but passes the resale and
   flywheel tests — it's a potential asset that requires [name the missing
   investment] before it can be monetized." Don't present potential as
   already-realized value.
6. **Connect the diagnosis to the next decision:** if data is an enabler
   and isn't meant to change, prioritize governance/quality investments
   (not this pack's core focus, see other sources). If the data validates
   as an asset, move on to
   `../data-ai-strategy-design-and-prioritization/SKILL.md` to prioritize
   the value, then to
   `../data-monetization-model-selection/SKILL.md` to select a model.

## What this skill does NOT do

- Doesn't implement data governance or technical architecture — only
  diagnoses the role and justifies it.
- Doesn't calculate the monetary value of data or its ROI — see
  `../data-monetization-model-selection/SKILL.md` and
  `../../../business-case-and-analysis/skills/roi-npv-sensitivity-model/SKILL.md`.
- Doesn't claim every data source should be pushed toward becoming an
  asset — many data sources are, and should remain, pure enablers;
  forcing asset-thinking without passing the resale/flywheel/defensibility
  tests leads to overvalued data strategies.
- Doesn't confirm figures, market data, or competitor data from memory —
  uses the inputs you provide, or marks an assumption clearly
  (`[assumption — verify]`).

## Refinement notes

Areas to keep deepening with real practice:

- your own examples of a client overvaluing the asset-value of their
  data (which test would have revealed this in advance)
- a concrete diagnosis workshop/interview template per data source
  (into `../../references/`)
- rules of thumb for which industries/situations the enabler role is
  almost always the right answer and pursuing asset status isn't
  worthwhile

Once this section is filled in and validated in practice, update the
`maturity` field in `skills_index.json` to `draft`, `validated`, or
`canonical` (see `../../../meta/maturity_levels.md`). **Don't add new
fields to the frontmatter** — `name` and `description` are the only ones
allowed (see `../../../meta/frontmatter_schema.md`).

## Continue from here

- Before this (if the data is already suspected to be biased or
  incomplete): `../data-bias-and-quality-critical-reading/SKILL.md`
- Next in this pack (if the data validated as an asset):
  `../data-ai-strategy-design-and-prioritization/SKILL.md`
- If the role is already clear and the question is HOW to monetize:
  `../data-monetization-model-selection/SKILL.md`
- Related skill in another pack: `../../../ai-strategy-and-governance/skills/ai-opportunity-portfolio/SKILL.md`
  — uses the Data Readiness dimension in scoring AI opportunities; this
  skill deepens it at the level of a single data source's role.
- A ready-made skill chain for this situation: see `../../../playbooks/`
- This pack's shared guardrails: `../../CLAUDE.md`

## References

- `../../references/data-role-heuristics.md` — a broader collection of
  diagnostic questions and examples
- `../../../ai-strategy-and-governance/references/ai-native-reshuffle-heuristics-research.md` —
  grounding notes for the relevance test
- `../../references/` — the pack's shared background material
- `../../CLAUDE.md` — the pack's shared guardrails
