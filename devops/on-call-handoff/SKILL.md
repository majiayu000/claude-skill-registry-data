---
name: on-call-handoff
description: Structure effective on-call shift handoffs to ensure continuity of incident response. Covers what to communicate, how to document open issues, system health state, and how to set the incoming engineer up for success. Reduces MTTR by eliminating context loss at handoff.
triggers:
  - "on-call handoff"
  - "shift handoff"
  - "paging handoff"
  - "end of on-call"
  - "taking over on-call"
  - "incident handoff"
audience:
  - engineer
  - manager
---

# On-Call Handoff

Transfer on-call context completely so the incoming engineer can respond effectively from minute one.

---

## Why Handoffs Fail

- Ongoing incidents described as "it's fine now" when the root cause isn't fixed
- Open alerts silenced without documentation
- Workarounds applied but not written down
- Incoming engineer has to ask the same questions in the middle of the next incident
- No signal on system health heading into the shift

---

## Handoff Checklist

Before your shift ends, complete this checklist:

### Active Incidents
- [ ] Any P1/P2 still in progress? If yes, do NOT hand off mid-incident — stay until stable
- [ ] Any incidents resolved in the last 24h that are "resolved but watching"?
- [ ] Any open postmortem action items that affect on-call response?

### Open Alerts / Silences
- [ ] Any alerts currently silenced? Why? Until when?
- [ ] Any alerts that fired but are "known flaky"? Ticket linked?
- [ ] Any Dependabot / security alerts that need immediate action?

### System Health
- [ ] Error rates normal on all services? (link to dashboard)
- [ ] Any elevated latency or saturation trends?
- [ ] Any deployments in the last 24h that should be watched?
- [ ] Any scheduled jobs that failed or are overdue?

### Upcoming Risks
- [ ] Any deploys scheduled in the next 24h?
- [ ] Any maintenance windows or infrastructure changes?
- [ ] Any traffic events expected (launches, marketing pushes, seasonal spikes)?

---

## Handoff Document Template

```markdown
## On-Call Handoff: [Date] [Your Name] → [Incoming Name]

**Shift**: [start time] → [end time]  
**Dashboard**: [link]  
**Incident tracker**: [link]  
**Runbook index**: [link]

---

### 🔴 Active Issues (needs immediate attention)

#### Issue: [Title]
- **Status**: [investigating / mitigated / monitoring]
- **Impact**: [who/what is affected]
- **Current state**: [what you know so far]
- **What to watch**: [metric, alert, log query]
- **Next action**: [what needs to happen next]
- **Ticket**: [link]

---

### 🟡 Watching (stable but monitor)

| Service | Symptom | Since | Ticket | Watch Until |
|---|---|---|---|---|
| [name] | [description] | [time] | [link] | [condition] |

---

### 🔇 Silenced Alerts

| Alert | Silenced Since | Why | Restore When |
|---|---|---|---|
| [name] | [time] | [reason] | [condition] |

---

### 📋 Recent Incidents (last 24h)

| Time | Service | Summary | Status | Postmortem |
|---|---|---|---|---|
| [time] | [service] | [1-line summary] | Resolved | [link or "in progress"] |

---

### 🚀 Upcoming Changes

| When | What | Risk | Owner |
|---|---|---|---|
| [time] | [description] | [Low/Med/High] | [name] |

---

### 💡 Tips for This Shift

[Anything unique about the current state of the system, known quirks,
 who to call for what, etc.]

**Key contacts**:
- Database issues: [name / Slack handle]
- Infra/AWS: [name / Slack handle]
- Product escalation: [name / Slack handle]
```

---

## Synchronous Handoff (Live)

For high-stakes shifts (post-major-incident, complex active issues), do a live handoff:

**Format**: 15-minute sync

**Agenda**:
1. Walk through active issues (5 min)
2. Dashboard review — walk the incoming engineer through current state (5 min)
3. Questions from incoming engineer (5 min)

**Outgoing engineer rule**: Don't say "it's fine" — describe specifically *why* it's fine and what you'd watch for.

---

## Manager: On-Call Health Signals

Watch for these signals that on-call is becoming unsustainable:

| Signal | Threshold | Action |
|---|---|---|
| Incidents per shift | > 3 | Reduce alert noise; fix recurring issues |
| Pages outside business hours | > 2/week avg | Audit alert thresholds and routing |
| "Watching" items that never resolve | > 1 week old | Prioritize fix in backlog |
| Same incident repeats | 2+ times | Block for postmortem and systemic fix |
| Engineer reports burnout | 1 mention | Immediate backlog reprioritization |

---

## Post-Shift: What to File

After your shift ends:
- [ ] Link to any new runbook entries you created
- [ ] File tickets for anything that needs fixing but wasn't urgent
- [ ] Update known-issues doc if you found new quirks
- [ ] Provide verbal/written feedback on alert quality: was anything too noisy? too silent?

---

## References
- Google SRE Book: [Chapter 12 — Effective Oncall](https://sre.google/sre-book/being-on-call/)
- PagerDuty: [On-Call Best Practices](https://www.pagerduty.com/resources/learn/on-call-management/)
- LeadDev: [Sustainable on-call practices](https://leaddev.com/on-call)

## MCP Integration

**Query open and in-progress incidents from Jira:**
```
jira_search_issues(jql: "project = INC AND status in ('Open', 'In Progress') ORDER BY priority DESC, created ASC")
```

**Read known-issue tickets linked to current incidents:**
```
jira_get_issue(issue_key: "INC-<id>")
```

**Search for the current runbook in Confluence:**
```
confluence_search(query: "runbook <service_name>", space_key: "OPS", limit: 3)
```

**Write the handoff document to Confluence:**
```
confluence_create_page(space_key: "OPS", title: "On-Call Handoff — <Date> (<Outgoing> → <Incoming>)", content: "<formatted handoff document>", parent_page_id: "<on_call_logs_page_id>")
```

**Graceful fallback:** Output the handoff document as Markdown with a message: `> 📋 Paste into Confluence > OPS > On-Call Logs > <Date>`.
