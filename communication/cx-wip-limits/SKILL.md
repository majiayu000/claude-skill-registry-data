---
name: cx-wip-limits
description: Use to set concurrency and work-in-progress limits for support teams — chat concurrency, personal WIP on async work, and limits as quality protection rather than arbitrary caps. Trigger for "how many chats per agent", "concurrency settings", "WIP limits", "agents juggling too many tickets", async backlog per person, or quality dropping as concurrent load rises.
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: playbook
---

# WIP limits

Concurrency and WIP limits look like capacity levers. Used wrong, they are quality
destroyers dressed up as free capacity.

**Chat concurrency is not free capacity.** Doubling chats per agent increases
throughput until it does not — errors, slow replies, missed messages, and customers who
leave thinking nobody is there. The gain shows on occupancy charts; the loss shows in
CSAT, repeat contact, and abandon — often on a lag nobody connects.

**Limits are quality protection**, not pessimism. They encode how much parallel work a
human can do without the customer noticing the split attention.

## Chat concurrency: the false free lunch

Each concurrent chat adds:

- Context-switching cost between threads
- Staggered response times as the agent finishes another reply first
- Risk of wrong-thread replies (quality and compliance incident)
- Perceived ghosting when gaps exceed channel norms

Throughput rises with concurrency only while response-time targets still hold. Past an
inflection point, customers abandon or repeat contact, erasing the capacity gain.

**Set concurrency from observed response time and quality**, not from a vendor default:

1. Plot median and p90 **first response time** and **inter-response time** by
   concurrency level (if the platform logs active concurrent count).
2. Plot **quality and repeat contact** at those levels — lagged if necessary.
3. Choose the highest concurrency where p90 response stays within target and quality
   does not step-change down.

If you cannot observe concurrency in data, run a controlled period at one setting and
compare — do not assume the platform maximum is optimal.

| Signal | Likely past the limit |
| --- | --- |
| p90 response time jumps with concurrency | Agents physically cannot keep pace |
| Abandon up, ASA flat | Customers leave during gaps |
| Repeat contact up on chat | Under-resolution from rushed closes |
| Wrong-customer replies in QA | Context-switch failure |
| Occupancy high, CSAT down | Busy looks productive; customers disagree |

## Personal WIP for async work

Email, messaging tickets, and back-office tasks accumulate as **open work per agent**.
Without a WIP cap, the backlog is invisible until SLAs breach — and the breach looks
like an individual failure when it was a system with no limit.

**Personal WIP limit** — maximum open items assigned to one person at once, counted by
items actively owned, not by items touched today.

Design rules:

- **Limit = what one person can advance meaningfully in one day** at median complexity
  for that queue, with headroom for one urgent insertion.
- **New work enters only when WIP drops** — pull model, not push-to-random-available-agent
  until everyone holds 40 stale tickets.
- **Different limits per work type** — a simple transactional queue can carry higher WIP
  than investigations requiring external waits.

WIP limits interact with **SLA clocks**. A ticket sitting in someone's queue at limit
while others are idle is a dispatch problem, not proof the limit is wrong.

## Team and queue WIP

Above personal limits, some operations cap **queue WIP** — total open not-yet-assigned
work — to force staffing or overflow decisions instead of infinite backlog absorption.

Use when:

- Unassigned pile grows without plan
- SLA is met on paper by timestamps but customers wait days
- Triage quality collapses because everything is "urgent"

Queue WIP cap triggers overflow, callback offer, or explicit deferral message — not
silent queue growth.

## Limits as policy, not secret shame

Publish limits where agents and planners see them:

- Chat concurrency max and when supervisors may temporarily raise it (peak with
  monitoring, not permanent creep)
- Personal async WIP by queue type
- What happens at limit — work stays unassigned, routes to overflow, or customer gets
  status message

**Temporary limit raises during peak** are valid if paired with real-time monitoring of
response time and quality same day. Permanent raises without that review are how
concurrency creeps to 6 and nobody remembers why CSAT dropped in Q2.

Supervisors need authority to **lower** concurrency when quality signals spike, not
only to add bodies.

## Relationship to occupancy and scheduling

High occupancy from concurrency is not the same as efficient staffing:

- **Occupancy** — share of available time spent handling contacts
- **Concurrency** — parallel sessions per agent on chat

An agent at 85% occupancy on three chats may be slower per chat than the same agent at
70% on two. Scheduling models that treat chat handle time as voice handle time without
a concurrency assumption will mis-staff.

For async, **WIP limits replace occupancy** as the load measure. Adherence tells you
they were at desk; WIP tells you whether work was structurally possible.

## Traps

- **Vendor default concurrency** treated as recommendation. Defaults optimise vendor
  demos, not your targets.
- **Raising concurrency to fix ASA** without measuring abandon and repeat contact —
  trades visible wait for invisible failure.
- **WIP limits without unassigned routing** — agents hit cap; new work vanishes into
  limbo with no customer message.
- **Per-agent limits on shared queues** where assignment is automatic — limit must be
  enforced by the router, not honour system.
- **Counting snoozed or pending-customer tickets in WIP** — inflates load; define open
  as "agent owes next action".
- **Same WIP for new hires and tenured agents** — ramp limits separately (see onboarding
  ramp skills elsewhere in cx-ops).

## Present results to the user

1. **Current settings** — chat concurrency, personal WIP, queue caps; stated vs actual
   if logs show drift.
2. **Response-time and quality by load level** — evidence for where inflection occurs,
   with explicit gaps if data cannot separate concurrency.
3. **Recommended limits** — chat concurrency, async WIP by queue type, with rationale tied
   to targets not benchmarks.
4. **Overflow behaviour at limit** — what customer and system should do when cap hit.
5. **Supervisor playbooks** — temporary raise/lower rules and metrics to watch same day.
6. **Staffing implication** — honest capacity at recommended limits vs current plan;
   flags false free capacity in forecasts.
7. **Implementation order** — measure → set limit → enforce in router → review in two
   weeks; not limit-first without baseline.
