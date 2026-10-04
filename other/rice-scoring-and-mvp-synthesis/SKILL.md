---
name: rice-scoring-and-mvp-synthesis
description: "Scores multiple solution directions with the RICE model (Reach, Impact, Confidence, Effort) to select an MVP, and turns the choice into an MVP definition, a one-sentence positioning statement, and three 'why we win' claims."
---

# RICE Scoring and MVP Synthesis

## Purpose

Turn a comparison of multiple solution alternatives into an objective,
justified MVP choice using the RICE model, and translate that choice
directly into a usable strategy: what the MVP exactly does, how it's
positioned in one sentence, and why exactly this one wins. This is a
bridge skill between solution ideation (many alternatives) and writing
the PRD (one chosen direction).

## Based on

- The RICE prioritization model (Reach, Impact, Confidence, Effort) — a
  generally known product-prioritization framework, not the owner's own.
- The methodology of an external "AI-first SaaS Product" workshop,
  applied by the owner to one own case — see
  `../../references/ai-first-saas-workshop-source.md` and the worked
  example `../../cases/ai-decision-coach-mvp-case.md`, sections 6–7.
  **Note:** applied only once so far — not broadly validated.

## Method (draft — to be filled in further)

1. **Score each solution direction on four criteria (1–5):**
   - **Reach** — how many users this would touch.
   - **Impact** — how significant the effect is for the user it touches.
   - **Confidence** — how sure you are that your Reach/Impact/Effort
     estimates hold up (high = strong evidence, low = a guess).
   - **Effort (inverted: 5 = easiest/lowest effort, 1 = hardest/highest
     effort)** — note the inversion: in this model a high Effort score
     means LOW build cost, so all four criteria sum in the same
     direction (higher = better MVP candidate).
2. **Calculate the total RICE score** (max 20 across the four criteria,
   or scale as needed) for each direction and rank them.
3. **Briefly justify the score for each criterion** — don't leave scores
   unexplained. In particular, tie the Effort estimate concretely to the
   existing tech stack/data/tools (what already exists vs. what needs to
   be built from scratch).
4. **Choose the MVP with the highest RICE score**, UNLESS a specific
   strategic reason favors another (e.g. a higher-Effort direction is the
   only one that proves a genuine differentiator, not just table-stake
   value). If you deviate from the highest score, explicitly justify why.
5. **Write the MVP definition (2-3 sentences).** Combine the chosen AI
   wedge (differentiator need) and the essential table-stake needs into
   one concise description of what the MVP does and for whom.
6. **Sketch the MVP flow concisely** (5-8 steps): user input → AI
   synthesis/scoring → decision engine/logic → AI output(s) → next-step
   plan → (optional) communication support → (optional) path to deeper
   tools.
7. **Write a one-sentence positioning statement.** Format: "[Product]
   gives [target customer] [core benefit] through [distinctive
   mechanism]." Test: could this sentence describe any competitor? If
   yes, it isn't specific enough yet.
8. **Write 3 "why we win" claims.** Each claim ties one strength
   (differentiator need, existing data/tool, unique approach) to a
   concrete competitive advantage — not general claims ("we're better")
   but justified reasons.
9. Carry the MVP definition, flow, positioning statement, and "why we
   win" claims into `../ai-buildable-prd-writing/SKILL.md` as the basis
   for the PRD.

## What this skill does NOT do

- Does not make the final MVP choice for you in a fully mechanical way —
  the RICE score supports the decision, it isn't an automatic rule; a
  strategic deviation from the highest score is allowed if justified.
- Does not assess financial viability or unit economics — only relative
  prioritization between solution alternatives. See
  `../../../../business-case-and-analysis/skills/roi-npv-sensitivity-model/SKILL.md`
  for deeper financial modeling once the MVP is chosen.
- Does not replace `../../../opportunity-recognition/skills/opportunity-evaluation-
  and-judgment/SKILL.md` — this is a narrower, faster choice between
  2-3 already-identified solution directions, not a full assessment of
  an opportunity from scratch.

## Refinement notes

This skill has so far been applied to one case (the owner's own case).
As you apply it to more businesses, add:

- your own rules of thumb for when it's worth deviating from the
  highest RICE score
- concrete examples of positioning statements and "why we win" claims
  from other cases in the `../../cases/` folder

Once this section has been filled in with multiple cases, raise
`skills_index.json`'s `maturity` field to `validated`
(see `../../../../meta/maturity_levels.md`).

## Continue from here

- Preceding skill in this pack:
  `../ai-differentiator-solution-ideation/SKILL.md` — produces the three
  alternatives scored here.
- Next skill in this pack: `../tiny-core-identification-and-feature-freeze/SKILL.md`
  — once a direction is chosen here, isolates the one interaction that
  is its actual reason to exist and blocks feature creep before the PRD
  is written.
- Next skill in this pack: `../ai-buildable-prd-writing/SKILL.md`
  — writes the PRD for the chosen MVP.
- Related skill in this pack, if the chosen MVP is a conversational/
  agentic product: `../ai-native-conversational-os-design/SKILL.md`.
- Worked example: `../../cases/ai-decision-coach-mvp-case.md`, sections 6–7.
- The pack's shared guardrails: `../../CLAUDE.md`

## References

- `../../references/ai-first-saas-workshop-source.md` — source information
- `../../cases/ai-decision-coach-mvp-case.md` — worked example
- `../../CLAUDE.md` — the pack's shared guardrails
