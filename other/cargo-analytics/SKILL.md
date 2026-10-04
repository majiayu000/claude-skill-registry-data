---
name: cargo-analytics
description: "Get data out of Cargo and measure what ran — download a run output, export a segment or model to CSV or JSON, and pull run and batch success and error counts. Triggers: \"download the results\", \"export this to CSV\", \"give me the file\", \"how many succeeded\", \"what is my error rate\", \"send me the enriched list\", \"get the output of that run\", \"how many records did it write\". Skip when: asking why something failed or where credits went — use cargo-diagnostics; asking about credits, plans, or invoices — use cargo-billing."
version: "1.6.0"
compatibility: Requires @cargo-ai/cli (npm). Sign in or create an account with `cargo-ai login --email` (emailed code, no browser), `--oauth`, or an API token
homepage: https://github.com/getcargohq/cargo-skills
metadata:
  author: getcargo
  openclaw:
    requires:
      bins:
        - cargo-ai
    install:
      - kind: node
        package: "@cargo-ai/cli@latest"
        bins:
          - cargo-ai
    homepage: https://github.com/getcargohq/cargo-skills
---

# Cargo CLI — Analytics

Measurement and export: monitoring run metrics, downloading run and batch results, and exporting segment data.

> See `references/response-shapes.md` for full JSON response structures.
> See `references/troubleshooting.md` for common errors and how to fix them.
> See `references/examples/run-analytics.md` for run metrics and error monitoring.
> See `references/examples/exports.md` for data export and download examples.
> For billing, usage metrics, and subscription: use the `cargo-billing` skill.

## Bootstrap

Already signed in (`cargo-ai whoami` returns a workspace)? Skip to the next section.

```bash
npm install -g @cargo-ai/cli            # no global install? prefix every command with `npx @cargo-ai/cli`
cargo-ai login --email you@company.com  # emailed code, no browser; creates the account on first use
                                        # alternatives: --oauth (browser) · --token <api-token> (CI)
cargo-ai whoami                         # confirm the active workspace before any write
```

Every command prints JSON to stdout; failures exit non-zero with `{"errorMessage": "..."}`. Anything that creates a run or a batch is async — pass `--wait-until-finished` or poll the matching `get`. When the full skill bundle is installed, [`../cargo/references/prerequisites.md`](../cargo/references/prerequisites.md) adds the CLI version pin, token scopes, and the admin-only surface.

## Scope — measure and export, not explain

This skill answers **"what happened"** and **"give me the data"**: metrics, counts, downloads, exports. The moment the question becomes **"why"** — why did this run fail, why is the output wrong or empty, which root cause explains these errors, why is this play so expensive — switch to the `cargo-diagnostics` skill; its runbooks sequence the raw surfaces into a diagnosis.

| The question sounds like… | Load |
| --- | --- |
| "What's the error rate?" / "How many runs failed this week?" / "Export the results / segment" | **this skill** |
| "Why did this run fail?" / "Run succeeded but the output looks wrong" | `cargo-diagnostics` → `references/run-trace.md` |
| "Why does this batch have errors? Which node keeps failing, and is it one cause or many?" | `cargo-diagnostics` → `references/batch-error-sweep.md` |
| "Why is this play so expensive? Where do the credits go?" | `cargo-diagnostics` → `references/play-optimize-credits.md` |

The two skills chain naturally: analytics **detects** (error rate spiked, batch reports failures), diagnostics **explains** (18 of 20 failures share one root cause), then analytics **retrieves** the clean results once the cause is fixed and the runs re-executed.

## Discover resources first

Most analytics commands require UUIDs. Discover them before querying.

```bash
cargo-ai orchestration play list            # all plays (name, workflowUuid)
cargo-ai orchestration tool list            # all tools (name, workflowUuid)
cargo-ai orchestration workflow list        # all workflows (uuid only — no name)
cargo-ai ai agent list                     # all agents (uuid, name)
cargo-ai connection connector list          # all connectors (uuid, name, integrationSlug)
cargo-ai storage model list                # all models (uuid, name, slug)
```

## Quick reference

```bash
cargo-ai orchestration run get-metrics --workflow-uuid <uuid>
cargo-ai orchestration run download --workflow-uuid <uuid> --is-finished
cargo-ai orchestration run count --workflow-uuid <uuid> --statuses error
cargo-ai orchestration query execute "SELECT status, count() FROM runs GROUP BY status"
cargo-ai segmentation segment download --model-uuid <uuid> --filter '{"conjonction":"and","groups":[]}'
```

**Picking the right command:**

- `run get-metrics` / `run count` — workflow-scoped, predefined aggregations. Best when you already have a `workflowUuid`.
- `orchestration query execute` — ad-hoc SQL across the entire workspace (`runs`, `batches`, `spans`, `records`). Best for cross-workflow analytics, per-node breakdowns, and time-series.
- `run download` / `run download-outputs` — per-record output retrieval.
- `segment download` / `storage query execute` — storage data (Companies, Contacts, …).

