---
name: status-reporting
description: >
  Use when reporting progress, status updates, or completion of work to managers,
  stakeholders, or dependent agents. This skill defines a standard format for clear,
  consistent, and actionable status updates.
---

# Status Reporting

## Overview
This skill defines how to communicate progress and status clearly and consistently. Good status reporting enables coordination, prevents surprises, and helps stakeholders plan their work based on yours.

## When to Use
- When providing regular progress updates (heartbeat, daily, weekly)
- When a task or project stage is completed
- When stakeholders request a status update
- When blockers or delays affect dependent work
- Before handoffs to the next agent in a workflow
- **Don't use when:** Status is unchanged since last report, or no one needs to know

## Core Procedures

### Step 1: Determine Report Audience and Frequency
| Audience | Frequency | Detail Level |
|----------|-----------|-------------|
| Manager/CEO | Daily or milestone summary | Concise, key metrics |
| Dependent Agent | On completion or delay | Technical details needed for next step |
| Stakeholders | Weekly or milestone | Executive summary, impact |
| Team Members | As needed | Full technical detail |
| Quality/Compliance | Per schedule | Evidence, metrics, compliance status |

### Step 2: Build Status Report
```
STATUS REPORT
=============
Agent: [name, company, role]
Date: [report date/time]
Task: [what task or project this covers]
Period: [what time range this report covers]

STATUS: [ON TRACK / AT RISK / BLOCKED / COMPLETED]

PROGRESS:
- What was completed this period:
  - [specific item 1]
  - [specific item 2]
- What is in progress:
  - [specific item 3] - % complete
  - [specific item 4] - % complete

BLOCKERS:
- [blocker description, when it started, what is being done]
- NONE

NEXT PERIOD:
- [what will be worked on next]
- [expected completions]

METRICS:
- [relevant key metrics: completion %, quality score, time on task]

RISKS:
- [any risks that could derail plan, current status]
```

### Step 3: Validate Report
Before sending:
- [ ] Status accurately reflects reality (no sugar-coating or unnecessary alarm)
- [ ] Completed items are actually done (passed output-validation-checklist)
- [ ] Blockers are specific with active resolution efforts
- [ ] Next period goals are realistic
- [ ] Metrics are current and accurate

### Step 4: Send and Follow Up
- Send report through appropriate channel (messaging, dashboard, handoff)
- If BLOCKED or AT RISK, also trigger escalation-management
- Acknowledge any questions or feedback on the report
- Update next report based on whether this period's plan was achieved

## Quality Checklist
- [ ] Status honestly reflects situation (accurate, not optimistic/pessimistic)
- [ ] All completed items pass quality validation
- [ ] Blockers have clear description and active resolution
- [ ] Next period goals specific and achievable
- [ ] Metrics and dates current
- [ ] Sent to all who need this information

## Error Handling
- **Error:** Report reveals you're significantly behind schedule
  **Response:** Include this honestly, propose revised timeline, escalate if impact is critical
- **Error:** Dependent agent reports they can't use your output
  **Response:** Understand the gap, fix if possible, update status to reflect rework needed
- **Error:** Status changed to BLOCKED since last report
  **Response:** Trigger escalation immediately, update all affected stakeholders

## Cross-Team Integration
**Related Skills:** handoff-protocol, escalation-management, risk-assessment, output-validation-checklist
**Used By:** ALL agents for regular updates; especially CEOs, monitors, reporters, project managers