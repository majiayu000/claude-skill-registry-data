---
name: review-feedback
description: "Developer tool that analyses feedback entries and generates an improvement backlog. Use when the developer says 'review feedback', 'backlog', 'what needs fixing', or wants to process accumulated feedback into actionable improvements."
---

# Review Feedback (Developer Tool)

## Instructions
1. Read `feedback/log.jsonl`, weekly reviews, developer summaries.
2. For high-severity items: reconstruct via commit hash, identify root cause (template/extract/rules/skill/schema).
3. Generate/update `feedback/backlog.md`: problem → root cause → fix → file to change → priority → effort.
