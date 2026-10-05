---
name: finops-nat
description: Review NAT Gateway routing, endpoint, and cross-AZ cost findings.
user_invocable: false
---

# NAT Review

> **Review-only authority:** LangGraph owns detection and calculations. Claude must not rerun rule arithmetic.

## Review Checklist

- Confirm caller, destination, region, route table, bytes, and processing-cost facts.
- Validate endpoint service support, policy, private DNS, and route associations.
- Do not remove NAT while any required egress path remains unaccounted for.
- Require an observed caller-to-cost relationship before accepting remediation.

## Output Contract

Write each finding decision and rationale to `result/claude_review.json`. Do not change machine savings or remediation candidates.
