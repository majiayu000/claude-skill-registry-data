---
name: jade-core-batch-processor
description: >-
  Enforces Rule-by-Rule Sequential Batching — processes exactly ONE rule_id batch
  at a time. For the selected rule_id, prepares all per-file tasks from the flag
  index, tracks per-file completion, and persists batch artifact + status. No
  cross-rule parallel execution.
when_to_use: >-
  Use inside the RULE_BATCH_LOOP phase. The orchestrator invokes this skill once
  per rule_id from the rule queue. Do not invoke independently.
arguments: [rule_id]
argument-hint: "<rule-id>"
context: fork
agent: Explore
allowed-tools: Bash(grep *) Bash(find *) Bash(wc *) Write Edit
paths: "**/*.java"
---

# JADE Rule Batch Processor

## Objective

Process exactly ONE `rule_id` at a time. No next rule until the current rule's
batch is fully processed, verified, and committed (by the orchestrator).

## Sequential Batching Policy

1. **One rule at a time.** The orchestrator feeds a single `rule_id`. This skill
   produces the per-file task list for that rule and tracks each file's
   completion. It does NOT dispatch the next rule.

2. **Per-file task list.** For the selected `rule_id`, query `04-flag-index.json`
   for all flagged entries. Group entries by file. Each file becomes a task with
   its own status (`PENDING`, `IN_PROGRESS`, `DONE`, `SKIPPED`, `FAILED`).

3. **No cross-rule parallelism.** Files flagged under different `rule_id` values
   are never processed together. Each rule is a self-contained batch.

4. **Atomic outputs.** All writes use tmp-file + atomic replace. Status JSON is
   updated after every file completion so the batch can be resumed if
   interrupted.

5. **Halt on failure.** If a file task fails, mark it `FAILED`, update the batch
   status, and return a non-zero exit code. The orchestrator handles halting.

## Required Input

- `artifacts/04-flag-index.json` — produced by jade-core-scanner
- `artifacts/05-rule-queue.json`   — produced by orchestrator (validates rule_id exists)
- `rule_id` (CLI argument)
- `artifacts/03.5-knowledge-graph.json` — optional; adds impact context only

## Produced Artifacts

- `artifacts/05-rule-batch-{rule_id}.json` — per-file task list with statuses
- `artifacts/05-rule-batch-status.json`     — aggregate completion tracker

The `files` list remains limited to files directly flagged for the requested rule.
Each entry is marked `transform_scope: "DIRECT"`.
When graph metadata is available, `impact_only` records sorted dependent files and
their graph paths/reasons, source artifact, and source identity. Graph diagnostics
are retained as additive metadata and warnings; they never change direct task
selection. Each impact entry is marked `transform_scope: "IMPACT_ONLY"`; these
files never change `total_files` or dispatch.

## Script

Use `scripts/rule_batch_runner.py` with the required arguments.
