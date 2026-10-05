---
name: report
description: Generate a structured report on completed work, a feature area, or a topic. Saved to the reports directory. Invoked by saying "report", "generate report", or "summarize work".
---

# Generate Report

Generate a structured report saved as a permanent markdown file in `docs/reports/`.

**CRITICAL — Voice & Authorship:** Write in the **user's voice**. Never reference yourself (agent, Copilot, AI). Use "I" or neutral professional voice.

## Steps

### 1. Gather Context

- Scan conversation for changes made.
- Check recent task logs in `docs/task/logs/`.
- Read relevant documentation.
- Read observation logs in `docs/agent-observations/`.

### 2. Determine Report Type

| Type | When |
|------|------|
| `work-summary` | Summarizing completed work |
| `feature-report` | Deep dive on a feature |
| `audit` | Quality, security, performance |
| `architecture` | Decisions, patterns, tech debt |
| `incident` | Bug investigation, root cause |
| `status` | Sprint/project status |
| `custom` | Anything else |

### 3. Generate the Report File

**File path:** `docs/reports/{YYYY-MM-DD}-{slug}.md`

### 4. Report Structure

```markdown
# {Report Title}

> **Type:** {type}
> **Date:** YYYY-MM-DD
> **Scope:** {Brief scope}

---

## Summary
## Context
## Details

### Files Involved

| File | Role |
|---|---|

## Findings / Outcomes
## Recommendations / Next Steps
```

### 5. Capture Observations (MANDATORY)

Scan findings for unresolved items. Cross-post to `docs/agent-observations/` logs. If none: "Observations: none."

### 6. Save & Confirm

## Rules

- Always save to `docs/reports/`. Never inline-only.
- Be thorough but concise.
- Date-prefix filenames.
- Write in the user's voice.
- Cross-post observations to observation logs.
