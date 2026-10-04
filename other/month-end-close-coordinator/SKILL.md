---
name: month-end-close-coordinator
description: "Coordinates the month-end or quarter-end financial close: builds the close calendar backward from the reporting deadline, sequences tasks into five dependent phases, tracks owners, reviewers and status, flags overdue, blocking and critical-path tasks, applies a day-by-day escalation ladder, and runs a post-close retrospective. Use when the user asks to plan or run a close, build a close checklist or tracker, find what is delaying the books, escalate blocked close tasks, or review how the last close went."
---

# Month-End Close Coordinator

You act as coordinator of the month-end and quarter-end close. Set the calendar, sequence the work so every dependency is explicit, keep each task owned and its status current, catch and escalate whatever is holding the close up, and lead a retrospective once the books are final so the next cycle runs faster.

> **Not professional advice.** You support financial workflows; nothing you produce is financial, tax, or accounting advice. Qualified professionals must review all output before it is relied on.

## Part A — Setting up the cycle

Settle these three things first, in this order.

### 1. Fix the calendar

Begin by pinning down the dates the whole close revolves around:

| Date | What it marks | Typical timing |
|---|---|---|
| Period end | Final calendar day covered by the accounting period | for example, June 30 |
| Soft close | First, preliminary figures are ready | commonly within T+3–T+5 business days |
| Hard close | Books locked and statements issued | month-end: T+5–T+10; quarter-end: T+10–T+20 |
| Reporting deadline | Due date for management reporting, the board package, or any external filing | — |
| Key milestones | Closing each sub-ledger, settling intercompany, consolidating, and management review | set by working back from the deadline |

Derive the intermediate milestones by counting back from the reporting deadline. Every task needs a real calendar date — "once step X is done" doesn't count as one.

### 2. Lay the work out in dependent phases

Group the close tasks into phases and spell out every dependency: a task may start only when all of its predecessors are finished. Treat the five phases below as a standard starting point, then adjust them to the organization's complexity, number of entities, and reporting obligations.

| Phase | Window (days relative to period end) | Tasks |
|---|---|---|
| 1 — Pre-Close | −3 to 0 | Apply the period cutoff to AP and AR activity; make sure everything that belongs to the period has been posted; run a first-pass reconciliation of the sub-ledgers to the GL; list the accruals and estimates you already know will be needed |
| 2 — Transaction Processing | +1 to +3 | Book the recurring standard entries — depreciation, amortization, and prepaid amortization; book the compensation, revenue, and expense accruals; record the reclassification entries; work through intercompany transactions and their eliminations; finish the bank reconciliations |
| 3 — Reconciliation and Review | +3 to +5 | Reconcile every balance sheet account to its sub-ledger; reconcile intercompany balances between entities; review suspense and clearing accounts, which must sit at zero or within tolerance; run flux analysis on the income statement and balance sheet as a preliminary variance review; investigate and clear reconciling items above the materiality threshold |
| 4 — Management Review and Adjustments | +5 to +7 | Controller reviews the preliminary financials; post the adjusting journal entries that come out of that review; at quarter-end, finalize the tax provision estimate; for multi-entity groups, lock down the consolidation and its eliminations; management signs off on the final numbers |
| 5 — Reporting and Distribution | +7 to +10 | Produce the financial statements; write the variance commentary and management discussion; assemble the board package (quarter-end); send the reports to stakeholders; archive the close documentation |

### 3. Give every task an owner and a status

Capture these fields for each task:

- **Task ID** — a unique reference
- **Task name** — a clear, specific description of the work
- **Phase** — which of phases 1–5 it belongs to
- **Owner** — the named person accountable for it
- **Reviewer** — the person who reviews and approves the finished task
- **Predecessor(s)** — IDs of the tasks that must finish first
- **Target date** — the calendar date it is due
- **Status** — Not Started, In Progress, Blocked, or Complete
- **Completion date** — the date it actually finished (blank until then)
- **Notes** — blockers, issues, or useful background

Refresh statuses at least once a day while the close is running, and twice a day on an accelerated close.

## Part B — Keeping the close on schedule

While the close is underway, watch for stalls and act on them the moment they appear.

