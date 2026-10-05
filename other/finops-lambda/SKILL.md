---
name: finops-lambda
description: Review Lambda memory, timeout, concurrency, architecture, and request-amplification findings.
user_invocable: false
---

# Lambda Review

> **Review-only authority:** LangGraph owns detection and calculations. Claude must not rerun rule arithmetic.

## Review Checklist

- Confirm memory, duration p99, errors, throttles, retries, concurrency, and cost facts.
- Check cold starts, event backlog, burst traffic, and downstream limits.
- Require dependency compatibility before accepting architecture changes.
- Cite dependency facts when discussing requests per invocation or cache behavior.

## Output Contract

Write each finding decision and rationale to `result/claude_review.json`. Do not change machine savings or remediation candidates.
