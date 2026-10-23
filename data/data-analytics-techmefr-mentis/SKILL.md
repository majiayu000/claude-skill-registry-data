---
name: data-analytics
description: Use when working against a real data landscape for reporting, dashboards, KPIs or extraction, especially when it is split across several independent systems of record rather than one warehouse.
---

# data-analytics

Business layer (`business/README.md`). For the mechanics of writing SQL well, defer to whatever
stack skill applies (`skills/*-conventions`, a query tool); this block is about the shape of the
data *landscape* itself — the thing that has to be understood correctly before a query is safe to
trust.

**This is not a substitute for the company's own data engineering expertise.** It's the set of
questions and defaults that keep an AI-assisted query from being confidently wrong about a landscape
it can't see in full. Where the company has a documented schema, a data dictionary or a governance
policy, that wins outright.

**An applied override is recorded, not hidden.** Write what the company's own documentation or governance
policy requires, and leave one short neutral trace addressed to whoever can decide (a line in the PR
description, the task summary or an ADR): which rule was overridden, by what, and that it is a resolved case.
Never phrase it as "a conflict between mentis and the house rules" to a non-technical stakeholder — that
framing reads as broken even when the case is a normal, resolved one, and has already caused a real project to
get abandoned and restarted over nothing. Raise one specific, named question to the decider only when no rule
anywhere actually resolves the case.

## When
As soon as a task touches reporting, a dashboard, a KPI, an extraction or a consolidation across more
than one data source — before the first query is written, not after it returns a plausible-looking
number.

## Steps

**Read only the sections the task actually touches.** The rules live one file per section under
`references/`; §1 comes first on any task, §4 applies to all of them, and §2, §3 and §5 are read when
the task is documentation, a consolidation or a metric. `agents/oracle` reads them §-by-§ in that
order.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Map the landscape before querying it | always, before the first query | [`01-landscape.md`](./references/01-landscape.md) |
| 2 | Usage guide, not schema dump | writing down what a table is for, or judging an existing note | [`02-usage-guide.md`](./references/02-usage-guide.md) |
| 3 | Consolidation across independent instances | a figure has to span several per-entity databases | [`03-consolidation.md`](./references/03-consolidation.md) |
| 4 | Data-handling invariants | any task that reads real data | [`04-invariants.md`](./references/04-invariants.md) |
| 5 | KPI and dashboard discipline | a metric or a dashboard is proposed, defined or reviewed | [`05-kpi-dashboard.md`](./references/05-kpi-dashboard.md) |

## Output / checkpoint
No pipeline checkpoint (business layer, see `business/README.md`). What it owes: the landscape mapped
(§1) before the first query, a usage-guide-shaped note on any table whose role isn't obvious, the
consolidation tradeoff named explicitly when a `UNION ALL`-shaped fix is proposed, every number
traceable to the table and logic that produced it, and — for a KPI or dashboard — a written definition
(§5.1) that survives being questioned a month later.

## Guardrails
- Never treat an identifier as portable across independent per-entity/per-tenant instances of the same
  schema without checking (§1.2).
- Never present a fragile hand-maintained consolidation view as a permanent architecture without
  naming its maintenance and performance cost (§3.1).
- Never write to a system of record to answer a reporting question (§4.1).
- Never substitute a default for a missing value to make a number look complete (§4.2).
- Never put a metric on a decision-making dashboard without running the decision test (§5.2) first.
- Never let the same business term be computed two different ways in two places without flagging it —
  that's the single-source-of-truth rule (§5.3), and it's cheaper to fix before both numbers ship.
- Never guess at a company's data governance, retention or access-control policy (§4.10) — ask the team
  that owns the data landscape, the same way `business/data-protection` routes lawful-basis questions
  to a DPO rather than answering them.
- This block has no dedicated in-house data-engineering expertise behind it yet: a solid set of
  defaults, not proven doctrine, to be confronted with a real analytics engagement.

## Origin
Generalised from the org catalogue's two BI landscape skills, plus public sources for the layered
modeling, the data-quality vocabulary and the KPI discipline. The full provenance and the refresh log
are in [`references/origin.md`](./references/origin.md).
