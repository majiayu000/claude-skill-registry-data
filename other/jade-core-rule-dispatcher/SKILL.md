---
name: jade-core-rule-dispatcher
description: >-
  Routes rule tasks to registry recipes via recipe-registry.json. Handles
  LOAD/MATCH/RECORD workflow but delegates all transform logic to recipe
  subprocesses. Contains ZERO version-specific or rule-specific transform code.
  Accepts one task at a time from the rule batch.
when_to_use: >-
  Use inside the RULE_BATCH_LOOP phase, dispatched once per task entry from
  jade-core-batch-processor output. The orchestrator invokes this skill per-task.
arguments: [artifacts_dir, rule_id, task_id]
argument-hint: "<artifacts-dir> <rule-id> <task-id>"
allowed-tools: Bash(python *) Read Write
---

# JADE Core Rule Dispatcher

## Objective

Route a single rule task to the correct registry recipe. The dispatcher contains **zero
transform logic** — its only job is to load the task, find the matching recipe
in `recipe-registry.json`, invoke the recipe script as a subprocess, and record
the result.

## Core constraints

1. **Never modify source files directly** — only registry recipe scripts touch source.
2. **Never contain regex or AST transform logic** — all transforms live in recipes.
3. **One execution = one file + one rule_id.**
4. All artifact writes use tmp-file + atomic rename.

## Required input

- `artifacts/05-rule-batch-{rule_id}.json` — task entry list
- `artifacts/01-breaking-changes-manifest.json` — rule definitions
- `recipe-registry.json` (in dispatcher directory)

## Produced output

- `artifacts/06-fix-results-{rule_id}.json` — aggregate array of fix records (per-flag)

## Recipe invocation contract

The dispatcher invokes recipe scripts as:
```
python <recipe-script> --file <path> --line <num>
```

Registry recipe scripts MUST:
- Exit 0 on success, non-zero on failure
- Print a single JSON line to stdout: `{"status": "FIXED|FAILED|SKIPPED|DEFERRED", "changes": N, "warnings": [...], "errors": [...], "diff_summary": "..."}`
- Handle file I/O internally (read, transform, atomic write)

The dispatcher records each result with `task_id`, `rule_id`, `file`, `status`,
`match_count`, `match_region`, `match_context`, `diff_summary`,
`verification_hint`, `errors`, `warnings`, and `applied_at`.

## Fix strategy format

In `01-breaking-changes-manifest.json`, rules specify:
```json
"fix_strategy": "recipe:jade-recipe-java1.5-generics"
```

The dispatcher looks up `rule_id` in `recipe-registry.json` to resolve the
actual script path.

## Script

Use `scripts/dispatcher.py`:
```
python scripts/dispatcher.py \
  --artifacts-dir migration-runs/sample/artifacts \
  --rule-id RAW_TYPES \
  --task-id RAW_TYPES-0001
```

## Agent mode

A recipe-registry.json entry may carry `"mode": "agent"` instead of a
`"script"` field (see `skill_md` in place of `script`). An entry with no
`mode` key behaves exactly as before -- this section only applies once a
rule's registry entry explicitly opts in.

For an agent-mode rule, the dispatcher never spawns a recipe subprocess.
Instead it turns a `05-rule-shards-<rule_id>.json` plan (produced by
`jade-core-knowledge-graph`'s `plan_shards.py`) into a self-contained task
list, and later validates + records the envelope a subagent hands back for
one shard at a time:

```
# Turn the shard plan into a task list (05-agent-tasks-<rule_id>.json).
python scripts/dispatcher.py \
  --artifacts-dir migration-runs/sample/artifacts \
  --rule-id THREAD_STOP_DISABLED \
  --emit-agent-tasks \
  --workspace-root migration-runs/sample/workspace

# After a subagent has worked one shard and written its result envelope
# (06-agent-result-<rule_id>-<shard_id>.json, schema below), record it.
python scripts/dispatcher.py \
  --artifacts-dir migration-runs/sample/artifacts \
  --rule-id THREAD_STOP_DISABLED \
  --record-agent-result \
  --shard-id THREAD_STOP_DISABLED-body-local-001 \
  --result-file migration-runs/sample/artifacts/06-agent-result-THREAD_STOP_DISABLED-THREAD_STOP_DISABLED-body-local-001.json
```

`--emit-agent-tasks` and `--record-agent-result` are mutually exclusive and
both refuse (exit 3, no artifact written) a registry entry that is not
`mode="agent"`. Neither ever opens a source file directly -- both work
only from the shard plan and the envelope, both of which carry paths and
metadata, never file content.

Result-envelope schema (one per shard, written by the subagent session,
never by this script):
```json
{
  "schema_version": 1,
  "rule_id": "THREAD_STOP_DISABLED",
  "shard_id": "THREAD_STOP_DISABLED-body-local-001",
  "status": "FIXED",
  "match_quality": "exact",
  "diff_summary": "...",
  "files": [
    {"file": "...", "match_count": 1, "changes": 1,
     "touched_line_start": 10, "touched_line_end": 12,
     "migration_skip_marker": false, "diff_summary": "..."}
  ],
  "errors": [],
  "warnings": []
}
```

Every file entry's `file` must be one of the shard's `editable_files` --
otherwise `--record-agent-result` refuses the whole envelope (exit 3, no
`06-fix-results-*` write) rather than record a partial, contract-violating
result. A declared `FIXED` result is promoted to `NEEDS_REVIEW` when the
final confidence is low, matches are ambiguous, the fix strategy calls for
manual review, the diff falls outside the flagged region, the rule is a
`BEHAVIOR_CHANGE`, or a file carries a `MIGRATION-SKIP` marker -- `FAILED`
is never promoted or demoted.

Exit codes: `--emit-agent-tasks` returns 0 (clean), 1 (task list written
with warnings) or 3 (structural error, e.g. a bad shard plan or overlapping
shards -- nothing is written). `--record-agent-result` returns 0
(FIXED/SKIPPED/DEFERRED), 2 (FAILED), 3 (contract violation -- nothing is
written) or 4 (NEEDS_REVIEW).
