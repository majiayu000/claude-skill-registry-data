---
name: layer-autoresearch
description: Contributor-only autonomous keep/discard experiment loop (after karpathy/autoresearch) that edits Flisk's L1-L4 Docker layer generators in a flisk checkout and keeps only changes that lower idle memory per service, toward 100 services on a 16 GB machine. Use when asked to run autoresearch on the Docker layers or to optimise the golden/runtime layers experimentally. To only measure a stack, use flisk-benchmark.
license: MIT
compatibility: Contributor skill. Requires a flisk checkout, Docker and git. Does not deploy.
metadata:
  author: flisk-sh
  version: "1.0"
---

# Layer autoresearch

Adapted from karpathy/autoresearch `program.md`. You are an autonomous researcher making the Flisk runtime layers cheaper **without removing features**.

## Setup (with the user, once)

1. Agree a run tag (e.g. `sep25`). Create `git checkout -b autoresearch/<tag>` from `main`. The branch must be new.
2. Ask the user whether any tool auto-commits or pushes working-tree edits in this checkout. If one does, ask them to pause it for the run (or run from a separate `git worktree`), because experiment commits and resets must not reach `origin/main`.
3. Read the in-scope files in full:
   - Editable: `runtime/engine/topologies/platform/docker/layers/*.star`, `runtime/engine/topologies/platform/docker/layers/prisma/*.star`, `runtime/engine/topologies/platform/docker/build/golden_image_dockerfile.star`, `runtime/engine/topologies/platform/docker/config/healthcheck.star`.
   - Read-only ground truth: `scripts/autoresearch/layer-eval.sh`, `scripts/benchmark/container-scale.ts`, `tests/tilt-engine/test_runtime_container_footprint.py`, and any spec for the runtime container footprint under `openspec/`.
4. The eval needs a Flisk project with at least `LAYER_EVAL_SAMPLE` (default 20) services. It uses `FLISK_BENCH_PROJECT`, or `../flisk-erp-system` next to the checkout when that is unset. If neither exists, ask the user to clone the ERP scale-test project (about 100 services) once with `flisk project erp --path ../flisk-erp-system` (the eval generates and builds what it needs; do not start all of it with `flisk up`), or to point `FLISK_BENCH_PROJECT` at another large project.
5. Create an untracked `autoresearch-results.tsv` with the header `commit	mem_mib	image_mib	status	description`.
6. Confirm with the user, then start.

## Experiment

Run `scripts/autoresearch/layer-eval.sh > run.log 2>&1` (about 5-10 minutes). Read the results with `grep -A20 '^---' run.log`.

- **Primary metric: `mem_per_service_mib`, lower is better.** This is idle memory per real service in the bench project, and it is what limits 100 services on 16 GB.
- **Tie-breaker:** if memory is within 0.5 MiB of the best, a lower `unique_per_service_mib` or `service_image_mib` wins, then simpler code.
- **Hard constraints.** `status: ok` requires all 20 services healthy, zero crashes, and passing feature tests. Anything else is a discard, or a crash if it didn't run.
- **Never** edit the eval harness, benchmark, tests or spec. Never remove a user-facing feature: Prisma, Infisical entrypoint, hugo-as-feature, healthchecks, signal handling. Don't add dependencies.

Candidate ideas from earlier measurements (re-measure before relying on them):
- Duplicate `node_modules` copy in the L4 backend runtime (4.2 MB twice per service).
- L1 installs `file`, `bash` and `openssl` into every runtime image (30 MB apk layer). Check what actually needs them first.
- Bun runtime memory flags (e.g. `--smol`) in the resolved `CMD`.
- Distroless or slimmer Bun base for L4.
- Per-service unique layer size.

## Loop (never stop until the human interrupts)

1. Note the current commit.
2. Change the editable files with one idea.
3. `git commit -m "<idea>"`.
4. Run the eval, redirected to `run.log` (don't flood context).
5. If there's no `---` block, `tail -n 50 run.log`. Fix trivial mistakes, otherwise log `crash`.
6. Append a row to `autoresearch-results.tsv` (untracked).
7. If the metric improved and `status: ok`, keep the commit. Otherwise `git reset --hard HEAD~1`.
8. An eval that runs longer than 20 minutes counts as a failure.

The first run is always the unmodified baseline.
