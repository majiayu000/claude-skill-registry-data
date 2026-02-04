---
name: telemetry
description: Parent skill that routes between telemetry-pr-insights (PR/CI) and telemetry-insights (interactive analysis).
---

# Telemetry Parent Skill

Routes to the appropriate telemetry sub-skill based on context.

## Sub-Skills

| Skill | When to Use |
|-------|-------------|
| `telemetry-pr-insights` | PR reviews, CI bots, automated reports |
| `telemetry-insights` | User questions about efficiency, usage, productivity |

## Routing Logic

```
If PR/CI context:
    → telemetry-pr-insights
Else if user asks about telemetry/usage/productivity:
    → telemetry-insights
Else:
    → don't run telemetry
```

## Examples

**PR bot**: Use `telemetry-pr-insights` with branch-scoped window.

**"How efficient am I?"**: Use `telemetry-insights` with current-session scope.

**"How efficient was I this week?"**: Use `telemetry-insights` with 7-day scope.

**Follow-up in PR**: Start with `telemetry-pr-insights`, switch to `telemetry-insights` for deeper analysis.
