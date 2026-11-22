---
name: diagnose
description: Diagnose Yuzu bugs and performance regressions with a disciplined reproduce-minimize-hypothesize-instrument-fix-regression-test loop. Use when the user says `/diagnose`, "debug this", reports a failure, flake, broken behavior, or performance regression.
---

# Diagnose

Build a feedback loop before guessing. Read `CONTEXT.md` and relevant ADRs so hypotheses use Yuzu's domain vocabulary.

## Loop First

Create the fastest deterministic signal that reproduces the user-visible failure:

- focused unit or integration test
- `scripts/start-UAT.sh` plus REST/gRPC/CLI probe
- gateway EUnit/CT/Dialyzer command
- replayed log, request, proto payload, or DB fixture
- reduced harness around a store, handler, plugin, or gateway module
- repeated stress loop for flakes
- perf measurement before changing code

If no loop is possible, stop and ask for the missing artifact or environment. Do not proceed on vibes.

## Phases

1. Reproduce: confirm the loop shows the same symptom the user reported.
2. Minimize: reduce the input, fixture, test, or command until the signal is sharp.
3. Hypothesize: list 3-5 ranked falsifiable hypotheses and the prediction each makes.
4. Instrument: probe one hypothesis at a time. Use debugger/REPL first, targeted logs second.
5. Fix: add the regression test at the correct seam before the fix when possible.
6. Verify: run the original loop, the regression test, and the relevant targeted suite.
7. Cleanup: remove temporary probes and `[DEBUG-...]` logs; delete throwaway harnesses unless intentionally kept under a debug path.

## Yuzu Checks

- For Erlang failures, source `scripts/ensure-erlang.sh`; remember `rebar3 eunit --module` is not isolation.
- For build/test selection, invoke `$yuzu-build`.
- For Meson/proto/plugin/Windows boundaries, invoke the matching Yuzu skill.
- For performance, use measurement scripts such as `scripts/test/perf-gate.sh` or a narrow harness before and after. Perf gates are measure-only unless the specific test enforces a threshold.

## Final Report

State the reproduced symptom, the hypothesis that won, the fix, the regression test, exact validation commands, and any architectural gap that prevented a clean regression test.
