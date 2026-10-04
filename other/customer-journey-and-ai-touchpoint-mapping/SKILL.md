---
name: customer-journey-and-ai-touchpoint-mapping
description: "Maps the stages and friction points of a customer's service journey, and places AI on the journey only at the points where it genuinely creates value for the customer — not technology-first."
---

# Customer Journey & AI Touchpoint Mapping

## Purpose

Maps the customer's service journey stage by stage from the customer's own
point of view, identifies friction points, and deliberately decides where
on the journey AI is worth placing — only where it removes real friction or
creates new value, not everywhere it's technically possible.

## Anchored in research

- The service design / customer journey mapping tradition (a widely known
  service design technique, e.g. Stickdorn & Schneider, *This Is Service
  Design Thinking*).
- A research report supplied by the user, "AI Business Designer in the Age
  of AI" (2026) — the concept-and-modeling section: strategic goals are
  translated into service journeys and prototypes, and AI is placed on the
  journey in a way that adds value.

## Method

1. **Choose the customer journey to examine** (e.g. the purchase process,
   onboarding, a support process) and set its start and end points.
2. **Map the journey's stages chronologically from the customer's point of
   view** — what the customer does, thinks, and feels at each stage. Use a
   standard journey-map structure (stage, customer action, customer
   thought, customer emotion, touchpoint/channel) so the map stays
   comparable across projects.
3. **Identify friction points (pain points):** at which stages does the
   customer experience frustration, uncertainty, delay, or unnecessary
   effort? Distinguish friction the customer actually notices from friction
   that's only visible internally (e.g. a manual handoff between two teams
   that the customer never sees) — this skill maps the former.
4. **At each friction point, ask whether this is a problem where AI could
   genuinely create value for the customer** — not just internal
   efficiency. Use the triage in
   `../../../ai-strategy-and-governance/skills/ai-opportunity-portfolio/SKILL.md`
   (prediction/classification/generation + data availability) for this
   assessment, and check specifically: does removing this friction change
   what the customer *experiences*, or only what happens behind the scenes?
   Internal efficiency gains belong in a value chain or automation-fit
   analysis, not on this map.
5. **Place AI touchpoints on the journey only at the points where they
   remove real friction or create new value** — resist adding AI simply
   because it's possible. A journey stage with no identified friction point
   is a candidate for *no* AI touchpoint, and that's a legitimate outcome
   of this exercise, not a gap to fill.
6. **Check the overall picture:** does the sum of the AI touchpoints
   produce a coherent, consistent experience, or a scattered collection of
   isolated AI features that each solve a local problem but don't add up to
   a journey the customer would describe as "better"?
7. **Produce a structured journey map** (stage, friction point, AI
   touchpoint or not, rationale) and validate it with customer data or
   interviews, not just an internal assumption.

## What this skill does NOT do

- Doesn't replace real customer research — identifying friction points is
  only as good as the customer data behind it, not an internal assumption.
- Doesn't make the AI implementation decision for you — see
  `../../../ai-strategy-and-governance/skills/ai-opportunity-portfolio/SKILL.md`
  and `ai-use-case-feasibility-and-poc-scoping` for the technical/business
  assessment.
- Isn't the same thing as `../value-chain-mapping/SKILL.md` — the value
  chain looks at the company's internal activities; this skill looks at the
  customer's experience from the outside in.

## Refinement notes

Areas to keep deepening with real practice:

- your own rules of thumb for when an AI touchpoint is worth adding to the
  journey vs. when it isn't
- concrete templates (into `../../references/`, e.g. a journey-map
  template)
- reference cases / your own examples of a successful or failed AI
  touchpoint placement
- what this skill deliberately does *not* do (guardrails, common mistakes) —
  add to the list above

Once this section is filled in and validated in practice, update the
`maturity` field in `skills_index.json` to `draft`, `validated`, or
`canonical` (see `../../../meta/maturity_levels.md`). **Don't add new
fields to the frontmatter** — `name` and `description` are the only ones
allowed (see `../../../meta/frontmatter_schema.md`).

## Continue from here

- Related skill in the same pack: `../value-chain-mapping/SKILL.md`
  (a complementary internal perspective), `../strategy-canvas-and-value-curve/SKILL.md`
  (friction points can be sources of differentiation against competitors).
- Related skill in another pack:
  `../../../ai-strategy-and-governance/skills/ai-opportunity-portfolio/SKILL.md`,
  `../../../specialisation-packs/ai-native-startup-design/skills/customer-vision-to-jtbd/SKILL.md`
  (JTBD-based customer understanding supports building the journey).
- This pack's shared guardrails: `../../CLAUDE.md`

## References

- `../../references/` — the pack's shared background material
- `../../CLAUDE.md` — the pack's shared guardrails
