---
name: finops-dynamodb
description: Review DynamoDB capacity, autoscaling, throttling, and commitment findings.
user_invocable: false
---

# DynamoDB Review

> **Review-only authority:** LangGraph owns detection and calculations. Claude must not rerun rule arithmetic.

## Review Checklist

- Confirm consumed capacity, p95, throttles, billing mode, and GSI facts.
- Keep table and index recommendations separate.
- Reject downsizing when throttling, backlog, latency, or unknown peak evidence exists.
- Avoid double counting workload savings and organization commitment savings.

## Output Contract

Write each finding decision and rationale to `result/claude_review.json`. Do not change machine savings or remediation candidates.
