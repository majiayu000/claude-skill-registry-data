---
name: cs-escalation
version: 1.0.0
description: Package a customer escalation for engineering, product, or leadership as a decision-ready handoff — impact, timeline, facts vs. hypotheses, and a specific ask with an owner.
author: matrixx0070
tags: [customer-support, escalation, handoff, incident, impact, ownership]
capabilities: []
---

## When to use

Use this when a ticket exceeds frontline scope and needs an owner outside support: a confirmed bug, data-loss risk, security concern, churn-threatening account, or a repeat issue with no support fix. Write it so the receiving team acts without a second round of questions.

**Not for:** routine tickets you can resolve yourself (use cs-draft-response), sorting a fresh inbox (cs-ticket-triage), or venting frustration up the chain. If you cannot name a specific ask and owner, it is not ready to escalate.

## Method

1. Classify the type (Bug / Outage / Data / Security / Billing / Churn-risk / Feature-gap) and pick the target team. State in one line why it leaves support scope.
2. Quantify impact: users/accounts affected, revenue at stake, plan tier, renewal date, and whether it is spreading. **Decision point:** if it is spreading or touches data/security, treat as P1 and page the on-call now instead of filing async.
3. Reconstruct a dated timeline: when it started, what the customer did, what support already tried, current state. Link the ticket, logs, screenshots, and repro steps.
4. Tag every line `[confirmed]` or `[suspected]`. **Decision point:** if the root cause is only `[suspected]`, ask for investigation — do not assign a fix.
5. State the specific ask, the deadline, and the interim customer unblock (workaround given? credit offered?).
6. Name an owner and a next check-in time so it cannot stall silently.

## Example

> **[P1] Enterprise exports returning empty ZIPs since 09:00 UTC**
> Impact: 1 enterprise account (Acme, $48k ARR, renewal in 3 weeks), spreading — 2 more accounts reported in the last hour.
> Timeline: 09:00 first report · 09:20 reproduced on staging · 09:35 rollback of deploy #4821 did not resolve.
> `[confirmed]` ZIP is 0 bytes. `[suspected]` linked to storage-service latency.
> Ask: eng to root-cause and confirm by 14:00 UTC. Interim: manual export sent to Acme.
> Owner: @storage-oncall · Check-in: 13:00 UTC.

## Pitfalls

- Vague impact ("important customer") — always attach numbers and a renewal date.
- Presenting a guess as diagnosis — an unmarked hypothesis sends eng down the wrong path.
- No deadline or owner — the escalation dies in a queue.
- Leaving the customer dark while you escalate — always ship an interim message or workaround.

## Output format

```
Title: [SEVERITY] one-line summary
Impact: users · revenue · tier · renewal · spreading?
Timeline:
  - HH:MM event
Facts vs. hypotheses:
  - [confirmed] ...
  - [suspected] ...
The ask: <what> by <deadline>
Interim unblock: workaround / credit
Links: ticket · logs · repro
Owner: @name · Next check-in: <time>
```
