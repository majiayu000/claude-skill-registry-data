---
name: ai-behavioral-specification-design
description: "Specifies an AI's sentiment, tone, and precision (\"temperature\") as an explicit design artifact — a Behavioral Document — instead of leaving it implicit; includes how the AI should redirect rather than go silent when it hits a guardrail, and \"prompt trees\" as the dynamic replacement for a static service blueprint."
---

# AI Behavioral Specification Design

## Purpose

Treats an AI's behavior — not just its capability — as something a
designer specifies on purpose, the same way a service designer specifies a
service blueprint. Traditional UI design isn't enough for an AI product,
because the AI's output IS the experience: its tone, how creative or
literal it is, and what it does when a user pushes it outside its intended
scope are all product decisions, not incidental model behavior. This skill
produces the artifact — a Behavioral Document — that a system prompt is
then built from, so the probabilistic system stays inside the brand and
safety boundaries a human actually decided on.

## Anchored in research

- Jasmine Orange (UX/experience designer, conference speaker on AI and
  design) — the principle that designers must own what "a good experience"
  means for an AI product so engineers have something concrete to test
  against, and the framing that an AI answering a user isn't optimizing
  for the objectively best answer but emulating what a knowledgeable human
  would have done. The general area of her public work matches this
  framing; the exact quote attributed to her in the source material for
  this skill could not be independently verified word-for-word — treat it
  as a paraphrase of a real, publicly discussed position, not a confirmed
  direct quote.
- Yasemin Cenberoglu — cited in the source material as the originator of
  "prompt trees" replacing static service blueprints. This specific
  individual and quote could not be independently verified in available
  search results. The underlying concept — that AI-native services need a
  dynamic decision structure instead of a fixed flowchart, because the
  system's actual path through a conversation is probabilistic — is
  independently well documented in 2026 UX literature on "probabilistic
  design" (e.g. Smashing Magazine's June 2026 piece "Designing With
  Uncertainty: How AI Supercharges Probabilistic Thinking"). Use the
  concept with confidence; treat the specific named attribution as
  unconfirmed.
- The Whoop fitness-AI guardrail example (a fitness AI redirecting a user
  who tries to steer the conversation toward an unrelated topic, e.g.
  political history, back to fitness) is used in the source material as an
  illustrative case for the redirect-not-silence principle in step 4. It
  has not been independently verified against Whoop's own published
  documentation — treat it as illustrative of the pattern, not a confirmed
  citation of Whoop's actual product behavior.

## Method

1. **Define sentiment before writing a single line of prompt.** Decide
   deliberately where this AI sits between professional and friendly, and
   write the decision down — don't let it emerge by accident from whichever
   examples happened to be in the first prompt draft. A support bot for a
   regulated financial product and a brainstorming companion for a
   creative team need opposite defaults.
2. **Guard against sycophancy explicitly.** An AI tuned purely to be
   agreeable will validate a user's incorrect assumption rather than
   correct it, especially under a confident or leading question. State in
   the behavioral spec where objectivity must override agreeableness (e.g.
   any factual claim, any safety-relevant judgment) — don't leave this to
   the model's default disposition.
3. **Set precision ("temperature") per task, not once for the whole
   product:**
   - **Low precision setting / high determinism (roughly 0.1–0.3
     temperature)** — for tasks needing a "bullseye" answer: billing,
     compliance text, factual lookups. Consistency matters more than
     variety.
   - **High precision setting / high creativity (roughly 0.7–1.0
     temperature)** — for ideation, brainstorming, marketing copy
     variation. Variance is the point.
   Cross-check this against the deterministic/probabilistic task
   classification in
   `../../../ai-strategy-and-governance/skills/task-level-decomposition-and-automation-fit/SKILL.md`'s
   error-tolerance criterion — the two should agree; if they don't,
   something in the task's risk profile has been misjudged on one side or
   the other.
