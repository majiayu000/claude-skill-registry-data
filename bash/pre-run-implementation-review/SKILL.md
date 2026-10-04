---
name: pre-run-implementation-review
description: Apply risk-based implementation checks before official research runs; require formal review only for targeted_review or full_review.
---

# Pre-run Scientific Implementation Review

## Core-only Default

PRERUN is an exception for scientific-contract risk, not a routine review stage. Ordinary
documentation, bookkeeping, tests, launch binding, monitoring, cleanup, transport, retry,
RunID/path changes, and L0-L2 implementation work do not create a PRERUN row and do not call a
reviewer. Use the smallest matching route and proceed after targeted evidence.

Only changes to model computation, data/label flow, loss, metric, checkpoint semantics,
scientific arguments, computation sinks, or result attribution use the full sequence below.
That sequence contains one smoke and one scientific review; it never expands into repeated
review, coverage review, or a closing scientific review.

## Purpose

Use this gate to catch research code that runs but implements the wrong method, carries the wrong data, or never consumes a configured value at the intended computation sink.

For GPU-reachable scientific changes, use exactly this sequence:

```text
implementation
-> local lightweight validation
-> isolated remote GPU few-step smoke
-> one scientific implementation review
-> official training/evaluation
```

GPU smoke proves runtime reachability. The scientific review proves intent, data flow, sink effect, and experiment identity. Neither substitutes for the other.

This is not TDD, per-file review, final result review, runtime orchestration review, or a prediction of whether the metric will improve.

## Risk Routing

Run `prerun_route.py` on the committed change manifest before creating review work:

```bash
python <skill-dir>/scripts/prerun_route.py <change-manifest.json>
```

- `no_prerun`: documentation, state, test-only, formatting, or other non-runtime changes. Do not create a PRERUN row.
- `micro_validation`: deterministic runtime-binding changes that preserve the scientific contract and pass production-reaching probes. Do not call a reviewer.
- `smoke_validation`: process supervision, monitoring, scheduler plumbing, cleanup ownership, or artifact transport. Verify through a real production-launcher smoke; do not call a reviewer.
- `targeted_review`: credential or destructive-lifecycle changes. Review only the adjacent safety invariant.
- `full_review`: model, attention, loss, data, metric, checkpoint, scientific args, computation sink, computing entrypoint, result attribution, dependency-closure, or unknown changes. Require current-commit smoke and one `scientific_review`.

Commit identity alone never selects a reviewer. `entrypoint` means code that computes a scientific result, not a launcher that supervises it.

## Formal Review Scope

The scientific reviewer checks only:

1. approved Spec/theory intent and explicit non-goals;
2. active canonical implementation location and actual module instantiation;
3. important values across `CLI/CSV -> argparse/config -> train/eval script -> pipeline/model/module -> forward/loss/attention/eval sink`;
4. selected blocks/layers, optimizer groups, connected losses, dtype/device behavior, and disabled paths;
5. sink effect: config presence is not evidence that computation consumes a value;
6. baseline/disable behavior and unrelated scientific routes — **when the change claims equivalence (see Baseline-Equivalence Probe), the reviewer records the probe verdict; it does not decide equivalence by reading code**;
7. dataset and label preprocessing, sampling policy, checkpoint, benchmark settings, random seed, metric computation, and result attribution;
8. exact official command and reviewed code snapshot.

Do not allow a run with "probably correct" data flow. A critical value that reaches config but not the intended forward/loss/attention/eval sink is scientifically incorrect.

## Excluded Scaffolding

Do not send these surfaces to a formal reviewer:

- rrctl, process sessions, PID/process ownership, cleanup, health polling, watchers, and schedulers;
- CSV bookkeeping, RunID/path/profile changes, coverage manifests, and frozen ExecutionPlans;
- artifact transport and closing review machinery;
- predictions about final method quality or effect size.

Validate these with smoke, ordinary tests, health checks, or artifact verification. They cannot create another scientific review.

## Pre-review Smoke

For `full_review`, the final candidate commit must pass an isolated production-reaching GPU smoke before the reviewer is called:

