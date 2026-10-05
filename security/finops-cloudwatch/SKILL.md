---
name: finops-cloudwatch
description: Review CloudWatch Logs retention and deletion-candidate findings.
user_invocable: false
---

# CloudWatch Logs Review

> **Review-only authority:** LangGraph owns detection and calculations. Claude must not rerun rule arithmetic.

## Review Checklist

- Confirm environment, ingestion history, retention, and stored-bytes facts.
- Check audit, security, legal-hold, incident-response, and replay requirements.
- Reject deletion language when ownership or recent-event evidence is missing.
- Explain whether the candidate changes retention or only requests more evidence.

## Output Contract

Write each finding decision and rationale to `result/claude_review.json`. Do not change machine savings or remediation candidates.
