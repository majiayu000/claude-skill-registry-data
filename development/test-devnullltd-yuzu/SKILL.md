---
name: test
description: Run or plan Yuzu's `/test` pre-commit and pre-push validation pipeline with quick, default, full, instructions, and quarantine modes. Use when the user says `/test`, `/test --quick`, `/test --full`, asks for the full test gate, or needs the Yuzu test-runs DB workflow.
---

# Test

Use this skill for the high-level Yuzu validation pipeline. Route low-level build choices through `$yuzu-build`, Windows through `$yuzu-windows-msvc`, and Erlang caveats through the gateway guidance below.

## Modes

- default: build, upgrade test, live UAT, standard gates. About 30-45 minutes.
- `--quick`: build plus offline C++ unit, EUnit, and Dialyzer. No live stack, no synthetic UAT.
- `--full`: default plus OTA stubs/flows, sanitizer dispatch, coverage, and perf measurement. About 60-120 minutes.
- `--instructions`: live-stack instruction definition suite only.
- `--instructions-quarantine`: local quarantine ceremony only. Do not run on remote or SSH-only hosts.
- `--force-cleanup`: clean this run's dangling containers before start.
- `--keep-stack`: leave debug stacks running when the script supports it.

## Run State

Every local `/test` pipeline run records gate results and timings in
`~/.local/share/yuzu/test-runs.db`, overrideable with `YUZU_TEST_DB`. Query with:

```bash
bash scripts/test/test-db-query.sh --latest
bash scripts/test/test-db-query.sh --last 5
bash scripts/test/test-db-query.sh --diff RUN_A RUN_B
bash scripts/test/test-db-query.sh --trend timing=phase7.perf
bash scripts/test/test-db-query.sh --flaky
```

The self-hosted CI pools also keep a **persistent database per runner agent**;
they do not share one host-wide SQLite file:

- Big Tam: `/srv/ci/work-N/_tool/yuzu-test-runs/yuzu-bigtam-linux-N/test-runs.db`
- Wee Tam: `D:\ci\test-runs\yuzu-weetam-windows-N\test-runs.db`

`ci.yml`'s Linux and Windows jobs initialize and write these databases
automatically. Schema v3 preserves GitHub rerun attempts separately and stores
job outcome/duration, platform, runner, commit/branch/event, ccache hit ratio,
Meson suite result/duration/timeout, and recovered known-flake events. Query one
on its host by setting `YUZU_TEST_DB`, for example:

```bash
YUZU_TEST_DB=/path/to/runner/test-runs.db \
  bash scripts/test/test-db-query.sh ci-stats --since 30d
YUZU_TEST_DB=/path/to/runner/test-runs.db \
  bash scripts/test/test-db-query.sh ci-suite-stats --since 30d
YUZU_TEST_DB=/path/to/runner/test-runs.db \
  bash scripts/test/test-db-query.sh ci-flakes --since 30d
```

Provision/repair paths are `deploy/linux/Provision-BigTam-Runner-Telemetry.sh`
and `deploy/windows/Provision-Windows-Runner.ps1`. GitHub-hosted macOS runners
are ephemeral and therefore cannot satisfy the runner-local persistence
contract; their Meson logs remain Actions artifacts. `ci-ingest` is a coarse
workflow-level backfill for older GitHub history, not a replacement for direct
runner recording.

`tests/known-flaky.json` remains the reviewed allowlist. A listed case only
passes CI if an isolated retry recovers; each recovery is also persisted in
`ci_flake_events` so recurrence can be measured instead of inferred from logs.

Initialize each manual orchestration with a `RUN_ID`, `TEST_DIR=/tmp/yuzu-test-$RUN_ID`, `LOG_DIR=$HOME/.local/share/yuzu/test-runs/$RUN_ID`, `COMMIT`, `BRANCH`, and `BUILDDIR=$(build_dir)` from `scripts/test/_portable.sh`. Record gates with `scripts/test/test-db-write.sh`.

## Phase Order

Wall-clock order is fixed:

1. Phase 0 preflight: `bash scripts/test/preflight.sh` or `--force-cleanup`.
2. Phase 1 build HEAD: Meson compile, Erlang `rebar3 as prod release`, and docker images except in quick mode.
3. Phase 2 upgrade test: `bash scripts/test/test-upgrade-stack.sh ...`; skipped in quick mode.
4. Phase 3 OTA: full mode only; may record SKIP if still stubbed.
5. Phase 7a perf: full mode only, before UAT stack; measure-and-report only.
6. Phase 4 fresh stack: `bash scripts/start-UAT.sh`; skipped in quick mode.
7. Phase 5 gates: unit, EUnit, Dialyzer, CT, integration/e2e/synthetic UAT/puppeteer/instructions as applicable. Security E2E runs after the parallel fan-out, alone (its rate-limit probe empties the shared login bucket). Puppeteer records SKIP when `tests/puppeteer/node_modules` is absent.
8. Phase 6 sanitizers: full mode only, dispatched runner.
9. Phase 7b coverage: full mode only, enforces `tests/coverage-baseline.json`.
10. Phase 8 teardown and summary.

Phase 1 is mandatory-blocking. Other phases should normally continue so the operator gets one prioritized report.

## UAT Lifetime Rule

Phase 8 must not stop the native UAT stack from `scripts/start-UAT.sh`. A successful default/full run intentionally leaves a working stack at tested HEAD for human inspection. Only stop it if the user explicitly asks.

## Erlang Gateway Rules

- Source `scripts/ensure-erlang.sh` before direct `rebar3` work, then verify `command -v erl`.
- For EUnit, use `rebar3 eunit --dir apps/yuzu_gw/test`; the `--dir` flag is mandatory.
- Do not treat `rebar3 eunit --module X` as isolated; it runs after the full `--dir` phase in the same VM.
- In parallel test fanout, use separate `REBAR_BASE_DIR` values for EUnit and CT to avoid `_build` races.
- Always run Dialyzer after Erlang changes.

## Perf Status

Perf is measure-only as of 2026-05-03. `scripts/test/perf-gate.sh` records metrics and exits PASS; humans inspect trend and distribution shape using the test-runs DB and `docs/perf-baseline-calibration-2026-05-03.md`.

## Mode Shortcuts

For `--quick`, resolve the build directory and run only compile plus offline suites. Do not start UAT and do not invoke synthetic UAT.

For `--instructions`, use `scripts/test/instructions-tests.sh` after bringing up only the required live stack.

For `--instructions-quarantine`, use `scripts/test/instructions-quarantine.sh` only on a local machine where temporary self-disconnect is acceptable.
