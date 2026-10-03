---
name: kvs-benchmark-operator
description: Operate and monitor this repository's AWS DynamoDB, ADB DynamoDB API, and OCI NoSQL benchmarks through the existing dashboard pipeline. Use for benchmark launch, live status, evidence summaries, failure diagnosis, or authorized post-run cleanup; do not use for unrelated cloud provisioning.
---

# KVS benchmark operator

These repository-owned instructions are the canonical workflow for both Codex and Claude Code. The Claude discovery entrypoint is `.claude/skills/kvs-benchmark-operator/SKILL.md`; keep behavior and safety rules centralized here.

Use the repository's dashboard pipeline as the source of truth. Do not recreate provider commands or benchmark accounting when the existing controller supports the requested action.

## Choose the operation

- For status or diagnosis, perform read-only inspection of the active run, its `.dashboard-state.json`, logs, control-plane status, and collected evidence. Do not launch, retry, resize, delete, or rotate credentials.
- For a local status snapshot, run `node .codex/skills/kvs-benchmark-operator/scripts/snapshot.mjs` from the repository root. Pass `--run-id=<id>` only when the user requests a non-active run.
- For a launch, validate the selected targets, immutable image digest, workload matrix, repetitions, T0 lead, evidence buckets, and explicit dataset-write authorization. Use `node scripts/run-cloud-benchmark.mjs --spec=<file>` or the dashboard API.
- For live monitoring, prefer `GET /api/runs/active` and `GET /api/runs/<id>` when the dashboard is running. Otherwise monitor the controller process and `.kvs/cloud-runs/<id>/.dashboard-state.json`.
- For run history, read `GET /api/runs`, then inspect a selected immutable run with `GET /api/runs/<id>`. Never replace or stop the active monitor merely because the user selects an older run for comparison.
- For an authorized stop, use the owning dashboard's `POST /api/runs/<id>/stop`. It cancels active remote commands but preserves tables, infrastructure, and evidence. An attached read-only dashboard cannot stop a run owned by another controller.
- For a report, use only completed evidence. Distinguish provisional live samples from final summaries.

## Live progress

Report stage changes immediately. During workload sessions, summarize per target:

- completed, scheduled, and failed operations;
- completion percentage, calculated from completed plus failed attempts over scheduled operations;
- achieved operations/s and offered operations/s;
- current in-flight requests;
- rolling P95 while provisional;
- session index, name, human-readable description, repetition, duration, and shared T0;
- effective read/write mix, consistency, load model, execution mode, rate schedule or fixed concurrency, in-flight limit, retry policy, timeout, and dataset shape.

Poll without blocking user communication for more than 60 seconds. Avoid repeating unchanged metrics; provide a short heartbeat when a control-plane wait is materially long.

Preload performance is live only at stage level. After `dataset-preload` completes, read every `evidence/preload/<target>/preload-summary.json` and compare start skew, duration, requested/completed/failures, attempted and successful operations/s, latency percentiles, attempts/retries, and write units. Treat absent consumed-capacity data as unavailable rather than zero consumption.

When reporting a run with multiple stages, keep completed gate and workload-session results accessible while a later stage runs. Distinguish the pipeline gate number from the zero-based offered-load stage inside a session. For a variable open-loop schedule, report each stage's offered rate, duration, and complete/running/pending state; never describe a manually configured database compute change as automatic scaling.

## Acceptance and safety

- Do not call the benchmark complete until all selected sessions pass accounting, service acceptance, evidence collection, manifest generation, and package generation.
- A failed dataset certificate or hash comparison blocks workloads. Diagnose from evidence; do not silently bypass the gate.
- A delivery timeout can race with late execution. Inspect provider command state before retrying so commands do not overlap.
- Keep credentials and private runtime files out of output, logs, commits, and specifications intended for reuse.
- Include the verified runner instance IDs/OCIDs, database OCID, table identifiers, regions, and compartments in the final resource inventory without exposing credential profile names.
- Resource cleanup requires explicit authorization and exact targets. Never delete OCI tables as an inferred benchmark cleanup step. Delete any temporary resource only after the final package is verified and only when the user requested that cleanup.
- Keep the workflow portable: use Node.js and provider CLIs; do not require an operating-system-specific shell for dashboard operation.

At handoff, provide the run ID, terminal state, targets, completed session count, preload comparison when enabled, key workload results, evidence/package path, cleanup performed, and challenges encountered.
