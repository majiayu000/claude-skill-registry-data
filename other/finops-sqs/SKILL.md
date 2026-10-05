---
name: finops-sqs
description: Review SQS long-polling, batching, visibility, and backlog findings.
user_invocable: false
---

# SQS Review

> **Review-only authority:** LangGraph owns detection and calculations. Claude must not rerun rule arithmetic.

## Review Checklist

- Confirm wait time, empty receives, request volume, message age, DLQ, and cost facts.
- Check client read timeout, worker shutdown, latency SLA, and visibility behavior.
- Reject polling changes when client timeout compatibility is unknown.
- Keep reliability findings separate from request-cost findings.

## Output Contract

Write each finding decision and rationale to `result/claude_review.json`. Do not change machine savings or remediation candidates.
