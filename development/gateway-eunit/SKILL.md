---
name: gateway-eunit
description: Run the Yuzu Erlang gateway eunit test suite correctly. Sources the Erlang toolchain, uses --dir to work around rebar3 auto-discovery bug (#337), and explains how to interpret the output. Use when the user asks to run gateway unit tests, verify a gateway change, check for regressions in eunit, or chase an eunit flake.
---

# gateway-eunit

Runbook for exercising the Yuzu Erlang gateway eunit suite.

## Command

From the repo root:

```bash
source scripts/ensure-erlang.sh >/dev/null && \
  command -v erl >/dev/null || { echo "Erlang missing — check scripts/ensure-erlang.sh output"; exit 1; }
cd gateway && rebar3 eunit --dir apps/yuzu_gw/test
```

Extra args (e.g. `--module yuzu_gw_agent_tests`) go on the end. If the user names a specific module, still pass `--dir apps/yuzu_gw/test` — it is required, not optional.

To capture output without burning tokens, redirect to `/tmp/` and tail the result:
```bash
rebar3 eunit --dir apps/yuzu_gw/test > /tmp/eunit_run.txt 2>&1; tail -30 /tmp/eunit_run.txt
```

## Why `--dir` is mandatory

rebar3 3.27 decides "is this test module in the project" by intersecting against the application's compiled `modules` list in `yuzu_gw.app`, which only contains `src/` modules. Test modules whose name has no 1:1 `src/` counterpart (`yuzu_gw_circuit_breaker_tests`, `yuzu_gw_env_override_tests`, `yuzu_gw_scale_tests`, every `*_SUITE` file, helpers like `yuzu_gw_perf_helpers`) get rejected before any test runs:

```
===> Error Running EUnit Tests:
  Module `yuzu_gw_circuit_breaker_nf_tests' not found in project.
  ...
```

With `--dir apps/yuzu_gw/test`, rebar3 scans the directory directly and accepts every module. This is tracked as issue #337; the workaround is in tree in `scripts/run-tests.sh` already.

## Interpreting output

- **`All N tests passed.`** — clean pass (count changes often; a clean run's summary line reports it).
- **`Passed: N.  One or more tests were cancelled.`** — at least one test timed out at the eunit 5-second default. The cancellation usually cancels the entire enclosing `{setup, ...}` group, so the real impact is larger than "one test". Search for `*timed out*` in the full output to find the culprit.
- **`Module X not found in project.`** — you forgot `--dir`. See #337 above.
- **Stray `connection_refused` / `Failed to notify stream status`** log lines — fixture leak from a prior test module. Don't ignore; they have caused real test flakes (#336).

## `--module` does NOT give isolation

A common trap: running `rebar3 eunit --dir apps/yuzu_gw/test --module yuzu_gw_agent_tests` to "isolate" a single module. It does not. rebar3 runs the full suite FIRST (the `--dir` phase), then the filtered module SECOND, **in the same BEAM VM**. The second run inherits polluted state (meck mocks, registered names, leaked processes) from the first — so a passing filtered run does not prove the test is order-independent, and a failing one may be failing because of pollution rather than the test itself.

To get real isolation, either:
1. Delete `_build/test` between runs (`rm -rf gateway/_build/test`), which forces a fresh BEAM.
2. Spin up `erl` directly on the compiled beams (`erl -pa _build/test/lib/yuzu_gw/ebin -pa _build/test/lib/*/ebin`) and run test functions manually — useful for reproducer scripts when bisecting a leak source.

## Debugging a hang

If a test times out and fixture state at setup time looks clean, the problem is often a mock process registered under a canonical gen_server name (e.g. `yuzu_gw_registry`) that silently discards `gen_server:call` messages. The diagnostic that finds these fast: `process_info(Pid, [message_queue_len, status, current_function, current_stacktrace])` on the target pid. Spawn the probe from inside the hanging `init/1` via a sleeping helper process so it fires while the call is stuck. This technique found the root cause of #336 when the issue's original hypothesis was wrong.

## After any change

Always follow up with `rebar3 dialyzer` (see the `gateway-dialyzer` skill). AGENTS.md mandates dialyzer runs after every Erlang change — compilation succeeding is not enough because `warnings_as_errors` only catches compile warnings, not dialyzer warnings.
