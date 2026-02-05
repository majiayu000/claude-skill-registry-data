---
name: skillstash-review
description: Review skillstash PRs and summarize validation issues
---

# Skillstash Review

Use this skill to review a skill PR and report validation issues.

## When this skill activates

- A PR updates `skills/**`
- A review or validation is requested

## What this skill does

1. Run validation checks (structure, frontmatter, naming, size).
2. Report blocking issues with file/line context.
3. Suggest improvements for non-blocking issues.
