---
name: simplify-topic
description: Use when a concept is too abstract for the learner's current level and needs analogy-first teaching before complexity re-injection.
version: 1.1.0
authors:
  - edu-agent-skills contributors
tags: [teaching, simplification, analogy, accessibility]
status: stable
---

# Purpose

Reframe a concept at a lower abstraction so the learner builds accurate intuition before encountering technical complexity. Simplification is choosing the right abstraction for the learner's mental model, then re-injecting complexity once the foundation is stable.

# Activation

- Learner says "I don't understand" or "explain like I'm new." `check-understanding` reveals prior explanation was too abstract/jargon-heavy. Cross-domain learner needs an analogy bridge. `teach-concept` was used and learner still can't state the core intuition.
- **Skip if**: learner understands basics and needs depth → `deep-dive`. Confusion is from a misconception → `misconception-detector`. Concept is simple enough already.
- **Routing**: after successful simplification, use `teach-concept` to re-introduce correct technical terminology. Never leave learner permanently at simplified level.

# Inputs

- Concept to simplify, learner's background domain, abstraction level where understanding broke, specific unclear aspect.

# Abstraction Levels

- **Level 0 (Everyday)**: household/daily life analogy, zero technical vocab → absolute beginner.
- **Level 1 (Domain-Adjacent)**: analogy from learner's known field → practitioner switching domains.
- **Level 2 (Simplified Technical)**: correct terms, simplified mechanism → beginner with some background.
- **Level 3 (Full Technical)**: precise mechanism with edge cases → standard `teach-concept` level.

# Workflow

1. **Detect** — Ask one question to identify where understanding breaks (terminology? mechanism? motivation?). Identify learner's domain for analogy selection. Select starting level (0, 1, or 2).
2. **Build Analogy** — One analogy from the learner's known domain. State explicitly where it holds AND where it breaks down — oversimplified analogies create new misconceptions.
3. **Simplified Explanation** — Deliver at selected level using the analogy as scaffold. One core idea per step. No technical vocabulary at level 0; introduce terms one at a time at level 2.
4. **Intuition Check** — Ask learner to restate in their own words using the analogy. If wrong: identify failure point and rebuild with a different analogy.
5. **Complexity Re-Injection** — Introduce one layer of technical accuracy on top of confirmed intuition. Replace analogy language with correct terms, one at a time. Confirm at each step.
6. **Handoff** — When learner articulates using correct vocabulary: hand off to `teach-concept` or `deep-dive`.

# Rules

- DO: always state where the analogy breaks down — analogies that never fail create misconceptions.
- DO: complexity re-injection is mandatory — simplification is a bridge, not a destination.
- DO: confirm the analogy domain is familiar to the learner before using it.
- DON'T: use multiple analogies simultaneously — pick the best one until it fails.
- DON'T: discard a failing analogy until after 2 attempts; then switch.
- DON'T: leave the session at simplified level — at minimum introduce correct vocabulary.
- DON'T: simplify a concept the learner already understands correctly — probe first.

# Output

Responses should contain: context (concept + confusion level + learner background + selected level), analogy (with explicit limits), simplified explanation, intuition check prompt, complexity re-injection steps, and handoff plan. Format naturally.

# Checklist

- [ ] Analogy grounded in learner's known domain and limits stated.
- [ ] Learner restates concept using analogy before re-injection.
- [ ] Complexity re-injection introduces correct technical vocabulary.
- [ ] Session does not end at simplified level.
