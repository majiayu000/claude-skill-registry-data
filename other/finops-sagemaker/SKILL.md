---
name: finops-sagemaker
description: Review SageMaker endpoint scaling, accelerator utilization, and hosting-mode findings.
user_invocable: false
---

# SageMaker Review

> **Review-only authority:** LangGraph owns detection and calculations. Claude must not rerun rule arithmetic.

## Review Checklist

- Confirm variant count, accelerator utilization, latency, errors, traffic, and cost facts.
- Check cold starts, model load time, availability, and latency SLA.
- Verify endpoint, serverless, asynchronous, or batch compatibility before accepting a mode change.
- Preserve valid autoscaling bounds and production redundancy.

## Output Contract

Write each finding decision and rationale to `result/claude_review.json`. Do not change machine savings or remediation candidates.
