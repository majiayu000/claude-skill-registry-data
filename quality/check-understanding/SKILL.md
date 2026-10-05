---
name: check-understanding
description: Use when verifying whether the learner truly understands a concept through reasoning and application, not recall trivia.
version: 1.1.0
authors:
  - edu-agent-skills contributors
tags: [assessment, reasoning, misconception-detection]
status: stable
---

# Purpose

Assess conceptual and practical understanding using reasoning-first prompts, then adapt teaching based on detected weak areas.

# Activation

- Concept explanation just completed. Learner claims understanding and needs validation. Repeated related mistakes. Readiness check needed before advancing.
- **Skip if**: no concept context established, or user explicitly declines assessment.
- **Routing**: pair with `teach-concept` for explanation→assessment loops. Escalate to `socratic-mode` when misconceptions persist.

# Inputs

- Target concept(s), learner level, prior mistakes/confusion signals, repo/project context.

# Workflow

1. **Target** — Select 1–2 concepts being validated.
2. **Question** — Generate tiered questions: conceptual reasoning, practical application, debugging/diagnostic.
3. **Evaluate** — Grade reasoning quality, not keyword match.
4. **Classify** — Categorize mistakes: misconception, partial model, or execution gap.
5. **Correct** — Explain root cause and provide corrected model.
6. **Recheck** — One follow-up question to confirm recovery.

# Rules

- DO: test reasoning and transfer, not memorization.
- DO: use plausible distractors in MCQ format.
- DO: explain *why* an answer fails, not just that it's wrong.
- DO: track weak areas across turns when context allows.
- DON'T: use only right/wrong labels — always output mistake type and remediation.
- DON'T: end without a recheck after correction.
- DON'T: ignore repeated weak areas — log and prioritize them.

# Output

Responses should contain: concepts under assessment, questions (conceptual + practical + diagnostic), evaluation (strengths, weak areas, mistake types), corrective feedback, and recheck question. Format naturally.

# Checklist

- [ ] Includes conceptual and practical checks.
- [ ] Mistakes categorized, not just scored.
- [ ] Corrective feedback explains root cause.
- [ ] Follow-up recheck present.
