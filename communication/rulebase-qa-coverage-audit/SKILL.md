---
name: rulebase-qa-coverage-audit
description: Use to audit QA coverage and scorecard health in a Rulebase workspace via the Rulebase MCP server. Trigger for "audit our QA coverage", "which agents or channels aren't being evaluated", "are our QA scores meaningful", "is our scorecard working", QA blind spots, score distribution or ceiling effects, and checking whether QA scores relate to SLA or complaint outcomes.
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: product
---

# Rulebase QA coverage audit

Audits a Rulebase workspace for the two failure modes that make a QA programme
look healthy while producing nothing usable: **coverage blind spots** (whole
segments never evaluated) and **instrument failure** (scores that don't
discriminate or predict anything).

This is read-only. It reports; it does not change scorecards, evaluations, or
conversations.

## Prerequisites

The Rulebase MCP server must be connected. If its tools aren't available, stop and
tell the user to connect it — do not attempt the audit from exported files, since
the coverage denominator lives in the workspace.

## Step 0: Introspect before querying

**Do not assume tool signatures or field names.** They change between workspace
versions and differ by plan. Start every run by discovering the actual shape:

1. `get_current_organization` — confirm which workspace you are in, and state it
    back to the user before doing anything else. Auditing the wrong tenant is the
    main risk here.
2. `get_workspace_schema` — the authoritative list of queryable entities and
    fields. Every query below must be built from what this returns, not from the
    field names used in this document.
3. `list_scorecards` — how many scorecards exist, and whether they are versioned.

If a field this skill references doesn't exist in the schema, adapt or skip that
check and say which checks you skipped. Never invent a field name to make a query
run.

Prefer `query_workspace_data` for anything aggregate. The `list_*` tools are for
structure and small result sets; paginating them to compute totals is slow and
usually unnecessary.

## Step 1: Coverage

The question is not "how many evaluations did we do" but "what did we never
look at".

Compute evaluated conversations as a share of eligible conversations, broken down
independently by:

- **Channel** — email, chat, voice, messaging
- **Team / queue**
- **Agent**
- **Period** — by month, to catch coverage that quietly stopped
- **Intent or topic**, if the workspace labels them

Report **zero-coverage segments first**. A channel or team with no evaluations at
all is a bigger finding than one with low coverage, and it will not appear in any
average.

Define eligibility explicitly from the schema and say what you excluded. Spam,
auto-closed, and no-response conversations are legitimate exclusions; excluding
transfers or very short conversations quietly removes the cases most likely to
have failed.

Query patterns: [references/audit-queries.md](references/audit-queries.md).

## Step 2: Statistical power per agent

Coverage percentages hide the problem that matters for anyone using these scores
to coach or rank. For each agent and period, get the evaluation count `n`, then
report the confidence interval on their score.

For a pass rate from `n` evaluations, the 95% interval is roughly
`±1.96 × sqrt(p(1−p)/n)`:

| n per agent per period | ±95% CI at p = 0.90 |
| --- | --- |
| 4 | ±29 pp |
| 10 | ±19 pp |
| 25 | ±12 pp |
| 50 | ±8 pp |
| 100 | ±6 pp |

At small `n` use a Wilson interval, which is asymmetric and honest: **4 out of 4
passes gives a 95% interval of 51%–100%.**

Report the share of agents whose `n` is below the threshold needed for the
decisions the scores are actually being used for. If scores drive rankings or
bonuses at `n < 25`, that is the headline finding of the audit, ahead of anything
about coverage.

## Step 3: Distribution health

Pull the score distribution overall and per scorecard: count, mean, standard
deviation, p25, p50, p75.

- **Interquartile range under ~5 points** is a ceiling effect. The scorecard
  cannot distinguish anyone from anyone, and no coaching will ever show up in it.
- **Mean above ~95% with low variance** means criteria are being passed by
  default rather than assessed.
- **A spike at exactly 100%** often indicates unfinished or rubber-stamped
  evaluations. Check whether those evaluations have criterion-level detail.

## Step 4: Criterion health

For each criterion on each scorecard, compute the fail rate.

- **Fail rate under ~2%** — the criterion carries almost no information. Either
  promote it to auto-fail, where rarity is the point, or cut it.
- **Fail rate near 50% with high grader disagreement** — likely an ambiguous
  criterion rather than a genuine split.
- **Fail rate at 0% across thousands of evaluations** — it is ceremony. Say so.

If the workspace records auto-fails separately, check they are routed and closed
out rather than only recorded. An auto-fail with no follow-up is a compliance
finding.

## Step 5: Outcome linkage

The test of whether the scorecard measures quality: does it relate to anything the
business cares about? Aggregate to agent-period level first — conversation-level
correlations are dominated by noise.

Compare agent-period QA score against:

- SLA attainment (`get_sla_performance_summary`)
- Complaint volume (`list_complaints`, `search_complaints`)
- Repeat contact or reopen rate, if the schema exposes it
- CSAT, if present

Expected directions: QA score up, complaints down, SLA attainment up. Report the
correlation and the number of agent-periods behind it. Near-zero correlation means
the scorecard measures conformity rather than quality — that is a rebuild
recommendation, not a tuning one.

Restrict to agent-periods with `n ≥ 10` evaluations, and say how many agents that
excluded. A correlation computed across agents with 3 evaluations each is measuring
sampling noise.

## Step 6: Coaching loop closure

Coverage is worthless if nothing follows from it. Using `list_coaching_sessions`
and the evaluation records:

- What share of low-scoring evaluations led to a coaching session?
- What is the median lag from evaluation to coaching? Beyond a couple of weeks the
  conversation is no longer memorable and the feedback lands as an audit finding.
- Do agents who received coaching show subsequent score movement? Weak evidence
  without a control, so state it as descriptive.

## Guardrails

- **Read-only.** Do not create, update, or delete scorecards, evaluations, or work
  items. If the user asks for remediation, propose it and let them confirm; use the
  write tools only on explicit instruction.
- **Confirm the tenant first.** Report the organization name from
  `get_current_organization` before presenting findings.
- **Do not quote transcripts in the report.** Reference conversation IDs. If an
  example is genuinely needed, ask first, then redact.
- **Small cells stay suppressed.** Do not report a rate for a segment with fewer
  than ~30 evaluations without labelling it as indicative only, and never rank
  agents on such cells.

## Present results to the user

Lead with the finding that changes a decision, not with the coverage percentage.

1. **Workspace and window** — organization name, period audited, scorecards in
   scope, and the eligibility rule you used.
2. **Blind spots** — segments with zero or near-zero coverage, as a table.
3. **Decision validity** — the share of agents whose evaluation count is too low
   for how the scores are being used, with the confidence interval stated in plain
   terms ("an agent's monthly score is ±29 points — usable for picking coaching
   examples, not for ranking").
4. **Instrument health** — ceiling effect yes/no, IQR, and the list of criteria
   that never fail.
5. **Outcome linkage** — correlations with the number of agent-periods behind
   them, and the direction check.
6. **Loop closure** — coaching follow-through rate and median lag.
7. **Ranked recommendations**, each naming the specific finding it addresses and
   whether it is a coverage fix, a rubric fix, or a process fix. These have
   different owners.
8. **Checks skipped**, and why — missing schema fields, insufficient data, tools
   unavailable. Do not let an incomplete audit read as a clean one.
