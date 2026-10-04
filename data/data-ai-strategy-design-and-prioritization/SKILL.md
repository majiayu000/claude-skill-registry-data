---
name: data-ai-strategy-design-and-prioritization
description: "Designs a Data & AI strategy holistically (not in silos) using a Driver Tree tool to break business goals down into data points, and prioritizes what data to collect/use now vs. for the future with a Data Readiness x Strategic Value matrix. Use when an organization is planning which data and AI capabilities to invest in next."
---

# Data & AI Strategy Design and Prioritization

## Purpose

Prevents two common data strategy mistakes: (1) AI/data investments are
made in silos without anyone having broken a business goal down into
concrete data points, so the result is technically impressive but
strategically disconnected; and (2) an organization tries to build
tomorrow's models on today's data without noticing that the right data
should already be collected now. This skill produces a structured bridge
between a business goal and a concrete data/AI investment, and prioritizes
investments by what's both strategically valuable AND achievable given
data readiness.

## Anchored in research

- The Data & AI Design Thinking tradition (industry consulting practice, a
  synthesis of multiple sources): an AI strategy isn't built in silos —
  cross-functional facilitation ensures the strategy solves genuine user
  and stakeholder needs ("Systems over Objects").
- The Driver Tree tool (an established business-analytics method): a
  business goal is broken down hierarchically into components until
  concrete, measurable drivers are reached — the same logical principle
  as the McKinsey-tradition issue tree (see
  `../../../strategic-thinking/skills/hypothesis-driven-strategy/SKILL.md`),
  applied here to identifying data points and AI solutions.
- The "tomorrow's models require today's data" heuristic (a design
  principle from data monetization pipelines): if a given AI model is
  meant to be feasible 12-24 months from now, the unique data it requires
  needs to start being collected today — the lead time for a data
  investment is typically longer than the lead time for building the
  model.

## Method

1. **Build a Driver Tree from the business goal down to data points.**
   Start from the top-level business goal (e.g. "increase customer
   retention") and break it down into successive questions: what
   sub-drivers drive this goal? What data is needed to measure each
   sub-driver? What AI/analytics solution could influence each
   sub-driver? Keep breaking it down until you reach concrete, measurable
   data points — don't stop at an abstract level ("better customer
   understanding" isn't a data point, "usage rate of feature X over the
   past 30 days" is).
2. **Assess every branch of the tree: does AI/data genuinely add value
   here, or is it noise?** Not every component of a business goal
   benefits from data or AI — some are better solved with a process
   change or a human decision. Mark each branch either "data/AI-relevant"
   or "not data/AI-relevant, solve otherwise" before continuing only
   with the relevant branches.
3. **Separate "what can we do now" from "what do we need to build for the
   future" (Agile Value Assessment).** For every identified data point:
   - **Available now:** the data already exists at sufficient quality —
     analysis/modeling can start immediately.
   - **To be built:** the data doesn't yet exist or its quality isn't
     sufficient — requires designing a collection point before the model
     is possible. Apply the "tomorrow's models require today's data"
     heuristic: if this data is wanted for use in 12-24 months,
     collection needs to start now, not when the model is wanted.
4. **Place every identified data/AI opportunity on a Data Readiness ×
   Strategic Value matrix:**
   - **Achievable now, high value:** start here first — the fastest path
     to proven value.
   - **To be built, high value:** launch the data-collection investment
     now, even though the model won't be ready right away — this is the
     matrix's most strategic quadrant, because it builds future
     defensible advantage (see the flywheel test in
     `../data-role-diagnosis/SKILL.md`).
   - **Achievable now, low value:** don't prioritize, even though ease
     makes it tempting — low strategic value doesn't change with ease.
   - **To be built, low value:** reject or shelve — the costliest
     combination (long lead time, small payoff).
   This matrix follows the same logic as the 2x2 prioritization matrix
   in `../../../ai-strategy-and-governance/skills/ai-opportunity-portfolio/SKILL.md`,
   but the axes are data-specific (Data Readiness, not Technical
   Feasibility in general) — use this BEFORE the general AI opportunity
   scoring, when the question is specifically about data readiness.
5. **Facilitate building the tree cross-functionally**, not alone or with
   just the data team. The business owner knows which driver actually
   matters; the data/technical expert knows what's feasible; the end
   user knows which solution would actually help day-to-day. A tree
   built together with these three perspectives is far more likely to be
   right than one built inside a single function.
6. **Produce a prioritized roadmap** that separates "start now" (high
   value, data ready) and "start data collection now, model later" (high
   value, data to be built) into their own parallel tracks — don't merge
   them into a single timeline, since they have different time horizons
   and different success criteria.

## What this skill does NOT do

- Doesn't make the final investment decision for you — produces a
  structured prioritization to support human decision-making.
- Doesn't replace the broader 5-dimension scoring in
  `../../../ai-strategy-and-governance/skills/ai-opportunity-portfolio/SKILL.md`
  — this skill produces an input into it (particularly the Data
  Readiness dimension), not a full scoring of overall business impact by
  itself.
- Doesn't build the technical data architecture or collection system —
  identifies WHAT data is needed, not HOW it's technically collected.
- Doesn't confirm figures, market data, or data-quality assessments from
  memory — uses the inputs you provide, or marks an assumption clearly
  (`[assumption — verify]`).

## Refinement notes

Areas to keep deepening with real practice:

- your own Driver Tree examples from different industries
- a concrete facilitation template for a Driver Tree workshop (into
  `../../references/`)
- rules of thumb for how deep the tree typically needs to be broken down
  before reaching a useful data-point level

Once this section is filled in and validated in practice, update the
`maturity` field in `skills_index.json` to `draft`, `validated`, or
`canonical` (see `../../../meta/maturity_levels.md`). **Don't add new
fields to the frontmatter** — `name` and `description` are the only ones
allowed (see `../../../meta/frontmatter_schema.md`).

## Continue from here

- Before this: `../data-role-diagnosis/SKILL.md`
  — first establish whether data functions as an enabler or the asset
  role is being pursued, before prioritizing investments.
- Next in this pack (if the goal is monetization):
  `../data-monetization-model-selection/SKILL.md`
- Related skill in another pack: `../../../ai-strategy-and-governance/skills/ai-opportunity-portfolio/SKILL.md`
  — receives this skill's prioritized data/AI opportunities into a
  broader 5-dimension scoring.
- Related skill in another pack: `../../../strategic-thinking/skills/hypothesis-driven-strategy/SKILL.md`
  — the same issue tree logic applied more generally to strategic
  questions, not just data points.
- A ready-made skill chain for this situation: see `../../../playbooks/`
- This pack's shared guardrails: `../../CLAUDE.md`

## References

- `../../references/` — the pack's shared background material
- `../../CLAUDE.md` — the pack's shared guardrails
