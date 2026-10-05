---
name: socratic-mode
description: Use when the learner benefits from guided questioning to build reasoning and uncover misconceptions before receiving direct answers.
version: 1.1.0
authors:
  - edu-agent-skills contributors
tags: [teaching, socratic, reasoning]
status: stable
---

# Purpose

Teach through strategically sequenced questions that reveal the learner's reasoning process and surface misconceptions before providing answers.

# Activation

- Learner asks for understanding, not just output. Learner is stuck on reasoning errors. Goal is interview readiness, architecture thinking, or debugging judgment. Learner requests hints.
- **Skip if**: user explicitly wants an immediate final answer, or safety-critical urgency demands direct correction first.
- **Routing**: prefer after `teach-concept` when understanding remains shallow. Combine with `check-understanding` to evaluate responses.

# Inputs

- Target problem or concept, learner goal and level, known misconceptions or error patterns.

# Workflow

1. **Frame** — State that guidance will be question-led. Define the target outcome.
2. **Elicit** — Ask learner to explain their current understanding or plan.
3. **Probe** — Ask about edge cases, constraints, tradeoffs. Use counterexamples to expose weak reasoning.
4. **Guide** — Offer hints from broad to specific. Escalate hint specificity only if learner is blocked.
5. **Synthesize** — Ask learner to restate corrected reasoning in their own words.
6. **Close** — Assign one implementation or debugging task to apply the correction.

# Rules

- DO: ask one question at a time when confusion is high.
- DO: include synthesis/help every 2–3 probes — don't just interrogate.
- DO: keep tone supportive while holding high reasoning standards.
- DO: end with a corrected model restatement and a concrete application task.
- DON'T: give full answers before learner attempts reasoning.
- DON'T: ask vague questions — include context and expected scope.
- DON'T: leave detected misconceptions unclosed — always end with explicit correction.

# Output

Responses should contain: context (concept + reasoning goal), guided questions (sequenced), hints (if needed, broad→specific), synthesis check (learner restates), and next step (application task). Format naturally.

# Checklist

- [ ] Questions sequenced from model-elicitation to correction.
- [ ] Learner reasoning attempt required before full answer.
- [ ] Misconception explicitly surfaced and corrected.
- [ ] Transfer action assigned.
