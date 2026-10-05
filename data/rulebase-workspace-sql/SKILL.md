---
name: rulebase-workspace-sql
description: Use when querying a Rulebase workspace with SQL through the MCP server's query tool — writing queries that finish inside the statement timeout, and avoiding the join fan-outs that silently inflate QA evaluation counts. Trigger for "query my Rulebase data", "the query timed out", "statement timeout", "canceling statement due to statement timeout", counts that don't reconcile between two Rulebase queries, criterion counts exceeding team counts, or any multi-step analysis over Rulebase conversations and evaluations.
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: product
---

# Querying a Rulebase workspace with SQL

Rulebase exposes workspace data to an AI client as a **read-only SQL sandbox over
organization-scoped views**. It is the most capable tool on the server and the one
that fails most often, in two ways that look nothing alike:

1. **The query times out.** Recoverable, obvious, and expensive in wasted turns.
2. **The query returns a wrong number confidently.** Not recoverable, not obvious,
   and it ends up in someone's board deck.

This skill is about both. Read-only: it cannot change workspace records.

## Step 0: introspect, always

**Never write a query from remembered field names.** Views and columns differ
between workspaces and plans.

1. `get_current_organization` — confirm the tenant and state its name to the user.
2. `get_workspace_schema` — the authoritative catalog of views and columns. Every
   query must be built from what this returns.

If a column this skill mentions is not in the schema, adapt or skip that step and
say which you skipped. Never invent a column name to make a query parse.

The sandbox runs read-only with a bounded statement timeout. Treat that timeout as
a design constraint from the first query, not as an error to react to.

## Why queries time out

**`LIMIT` bounds the output, not the work.** This is the single most useful thing
to understand about the sandbox.

The views are wide: they coalesce content across several underlying tables and some
compute per-row aggregates for things like call transcripts. Cost is driven by *how
many rows match your predicates*, not by how many you asked to see. Two consequences:

- **`ORDER BY` over a computed expression forces full evaluation before the limit
  applies.** `ORDER BY COALESCE(external_created_at, created_at) LIMIT 50` cannot
  stop early — the database must produce and sort every matching row to know which
  50 win. A query shaped like that over a busy conversation is not slow because of
  the 50; it is slow because of the 400,000.
- **A `LEFT JOIN LATERAL` with an aggregate inside runs once per matching row.**
  Narrow the row set before it, never after.

So the fix is almost never a smaller `LIMIT`. It is a smaller *matching set*.

## Patterns that finish

**1. Resolve identifiers first, fetch content second.** Two cheap queries beat one
expensive one. Query for the ids and metadata you need using indexed predicates,
then query content keyed by those specific ids. This is the highest-leverage
pattern in the sandbox and it works for almost every "show me the messages where…"
question.

**2. Bound the time window explicitly, on an indexed timestamp.** Every analytical
query should carry a date range even when the user did not give one. Ask, or state
the window you chose.

**3. Slice long windows and union the slices.** If a month times out, run two
half-months and add them. Slicing is not a workaround to apologise for — for
anything with per-row work it is the correct shape. Keep the slices in one query
with `UNION ALL` when you need a single result set.

**4. Prefer `UNION ALL` over `OR` across different predicates.** An `OR` spanning
two columns commonly defeats index use where two unioned branches each use one.

**5. Aggregate in SQL. Never page rows into context to count them.** If you find
yourself asking for 5,000 rows to compute a rate, the rate belongs in the query.
Context is the scarcest resource in the loop and row dumps are the fastest way to
spend it.

**6. Calibrate on one day before running the window.** A query that works on a day
usually works on a month; one that times out on a day never will. This costs one
cheap round trip and saves several expensive ones.

**7. Sort small, not large.** Order by an indexed column, or return the small
aggregate and sort it in your head. Do not ask the database to sort a large set by
a derived expression.

**8. Count distinct conversations, not rows,** whenever the grain is uncertain —
`count(distinct conversation_id)` is the honest denominator when a join may fan
out. Which brings us to the part that produces wrong answers.

