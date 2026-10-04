---
name: pyfixest-grid-sharding
description: |
  Diagnose and fix slow pyfixest regression GRIDS (many feols/fepois calls run
  sequentially) that stay slow despite demeaner_backend="cupy64" and an idle
  GPU. Use when: (1) a script looping dozens of pf.feols models on a 100k+ row
  panel takes ~1 min/model, (2) process inspection shows ~1-1.5 cores busy and
  nvidia-smi shows ~0% GPU utilization with a resident cupy context, (3)
  planning any worker prompt that will run a model grid (robustness variants x
  FE structures x domains). Root cause: per-model CPU-side single-threaded
  fixed costs (formulaic model-matrix build, interaction construction,
  singleton detection, cluster vcov) dominate wall time; GPU demeaning is a
  small slice. Fix: shard the model grid across OS processes and/or use
  pyfixest multiple-estimation syntax; mandate this IN THE WORKER PROMPT.
author: Claude Code
version: 1.0.0
date: 2026-07-21
---

# pyfixest Grid Sharding

## Problem

A regression grid (e.g. 2 measures x 3 FE structures x pooled+per-domain x 3
label variants ~ 70 models) on a 327k-row panel with high-cardinality director
FE ran ~55 s/model sequentially — ~65 min wall — on an RTX 5080 machine with
`demeaner_backend="cupy64"` on every call. The GPU was NOT the bottleneck.

## Context / Trigger Conditions

- Measured signature (verified 2026-07-21, H5 seat-loss rerun): job process at
  ~1.4 cores CPU (37.7 CPU-min in 27 wall-min), `nvidia-smi` 0% utilization
  with ~4 GB resident (cupy context loaded, idle), one pyfixest singleton
  warning per completed model ticking by in the log.
- Any orchestration prompt that asks a worker to "rerun every headline cell
  under variants A/B/C" without specifying execution structure.

## Solution

1. Diagnose before blaming the GPU: check process CPU-minutes vs wall-clock
   (~1 core => serial CPU-bound) and GPU utilization (near 0% => demeaning is
   not the constraint). The cupy64 kwarg is still correct; it just cannot fix
   a CPU-dominated pipeline.
2. Shard the GRID, not the data: split the model list across N OS processes
   (`--shard i --nshards N` over the model index, one output part-file each,
   merge step at the end), N ~ cores-4. Models are independent — this is the
   Execution Style process-sharding pattern applied to regressions.
3. Amortize fixed costs inside a shard: build the panel/interactions ONCE per
   variant and reuse; where specs share RHS/FE, use pyfixest multiple-
   estimation syntax (multiple depvars / sw()/csw() stepwise) so one model
   matrix serves several reported cells.
4. Orchestrator rule: put the sharding mandate IN the worker prompt for any
   grid larger than ~10 models. Workers default to sequential loops otherwise.
5. Mid-flight call: if a sequential grid is already >1/3 done with no
   per-model checkpoint, let it finish — restart+shard usually nets slower.
   Grids launched fresh should checkpoint per model (append-only part file) so
   this trade-off never binds again.

## Verification

Sharded reruns of the same grid should show near-linear speedup up to
memory/RAM limits; per-model results must be byte-identical to the sequential
run (same seeds not needed — feols is deterministic).

## Measured GPU-saturation verdict (2026-07-21 escalation experiment)

A controlled escalation loop (same 327k-row seat-loss grid, N concurrent OS
shard processes, nvidia-smi sampled every 2 s, RTX 5080) settled the question
empirically: mean GPU utilization was **0.7% at N=4, 0.6% at N=8, and ~1% at
N=12** (peaks 2-5%), with total VRAM flat around 4 GB. GPU saturation is
UNATTAINABLE for pyfixest cupy64 grids — the demeaning kernel is a brief burst
inside a CPU-bound per-model pipeline — so the correct objective is CPU-core
saturation via process shards, with cupy64 kept on per project rules. Two
further measured costs: (1) kill-and-escalate restarting loses in-flight fits
(throughput FELL from 1.29 to 0.64 fits/min when escalating 4->8 mid-run) — pick
N once from cores and RAM, do not escalate live; (2) each shard holds the panel
in RAM (~1.2 GB for a 327k-row panel; scale linearly), so cap N by free RAM
before cores. Evidence: `.claude-local\specialist-directors-us\
classifier_aug_2026-07-21\stageB_v2\h5_seatloss_gpu\attempts.json`.

## Notes

- VRAM: N concurrent cupy64 processes each hold a context (~4 GB observed on
  a 327k x 40k-FE problem); on a 16 GB card cap GPU-sharing shards at ~3 or
  run overflow shards with the numba default (flag them per project rules).
- See also: [pyfixest-cupy64-absorbed-regressors] (numerical differences of
  the cupy backend — unrelated to speed), and the global CLAUDE.md Execution
  Style section (process-level parallelism; GIL makes threads useless here).
