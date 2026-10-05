---
name: finops-tgw
description: Review Transit Gateway attachment, routing, and data-processing findings.
user_invocable: false
---

# Transit Gateway Review

> **Review-only authority:** LangGraph owns observable relationships and calculations. Claude reviews policy and ownership without rerunning arithmetic.

## Review Checklist

- Confirm attachments, route dependencies, traffic, accounts, regions, and cost facts.
- Preserve transitive routing, inspection, centralized egress, and multi-account requirements.
- Require caller-to-cost evidence before accepting peering or attachment changes.
- Mark missing cross-account route or ownership evidence as `needs_evidence`.

## Output Contract

Write each finding decision and rationale to `result/claude_review.json`. Do not change machine savings or remediation candidates.
