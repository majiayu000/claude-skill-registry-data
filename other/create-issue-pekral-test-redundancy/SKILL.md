---
name: create-issue
description: Use when create a single issue from provided text without modifying its content
license: MIT
metadata:
  author: Petr Král (pekral.cz)
---

## Constraints
- Preserve original text exactly (no rewriting or summarizing)
- Improve formatting only (headings, lists, spacing)
- Assign issue to current user
- Use available CLI tools

---

## Execution

### 1. Prepare Content
- Use original text as-is
- Apply readable formatting (headings, lists)

### 2. Generate Title
- Use first line of input
- Remove formatting only

### 3. Create Issue
- Use available CLI tool
- Set title and formatted description
- Assign to current user
- Select and apply the single most relevant existing label per `@rules/compound-engineering/tracker.md` *Label tracker issues, and keep the labels true* (never create a new label; leave the issue unlabeled when none fits)

### 4. Output
- Return direct link to created issue

---

## Output Format

```markdown
# Task

<original text>

---

# Notes

Formatted automatically. Content unchanged.
```

## Output Humanization
- Use [blader/humanizer](https://github.com/blader/humanizer) for all skill outputs to keep the text natural and human-friendly.
