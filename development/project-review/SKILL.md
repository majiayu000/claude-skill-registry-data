---
name: project-review
description: Use when evaluating a completed or in-progress project across scope, correctness, quality, testing, and learning outcomes using structured Praise-Critique-Grow feedback.
version: 1.1.0
authors:
  - edu-agent-skills contributors
tags: [projects, review, feedback, assessment]
status: stable
---

# Purpose

Provide structured, constructive review of a learner's project at a milestone or completion checkpoint. Combines technical evaluation with learning-outcome assessment. Uses Praise-Critique-Grow to maintain learner motivation while surfacing real issues.

# Activation

- Milestone reached in `build-with-me`. Feature or project completed. Learner asks for feedback on their work. Pre-submission review (assignment, portfolio, interview take-home).
- **Skip if**: project hasn't started. Learner needs concept help → `teach-concept`. Active debugging in progress → `debug-teacher`.
- **Routing**: issues found → use `challenge-generator` for targeted practice. Concept gaps → `teach-concept`. Design issues → `architecture-review`. Log weak areas to `weak-area-tracker`.

# Inputs

- Project/feature code and documentation, original requirements/scope, learner's stated goals, relevant assessment criteria.

# Review Dimensions

- **Scope**: does it meet stated requirements? Scope creep? Missing features?
- **Correctness**: does it produce correct results? Edge cases handled?
- **Code Quality**: readability, naming, structure, DRY, separation of concerns.
- **Testing**: test coverage, test quality, edge case testing.
- **Learning Outcomes**: what did the learner demonstrate they understand? What gaps remain?

# Workflow

1. **Self-Assessment** — Ask learner first: "What do you think went well? What would you change?" This surfaces their self-awareness before external feedback.
2. **Review** — Evaluate across all 5 dimensions. Note strengths and issues with specific code/design references.
3. **Praise** — Start with 2–3 specific strengths. Reference actual decisions/code, not generic compliments.
4. **Critique** — List issues priority-ordered. Each: dimension, description, severity, specific code reference. Max 5 issues per review — more overwhelms.
5. **Grow** — For each major issue: one concrete next action. Frame as growth opportunity, not failure. Include a learning recommendation (skill or concept to revisit).
6. **Retrospective** — Ask one synthesis question: "What's the most important thing you learned from building this?" Record answer for `learning-memory`.

# Rules

- DO: require self-assessment before giving feedback.
- DO: praise specific decisions, not generic effort.
- DO: limit critique to top 5 issues — prioritize by impact.
- DO: frame growth actions as opportunities, not failures.
- DO: end with a retrospective question and record the answer.
- DON'T: start with criticism — always Praise first.
- DON'T: give vague feedback ("good job" / "needs work").
- DON'T: rewrite the learner's code — point to issues and let them fix.
- DON'T: skip the self-assessment — it builds metacognitive skill.

# Output

Responses should contain: self-assessment prompt, praise (2–3 specific strengths), critique (issues with dimension + severity + code reference), grow (next actions + learning recommendations), and retrospective question. Format naturally.

# Checklist

- [ ] Self-assessment requested before external feedback.
- [ ] Praise references specific code/decisions.
- [ ] Critique limited to top 5 issues, priority-ordered.
- [ ] Retrospective question asked and answer recorded.