## The fan-outs that produce wrong numbers

These are correctness bugs, not performance bugs, and they do not announce
themselves. Each one has been the cause of a real reconciliation failure.

**One conversation carries many evaluations.** Rulebase produces one evaluation per
eligible agent per matching scorecard. A ticket three people touched can hold three
scores, and two scorecards double that again. Any query joining conversations to
evaluations and then counting conversations will over-count unless you aggregate
first or count distinct.

**Criterion-level counts exceeding team-level counts.** The canonical symptom of a
fan-out. It has two usual causes, and they compound:

- Joining criterion results through to conversations or conversation-agent records
  **without restricting to the evaluated agent**, so every criterion row multiplies
  by the number of agents on the ticket.
- Grouping criteria **by name rather than by scorecard-scoped identity**, so
  same-named criteria from two scorecard versions merge into one inflated bucket.

If your item-level `n` is larger than the team's evaluation total, stop and find the
fan-out. Do not report the number with a caveat.

**Superseded and inactive evaluations.** Re-evaluated tickets leave older
evaluation records behind. A query that omits the active/completed filter counts
history as if it were current, and — this is the trap — it inflates *some*
aggregates and not others, so totals stop reconciling between two of your own
queries. Apply the same status filter everywhere in one analysis, and say which
filter you used.

**Bot and system accounts look like agents.** Automated repliers, AI agents, and
integration service accounts appear in agent-shaped columns. Left in, they become
your top-volume "agent" and distort every per-agent average. Author-type and
actor-type fields distinguish them, but **do not trust a single field in either
direction** — validate against the actual distribution on a small sample before
building attribution on it, and name the accounts you excluded.

**Duplicate and merged conversations.** Workspaces carry duplicate-pointer columns.
A self-join through one of these can silently return zero rows for a filter that
should match plenty, which reads as "no data" rather than as a broken join. If a
plausible filter returns exactly zero, suspect the join before believing the result.

**Channel is not evenly populated.** Voice, chat, and email conversations carry
different fields, and a predicate that is `NULL` for one channel drops it from the
result entirely. Check per-channel counts before comparing across channels.

## Reconciling against the app

When a number must match what the user sees in Rulebase, do not reverse-engineer
the definition from SQL. Pull the equivalent figure from the purpose-built summary
tools first, then reconcile your query to it. If they differ, the difference is
almost always one of: the status filter, the date field (event time vs. evaluation
time vs. import time), the scorecard scope, or a fan-out from the list above. Check
those four before concluding either number is wrong.

State which date field you used. "July" means three different sets of conversations
depending on whether you filtered on when the conversation happened, when it was
imported, or when it was evaluated.

## Guardrails

- **Read-only.** Do not attempt writes through this tool, and do not use write
  tools mid-analysis to "fix" data you find.
- **Confirm the tenant before reporting.** Name the organization.
- **Never echo transcript text into chat.** Report counts, ids, and aggregates. If
  a genuine example is needed, ask first, then redact. Support transcripts contain
  names, addresses, card fragments, and health and financial disclosures.
- **Suppress small cells.** Do not report a rate for a segment with fewer than ~30
  observations without labelling it indicative, and never rank people on such
  cells.
- **Do not compare people on unadjusted numbers.** Agents work different mixes of
  channel, queue, and difficulty. An unadjusted per-agent ranking mostly ranks
  their inbox.

## Present results to the user

1. **The window and the date field** you filtered on, stated explicitly.
2. **The filters that define the population** — status, scorecard scope, excluded
   accounts. This is the part that makes the number reproducible.
3. **The answer**, with the denominator visible next to every rate.
4. **Reconciliation**, if a comparable figure exists in the app, and the explanation
   for any gap.
5. **What you could not compute** — slices that timed out, fields absent from the
   schema, segments suppressed for size. An incomplete analysis must not read as a
   complete one.
