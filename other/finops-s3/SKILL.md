---
name: finops-s3
description: Review S3 lifecycle, version, multipart, transition, and request findings.
user_invocable: false
---

# S3 Review

> **Review-only authority:** LangGraph owns detection and calculations. Claude must not rerun rule arithmetic.

## Review Checklist

- Confirm versioning, noncurrent bytes, multipart age, access pattern, and cost facts.
- Check Object Lock, legal hold, replication, compliance, and restore requirements.
- Keep storage savings and request-amplification savings from being double counted.
- Describe lifecycle changes as candidates until retention owners approve them.

## Output Contract

Write each finding decision and rationale to `result/claude_review.json`. Do not change machine savings or remediation candidates.