4. **Design the redirect, not just the refusal.** When the AI hits a
   guardrail (an out-of-scope topic, an unsafe request), specify what it
   says and does next, not just what it won't do. Going silent or giving a
   generic refusal reads as broken; actively steering the user back to
   what the product IS for reads as designed. Write the actual redirect
   language into the behavioral spec, don't leave it to the model's
   improvisation.
5. **Build "prompt trees" for any AI-native service replacing a static
   flow.** A traditional service blueprint assumes one fixed sequence of
   steps; an AI-native equivalent needs a branching structure of
   assumptions and fallbacks that still holds together when the
   conversation takes an unplanned path. For each branch point, specify:
   what triggers it, what the AI should assume, and what it does if that
   assumption turns out wrong.
6. **Write the whole spec as a Behavioral Document** — a design artifact,
   not just prompt-engineering notes buried in an engineer's working file.
   It should be reviewable by a non-technical stakeholder and should be
   the thing a system prompt gets built FROM, not written independently of.
   Structure it by scenario: normal path, edge case, guardrail hit,
   ambiguous input.
7. **Test the spec against real edge cases before shipping**, specifically
   ones where a user tries to push the AI outside its intended sentiment,
   precision, or scope — a spec that only survives friendly test inputs
   hasn't actually been tested.
8. **Hand the finished Behavioral Document to
   `../ai-accuracy-guardrails-and-grounding-design/SKILL.md`** for the
   guardrail and grounding layer that sits underneath tone — sentiment and
   accuracy are different problems and need separate specification, even
   though they're often designed together in practice.

## What this skill does NOT do

- Doesn't write the production system prompt itself — produces the design
  spec a system prompt is built from.
- Doesn't set factual-accuracy guardrails or grounding rules — see
  `../ai-accuracy-guardrails-and-grounding-design/SKILL.md`.
- Doesn't decide the human-oversight level for a given task — see
  `../hitl-maturity-and-confidence-routing/SKILL.md`; use both together,
  since a behavioral spec and an oversight level are different design
  decisions that need to agree with each other.
- Doesn't replace
  `../../../specialisation-packs/ai-native-startup-design/skills/ai-native-conversational-os-design/SKILL.md`
  for the overall conversational architecture (Intent → Strategy Cards →
  Output Cards, etc.) — this skill specifies HOW the AI behaves within
  that architecture, not the architecture itself.

## Refinement notes

Areas to keep deepening with real practice:

- your own worked Behavioral Document template, with real
  sentiment/precision/redirect examples (into `../../references/`)
- concrete before/after examples of a redirect that worked vs. one that
  read as a broken refusal
- your own calibrated temperature ranges by task type, validated against
  real production behavior rather than the illustrative ranges above

Once this section is filled in and validated in practice, update the
`maturity` field in `skills_index.json` to `draft`, `validated`, or
`canonical` (see `../../../meta/maturity_levels.md`). **Don't add new
fields to the frontmatter** — `name` and `description` are the only ones
allowed (see `../../../meta/frontmatter_schema.md`).

## Continue from here

- Before this in this pack: `../hitl-maturity-and-confidence-routing/SKILL.md`
  — the oversight-level decision this skill's behavioral spec should agree
  with.
- Next in this pack: `../ai-accuracy-guardrails-and-grounding-design/SKILL.md`
  — the accuracy and grounding layer underneath tone.
- Related skill in another pack:
  `../../../specialisation-packs/ai-native-startup-design/skills/ai-native-conversational-os-design/SKILL.md`
  — the broader conversational architecture this skill's behavior spec
  fits inside.
- Related skill in another pack:
  `../../../ai-strategy-and-governance/skills/task-level-decomposition-and-automation-fit/SKILL.md`
  — the deterministic/probabilistic task classification that the
  precision-setting decision in step 3 should agree with.
- This pack's shared guardrails: `../../CLAUDE.md`

## References

- `../../references/hitl-partnership-heuristics-research.md` — full
  sourcing and grounding-strength notes for this pack
- `../../references/` — the pack's shared background material
- `../../CLAUDE.md` — the pack's shared guardrails