- 1 to 100 production steps: training steps or inference batches, with the unit and fixed input selection recorded in evidence;
- exact candidate commit and production entrypoint;
- zero exit and a numerical check matching the computation: training requires finite loss; inference requires finite model outputs;
- isolated fail-on-collision output;
- `official_metrics_disabled:true` and `artifact_ingest_disabled:true`, except the bounded Baseline-Equivalence Probe below.
- thin rrctl readiness only: candidate commit, production command, GPU/environment, isolated RunID output, 1–100 step budget, disabled official metrics/ingest, and cleanup boundary;
- no coverage manifest, reviewer packet, scientific anchors, official artifact completeness, experiment ingest, `prerun_ready.py`, or reviewer before launch;
- terminal cleanup on success, failure, and abort: delete checkpoint/optimizer/scheduler/large intermediates only within the bound smoke output root;
- retain `console.log`, `status.json`, and `smoke_summary.json`; require `checkpoint_cleanup_completed:true` and `checkpoint_paths_remaining:[]`.

The smoke object declares `computation_kind:training|inference`. Omission keeps the existing
training contract and requires `finite_loss:true`. A loss-free inference path instead records
`computation_kind:inference` and `finite_outputs:true`; omit `finite_loss` or set it to null.
Check the actual numerical model outputs before argmax, thresholding, or another operation
that can hide NaN/Inf. The evidence must identify the checked outputs and production call.
Do not invent a zero loss. Absence of a training loss does not make a GPU smoke
`not_applicable`; that disposition is reserved for code without a GPU production path.

Inference keeps `production_entrypoint_reached:true`, the bounded step budget, disabled
official metrics/ingest, isolated output, and terminal cleanup requirements. When inference
creates no checkpoints, verify the bound output root is free of checkpoint/optimizer/scheduler
and large intermediate files, then record the completed cleanup and empty remaining list.
Pretrained input weights belong outside the smoke cleanup root.

Smoke failures stay in the implementation row. Fix and rerun smoke without creating `FIX-*` or `PRERUN-REVIEW-*` rows. A smoke on an older commit cannot validate a new scientific candidate.

Local validation before smoke follows risk and affected behavior: compile affected Python files and select tests/probes that cover direct dependencies and relevant failure boundaries. Reuse successful evidence while it still covers the current code, configuration, inputs, environment, and unresolved questions; rerun affected checks when these change. Before committing, confirm that passing validation covers the staged content and test any uncovered changes. Shared-core or high-risk changes use their relevant regression set. Full-repository tests are reserved for release, breaking migration, broad shared-infrastructure changes, explicit user request, or a demonstrated gap that targeted regressions cannot cover. Test counts are not a quota; the bounded GPU smoke budget still applies.

### Baseline-Equivalence Probe

Required when the change claims any of: baseline-preserving, zero-init no-op, disabled-path equivalence, or reuse of a canonical implementation.

When scientific computation changes, bind each side to its actual implementation as well as its weights. A reference label or entry file is insufficient if it still instantiates the changed candidate; evidence must identify the reference computation actually executed.

Structural evidence does not establish equivalence. Zero residual, zero additivity, and matching counters are necessary, not sufficient: a path disabled elsewhere in the forward can still change the output while every new residual reads exactly zero.

So the claim is settled by a number, not by reading code:

- run the production entrypoint before any parameter update on one fixed evaluation setting (dataset, project parameters, fixed seed, and small fixed sample count); for inference, use the same frozen weights and bounded batches;
- compare against the named reference under the same cell and post-processing;
- record `reference_id`, `reference_weights_path`, `candidate_weights_path`, both metric values, the absolute difference, and the tolerance;
- this is the only metric a smoke may compute; it is not an official result and is never ingested.

For an equivalence claim, set `pre_review_smoke.baseline_equivalence_required:true` and attach
`baseline_equivalence_probe` in that same smoke object:

```json
{
  "reference_id": "named canonical reference",
  "reference_weights_path": "reference weights path",
  "candidate_weights_path": "candidate weights path",
  "metric_name": "metric used by the fixed comparison",
  "reference_metric": 0.25,
  "candidate_metric": 0.25,
  "absolute_difference": 0.0,
  "tolerance": 0.000001,
  "evaluation_setting": {
    "dataset": "fixed evaluation dataset",
    "parameters": {},
    "seed": 0,
    "sample_count": 1,
    "post_processing": "identical post-processing for both paths"
  },
  "evidence_paths": ["path to measured comparison evidence"]
}
```