## Workflow run metrics

Aggregated metrics for workflow runs (success/error rates, credits per node).

```bash
# Metrics for a workflow
cargo-ai orchestration run get-metrics --workflow-uuid <uuid>

# Scoped to a release, batch, or date range
cargo-ai orchestration run get-metrics --workflow-uuid <uuid> --release-uuid <uuid>
cargo-ai orchestration run get-metrics --workflow-uuid <uuid> --batch-uuid <uuid>
cargo-ai orchestration run get-metrics --workflow-uuid <uuid> \
  --created-after <start-date> --created-before <end-date>
```

## Run count

Count runs matching specific criteria — useful for monitoring.

```bash
cargo-ai orchestration run count --workflow-uuid <uuid> --statuses error
cargo-ai orchestration run count --workflow-uuid <uuid> --is-finished \
  --created-after <start-date> --created-before <end-date>
cargo-ai orchestration run count --workflow-uuid <uuid> --batch-uuid <uuid>
```

Supports: `--statuses`, `--batch-uuid`, `--release-uuid`, `--is-finished`, `--created-after`, `--created-before`, `--record-id`, `--record-title`.

For cross-workflow analytics or shapes that `run count` doesn't expose (per-node failure breakdowns, p95 durations, error rate over time), use `orchestration query execute` — see the [Ad-hoc execution analytics](#ad-hoc-execution-analytics-orchestration-query) section.

## Ad-hoc execution analytics (`orchestration query`)

Run SQL against orchestration runtime tables — `runs`, `batches`, `spans`, `records` — for analytics that the canned metrics commands don't cover. Tables are referenced without a schema prefix; workspace scoping is automatic. See `cargo-orchestration/references/examples/queries.md` for schemas and limits.

```bash
# Error rate across the workspace in the last day
cargo-ai orchestration query execute \
  "SELECT countIf(status='error') / count() AS error_rate FROM runs WHERE created_at > now() - INTERVAL 1 DAY"

# Failed runs per workflow this week
cargo-ai orchestration query execute \
  "SELECT workflow_uuid, count() AS errors FROM runs WHERE status='error' AND created_at > now() - INTERVAL 7 DAY GROUP BY workflow_uuid ORDER BY errors DESC"

# Per-node failure counts (last 24h)
cargo-ai orchestration query execute \
  "SELECT node_slug, count() AS failures FROM spans WHERE execution_status='error' AND execution_started_at > now() - INTERVAL 1 DAY GROUP BY node_slug ORDER BY failures DESC"

# Credit spend by workflow this month
cargo-ai orchestration query execute \
  "SELECT workflow_uuid, sum(credits_used_count) AS credits FROM batches WHERE created_at >= toStartOfMonth(now()) GROUP BY workflow_uuid ORDER BY credits DESC"
```

Read-only and capped: 30s execution time, 10 000 result rows, 10 000 000 rows scanned. Narrow with a `created_at`/`execution_started_at` predicate to stay under the row-scan cap.

## Downloading run results

Two distinct commands — pick the right one for the job.

### `run download` — one row per run, one column per node (gzipped CSV)

Returns `{"url": "..."}` — a signed URL to a **gzipped CSV**. Each row is a run: `_uuid`, `_workspace_uuid`, `_workflow_uuid`, `_record_id`, `_record_title`, `_created_at`, `_finished_at`, `_status`, `_error_message`, followed by **one column per node slug**.

**Each node column holds that execution's `title` — a truncated human-readable summary, not the node's output.** There is no `runContext` and no `executions[]` in this file. Treat it as a status board across many runs (which node errored, on which record), never as evidence of what a node produced — the same rule `cargo-diagnostics` applies to `title` everywhere else.

```bash
# Every run of a workflow
cargo-ai orchestration run download --workflow-uuid <uuid>

# Date range
cargo-ai orchestration run download --workflow-uuid <uuid> \
  --created-after <start-date> --created-before <end-date>

# Specific statuses (run statuses: idle, pending, running, success, error,
# cancelling, cancelled, skipped — NOT "finished"/"failed")
cargo-ai orchestration run download --workflow-uuid <uuid> --statuses success,error

# Every run that reached a terminal state. `--is-finished` is `finished_at IS
# NOT NULL`, which is wider than success+error: cancelled and skipped runs
# stamp finishedAt too, so don't substitute one for the other.
cargo-ai orchestration run download --workflow-uuid <uuid> --is-finished

# From a specific batch
cargo-ai orchestration run download --workflow-uuid <uuid> --batch-uuid <uuid>
```

### `run download-outputs` — per-run input + output (CSV/JSON via signed URL)

**This is the canonical way to get action results out of the platform.** Maps to API `POST /v1/orchestration/runs/download-outputs`. Returns `{"url": "..."}` — a signed URL to a CSV (default) or JSON file. One row per run: the same `_`-prefixed run metadata, plus `input` (the first node's resolved config) and `output` (the chosen node's context, defaulting to the **last executed node** when `--output-node-slug` is omitted).

```bash
# --workflow-uuid is the only required flag
cargo-ai orchestration run download-outputs \
  --workflow-uuid <uuid> \
  --format json \
  --limit 20

