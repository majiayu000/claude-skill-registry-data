---
name: finops-cloudwatch-alarm
description: Review CloudWatch alarm resolution and monitoring-cost findings.
user_invocable: false
---

# CloudWatch Alarm Review

> **Review-only authority:** LangGraph owns detection and calculations. Claude must not rerun rule arithmetic.

## Review Checklist

- Confirm metric resolution, evaluation window, alarm purpose, and SLA evidence.
- Preserve sub-minute detection when an operational requirement is documented.
- Check dashboards, composite alarms, and incident automation dependencies.
- Describe changes as candidates until alert behavior is validated.

## Output Contract

Write each finding decision and rationale to `result/claude_review.json`. Do not change machine savings or remediation candidates.