The numbers above illustrate the schema, not a result or recommended tolerance. Choose the
tolerance from the approved numerical contract. The shared evaluation setting must apply to
both reference and candidate, and the evidence must show both production invocations.
Readiness checks finite values, the reported absolute difference, and the tolerance; a failed
or missing required probe returns to the implementation row. A supplied probe is checked even
when the requirement flag is false. Existing training packets without an equivalence claim
keep their previous contract.

Verdict feeds the `Baseline/disabled path` dimension directly:

- within tolerance -> `correct`;
- outside tolerance -> `incorrect`, and this is a blocker;
- probe not runnable -> `not_evaluable`, and the official run does not start.

`not_evaluable` is not a pass. A claim of equivalence that cannot be measured is an unverified claim.

## Lean Packet

Create one `prerun.scientific-review.v1` JSON packet containing only:

- `review_mode`: `scientific_review` or `targeted_review`;
- repository, reviewed commit, diff base, approved basis, implementation intent, and exact official command;
- passing local validations;
- current-commit `prerun.pre-review-smoke.v1` evidence for `scientific_review`;
- critical values with expected source, sink, and production-reaching evidence;
- experiment identity and output collision policy.

Project-specific evaluation dimensions belong to the experiment configuration and critical-value evidence. They are not universal required packet fields.

Run the deterministic checker once:

```bash
python <skill-dir>/scripts/prerun_ready.py <packet.json>
```

`ready:false` means the implementation row lacks reviewable evidence. Fill the reported gap and rerun readiness before creating the single PRERUN row. Readiness is not an implementation review.

The packet has no attempt, lineage, generation, resolution mode, frozen coverage, review-state, rrctl provenance, or reviewer-liveness fields.

## One Reviewer

Call one independent reviewer with only the lean packet, approved source, committed diff, and referenced evidence.

<!-- reviewer-launcher:start -->
Write the complete review task to a file, then run the project-owned persistent reviewer job. It uses a fixed read-only Pi session, resumes that same session across transport failures, and writes the only accepted verdict artifact:

```bash
python .agents/harness/reviewer_job.py \
  --backend pi \
  --packet <packet.json> \
  --task <review-task.md> \
  --job-dir <mission-dir>/reviews/<prerun-row>
# 模型不在命令行复述：runner 按 --backend 取 review_model.review_job_model(<backend>)；切换模型只改 review_contract.toml
```

Do not use `pi-sub-agent --no-session`, parallel/chain mode, or another one-shot child for this gate.
<!-- reviewer-launcher:end -->

Do not send the main conversation or the main agent's conclusions.

The reviewer must inspect the committed code and return all currently evaluable scientific findings in one response. Its result is exactly one of:

- `scientifically_correct`: implementation, scientific data flow, sink effect, and experiment identity are correct; allow official run.
- `scientifically_incorrect`: one or more reproducible scientific correctness blockers exist; do not run until fixed.
- `not_evaluable`: name the exact missing scientific evidence; do not infer correctness from smoke or scaffolding.

Treat quota errors, launcher failures, and silence before any scientific verdict as review-service failures. A `running` status alone is not evidence of progress. Let `reviewer_job.py` resume the recorded session first; transport resumes of that same session are not replacements and do not create another scientific opinion. Only after bounded same-session recovery is exhausted may the runner create a fresh independent execution, with the default maximum of one replacement. Keep the candidate commit, evidence, review scope, and single PRERUN row unchanged. Continue within existing task authorization.

Reviewer job lifecycle operations:

- Ownership comes from the job's lock, not from a process-name match. `reviewer_job.py` takes an exclusive `flock` on `<job-dir>/job.lock`, so a second runner fails with `reviewer job is already running`; establish ownership from that lock plus the recorded job inputs (`job.json` backend / packet / task identity) before terminating anything. Never use a fuzzy `pkill -f reviewer_job`: the Executor's own shell command line contains the same string, so the pattern also kills the Executor shell.
- To recover a job you have established ownership of, terminate that exact PID and rerun the same `reviewer_job.py` command. The runner then sees the recorded `running` state while no reviewer transport child is running under its own PID, records `service_failed`, and resumes the recorded session instead of creating a second scientific opinion. Transport children orphaned by the killed runner are not visible to the new runner; confirm them manually with `pgrep`/`ps`. Where the process table is unavailable the runner conservatively treats the job as alive and the bounded attempt timeout ends the attempt instead.
- Keep the candidate commit, evidence, review scope and the single PRERUN row unchanged through recovery.

