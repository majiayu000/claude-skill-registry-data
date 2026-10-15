---
name: quiz
description: Interactive quiz from flashcards or topic area with scoring and review
version: 0.1.0
execution-mode: advisory
argument-hint: "<topic> [count] [difficulty]"
category: fleet-ops
status: candidate
---
# [quiz]

## When to Use
- Self-assessment during certification study
- Testing retention after a study session
- CCA-F exam preparation
- Quick knowledge check on any topic with existing flashcards

## Execution

### Inputs
- **topic** (required): Must match a flashcard deck in `_state/study/<topic>/`
- **count** (optional): Number of questions, default 10
- **difficulty** (optional): `easy`, `medium`, `hard`, `mixed` (default: mixed)

### Steps
1. Load flashcard deck from `_state/study/<topic>/cards.json`
2. If no deck exists, offer to generate one first via `[flashcard] generate`
3. Select cards based on difficulty filter and spaced repetition priority
4. Randomize question order
5. For each question, generate 3 plausible distractors from other cards or domain knowledge
6. Present all questions with answers hidden behind a clear separator
7. Score: correct/total, percentage, per-difficulty breakdown
8. List wrong answers with correct explanations
9. Save results to `_state/study/<topic>/quiz-history.json`

### Question Formats (vary within quiz)
- **Multiple choice**: Q + 4 options (1 correct, 3 distractors)
- **True/False**: Statement derived from card, randomly true or inverted
- **Fill-in**: Key term blanked from answer

## Output Format

```
Quiz | CCA-F (10 questions, mixed difficulty)
============================================================

Q1 [medium]: What are the three pillars of AI governance?
  a) Speed, scale, automation
  b) Transparency, accountability, fairness
  c) Privacy, security, compliance
  d) Design, deployment, monitoring

Q2 [hard]: Which framework specifically addresses AI risk
   at the organizational level?
  a) ISO 27001
  b) NIST AI RMF
  c) SOC 2
  d) GDPR

... (8 more questions)

============ ANSWERS (attempt before scrolling) ============

Q1: b) Transparency, accountability, fairness
Q2: b) NIST AI RMF
...

## Score: 8/10 (80%)
| Difficulty | Correct | Total |
|------------|---------|-------|
| Easy       | 3/3     | 100%  |
| Medium     | 3/4     | 75%   |
| Hard       | 2/3     | 67%   |

## Review These:
- Q5: Difference between AI audit and AI assessment [medium]
- Q9: OECD AI Principles adoption timeline [hard]

Saved to: _state/study/cca-f/quiz-history.json
------------------------------------------------------------
Next: [flashcard] review CCA-F (review missed cards)
```

## Skill Chains
- After quiz with <80% -> suggest `[flashcard] review` on missed topics
- After quiz with >90% -> suggest moving to next domain via `[study-plan]`
- Track study time with `[cert-tracker]`
