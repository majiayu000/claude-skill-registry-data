---
name: agent-evaluation
description: Defines measurable evaluation metrics for extraction, matching, tailoring, and application workflows.
---

# Agent Evaluation

This project must not claim to be autonomous or accurate without measurable evidence. All critical flows should be evaluated with repeatable tests or benchmark fixtures.

## What to measure

- Resume extraction accuracy for structured fields.
- Job retrieval quality: precision@k, recall@k, duplicate rate.
- Matching quality: ranking quality, false positive / false negative rate.
- Tailoring quality: factual consistency, hallucination rate, job relevance.
- Browser automation quality: form completion success, navigation failures, verification rates.
- Application flow quality: successful vs failed applications, human intervention rate, verification confidence.

## Implementation rules

1. Prefer fixtures and local test jobs over live employer sites during early evaluation.
2. Store eval datasets under `tests/` or `docs/evaluations/` when applicable.
3. Evaluate measurable outcomes for each workflow step, not just the final output.
4. Make each automation step verifiable before claiming success.
5. Log failures and reasons explicitly.
6. Report the component-level scores, not a single opaque quality score.

## Core principle

Do not treat model output as truth without checking it against source documents, job descriptions, and candidate data. Evaluation must protect against fabricated candidate details, over-matching, and unsafe browser automation.
