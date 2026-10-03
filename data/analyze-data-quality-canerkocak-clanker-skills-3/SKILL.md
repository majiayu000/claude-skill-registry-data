---
name: analyze-data-quality
description: "Assess whether structured data, financial equations, state-machine accounting, query results, dashboards, or analytical evidence are trustworthy enough to use. Use to check data quality, reconcile conflicting sources or metric definitions, adjudicate financial-data findings, or decide whether evidence is safe to cite."
---

## Related Skills

Use $design-kpis when the work is to define or redesign a KPI framework, metric definition, guardrail, or target rather than checking whether existing data is trustworthy.

# Analyze Data Quality

Assess whether a dataset is trustworthy enough for analysis, modeling,
dashboards, experiments, or downstream pipelines. Start with the intended use and grain, run the highest-value checks for the data shape, and report concrete evidence, analytical risk, likely causes, and the smallest useful remediation or automated test.

## Workflow

1. Clarify the quality question and operating context.

   Establish what the dataset represents, the intended unit of analysis, the downstream use, whether the user cares about raw ingestion quality,
   transformed-model quality, or both, and the comparison baseline such as prior weeks, prior schema, or a trusted reference table. Identify expected grain,
   primary keys or candidate keys, important date columns, timezone assumptions,
   domain rules, allowed values, and business thresholds. If context is missing,
   infer cautiously and label assumptions.

2. Choose an inspectable analysis path.

   Preserve an inspectable SQL, query, or script artifact when computation is
   required. Use a notebook only when a notebook capability is available and it
   materially improves inspection or iteration. For queryable tables, use the
   relevant structured-data connector to confirm schema, grain, representative
   rows, and query rules before heavier checks. Use operational logs for
   freshness and lineage when those checks matter.

3. Build a compact profile.

   Start with row count, column count, column names and types, candidate keys,
   duplicate rates on likely identifiers, min/max timestamps for relevant date columns, null rates, distinct counts for likely categorical columns, and basic numeric summaries for measure columns. Confirm grain before interpreting anomalies; many apparent quality problems are mixed-grain data,
   partial backfills, late-arriving data, or duplicated joins.

4. Run core quality checks.

   Select checks that match the dataset and task. Default to the most relevant checks across completeness, uniqueness, validity, consistency, integrity,
   timeliness, volume, and shape. Compare rates, not just counts, and segment by time, source, country, platform, model version, or other key dimensions when that helps distinguish real issues from expected variation.

5. Run shape-specific checks.

   Adapt the checks to the data shape:

   - Event data: duplicate event IDs, future event timestamps, session or user
     coverage gaps, and abrupt event-mix changes after releases.
   - Dimension tables: non-unique business keys, orphan surrogate keys, status
     changes without corresponding timestamps, and unexpected churn in reference
     values.
   - Fact tables: mixed grain, impossible measures such as negative revenue or
     quantity, join blowups to dimensions, and late-arriving or partially loaded
     partitions.
   - ML feature or scoring tables: leakage from post-outcome fields, feature
     sparsity spikes, range shifts after model or feature-store changes, and
     class-label drift.
   - Experiment data: duplicate assignments, variant imbalance beyond
     expectation, exposure without assignment, and events before assignment
     timestamp.

6. Run temporal and distribution checks when history exists.

   Prioritize temporal diagnostics when the user mentions "after X date",
   "suddenly", "recently", or "only started appearing". Check first-seen dates,
   last-seen dates, daily or weekly null-rate trends, duplicate-rate trends, row count trends, category-share shifts, distribution drift, and change points around launches, migrations, incidents, model changes, or backfills.

7. Investigate analytical risks and likely causes.

   Tie each issue to the downstream risk: broken trusted analysis, biased decisions, broken joins, stale dashboards, incorrect experiments, leakage,
   unreliable model features, or misleading segments. When possible, identify whether the issue is isolated to a source, segment, partition, time window,
   release, migration, backfill, or upstream pipeline change.

