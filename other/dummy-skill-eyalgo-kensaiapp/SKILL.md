---
name: standup-formatter
description: Format work updates into a structured daily standup summary. Use when someone provides tasks completed and blockers and wants a standup-ready summary.
license: MIT
---

# Standup Formatter

Takes work updates and formats them into a structured `standup.md`.

## Output Format

```markdown
**Done:**
- [past-tense action verb] [what was completed]

**Next:**
- [what is planned next]

**Blocked:**
- [blocker] OR N/A
```

## Rules

- **Done** items must start with a past-tense action verb (e.g., "Fixed", "Completed", "Shipped", "Reviewed")
- **Blocked** section is always present — use `N/A` if no blockers were mentioned
- Each bullet is one line only
- Save to `standup.md` in the output directory specified in the task prompt
