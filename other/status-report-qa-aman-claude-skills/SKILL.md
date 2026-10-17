---
name: status-report
description: >
  Write a structured client status report for a consulting engagement. Use when a
  consultant says "write my weekly status update", "I need to send a status report",
  "draft the client update", "what should be in the weekly report", "client wants a
  progress update", "help me write the RAG status", "I need to report on blockers",
  "end of week update to the client", or "help me communicate what's stuck". Also
  trigger when someone needs to communicate engagement progress, surface blockers to
  the client, or flag decisions that need to be made by the sponsor.
---

## Overview

A consulting status report has one primary job: give the client the information they need to make decisions and take action, without making them read everything. The audience is a busy executive or sponsor. They want to know: are we on track, what got done, what is stuck, and what do they need to decide. The structure must be immediately scannable - RAG status visible in 5 seconds, blockers visible in 10, detail available for those who want it.

The fatal mistake: reports that describe activity without surfacing risk. A Green status with no blockers on a troubled engagement is worse than an Amber status with a clear ask.

## Workflow

### Step 1: Determine the Audience Tier

Different audiences need different depth. Before drafting, identify who reads this report:

**Executive sponsor (C-suite or VP)**: Wants RAG, top 2 accomplishments, top 2 risks, 1 decision needed. Max 1 page.

**Project owner / day-to-day client lead**: Wants all of the above plus detail on blockers, workstream status, upcoming deliverables. Max 2 pages.

**Steering committee / program office**: Wants metrics, milestone status, dependency flags, financial summary. Structured table format.

Write once, format for the tier. If multiple audiences receive the same report, structure the top half for executives and put detail below.

### Step 2: Set the RAG Status

RAG (Red / Amber / Green) is the most important element. Set it honestly.

```
Green:  On track. No material risks to scope, timeline, or budget.
        No decisions needed from the client.

Amber:  At risk. One or more risks that could affect delivery if not addressed.
        A specific action is needed within [X days] to prevent escalation.

Red:    Off track. Scope, timeline, or budget has been materially impacted.
        Escalation and immediate client decision required.
```

Rules:
- Amber requires a specific ask - "this is Amber because X, and to return to Green by [date] we need [action from client]"
- Red requires an executive notification, not just a report
- Never set Green on an engagement where the consultant has an unresolved ask that is delaying work
- If you set Amber or Red, the call to action must appear in the report - not just the risk

### Step 3: Accomplishments This Period

List 3-5 specific accomplishments from the reporting period (week or two weeks). These should be outcome-oriented, not activity-oriented.

Template:
```
Accomplishments (Week of [date]):
- Completed interviews with 8 of 10 target stakeholders; key finding: [specific insight]
- Delivered Phase 1 report to [your client] project team; review session scheduled [date]
- Resolved [specific blocker] by [action taken]; workstream now unblocked
- [Milestone]: [brief description of what was completed and why it matters]
```

Each bullet should be one sentence. "Made progress on X" is different from "Completed X." Both are valid, but the distinction matters.

### Step 4: Blockers and Risks

This is the most important section for client action. Structure each blocker/risk clearly.

Template per item:
```
[Blocker/Risk name]: [One sentence describing the issue]
Impact: [What happens if not resolved - specific effect on timeline, deliverable, or outcome]
Owner: [Consultant or client - who needs to act]
Ask: [Specific action needed, by whom, by when]
Status: [New / In progress / Escalated]
```

Example:
```
Data access - Finance system: [Your client] finance team has not yet provisioned read
access to the revenue database requested 12 days ago.
Impact: Phase 2 revenue analysis cannot begin until access is granted. Delays Phase 2
completion by minimum 5 business days.
Owner: [Your client] IT (ticket #1234) + Finance Director approval required.
Ask: Finance Director approval by [date] to unblock IT provisioning.
Status: Escalated to project lead on [date].
```

Never list a blocker without an ask. "We are unable to access X" is a complaint. "We need Y from Z by date to unblock X" is actionable.

