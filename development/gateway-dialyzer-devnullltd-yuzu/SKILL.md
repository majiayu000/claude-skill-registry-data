---
name: gateway-dialyzer
description: Run dialyzer over the Yuzu Erlang gateway. Sources the Erlang toolchain and runs rebar3 dialyzer. Use after any .erl change in gateway/ — CLAUDE.md mandates dialyzer be clean before commit because compilation success does not imply type correctness.
---

# gateway-dialyzer

Runbook for static type analysis on the Yuzu Erlang gateway. **Mandatory after every `.erl` change** per CLAUDE.md.

## Command

From the repo root:

```bash
source scripts/ensure-erlang.sh >/dev/null && \
  command -v erl >/dev/null || { echo "Erlang missing"; exit 1; }
cd gateway && rebar3 dialyzer
```

First run on a fresh checkout builds the PLT (persistent lookup table) for the full OTP + dependency closure — this takes 2-5 minutes. Subsequent runs are incremental and complete in 10-30 seconds. The PLT lives under `_build/default/rebar3_<otp>_plt`; if it gets corrupted, delete it and rerun.

## Why this is mandatory

`rebar.config` uses `warnings_as_errors` for compile, so compile warnings block the build. But dialyzer warnings are separate — the compiler silently accepts:
- `-spec` contract violations (function called with an arg that the spec rejects)
- Unreachable patterns in case clauses
- Dead code from structurally impossible states
- Missing dependencies (functions called from modules not listed in `applications`)
- Opaque type leaks

Dialyzer catches all of these. Skipping dialyzer is how the gateway acquires silent type bugs that only surface weeks later.

## Interpreting output

- **No output after "Analyzing N files ..."** — clean, no findings. Exit code 0.
- **`Unknown functions:` / `Unknown types:`** — a transitive dep is missing from the `applications` list in `yuzu_gw.app.src`. Rule: **if you call a function from a transitive dependency, add its owning app to `applications`.** `ctx` is the canonical example — the gRPC layer's request-context type, which used to arrive transitively through `grpcbox` (now gone) and which we call directly (`ctx:get/3`, `ctx:t()` in specs), so it must be listed explicitly or dialyzer can't find it in the PLT. Apps that only appear in callback types (`cowlib`, `gun`) go in `rebar.config`'s `dialyzer` `plt_extra_apps` instead.
- **`The call ... will never return since it differs in arguments from the success typing`** — the call arguments contradict the callee's `-spec`. Fix the caller, not the spec (unless the spec is wrong).
- **`The variable _ can never match since previous clauses completely covered the type`** — dead code from a structurally impossible state. Delete the catchall. The circuit breaker's `on_success/on_failure` functions are the canonical example: only `closed` and `half_open` are reachable because `check_circuit/1` rejects `open` before the RPC runs, so a `_ -> ...` catchall is unreachable.
- **`Plugin gpb does not export init/1`** — benign warning from rebar3 itself, not dialyzer. gpb is used via `grpc` config, not as a rebar3 plugin. Ignore.

## Known pitfalls

| Symptom | Root cause | Fix |
|---------|-----------|-----|
| Dialyzer can't find a function you can clearly see in a dep's source | Dep is transitive, not in `applications` | Add the app to `yuzu_gw.app.src` `applications` list |
| Warnings about a fallback clause you added "just in case" | The -spec declares it unreachable | Delete the clause; respect the spec |
| PLT-related errors after an OTP upgrade | Stale PLT from prior OTP version | `rm -rf gateway/_build/default/rebar3_*_plt` and rerun |
| Warnings you don't understand after adding a new dep | New dep's types weren't added to the PLT | `rebar3 dialyzer --update-plt` (automatic on next run anyway) |

## Workflow discipline

Per CLAUDE.md, the required sequence after any gateway `.erl` edit is:
1. `rebar3 compile` — catches syntax + explicit compile warnings
2. `gateway-eunit` skill — catches runtime behavior regressions
3. `gateway-dialyzer` (this skill) — catches type violations and dead code
4. Commit only if all three are clean

If dialyzer reports a warning you believe is wrong, do not suppress it — investigate. Every dialyzer warning that was "known and benign" has, at some point, turned out to be a real bug.
