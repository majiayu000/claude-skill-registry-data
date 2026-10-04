---
name: marketing-psychology
description: >-
  Apply psychological principles and behavioral design to product copy,
  onboarding flows, landing pages, feature descriptions, CTAs, and pricing
  tiers. Covers cognitive biases (loss aversion, social proof, anchoring,
  paradox of choice, Zeigarnik effect, IKEA effect, reciprocity, commitment &
  consistency) and the Fogg Behavior Model (B = MAP).
  Use when the user asks about copy psychology, persuasion, behavioral design,
  conversion optimization, onboarding flow design, CTA wording, pricing
  psychology, or ethical influence.
user-invocable: false
disable-model-invocation: false
version: "2.0.1"
author: "Ali Farahat"
tags: ["marketing-psychology", "behavioral-design", "cognitive-biases", "conversion", "ethical-influence"]
when_to_use: |
  USE WHEN:
  - User asks about copy psychology, persuasion, or behavioral design.
  - User is designing an onboarding flow, landing page, CTA, or pricing tier.
  - User asks how to frame a value proposition, nudge, or feature description.
  - User wants to reduce cognitive load or improve conversion without dark patterns.

  DO NOT USE WHEN:
  - User needs SEO (use everything-seo or seo-audit).
  - User needs agent discovery / well-known protocol cards (use agent-ready).
  - User needs overall startup marketing strategy (use startup-marketing-brain).
  - User is asking about visual/UI design, not behavioral copy.
---

# Marketing Psychology

> **Leading words:** loss aversion, social proof, anchoring, paradox of choice,
> Zeigarnik effect, IKEA effect, reciprocity, commitment & consistency, Fogg
> behavior model, ethical influence.

Apply cognitive biases and behavioral models to product surfaces — *ethically*.
The goal is to reduce cognitive load, surface genuine value, and help the user
act on what they already want — not to manipulate.

## Decision model — surface → principle

Pick the surface the user is working on, then apply the primary principle
(secondary principles reinforce). Depth on each principle lives in
[references/principles.md](references/principles.md).

| Surface | Primary principle | Secondary principle |
|---|---|---|
| CTA (call-to-action) | Commitment & consistency | Reciprocity |
| Pricing tier comparison | Anchoring | Loss aversion |
| Onboarding flow | IKEA effect | Paradox of choice (avoid) |
| Feature description | Loss aversion | Social proof |
| Reviews / testimonials / trust | Social proof | Reciprocity |
| Dashboard engagement | Zeigarnik effect | Loss aversion |
| Error / empty state | Reciprocity | Fogg: reduce ability cost |

## Phase 1 — Audit

```
- [ ] Identify the surface type from the decision model table above.
- [ ] Map the primary + secondary principle for that surface.
- [ ] Check the current copy's cognitive load (how many concepts must the
      user hold at once to act?).
- [ ] Check ethics: would the ethical-influence test pass? (see references/)
```

🛑 **Checkpoint:** State the surface type, primary/secondary principles, and
cognitive-load assessment in one sentence. Do not proceed to Design until the
audit is named.

## Phase 2 — Design

```
- [ ] Choose 1-2 principles max for the surface (more = noise).
- [ ] Inject the leading word for the chosen principle into the copy.
- [ ] Apply the pattern for that principle (see references/principles.md).
- [ ] Verify the principle is real, not fabricated (real metrics, real
      testimonials, real scarcity).
```

🛑 **Checkpoint:** Show the chosen principle(s) and the planned copy
structure. Do not draft prose until the design is named.

## Phase 3 — Write

```
- [ ] Draft the copy anchored by the leading word.
- [ ] Use concrete metrics over vague adjectives ("3 missed calls last week"
      > "many missed calls").
- [ ] Run the read-aloud test — does it sound like a person, not a marketer?
- [ ] Run the ethical-influence test (see references/ethical_boundaries.md).
```

## Phase 4 — Validate

```
- [ ] No dark patterns (fabricated stats, manufactured urgency, confirm-shaming,
      roach motel, bait-and-switch, asymmetric consent).
- [ ] No addiction design (infinite scroll without exit, variable reward
      exploitation).
- [ ] No product-truth overrides (claims must match what the feature actually
      does).
- [ ] Cognitive load reduced, not increased.
- [ ] Plain language — no marketing jargon the user would not use themselves.
```

Any miss → back to Phase 2.

## What NOT to do

Hard boundaries — see [references/ethical_boundaries.md](references/ethical_boundaries.md)
for the full list and the ethical-influence test. Summary:

- **No fabricated stats.** Real metrics only; if unknown, omit the figure.
- **No manufactured urgency.** Real scarcity only — countdowns that reset are
  deception.
- **No confirm-shaming.** Opt-out copy must be neutral.
- **No addiction design.** Surfaces must serve the user's goal, not exploit
  dopamine response.
- **No overriding product truth.** Copy must match what the feature actually does.

## References

| File | Use it for |
|---|---|
| [references/principles.md](references/principles.md) | Full reasoning behind each cognitive bias + the Fogg Behavior Model |
| [references/ethical_boundaries.md](references/ethical_boundaries.md) | Dark patterns, addiction design, product-truth overrides, ethical-influence test |
| [references/yappi_examples.md](references/yappi_examples.md) | Worked examples from the Yappi.ai context (the original skill's content) |
