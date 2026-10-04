---
name: opportunity-intake-elicitation
description: "Collects sufficient structured input on an identified opportunity through well-designed questions — even when the client can't yet frame their idea in business terms."
---

# Opportunity Intake Elicitation

## Purpose

Collects sufficient structured input on an identified opportunity through
well-designed questions — even when the researcher or team can't yet frame
their idea in business terms. The goal isn't just data collection: by
answering the questions, the client also learns to think through their own
idea more deeply.

## Based on

The owner's own service — the Opportunity Value Assessment product's Input
Wizard (own product, see `../../references/intake-questions.md`) and its
supporting background research "S1 — Opportunity Package".

- Doug Richard's 10 questions for evaluating a business opportunity (VC Cafe, 2012)
- SRI's NABC model (Need, Approach, Benefits, Competition)
- Opportunity Canvas (Jeff Patton) — a one-page structure for framing an opportunity

## Method

1. **Origin of the opportunity.** Ask how the opportunity was identified: a
   research finding, an unexpected discovery/anomaly in experiments, a new
   technical approach, an observed customer need, a gap revealed by data, or
   an improvement on an existing solution? This establishes a shared
   vocabulary and helps tailor the remaining questions.
2. **The problem and who has it.** Ask for a concrete description of the
   problem or need, without the solution: "Describe the situation the
   customer is in today, without your solution — what's going wrong, or what
   are they missing out on?" Map out who the problem affects (users,
   organizations, industries).
3. **Solution concept and novelty.** Ask for a simple description of the
   proposed solution (product, service, material, method, capability asset):
   "what would someone 'get' or 'use'?" Establish what's new or different
   compared to existing solutions.
4. **Market and early customers.** Ask who the first customers or users could
   be — not the final market, but a logical, reachable first target.
   Establish the customer type (B2C, B2B, public sector, academia) and a
   rough market sense (size, trends, urgency) — figures aren't mandatory, an
   impression is a fine starting point too.
5. **Current state and readiness.** Ask for the solution's maturity level on
   a plain-language scale (idea only → proof-of-concept → lab prototype →
   tested prototype → pilot/field test → market-ready — TRL in plain
   language). Establish what's already been achieved (milestones, results,
   funding, patents, collaborations). If a PoC exists: what hypotheses were
   tested, and what was learned? If not: what should be tested, and at what
   scale, to demonstrate feasibility? Also ask whether the opportunity has
   already been protected or published (IP, patents, publications) — a
   general-level answer is enough, no detailed legal description is needed.
6. **Goals and next hypotheses.** Ask what kind of business or impact could
   emerge from the opportunity (startup, license, new business line, public
   service) and what the assessment is meant to achieve (clarity for an
   application, input for a TTO decision, partner discussions, portfolio
   comparison). Ask which hypotheses should be tested next (e.g. "Will
   customers pay for X?", "Does the technology scale?").
7. **Fill in missing pieces with expertise, not guesswork.** If the
   respondent knows the target customer but not the market size, use
   industry knowledge to estimate an order of magnitude and flag it as an
   assumption. A partial answer is enough as a starting point — don't demand
   a complete business plan before you can proceed.

## Gotchas

- Step 7 permits filling gaps with expert estimates, but only when tagged
  `[assumption — verify]` — an estimated market size or TRL that loses this
  tag as the answers get cleaned up into a report is indistinguishable from
  a client-confirmed fact, which is exactly what the "does NOT do" section
  warns against.
- Step 2 asks for the problem "without your solution," but respondents
  (especially technical inventors) reflexively describe their invention
  instead of the pain it addresses — if the answer to "what's going wrong"
  already names a product or mechanism, it hasn't actually answered the
  question and needs to be re-asked.
- Step 5's TRL and IP questions are meant to stay at plain-language,
  general level ("idea → PoC → prototype…"; "has this been protected, in
  general terms?") — pushing for a detailed legal description of IP status
  or a precise TRL number contradicts the skill's own "partial answer is
  enough" principle and can make a client stall entirely.
- Step 4's market figures are explicitly optional ("an impression is a fine
  starting point too") — treating a vague answer like "probably a big
  market" as insufficient and blocking progress until a number appears
  defeats the purpose of an intake stage that exists to work with partial
  information.
- This skill only collects structured input; it does not itself judge
  whether the opportunity is viable. Slipping viability judgments ("this
  doesn't sound big enough") into the elicitation questions can bias what
  the client is willing to disclose — that judgment belongs to
  `opportunity-value-assessment`, not here.

## What this skill does NOT do

- Doesn't require the client to have a finished business plan — collects
  even partial information in a structured way and makes visible what's
  still missing.
- Doesn't guess market size, competitive landscape, or other figures to fill
  gaps in the answers without a clear `[assumption — verify]` flag.
- Doesn't itself assess the opportunity's viability — produces the
  structured input for the `opportunity-value-assessment` skill.

## Continue from here

- Next in this pack: `../opportunity-value-assessment/SKILL.md` — Places the
  collected opportunity in an attractiveness × feasibility matrix and
  assesses it from seven commercialization angles.
- Related skill in another pack: `../../../specialisation-packs/research-commercialisation/skills/research-opportunity-recognition/SKILL.md`
- This pack's shared guardrails: `../../CLAUDE.md`

## References

- `../../references/intake-questions.md` — the full question bank, by theme
- `../../references/opportunity-frameworks-review.md` — Doug Richard, NABC, Opportunity Canvas
- `../../CLAUDE.md` — this pack's shared guardrails
