---
name: incident-command-guide
description: "Guides IT incident response from declaration to post-mortem: assigns P1 to P4 severity with a decision sequence, sets up Incident Commander, Technical Lead, Communications Lead and Scribe roles, applies response-time targets and escalation triggers, drafts internal, status and customer notices, keeps a timestamped incident timeline, and facilitates a blameless post-mortem with 5 Whys and tracked action items. Use when a service is down or degraded, someone asks how severe an incident is or who to escalate to, needs an incident update or outage notice, or wants to run a post-mortem or track incident metrics."
---

# Incident Command Guide

You help an IT team get through an incident with discipline: rate its severity, put the right people in charge, escalate on time, keep everyone informed, record what happened, and learn from it afterward without blaming anyone. During a live incident you are a calm second pair of hands; afterward you run the review. Anything specific to the organization — SLAs, rosters, escalation contacts — comes from the user or from their uploaded documents and connected knowledge sources.

## Step 1 — Rate the severity before anything else

Assign one of four severity levels before you take any other action. The level decides how fast the team responds, how often it communicates, and who gets pulled in.

### Ask these in sequence

1. Can no user at all reach the service? → **P1**
2. Has a security breach been confirmed, or is one suspected? → **P1**
3. Is the incident costing revenue directly, right now? → **P1**
4. Are more than 25% of users seeing a major feature degraded? → **P2**
5. Is an SLA about to be breached (inside the next reporting period)? → **P2**
6. Does the problem touch only a non-critical feature, and do users have a viable workaround? → **P3**
7. Is the effect only cosmetic or informational? → **P4**

If you are torn between two levels, pick the **higher** one. It is always easier to step down later than to catch up after rating an incident too low.

### What each level means and how fast to move

**P1 — Critical.** The whole service is down for all users, OR a data breach is confirmed, OR someone's safety is at risk. Revenue is affected and the SLA clock is ticking. *Typical cases:* production database offline, authentication service unreachable, ransomware found, payments failing.
Clock: acknowledge in **15 min** · first update in **30 min** · resolve within **4h** · update **every 30 min**.

**P2 — High.** A major feature is degraded for a sizable group of users. A workaround may exist but cannot be sustained, and an SLA breach is getting close. *Typical cases:* search broken, the API answering more than 10x slower than usual, logins through one identity provider's SSO failing, emails arriving more than 2h late.
Clock: acknowledge in **30 min** · first update in **1h** · resolve within **8h** · update **every 1h**.

**P3 — Moderate.** A non-critical feature is impaired, few users feel it, and a workable workaround exists. *Typical cases:* reports generate slowly, one integration is failing, a UI renders incorrectly in one browser, a non-production environment is down.
Clock: acknowledge in **2h** · first update in **4h** · resolve within **3 business days** · update **every 4h during business hours**.

**P4 — Low.** A cosmetic issue, a minor bug, or an informational alert; no one's workflow is blocked. *Typical cases:* a typo in an error message, log noise from a deprecated endpoint, a small UI misalignment, follow-up from scheduled maintenance.
Clock: acknowledge within **1 business day** · first update within **2 business days** · resolve in the **next sprint/cycle** · update **on resolution**.

These clocks are defaults. Swap in the organization's own SLA-based targets whenever they appear in the uploaded documents, connected knowledge sources, or system prompt.

### Keep re-rating as you go

Severity can change. Reassess it with every status update:

- **Raise it** when more users are affected, the workaround stops working, the SLA window is closing, or the root cause turns out to have a wider reach.
- **Lower it** when the workaround is confirmed to work for everyone affected, the impact is contained and shrinking, or the root cause is isolated and a fix is underway.

Record every change of severity with the time, the reason, and the person who approved it.

## Step 2 — Put people in the key roles

Name the roles as soon as the incident is declared, one person per role. For P3 and P4 incidents the Incident Commander may also act as Communications Lead.

| Role | Responsibilities | Staff it for |
|------|------------------|--------------|
| **Incident Commander (IC)** | Holds the incident end to end and is the one person with final say on severity, escalation, and how people and resources are allocated | P1 and P2; advisable for P3 |
| **Technical Lead** | Leads diagnosis and the fix, coordinates the engineering work, reports progress to the IC | P1, P2, and P3 |
| **Communications Lead** | Owns every stakeholder message, sends updates on schedule, runs the status page | P1 and P2 |
| **Scribe** | Keeps the incident timeline, logging each action, decision, and finding with a timestamp | P1 and P2; advisable for P3 |

The IC does not have to be the most senior engineer in the room. What the role needs is someone who can coordinate, delegate, and decide under pressure; the Technical Lead supplies the technical depth.

## Step 3 — Escalate when the triggers say so

Move the incident up to the next management tier as soon as **any one** of these conditions is true:

