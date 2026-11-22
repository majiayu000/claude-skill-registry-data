---
name: test
description: Run the Yuzu pre-commit/pre-push test pipeline. Compiles HEAD, stands up the previous release, upgrades it, runs the full standard test surface, records every result + sub-step timing into a durable SQLite test-runs DB. Use when the user says "/test" or asks to run the full test pipeline before commit.
---

# test

Runbook for the Yuzu `/test` pipeline. This skill is a **bash-first orchestrator**, not an agent fan-out. Each phase is one or more shell invocations the LLM executes via the `Bash` tool. The LLM's job is to interpret failures, decide whether to continue, and produce the consolidated report at the end. Every gate result + sub-step timing lands in `~/.local/share/yuzu/test-runs.db` so the operator can compare runs over time.

## Usage

```
/test                  — default mode (~30-45 min): build + upgrade test + standard gates
/test --quick          — sanity check (~10 min): build + unit + EUnit + dialyzer (no live stack)
/test --full           — pre-tag (~60-120 min): adds OTA, sanitizers, perf measurement, coverage enforce
/test --instructions   — content-suite gate (~5-15 min): exercises the safe + mutating
                         InstructionDefinitions (the runner prints the count) against a live UAT stack via REST.
                         Standalone: brings up Phase 4 stack + the new Phase 5 instructions gate
                         only. Skips build/upgrade/sanitizers/coverage. Use when content
                         changes (yaml under `content/definitions/`) or after touching the
                         instruction-engine dispatch path.
/test --instructions-quarantine
                       — quarantine ceremony (~30-40s): exercises the security.quarantine
                         cluster (isolate / release / status / whitelist) with the
                         self-disconnect/auto-resume dance. DO NOT RUN ON A REMOTE / SSH-ONLY
                         HOST — see safety section below. Destructive and forensic
                         InstructionDefinitions are never run by /test; drive the runner by
                         hand (see "`--instructions` mode" below).
/test --force-cleanup  — tear down THIS RUN's dangling test containers before starting
/test --keep-stack     — leave docker stacks running after the run (debugging)
```

Modes are layered: `--full` includes everything `default` runs, `default` includes everything `--quick` runs. The most common invocation is bare `/test` before `git push`.

**`--quick` does NOT include synthetic UAT or any other test that needs a live stack.** Quick mode is build + offline unit/EUnit/dialyzer only — there is no Phase 4 stack stand-up in quick mode, so no Phase 5 gate that requires HTTP to a live server. If you need stack-level confidence, use default mode.

## Cross-platform support

The skill runs on both **Linux** (CI, WSL2) and **macOS** (operator dev box). The orchestration prefers a single OS-aware script per concern over OS-specific forks:

- Build dir is `build-linux` on Linux, `build-macos` on macOS — `scripts/setup.sh` auto-picks. The skill computes `BUILDDIR=build-$(host_os)` (with `darwin → macos`) via `scripts/test/_portable.sh` and uses `$BUILDDIR` everywhere.
- Stack stand-up (Phase 4) calls `scripts/start-UAT.sh` — cross-platform; the historical `start-UAT.sh` name is a back-compat shim.
- Port checks, disk-free, loadavg/CPU/mem fingerprints all go through `scripts/test/_portable.sh` (lsof + sysctl on macOS, ss + /proc on Linux).

**Security E2E prerequisite:** curl >= 7.68 (>= 7.84 for the Retry-After check; an older curl skips that one assertion, below 7.68 the gate fails with an explicit message).

