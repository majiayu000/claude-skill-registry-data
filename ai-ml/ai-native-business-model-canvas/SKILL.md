---
name: ai-native-business-model-canvas
description: "Designs the shift from an AI-enhanced business (AI bolted onto existing operations) to an AI-native one, using an extended Business Model Canvas with four AI-specific lenses: value proposition, data moat, human-AI interaction model, and cost of compute vs. revenue. Use when deciding whether AI is an add-on to the current business model or whether the model itself needs to be rebuilt around AI."
---

# AI-Native Business Model Canvas

## Purpose

Designs the transition from a traditional "AI-enhanced" business (a
business improved by AI) to an "AI-native" business model — a business
model built on AI from the ground up, whose entire value proposition
depends on the ML ecosystem.

## Anchored in research

- A research report supplied by the user, "AI Business Designer in the
  Age of AI" (2026) — the extended AI Business Model Canvas
- Business Model Canvas (Osterwalder & Pigneur) — the base structure
  this framework extends with four AI-specific lenses
- A research report supplied by the user, "Methods, Frameworks, and
  Competencies for Identifying AI Opportunities and Capacity in
  Business" (2026) — the "AI Value Canvas" (the same four-lens
  structure under different names: Unique AI Value Proposition, Data
  Moat & Flywheel, Human-AI Interaction Model, Cost of Compute vs.
  Marginal Revenue). This report confirmed three lenses that already
  existed (points 1–3 below) and explicitly surfaced a fourth — the
  Human-AI Interaction Model (point 4 below) — which this skill hadn't
  yet treated as its own point.
