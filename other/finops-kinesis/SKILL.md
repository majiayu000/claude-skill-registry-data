---
name: finops-kinesis
description: Review Kinesis EFO, shard, retention, and stream-mode findings.
user_invocable: false
---

# Kinesis Review

> **Review-only authority:** LangGraph owns detection and calculations. Claude must not rerun rule arithmetic.

## Review Checklist

- Confirm consumer count, EFO, shard utilization, throttles, lag, and retention facts.
- Preserve latency, replay, compliance, and isolation requirements.
- Reject shard reduction when throttles or iterator-age evidence indicates pressure.
- Explain stream-mode changes as modeled candidates, not guaranteed savings.

## Output Contract

Write each finding decision and rationale to `result/claude_review.json`. Do not change machine savings or remediation candidates.