# Pin the output node explicitly, and filter by batch
cargo-ai orchestration run download-outputs \
  --workflow-uuid <uuid> \
  --output-node-slug <slug> \
  --batch-uuid <uuid>
```

To find the `output-node-slug`: `cargo-ai orchestration release get <release-uuid>` → look at `nodes[].slug`. The terminal output node is typically named `output` or `end`. Without `--limit`, the file covers **every** matching run of the workflow, so pass one when you only need a sample.

**Per record instead of per run:** `cargo-ai orchestration record download-outputs` takes the same `--workflow-uuid` / `--output-node-slug` and emits one row per **record**. It pages with `--limit` and `--offset` (CLI ≥ 1.0.90) — the way to export a set too large for a single file is to walk it in fixed slices (`--limit 1000 --offset 0`, then `--offset 1000`, …) rather than requesting everything at once. `run download-outputs` pages the same way, over runs.

### Getting the full `runContext` for several runs

You can't, in one call. The full per-node context is a **per-run S3 object**, and `orchestration run get <run-uuid>` is the only command that hydrates it — one run at a time. The two exports above are projections: `download` gives you node *titles* across many runs, `download-outputs` gives you first-node input + one node's output across many runs. For everything in between, loop `run get` over the UUIDs from the discovery ladder in [`../cargo-diagnostics/references/run-trace.md`](../cargo-diagnostics/references/run-trace.md) § 0.

Orchestration SQL is not an alternative here: `runs` and `spans` carry status, timing, and credits, but no node input/output columns.

## Downloading batch results

```bash
cargo-ai orchestration batch download --uuid <batch-uuid> --output-node-slug <node-slug>
```

To find the `output-node-slug`: run `cargo-ai orchestration release get <release-uuid>` (get the release UUID from the batch) and look at `nodes[].slug`.

## Handling partial batch failures

A batch with `status: "success"` can still contain individual run failures. Always inspect the batch for errors before treating results as complete.

**Step 1 — Check the batch summary:**

```bash
cargo-ai orchestration batch get <batch-uuid>
# → .runsCount          = total records submitted
# → .executedRunsCount  = records that reached a terminal state (success or error)
# → .failedRunsCount    = records that errored
```

**Step 2 — Count and download the failed runs:**

```bash
cargo-ai orchestration run count \
  --workflow-uuid <uuid> \
  --batch-uuid <batch-uuid> \
  --statuses error

cargo-ai orchestration run download \
  --workflow-uuid <uuid> \
  --batch-uuid <batch-uuid> \
  --statuses error
```

**Step 3 — Diagnose.** Working out *why* they failed — grouping failures by root cause, picking exemplar runs, reading `runContext` — is the `cargo-diagnostics` skill's job: load `../cargo-diagnostics/references/batch-error-sweep.md` and feed it the batch UUID.

**Step 4 — Re-run only the failed records:**

After the diagnosis and fixing the underlying issue (connector credentials, bad input data, rate limits):

```bash
# Extract record IDs from the failed run download, then:
cargo-ai orchestration batch create \
  --workflow-uuid <uuid> \
  --data '{"kind":"recordIds","recordIds":["id1","id2","id3"]}'
```

**Filtering by node output slug:**

To download only a specific node's output from a batch (e.g. just the enrichment node, not the full run):

```bash
# 1. Get the release UUID from the batch
cargo-ai orchestration batch get <batch-uuid>
# → .releaseUuid

# 2. Find the node slug
cargo-ai orchestration release get <release-uuid>
# → nodes[].slug

# 3. Download that node's output
cargo-ai orchestration batch download \
  --uuid <batch-uuid> \
  --output-node-slug <node-slug>
```

## Segment data export

Filter JSON uses `conjonction` (not `conjunction`) — this is intentional. See the `cargo-orchestration` skill's `references/filter-syntax.md` for the full filter syntax.

```bash
# Full export (all records)
cargo-ai segmentation segment download \
  --model-uuid <uuid> \
  --filter '{"conjonction":"and","groups":[]}'

# With sorting and limit
cargo-ai segmentation segment download \
  --model-uuid <uuid> \
  --filter '{"conjonction":"and","groups":[]}' \
  --sort '[{"columnSlug":"created_at","kind":"desc"}]' \
  --limit 1000
```

**IMPORTANT:** `segment download` requires `--model-uuid`, not `--segment-uuid`. Get the `modelUuid` from `segment list`.

For live paginated queries with enrichment, use `segmentation segment fetch` from the `cargo-orchestration` skill.

## Help

Every command supports `--help`:

```bash
cargo-ai billing usage get-metrics --help
cargo-ai orchestration run download --help
cargo-ai segmentation segment download --help
```
