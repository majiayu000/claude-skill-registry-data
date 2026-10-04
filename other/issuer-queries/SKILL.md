---
name: issuer-queries
description: Takes an unexplained or wasted line back to whoever billed it, says what is being disputed and what it is worth, and records the answer against the line, whether that answer is a credit, a fix, a replacement or a refusal. Use it when running `ref/mkt/reconcile-media-spend` and `ref/mkt/verify-ad-placement`.
license: CC-BY-4.0
metadata:
  agent: spend-reconciler
  agent-version: "1"
---

# Issuer queries

## What it does

Takes an unexplained or wasted line back to whoever billed it, says what
is being disputed and what it is worth, and records the answer against
the line, whether that answer is a credit, a fix, a replacement or a
refusal.

## Where it happens

The agent does this in three activities across two reference processes.
Each one names the activity as that process words it.

- **Claim Back the Wasted Spend**
  - `ref/mkt/verify-ad-placement`, activity 12 -
    [Verify Ad Placement Quality](../../../../processes/marketing/verify-ad-placement.md)
- **Raise the Queries**
  - `ref/mkt/reconcile-media-spend`, activity 9 -
    [Reconcile Media Spend](../../../../processes/marketing/reconcile-media-spend.md)
- **Track the Answers**
  - `ref/mkt/reconcile-media-spend`, activity 10 -
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