### Step 5: Decisions Needed

Separate from blockers - decisions are judgment calls the client must make that affect the engagement direction.

Template:
```
Decision needed: [Topic]
Background: [1-2 sentences - why is this decision needed now]
Options: A) [brief option]  B) [brief option]
Consultant recommendation: [Option X, with one-sentence rationale]
Deadline: [When the decision is needed to avoid timeline impact]
```

Include only decisions where the delay has a measurable consequence. Do not surface every minor preference as a "decision needed."

### Step 6: Next Period Plan

List 3-5 planned activities for the coming period with owner and target date.

Template:
```
Planned (Week of [date]):
- Complete remaining 2 stakeholder interviews [Owner: Consultant] [Due: date]
- Deliver Phase 2 draft findings to project team [Owner: Consultant] [Due: date]
- [Client action] - pending Finance Director approval [Owner: [your client]] [Due: date]
```

### Full Report Template

```
ENGAGEMENT STATUS REPORT
[Engagement name] | [Reporting period] | Prepared by: [Consultant]

OVERALL STATUS: [GREEN / AMBER / RED]
[If Amber or Red: one sentence explaining why and the specific ask to restore Green]

---------------------------------------------------------------------
ACCOMPLISHMENTS
- [bullet 1]
- [bullet 2]
- [bullet 3]

---------------------------------------------------------------------
BLOCKERS / RISKS
[Blocker 1 - use template from Step 4]
[Blocker 2 - if applicable]

DECISIONS NEEDED
[Decision 1 - use template from Step 5, if applicable]

---------------------------------------------------------------------
UPCOMING
- [bullet 1 with owner and date]
- [bullet 2 with owner and date]
- [bullet 3 with owner and date]

---------------------------------------------------------------------
METRICS (if tracked)
| Metric             | Target | Actual | Status |
|--------------------|--------|--------|--------|
| [Milestone X]      | [date] | [date] | Green  |
| [Budget used]      | [%]    | [%]    | Amber  |
| [Interviews done]  | 10     | 8      | Green  |
```

## Anti-Patterns

**1. Green-washing status**
Bad: Setting Green because everything is "fine" while the consultant is waiting on 3 unresolved client actions.
Good: Set Amber the moment any external dependency is blocking progress, and include the specific ask.
Green-washing builds false confidence and removes the basis for escalating when things deteriorate.

**2. Activity reporting without outcomes**
Bad: "Conducted 3 workshops, held 6 meetings, reviewed documents."
Good: "Completed diagnostic for Phase 1; identified 4 root causes of margin erosion."
Activity reports tell the client what you did. Outcome reports tell them what got accomplished.

**3. Blockers without asks**
Bad: "Data access has not been granted."
Good: "Data access requires Finance Director approval by [date]. Without it, Phase 2 analysis delays by 5 days. Ask: [Name], can you approve by [date]?"
A blocker without an ask is noise. An ask tells the client what to do next.

**4. Too long for the audience**
Bad: A 3-page status report sent to a C-suite sponsor.
Good: Top half of the first page covers RAG, accomplishments, and decisions needed. Detail is available below.
Senior stakeholders do not read status reports - they scan them.

**5. Irregular reporting cadence**
Bad: Sending status reports only when there is bad news.
Good: Weekly or biweekly cadence regardless of status. Consistent reporting builds the channel for bad news when it arrives.
Irregular reporting signals to the client that the consultant is managing them, not partnering with them.

## Quality Checklist

- [ ] Audience tier identified - report length and depth matched to tier
- [ ] RAG status set honestly - Amber/Red includes a specific client ask
- [ ] Accomplishments are outcome-based, not activity lists
- [ ] Every blocker has an owner, impact statement, and specific ask with deadline
- [ ] Decisions needed are true decisions - each has a deadline and recommendation
- [ ] Upcoming items have owners and dates
- [ ] Report is scannable - key information visible without reading full text
- [ ] No jargon or methodology descriptions
- [ ] Sent on agreed cadence, not only when there is something to report
