---
name: finops-anomaly
description: Review CloudSweep cost-spike, service-attribution, and CloudTrail correlation findings.
user_invocable: false
---

# Cost Anomaly Review

> **Review-only authority:** LangGraph owns spike detection, service attribution, and confidence facts. Claude must not recalculate the machine result.

## Review Checklist

- Cite spike, service-attribution, and event-correlation `fact_id` values.
- Keep spike confidence, service confidence, and triggering-event confidence separate.
- When CloudTrail evidence is absent, do not state a triggering action as fact.
- Label plausible but unobserved causes as hypotheses and exclude them from savings.

## Output Contract

Write review decisions to `result/claude_review.json`. Use only `accepted`, `rejected`, or `needs_evidence`; add rationale and documentation links without changing machine values.