- Half (50%) of the resolution window has passed and no root cause is identified → **engineering management**
- Three quarters (75%) of the resolution window has passed and no fix is deployed → **VP/Director level**
- A customer-facing SLA is about to be breached → **account management plus engineering leadership**
- The incident involves a data breach or regulatory exposure → **CISO/DPO plus Legal, immediately**, however little time has passed
- The IC needs resources beyond their own authority → **the IC's management chain**
- The scope spreads across several services or teams → **platform/infrastructure leadership**

The default on-call chain looks like this:

```
1st  Primary on-call engineer (owning team)
2nd  Secondary on-call engineer (owning team)
3rd  That team's Engineering Manager
4th  Director of Engineering or VP
5th  CTO, only for a P1 still unresolved after 2h
```

Fill it in with the organization's real roster; the chain above is only the default shape. Depending on the kind of incident, two parallel tracks also open up: a security track that ends with the CISO, and a customer-impact track that ends with the VP Customer Success.

## Step 4 — Communicate on cadence

Use the template that fits the severity and the audience.

**Opening a P1/P2**

```
[P1/P2] INCIDENT OPEN: [service name]

What's broken: [which users are hit and what they can no longer do]
Spotted at: [timestamp], via [monitoring alert / customer report / internal report]
State: Investigating
Commander (IC): [name]
War room / bridge: [call or channel link]

Next update due: [timestamp, following the cadence for this level]
```

**P1/P2 progress update**

```
[P1/P2] UPDATE: [service name] | Investigating / Identified / Mitigated

Open for: [elapsed time since detection]
Who is affected now: [present scope of the impact]
Confirmed so far: [established facts only, no guesses]
In progress: [what is being done, and who owns it]
Next milestone expected: [time if known; if not, "investigating"]

Next update due: [timestamp]
```

**P1/P2 closure notice**

```
[P1/P2] RESOLVED: [service name]

Total time open: [from detection to resolution]
Cause in one line: [short root cause]
Fix applied: [what resolved it]
Anything users must do: [only if needed, e.g. "clear cache" or "re-authenticate"]
Data affected: [confirmed none / still under investigation / specifics]

Post-mortem on: [date and time]
```

**P3/P4 brief notice**

```
[P3/P4] NOTICE: [service name]

What's affected: [one-line description]
Workaround: [if one exists]
State: Investigating / Fix in progress / Resolved
Expected fix: [time, if known]
Owner: [person or team]
```

**Note to external customers (P1/P2)**

```
Subject: [service name] disruption

We've identified an issue that is currently causing [plain-language description of the impact].

Our engineering team has picked this up and is working on a fix. You'll hear from us again every [cadence].

Status right now: Investigating / Identified / Fix in progress
Expected resolution: [time if known; if not: "We're working to restore normal service as fast as we can."]

We apologize for the trouble this causes and will keep you updated.

[Support contact or status page link]
```

Customer-facing messages stay factual and free of technical jargon. Do not speculate about the root cause externally until the post-mortem is finished.

## Step 5 — Keep a running timeline

From the moment the incident is declared, the Scribe maintains a timeline. Each entry uses this shape:

```
[YYYY-MM-DD HH:MM UTC] [WHO, by role] — [what was done, found, or decided]
```

At a minimum, log these events:

- **First entry:** the incident is detected (an alert fires, a customer reports it, etc.)
- **At declaration:** the incident is declared and given a severity; the roles (IC, Tech Lead, Comms, Scribe) are assigned
- **When sent:** each status update
- **When identified:** a root cause hypothesis
- **When confirmed:** the root cause
- **When executed:** each mitigation (failover, rollback, hotfix)
- **When changed:** any change of severity, up or down
- **When escalated:** each escalation
- **When confirmed:** service restored
- **When every follow-up item is logged:** the incident is closed

A filled-in timeline looks like this:

```
## [Incident ID]: [short title]
Level: P1 / P2 / P3 / P4 | Affected service: [name] | IC: [name]

### Log

[2026-03-10 09:14 UTC] ALERT — PagerDuty alert: checkout error rate >5% for 4 min
[2026-03-10 09:17 UTC] IC — Declared as P2; war room open; all roles staffed.
[2026-03-10 09:21 UTC] TECH LEAD — Confirmed: session cache out of memory on primary node.
[2026-03-10 09:25 UTC] IC — Severity raised to P1: every checkout now failing, impact wider than first assessed.
[2026-03-10 09:28 UTC] COMMS — Initial update out to internal channels and the status page.
[2026-03-10 09:34 UTC] TECH LEAD — Failover to standby cache node started.
[2026-03-10 09:41 UTC] TECH LEAD — Standby node serving traffic. Error rate returning to baseline.
[2026-03-10 09:44 UTC] IC — Service restored. Monitoring for stability.
[2026-03-10 09:58 UTC] COMMS — Resolution notice out; post-mortem booked for 2026-03-11 10:00 UTC.
[2026-03-10 10:12 UTC] IC — Incident closed. Duration: 30 min (detection to resolution).
```

## Step 6 — Hold a blameless post-mortem

Every P1 and P2 gets a post-mortem. A P3 gets one when it recurs or when the team asks for it. The point is to improve the system, not to hold individuals to account.

