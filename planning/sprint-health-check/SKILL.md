---
name: sprint-health-check
description: Assess the health of a sprint mid-cycle using objective signals and leading indicators. Identify scope creep, blocked work, velocity anomalies, and team morale issues before they derail the sprint. Produce a clear status and recommended interventions.
triggers:
  - "sprint health"
  - "how is the sprint going"
  - "sprint check-in"
  - "mid sprint review"
  - "sprint at risk"
  - "scope creep"
  - "sprint is off track"
audience:
  - manager
  - engineer
---

# Sprint Health Check

Assess sprint status mid-cycle and intervene early before problems compound.

---

## When to Run

- **Standard**: Mid-sprint (day 4-5 of a 10-day sprint)
- **On-demand**: When you sense something is wrong
- **Signals that trigger an emergency check**: Blockers open > 2 days, scope added after day 2, 3+ tickets not started by mid-sprint

---

## The Five Health Signals

### 1. Scope Integrity
*Did we add or change work after sprint planning?*

| Status | Condition |
|---|---|
| 🟢 Healthy | 0-1 items added; scope stable |
| 🟡 Watch | 2-3 items added; team aware |
| 🔴 At Risk | 4+ items added; or any item added without removing something |

**Questions to ask:**
- What was added, and why?
- Did the team agree to the addition, or was it assigned top-down?
- Was anything removed to compensate?

---

### 2. Progress Rate
*Are we on track to complete committed work?*

**Simple burn-down check** (by mid-sprint, you should have completed ~50% of story points or tickets):

```
Committed points: [X]
Completed by mid-sprint: [Y]
Expected by now: [X * 0.5]

Status:
  Y >= X * 0.5: 🟢 On track
  Y >= X * 0.35: 🟡 Behind, watch
  Y < X * 0.35: 🔴 At risk — intervene
```

**Note**: Don't treat story points as precise. Use as a signal, not a measurement.

---

### 3. Blocked Work
*Is work stuck waiting on something?*

| Status | Condition |
|---|---|
| 🟢 Healthy | 0 blockers, or blockers resolved same day |
| 🟡 Watch | 1-2 items blocked < 2 days; owner identified |
| 🔴 At Risk | Any item blocked > 2 days, OR blocker has no owner |

**Questions to ask:**
- What is blocked and why?
- Who owns unblocking it?
- Is this a dependency problem we need to escalate?

---

### 4. Work in Progress (WIP)
*Are people focused, or is everything partially done?*

Too much WIP = context switching = nothing gets done.

**Healthy WIP ceiling**: Each engineer should have at most 2 items In Progress simultaneously.

| Status | Condition |
|---|---|
| 🟢 Healthy | Most engineers at 1-2 items in progress |
| 🟡 Watch | 1-2 engineers at 3 items; discussing in standup |
| 🔴 At Risk | Multiple engineers at 4+ items; tickets aging in "In Progress" |

---

### 5. Team Morale Signal
*How is the team feeling?*

Quantitative morale check (1-5 scale, anonymous):
- **Energy**: How energized do you feel about the work this sprint?
- **Clarity**: How clear is the goal and what "done" looks like?
- **Confidence**: How confident are you we'll complete the sprint?

Thresholds:
| Avg Score | Status |
|---|---|
| 4.0+ | 🟢 Strong |
| 3.0–3.9 | 🟡 Worth discussing |
| < 3.0 | 🔴 Needs immediate attention |

---

## Sprint Health Report Template

```markdown
## Sprint Health Check: [Sprint Name/Number]
**Date**: [mid-sprint date]  
**Team**: [name]  
**Reported by**: [EM/TL name]

### Overall Status: 🟢 / 🟡 / 🔴

| Signal | Status | Notes |
|---|---|---|
| Scope Integrity | 🟢/🟡/🔴 | [items added: X, removed: Y] |
| Progress Rate | 🟢/🟡/🔴 | [X/Y points done at midpoint] |
| Blocked Work | 🟢/🟡/🔴 | [# blocked, longest-blocked item] |
| WIP Level | 🟢/🟡/🔴 | [avg WIP per engineer] |
| Team Morale | 🟢/🟡/🔴 | [avg score if surveyed] |

### What's at Risk
[Specific items or work streams that may not complete]

### Interventions

| Action | Owner | By When |
|---|---|---|
| [descope / unblock / pair on / re-plan] | [name] | [date] |

### Decisions Made
[Any scope cuts, priority changes, or re-assignments agreed in this check]

### Outlook
[ ] Sprint will complete as committed  
[ ] Sprint will complete with agreed scope reduction  
[ ] Sprint is off track — escalating to stakeholders
```

---

## Intervention Playbook

### If scope was added
1. Make it visible: add to board, count the scope change
2. Ask: what comes out? (LIFO — last item added is first to descope)
3. If stakeholder-driven: loop in PM; protect team from silent scope growth

### If progress is behind
1. Identify the largest in-flight item — is it actually too big?
2. Split it: can we deliver partial value and carry the rest?
3. Check for hidden work: undocumented tasks, context switching, technical debt payments

### If work is blocked
1. Name a blocker owner by end of standup
2. If blocked on external team: manager escalates immediately, not "let's see"
3. If blocked on technical unknowns: timebox the investigation (1 day max before re-planning)

### If WIP is high
1. Stop starting, start finishing — team pull policy
2. Ask each engineer: "what would it take to close one of these today?"
3. Consider pairing to unblock the stalled item

### If morale is low
1. Don't ignore it — low morale predicts low output within 1-2 sprints
2. 1:1s within 24h with each team member
3. Ask: is the work unclear? Is the work meaningful? Is the pace sustainable?
4. Consider: sprint scope cut to reduce pressure, or retrospective pulled forward

---

## References
- Henrik Kniberg: [Scrum and XP from the Trenches](https://www.infoq.com/minibooks/scrum-xp-from-the-trenches-2/)
- LeadDev: [Sprint anti-patterns](https://leaddev.com/agile-other-ways-working)
- Daniel Vacanti: *Actionable Agile Metrics* (WIP and flow)

## MCP Integration

**Query in-progress items and their age:**
```
jira_search_issues(jql: "project = PROJ AND sprint in openSprints() AND status in ('In Progress', 'In Review') ORDER BY updated ASC")
```

**Count total sprint scope and completed items:**
```
jira_search_issues(jql: "project = PROJ AND sprint in openSprints()")
jira_search_issues(jql: "project = PROJ AND sprint in openSprints() AND status = Done")
```

**Identify blocked items:**
```
jira_search_issues(jql: "project = PROJ AND sprint in openSprints() AND labels = 'blocked'")
```

**Pull sprint details (dates, goal):**
```
jira_get_issue(issue_key: "PROJ-sprint-board")  -- or query via sprint boards if available
```

**Graceful fallback:** Ask the team to paste the sprint board snapshot (stories, statuses, remaining days) as plain text. Apply the same Sprint Health Score analysis to the text input.