8. Recommend fixes or automated tests.

   Recommend the smallest set of follow-up fixes, monitoring, or automated tests that would materially reduce risk. Suggest automation only when the rule is stable and worth maintaining. Include or save the notebook/query path when code produced the findings.

## Financial equation reconciliation mode

Use this mode when a dashboard or query compares charges, fees, balances,
reimbursements, costs, proceeds, PnL, or margin.

1. Write the exact equation before interpreting the result.
2. Materialize or otherwise compare the exact record identities on both sides;
   equal counts do not prove equal cohorts.
3. State grain, join cardinality, status filters, time window, rail, asset,
   currency, decimal scale, and sign convention.
4. State the valuation basis and price timestamp for every converted term.
5. Keep realized, retained, reimbursed, accrued, confirmed, pending, estimated,
   and mark-to-market values distinct.
6. Test retries, duplicate receipts, missing receipts, partial reimbursements,
   failed rows, and status transitions for exact-once behavior when applicable.
7. Reconcile the runtime query result against the dashboard response or rendered
   values. If the task authorizes implementation, add a regression at the
   narrowest stable boundary. Otherwise identify that boundary without editing.

A synthetic database or copied calculation can prove local equation logic. It
cannot prove the production query text, ORM/database behavior, live cohort,
credential role, or deployed data boundary. Record that gap as `partial` rather
than treating a copied expression as an integration test.

### Financial state-machine finding gate

Use this gate before calling a status-transition, fee, balance, reimbursement,
cost, or margin discrepancy a verified defect or recommending a repair.

1. Name the canonical equation and its authority. Distinguish nominal payment,
   reusable or refundable credit, accrued obligation, and realized cost.
2. Build this matrix at the exact entity and event grain:

   | Entity/state | Transition producer and guard | Persisted amount/status | Writer and idempotency identity | Downstream readers or compensation | Retry/terminal behavior | Evidence |
   |---|---|---|---|---|---|---|

3. Include application and worker code, database triggers, migrations,
   backfills, replays, retries, recovery jobs, admin/manual actions, and external
   events. A static caller graph that omits any of these is not complete state
   proof.
4. Prove whether writers are additive, alternative, or compensating. Identify
   every dashboard or query that adds a term missing from the write model.
5. Test success, failure, ambiguous outcome, duplicate delivery, replacement,
   trigger-before-worker ordering, partial reimbursement, and reprocessing after
   terminality when those states are supported.
6. Reconcile against deployed migration state and runtime rows. Static source
   can verify an edge or a local equation; it cannot verify the production
   cohort or defect when a material runtime boundary is inaccessible.
7. Before recommending a fix, nominate one canonical owner and show that the
   change cannot double-count, reopen terminal state, or move the discrepancy
   into another reader. Include removal or preservation of compensating reader
   logic in the same proof.

If the contract, a material transition producer, runtime boundary, canonical
owner, or non-interference proof is missing, classify the candidate `partial`.
Do not assign defect severity, recommend code, or use it as a blocker. If the
observed behavior matches an explicit current policy or metric contract, record
it as `policy`, not a data defect.

## Standards

### Core Checks

- Completeness: null rate by column; null rate by partition, segment, and time bucket; unexpected empty strings or sentinel values; required-column population rate.
- Uniqueness: exact duplicate rows, duplicate primary keys, duplicate composite keys, and proportion unique for semi-unique fields such as emails or device IDs.
- Validity: type conformance after casting; format checks for IDs, emails, URLs,
  enums, country codes, and timestamps; range checks for measures, percentages,
  counts, and dates; allowed-values checks for controlled vocabularies.
- Consistency: cross-field rule checks, units or currency consistency, status and timestamp alignment, and agreement between duplicated fields from different sources.
- Integrity: parent-child key coverage, orphan records, unexpected many-to-many joins, and broken slowly changing dimension joins.
- Timeliness: freshness lag from source event time to load time, freshness lag from load time to report time, missing recent partitions, and unexplained historical rewrites or backfills.
- Volume and shape: row-count drift, distinct-count drift, distribution drift,
  share-of-total drift for major categories, and new or disappeared categories.

### Specific Check Guidance

