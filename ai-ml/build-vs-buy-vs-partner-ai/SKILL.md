---
name: build-vs-buy-vs-partner-ai
description: "Structures the build/buy/partner decision for an AI capability, including hybrid options, scored on differentiation value, time to value, and total cost of ownership (inference, retraining, ML-ops talent, not just license cost). Use when an AI capability decision needs a defensible comparison instead of defaulting to \"build\" or \"buy\" by habit."
---

# Build vs. Buy vs. Partner (AI)

## Purpose

Structures the decision to build an AI capability in-house, buy it as a
platform/API, or partner on it — applying the same structured-comparison
discipline as
`../../../strategic-thinking/skills/strategic-options-evaluation/SKILL.md`,
but scored against criteria specific to AI capabilities (proprietary
data advantage, model/vendor lock-in, and the pace at which the
underlying technology itself is moving).

## Anchored in research

- `../../../strategic-thinking/skills/strategic-options-evaluation/SKILL.md`
  logic — list the real options including "do nothing," fix comparison
  dimensions before scoring, score each option independently, separate
  reversible from irreversible choices — applied here to Build/Buy/
  Partner decisions on an AI capability specifically.

## Method

1. **List the real options, including "do nothing" and hybrid paths.**
   Build, Buy, and Partner aren't always three mutually exclusive
   choices for the whole capability — a common real option is a hybrid
   (e.g. buy the base model/platform, build the proprietary data layer
   and orchestration on top). List the hybrid explicitly rather than
   forcing a three-way choice where a fourth, blended option is what
   actually fits.
2. **Fix the comparison dimensions before scoring any option** —
   specific to AI capabilities, not the generic set:
   - **Differentiation value** — is this capability core to the
     competitive advantage (e.g. it depends on proprietary data other
     players don't have), or is it table-stakes infrastructure every
     competitor will have access to the same way? Table-stakes
     capabilities lean toward Buy; genuinely differentiating ones lean
     toward Build.
   - **Time to value** — how fast does the organization need this
     working? Buy and Partner are almost always faster to a working
     first version than Build.
   - **Total cost of ownership (TCO)** — not just build/license cost,
     but ongoing inference costs, fine-tuning/retraining, monitoring,
     and the internal ML-ops talent needed to run it — a Build option
     that looks cheaper on initial cost often loses on TCO once
     ongoing model maintenance is priced in.
   - **Lock-in and reversibility** — how hard is it to switch vendors
     or bring a bought/partnered capability in-house later if the
     vendor's roadmap, pricing, or reliability changes? A Buy decision
     with a proprietary data format or deep API dependency is much
     less reversible than one built on open standards.
   - **Data and IP control** — does the vendor's model see or train on
     the organization's proprietary data, and under what terms? This
     is often the deciding factor for capabilities that ARE the
     differentiation (point above) — ceding control of the data that
     creates the advantage can quietly undo the advantage even if the
     vendor relationship is otherwise good.
   - **Pace of underlying technology change** — capabilities riding on
     a fast-moving frontier (e.g. general-purpose LLM capability) often
     favor Buy/Partner, since a Build investment risks being
     technologically stale before it ships; capabilities riding on
     stable, well-understood techniques are safer to Build.
3. **Score each option on each dimension independently** before
   collapsing to a single recommendation — a lot of the useful
   information is in *where* the options diverge (e.g. Build wins on
   differentiation and control but loses badly on time-to-value and
   TCO), not just which one wins on average.
4. **Separate reversible from irreversible choices explicitly.** A
   Partner or Buy arrangement that can be unwound in a fiscal quarter
   is a fundamentally different risk than a Build investment that
   consumes 12 months of a scarce ML engineering team, even if both
   score similarly on paper. When time-to-value pressure is high but
   the capability is genuinely differentiating, consider Buy/Partner
   now with an explicit plan to Build later, once the differentiation
   thesis is validated — rather than treating the choice as permanent
   on day one.
5. **Name the vendor/partner risk explicitly if Buy or Partner is
   chosen:** vendor viability (will they exist and support this in 3
   years), pricing risk at scale, and dependency concentration (is the
   organization becoming single-sourced on a capability core to its
   operations).
6. **Produce a decision-ready comparison**, not a recommendation
   disguised as analysis — the output should make the trade-offs
   legible enough that a different, reasonable person could look at
   the same table and land on a different choice for defensible
   reasons (see `../../references/` once a template is added).
7. Validate the result with stakeholders or your own experience-based
   checklist, particularly whoever owns the budget for ongoing TCO,
   not just the upfront decision.

## What this skill does NOT do

- Doesn't make the final decision for you — it produces a structured
  draft to support a human decision.
- Doesn't confirm figures, market data, or competitor data from
  memory — it uses the inputs you provide, or marks an assumption
  clearly (`[assumption — verify]`).
- Doesn't run a vendor procurement process or put a vendor selection
  out to tender — it structures the decision criteria that a
  subsequent procurement process would use.

## Refinement notes

Areas to keep deepening with real practice:

- your own rules of thumb and heuristics for this technique — e.g.
  typical TCO multipliers you've seen between a Build estimate and its
  actual ongoing cost
- concrete templates (into `../../references/`, e.g. a build-vs-buy
  scoring table)
- reference cases / your own examples
- what this skill deliberately does *not* do (guardrails, common
  mistakes) — add to the list above

Once this section is filled in and validated in practice, update the
`maturity` field in `skills_index.json` to `draft`, `validated`, or
`canonical` (see `../../../meta/maturity_levels.md`). **Don't add new
fields to the frontmatter** — `name` and `description` are the only
ones allowed (see `../../../meta/frontmatter_schema.md`).

## Continue from here

- Next in this pack: `../ai-capability-roadmap/SKILL.md` — builds the
  organization's AI capability map and roadmap from the current state
  to the target state.
- A ready-made skill chain for this situation: see `../../../playbooks/`
- This pack's shared guardrails: `../../CLAUDE.md`

## References

- `../../references/` — the pack's shared background material
- `../../CLAUDE.md` — the pack's shared guardrails
