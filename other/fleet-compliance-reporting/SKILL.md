---
name: fleet-compliance-reporting
description: How accountability produces structured compliance reports for PO — the output format that makes governance data actionable. Sprint reports, module reports, trend analysis.
---

# Compliance Reporting — Accountability's Output Skill

You verify. You detect patterns. But verification and detection are useless without REPORTS. The PO needs structured, actionable compliance data to make governance decisions. This skill defines what those reports look like.

## Report Types

### 1. Sprint Compliance Report (Weekly)

Produced by your **sprint-compliance-report** CRON (Friday 5pm) or on-demand via `acct_sprint_compliance(sprint_id)`.

```
## Sprint Compliance Report: {sprint_id}
Generated: {date}
Period: {start} — {end}

### Summary
- Tasks completed: {N}
- Compliant: {X}/{N} ({pct}%)
- With gaps: {Y}
- Trend: {improving/stable/declining} vs last sprint

### Compliance by Dimension
| Dimension | Score | Details |
|-----------|-------|---------|
| Stage traversal | {pct}% | {X}/{N} tasks followed stage progression |
| Contributions | {pct}% | {X}/{N} stories had required contributions |
| PO gates | {pct}% | {X}/{N} tasks with gate at 90% had PO approval |
| Trail completeness | {pct}% | {X}/{N} tasks have complete trail |
| Quality standards | {pct}% | {X}/{N} tasks met commit/PR/artifact standards |

### Per-Task Detail (gaps only)
| Task | Agent | Gap | Score |
|------|-------|-----|-------|
| {title} | {agent} | {specific gap} | {pct}% |

### Patterns Detected
- {pattern description with frequency and affected agents}

### Recommendations
1. {specific action} — addresses {pattern}
2. {specific action} — addresses {gap trend}
```

### 2. Agent Compliance Summary (On Request)

When PO asks about a specific agent's process adherence:

```
## Agent Compliance: {agent_name}
Period: last {N} tasks

### Overall: {pct}%
- Tasks completed: {N}
- Fully compliant: {X}
- With gaps: {Y}

### Common gaps for this agent:
- {gap type}: {count} occurrences
- {gap type}: {count} occurrences

### Trend: {improving/stable/declining}
### Teaching interventions: {count} (from immune system)
```

### 3. Trend Report (Monthly/On Request)

Cross-sprint compliance trends:

```
## Compliance Trend Report
Period: {sprints covered}

### Overall Trend
| Sprint | Compliance | Trend |
|--------|-----------|-------|
| sprint-1 | 65% | — |
| sprint-2 | 72% | +7% |
| sprint-3 | 78% | +6% |
| sprint-4 | 75% | -3% |

### Dimension Trends
[chart data showing each dimension over time]

### Systemic Improvements
- Trail completeness: 55% → 78% (teaching interventions effective)
- Contribution compliance: 60% → 82% (PM contribution checks working)

### Persistent Gaps
- QA predefinition still at 65% (below 80% target)
- Recommendation: schedule QA contribution backlog CRON more frequently
```

## Report Quality Standards

1. **Always include numbers** — "compliance is low" is useless. "Compliance: 62%, down from 75% last sprint" is actionable.
2. **Always include trend** — single-point data means nothing. Compare to last sprint or last N tasks.
3. **Always include recommendations** — data without action is noise. Each pattern or trend should have a suggested response.
4. **Never blame agents** — report facts. "Agent X has 3 tasks without trail" not "Agent X is lazy." The immune system handles behavioral correction.
5. **Post to board memory** — tags: `[compliance, report, sprint:{id}]`. PO sees in directive context.

## The Reporting Pipeline

```
Trail events (board memory)
    ↓
acct_trail_reconstruction (per task)
    ↓
acct_sprint_compliance (aggregate)
    ↓
Compliance report (structured artifact)
    ↓
acct_pattern_detection (cross-task analysis)
    ↓
Pattern report → immune system signals
    ↓
Trend analysis (cross-sprint)
    ↓
PO governance decisions
```

Each step builds on the previous. Trail events are raw data. Reconstruction organizes per-task. Sprint compliance aggregates. Patterns find systemic issues. Trends track improvement or decline. Reports communicate it all to the PO.

## Artifact vs Board Memory

- **Quick findings:** Board memory with compliance tags. PO sees in heartbeat context.
- **Full reports:** `fleet_artifact_create("compliance_report", title)` with progressive updates. Plane HTML rendered. Completeness tracked.

Use board memory for real-time signals. Use artifacts for structured reports that need review.
