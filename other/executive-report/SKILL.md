---
name: executive-report
description: Generate a comprehensive project intelligence report — the thing managers actually read.
compatibility: opencode
metadata:
  audience: delivery-leads
  purpose: reporting
---
## What I do

Generate a comprehensive project health report that aggregates pulse,
velocity, drift, coverage, and suggestions into a single document.
This is the "CTO dashboard" in document form — a report that gives
leadership visibility without them needing to learn CLI commands.

## When to use me

- When the user says "give me a report", "what's the state of things",
  "prepare an update for the team"
- At the end of a sprint for a retrospective summary
- When onboarding a new team member who needs the big picture

## How to generate the report

Run these commands and aggregate the output:

1. `hero sprint status --week` — sprint health (done, in-flight, at-risk, drift)
2. `hero sprint velocity --since 30d` — delivery velocity by agent/engineer
3. `hero drift --in-flight` — current spec-vs-code divergence
4. `hero suggest --top 5` — high-churn areas without specs
5. `hero search --list --status planning` — backlog size
6. `hero search --list --status delivering` — WIP count
7. `hero spec contract check` — regression status across delivered specs

## Report format

Write the report to `.hero/reports/report-<date>.md`:

```markdown
# Project Intelligence Report — <date>

## Health summary
- N specs completed this sprint, N in-flight, N at risk
- Delivery velocity: N specs/week (trend: up/down/flat)
- Drift: N specs with warnings, N boundary violations
- Contract coverage: N/M criteria verified, N regressions

## What shipped
<from pulse — done specs with titles>

## What's at risk
<from pulse — at-risk specs with staleness>
<from drift — specs with warnings>

## Where attention is needed
<from suggestions — high-churn uncovered areas>
<from contract check — any regressions>

## Backlog
N specs in planning, N in review
Top priorities: <list top 3 by priority>

## Velocity trend
<from velocity — per-agent metrics>
```

## What not to do

- Don't editorialize or add opinions — report facts from Hero data
- Don't include full spec content — link to slugs
- Don't require external data — everything comes from Hero commands
