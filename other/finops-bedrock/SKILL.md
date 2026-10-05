---
name: finops-bedrock
description: Review Bedrock commitment, token, prompt-cache, and semantic-cache findings.
user_invocable: false
---

# Bedrock Review

> **Review-only authority:** LangGraph owns detection and calculations. Claude must not rerun rule arithmetic.

## Review Checklist

- Confirm model, region, token usage, cache support, and pricing evidence are cited.
- Review prompt stability, freshness, tenant isolation, PII, and invalidation risks.
- Treat semantic-cache suitability as an operational review, not a guaranteed saving.
- Use MCP only when pricing or documentation is marked `evidence_only` or `unavailable`.

## Output Contract

Write each finding decision and rationale to `result/claude_review.json`. Do not change machine savings or remediation candidates.
