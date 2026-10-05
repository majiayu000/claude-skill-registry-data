---
name: log-insight
description: "Log a technical insight to docs/insights-log.md immediately. Do not defer — sessions can clear. TRIGGER when the user says \"log this insight\", \"that's worth noting\", \"remember this\", \"note this gotcha\", \"TIL\", \"important discovery\", \"capture this learning\", or any request to record a technical observation."
argument-hint: <topic> <insight text>
---

# Log Technical Insight

Immediately add an entry to `docs/insights-log.md`.

## Current Context

- Branch: !`git branch --show-current`
- Milestone: detected from branch name

## What to Log

**Arguments**: $ARGUMENTS

Insights are non-obvious technical observations discovered during implementation:
- Platform quirks and gotchas
- Architectural trade-offs discovered during implementation
- Debugging techniques that saved significant time
- Performance observations
- Patterns worth remembering across sessions

## Entry Format

Add a new row to the insights log table:

| Date | Milestone | Topic | Insight | Verification | Status |
|------|-----------|-------|---------|--------------|--------|
| [today] | [from branch] | [hierarchical tag] | [the observation] | [how to verify] | Raw |

### Topic Tags (Hierarchical)

Use format like: `Platform/Area`, `Framework/Feature`, `Architecture/Pattern`, `Testing/Approach`

## After Logging

Check promotion rules:
- **3+ insights on same topic** → Suggest creating a Learning Note in `docs/learning-notes/`
- **Architectural decision with trade-offs** → Suggest creating an ADR in `docs/architecture/`
- **Recurring gotcha** → Suggest adding to CLAUDE.md

Report the promotion check result after logging.
