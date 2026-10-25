---
name: job-matching
description: Implements deterministic-first hybrid job matching with explicit explanations and configurable weights.
---

# Job Matching

Matching should be explainable and grounded in structured data. The system should not rely on embeddings or model guesses alone.

## Matching goals

Compute a job score from a combination of:

- semantic similarity
- skill overlap
- experience compatibility
- seniority compatibility
- location compatibility
- work mode compatibility
- salary compatibility
- candidate preferences
- domain relevance

## Rules

- Start with deterministic scoring from structured `CandidateProfile` and `JobListing` objects.
- Add LLM reasoning only where it improves explanation or handles ambiguity.
- Every score must explain why it was high or low.
- Keep weights configurable and measurable.
- Never claim a candidate has a skill or qualification unless it is supported by validated profile data.

## Output format

Each match should return a score and an explanation such as:

```text
Job Match: 87/100
Skills: 92% | Experience: 88% | Seniority: 95% | Semantic: 84%
Strong: Python, FastAPI, SQL, REST APIs
Missing: Kubernetes, AWS
```

## Repo principle

Deterministic logic should handle the bulk of matching. The LLM is an assistive layer for explainability and edge cases, not a source of fabricated experience or invented qualifications.
