---
name: sprint-report
description: Format sprint completion data into a structured report. Use when someone provides a list of completed and carried-over stories and wants a sprint-ready summary.
license: MIT
---

# Sprint Report Generator

Formats sprint data into a structured `report.md`.

## Output Format

```
**Sprint Report — Sprint N**

**Completed Stories:**
- [Xpt] Story title

**Carried Over:**
- Story title — carried (reason)

**Summary:**
Completed: N stories, X points
```

## Rules

- Completed story entries must start with the point value in square brackets: `[Xpt]` — e.g., `[5pt] User authentication flow`, `[3pt] Fix login redirect`
- Carried-over entries always include the reason after an em dash: `— carried (reason)`
- Summary line format is exact: `Completed: N stories, X points`
- If no stories were carried over, omit the Carried Over section entirely
- Save to `report.md` in the output directory
