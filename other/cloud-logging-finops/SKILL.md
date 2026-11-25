---
name: cloud-logging-finops
metadata:
  version: "1.0.1"
  category: CloudObservabilityAndMonitoring
description: >-
  Audits Cloud Logging costs for a Google Cloud project: the charges for log entries written to log buckets, the services, log streams and severities that drive them, and the log sinks that route them. Reconciles Cloud Billing export costs with Cloud Monitoring volume metrics, and generates a FinOps report with charts and copy-paste exclusion filters. Use when auditing Cloud Logging spend, finding logging waste, identifying top logging contributors, generating log cost reduction reports, or creating log sink exclusion filters. Don't use for querying log entries (use cloud-logging-query-generation), configuring Cloud Monitoring alerts, or querying metrics/traces.
---

# Cloud Logging Finops

**Non-interactive runs.** When no user can answer (e.g. a scheduled or
automated run), ask nothing: audit the project named in the request, or the
active gcloud project; use `--billing-mode=search`; cover all five report topics
(Step 2.5); and never enable an API or upgrade a log bucket. Put anything that
needed a user (a disabled API, a missing role, the upgrade advisory) in the
report instead.

## Usage Attribution

**MUST READ**: Before executing any `gcloud`, REST API, or MCP command, you
MUST read and follow the instructions in
[Usage Attribution](references/attribution.md).

## Step 0: Locate the Cloud Billing Export

The audit covers one Google Cloud project, `{project_id}`: the project the user
names or, if they don't name one, the active gcloud project (`gcloud config get
project`), confirmed with the user.

Discover everything else (log buckets, Observability Analytics, sinks,
exclusions, metrics) yourself; never ask the user about those. The billing export is the
exception: finding it unaided can mean scanning every project on the billing
account, so ask once, before running anything, and don't start a search until
the user has chosen answer 3 (single-select, using the host's question tool if
it has one):

> **Do you know where the Cloud Billing export for `{project_id}` is?**
>
> 1.  **Yes** — here it is *(the BigQuery table ID `project.dataset.table`, or
>     just the project and dataset)*
> 2.  **There's no billing export** for this project
> 3.  **No / not sure** — search for it *(seconds on a small project; on a large
>     billing account it can take a long time)*

Answer | Flags                                                                                         | Cost figures
------ | --------------------------------------------------------------------------------------------- | ------------
1      | `--billing-mode=explicit` plus `--billing-table` (or `--billing-project`/`--billing-dataset`) | invoiced
2      | `--billing-mode=none`                                                                         | list-price estimates
3      | `--billing-mode=search` *(default)*                                                           | invoiced if found, else estimates

Answer 3's search has no time limit: it checks `{project_id}` first (usually
under 10 s, 1–2 min with many tables), then every project on its billing account
(can take many minutes; progress prints every 30 s). Tell the user this before
launching. If the wait is unacceptable, offer to switch to answer 1 (they look up
the table) or answer 2 (skip the export and use list-price estimates). Don't
suggest setting up an export to make the search faster.

If the search found an export, tell the user: *"Next time, pass
`--billing-table=<table>` and discovery drops to about two seconds."*

## Step 1: Environment Setup

Check these prerequisites before Step 2; fix only what is missing:

*   **gcloud:** if `gcloud` is not installed, follow
    https://docs.cloud.google.com/sdk/docs/install-sdk.md.txt.
*   **Project:** run `gcloud config get project`; if it isn't `{project_id}`
    (from Step 0), run `gcloud config set project {project_id}`.
*   **Credentials:** the scripts use Application Default Credentials. Run
    `gcloud auth application-default login`, or set
    `GOOGLE_APPLICATION_CREDENTIALS` to a service account key.
*   **Billing:** the project must have an active billing account attached.
*   **APIs:** don't enable APIs up front; the Logging, Monitoring, BigQuery and
    Observability APIs are on by default in new projects. Only if the collector
    reports an API as disabled (`SERVICE_DISABLED`, "has not been used in
    project"), name it, ask the user, and on approval run `gcloud services
    enable {api} --project={project_id}` (tagged as described below):
    *   `logging`, `monitoring`: required; without them there is nothing to
        audit.
    *   `bigquery`: invoiced costs from the billing export.
    *   `observability`: resolves the project's default log scope, so log
        samples match what Logs Explorer shows.
    *   `cloudasset`, `cloudbilling`: only answer 3's search across the billing
        account.

IAM roles for the identity running the audit. The skill never grants roles: the
scripts run with the user's own credentials and read only what those
credentials can. When a step fails on permissions, its advisory names the step;
tell the user which role below it needs:

Role                                                                 | Needed for
-------------------------------------------------------------------- | ----------
`roles/logging.viewer`, `roles/monitoring.viewer`                    | Every audit: log buckets, sinks, log samples, volume metrics
`roles/bigquery.jobUser`, `roles/bigquery.dataViewer` (on the export dataset) | Invoiced costs from the billing export
`roles/logging.viewAccessor` on log views in other projects        | Reading samples through a default log scope that includes them
`roles/cloudasset.viewer`, `roles/billing.viewer` (billing account)  | `--billing-mode=search` across the billing account
`roles/logging.configWriter`                                         | Only the optional Observability Analytics upgrade (Step 3B)

```bash
[ -f /tmp/finops_venv/bin/python ] || (uv venv /tmp/finops_venv && uv pip install -r scripts/requirements.txt --python /tmp/finops_venv/bin/python)
```

The bundled scripts tag their Google Cloud API requests. For commands you run
yourself, follow [Usage Attribution](references/attribution.md).

## Step 2: Data Collection

Start the collector below as a background process (it takes from seconds to
many minutes), then go to Step 2.5 while it runs:

```bash
/tmp/finops_venv/bin/python scripts/collect_logging_data.py \
  --project-id {project_id} --billing-mode={none|explicit|search}
