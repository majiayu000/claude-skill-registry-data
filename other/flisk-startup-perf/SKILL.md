---
name: flisk-startup-perf
description: Finds out where a Flisk start (flisk up or the one-command flisk demo) spends its time, tells a slow start from a stuck one, and guides a fix with before and after numbers. Use when a user says the demo or flisk up is slow, hangs on "Starting services", or asks to speed up startup, image builds or the first run.
license: MIT
compatibility: Needs the flisk CLI, Docker, Tilt and Node 22+. Analysis of a saved Tilt JSON needs only Node.
metadata:
  author: flisk-sh
  version: "1.0"
---

# Flisk startup performance

The demo is P1 (`AGENTS.md`), so a slow or hung start outranks other work. Measure first; change one thing; measure again.

## 1. Slow or stuck?

Most "slow" reports are stuck starts. Run the analysis against the project's Tilt (the port is in the `flisk up` output; the default is 10350, and another project may have moved it):

```bash
node scripts/benchmark/startup-analysis.mjs --port <tilt port>
```

- `FAILED: <resource>` plus "can never start" means stuck. The count of "building" services in the demo frame includes services waiting on a failed resource. Read that resource's log (`tilt --port <p> logs <resource>`) and fix the cause. Known causes: `init-networks` with `all predefined address pools have been fully subnetted` (Docker out of network ranges; `flisk doctor --fix --scope=machine`), a held host port, Docker not running.
- No failure: it is slow. Go to step 2.

Also check that the command ran the version you think: `npx` prefers a `node_modules/.bin/flisk` in the current folder or any parent over the registry. A stale install in `~` hides every fix. `ls ~/node_modules/@flisk-sh/flisk/package.json`.

## 2. Where did the time go

The analysis prints wall time, parallelism (sum of build times over wall time; about 1 means one build did all the work) and idle time. Then:

- One long build with parallelism near 1: read its log. For `golden-layers-build`, find the slow step: `tilt --port <p> logs golden-layers-build | grep -E '^#[0-9]+ DONE [0-9.]+s' | sort -t' ' -k3 -rn | head`. An `exporting to image` step of 100 s or more points at the Docker store or too many parallel builds, not at the Dockerfile.
- Many builds, parallelism at the Tilt limit: raise `FLISK_MAX_PARALLEL_BUILDS` (default is from the engine's CPUs and memory, minimum 3, maximum 8, see `runtime/engine/topologies/tilt/resources/build_concurrency.star`). Check `docker info` for CPUs and memory first.
- Idle time: something waits on a serial step. `scripts/benchmark/tilt-build-durations.mjs` lists the order.

Reference from a real run (4 CPU / 7.7 GB Docker, 2026-10-31): `golden-layers-build` took 167 s of a 177 s start with parallelism 1x. 102 s of it was the `exporting to image` step of `l3-backend`, and all 8 golden images are built even though a project may use fewer. Skipping unused golden targets is the next candidate; it needs a layer-usage check per project so no service loses its base image, and a cold run on healthy Docker to prove it.

## 3. Compare cold and warm

Cold means no golden images and no layer cache. The demo is cold for every new user, so cold is the number that matters. `scripts/benchmark/flisk-up-warm-start.sh` runs cold and warm rounds and writes `summary.md`.

## 4. Change and prove

1. Write the number down before the change (wall, slowest resource).
2. Make one change. Prefer work that is skipped (do not build targets the project does not use) over work that is faster.
3. Add a test for the behaviour. A Starlark change needs a test in `cli/src/utils/__tests__` or `tests/`; the demo flow is covered by `tests/e2e/journeys/demo` (it runs twice; keep it passing).
4. Rerun cold and write both numbers in the PR.

Do not claim a speed-up from a run on a machine whose Docker is unhealthy (`docker images` erroring, containers `unhealthy`, no free network ranges): fix the machine first or the numbers mean nothing.