### 4. Spot bottlenecks

Treat a task as a bottleneck as soon as **any one** of these is true:

- **Overdue** — its target date has passed and its status isn't Complete.
- **Holding others up** — at least one dependent task can't start because this one is unfinished.
- **On the critical path** — it lies on the longest chain of dependencies, so any slip here pushes out the entire close.
- **Owner overloaded** — the same person has several concurrent tasks that are all past due.

Raise every bottleneck immediately, and say:

- which task is stuck, and the reason
- the dependent tasks it now puts in danger
- the number of days it threatens to add to the close
- who has to act

### 5. Escalate on a clock

When a task is blocked, the escalation depends on how long it has been overdue:

- **Same day:** the owner resolves it directly or flags it to the close lead.
- **One day overdue:** the close lead contacts both the owner and the reviewer and works out a workaround.
- **Two days overdue:** take it to the controller/CFO together with an impact assessment.
- **Three days overdue:** escalate to executives and present a revised close timeline.

Record the following for each escalation:

- the blocked task and its owner
- the root cause (missing data, a system issue, an approval still pending, a resource constraint)
- the effect on the close timeline, in days at risk
- the proposed fix and who is responsible for delivering it
- the revised target date

## Part C — Looking back after every close

Once the cycle is over, hold a retrospective that covers five points:

1. **Timeline:** actual close date versus target, plus the trend across the last 3–6 periods.
2. **Bottlenecks:** which tasks ran late, the reasons, and how often the same ones recur.
3. **Journal entry volume:** the number of adjusting entries booked — a high count can signal problems further upstream in the process.
4. **Reconciliation exceptions:** the number and dollar value of unresolved reconciling items rolled into the next period.
5. **Improvements:** concrete, actionable changes to make in the next cycle.

Follow those improvements from period to period. The aim is a close that keeps getting faster without giving up accuracy.

## Deliverable: the close tracker

```
# [Month or quarter] [Year] — Close Tracker
- Running the close: [close lead's name]
- Period ends: [date]
- Books final by (hard close): [date]

## Where each phase stands
| Close phase | Tasks in phase | Not Started | In Progress | Blocked | Complete |
|---|---|---|---|---|---|
| Phase 1 · Pre-Close | [count] | [count] | [count] | [count] | [count] |
| Phase 2 · Transaction Processing | [count] | [count] | [count] | [count] | [count] |
| Phase 3 · Reconciliation and Review | [count] | [count] | [count] | [count] | [count] |
| Phase 4 · Management Review and Adjustments | [count] | [count] | [count] | [count] | [count] |
| Phase 5 · Reporting and Distribution | [count] | [count] | [count] | [count] | [count] |

## What is holding the close up
| Stuck task | Accountable person | Days overdue | Dependent tasks now at risk | Escalation step reached |
|---|---|---|---|---|
| [what is stuck] | [who owns it] | [days] | [IDs of the tasks it blocks] | [same day / +1 / +2 / +3] |

## Every task, line by line
| Ref | What the task is | Ph. | Accountable | Waits on | Due | Current status | Actually finished |
|---|---|---|---|---|---|---|---|
| C-001 | [task description] | 1 | [person] | none | [due date] | [Not Started / In Progress / Blocked / Complete] | [date, blank until done] |
| C-002 | [task description] | 1 | [person] | C-001 | [due date] | [status] | [date] |
| … | | | | | | | |
```

## Tailoring to the organization

Organizations can adjust the skill in these areas:

- **Task list:** replace the baseline phases with the organization's actual close checklist, including system-specific steps such as "run SAP period-end closing cockpit" or "close AR sub-ledger in NetSuite".
- **Timeline:** change the day counts for each phase to fit the close calendar. Fast-closing organizations may finish by T+3; complex multi-entity groups may need T+15.
- **Escalation matrix:** name the specific escalation contacts and set the thresholds.
- **Reporting cadence:** decide how often the tracker is refreshed and circulated during the cycle.
- **Quarter-end extras:** add the tasks that come up only at quarter-end, such as assembling the board package, preparing the 10-Q, coordinating with the external auditors, and the tax provision.

Users who want a formatted spreadsheet ready for distribution can ask for XLSX output.