- The proprietary learning-engine principle in Method step 6 (added
  later) is grounded in current AI-moat/data-engine discourse (Y
  Combinator's "7 Real Moats for AI Startups," McKinsey's "From AI
  Table Stakes to AI Advantage," among others), consistently making the
  same point: proprietary, accumulating feedback loops are the durable
  moat, not the underlying algorithms, which commoditize faster than
  data streams do. Recursion Pharmaceuticals is used as the reference
  case — see
  `../../references/ai-native-reshuffle-heuristics-research.md` for
  the full grounding and why this was added as a deepening of an
  existing step rather than a new skill.

## Method

1. **Value Proposition.** Determine how AI personalizes, scales, or
   creates new value in real time — not just speeds up an existing
   process. Example: a hyper-personalized learning platform that
   adapts content and tone to the user's emotional state. Test: if AI
   were removed, would the value proposition collapse, or would it
   just be slower? (The latter = AI-enhanced, not AI-native.)
2. **Key Resources.** Identify proprietary data — unique data that
   competitors can't easily copy or acquire. Map algorithms and the
   orchestration layer as a core company asset, not a support process.
3. **Cost Structure.** Model the economics of training and running
   models (inference costs): cloud compute pricing, API costs at
   scale, and how these costs behave as user/transaction volume grows
   (linearly or sublinearly).
4. **Ecosystem & Partnerships.** Decide what models/capabilities are
   built in-house (Build), what's used through ready-made interfaces
   (Utilize), and who to partner with (Partner). For a deeper look at
   this decision: `../build-vs-buy-vs-partner-ai/SKILL.md`.
5. **Human-AI Interaction Model.** Explicitly decide which interaction
   mode humans and AI use to work together in this business model —
   this is a separate choice from the level of human oversight (see
   below):
   - **Copilot** — AI assists human-driven work in real time, the
     human remains the primary actor.
   - **Autonomous Agent** — AI independently performs a bounded set of
     tasks, the human sets the goal and checks the result.
   - **Generative Interface** — the interface itself is generative and
     adaptive rather than fixed (see
     `../../../specialisation-packs/ai-native-startup-design/skills/ai-native-conversational-os-design/SKILL.md`
     for a broader treatment of designing a conversational interface
     architecture, if this is the form chosen).
   This choice is a different question from the LEVEL of human
   oversight (in/on/outside-the-loop, see
   `../../../specialisation-packs/ai-native-startup-design/skills/closed-loop-process-and-human-oversight-design/SKILL.md`)
   — the interaction mode describes HOW humans and AI work together,
   the oversight level describes HOW MUCH the human checks. Use both
   together: e.g. "Autonomous Agent + human-on-the-loop" is a valid
   combination.
6. **Data flywheel check — and the proprietary learning-engine
   principle behind it.** Assess whether usage feeds data back into the
   model so the product improves on its own through use — this is one
   of the key differences between an AI-enhanced and an AI-native
   model. Go one level deeper than the check itself: the durable moat
   in an AI-native business is essentially never a single AI module on
   its own — individual modules commoditize quickly once unbundled,
   because a competitor can assemble an equivalent module from the same
   commodity building blocks. The moat is the CONTINUOUS, PROPRIETARY
   INTEGRATION of modules into one feedback loop spanning the full
   chain — from experimentation, through delivery, to the go-to-market
   signal that comes back from real usage — getting measurably stronger
   with every transaction. A well-documented reference case: Recursion
   Pharmaceuticals records millions of cellular images to train models
   on how diseases change cell morphology — a proprietary "wet-lab"
   feedback loop independently assessed as more durable than the
   algorithms it runs, precisely because the algorithms alone are
   increasingly commoditized while the integrated, accumulating dataset
   isn't. When evaluating a canvas's Key Resources and this flywheel
   check together, ask explicitly: if a competitor could buy or copy
   every individual AI module this business uses, would the business
   still have an advantage? If the honest answer is no, the "moat" is
   an illusion built on components, not on an integrated loop. Once a
   flywheel is DESIGNED this way, validate whether the claim actually
   holds using `../../../data-strategy-and-literacy/skills/data-monetization-model-selection/SKILL.md`'s
   four-point flywheel checklist (unique collection channel, measurable
   model improvement, observable UX improvement, the loop closing as
   growth) — that skill audits whether a flywheel claim is real; this
   step is about designing the architecture so it can be.
7. Produce a structured output (a canvas table or equivalent, see
   `../../references/` once added) and validate it with stakeholders
   or your own experience-based checklist.

## What this skill does NOT do

- Doesn't make the final business-model decision for you — it produces
  a structured draft to support a human decision.
- Doesn't confirm exact inference or cloud-cost figures from memory —
  it uses the inputs you provide, or marks an assumption clearly
  (`[assumption — verify]`).
- Doesn't make the build-vs-buy-vs-partner decision finally — it
  structures it as part of the canvas but points to a deeper analysis
  in another skill.
- Doesn't assess technical feasibility or PoC scoping — that's
  `ai-use-case-feasibility-and-poc-scoping`'s job.

## Refinement notes

Areas to keep deepening with real practice:

- your own rules of thumb and heuristics for this technique
- concrete templates (into `../../references/`, e.g. a canvas
  template)
- reference cases / your own examples of AI-native business models
- what this skill deliberately does *not* do (guardrails, common
  mistakes) — add to the list above

Once this section is filled in and validated in practice, update the
`maturity` field in `skills_index.json` to `draft`, `validated`, or
`canonical` (see `../../../meta/maturity_levels.md`). **Don't add new
fields to the frontmatter** — `name` and `description` are the only
ones allowed (see `../../../meta/frontmatter_schema.md`).

## Continue from here

- Preceding skill in this pack: `../ai-opportunity-portfolio/SKILL.md`
  — identifies and prioritizes AI use cases before business-model
  design.
- Next in this pack: `../ai-use-case-feasibility-and-poc-scoping/SKILL.md`
  — determines the technical boundary conditions of an AI use case and
  scopes the PoC phase.
- A deeper-dive skill for the ecosystem decision:
  `../build-vs-buy-vs-partner-ai/SKILL.md`
- Related skill in another pack (once the model is validated and a
  full business case is needed):
  `../../../business-case-and-analysis/skills/business-case-builder/SKILL.md`
- A ready-made skill chain for this situation: see `../../../playbooks/`
- This pack's shared guardrails: `../../CLAUDE.md`

## References

- `../../references/ai-native-reshuffle-heuristics-research.md` —
  grounding notes for the proprietary learning-engine principle in
  step 6
- `../../references/` — the pack's shared background material
- `../../CLAUDE.md` — the pack's shared guardrails
