---
name: incident-retrospective
description: Run a structured blameless post-mortem after an incident
triggers: [postmortem, post-mortem, incident review, blameless, outage review, RCA, root cause, incident post-mortem]
audience: manager
---

# Incident Retrospective (Blameless Post-Mortem)

## Context
A blameless post-mortem examines what happened during an incident, how systems and processes contributed, and what can be improved — without assigning blame to individuals. Psychological safety is a prerequisite for honest, useful retrospectives. Without it, people hide information to protect themselves, which prevents learning.

Use this skill when:
- An incident has occurred (outage, data loss, security event, missed SLA)
- You want to improve from a near-miss
- You're facilitating a retrospective and need a structured format

## Instructions

### Before the Retrospective
1. **Assign a facilitator** who was not the on-call engineer. Keeps discussion objective.
2. **Set the ground rules** at the start: *"We operate under the assumption that everyone did their best with the information available. We are here to improve our systems, not to judge our colleagues."*
3. **Gather the data first.** Pull logs, alerts, deployment history, communication threads before the meeting. Build the timeline from facts, not memory.
4. **Timeframe:** Hold within 48–72 hours of resolution while context is fresh.

### Post-Mortem Template

```markdown
# Incident Post-Mortem — [Title]

**Date:** YYYY-MM-DD  
**Severity:** P1 / P2 / P3  
**Duration:** X hours Y minutes  
**Impact:** [Users affected, revenue impact, SLA breach, data affected]  
**Facilitator:** [Name]  
**Participants:** [Names / roles]

## Summary
One paragraph: what happened, what the impact was, and how it was resolved.

## Timeline (UTC)
| Time | Event |
|------|-------|
| HH:MM | First alert fired |
| HH:MM | On-call acknowledged |
| HH:MM | [Key investigation step] |
| HH:MM | Root cause identified |
| HH:MM | Mitigation applied |
| HH:MM | Service restored |
| HH:MM | Post-incident monitoring confirmed stable |

## Root Cause
Describe the technical root cause. Be specific. Avoid "human error" as a root cause — always ask why the system allowed the error to have this impact.

## Contributing Factors
List systemic issues that allowed the incident to happen or made it worse:
- Missing alert on X
- Lack of runbook for Y scenario
- Insufficient test coverage for Z edge case
- Deployment process didn't catch W

## Impact
- Users affected: [number / %]
- Duration of degradation: X min
- SLA impact: [breach / near-miss]
- Data loss: [yes/no/scope]

## What Went Well
- [The on-call escalation path worked]
- [Rollback procedure executed cleanly]

## Action Items
| Action | Owner | Due | Priority |
|--------|-------|-----|----------|
| Add alert for X | @engineer | Date | High |
| Write runbook for Y | @engineer | Date | Medium |
| Fix root cause in Z | @team | Date | High |

## Follow-Up
Link to tickets created for each action item.
```

### Facilitation Tips
- Ask **"why?"** at least five times to get past symptoms to root cause (5 Whys technique)
- When someone starts to say "X should have done Y", redirect: *"What would have needed to be true about the system for X to have done Y automatically?"*
- Review action items for completion in the next team meeting — retrospectives without follow-through erode trust

## Principles
- Source: [LeadDev — Blameless Culture](https://leaddev.com)
- Source: [Google SRE Book — Postmortem Culture](https://sre.google/sre-book/postmortem-culture/)
- Key idea: *"The goal is not to find who made the mistake. The goal is to find what made the mistake possible and what would prevent it from being possible in the future."*

## Output Format
When applying this skill, the agent should:
- Generate the filled-in post-mortem document from provided incident details
- Reconstruct the timeline from logs/alerts if available
- Surface contributing factors beyond the immediate root cause
- Generate specific, actionable action items with suggested owners and priority

## MCP Integration

**Read the incident ticket from Jira for timeline and impact data:**
```
jira_get_issue(issue_key: "INC-456")
```

**Search for related incidents to identify repeat patterns:**
```
jira_search_issues(jql: "project = INC AND labels = 'incident' AND created >= -90d ORDER BY created DESC")
```

**Create follow-up action items in Jira:**
```
jira_create_issue(project: "PROJ", issue_type: "Task", summary: "Post-mortem action: <action>", description: "<what, owner, deadline, success criteria>", labels: ["post-mortem"], priority: "High")
```
Link the action back to the incident:
```
jira_create_issue_link(inward_issue: "INC-456", outward_issue: "PROJ-789", link_type: "is blocked by")
```

**Publish the post-mortem to Confluence:**
```
confluence_create_page(space_key: "ENG", title: "Post-Mortem: <Incident Title> (<Date>)", content: "<filled post-mortem template>", parent_page_id: "<post_mortems_page_id>")
```

**Graceful fallback:** Output the post-mortem as structured Markdown — ready to copy into Confluence. List action items with PROJ ticket format for manual creation.
