---
name: kelly-local-model-lab
description: Curate Busabase training examples, create immutable dataset snapshots, run reproducible LoRA or QLoRA fine-tunes on a local Apple Silicon Mac with MLX-LM, compare the untouched baseline and adapter on locked evaluations, and register approved adapters. Use when the user wants to train, fine-tune, evaluate, compare, promote, or manage a local language model with Busabase as the workflow source of truth. Do not use for RAG-only knowledge retrieval, cloud training, or training a foundation model from scratch.
license: MIT
metadata:
  category: platform
  tags:
    - risk:local-write
    - surface:busabase
  busabase:
    template: true
    folderSlug: kelly-local-model-lab
    resources:
      - training-examples
      - training-runs
      - evaluations
      - model-registry
      - settings
    risk: local-write
---

# Kelly Local Model Lab

Use Busabase as the durable data and control plane while a trusted local Worker
performs compute on Apple Silicon. Fine-tuning changes behavior; it is not a
replacement for RAG when the goal is to inject current knowledge.

## Mandatory Dependencies

Before creating, provisioning, or changing the AirApp, read and follow:

1. `$kelly-app-skill-creator` for product behavior and UI quality;
2. `$busabase` for Space selection, node discovery, ChangeRequests, and trusted writes;
3. `$busabase-app-creator` for AirApp runtime, SDK, security, validation, and deployment;
4. `$kelly-app-skill-creator-tests` before claiming full conformance.

If a dependency is unavailable, keep the canonical local artifact and training
pipeline intact, stop before the unavailable Busabase operation, and report the
missing dependency. Never replace Busabase with SQLite, local JSON, or another
persistent workflow backend.

## Operating Boundary

- The AirApp reviews examples, runs, evaluations, and registered adapters. It
  never launches MLX, reads local model files, or performs training itself.
- A trusted local Agent/Worker claims one eligible `training-runs` record,
  downloads its immutable Drive snapshot, trains locally, writes heartbeats,
  uploads the adapter and report, and then marks the run terminal.
- Busabase Base records hold structured state and provenance. Drive/File holds
  dataset snapshots, adapters, reports, and model cards. Vault holds only named
  credential requirements; values never enter the browser.
- Base-model caches are disposable local compute caches. They are not canonical
  workflow state and need not be uploaded to Busabase.
- A deployed AirApp cannot call the Mac's `localhost`. Inference or training
  requests cross the same reviewed Busabase job boundary.

Read [references/lab-schema.md](references/lab-schema.md) before operating on
resources, exporting data, claiming work, evaluating, or registering an adapter.

## Default Experiment

For a first Apple Silicon validation, use:

- base model: `mlx-community/Qwen3-0.6B-4bit` for a fast smoke run;
- method: QLoRA through MLX-LM;
- task: short App-in-Skill brief to strict `app_spec` JSON;
- metrics: JSON validity, schema validity, exact-field accuracy, and latency;
- output: a LoRA adapter, never a rewritten foundation checkpoint.

For customer-support training, use task `support_qa`. Approved QA pairs from
`$kelly-support` cross the trusted bridge into `training-examples` with their
source article and pair ids, but return to `needs_review` before they can enter
a snapshot. The evaluator reports normalized exact-answer match and Unicode
character F1 instead of the `app_spec` JSON/schema metrics.

Treat the bundled `training/fixture/` data as a pipeline smoke fixture only. It
never impersonates reviewed Busabase data. Production experiments must carry a
Drive snapshot reference and SHA-256 hash on the run record.

## Workflow

1. Inspect runtime readiness, the explicit Space, resource versions, and local
   Worker readiness. Do not read or mutate app resources before Space selection.
2. Review examples individually. Use `approve`, `request_changes`, or `block`;
   preserve the note, reviewer, timestamp, source, and content hash.
3. Export only approved examples. Split by source or another leakage-resistant
   grouping, write `train.jsonl`, `valid.jsonl`, and locked `test.jsonl`, upload
   one immutable snapshot to Drive, and record its SHA-256 digest.
4. Create a `ready` training run containing the exact base model and revision,
   method, snapshot reference/hash, and config. Never train from a mutable live
   query whose contents cannot be reproduced.
5. Claim the run atomically. Record claimant, attempt, claimed time, and
   heartbeat. Re-read eligibility before starting MLX.
6. Evaluate the untouched base model first, train the adapter, then evaluate the
   adapter on the identical locked test file and decoding settings.
7. Upload the adapter, full evaluation report, and model card. Record terminal
   status and sanitized errors. Do not mark a run done merely because MLX exited.
8. Let a human choose `promote`, `hold`, or `reject` on the adapter evaluation.
   Promotion creates or updates a model-registry candidate/active record with
   base revision, dataset hash, run id, and artifact reference.

## Local Smoke Command

Use an isolated virtual environment. The installed MLX-LM version must be pinned
in `requirements-mlx.txt` before a result is treated as reproducible.

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-mlx.txt
.venv/bin/python scripts/mlx_smoke.py
```

Support QA handoff and training:

```bash
pnpm sync:support-qa
pnpm sync:support-qa -- --apply
.venv/bin/python scripts/mlx_smoke.py --task support_qa --data <snapshot-directory>
```

The bridge groups split assignment by source article so QA from one material
cannot leak across train and locked test. A single source can populate a review
queue, but it is not sufficient evidence for model promotion; collect at least
three independent source groups and keep one or more groups locked for testing.

Outputs go under the ignored `.cache/smoke-run/` directory. The script validates
the fixture, hashes all splits, records the exact package version and command,
evaluates the baseline, trains, evaluates the adapter, and writes `report.json`.

## UI

- `#/overview`: readiness, approved split counts, active runs, candidate adapters,
  pipeline stages, latest baseline/adapter delta, and recent runs.
- `#/examples[/<id>]`: desktop list/detail review queue and separate phone list
  and detail panes with stable example ids and review actions.
- `#/runs`: base model, method, claim/status, heartbeat, artifacts, and failures.
- `#/evaluations`: locked baseline/adapter comparisons and promotion verdicts.
- `#/registry`: active, candidate, and retired adapters with complete lineage.
- `#/settings`: responsive Help & Settings modal with guide, resources, and
  sanitized training configuration.

Demo mode is explicit and in-memory only. `?demo=1` opens the overview;
`?demo=dataset`, `?demo=evaluations`, and `?demo=registry` open named screenshot
scenes. `lang=en` or `lang=zh` forces the UI language. Demo never claims a real
connection, writes Busabase, or proves the local Worker is online.

## Completion

Do not claim a production fine-tune until:

- the snapshot came from reviewed Busabase examples and has a stable Drive ref/hash;
- the base model revision, MLX-LM version, command, and config are recorded;
- baseline and adapter used the same locked cases and decoding settings;
- adapter artifacts and reports exist and are referenced by a terminal run;
- the human promotion verdict is recorded against the evaluated version;
- app checks, local/OSS conformance, responsive browser checks, and available
  Cloud/AirApp suites passed or are explicitly reported as skipped.

Stop when the Space or dataset is ambiguous, examples lack review/provenance,
the run changed after claim, test leakage is detected, the model license is
incompatible, an artifact hash fails, or a secret would cross into the browser.