This replaces a failed execution of the same review; it does not request another scientific opinion. A returned scientific verdict, including `not_evaluable`, ends service recovery and must be handled on its merits. Formatting problems in an available verdict can be normalized without repeating the review. If the replacement also fails, record the capability gap once and continue independent work; do not loop, infer a pass, or weaken the scientific gate. Any user-authorized exception belongs in the project's run record, with the unfulfilled review requirement stated explicitly.

The review gate accepts only `verdict.json` with schema `prerun.scientific-verdict.v1`. Its packet, task, raw-response digests, candidate commit, review mode, result, and reviewer id must validate. Record its repository-relative path as `verdict_artifact:<path>` and in `gate_provenance.verdict_artifact`; reviewer prose or a process exit code alone cannot open the gate.

A verdict written by `reviewer_job.py` also records `requested_model` and an event-stream `observed_model`, and RunSpec construction checks both with the shared validator in `.agents/harness/review_model.py`: an `observed_model` of `unknown` is rejected as unverifiable, any other recorded identity must match a model approved for a configured host, and verdicts that record no model fields stay accepted for backward compatibility. The approved identity for each host lives only in `review_model.py`, which is the single place to change it.

For the codex backend, the runner extracts `observed_model` from the stdout event stream first; when the stream records no model (codex 0.155.x `exec --json`), it falls back to the runtime rollout session file under `$CODEX_HOME/sessions` (default `~/.codex/sessions`) located by the recorded `thread_id`, whose `turn_context` payload carries the effective model. The reviewer's own message text is never parsed for identity.

## Blocker Repair

When the result is `scientifically_incorrect`:

1. keep the official run blocked;
2. repair all listed blockers in the original implementation row;
3. run a production-reaching probe for each affected source-to-sink path;
4. rerun GPU smoke when scientific code, data flow, or a sink changed;
5. have the main agent record blocker-to-fix-to-evidence closure;
6. proceed when every blocker has reproducible closure evidence.

Do not create a second formal reviewer, Attempt 2, resolution review, new lineage, new generation, or closing scientific review. If the main agent cannot verify closure, record `validation_gap` and stop the run rather than substituting runtime-management evidence.

## Output Format

```markdown
## PRERUN-REVIEW-N
- Review mode: scientific_review | targeted_review
- Reviewer: <id and independent mode>
- Result: scientifically_correct | scientifically_incorrect | not_evaluable
- Decision: allow_run | do_not_run
- Gated run: <row or command>
- Code snapshot: <branch>/<pre_run_code_commit>
- Approved basis: <Spec/requirement>
- Intent alignment: correct | incorrect | not_evaluable
- Canonical code location: correct | incorrect | not_evaluable
- Critical data flow: correct | incorrect | not_evaluable
- Computation sink effect: correct | incorrect | not_evaluable
- Runtime scientific state: correct | incorrect | not_evaluable
- Baseline/disabled path: correct | incorrect | not_applicable | not_evaluable  (equivalence claims: cite the Baseline-Equivalence Probe, never a code reading)
- Experiment identity: correct | incorrect | not_evaluable
- Local validation: <commands and literal outcomes>
- GPU smoke: <RunID, command, steps, result, evidence>
- Blockers: <none or source/evidence/why/fix target>
- Validation gaps: <none or exact missing evidence>
```

Write `pre_run_result:pass` only for `scientifically_correct` or after every reported blocker has been fixed and closed with production/sink evidence. The recorded `pre_run_code_commit` is the code used for the official run, not the CSV's eventual final commit.

## Compatibility

New actionable work uses only this single-review protocol. Attempt, lineage, generation, resolution mode, frozen coverage, review-state and reviewer-liveness fields are invalid inputs and have no executable helper path.
