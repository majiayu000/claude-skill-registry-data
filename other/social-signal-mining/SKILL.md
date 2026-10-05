---
name: social-signal-mining
description: Extract implementation lessons from Reddit/HN/X/blogs with anti-hype filtering, engagement thresholds, and evidence-linked Social Pattern records.
---

# Social Signal Mining

## Overview

Use this skill for Phase C social/blog extraction to complement repository evidence.
The output should capture practical lessons and failure modes, not popularity commentary.

## Source Rules

- Prioritize Reddit + Hacker News first.
- Use blogs/news only after topic-specific social discovery.
- Use X only via API-backed queries when available.

## Filtering Rules

- Require date bounds and relevance keywords.
- Require minimum engagement threshold per source.
- Drop opinion-only threads with no implementation details.

## Required Outputs

Write:
- `reports/research-ros/<date>-phase-c-social-signals.md`
- `reports/research-ros/<date>-social-pattern-records.jsonl`

Use `PatternRecord` schema for structured lessons.

## Exit Criteria

- Minimum 20 non-repo artifacts reviewed.
- At least 5 actionable implementation lessons with concrete source links.