```

Optional: `--billing-project`, `--billing-dataset`, `--billing-table` (e.g.
`billing-proj.ds.gcp_billing_export_v1_XXXX` or a curated FinOps view).

Outputs: `logging_usage_summary.json`, `monthly_details/`, `service_details/`,
and `[FINOPS ADVISORY]` lines (see Step 3). The collector's output ends with a
`[COLLECTION PROFILE]` table of per-stage timings; if the run took longer than
the times in Step 0, or the user asks why the audit took so long, read that
table before guessing.

## Step 2.5: Ask What the Report Is For

Always ask this while the collector runs (multi-select). If the user skips it,
cover all five topics:

> **What should this report answer?**
>
> -   Where is the money going — attribution by service and stream
> -   Is spend growing — trends and projection
> -   What can I safely turn off — concrete savings actions
> -   What are these logs actually saying — noisiest patterns and samples
> -   Severity and audit-log posture

The user's choices decide which outputs you read in depth and what your
summary leads with; they never change what the collector gathers:

Interest         | Read deeply
---------------- | -----------
Attribution      | `service_details/*.json`, `daily_services`
Growth           | `monthly_details/*.json`, `mom_patterns`, `cost_projection`
Savings actions  | `reduction_actions`, `extraneous_spend`
What logs say    | `severity_summary.samples_by_service`, `granular_analytics.top_signatures` (Observability Analytics only)
Severity / audit | `severity_summary`, withheld-rule reasons

Your narrative goes in `insights/executive_summary.html` (see
[Executive Summary Authoring](references/executive_summary_authoring.md)).
You don't write the savings actions: the generated report's Cost Optimizer tab
lists them from `reduction_actions`.

> [!CAUTION] Never edit `assets/report_template.html`.

## Step 3: Follow the Advisories

### A. Tell the User What the Cost Figures Are Based On

> [!IMPORTANT] Unless figures are invoiced (`billing_metadata.invoiced`), tell
> the user in plain language where you looked, what you found, and what the
> numbers are based on. Keep internals (stage numbers, mode names, HTTP codes,
> "quota project", "Cloud Asset Inventory") in the log and
> `billing_metadata.fallback_chain`.

*   **Answer 1, the location gave no costs** (`explicit_table` or
    `explicit_scope` step not `found`): the collector never searches beyond what
    the user named. Tell them what was wrong, from the step's `detail` (no rows
    for this project, no export table there, or the query failed), that costs
    are list-price estimates, and offer to rerun with a corrected location or
    with answer 3.
*   **Answer 2** (`user_declared_no_export`): "I didn't search — you told me
    there's no billing export — so costs are list-price estimates, not invoiced
    amounts." Never call a skipped search exhausted.
*   **Answer 3, found nothing** (`billing_account` status `not_found`): "I
    searched this project and your billing account and found no billing export.
    Costs are list-price estimates (quote each SKU's price and free tier from
    `pricing.skus`) over a trailing 30 days." Only this case supports
    recommending export setup. Cite the official pricing page
    (https://cloud.google.com/products/observability/pricing) as the source of
    list prices.
*   **Answer 3, search failed on permissions** (any step status
    `inconclusive`): tell the user the lookup couldn't complete, so costs are
    estimates. Never tell them no billing export exists; the search didn't
    finish.
*   **Answer 3, this project's table rejected** (`local_project` status
    `no_project_records`): "This project has a billing export, but it holds no
    records for this project, so I searched the rest of the billing account."
    Then report the outcome of that wider search as above.
*   **Partial history:** months are labelled `actual_bq_billing` or
    `usage_estimated`; state the exact date boundary in the executive summary.

When on list pricing, recommend export for accuracy: future audits would use the
actual invoice, including discounts, over multiple months.

### B. Observability Analytics

Observability Analytics was formerly called Log Analytics; the scripts'
advisories and field names still use the old name.

*   **Disabled:** present the advisory, including that upgrading the log bucket
    is irreversible, then end your reply with a direct question, e.g. *"Do you
    want me to upgrade the `_Default` log bucket to Observability Analytics?
    This can't be undone."* Telling the user how to run it themselves is not
    asking. Only after they approve upgrading that log bucket, run `/tmp/finops_venv/bin/python
    scripts/enable_log_analytics.py --project-id {project_id}`. The audit
    proceeds on Cloud Monitoring either way.

> [!CAUTION] Never run `enable_log_analytics.py` or `gcloud logging buckets
> update --enable-analytics` in the same turn you raise the advisory, or on
> general permission like "do whatever you need".

*   **< 24 hours old:** the 14-day Cloud Monitoring baseline is used until
    samples accumulate (~1–2 hours).
*   **1–13 days:** cite the sample window in the report.
*   **≥ 14 days:** full SQL analytics.
*   **`Representative logs unavailable` advisory:** samples are missing because
    your environment can't read log entries (needs `roles/logging.viewer`), not
    because streams are empty. Relay the error and role; per-stream detail is in
    `severity_summary.sample_errors`.
*   **Samples empty but the stream has volume:** samples are read through the
    project's default log scope, like Logs Explorer
    (`analytics_metadata.log_read_scope`). If its `source` is `project` and it
    has a `note`, the scope couldn't be resolved, so logs held outside this
    project's log buckets weren't read. Say that and relay the `note`; never say the
    stream has no logs.

### C. Measurement Integrity

> [!CAUTION] Never quote cost or volume derived from Observability Analytics
> payload byte sums; they overstate billed volume about 2x.

Question                     | Source
---------------------------- | ------
Cost, GiB ingested           | Billing export (`billing.query_logging_billing_costs`, `daily_gib`, `monthly_costs`)
Service mix                  | `logging.googleapis.com/billing/bytes_ingested` (`resource_type`)
Log stream / severity volume | `logging.googleapis.com/byte_count` (`log`, `severity`)
Severity mix, entry content  | Observability Analytics SQL (`constants.PAYLOAD_BYTES_SQL`)

*   Totals come from the invoice when it exists; metrics only supply shares.
    Never put a metric-derived total next to an invoiced one.
*   `byte_count` (received) and `billing/bytes_ingested` (billed) differ by
    ~1.5x or more; never divide one by the other.
*   If `telemetry_integrity.status` is `degraded`, say dips on the listed days
    look like a metric defect that won't self-correct, and repeat the limits in
    `telemetry_integrity.note`. Never claim with certainty that nothing changed.
*   A month with `is_partial: true` is month-to-date. Label it so, and never
    call it a complete month or "last month".

### D. Extraneous Spend

`extraneous_spend.headline` is a conservative floor: the sum of the
`reduction_actions.actions` with `counted: true` (duplicate bucket routing,
flow-log sampling, DEBUG logs, stale exclusions), each priced on exactly what
its remedy removes. Everything else is surfaced, never counted: over-retention
(not quantified), sampled exclusion rules (estimates), and Data Access audit
logs (in `withheld`).

1.  Report it as a floor (`≥ X%`), never a point estimate or "up to".
2.  If `status` is `insufficient_data`, give no figure — not a guess, a
    benchmark, or $0.
3.  Quote any action's `flag` verbatim; it is written for the reader.
4.  Uncounted actions and `uncounted_total_pct` may be mentioned as upside,
    never added to the headline.
5.  If `headline.exceeds_sanity_ceiling`, say the headline isn't reliable, name
    the largest counted action, and flag it for manual review. Offer no number.
6.  If `inventory_unavailable` is non-empty, say log sink, exclusion and
    flow-log actions weren't checked; never say none exist.
7.  Whenever Data Access audit logs come up (a `withheld` entry, or the user
    names them), say they are left out of the number because they need a
    compliance decision: disabling or excluding them is frequently prohibited
    by compliance or security policy, so the owner must confirm before acting.

### E. Exclusion Filters and Actions

*   Only Cost Optimizer actions carry filters and savings; Service Details
    volumes are not savings. Report `sample_coverage.shown_pct`.
*   Quote an action's monthly figures (`monthly_gib`, `monthly_usd`), never a
    rule's sample-window GiB (`granular_analytics.exclusion_candidates`).
*   `rule_scope: stream` drops every log entry of that severity in the stream; say so.
*   If `refused_claims` is non-empty, name the streams the safety gate removed.

Never offered as actions: `CRITICAL`/`ALERT`/`EMERGENCY` (incident signal), free
`_Required` streams ($0, audit retention), Data Access audit logs (often
compliance-mandated; report, never count), and streams with no measured volume.

> [!CAUTION] Hand-written exclusion filters must: include a severity predicate
> (`severity = "DEFAULT"` for DEFAULT — omitting it matches everything); use the
> URL-encoded log ID (`compute.googleapis.com%2Ffirewall`); never embed
> unescaped log text or rotating tokens (UUIDs, IPs, long integers, times) in a
> regex; and respect the list above.

## Step 4: Build and Deliver the Report

```bash
/tmp/finops_venv/bin/python scripts/build_report.py --summary logging_usage_summary.json --insights-dir insights/ --output log_usage_report.html
```

`build_report.py` writes an executive summary unless you provide
`insights/executive_summary.html`.

Give the user one link that, when clicked, opens the fully rendered report — not
raw HTML, not a missing file — from wherever the user actually is. Confirm that
will happen before you post it.

Then list what they can explore (charts, service drilldowns, ranked actions with
copyable filters, ✓ Prove It drawers) and suggest 3–4 follow-up questions drawn
from this project's data, phrased to ask as-is.

If the user asked something specific, answer it directly with both GiB and USD,
from `monthly_aggregations` (`latest_complete_month` names the newest whole
month; each month's `top_service` is its Top Cost Driver), `mom_patterns`,
`cost_projection`, `trailing_30d_summary` (its `top_driver` is the report's Top
Cost Driver without an invoice), `granular_analytics` (present only when
Observability Analytics ran), or the per-service/month detail files.

## Step 5: Follow-Up Questions

**Phase 1 (default):** answer from the JSON on disk in a few sentences or a
small table, name what the data can't settle, then stop and offer 3–4 ways to go
deeper. Don't re-run collection or re-query sources.

Question about         | Read
---------------------- | ----
A severity             | `severity_summary`, `granular_analytics.top_signatures` for that severity
A service              | `service_details/{service}.json`, `top_signatures` and `top_log_names` for it
An optimization action | its entry in `reduction_actions.actions` (`claims`, `refused_claims`, `flag`, `counted`)

**Phase 2 (only after the user picks a direction):** go as deep as it needs. Run
Observability Analytics SQL against `analytics_metadata.table_name`, the `_AllLogs` view
the collector measured. Step 3 still applies.

## Step 6: Prove It

`provenance.claims[<id>]` records each headline figure's `formula`, `sources`
(exact query, Google Cloud console link, steps; only the 10 largest streams per action),
known `differences` from the console, and runnable `checks` (covering every
stream). Ids include `latest_complete_spend`, `mtd_run_rate`,
`trailing_30d_volume`, `estimated_run_rate`, `top_cost_driver`,
`extraneous_spend`, `severity_costs`, `service_mix`, `action::<action id>`. A
claim built from others lists them in `see_also` (`extraneous_spend` → its
counted actions); prove those too, and `verify_claim.py` re-checks them with it.

When asked to prove a figure:

1.  **Now, from disk:** walk the formula with its inputs; list each source with
    its Google Cloud console link, its query exactly as recorded, and steps; then the
    `differences`.
2.  **Same turn, in the background:** run `/tmp/finops_venv/bin/python
    scripts/verify_claim.py --summary <summary> --claim "<id>"`; don't wait.
3.  **When it finishes:** a table (check | report | live | Δ | ✓/△/✗) and a
    one-line verdict. Explain △ with the recorded `differences`; give ✗ causes
    in one line each.

> [!CAUTION] Prove It is the only request that may re-query sources, and only
> via `verify_claim.py`. Don't re-run collection or alter the recorded queries.

Disclose when relevant: whether the claim was priced (`pricing.mode`) `per_sku`
(each SKU's price and free tier in `pricing.skus`) or `blended` (reason in
`pricing.notes`); that service and severity figures exclude credits; and, if
`cross_project_billing`, that reproducing it needs `roles/bigquery.dataViewer`
on the billing export dataset and `roles/bigquery.jobUser`.
