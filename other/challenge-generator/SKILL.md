---
name: challenge-generator
description: Use when generating personalized practice challenges calibrated to the learner's weak areas, level, and project context.
version: 1.1.0
authors:
  - edu-agent-skills contributors
tags: [assessment, practice, active-learning, weak-area-targeting]
status: stable
---

# Purpose

Generate targeted, level-appropriate practice challenges that force application over recall. Challenges must be grounded in learner's weak areas, current project, and chosen difficulty tier.

# Activation

- Concept just taught and practice needed. Learner asks for exercises/challenges. `check-understanding` or `misconception-detector` flagged a weak area. Interview/exam/milestone prep.
- **Skip if**: no concept context established → run `teach-concept` first. Learner is blocked on production issue → `debug-teacher`.
- **Routing**: pair with `check-understanding` to evaluate responses. Escalate to `interview-mode` for timed pressure practice.

# Inputs

- Target concept(s), learner level, known weak areas, project/repo context, preferred type (implement/debug/explain/design).

# Challenge Types

- **Implement**: write code from scratch to satisfy criteria.
- **Debug**: identify and fix a deliberately broken snippet.
- **Explain**: articulate behavior, tradeoffs, or mechanism in prose.
- **Design**: propose architecture or algorithm for given constraints.

# Difficulty Tiers

- **Beginner**: one concept, well-defined, limited scope.
- **Intermediate**: composite concepts, partially specified, tradeoff thinking required.
- **Advanced**: ambiguous spec, production constraints, edge-case awareness required.

# Workflow

1. **Calibrate** — Identify target concept(s) from session history or learner request. Select challenge type based on learning objective. Map learner level to difficulty tier.
2. **Construct** — State challenge clearly: context, constraints, success criteria, time/scope hint. Include starter scaffold where appropriate. Embed at least one non-obvious constraint testing deeper understanding.
3. **Hint Ladder** — Prepare 2–3 progressive hints (broad→specific) but don't volunteer them. Release only on request or after two failed attempts.
4. **Evaluate** — Grade reasoning quality, not just correctness. Identify what's right, where reasoning broke down, root cause. Classify: conceptual gap, implementation slip, or edge-case blindness.
5. **Advance or Retry** — Significant errors: simpler variant or targeted hint, then retry. Clean pass: increase tier or shift to next weak area.
6. **Reinforce** — Summarize the key insight the challenge surfaced. Record outcome for `weak-area-tracker`.

# Rules

- DO: require active reasoning — not definition recall.
- DO: make success criteria explicit and testable before learner starts.
- DO: state difficulty tier and confirm before starting.
- DO: ground at least one challenge variant in the learner's current project/repo.
- DON'T: reveal the solution before the learner attempts.
- DON'T: release hints before at least one learner attempt.
- DON'T: end without a one-sentence insight summary.
- DON'T: generate generic challenges disconnected from session context.

# Output

Responses should contain: context (concept + type + tier + grounding), challenge statement with acceptance criteria, starter scaffold if applicable, checkpoint prompt, and next step after evaluation. Format naturally.

# Checklist

- [ ] Difficulty tier stated and calibrated.
- [ ] Acceptance criteria are measurable.
- [ ] Challenge references session context or learner's project.
- [ ] Post-challenge insight summary included.
