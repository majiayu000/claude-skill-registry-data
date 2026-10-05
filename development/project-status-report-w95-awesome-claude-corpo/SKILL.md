---
name: project-status-report
description: "Generate project status reports with RAG status, milestones, risks, blockers, resource utilization, and executive summaries"
---

# Project Status Report Builder

## Overview

Create comprehensive project status reports that provide executives and stakeholders with accurate visibility into project health, progress, and risks. These reports combine RAG status indicators, milestone tracking, and actionable insights to enable informed decision-making.

## Key Report Sections

### 1. Executive Summary (1 page)
Concise overview for time-constrained stakeholders:
- **Overall Status**: RED / AMBER / GREEN with 2-3 sentence explanation
- **Key Wins This Period**: Top 2-3 accomplishments
- **Critical Issues**: Top 1-2 blockers requiring escalation
- **Next Period Focus**: What's next and key milestones
- **Budget Status**: On track / at risk with % utilization

### 2. RAG Status Framework

**RED** (Critical):
- Major milestones missed or at severe risk
- Budget overrun >15%
- Resource gaps impacting delivery
- Technical blockers with no clear solution
- Dependencies unresolved

**AMBER** (At Risk):
- Milestones at risk of missing (within 5 days)
- Budget at 80%+ utilization
- Moderate resource constraints
- Known risks with mitigation in progress
- Some dependency delays

**GREEN** (On Track):
- Milestones on schedule
- Budget under 80% utilization
- Resources allocated and productive
- Risks identified with controls
- Dependencies resolved or on track

### 3. Milestone Tracking
```
Milestone | Target Date | Status | % Complete | Owner | Notes
-----------|-------------|--------|-----------|-------|-------
Phase 1    | Jan 31      | GREEN  | 100%      | John  | Delivered on time
Phase 2    | Feb 28      | AMBER  | 45%       | Sarah | 5-day slip risk
Phase 3    | Mar 31      | GREEN  | 15%       | Mike  | On schedule
```

### 4. Resource Utilization
```
Resource | Allocated | Utilized | Capacity | Status | Notes
---------|-----------|----------|----------|--------|------
Dev Team | 8 FTE     | 7.2 FTE  | 90%      | GREEN  | 1 developer on vacation
QA       | 2 FTE     | 1.5 FTE  | 75%      | GREEN  | Peak testing phase coming
PM       | 1 FTE     | 1 FTE    | 100%     | AMBER  | Overallocated across projects
Design   | 1 FTE     | 0.3 FTE  | 30%      | RED    | Backlog review needed
```

### 5. Risk Register
```
Risk ID | Description | Probability | Impact | Status | Mitigation | Owner
--------|-------------|------------|--------|--------|-----------|-------
R-001   | Key vendor delayed | Med (50%) | High | ACTIVE | Backup vendor identified | Sarah
R-002   | Budget inflation | Low (20%) | Med | WATCH | Monthly reviews | Finance
R-003   | Scope creep | High (80%) | High | ACTIVE | Change control process | John
```

### 6. Blockers & Dependencies
**Current Blockers**:
1. [BLOCKER ID]: [Description] | Impact: [Days blocked] | Owner: [DRI] | Resolution ETA: [Date]
2. [BLOCKER ID]: [Description] | Impact: [Days blocked] | Owner: [DRI] | Resolution ETA: [Date]

**Dependencies**:
- Waiting on: [External team/vendor] | Needed by: [Date] | Owner: [Contact]
- Provides to: [Downstream team] | Delivery date: [Date] | Status: [On track/At risk]

### 7. Budget Summary
```
Category | Budget | Spent | Remaining | % Used | Forecast | Status
---------|--------|-------|-----------|--------|----------|--------
Personnel | $250K | $185K | $65K | 74% | $252K | AMBER
Contractors | $50K | $42K | $8K | 84% | $52K | AMBER
Tools | $30K | $18K | $12K | 60% | $30K | GREEN
Travel | $20K | $8K | $12K | 40% | $20K | GREEN
TOTAL | $350K | $253K | $97K | 72% | $354K | AMBER
```

## Template Structure

**PROJECT STATUS REPORT**
Project: [Name]
Period: [Date Range]
Report Date: [Date]
Project Manager: [Name]
Status: [RAG]

**EXECUTIVE SUMMARY**
[1 paragraph overview]

Overall Status: [RAG with explanation]
Budget: [Spent/$Total] [Status]
Schedule: [% Complete] [Status]
Scope: [Green/Amber/Red]

**HIGHLIGHTS**
- [Accomplishment 1]
- [Accomplishment 2]
- [Accomplishment 3]

**CRITICAL ISSUES**
1. [Issue]: [Impact] | [Mitigation] | [Owner]
2. [Issue]: [Impact] | [Mitigation] | [Owner]

**MILESTONES**
[Milestone table above]

**RESOURCE STATUS**
[Utilization table above]

**RISK SUMMARY**
[Risk register highlighting top 3-5 risks]

**BLOCKERS & DEPENDENCIES**
[List format above]

**BUDGET STATUS**
[Budget table above]

**NEXT PERIOD FOCUS**
- Milestone 1: [Description] | [Owner] | [Date]
- Milestone 2: [Description] | [Owner] | [Date]
- Milestone 3: [Description] | [Owner] | [Date]

## Best Practices

1. **Frequency**: Weekly for active projects, bi-weekly for stable projects
2. **Timeliness**: Consistent day/time; before executive meetings
3. **Accuracy**: Verify data with team leads before publishing
4. **Consistency**: Same format every report; trends visible quarter-to-quarter
5. **Actionability**: Every red/amber item has an owner and resolution path
6. **Brevity**: 2-3 pages max; appendices for detailed data
7. **Visual**: Use charts, graphs, and color coding for quick scanning
8. **Honest Reporting**: Flag issues early; don't hide problems
9. **Context**: Include previous period status to show trends
10. **Sign-off**: PM signature confirms accuracy

## Common Report Structures

**Weekly Flash Report** (1 page):
- Status badge
- Top 3 accomplishments
- Top 3 blockers
- Key metrics (% complete, budget, resource utilization)
- Next week focus

**Biweekly Status Report** (2-3 pages):
- Executive summary
- Milestone tracking
- Risk summary
- Budget status
- Resource utilization
- Next period focus

**Monthly Steering Committee Report** (3-5 pages):
- Executive summary with business impact
- Full milestone tracking
- Complete risk register
- Budget analysis with variance explanations
- Resource and dependency review
- Forward-looking analysis for 90 days
- Appendix: detailed metrics and artifacts

## Key Metrics to Track

- **Schedule Performance Index (SPI)**: Earned Value / Planned Value
- **Cost Performance Index (CPI)**: Earned Value / Actual Cost
- **Schedule Variance**: Earned Value - Planned Value
- **Cost Variance**: Earned Value - Actual Cost
- **Resource Utilization Rate**: Hours used / Hours allocated
- **Milestone Variance**: Days ahead/behind schedule
- **Risk Velocity**: Number of new risks emerging

## Red Flags & Escalation Triggers

Escalate immediately if any of:
- Overall status turns RED
- Budget variance exceeds 10%
- Schedule slip exceeds 5 days
- Critical resource departure
- Scope change >10% baseline
- Three or more blockers active
- Unresolved dependency blocking downstream work

## Communicating Status

**GREEN**: "We're on track. No escalations needed."
**AMBER**: "We're managing some risks. Here's our mitigation plan."
**RED**: "We need help. Here's the issue and what we need from leadership."

---

**Use this skill to**: Track project health, identify risks early, communicate status accurately, and enable informed decision-making by executives and stakeholders.
