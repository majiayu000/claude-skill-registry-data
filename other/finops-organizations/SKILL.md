---
name: finops-organizations
description: Review consolidated billing, RI and Savings Plans sharing, and allocation findings.
user_invocable: false
---

# Organizations Review

> **Review-only authority:** LangGraph owns observable relationships and calculations. Claude reviews policy and ownership without rerunning arithmetic.

## Review Checklist

- Confirm account membership, eligible usage, commitment utilization, and sharing facts.
- Review account ownership, chargeback, legal entity, and organization policy constraints.
- Mark unavailable cross-account data as an evidence gap.
- Prevent organization savings from being added again to workload-level savings.

## Output Contract

Write each finding decision and rationale to `result/claude_review.json`. Do not change machine savings or remediation candidates.
