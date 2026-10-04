---
name: layer-based-business-structuring
description: "Structures a business, service concept, or business model into distinct functional layers (OSI-model-like) from infrastructure to brand, in order to decide which layers to build in-house and which to source through partners."
---

# Layer-Based Business Structuring

## Purpose

Structures a business, service concept, or business model into distinct
functional layers — analogous to the telecommunications OSI model — from
the physical/infrastructure layer up to the brand layer, or, from a
commerce perspective, into layers such as logistics, contracts, payments,
assortment, and marketing. The core idea of a layer model is to separate
distinct functional units into their own, independent layers, so that each
layer can be decided on its own merits: build it in-house, or source it
through a partner.

## Anchored in research

- The OSI model (telecommunications, ISO/IEC 7498-1) — the original
  inspiration for the layer principle: each layer handles its own, bounded
  task and can be swapped out and tested independently without other
  layers needing to know anything about its internal implementation.
- Hagel, J. & Singer, M. (1999), "Unbundling the Corporation," *Harvard
  Business Review* — three underlying businesses that most companies bundle
  into a single organization: infrastructure management (optimized for
  scale), product innovation (optimized for speed), and customer
  relationship management (optimized for scope). These three can't be
  optimized simultaneously — which is why separating them into their own
  layers is often worthwhile.
- Baldwin, C. & Clark, K. (2000), *Design Rules: The Power of Modularity* —
  modularity theory: splitting a system into modules/layers with clear
  interfaces allows each part to be developed, replaced, or outsourced
  independently, without having to redesign the whole system.

## Method

1. **Pick a layer perspective that fits the situation.** Examples: a
   **technical/functional stack** (infrastructure → operations → product/
   service → customer interface → brand), or a **commerce stack**
   (logistics → contracts → payments → assortment → marketing → customer
   experience). The layer perspective always has to be adapted to context —
   there's no single correct way to divide it up.
2. **List every functional part of the business or concept** and assign
   each one to the layer it belongs in.
3. **Define each layer's interface to its neighboring layers** — what it
   takes in and what it produces — so the layers stay genuinely swappable
   (as in the OSI model: each layer provides a service to the layer above
   it without that layer needing to know how it's implemented internally).
4. **Classify each layer using the Hagel & Singer lens.** Ask which of the
   three underlying businesses the layer belongs to — infrastructure
   management (wins on scale and low unit cost), product innovation (wins
   on speed to market and creative talent), or customer relationship
   management (wins on scope and reach) — and note that these three logics
   pull against each other inside a single organization. A layer that is a
   genuine source of competitive advantage under its logic is a build
   candidate; a layer that is mature or commoditized, or that is optimized
   under a different logic than the rest of your business, is a partner or
   buy candidate.
5. **Make a build/partner/buy call layer by layer**, using step 4's
   classification as the primary input (the same decision logic applies
   outside AI contexts too — see
   `../../../ai-strategy-and-governance/skills/build-vs-buy-vs-partner-ai/SKILL.md`).
6. **Check the modularity of the interfaces you've drawn**, per Baldwin &
   Clark: can a layer actually be replaced without redesigning its
   neighbors? A layer boundary that leaks implementation detail into the
   next layer isn't a real module yet — tighten the interface before
   treating the build/partner decision as final.
7. **Visualize the layer model as a stack** (e.g. bottom to top) and mark
   each layer's build/partner decision and its rationale.
8. **Check the whole:** does the sum of the layers produce a coherent
   customer experience, or does friction at the interfaces show through to
   the customer (e.g. a slow handoff when two layers sit with different
   providers)?

## What this skill does NOT do

- Doesn't hand you a ready-made layer breakdown for every situation — the
  layer perspective always has to be chosen and adapted to context.
- Doesn't make the build/partner/buy decision for you — it structures the
  decision criteria layer by layer to support a human decision.
- Doesn't replace in-depth supplier or partner due diligence for an
  individual layer's outsourcing decision.

## Refinement notes

Areas to keep deepening with real practice:

- your own standard layer breakdowns that you reuse repeatedly in specific
  industries/situations
- concrete templates (into `../../references/`, e.g. layer-stack templates)
- reference cases / your own examples of a successful or failed layer split
- what this skill deliberately does *not* do (guardrails, common mistakes) —
  add to the list above

Once this section is filled in and validated in practice, update the
`maturity` field in `skills_index.json` to `draft`, `validated`, or
`canonical` (see `../../../meta/maturity_levels.md`). **Don't add new
fields to the frontmatter** — `name` and `description` are the only ones
allowed (see `../../../meta/frontmatter_schema.md`).

## Continue from here

- Next in this pack: `../value-chain-mapping/SKILL.md` — structures the
  business according to Porter's value chain model into primary and
  support activities; a second, more traditional way to structure the same
  business.
- Related skill in another pack: `../../../ai-strategy-and-governance/skills/build-vs-buy-vs-partner-ai/SKILL.md`
- This pack's shared guardrails: `../../CLAUDE.md`

## References

- `../../references/` — the pack's shared background material
- `../../CLAUDE.md` — the pack's shared guardrails
