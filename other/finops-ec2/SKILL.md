---
name: finops-ec2
description: Review EC2 accelerator scheduling, utilization, and residual-cost findings.
user_invocable: false
---

# EC2 Accelerator Review

> **Review-only authority:** LangGraph owns detection and calculations. Claude must not rerun rule arithmetic.

## Review Checklist

- Confirm GPU or accelerator type, utilization, schedule, ASG, and workload-role facts.
- Check training checkpoints, jobs, notebooks, serving SLA, and interruption tolerance.
- Include residual EBS, Elastic IP, and data-transfer costs in the explanation.
- Treat instance-family changes as needing compatibility evidence.

## Output Contract

Write each finding decision and rationale to `result/claude_review.json`. Do not change machine savings or remediation candidates.
