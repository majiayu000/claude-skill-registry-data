---
name: stage1-neurips-breakdown
description: Break down full NeurIPS reviewer responses into structured rebuttal units. Use when input contains NeurIPS reviewer fields (Summary, Strengths and Weaknesses, Questions, Limitations) and numeric scores (Rating, Confidence, Quality, Clarity, Significance, Originality). Splits questions and limitations into granular response items while preserving original wording for quoted issues.
---

# Stage 1 · NeurIPS Breakdown Skill (Template Extension)

Apply the shared template first:

- `skills/stage1/template/SKILL.md`

Then apply only the NeurIPS-specific overrides below.

## NeurIPS overrides

### Score mapping (required keys)

Extract exactly these six keys (numbers only):

- `rating` <- NeurIPS `Rating` / `Overall`
- `confidence` <- NeurIPS `Confidence`
- `quality` <- NeurIPS `Quality`
- `clarity` <- NeurIPS `Clarity`
- `significance` <- NeurIPS `Significance`
- `originality` <- NeurIPS `Originality`

Scores may appear as `3: good` or `5: Accept` — extract the leading number only.

### Preserved section mapping

- `summary` <- `Summary`
- `strength` <- `Strengths And Weaknesses`

### Atomic issue source mapping

- weakness-type source <- `Questions` (label as `weakness`)
- question-type source <- `Limitations` (label as `question`)

### Output header and score block

- Header must be exactly: `# Stage1 NeurIPS Breakdown`
- `## Scores` must contain exactly the six keys above.

## NeurIPS notes

- The `Limitations` field sometimes contains a standard phrase ("The authors thoroughly discussed the limitations of their work.") — preserve it verbatim rather than splitting into atomic issues if it is a single affirmative statement.
- Score values may include descriptive labels after the colon (e.g. `4: excellent`) — extract only the numeric portion.