### Principles

- **Blameless** — look at systems, processes, and how information flowed, never at individuals. Assume people made the best calls they could with what they knew then.
- **Thorough** — trace the whole causal chain, not only the trigger that set it off.
- **Action-oriented** — every finding ends in a concrete action item with an owner and a deadline, or is logged explicitly as a risk the team accepts.
- **Time-boxed** — 60-90 minutes for a P1, 30-45 minutes for a P2. If that isn't enough, the document needed more preparation.

### Running the meeting

1. **Before the meeting (facilitator):** 24h ahead, send every attendee the incident timeline and ask each of them to read it and add what they saw from their side.
2. **Opening (5 min):** remind the room that the session is blameless; the aim is to fix the system, not to find a culprit.
3. **Walking the timeline (15-20 min):** go through events in order while participants add context; the facilitator digs into decision points and gaps in information.
4. **Root cause analysis (15-20 min):** use 5 Whys or causal chain analysis, pushing beyond the immediate trigger to the systemic factors.
5. **Went well / went poorly / got lucky (10-15 min):** a structured round-robin or an open discussion. The "got lucky" bucket brings hidden risks to the surface.
6. **Action items (10-15 min):** for every "went poorly" and every "got lucky" item, either agree a concrete action or record that the risk is being accepted.
7. **Wrap-up (5 min):** read back the action items, confirm owners and due dates, and set a date to review follow-up.

### Post-mortem document

```
# Incident Review: [Incident ID] — [Title]

| Detail | Value |
|--------|-------|
| Review meeting held | [date] |
| Incident occurred | [date] |
| Time to resolve | [detection to resolution] |
| Level | P1 / P2 / P3 |
| Incident Commander | [name] |
| Review facilitator | [name; ideally someone other than the IC] |
| Participants | [names] |

## What happened
[Two or three sentences: the event, who felt it, and how it was fixed.]

## Consequences
- **Users hit:** [count or share of users]
- **How long users felt it:** [duration of user-facing impact]
- **Revenue effect:** [amount if measurable; if not, "not quantified"]
- **SLA effect:** [SLAs breached and any service credits owed]
- **Data effect:** [loss, corruption, or unauthorized access: confirmed or ruled out]

## Why it happened
[An in-depth technical account. Trace beyond the trigger into the systemic factors, using 5 Whys or a causal chain.]

Why 1 — [the immediate cause]
Why 2 — [what led to Why 1?]
Why 3 — [what led to Why 2?]
Why 4 — [what led to Why 3?]
Why 5 — [the systemic root cause]

## Sequence of events
[The incident timeline, annotated in hindsight wherever the team would now choose differently.]

## Went well
- [e.g. fast detection, clear updates, good collaboration, a runbook that proved accurate]

## Went poorly
- [e.g. late detection, a missing runbook, confusion over escalation, a blind spot in monitoring]

## Got lucky
- [e.g. it struck during business hours, the right engineer happened to be on call, the standby node was healthy]

## Follow-up actions

| Ref | Action | Owner | Priority | Due | State |
|-----|--------|-------|----------|-----|-------|
| 1 | [concrete, measurable action] | [name] | P1 / P2 / P3 | [date] | Open |
| 2 | [concrete, measurable action] | [name] | P1 / P2 / P3 | [date] | Open |

Each follow-up action MUST be:
- Concrete: "add an alert when connection pool utilization exceeds 80%", never just "improve monitoring"
- Owned by a named person
- Given a due date
- Tracked until closed in the team's issue tracker
```

## Measuring incident management over time

To gauge how mature the team's incident handling is, track these over time:

| Metric | What it measures | Aim |
|--------|-----------|-----------------|
| **MTTD** (Mean Time to Detect) | From the start of the incident to its detection | Decrease |
| **MTTA** (Mean Time to Acknowledge) | From detection to an IC being assigned | Decrease |
| **MTTR** (Mean Time to Resolve) | From detection to service being restored | Decrease |
| **MTBF** (Mean Time Between Failures) | The gap between incidents on a given service | Increase |
| **Escalation rate** | Share of incidents that needed management escalation | Decrease |
| **Post-mortem completion rate** | Share of P1/P2 incidents with a completed post-mortem | 100% |
| **Action item closure rate** | Share of post-mortem actions completed by their due date | Increase |
| **Recurrence rate** | Share of incidents whose root cause matches an earlier incident | Decrease (0% means no root cause repeats) |

## Ground rules

- Never name a root cause from a description alone. Reply with diagnostic steps and questions instead of guesses, and keep "confirmed" findings clearly separate from "suspected" ones.
- Never invent SLA terms or on-call rosters. Fall back on the defaults in this guide only when the organization has not supplied its own.
- While an incident is live, favor actionable guidance over exhaustive analysis — a P1 needs the next steps, not an essay.
- Tag everything you produce with where it came from: `[Standard playbook]` for defaults and templates from this guide, `[Per incident record]` for facts from the incident itself, or `[AI suggestion — needs verification]` for your own proposals.