- Duplicates and keys: check exact duplicates, primary key duplicates, composite key duplicates at the intended grain, and near-duplicates caused by whitespace,
  casing, formatting, or late updates. Report count, share of affected rows,
  duplicated keys, and whether duplication is isolated to a time range, source,
  or segment.
- Missingness: distinguish acceptable sparsity from broken completeness. Check null rates over time, newly null columns after schema or pipeline changes, and sentinel values such as `''`, `'unknown'`, `'n/a'`, `0`, or `-1`.
- Domain validity: check malformed identifiers, country codes, timestamps,
  impossible values, values outside allowed sets, and cross-field contradictions such as `is_cancelled = false` with a non-null `cancelled_at`.
- Join coverage: when multiple datasets are involved, check foreign keys that do not match a parent table, unexpected one-to-many expansion, coverage loss when joining to dimensions or experiments, and row counts before and after joins.
- Freshness and schema drift: check row-count changes against recent history,
  lag on important date columns, added/removed/retyped columns, and shifts in sparsity or cardinality that suggest upstream changes.
- Outliers and distribution shifts: use robust methods such as quantiles, MAD,
  or IQR before defaulting to z-scores. Check sudden changes in mean, median,
  variance, zero rate, category share, and long-tail behavior.
- Leakage, backfill, and time travel: check features populated before they should exist, future-dated records, late-arriving data causing unstable recent partitions, and backfills that change historical counts without annotation.

### Severity

Assign severity only after the failed data or metric contract, affected cohort,
and concrete downstream impact are verified. Keep `policy`, `partial`, and
disproved candidates outside the severity distribution. Missing tests or broad
reader fan-out change assurance and review priority; they do not prove severity.

- Critical: breaks trusted analysis, core joins, production dashboards, or key decisions, such as duplicated grain, missing primary keys, or stale production data.
- High: materially biases downstream decisions, such as large null spikes,
  category drift in a core dimension, invalid business-rule values, leakage, or severe join coverage loss.
- Medium: localized or explainable issues that still need documentation,
  monitoring, or owner follow-up.
- Low: cosmetic inconsistencies, expected sparsity, or known edge cases that do not materially affect current use.

Do not dump raw profiling output without interpretation. Tie each finding to an analytical risk and likely impact.

### Automated Test Guidance

- Good candidates for automation: primary key uniqueness, not-null checks on required columns, accepted values for stable enums, referential integrity,
  freshness thresholds, and seasonality-aware row-count or volume bounds.
- Use caution with hard-coded distribution thresholds on volatile product metrics, strict uniqueness in messy entity-resolution use cases, and recent partitions when late-arriving data is normal.
- Suggest automated tests only when the expected rule is stable, important, and maintainable.

### Output Standards

Use the artifact the user requested and the runtime can actually produce. A
concise chat result is sufficient for a focused reconciliation; use a report,
notebook, or dashboard only when it improves the decision or is explicitly
requested. The structure below defines the content regardless of surface.

Structure the response with:

1. dataset and grain summary
2. checks performed
3. findings
4. temporal or trend anomalies
5. likely causes and impacted use cases
6. recommended fixes or automated tests
7. assumptions and open questions

For each finding, include:

- what failed
- canonical contract or equation and authority
- evidence: counts, rates, segments, and dates
- why it matters
- severity and confidence level
- disposition: verified finding, policy, partial, or disproved candidate
- strongest counterevidence
- likely cause when known
- suggested remediation or automated test only after canonical ownership and
  non-interference are established

When code was used, include or save a notebook containing the key SQL and Python checks and make the notebook path easy to find.

### Defaults

- Prefer small, high-signal tables over exhaustive dumps.
- Compare rates, not just counts.
- Break checks out by time and key segments whenever possible.
- Normalize strings before judging duplicates or distinct-count spikes.
- Treat recent partitions carefully when data arrives late.
- Call out when an anomaly could be caused by a legitimate product launch,
  experiment, migration, incident, model change, or backfill.
- Preserve inspectable evidence: SQL, query links, notebook paths, source paths,
  sample rows, chart outputs, and calculation notes.
