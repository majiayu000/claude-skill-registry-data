---
name: ai-accuracy-guardrails-and-grounding-design
description: "Designs absolute guardrails and grounds AI outputs against a named source of truth to counter sycophancy and hallucination, weighed against \"tokonomics\" — the cost, latency, and token price of every added guardrail instruction — so safety is achieved with the minimum instruction footprint, not the maximum."
---

# AI Accuracy Guardrails & Grounding Design

## Purpose

Separates two things that get conflated under "the AI is wrong":
**accuracy** (is the underlying claim actually true) and **precision** (is
the response consistent and repeatable). An AI can be highly precise and
confidently, consistently wrong — the specific failure mode this skill
guards against is sycophancy: a model tuned to please the user, agreeing
with or elaborating on an incorrect premise instead of correcting it. This
skill designs the two mechanisms that catch that failure — absolute
guardrails and grounding against an external source of truth — and weighs
their cost.

## Anchored in research

- The accuracy/precision distinction and the sycophancy risk are drawn
  from the source material's synthesis of 2026 AI product-design practice
  (unattributed to a single named individual in a way that could be
  independently verified) — treat as an established industry concern
  rather than one person's original claim; sycophancy as a systemic LLM
  risk is broadly documented across the AI safety and product-design
  literature.
- The Whoop fitness-bot example (absolute topical guardrails — a fitness
  AI must refuse and redirect away from unrelated topics regardless of how
  the user tries to provoke it) and the IMDb example (grounding a movie
  cast question against IMDb as the specific source of truth, rather than
  the model's own trained knowledge) are used in the source material as
  illustrative cases. Neither has been independently verified against the
  named companies' own published documentation — use them as illustrations
  of the pattern (absolute topical guardrails; grounding against a named,
  authoritative source), not as confirmed citations of those companies'
  actual systems.
- "Tokonomics" (the source material's term for the cost/latency/token
  trade-off of guardrail complexity) is used here as a practical design
  heuristic, not a citation-requiring claim — the underlying trade-off
  (longer system instructions cost more tokens and add latency) is a
  straightforward, verifiable property of how LLMs are billed and run.

## Method

1. **Separate every quality complaint into an accuracy problem or a
   precision problem before designing a fix** — they need different
   guardrails. A model that gives different plausible-sounding answers to
   the same question each time is a precision problem (see
   `../ai-behavioral-specification-design/SKILL.md`'s temperature
   guidance). A model that confidently states something false is an
   accuracy problem — that's this skill's territory.
2. **Name the sycophancy risk explicitly wherever the AI interacts with a
   confident or leading user statement.** Write a rule into the guardrail
   spec that the AI checks a claim against ground truth (step 4) before
   agreeing with or elaborating on it, especially when the user states
   something as fact. An AI that only ever validates the user's framing is
   optimizing for approval, not correctness.
3. **Design absolute guardrails for anything genuinely out of scope or
   unsafe** — a hard "never" rule, not a soft preference, for topics the
   product must categorically decline regardless of how persistently or
   cleverly a user tries to provoke a response (see
   `../ai-behavioral-specification-design/SKILL.md` step 4 for HOW it
   declines — the redirect language). List these explicitly; don't assume
   the model will infer scope boundaries reliably on its own.
4. **Name a specific source of truth for every category of factual
   claim the AI makes**, and require the AI to check against it rather
   than answer from its own trained knowledge alone. "The system should
   only report what's actually true according to [named authoritative
   source]" is a testable design rule; "the system should be accurate" is
   not. If no authoritative source exists for a claim category, that's a
   signal the AI shouldn't be making confident claims in that category at
   all — flag it for a lower-confidence framing or an escalation (see
   `../hitl-maturity-and-confidence-routing/SKILL.md`).
5. **Weigh every added guardrail instruction against its "tokonomics"** —
   longer, more elaborate system instructions cost more in tokens, add
   latency, and (past a point) can start to confuse the model about
   priority among instructions. The design goal is maximum safety with
   minimum instruction footprint, not maximum instruction length. If a
   guardrail can be achieved with a shorter, sharper rule instead of an
   exhaustive list of edge cases, prefer the shorter rule and test it
   against the edge cases rather than writing all of them into the prompt.
6. **Test the guardrail set against adversarial framing, not just
   straightforward requests** — a user rephrasing a disallowed request as
   a hypothetical, a role-play, or a "just curious" aside is a normal
   real-world pattern, not an edge case to skip.
7. **Produce a structured output**: the accuracy/precision split for the
   product's main claim categories, the named source-of-truth per
   category, the absolute-guardrail list, and a short note on the
   token/latency cost of the guardrail set as designed.

## What this skill does NOT do

- Doesn't design the AI's tone or sentiment — see
  `../ai-behavioral-specification-design/SKILL.md`.
- Doesn't implement the retrieval/grounding pipeline technically (e.g. a
  RAG architecture against the named source of truth) — that's an
  engineering task; this skill specifies WHICH source and WHAT must be
  checked against it.
- Doesn't guarantee zero hallucination — grounding and guardrails reduce
  the risk materially, they don't eliminate it; a genuinely high-stakes
  claim category still needs the escalation path from
  `../hitl-maturity-and-confidence-routing/SKILL.md`, not guardrails alone.
- Doesn't perform the regulatory/ethics risk check — see
  `../../../ai-strategy-and-governance/skills/responsible-ai-and-governance-check/SKILL.md`.

## Refinement notes

Areas to keep deepening with real practice:

- your own worked examples of a sycophancy failure caught in review, and
  the guardrail rule that would have prevented it
- a concrete "source of truth" mapping template per claim category (into
  `../../references/`)
- real before/after token-cost comparisons for a guardrail set that was
  successfully shortened without losing safety coverage

Once this section is filled in and validated in practice, update the
`maturity` field in `skills_index.json` to `draft`, `validated`, or
`canonical` (see `../../../meta/maturity_levels.md`). **Don't add new
fields to the frontmatter** — `name` and `description` are the only ones
allowed (see `../../../meta/frontmatter_schema.md`).

## Continue from here

- Before this in this pack: `../ai-behavioral-specification-design/SKILL.md`
  — the tone/sentiment layer this skill's guardrails sit underneath.
- Next in this pack: `../hitl-override-metrics-and-feedback-audit/SKILL.md`
  — measures whether the guardrails designed here are actually holding up
  in production.
- Related skill in another pack:
  `../../../ai-strategy-and-governance/skills/responsible-ai-and-governance-check/SKILL.md`
  — the regulatory/ethics layer, complementary to this skill's product-
  design layer.
- This pack's shared guardrails: `../../CLAUDE.md`

## References

- `../../references/hitl-partnership-heuristics-research.md` — full
  sourcing and grounding-strength notes for this pack
- `../../references/` — the pack's shared background material
- `../../CLAUDE.md` — the pack's shared guardrails