**macOS prerequisites:** GNU bash 5+ (`brew install bash` — stock /bin/bash 3.2 doesn't support `mapfile`/`declare -A`), kerl-installed Erlang, vcpkg with `VCPKG_ROOT` set, OrbStack or Docker Desktop installed (and launched once so its CLI symlinks populate `~/.orbstack/bin`).

**What skips on macOS without a running Docker daemon:**
- Phase 1 docker-image-build → SKIP (operator can build locally only what they need)
- Phase 2 upgrade-test → SKIP via `test-upgrade-stack.sh`'s `docker_available` early-out, gate row records SKIP with operator-readable note
- Phase 6 sanitizers → still dispatches to the `yuzu-bigtam-linux` self-hosted pool, unaffected by local Docker availability

Everything else (Phase 0 preflight, Phase 1 C++ + Erlang build, Phase 4 native stack, Phase 5 unit/EUnit/dialyzer/CT/integration/e2e/synthetic-UAT/puppeteer, Phase 7a perf, Phase 8 teardown) runs natively on macOS. Phase 7b coverage is Linux-only: on macOS the gate refuses with a WARN row (#6187).

## Workflow summary

```
Phase 0 — Preflight             (toolchains, ports, disk, docker, init DB)
Phase 1 — Build HEAD            (meson + rebar3 + docker build local :test images)
Phase 2 — Upgrade Test          (latest release → HEAD: fixtures, migrate, verify)
Phase 3 — OTA Agent Test        (--full only — Linux + Windows self-exec)
Phase 7a — Perf gate            (--full only — runs HERE on a quiet box,
                                 BEFORE Phase 4 brings up the UAT stack;
                                 perf is fully self-contained and contention-
                                 sensitive, so it must measure with no other
                                 yuzu processes running)
Phase 4 — Fresh Stack Stand-up  (full-uat at HEAD + native agent — STAYS UP
                                 through Phase 8 so humans can poke at the
                                 stack before /release)
Phase 5 — Test Gates (parallel) (unit / EUnit / dialyzer / CT / integration /
                                 e2e-api / e2e-mcp / synthetic UAT /
                                 puppeteer / instructions; e2e-security runs
                                 alone after the fan-out)
Phase 6 — Sanitizers            (--full only — dispatched to yuzu-bigtam-linux pool)
Phase 7b — Coverage             (--full only — enforces tests/coverage-baseline.json)
Phase 8 — Teardown + Summary    (cleans Phase 2 compose projects + scratch dir,
                                 finalises run row; LEAVES THE UAT ALIVE on
                                 purpose — do NOT call start-UAT.sh stop)
```

**Wall-clock order: 0, 1, 2, 3, 7a-perf, 4, 5, 6, 7b-coverage, 8.** Perf is intentionally pulled forward of Phase 4 because it has no functional dependency on the UAT stack (every upstream RPC is meck'd inside the suite, gateway components run in-process) but its measurements are extremely sensitive to CPU/scheduler contention. Running perf on a quiet box — after Phase 1 binaries exist but before Phase 2's docker compose, Phase 4's native server+gateway+agent, and Phase 5's parallel fan-out — gives the most-isolated environment available in the pipeline. DB phase numbers stay stable (`phase=7` for both perf and coverage) so the report table groups them together at the end; the wall-clock split is purely an isolation guarantee.

**Phase 8 leaves the UAT alive.** `scripts/test/teardown.sh` only stops Docker compose projects matching `yuzu-test-${RUN_ID}-*` (Phase 2 fixtures); it does not touch the native processes started by `start-UAT.sh`. This is deliberate: a successful `/test --full` run leaves a working UAT at the tested HEAD so humans can sanity-check it before cutting `/release`. Do **not** add `bash scripts/start-UAT.sh stop` to your orchestration — if the operator wants the stack down they can run it themselves.

Phase 1 is the only mandatory-blocking phase — if HEAD doesn't compile, nothing else can run. Every other phase runs to completion regardless of upstream failures so the operator gets a prioritized fix list in one pass.

**Every phase emits structured timing data into the test-runs DB.** Top-level gate timings land in `test_gates.duration_seconds`; sub-step timings (upgrade phases, OTA flow steps, individual command round-trips) land in `test_timings`. This is how trend analysis catches "Phase 2 upgrade got 3× slower since last week" without grepping log files.

> **PR2 status.** Phases 0, 1, 2, 4, 5, 6, 7, 8 are wired. Phase 3 (cross-platform OTA self-exec) is still stubbed pending PR3; its gate rows record as `SKIP` with a "planned for PR3" note. Phase 6 (sanitizers) dispatches `.github/workflows/sanitizer-tests.yml` onto the `yuzu-wsl2-linux` self-hosted runner; if the runner is offline the gate records WARN and the rest of the run continues. Phase 7 coverage runs locally against `tests/coverage-baseline.json` (real captured numbers; the original PR2 `__seed: true` permissive baseline is gone). Phase 7 perf is **measure-and-report** as of 2026-05-03: the gate records `perf_*` metrics into the test-runs DB but no longer reads a baseline file or fails on regressions — see Phase 7a below and `docs/perf-baseline-calibration-2026-05-03.md`.

## Step 0 — Initialise run state

Generate a unique run ID and start the DB record. Run these in order at the start of every invocation:

```bash
RUN_ID="$(date +%s)-$$"
COMMIT="$(git rev-parse HEAD)"
BRANCH="$(git rev-parse --abbrev-ref HEAD)"
TEST_DIR="/tmp/yuzu-test-${RUN_ID}"
LOG_DIR="$HOME/.local/share/yuzu/test-runs/${RUN_ID}"
mkdir -p "$TEST_DIR" "$LOG_DIR"

# Pick mode from operator args (default if no flag)
MODE="${YUZU_TEST_MODE:-default}"  # quick / default / full

# Cross-platform: BUILDDIR resolves to build-linux on Linux, build-macos
# on macOS. All subsequent meson invocations use $BUILDDIR rather than a
# hardcoded path. The helper file also exposes port_listening,
# disk_free_gb, host_os, docker_available, ensure_docker_path.
# shellcheck source=scripts/test/_portable.sh
. scripts/test/_portable.sh
BUILDDIR=$(build_dir)

bash scripts/test/test-db-write.sh run-start \
    --run-id "$RUN_ID" \
    --commit "$COMMIT" \
    --branch "$BRANCH" \
    --mode "$MODE"
```

Record `RUN_ID` in your scratch space so every subsequent gate call can reference it. The DB row is in `RUNNING` state until Phase 8 finalizes it.

> **`--run-id` format.** Valid run ids match `[A-Za-z0-9._-]+` and must not be the bare `.` or `..`. The generated `"$(date +%s)-$$"` always satisfies this, as does a hand-supplied `--run-id manual` for coverage-baseline capture. An invalid run id (path separator, whitespace, shell/control char, `.`/`..`) is **rejected** (the Instructions runner is stricter, see "`--instructions` mode"): `test_db.py` and all three gate scripts print an error to stderr and exit `2`, and the gate scripts surface that as a gate FAIL. This guards the test-runs DB and its log root against path traversal — see the `[Unreleased]` Security entry in `CHANGELOG.md`.

## Phase 0 — Preflight

```bash
bash scripts/test/preflight.sh                 # sanity checks
# or with cleanup:
bash scripts/test/preflight.sh --force-cleanup # tear down dangling test containers
```

**On failure**: do NOT proceed. Exit non-zero. Preflight failures are operator-fixable (free a port, clean up dangling containers, install a missing toolchain, free disk). The skill should print the preflight output verbatim and stop.

The preflight script also creates the test-runs DB at `~/.local/share/yuzu/test-runs.db` if missing, so the run-start above is safe to call.

Record gate result:
```bash
PREFLIGHT_START=$(date +%s)
bash scripts/test/preflight.sh && PRE_STATUS=PASS || PRE_STATUS=FAIL
PREFLIGHT_DUR=$(( $(date +%s) - PREFLIGHT_START ))
bash scripts/test/test-db-write.sh gate \
    --run-id "$RUN_ID" --phase 0 --gate "Preflight" \
    --status "$PRE_STATUS" --duration "$PREFLIGHT_DUR"
[[ "$PRE_STATUS" == "FAIL" ]] && { bash scripts/test/teardown.sh --run-id "$RUN_ID" --status ABORTED; exit 1; }
```

## Phase 1 — Build HEAD

Three sub-gates that can run in parallel via `&` + `wait`. Use the
unconditional `meson compile -C "$BUILDDIR"` form rather than naming
specific targets — the explicit-target form requires those targets to
exist (`yuzu_server_tests` only exists when `-Dbuild_tests=true`) and
the bare-name resolution can collide with sibling targets if multiple
subprojects define the same name.

```bash
# Build C++ binaries (server + agent + tests if enabled)
(
    set -e
    BUILD_START=$(date +%s)
    if meson compile -C "$BUILDDIR" > "$LOG_DIR/build-cpp.log" 2>&1; then
        STATUS=PASS
    else
        STATUS=FAIL
    fi
    DUR=$(( $(date +%s) - BUILD_START ))
    bash scripts/test/test-db-write.sh gate \
        --run-id "$RUN_ID" --phase 1 --gate "Build (C++)" \
        --status "$STATUS" --duration "$DUR" --log "build-cpp.log"
    bash scripts/test/test-db-write.sh timing \
        --run-id "$RUN_ID" --gate phase1 --step meson-compile --ms $((DUR * 1000))
) &

# Build Erlang gateway. Don't swallow ensure-erlang.sh errors — if Erlang
# is missing, we want the rebar3 invocation to surface the real diagnosis.
# `as prod release` (not just `compile`) is required so Phase 4's
# start-UAT.sh can launch the gateway from gateway/_build/prod/rel/.
(
    set -e
    BUILD_START=$(date +%s)
    cd gateway
    source ../scripts/ensure-erlang.sh
    if rebar3 as prod release > "$LOG_DIR/build-erlang.log" 2>&1; then
        STATUS=PASS
    else
        STATUS=FAIL
    fi
    DUR=$(( $(date +%s) - BUILD_START ))
    bash scripts/test/test-db-write.sh gate \
        --run-id "$RUN_ID" --phase 1 --gate "Build (Erlang)" \
        --status "$STATUS" --duration "$DUR" --log "build-erlang.log"
    bash scripts/test/test-db-write.sh timing \
        --run-id "$RUN_ID" --gate phase1 --step rebar3-release --ms $((DUR * 1000))
) &

# Build local docker images for the upgrade test target (skip in --quick).
# Tag with the ghcr.io prefix directly so the upgrade-test compose file
# picks it up without a separate `docker tag` step in Phase 2.
# Cross-platform: SKIP gracefully if docker is unavailable (macOS dev box
# without OrbStack/Docker Desktop running). Linux CI always has docker.
#
# TRIPLET must match the BUILD HOST's architecture (#4546). Dockerfile.server
# defaults `ARG TRIPLET=x64-linux`, so on an arm64 host an unqualified build
# cross-compiles x64 under emulation and dies inside vcpkg with "unable to
# detect the active compiler's information" (detect_compiler) — the image gate
# then fails on EVERY branch on Apple Silicon, `dev` included, and cascades to
# the Phase 2 upgrade test. Derive it from `uname -m` and pass --platform to
# match, so an arm64 box builds arm64-linux natively and an x64 box is
# byte-unchanged from the historical behaviour.
if [[ "$MODE" != "quick" ]]; then
    (
        set -e
        BUILD_START=$(date +%s)
        case "$(uname -m)" in
            arm64|aarch64) HOST_DOCKER_ARCH=arm64; HOST_VCPKG_TRIPLET=arm64-linux ;;
            *)             HOST_DOCKER_ARCH=amd64; HOST_VCPKG_TRIPLET=x64-linux ;;
        esac
        if ! docker_available; then
            bash scripts/test/test-db-write.sh gate \
                --run-id "$RUN_ID" --phase 1 --gate "Build (HEAD docker images)" \
                --status SKIP --duration 0 \
                --notes "docker not available — install/start OrbStack or Docker Desktop"
        elif docker build \
            --platform "linux/${HOST_DOCKER_ARCH}" \
            --build-arg "TRIPLET=${HOST_VCPKG_TRIPLET}" \
            -t "ghcr.io/devnullltd/yuzu-server:0.10.1-test-${RUN_ID}" \
            --label "yuzu.commit=$(git rev-parse HEAD)" \
            -f deploy/docker/Dockerfile.server . \
            > "$LOG_DIR/build-images.log" 2>&1; then
            STATUS=PASS
            DUR=$(( $(date +%s) - BUILD_START ))
            bash scripts/test/test-db-write.sh gate \
                --run-id "$RUN_ID" --phase 1 --gate "Build (HEAD docker images)" \
                --status "$STATUS" --duration "$DUR" --log "build-images.log"
            bash scripts/test/test-db-write.sh timing \
                --run-id "$RUN_ID" --gate phase1 --step docker-build --ms $((DUR * 1000))
        else
            STATUS=FAIL
            DUR=$(( $(date +%s) - BUILD_START ))
            bash scripts/test/test-db-write.sh gate \
                --run-id "$RUN_ID" --phase 1 --gate "Build (HEAD docker images)" \
                --status "$STATUS" --duration "$DUR" --log "build-images.log"
        fi
    ) &
fi

wait
```

**Detect Phase 1 failure before continuing.** `wait` always exits 0 after
all background jobs complete — individual subshell failures do NOT
propagate via `wait`. Query the DB explicitly to detect any FAIL gate
in Phase 1 and short-circuit:

```bash
PHASE1_FAILS=$(python3 scripts/test/test_db.py query --export "$RUN_ID" \
    | python3 -c "
import sys, json
d = json.load(sys.stdin)
print(sum(1 for g in d.get('gates', []) if g.get('phase') == 1 and g.get('status') == 'FAIL'))
")
if [[ "$PHASE1_FAILS" -gt 0 ]]; then
    echo "Phase 1 FAILED ($PHASE1_FAILS gates) — see logs in $LOG_DIR/build-*.log"
    bash scripts/test/teardown.sh --run-id "$RUN_ID" --status ABORTED
    exit 1
fi
```

Phase 1 is the only mandatory-blocking phase. If HEAD doesn't compile,
nothing else can run.

## Phase 2 — Upgrade Test (the user's headline priority)

Skipped in `--quick`. In default and `--full`:

```bash
bash scripts/test/test-upgrade-stack.sh \
    --run-id "$RUN_ID" \
    --new-version "0.10.1-test-${RUN_ID}" \
    --new-image-loaded 1 \
    --test-dir "$TEST_DIR"
```

`--old-version` is omitted so the script resolves it from GitHub's current
"Latest release" at runtime (`gh api repos/DevNullLtd/Yuzu/releases/latest`).
This keeps the upgrade baseline tracking whatever the last published stable
tag is without needing a pipeline edit each release. Pass `--old-version
X.Y.Z` to pin an older baseline for debugging.

The script records its own gate row (`Upgrade vOLD->vNEW`) and sub-step timings (`pull-old-images`, `stack-up-old`, `fixtures-write`, `image-swap`, `ready-after-upgrade`, `fixtures-verify`, `synthetic-uat-against-upgraded`, `recreate-after-upgrade` — a same-image `--force-recreate` of the upgraded server that must come back ready with a byte-identical `/etc/yuzu/certs` and a working login, #5370). The skill doesn't need to record anything additional.

**On failure**: Phase 2 failure is informative but not blocking — continue to Phase 4. The teardown reads gate counts at the end and the operator decides whether to commit.

## Phase 3 — OTA Agent Test (PR3, stubbed in PR1)

For `--full` only:

```bash
if [[ "$MODE" == "full" ]]; then
    bash scripts/test/test-db-write.sh gate \
        --run-id "$RUN_ID" --phase 3 --gate "OTA Linux" \
        --status SKIP --duration 0 --notes "planned for PR3"
    bash scripts/test/test-db-write.sh gate \
        --run-id "$RUN_ID" --phase 3 --gate "OTA Windows" \
        --status SKIP --duration 0 --notes "planned for PR3"
    bash scripts/test/test-db-write.sh gate \
        --run-id "$RUN_ID" --phase 3 --gate "OTA macOS" \
        --status SKIP --duration 0 --notes "hardware pending Apple Silicon arrival"
fi
```

Once PR3 lands, replace the SKIP stubs with the real script invocations:
```bash
bash scripts/test/test-ota-agent-linux.sh   --run-id "$RUN_ID"
bash scripts/test/test-ota-agent-windows.sh --run-id "$RUN_ID"
bash scripts/test/test-ota-agent-macos.sh   --run-id "$RUN_ID"   # SKIP until hardware arrives
```

## Phase 7a — Perf measurement (runs HERE, before Phase 4)

`--full` only. Despite the `7a` label (rows are tagged `phase=7` in the DB so they group with coverage in the report), perf runs **here** in wall-clock order — after Phase 3 has finished but before Phase 4 brings up the UAT stack. This is the most-quiesced point in the pipeline:

- Phase 1 build is done (binaries exist; ccache hits stop competing).
- Phase 2 docker compose has been torn down.
- Phase 3 is just DB writes.
- Phase 4 hasn't started, so no native server/gateway/agent.
- Phase 5 hasn't started, so no parallel fan-out CPU pressure.

The perf suite is fully self-contained (every upstream RPC meck'd, gateway components in-process), so it has no functional dependency on the live stack. Running it here keeps measurements off contended cores.

```bash
if [[ "$MODE" == "full" ]]; then
    bash scripts/test/perf-gate.sh --run-id "$RUN_ID"
fi
```

**Measure-and-report, not enforce (as of 2026-05-03).** `perf-gate.sh` runs `yuzu_gw_perf_SUITE`, parses throughput and latency from `ct:pal` output, records each metric into the test-runs DB as `perf_*`, and exits PASS. It does **not** read a baseline file or fail on a regression — the N=300 calibration found that 3 of the 4 gateway perf metrics are ceiling-bounded with long left tails (not Gaussian), so neither σ nor %-tolerance bands are statistically defensible. Until the gate is rebuilt around percentile primitives, perf is human-judgement-driven: the operator inspects trend via `bash scripts/test/test-db-query.sh --trend timing=phase7.perf` and shape via `tests/perf-baseline-provenance-N300.{jsonl,json}`. Full rationale and the deferred redesign live in `docs/perf-baseline-calibration-2026-05-03.md`. The script still scans the seven UAT-related ports (8080, 50051, 50052, 50055, 50063, 8081, 9568) and refuses to run if any are listening (contended measurements mislead the human eyeball too), with `--allow-busy` as an explicit debug bypass. Loadavg pre/post and the hardware fingerprint stay recorded as metric context.

## Phase 4 — Fresh Stack Stand-up

Skipped in `--quick`. Default and `--full` use the existing `start-UAT.sh` to bring up server+gateway+agent natively (faster than docker for Phase 5 e2e gates that hit the live stack):

```bash
PHASE4_START=$(date +%s)
if bash scripts/start-UAT.sh > "$LOG_DIR/fresh-stack.log" 2>&1; then
    STATUS=PASS
else
    STATUS=FAIL
fi
DUR=$(( $(date +%s) - PHASE4_START ))
bash scripts/test/test-db-write.sh gate \
    --run-id "$RUN_ID" --phase 4 --gate "Fresh stack stand-up" \
    --status "$STATUS" --duration "$DUR" --log "fresh-stack.log"
```

**`start-UAT.sh` correctly returns non-zero on any connectivity test failure** (this is the post-PR1 behavior — earlier versions exited 0 unconditionally, see CHANGELOG `[Unreleased]`). The Phase 4 gate's PASS/FAIL accurately reflects whether the 6 inline connectivity tests passed against the fresh stack. The Phase 5 Synthetic UAT gate runs again standalone with sub-step timing capture into the test-runs DB — both gates are intentional, not a duplicate.

A Phase 4 FAIL whose `fresh-stack.log` says `ports still held` or `survived SIGKILL` means a foreign process holds a UAT port, or a recorded process could not be stopped. It is not a stack defect, and `start-UAT.sh` will not kill it (it only signals PIDs it recorded); the log names the held ports (and the holding process where `lsof` is available).

## Phase 5 — Test Gates (parallel)

Run all gates concurrently via `&` + `wait`. Each is a self-contained bash invocation that captures its own log to `$LOG_DIR/<gate>.log`. Don't try to collect their stdout — read the log paths in the failure summary instead.

### Race-free parallel rebar3 via `REBAR_BASE_DIR`

EUnit, CT suites, and CT real-upstream all consume `_build/test/lib/yuzu_gw/test/` for the same set of compiled `*_tests.beam` and `*_SUITE.beam` files. When run in parallel against a shared `_build/` they race on **two** different things:

1. **Dep fetching.** Each invocation calls `Verifying dependencies...`, decides to re-fetch `proper`/`meck`/`covertool` into `_build/{default,test}/lib/`, and concurrent extraction corrupts the partially-fetched packages — the loser sees `Dependency failure: source for proper does not contain a recognizable project`, and the post-failure `rm -rf` fails with `Directory not empty` because the writer still has open file handles. (Observed in run `1777704747-244808`.)
2. **Test source compile.** When any `test/` `.erl` is edited, both rebar3 processes recompile the entire test/ directory, racing on `.bea#` → `.beam` atomic-rename of every test module — manifests as `failed to rename .../yuzu_gw_health_nf_tests.bea# to .../yuzu_gw_health_nf_tests.beam: no such file or directory` (the writer's tempfile gets unlinked underneath it). Observed in run `1777727834-294523` after the first race fix landed.

Sequential pre-warming would fix (1) but not (2) — rebar3 has no clean way to compile test/ without running tests, and any test-running pre-warm doubles the wall time of the slowest gate. The cleaner cure is to give each parallel gate **its own `_build/` tree** via `REBAR_BASE_DIR`. EUnit writes to `_build_eunit/`, CT suites to `_build_ct/`, CT real-upstream to `_build_ct_realup/`, Dialyzer keeps the shared `_build/`. They cannot collide because they touch different filesystem paths.

The fan-out below sets `REBAR_BASE_DIR` per gate. First-run cost is one-time deps refetch into each tree (~10s); subsequent runs find both trees warm. Total Phase 5 wall time goes 60s pre-fix → 105-140s with REBAR_BASE_DIR (cold first run) → ~95s warm — comparable to the broken parallel fan-out, but actually correct.

Dialyzer keeps the default `_build/` because it's the only consumer of `_build/default/` in Phase 5 — there is no race partner. Keeping its tree separate also means a `rebar3 dialyzer` run from outside `/test` reuses the same PLT cache.

A pre-warm of the default `_build/` (compiling `src/` + `_build/default/lib/` deps) is no longer needed for race-correctness; it's still cheap (~17s) and shaves a few seconds off Dialyzer first-run cold starts, so we keep it as a small optimisation. It MUST NOT touch `_build_eunit/` or `_build_ct/`:

```bash
(
    cd gateway
    source ../scripts/ensure-erlang.sh 2>/dev/null
    rebar3 compile > "$LOG_DIR/prewarm-default.log" 2>&1 || true
)
```

Pre-warm failures use `|| true` because if `src/` genuinely can't compile, every gate will fail with the same error and that's the right reporting surface — the pre-warm step is just for first-run cold-start latency, not for gating.

The pattern for every gate (note: `eval "$cmd"` is safe here because every
caller below passes a literal string constructed inline in this same skill;
the `cmd` argument is never read from operator input or external state):
```bash
gate_run() {
    local gate_name="$1" log_basename="$2" cmd="$3" phase="${4:-5}"
    # Capture project root BEFORE entering the subshell. Several gates
    # eval a `cd gateway && rebar3 ...` compound — that cd survives into
    # the post-eval test-db-write.sh invocation, so a relative path would
    # resolve against gateway/ and fail. The absolute path keeps the
    # writer reachable regardless of where the gate's cmd left $PWD.
    local project_root="$PWD"
    (
        local start=$(date +%s)
        # eval is intentional: cmd contains compound shell expressions like
        # 'cd gateway && source ../scripts/ensure-erlang.sh; rebar3 ...'.
        # All cmd strings are author-controlled constants, never user input.
        if eval "$cmd" > "$LOG_DIR/$log_basename" 2>&1; then
            local status=PASS
        else
            local status=FAIL
        fi
        local dur=$(( $(date +%s) - start ))
        bash "$project_root/scripts/test/test-db-write.sh" gate \
            --run-id "$RUN_ID" --phase "$phase" --gate "$gate_name" \
            --status "$status" --duration "$dur" --log "$log_basename"
    ) &
}
```

The default-mode Phase 5 fan-out:

```bash
gate_run "C++ unit (Catch2)" "unit-cpp.log" \
    "meson test -C \"$BUILDDIR\" --suite agent --suite server --suite echo --suite proto --suite docs --suite platform --print-errorlogs"

gate_run "EUnit" "eunit.log" \
    "bash scripts/test/eunit-gate.sh"

gate_run "Dialyzer" "dialyzer.log" \
    "cd gateway && source ../scripts/ensure-erlang.sh 2>/dev/null; rebar3 dialyzer"

gate_run "CT suites" "ct.log" \
    "cd gateway && source ../scripts/ensure-erlang.sh 2>/dev/null; REBAR_BASE_DIR=\$PWD/_build_ct rebar3 ct --dir apps/yuzu_gw/test/ct --suite=yuzu_gw_e2e_SUITE,yuzu_gw_integration_SUITE,yuzu_gw_metrics_e2e_SUITE,yuzu_gw_prometheus_SUITE"

# Real-upstream CT suite — lives under apps/yuzu_gw/integration_test/
# (separate dir from the regular test/ tree so CI's `rebar3 ct --dir
# apps/yuzu_gw/test/ct` discovery does NOT pick it up). Requires:
#   1. A live yuzu-server reachable on 127.0.0.1:50055 (Phase 4 brings
#      this up via start-UAT.sh).
#   2. YUZU_GW_TEST_TOKEN env var set to a valid enrollment token, OR
#      start-UAT.sh must have just run (its scratch dir is
#      probed for the token).
# Failing either prerequisite, the suite reports {test_case_failed,
# "No enrollment token: …"} per-case rather than a useful skip — file
# an upstream issue if you hit that during /test.
gate_run "CT real-upstream" "ct-real-upstream.log" \
    "cd gateway && source ../scripts/ensure-erlang.sh 2>/dev/null; REBAR_BASE_DIR=\$PWD/_build_ct_realup rebar3 ct --dir apps/yuzu_gw/integration_test --suite=yuzu_gw_real_upstream_SUITE"

gate_run "Integration" "integration.log" \
    "bash scripts/integration-test.sh"

gate_run "REST API E2E" "e2e-api.log" \
    "bash scripts/e2e-api-test.sh"

gate_run "MCP E2E" "e2e-mcp.log" \
    "bash scripts/e2e-mcp-test.sh"

# Synthetic UAT — Phase 4's start-UAT.sh already ran its own 6
# tests; this gate runs them again standalone with timing capture into
# the test-runs DB. Skip if Phase 4 was the source.
gate_run "Synthetic UAT" "synthetic-uat.log" \
    "bash scripts/test/synthetic-uat-tests.sh \
        --dashboard http://localhost:8080 \
        --user admin --password 'YuzuUatAdmin1!' \
        --gateway-health http://localhost:8081 \
        --gateway-metrics http://localhost:9568 \
        --run-id $RUN_ID --gate-name phase5-synthetic-uat"

# Puppeteer is warn-only — flaky on first run. Its npm dependency is never installed by
# the pipeline (tests/puppeteer/node_modules is gitignored), so a missing install is
# recorded as SKIP with the fix, not as a permanent WARN; a WARN means it ran and failed.
(
    start=$(date +%s)
    if [[ ! -d tests/puppeteer/node_modules/puppeteer ]]; then
        bash scripts/test/test-db-write.sh gate \
            --run-id "$RUN_ID" --phase 5 --gate "Puppeteer" \
            --status SKIP --duration 0 \
            --notes "puppeteer not installed; run: (cd tests/puppeteer && npm ci)"
    else
        if node tests/puppeteer/dashboard-help-test.mjs > "$LOG_DIR/puppeteer.log" 2>&1; then
            STATUS=PASS
        else
            STATUS=WARN  # not FAIL — puppeteer is best-effort
        fi
        DUR=$(( $(date +%s) - start ))
        bash scripts/test/test-db-write.sh gate \
            --run-id "$RUN_ID" --phase 5 --gate "Puppeteer" \
            --status "$STATUS" --duration "$DUR" --log "puppeteer.log"
    fi
) &

# Instructions content-suite gate — schema-driven REST exerciser.
# Drives every default-risk (safe + mutating) InstructionDefinition and
# records per-instruction pass/fail/timing into the test-runs DB.
# The destructive, forensic, server-internal, interactive and network-disrupt
# classes are opt-in via --risks; default-mode invocation excludes them.
# Destructive and forensic additionally need --target-agent-id, --confirm-target,
# --run-id, a --params-override file and (off loopback) --allow-remote; /test never runs them.
gate_run "Instructions" "instructions.log" \
    "bash scripts/test/instructions-tests.sh \
        --dashboard http://localhost:8080 \
        --user admin --password 'YuzuUatAdmin1!' \
        --run-id $RUN_ID --gate-name phase5-instructions \
        --output $LOG_DIR/instructions-outcomes.json"

wait

# Security E2E runs AFTER the fan-out, alone. Its Category 7 probe deliberately empties the
# shared 127.0.0.1 login bucket (start-UAT.sh passes --login-rate-limit 200), which would 429
# the login of any gate still running. Do not move it back into the fan-out above.
gate_run "Security E2E" "e2e-security.log" \
    "bash scripts/e2e-security-test.sh"
wait
```

`--quick` runs only the unit / EUnit / dialyzer subset (NO synthetic UAT — quick mode skips Phase 4 and has no live stack). `--full` adds the optional MCP agent gate (invokes `mcp-uat-tester` via the Agent tool against the live stack).

### `--instructions` mode (content-suite standalone)

When the operator runs `/test --instructions`, the orchestration is **truncated**: Phase 0 preflight, Phase 4 stack stand-up, then the Instructions gate from Phase 5, then Phase 8 teardown. No build, no upgrade test, no other Phase 5 gates, no sanitizers, no coverage. Use when:

- A YAML under `content/definitions/` changed (added/edited/removed an InstructionDefinition).
- The instruction-engine dispatch path (`workflow_routes.cpp` `POST /api/instructions/:id/execute`, `agent_service_impl.cpp` `cmd_execution_ids_`, response store) was touched.
- Investigating a content regression flagged by the trend tooling.

Wall clock is dominated by Phase 4 (~60-90s) and the gate itself (5-15 min for the runnable instructions at parallelism=4). The gate writes per-instruction timings to `test_timings` so `bash scripts/test/test-db-query.sh --trend timing=phase5-instructions.<id>` shows latency drift over time.

```bash
# In --instructions mode:
if [[ "$MODE" == "instructions" ]]; then
    # Run only Phase 0, 4, the Instructions gate, and Phase 8.
    # Build is not gated — operator should already have $BUILDDIR populated;
    # if not, the start-UAT.sh in Phase 4 will surface the missing binary.
    start=$(date +%s)
    if bash scripts/test/instructions-tests.sh \
        --dashboard http://localhost:8080 \
        --user admin --password 'YuzuUatAdmin1!' \
        --run-id "$RUN_ID" --gate-name instructions \
        --output "$LOG_DIR/instructions-outcomes.json" > "$LOG_DIR/instructions.log" 2>&1; then
        STATUS=PASS
    else
        STATUS=FAIL
    fi
    bash scripts/test/test-db-write.sh gate \
        --run-id "$RUN_ID" --phase 5 --gate "Instructions" \
        --status "$STATUS" --duration $(( $(date +%s) - start )) --log "instructions.log"
    # then jump straight to Phase 8 teardown
fi
```

The runner's exit code is recorded as the `Instructions` gate row above, and that row sets the run's overall_status: 0 -> PASS; 1 (one or more instruction fail/error, the run stopped early, or a destructive/forensic run executed nothing), 2 (login, content-dir, or targeting/override/pre-flight configuration error, with nothing dispatched) or 130 (the runner was interrupted by Ctrl-C, Ctrl-Break or SIGTERM) -> FAIL. `/test` never selects destructive or forensic.

A destructive or forensic run is opt-in, by hand, and targets exactly one agent on a dedicated disposable stack. It needs `--target-agent-id`, `--confirm-target` (that agent's hostname), `--run-id` and a `--params-override` file, and a loopback `--dashboard` (127.0.0.1, ::1, localhost) unless `--allow-remote` is given. Get the agent id and hostname from the dashboard Devices page or `GET /api/agents`. The account needs `Execution:Execute` (dispatch), `Response:Read` (poll the results) and `Infrastructure:Read` (the agent lookup). The runner runs the definitions one at a time, checks the id and hostname against the server's agent list before any dispatch, writes each dispatch to a manifest file before sending it (created exclusively: an existing path, symlink or FIFO is refused, so rename an earlier run's manifest or pass a new --run-id), and polls each targeted row until every response row is terminal or the poll deadline passes (--poll-timeout; 120 s for these classes unless it is given). The deadline is checked per poll, so it can overrun by up to two polls (one in flight at the deadline plus the one final poll, about 20 s). A RUNNING row exists only for flushed output, so a quiet long-running action shows no rows at all until it finishes. A row passes only if every response row is SUCCESS with no error_detail. A row that ends without a verdict from terminal rows (no rows, rows still running, polls failing for any reason, or a row the runner does not recognise) fails and stops further dispatch, so a following action never overlaps it; a terminal FAILURE/TIMEOUT/REJECTED row is a known outcome and does not stop the run. Ctrl-C, Ctrl-Break (Windows) and SIGTERM stop dispatching (exit 130); a dispatch already claimed is reported as in_flight_unknown (claimed is not sent: the stop is checked at the claim and not again once the connection is open, so a connect or TLS handshake that stalls past the stop can still transmit that one request to the target). `--run-id` must match `^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$` (stricter than the generic run-id rule above). After a targeted POST was sent only these mean "not executed": any 4xx, a 503 carrying a recognised pre-dispatch refusal reason, a 202 pending_approval (approval mode always, role-gated for a non-admin caller, or an unrecognised mode; never auto), and a refused connection or unresolvable name. HTTP 200 means the server started it. Everything else is dispatch_unknown and stops the run (do not re-run blindly): a transport failure after send, any other 5xx, any 3xx, any 2xx other than 200 and a pending_approval 202, a 202 without pending_approval, the generic 503 "no agents reached" (it also covers a failed send on the agent stream and names no command id; #6102), and any exception after an accepted POST. Three consecutive 401/403 answers to execute, or 401/403/503 to a targeted poll, also stop the run. Permissions: Execution:Execute to dispatch, Response:Read to poll, Infrastructure:Read for the agent lookup. Exit codes: 0 every dispatched instruction passed (or is pending approval); 1 one or more failed or errored, the run stopped early, or a targeted run executed nothing (every destructive/forensic row skipped or pending approval); 2 a configuration, login or pre-flight error with nothing dispatched, including --poll-timeout below 1 (targeted runs only), --output equal to --manifest, an --output that is a symlink (POSIX only) or not a regular file, a --dashboard URL with userinfo (user:password@) or a backslash, or (targeted runs) an --output or a manifest that already exists; 130 interrupted (Ctrl-C, Ctrl-Break or SIGTERM). A failed write of --output at the end only warns. Note the bash entry takes `--risks` as a comma list while the Python runner takes them space-separated:

```bash
bash scripts/test/instructions-tests.sh --dashboard http://127.0.0.1:8080 \
    --user uat-admin --password 'PASSWORD' --risks destructive,forensic \
    --target-agent-id AGENT_ID --confirm-target HOSTNAME --run-id my-run-1 \
    --params-override overrides.json --output outcomes.json
```

`--confirm-target` is a wrong-target typo guard against what the connected server reports. It cannot detect an `ssh -L` tunnel or a port forward to a different stack, and it is not an authorisation or approval control; use a dedicated admin account on a disposable stack. The password on the command line is visible in `ps`, and `http://` with `--allow-remote` sends it in cleartext. If safe/mutating classes are in the same `--risks`, those definitions are still sent to every agent (the run warns on stderr). `--target-agent-id`, `--confirm-target` and `--allow-remote` given with no destructive or forensic class in `--risks` are ignored, with a warning. An untargeted run is stricter than it was before the targeted mode: every request carries a `yuzu-instructions-runner/<run-id>` User-Agent, proxy environment variables are ignored, a redirect on the execute POST is not followed, a missing or malformed `--params-override` (including a duplicate key or a value that is not a string or an integer), a `--run-id` outside the pattern above and a `--dashboard` with userinfo or a backslash exit 2, `--output` refuses a symlink or a multi-link file, and SIGTERM stops the run like Ctrl-C (exit 130); `/test` passes none of the inputs that exit 2.

The eligible ids are the entries classed `destructive` or `forensic` in the `_overrides` of `scripts/test/instructions-risk-classification.json`; each one's required parameters are under `spec.parameters.required` in `content/definitions/*.yaml`. The `--params-override` file is a JSON object keyed by definition id; each value is an object of parameter name to value, strings or integers only (write a boolean as `"true"`/`"false"`; a duplicate key is an error; top-level keys starting with `_` are ignored). A definition with no entry, a missing required parameter, a `server.*` row, or one not eligible on the target's OS is skipped, never guessed:

```json
{
  "device.tags.clear": {},
  "device.filesystem.append": {"path": "/tmp/yuzu_uat_scratch.txt", "content": "x"}
}
```

(`device.filesystem.append`: the path must already exist on the target; the path above is for a Unix target, on a Windows target use e.g. `C:\Windows\Temp\yuzu_uat_scratch.txt`.) An empty `{}` is valid only for a definition with no required parameters.

The manifest (`--manifest PATH`, default `instructions-runner-<run-id>.manifest.jsonl` in the current directory): The manifest is an attempt log, not outcome evidence: the first line is run-start, then a dispatch line per attempt (the exact params sent: treat it as sensitive; it is created 0600 on POSIX, at creation only; .gitignore covers only the default name), an accepted line when the server answers it, and a not-sent line when a stop won the race after the dispatch line and the manifest was still open (that POST was never made). The manifest is created exclusively: a path that already exists (an earlier run, a symlink, a FIFO) is refused with exit 2, so rename it or pass a new --run-id. --output is written through an owner-only descriptor (0600 at creation only; an existing file keeps its mode) that refuses a symlink (POSIX only); a targeted run creates it exclusively and refuses an existing one (rename it first: it holds the command_id record of an earlier run); an untargeted run truncates and rewrites an existing --output in place, but only if it is a regular single-link file. A SIGKILL, a double signal in the same instant, or SIGHUP (an ssh drop) can leave only the manifest. --output holds command_id for accepted rows; rows rebuilt at an abort, and answers that land after the manifest was closed, carry no command_id in --output or the manifest: check the target by definition id and timestamp. A closed stdout may still end the process with exit 120 at interpreter flush: --output and the metrics are written first and it fails closed, never a false 0. The stderr list of not-started ids is capped at 30; the rest are in --output and the manifest. Forensic rows read behavioural data from the target, and the responses are stored in the server's response store. Recovery after a stop. In the manifest a dispatch line is an attempt and an accepted line means only that the server answered it (http status and, when given, command_id, execution_id or approval_id): 200 means the server started it; an accepted line with a 5xx status may have run; 202 and 4xx were not executed (an open approval ticket may remain). A dispatch line with no accepted line may or may not have run, unless a not-sent line follows it (a SIGKILL, a double signal in the same instant, or SIGHUP can leave only the manifest and no --output). --output holds command_id for every accepted row, plus the in_flight_unknown and dispatch_unknown rows (a dispatch_unknown row may have no command_id: a POST that failed in flight has none). A definition with no dispatch line was never sent. Check the target by hand (and the dashboard's executions) before retrying. To resume, rename the old manifest and --output first (a targeted run refuses an existing one of either; a new --run-id names a new default manifest), then pass --match with an anchored regex for the remaining ids only after verifying, e.g. --match '^(device\.tags\.clear|device\.filesystem\.append)$' (--only-id takes exactly one id).

Side effects / how to restore (the runner undoes none of them; this list is NOT exhaustive and every destructive/forensic row in the risk table applies): `device.tags.clear` and `agent.storage.clear` delete the target's tags and storage keys with no undo; `crossplatform.echo.rollup` permanently deletes Echo rows past retention, is not recoverable and has no approval gate; `security.certificates.delete` deletes a certificate; `agent.content_dist.stage`/`execute_staged`/`cleanup`/`upload_file` (`execute_staged` RUNS the staged artefact); `crossplatform.printing.clear_queue` is irreversible; `crossplatform.service.set_start_mode`; `device.script_exec.*` runs arbitrary script text; `agent.http_client.download`; `device.wol.wake`; `workflow.config_search_and_replace`; filesystem writes, registry values and the power plan stay changed until you revert them by hand. The destructive `server.*` definitions (for example `server.policy.invalidate_all`) are skipped, never sent. Forensic rows read behavioural data from the target, and the responses are stored in the server's response store. `testing.chargen.start` streams until stopped, so a targeted run skips it (even with an override); start and stop it by hand through the dashboard or REST with `agent_ids`.

### `--instructions-quarantine` mode (the self-disconnect ceremony)

> **DO NOT RUN ON A REMOTE / SSH-ONLY HOST.** The ceremony briefly cuts ALL external network. If your only access path to the box is SSH-over-the-network, you will lock yourself out until the un-quarantine fires (~25-30s) — and if the un-quarantine fails, you stay locked out until you physically reach the box. Run only on your local dev box (the one with a keyboard and a screen).
>
> Additional preconditions:
> - The agent account must have the privileges declared in `docs/agent-privilege-model.md`. Run `sudo bash scripts/install-agent-user.sh` (Linux/macOS) or `powershell -ExecutionPolicy Bypass scripts/install-agent-user.ps1` from an elevated PowerShell (Windows) once per box before the first ceremony run; the install script is idempotent. Verify with `--check` / `-Check`.
> - If the agent is running as an account WITHOUT the `pfctl` / `iptables` / `netsh` grants, the survivor will dispatch isolate but the firewall won't actually close — the survivor catches that in `confirm-blackout`, dispatches emergency release, and exits FAIL/1 without locking the box. That's the *safe* failure mode; it tells you the install script hasn't been run on this host.

This mode exercises the four-instruction quarantine cluster (`security.quarantine.{isolate,release,status,whitelist}`) including the part the schema-driven runner can't: **the actual network blackout**. Because the blackout cuts Claude Code's path to api.anthropic.com, the ceremony is driven by a detached survivor (`scripts/test/instructions_quarantine_survivor.py`) that:

1. Probes preconditions (UAT reachable, plugin loaded, external connectivity present, Yuzu localhost reachable).
2. Dispatches `security.quarantine.isolate` with `server_ip=127.0.0.1` and `whitelist_ips=127.0.0.1`. The plugin auto-whitelists loopback on every platform, so localhost endpoints stay reachable.
3. After a 5s grace, probes external destinations (1.1.1.1, 8.8.8.8, github.com, api.anthropic.com on :443) — they MUST be unreachable. Probes Yuzu localhost (8080, 50051, 8081) — they MUST be reachable.
4. Sleeps 10s, re-probes external to confirm sustained blackout.
5. Dispatches `security.quarantine.release`. Probes external to confirm recovery.
6. Writes `results.json` to the state dir.
7. (If `--launch-resume`) Tries to spawn a new Terminal with `claude --resume <session-id>` via `osascript` (macOS) or `tmux` (other platforms). Always falls back to writing `<state-dir>/relaunch.sh` for manual use.

**Operator workflow inside Claude Code**:

```bash
bash scripts/test/instructions-quarantine.sh \
    --dashboard http://localhost:8080 \
    --user admin --password 'YuzuUatAdmin1!' \
    --launch-resume      # macOS only — opens a new Terminal window
```

This script captures the current Claude session UUID from `~/.claude/projects/-Users-<user>-Yuzu/<uuid>.jsonl` (most recent), backgrounds the survivor via `setsid nohup`, prints PID + state-dir + instructions, and exits 0 immediately. The survivor runs ~30-40s asynchronously.

**During the blackout**, this Claude Code session may lose its connection to api.anthropic.com. The user has three options:
- Type `/exit` and let the survivor's auto-resume open a new Terminal
- Wait for the connection to recover (it usually does after un-quarantine)
- Manually run `bash /tmp/yuzu-quarantine-test/relaunch.sh` after the survivor finishes

**On resume, read the results**:
```bash
cat /tmp/yuzu-quarantine-test/results.json
```

The results document each phase, every probe (with TCP latency), the agent's responses to isolate/release, and any operator-actionable note. Exit codes:
- 0 — full ceremony passed: blackout sustained, recovery confirmed
- 1 — blackout incomplete or recovery probe failed (firewall partially or fully not actually closed; OR external reachable mid-blackout)
- 2 — precondition fail (login, plugin not loaded, no external connectivity at start) — no firewall change happened
- 3 — release dispatch failed: **operator must clear firewall manually** (`pfctl -F all` / `iptables -F` / `netsh advfirewall reset`). The note in `results.json` tells you which.

**Probe-only mode** (`--probe-only`) runs only the precondition checks via the schema-driven runner — verifies the quarantine plugin is loaded without any firewall side effect. Use this first if you've never run the ceremony on this box.

## Phase 6 — Sanitizers (PR2)

Sanitizer rebuilds are dispatched to the `yuzu-bigtam-linux` self-hosted pool via `workflow_dispatch`. Running them locally would pin the dev box for ~15 min of compile time each; the always-on runner absorbs that cost while the operator continues Phase 5 gates locally.

```bash
if [[ "$MODE" == "full" ]]; then
    bash scripts/test/sanitizer-gate.sh --run-id "$RUN_ID"
fi
```

The gate script:
1. Resolves the current commit (`git rev-parse HEAD`) and dispatches `.github/workflows/sanitizer-tests.yml` via `scripts/test/dispatch-runner-job.sh`
2. Polls the run to completion (default 90 min budget — covers queued + compile + test)
3. Downloads `sanitizer-asan*` and `sanitizer-tsan*` artifacts into `/tmp/yuzu-test-${RUN_ID}/sanitizer/`
4. Parses each sanitizer log for `ERROR: AddressSanitizer`, `ERROR: LeakSanitizer`, `WARNING: ThreadSanitizer`, `ThreadSanitizer: data race`, `runtime error:`
5. Writes two Phase 6 rows to `test_gates`: `Sanitizers (ASan+UBSan)` and `Sanitizers (TSan)`

**Runner-offline path (WARN, not FAIL).** If the `yuzu-bigtam-linux` pool is offline or the dispatch times out, both gates record `WARN` with notes explaining the operator retry path. The skill continues with the rest of the run rather than blocking on CI infrastructure that's out of reach.

**Workflow-file requirement.** `workflow_dispatch` evaluates the workflow file on the target ref. If you're dispatching against a commit that doesn't have `sanitizer-tests.yml` yet (e.g. running /test from an older branch), the dispatch will fail hard. The gate treats that as WARN per the offline-runner path.

**Suite selection.** Default runs both (ASan+UBSan and TSan). Override with `--suite asan` or `--suite tsan` on the gate script — useful when diagnosing a single finding and you don't want the second rebuild to compete for runner time.

## Phase 7b — Coverage (PR2)

Coverage runs locally on the operator's dev box, at the end of the pipeline (after Phase 5 gates and Phase 6 sanitizer dispatch). It uses `${BUILDDIR}-coverage/` (separate from the main `${BUILDDIR}/` to keep ccache hit rates intact). Coverage is contention-tolerant — it's measuring code-execution coverage, not throughput, so the live UAT stack from Phase 4 doesn't affect the numbers. The earlier perf step (Phase 7a) already ran on a quiet box.

```bash
if [[ "$MODE" == "full" ]]; then
    bash scripts/test/coverage-gate.sh --run-id "$RUN_ID"
elif [[ "$MODE" == "default" ]]; then
    # Default mode: coverage in report-only (metric recorded, no enforce);
    # perf skipped (default-mode budget is too tight for the ~3-5 min
    # CT suite plus registry churn).
    bash scripts/test/coverage-gate.sh --run-id "$RUN_ID" --report-only || true
    bash scripts/test/test-db-write.sh gate \
        --run-id "$RUN_ID" --phase 7 --gate "Perf" \
        --status SKIP --duration 0 --notes "perf measurement runs in --full only"
fi
```

**Coverage enforcement.** The gate parses gcovr `--json-summary` (filter set mirrored from the `.github/workflows/nightly.yml` coverage job so local/CI numbers are comparable; the gate also passes `--native-file meson/native/linux-gcc13.ini` to pin its compiler when it creates the build directory, while nightly's coverage job uses `linux-gcc15.ini`, so compare against `tests/coverage-baseline.json` rather than nightly's absolute figure), records `branch_coverage_overall` and `line_coverage_overall` metrics, and compares against `tests/coverage-baseline.json`. In `--full` mode the gate fails if branch coverage drops below `baseline.branch_percent - slack_pp` (default 0.5 pp). The gate holds a `<build-dir>.lock` for the whole run (a second concurrent run is refused with a WARN row), and a run whose tests failed or timed out, whose libgcov reported counter-write errors, that could not delete every stale `.gcda` before the run, or that left the build filesystem nearly full (`YUZU_COVERAGE_MIN_FREE_KB`) is **inconclusive**: a WARN row (exit 2 in `--full`, 0 under `--report-only`), no `*_coverage_overall` metric, no baseline comparison, and `--capture-baselines` refuses it. A surviving `meson test` on the same build directory (left by a killed gate) is refused too. The gate checks coverage on a **Linux host only**: anywhere else (macOS) it refuses up front with a WARN row, no metric and no comparison, and `--capture-baselines` fails, because the baseline is Linux/gcc data and a macOS run measured an implausibly low figure (#6187). An interrupted run (Ctrl-C, SIGTERM, SIGHUP: exit 130, 143, 129) stops `meson test` and its test processes, waits up to `YUZU_COVERAGE_KILL_GRACE_SECS` (default 30; further signals are ignored meanwhile), logs it and leaves a WARN Coverage row; a process whose identity `ps` cannot prove (busybox) is left running and logged. `YUZU_COVERAGE_TIMEOUT_MULT` (default 3) scales the test timeouts. A stale `<build-dir>.lock` left by a killed gate is cleared on the next run when its holder is dead; a leaked `<build-dir>.lock.takeover` is NOT cleared automatically: when it sits next to a stale lock the run refuses, names the file, and the operator removes it after checking that its holder pid is not running. Give hand-run gates a unique `--run-id`: a second run with the same id truncates the first run's `coverage.log` before it is refused. A failure before the gate starts logging (an unusable `--build-dir`, an option without its value) prints an error and exits 2 with no Coverage row. In default mode a failed gate or metric DB write is only logged (the caller's `|| true` hides the exit code), so the Coverage row can be missing; `--full` and `--capture-baselines` fail instead. A PASS row written after an earlier DB write in the same run failed (a metric, say) is recorded as WARN, so Phase 8 cannot finalise the run as PASS with data missing, and `--capture-baselines` refuses to rewrite the baseline once such a write has failed. **A WARN or inconclusive Coverage row in `--full` means coverage was NOT checked** (Phase 8 does not block on a WARN): read the note, fix the cause, and re-run before relying on it. Default mode records the metric but doesn't enforce — `--report-only` short-circuits the comparison. The default-mode invocation wraps the script in `|| true` so a transient gcovr or build failure writes its own WARN row and does not block the rest of the run; in `--full` mode the gate is called without `|| true`, so build, gcovr or parse failures surface as a WARN row with exit 2.

**Perf is no longer enforced (2026-05-03).** Phase 7a runs `yuzu_gw_perf_SUITE` and records `perf_registration_ops_sec`, `perf_burst_registration_ops_sec`, `perf_heartbeat_queue_ops_sec`, `perf_fanout_*_ms`, `perf_session_cleanup_ms_per_agent`, and `perf_loadavg_pre/post` into the test-runs DB. There is no baseline file and no regression check. The N=300 calibration showed 3 of the 4 throughput/latency metrics are ceiling-bounded with long left tails — neither σ nor %-tolerance bands fit them — so until the gate is rebuilt around percentile primitives the operator does the inspection: `bash scripts/test/test-db-query.sh --trend timing=phase7.perf` for run-over-run movement, `python3 scripts/test/perf-histograms.py tests/perf-baseline-provenance-N300.jsonl` (gitignored scratch tool) for shape comparison against the calibration capture, and the inline histograms in `docs/perf-baseline-calibration-2026-05-03.md` for the empirical reference distributions. Full rationale and the deferred redesign live in the same doc.

**Coverage baseline update workflow.**
1. Make a change you believe deserves a new coverage baseline (coverage up, or an accepted trade-off).
2. **Pre-flight**: a clean `meson test -C ${BUILDDIR}-coverage` must pass — the gate refuses `--capture-baselines` (FAIL row, note `refused --capture-baselines: inconclusive run (...)`) if tests fail or time out, libgcov reports counter-write errors, a stale `.gcda` cannot be deleted before the run, or the build filesystem is nearly full (UP-18 guard protecting you from anchoring a broken-environment baseline).
3. Run `bash scripts/test/coverage-gate.sh --run-id manual --capture-baselines`. The script rewrites the JSON file with current numbers + `captured_at` + `captured_commit` and prints a diff of old-vs-new values before overwrite so you can sanity-check the direction.
4. `git add tests/coverage-baseline.json` alongside your feature commit. `git blame` is the audit trail.
5. Do NOT capture a baseline in the middle of an unrelated change — the commit SHA recorded in the baseline becomes the receipt for "this is the code that earned these numbers."

**Coverage baseline refresh cadence.** Recapture at every `vX.Y.0` release tag on the canonical dev box (any Linux with GCC 13). Commit the updated JSON in the release-prep commit. Coverage drift between release trains is informative trend data.

**Seed sentinel (historical, coverage only).** The `__seed: true` sentinel was the PR2 mechanism that kept the coverage gate from silently green-passing while the baseline was a placeholder. The gate still honors it: `__seed: true` forces WARN regardless of measured numbers. The seed phase has concluded — current `tests/coverage-baseline.json` holds real captured numbers (read the file for the figures; it records no platform, and the gate only measures on Linux) and the sentinel is absent, so enforcement is live. Do **not** re-add `__seed: true` as a "temporary disable" knob; to adjust thresholds, edit `slack_pp` directly and document why in the commit message.

**Concurrent --full runs on the same ref.** The sanitizer workflow's `concurrency: cancel-in-progress: false` group means a second dispatch queues behind the first until it completes (Phase 6 only — coverage/perf run locally; the coverage gate serialises on its own `<build-dir>.lock`). If you re-run `/test --full` immediately after a successful run on the same commit, expect Phase 6 to sit queued. Use `--suite asan` or `--suite tsan` on the gate script to halve runtime when re-running a specific finding.

## Phase 8 — Teardown + Summary

```bash
bash scripts/test/teardown.sh --run-id "$RUN_ID"
```

The teardown script:
1. Stops every `yuzu-test-${RUN_ID}-*` compose project
2. Removes `/tmp/yuzu-test-${RUN_ID}/`
3. Calls `test-db-write.sh run-finish --run-id "$RUN_ID"` which aggregates gate counts and computes overall status (any FAIL → FAIL, any WARN → WARN, else PASS)

After teardown, print the final summary by querying the just-finished run:

```bash
bash scripts/test/test-db-query.sh --latest
```

The skill should also produce a markdown table in its own response (so the operator sees it inline in the chat) summarizing the same data:

```
## /test run <RUN_ID>
Commit: <sha>  Branch: <branch>  Mode: <mode>  Duration: <wall>

| Phase | Gate                       | Status | Duration | Log                                              | Notes |
| ...   | ...                        | ...    | ...      | ...                                              | ...   |

Overall: N FAIL, M WARN — <commit decision>
```

## Querying the test-runs DB

The developer-local `/test` DB lives at `~/.local/share/yuzu/test-runs.db` and
persists across runs. Common queries:

```bash
# Most recent run with full gate detail
bash scripts/test/test-db-query.sh --latest

# Last 10 runs (one row each)
bash scripts/test/test-db-query.sh --last 10

# Side-by-side diff of two runs
bash scripts/test/test-db-query.sh --diff RUN_A RUN_B

# How has the upgrade-test image-swap step trended?
bash scripts/test/test-db-query.sh --trend timing=phase2.image-swap

# How has branch coverage trended on the dev branch?
bash scripts/test/test-db-query.sh --trend metric=branch_coverage_overall --branch dev

# Which gates have flapped PASS↔FAIL in the last 14 days?
bash scripts/test/test-db-query.sh --flaky --days 14

# Dump a single run as JSON
bash scripts/test/test-db-query.sh --export RUN_ID

# Prune old runs (keep most recent 100)
bash scripts/test/test-db-query.sh --prune 100
```

Power users can `python3 scripts/test/test_db.py query ...` directly, or `python3 -c "import sqlite3; ..."` against the DB for ad-hoc analysis.

Self-hosted CI uses the same schema but never shares one host-wide SQLite file.
Each runner agent owns a durable database outside its checkout:

- Big Tam: `/srv/ci/work-N/_tool/yuzu-test-runs/yuzu-bigtam-linux-N/test-runs.db`
- Wee Tam: `D:\ci\test-runs\yuzu-weetam-windows-N\test-runs.db`

`ci.yml` initializes and finalizes the current runner's row automatically.
Schema v3 keeps GitHub rerun attempts distinct and records the job result and
duration, platform/runner/commit/event, ccache ratio, Meson test-entry
result/duration/timeout, and known flakes recovered by isolated retry. Query a
runner in place by setting `YUZU_TEST_DB`:

```bash
YUZU_TEST_DB=/path/to/runner/test-runs.db \
  bash scripts/test/test-db-query.sh ci-stats --since 30d
YUZU_TEST_DB=/path/to/runner/test-runs.db \
  bash scripts/test/test-db-query.sh ci-suite-stats --since 30d
YUZU_TEST_DB=/path/to/runner/test-runs.db \
  bash scripts/test/test-db-query.sh ci-flakes --since 30d
```

Provision or repair all runner DBs with
`deploy/linux/Provision-BigTam-Runner-Telemetry.sh` or
`deploy/windows/Provision-Windows-Runner.ps1`. The reviewed
`tests/known-flaky.json` file remains the allowlist; database observations never
change pass/fail policy. GitHub-hosted macOS runners are ephemeral, so their
Meson logs remain Actions artifacts rather than runner-local history.

## Failure handling

The skill is designed so a single gate failure does NOT short-circuit the run. Goals:

1. **Always finalize the run row.** Even on a hard error or interrupt, `teardown.sh --run-id "$RUN_ID"` should be called so the DB has `finished_at` set and `overall_status` is something other than `RUNNING`. Wrap the body of the run in a `trap 'bash scripts/test/teardown.sh --run-id "$RUN_ID" --status ABORTED' ERR INT TERM` near the top.
2. **Phase 1 (build) is the only hard short-circuit.** Build failures mean nothing else can run.
3. **All other phases run to completion.** The operator gets a prioritized fix list in one pass instead of a fix-rerun loop.
4. **Print failure summaries inline.** When a gate fails, the skill should `tail -50 "$LOG_DIR/<gate>.log"` so the operator sees the actual error without having to find the log path themselves.

## Cost / ROI

| Mode | Phases | Wall clock | Use case |
|---|---|---|---|
| `--quick` | 0, 1 (no images), 5-subset, 8 | 8-15 min | "About to commit, want a fast sanity check" |
| default | 0, 1, 2, 4, 5, 8 | 25-45 min | "About to push to dev" |
| `--full` | 0-8 (PR2/PR3 features lit) | 60-120 min | "About to tag a release" |
| `--instructions` | 0, 4, 5-instructions, 8 | 8-20 min | "Content YAML changed / dispatch path edited" |
| `--instructions-quarantine` | 0, 4, ceremony | 30-40s | "Quarantine plugin / firewall behaviour edited" |

Default mode is the recommended pre-push gate. The upgrade test in Phase 2 catches the highest-stakes class of bugs (silent data loss on schema migration) which no other local gate finds.

## Known risks

1. **Port collisions** from prior interrupted runs — preflight + `--force-cleanup` flag.
2. **Stale Docker volumes** — `test-upgrade-stack.sh` always `down -v`s its own project before `up`.
3. **Disk space** — preflight refuses < 20 GB free.
4. **WSL2 + native dockerd** — preflight verifies `docker context show` is `default`, not `desktop-linux`.
5. **Erlang rebar3 cache pollution** — gateway gates always source `scripts/ensure-erlang.sh` first; the `--dir apps/yuzu_gw/test` flag is mandatory per bug #337.
6. **Fixture write race with migrations** — `test-fixtures-write.sh` polls `/readyz` for `{"status":"ready"}` (not `/livez`) before writing — uses the #339 compound-fix readiness contract.
7. **Self-hosted runner availability** — Linux jobs depend on the Big Tam
   `yuzu-bigtam-linux-{0..3}` pool and Windows jobs on Wee Tam's
   `yuzu-weetam-windows-{0..3}` pool; offline → WARN or fail-closed skip,
   depending on the workflow gate.
8. **DB retention is explicit** — local `/test` rows can be pruned with
   `test-db-query.sh --prune N`; runner-local CI telemetry is intentionally
   append-only for now so evidence is not silently aged out before a retention
   and export policy is measured.

## Post-run follow-ups

After a successful run, the operator typically wants to:

1. **Commit and push** — the green run is the gate. Reference `RUN_ID` in the commit message for traceability.
2. **Compare to the prior run** — `test-db-query.sh --diff <prev> <current>` shows what changed in gate status and timings.
3. **Investigate WARN gates** — these don't block but accumulate as tech debt. If a pattern emerges across runs, file an issue per `docs/agents/issue-standard.md`: dedupe first with both mandatory probes (`gh issue list --repo DevNullLtd/Yuzu --state open --search "<gate name>" --json number,title` and `gh search issues --repo DevNullLtd/Yuzu --state open "<gate keywords>" --json number,title --limit 20`), four body sections, one type label + one of `P1`/`P2` + `ready-for-agent`, and an Origin section citing the `RUN_ID`s that show the pattern.
4. **Bump the coverage baseline** if a legitimate drop or trade-off is intentional — `coverage-gate.sh --capture-baselines` and commit the updated `tests/coverage-baseline.json`. Perf has no enforced baseline as of 2026-05-03; perf movement is reviewed by the operator against `tests/perf-baseline-provenance-N300.{jsonl,json}` and is not blocking.

After a failed run:

1. **Read the failing log files** under `~/.local/share/yuzu/test-runs/${RUN_ID}/`.
2. **Re-run with `--force-cleanup`** if dangling state from the failed run is suspected.
3. **`--keep-stack`** lets you poke at the live UAT environment after the test exits.
