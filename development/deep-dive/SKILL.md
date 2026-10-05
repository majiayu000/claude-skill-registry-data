---
name: deep-dive
description: Use when a learner has surface understanding and needs to explore mechanism, tradeoffs, edge cases, and production implications at depth.
version: 1.1.0
authors:
  - edu-agent-skills contributors
tags: [teaching, depth, mechanism, advanced-learning]
status: stable
---

# Purpose

Take a learner from surface understanding to genuine depth on a single concept. Assumes the learner has a working mental model and pushes into mechanism, failure modes, tradeoffs, and production implications. Exit condition: learner can reason about the concept in novel, constrained contexts.

# Activation

- Learner asks to go deeper on a known concept. `check-understanding` confirms surface competence but weak mechanism knowledge. Interview prep or architectural decision needs depth.
- **Skip if**: beginner encountering concept for the first time → `teach-concept`. Needs immediate practical help → `build-with-me`/`debug-teacher`. Has a misconception → `misconception-detector` first.
- **Routing**: confirm current level with a quick probe before starting. Pair with `challenge-generator` at the end for advanced application.

# Inputs

- Target concept, confirmed current understanding level, motivating context (interview/architecture/debugging), known gaps or questions.

# Depth Ladder

Five rungs, each confirmed before ascending:
1. **Surface** — Definition and intuition → "State this in one sentence."
2. **Mechanism** — Step-by-step how it works → "Trace a concrete execution."
3. **Tradeoffs** — When it works vs. doesn't → "What would you choose instead, and why?"
4. **Edge Cases** — Boundaries and failures → "What breaks this?"
5. **Production** — Real-world tuning, monitoring, debugging → "How would you debug this at 3am?"

# Workflow

1. **Entry Check** — Ask one question to confirm starting rung. Skip confirmed rungs; jump to the frontier.
2. **Mechanism (Rung 2)** — Walk through with a concrete worked trace. Require learner to narrate it back.
3. **Tradeoffs (Rung 3)** — Present a decision context. Elicit learner's reasoning before canonical analysis. Include one case where the naive choice is wrong.
4. **Edge Cases (Rung 4)** — Pose 2–3 edge case questions. Require learner to surface them first, then supplement. For each: symptom + fix.
5. **Production (Rung 5)** — Observability, performance under load, tuning knobs, known failure patterns. Ground in a realistic system. Ask: "If this broke at 3am, what's your investigation sequence?"
6. **Exit Synthesis** — Ask learner to produce a one-paragraph explanation for someone who just learned the basics.

# Rules

- DO: confirm each rung before ascending — require exit question answers.
- DO: require learner narration at Rung 2, learner tradeoff reasoning at Rung 3, learner-surfaced edge cases at Rung 4.
- DO: use realistic scale at Rung 5 — not toy numbers.
- DON'T: re-teach confirmed surface level — skip to the frontier.
- DON'T: lecture all five rungs without learner participation at every rung.
- DON'T: end without learner producing an exit synthesis paragraph.

# Output

Responses should contain: context (concept + starting rung + motivation), depth ladder progress, current rung exploration, checkpoint question, and exit synthesis prompt. Format naturally per rung.

# Checklist

- [ ] Entry level confirmed; confirmed rungs skipped.
- [ ] Learner participation required at every rung.
- [ ] Rung 5 reached for intermediate+ learners.
- [ ] Exit synthesis produced by learner.
