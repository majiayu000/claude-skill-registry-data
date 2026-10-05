---
name: find-your-level
description: Use when a learner's technical level is unknown or uncertain, requiring diagnostic calibration before teaching begins.
version: 1.1.0
authors:
  - edu-agent-skills contributors
tags: [onboarding, level-detection, calibration, prerequisite-awareness]
status: stable
---

# Purpose

Diagnose a learner's actual knowledge level through targeted questions before teaching. Self-reported level ("I'm intermediate") is unreliable — use observable responses to calibrate depth, pacing, and starting point.

# Activation

- New learner with no prior profile. Self-reported level inconsistent with responses. New topic with unknown background. Stale profile (2+ weeks) needs reconfirmation. Learner says "I'm not sure where to start."
- **Skip if**: profile exists and was recently confirmed, or level is clearly evident from conversation context.
- **Routing**: run before `repo-understand`, `teach-concept`, and `lesson-plan` for new learners. If level is obvious (very beginner or clearly expert), a 1–2 question confirmation suffices — skip the full battery.

# Inputs

- Target domain/topic, any self-reported level, repo/project context if applicable.

# Level Definitions

- **Beginner**: can't explain core vocabulary or trace a basic example.
- **Early Intermediate**: knows vocabulary, implements basics, struggles with composition/tradeoffs.
- **Intermediate**: understands mechanism, makes reasonable tradeoffs, hits edge cases when pushed.
- **Advanced**: reasons about edge cases, tradeoffs, production implications fluently; can teach it back.

# Diagnostic Tiers

3–5 questions in escalating difficulty. Stop when ceiling is reached (two consecutive weak answers).

- **Tier 1**: "Explain X in one sentence." → Fluent: advance. Not: Beginner.
- **Tier 2**: "Write/describe a minimal example of X." → Correct mechanism: advance. Partial: Early Intermediate.
- **Tier 3**: "When would you NOT use X?" → Genuine tradeoffs: advance. Vague: Intermediate.
- **Tier 4**: "Describe a production failure mode involving X." → Detailed: Advanced. Partial: Intermediate-Advanced.

# Workflow

1. **Align** — Confirm domain and goal. Ask self-reported confidence (1–5). Record as starting hypothesis, not conclusion.
2. **Diagnose** — Start at tier matching self-report minus one. Ask one question at a time. Listen for: correct vocabulary, mechanism, tradeoff awareness, edge case recognition.
3. **Infer** — Level = highest tier answered confidently. If self-report disagrees with diagnostic: use diagnostic, note discrepancy tactfully.
4. **Confirm** — State inferred level with rationale. Ask: "Does this feel right?" Adjust based on learner input.
5. **Recommend** — Beginner: start at prerequisites. Early Intermediate: mechanism + applied examples. Intermediate: tradeoffs + project context. Advanced: edge cases or deep-dive.

# Rules

- DO: use domain-specific questions, not generic programming trivia.
- DO: stop after two consecutive weak answers — don't interrogate.
- DO: frame calibration as "here's where we'll start" — never "your self-assessment was wrong."
- DO: always confirm inferred level with the learner before starting.
- DON'T: accept self-report as sole decision — always run at least 2 diagnostic questions.
- DON'T: shame overconfident learners.
- DON'T: run all tiers mechanically when ceiling is clearly reached.

# Output

Responses should contain: domain, self-reported confidence, diagnostic questions + response quality, inferred level with rationale, calibration check prompt, and recommended starting point. Format naturally.

# Checklist

- [ ] Diagnostic questions are domain-specific.
- [ ] Battery stops when ceiling reached.
- [ ] Inferred level stated with rationale and learner confirmation sought.
- [ ] Starting point matches inferred level.
