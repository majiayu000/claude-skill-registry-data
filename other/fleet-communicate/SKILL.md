---
name: fleet-communicate
description: Communication guide — which surface for what, when to use each channel
user-invocable: false
---

# Fleet Communication Skill

## Which Surface for What

### Internal Chat (fleet_chat)
**For: agent-to-agent real-time communication**
- Request work: `fleet_chat("I'm idle, what should I work on?", mention="lead")`
- Ask a question: `fleet_chat("Is this the right pattern?", mention="architect")`
- Share info: `fleet_chat("FYI Plane API rate limits at 60/min")`
- Respond to requests: `fleet_chat("Take the CLI output format task", mention="ux-designer")`

### Board Memory (fleet_alert, fleet_task_complete)
**For: persistent knowledge that spans tasks**
- Decisions: tag with [decision, project:{name}]
- Alerts: tag with [alert, {severity}, {category}]
- Knowledge: tag with [knowledge, {topic}]
- Suggestions: tag with [suggestion, {area}]

### IRC Channels (automatic via fleet tools)
- #fleet — general activity
- #sprint — sprint progress and milestones
- #agents — agent status and health
- #security — security findings
- #human — items needing human attention
- #reviews — PR review notifications
- #builds — CI/CD and test results
- #memory — important decisions and knowledge
- #alerts — critical issues only
- #plane — Plane sync events

### ntfy (fleet_notify_human)
- Info → fleet-progress (quiet, in history)
- Important → fleet-review (prominent)
- Urgent → fleet-alert (sound, persistent)

### Escalation (fleet_escalate)
**For: when you need human attention NOW**
- Posts to: board memory + IRC #human + ntfy urgent
- Always include: what you need, why, what's blocked

## When to Use What

| Situation | Surface | Tool |
|-----------|---------|------|
| Quick question to teammate | Internal chat | fleet_chat |
| Decision that affects team | Board memory | fleet_alert(category) |
| Work completed | Automatic | fleet_task_complete |
| Stuck, need help | Escalation | fleet_escalate |
| Found security issue | Board memory + alert | fleet_alert(severity, "security") |
| Progress update | Task comment | fleet_task_progress |
| Need human decision | Escalation | fleet_escalate |
| Sprint milestone | Automatic | Orchestrator via ntfy |
| Idle, requesting work | Internal chat | fleet_chat(mention="lead") |