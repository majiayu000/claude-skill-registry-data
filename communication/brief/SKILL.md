---
name: brief
description: Generate contextual briefings for legal work. Supports three modes — daily brief (morning summary of legal-relevant items), topic brief (research synthesis on a specific legal question), and incident brief (rapid briefing for developing situations like data breaches or regulatory inquiries).
---

# /brief -- Legal Team Briefing

Generate contextual briefings for legal work. Supports three modes: daily brief, topic brief, and incident brief.

**Important**: This command assists with legal workflows but does not provide legal advice. Briefings should be reviewed by qualified legal professionals before being relied upon.

## Invocation

```
/brief daily              # Morning brief of legal-relevant items
/brief topic [query]      # Research brief on a specific legal question
/brief incident [topic]   # Rapid brief on a developing situation
```

## Modes

### Daily Brief

A morning summary of everything a legal team member needs to know to start their day.

#### Sources to Scan
- **Email**: Contract requests, compliance questions, counterparty responses, external counsel communications
- **Calendar**: Meetings needing legal prep, upcoming deadlines, team syncs
- **Chat**: Legal team channels, direct messages, escalations
- **CLM**: Contracts awaiting review/signature, approaching expirations
- **CRM**: Deals requiring legal involvement

#### Output Format

```
## Daily Legal Brief -- [Date]

### Urgent / Action Required
[Items needing immediate attention]

### Contract Pipeline
- **Awaiting Your Review**: [count and list]
- **Pending Counterparty Response**: [count and list]
- **Approaching Deadlines**: [items due this week]

### New Requests
[Contract review requests, NDA requests, compliance questions]

### Calendar Today
[Meetings with legal relevance and prep needed]

### This Week's Deadlines
[Upcoming deadlines and filing dates]
```

### Topic Brief

Research and brief on a specific legal question or topic across available sources.

#### Output Format

```
## Topic Brief: [Topic]

### Summary
[2-3 sentence executive summary]

### Background
[Context and history from internal sources]

### Current State
[Organization's current position or approach]

### Key Considerations
[Important factors, risks, or open questions]

### Internal Precedent
[Prior decisions, memos, or positions found]

### Recommended Next Steps
[What to do with this information]
```

### Incident Brief

Rapid briefing for developing situations requiring immediate legal attention (data breaches, litigation threats, regulatory inquiries).

#### Output Format

```
## Incident Brief: [Topic]
**Prepared**: [timestamp]
**Classification**: [severity assessment]

### Situation Summary
[What is known about the incident]

### Timeline
[Chronological summary of events]

### Immediate Legal Considerations
[Notification requirements, preservation obligations, privilege concerns]

### Relevant Agreements
[Contracts, insurance policies implicated]

### Recommended Immediate Actions
1. [Most urgent action]
2. [Second priority]
3. [etc.]

### Information Gaps
[What needs to be determined]
```

## General Notes

- If sources are unavailable, note the gaps prominently
- Briefs should be actionable: every item should have a clear next step
- Keep briefs concise — link to source materials rather than reproducing them
