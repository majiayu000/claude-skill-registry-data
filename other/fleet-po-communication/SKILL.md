---
name: fleet-po-communication
description: How PM communicates with the PO — filtering noise, summarizing decisions needed, routing gates. The signal-to-noise discipline that respects PO attention.
---

# PO Communication — PM's Signal Filter

The PO has limited attention. 10 agents produce constant activity. Your job is to filter that activity down to what the PO actually needs to see and decide. Never dump raw data. Always summarize, highlight, recommend.

## The 3 Communication Types

### 1. Gate Requests (BLOCKING — PO must decide)

**When:** Readiness reaches 90%, phase advancement, scope change.
**How:** `pm_gate_route(task_id)` packages the context, then `fleet_gate_request()` sends it.
**Format:**
```
GATE REQUEST: {task_title}
Type: readiness_90 | phase_advance
Agent: {who did the work}
Readiness: {pct}%
Contributions: {received list}
Plan confirmed: {yes/no}
RECOMMENDATION: Approve — all criteria met and contributions received.
```
**Rule:** Include your RECOMMENDATION. The PO decides, but you inform the decision.

### 2. Escalations (URGENT — PO input needed)

**When:** Unresolvable blocker, conflicting requirements, unclear scope, compound risk.
**How:** `fleet_escalate(title, details)` → ntfy + IRC + board memory.
**Format:**
```
ESCALATION: {specific question}
Context: {what led here — 2 sentences}
Options: {what you've considered}
WHAT I NEED: {specific decision or direction}
```
**Rule:** Never escalate without options. "I'm stuck" wastes PO time. "I'm stuck between A and B, here's the tradeoff" respects it.

### 3. Status Updates (INFORMATIONAL — PO reads when convenient)

**When:** Sprint standup, milestone reached, pattern noticed.
**How:** Board memory with `[sprint]` or `[status]` tags. PM standup via `pm_sprint_standup()`.
**Format:**
```
Sprint S4: 7/12 done (58%), 3 in progress, 1 blocked.
Blocked: task X on API dependency — reassigning to devops.
Velocity: on track for sprint completion by Friday.
```
**Rule:** Only report when there's something to report. "Everything fine" is HEARTBEAT_OK, not a status update.

## What NOT to Send the PO

| Don't Send | Why | Instead |
|-----------|-----|---------|
| "Agent X completed task Y" | PO sees this in board memory automatically | Nothing — it's already visible |
| "Tests are passing" | PO doesn't need to know routine operations | Only report if tests were FAILING |
| Raw task lists | PO can't process 20 tasks at once | Summarize: "3 blocked, 2 need review" |
| Technical details | PO decides WHAT, not HOW | "Design uses adapter pattern" → "Design ready for review" |
| Every contribution received | This is internal coordination | Only flag when ALL received → "Ready for work" |

## The PO Routing Rule from CLAUDE.md

```
- Readiness 50% → checkpoint notification (informational)
- Readiness 90% → gate request to PO (BLOCKING)
- Phase advancement → gate request to PO (ALWAYS)
- Unclear requirements → route to PO with specific question
- Never dump raw data on PO. Summarize, highlight what needs deciding.
```

## Batching

When multiple items need PO attention, batch them:
```
PO Summary (3 items):
1. GATE: Task "Auth middleware" at 92% — recommend approve
2. ESCALATION: Task "API redesign" scope unclear — need direction on endpoints
3. INFO: Sprint velocity tracking above target — no action needed
```

One message with 3 items is better than 3 separate interruptions.

## The ntfy Priority Map

| Communication Type | ntfy Priority | When |
|-------------------|--------------|------|
| Gate request | important | Readiness 90%, phase advance |
| Escalation | urgent | Blocker, compound risk, security |
| Status update | info | Sprint standup, milestone |
| Routine | (no ntfy) | Board memory only |

Don't cry wolf. If every message is urgent, nothing is urgent.
