---
name: close-scope
description: Fixes what a reconciliation covers before any figures are pulled, which means the accounts, the campaigns and the dates that are being closed. Use it when running `ref/mkt/reconcile-media-spend`.
license: CC-BY-4.0
metadata:
  agent: spend-reconciler
  agent-version: "1"
---

# Close scope

## What it does

Fixes what a reconciliation covers before any figures are pulled, which
means the accounts, the campaigns and the dates that are being closed.
Anything outside that scope stays out of the period.

## Where it happens

The agent does this in one activity across one reference process. Each
one names the activity as that process words it.

- **Set What the Close Covers**
  - `ref/mkt/reconcile-media-spend`, activity 1 -
    [Reconcile Media Spend](../../../../processes/marketing/reconcile-media-spend.md)

## What to record

The reconciliation for the period at a version, one row per line: what
was ordered, what ran, what was billed, the difference, and the amount
at stake. Against every unmatched line, the question that went to the
issuer, the date it went, the answer that came back, and what that
answer settled. A line still open on the day the period closes is
recorded as open, with its age and its amount. A credit is recorded
against the line it settles, so the next period is checked against a
figure that already accounts for it.

That contract covers every activity this abstract agent takes on, and it
is repeated in `com.agentcatalog.agent/RECORDS.md`. What the abstract
agent does not do is in `com.agentcatalog.agent/NOT.md`.
