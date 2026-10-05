---
name: finops-ebs
description: Review EBS snapshot retention, archive, and orphan-candidate findings.
user_invocable: false
---

# EBS Review

> **Review-only authority:** LangGraph owns detection and calculations. Claude must not rerun rule arithmetic.

## Review Checklist

- Confirm snapshot age, size, source volume, owner, and cost facts.
- Check AMI, launch template, AWS Backup, DLM, DR, audit, and legal-hold dependencies.
- Never convert an unverified orphan candidate into an automatic deletion instruction.
- Separate archive candidates from delete candidates.

## Output Contract

Write each finding decision and rationale to `result/claude_review.json`. Do not change machine savings or remediation candidates.
