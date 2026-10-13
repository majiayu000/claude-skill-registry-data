---
name: sim-bringup
description: >-
  Bring up a behavioral (RTL) simulation end-to-end: stand up or fix a testbench,
  compile (xvlog/xvhdl), elaborate (xelab), run (xsim), and methodically diagnose
  compile errors, elaboration failures, $fatal/assertion failures, X-propagation,
  and hangs. Use when the user says "simulate this", "run the testbench", "set up
  simulation", "my sim fails / hangs / shows X", "why does my testbench not pass",
  "add a testbench and verify the DUT", or "debug this RTL in simulation". Requires
  the SynthPilot MCP server (AI -> server.py -> TCP:9999 -> tcl_server.tcl running
  inside an open Vivado session). This is BEHAVIORAL sim only (no gate-level/timing
  sim); it does NOT prove timing closure or signoff. Measure (compile log / sim log
  / probe) before changing anything, classify the failure, apply the smallest safe
  fix, then re-run.
---

# Simulation Bring-Up (Behavioral / RTL)

A methodology playbook for getting a behavioral simulation **running and passing** on the SynthPilot xsim engine, and for diagnosing *why* it fails when it doesn't. The discipline is the same as timing closure: **observe with a tool, classify the symptom, apply the smallest safe change, re-run, and never claim a pass without fresh `sim_run` output that proves it.**

This skill drives the standalone xsim pipeline (`sim_compile` → `sim_run` → probe/diagnose), which runs `xvlog`/`xvhdl` → `xelab` → `xsim` directly and bypasses Vivado's `launch_simulation`. It does **not** require synthesis.

## When to use

- User says "simulate this", "run the testbench", "set up simulation", "verify this module in sim".
- A testbench exists but **fails to compile, fails to elaborate, fails its assertions, prints X, or hangs**.
- You need a behavioral testbench authored from scratch for a DUT and then run to a verdict.
- You want to inspect DUT internals over time (waveform-style) to understand a functional bug.
- You want functional code coverage of an RTL block (statement/branch/condition/toggle).

## When NOT to use

- **Timing signoff / timing closure / CDC / lint.** Behavioral sim has no notion of routed delays. Use the timing-closure / cdc-analysis / linting skills. A passing behavioral sim is **necessary, not sufficient** for signoff.
- **Gate-level or post-implementation (SDF) simulation.** This engine elaborates RTL behavioral models; it does not run timing-annotated netlists.
- **Hardware bring-up / on-chip debug** (ILA/VIO/JTAG). Use the hw-debug skill — `hw_ila_*`, `hw_vio_*`, `program_device`.
- **Pure RTL bug hunting with no testbench and no intent to run a sim** — if the user only wants static checks, prefer `check_syntax` / `run_quick_lint` (cheaper than a full compile).

## Prerequisites (verify first)

Run these *before* touching files. Do not assume state.

1. **MCP / Vivado link is alive** — `test_connection`. If it fails, STOP and tell the user to open Vivado and ensure the Tcl server (`tcl_server.tcl`) is running in the Tcl Console. Nothing below works without it.
2. **A project is open** — `get_project_info`. The xsim engine writes its scratch to `<project>/mcp_sim/` and resolves files via `get_files -compile_order sources -used_in simulation`; there must be a current project. If none, `open_project` / `create_project` (ask the user which).
3. **Know the design** — `list_source_files` and `list_simulation_files`. Confirm the DUT RTL is in the project and the intended testbench (if any) is in the **sim_1** fileset, not sources_1. A TB in the wrong fileset will silently be excluded from the sim compile order.
4. **Know the simulation top** — the testbench module name. `sim_compile(top_module=...)` takes it explicitly, so confirm the exact module name (case-sensitive) from the file, not a guess.

If any prerequisite is missing, resolve it (or ask) before proceeding. Do not fabricate a green result on a half-configured project.

## Methodology

One **change-class per iteration** so cause→effect stays attributable. The pipeline is strictly ordered: **author/locate TB → compile → elaborate → run → diagnose**. Each later stage assumes the earlier stage produced fresh, clean output.

### 0. Decide: author a testbench, or run an existing one?

- **Existing TB**: confirm it is in sim_1 (`list_simulation_files`); read it if needed (`read_file`) to get the exact `top_module` name. Skip to step 2.
- **No TB / author one**: continue to step 1.

### 1. Author a testbench (only if one does not exist)

Prefer structured, machine-checkable output over `$display` soup — it gives a clean pass/fail verdict the parser can read.

1. `sim_setup_report` — deploys `mcp_report.vh` into the project sim dir and tells you the `` `include `` directive. (`sim_compile` also auto-deploys it, but calling this first documents the macros: `` `MCP_INIT ``, `` `MCP_ASSERT ``, `` `MCP_ASSERT_EQ ``, `` `MCP_SIGNAL ``, `` `MCP_LOG ``, `` `MCP_FINISH ``.)
2. Write the TB with `create_testbench_file(file_name="tb_<dut>.v", content=...)` — this writes the file **and** adds it to the sim_1 fileset in one step. Inside the module: `` `include "mcp_report.vh" ``, call `` `MCP_INIT `` in the initial block, drive stimulus, check with `` `MCP_ASSERT_EQ(name, actual, expected) ``, and call `` `MCP_FINISH `` then `$finish`.
3. Testbench hygiene (you are responsible for these — they are the #1 cause of false fails and hangs):
   - **Always have a finite end** — a `$finish` reached by a counter/timeout, or use `sim_run(run_time="<bounded>")`. A free-running clock with no `$finish` will hang `run all`.
   - **Reset before checking.** Assert reset for ≥1 clock, deassert, *then* sample. Checking during reset yields X and false FAILs.
   - Use `===`/`!==` (4-state) for X-aware comparisons; `` `MCP_ASSERT_EQ `` already uses `===`.
   - Match the DUT port widths/names exactly — width mismatches elaborate as truncation, not errors.

If the user asks you to *change the DUT RTL* to make a test pass, treat that as a design change: **recommend** the edit and ask before applying it (see Safety rails). Fixing the *testbench* is in-scope; silently rewriting the DUT to chase a green is not.

### 2. Compile + elaborate

`sim_compile(top_module="tb_<name>")`.

This compiles all sim-used files (VHDL via `xvhdl`, Verilog/SV via `xvlog`), auto-discovers `glbl.v` and include dirs, defines `MCP_SIM_REPORT`, then elaborates with `xelab` into snapshot `mcp_snapshot`. Read the **status token** on the first line:

| Token | Meaning | Next action |
|---|---|---|
| `COMPILE_OK: ...` | xvlog/xvhdl + xelab succeeded | Go to step 3 (run). Note `warnings=N` — investigate if non-trivial. |
| `COMPILE_ERROR: N errors in xvlog/xvhdl` | Syntax / file / language error before elaboration | `sim_get_compile_log(stage="compile")`, classify (see table), fix, re-`sim_compile`. |
| `ELABORATE_ERROR: N errors in xelab` | Compiled, but linking the hierarchy failed (missing module, unresolved instance, library, param) | `sim_get_compile_log(stage="elaborate")`, classify, fix, re-`sim_compile`. |
| `SIM_LOCKED: ...` | A stale `xsimk.exe` kernel is locking the snapshot; xelab can't rebuild it | `sim_stop()` (kills the kernel + clears the lock), then re-`sim_compile`. Do **not** edit RTL — this is not a code error. |

Fix **one error class at a time**, then re-compile. Do not batch unrelated fixes — a single syntax error often cascades into dozens of phantom downstream errors that vanish once the first is fixed.

### 3. Run

Choose by expected runtime:

- **Short (< ~30 s wall):** `sim_run(run_time="all", detail_level=1)`. Returns the parsed test verdict (`detail_level`: 0=summary, 1=+failures, 2=+signals at failure times, 3=full JSONL) plus captured `$display` output.
- **Long / multi-minute:** `sim_run_async(run_time="all")`, then poll `sim_get_sim_status()` until it reports `COMPLETED` (it returns `RUNNING` with a tail + elapsed time while in progress). This is the required pattern for long sims — never block on `sim_run` for minutes.
- If `sim_run` returns a **timeout** message, the sim may still be running: re-issue via `sim_run_async` + `sim_get_sim_status`, or read progress with `sim_get_compile_log(stage="sim")`.

Read the result header:

- `=== Simulation Completed ===` with `tests=P/T, 0 failed` → candidate pass. Verify per Safety rails before claiming success.
- `=== Simulation Error ===`, any `FAIL`, `$fatal`, or `ERROR:` lines → go to step 4.

### 4. Diagnose (only when a stage failed or the verdict is FAIL)

Classify with the table below **before** changing anything. Pull the evidence that matches the failing stage:

- Compile/elab errors → `sim_get_compile_log(stage="compile"|"elaborate")`.
- Run-time failures / X / wrong values → `sim_get_report(detail_level=2)` for failure times + signals, then `sim_probe(...)` to watch the offending signals across the relevant window, and `sim_list_signals(scope=...)` first if you are unsure of exact hierarchical paths (escaped generate-block names are common).
- Hang/timeout → there is no `$finish` or the stimulus never satisfies the exit condition; inspect the TB and bound the run.

## Classification table (symptom → cause → smallest safe fix)

Apply the **first** fix that addresses the actual cause. Testbench and config fixes come before any DUT RTL change.

| Stage / Symptom | Likely cause | Smallest safe fix (in order) |
|---|---|---|
| `COMPILE_ERROR`: `syntax error`, `unexpected token` | TB or RTL syntax; SV used without `--sv` | Read the cited file:line (`read_file_lines`). Fix the source. If SV constructs in a `.v` file: `sim_compile(extra_args="--sv")`. Optionally pre-check with `check_syntax_file`. |
| `COMPILE_ERROR`: `cannot find include file` | `` `include "mcp_report.vh" `` placed before the module, or header not on a discovered include path | Move the include **inside** the module. Ensure headers are registered as `Verilog Header` file type so `sim_compile` adds their dir via `-i`. |
| `COMPILE_ERROR`: missing `` `define ``/macro | A required Verilog define isn't set for sim | `add_verilog_define` / `set_verilog_defines`, or pass `sim_compile(extra_args="-d NAME=VALUE")`. State the assumption you're making about the define's value. |
| `ELABORATE_ERROR`: `module <X> not found` / `instance ... has no ...` | DUT or a sub-module isn't in the sim compile order; wrong module name | `list_simulation_files` + `list_source_files`. If RTL missing from sim, `add_source_file`/`add_simulation_file`; check compile order with `check_compile_order`. Verify exact module name (case-sensitive). |
| `ELABORATE_ERROR`: unresolved Xilinx primitive / `unisim` / IP black box | IP behavioral model or library not pulled in; IP outputs not generated | Confirm IP outputs exist (`generate_ip_outputs` / `report_ip_status`). Pass extra libs via `sim_compile(extra_elab_args="-L <lib>")`. (`glbl.v` and the standard unisim/xpm libs are added automatically.) |
| `ELABORATE_ERROR`: port-width / param mismatch | TB instantiates DUT with wrong width/param | Fix the TB instantiation to match the DUT. Optionally confirm with `check_port_width_mismatch`. |
| `SIM_LOCKED` | Stale `xsimk.exe` from a prior async run holds the snapshot lock | `sim_stop()` then re-`sim_compile`. Never an RTL fix. |
| Run: `FAIL` with expected≠actual | Real functional mismatch — DUT bug **or** wrong expected value in TB | First confirm the TB's expected value and timing are correct (sample after reset, on the right edge). `sim_probe` the DUT inputs/outputs around the fail time. If TB is correct and DUT is wrong, **recommend** the RTL fix — do not silently patch the DUT. |
| Run: outputs are `X`/`Z` | Uninitialized reg, missing reset, multiple drivers, unconnected port, or sampling during reset | `sim_probe` from t=0 to find where X originates. If TB sampled too early → fix TB (delay/reset). If RTL has an uninitialized/unreset reg or a real X source → `check_latches`/`check_async_reset` and **recommend** the RTL fix. |
| Run: hang / timeout, no `$finish` | Free-running clock with no terminating condition; stimulus never reaches exit | Bound it: `sim_run(run_time="<finite>")`. Then fix the TB to reach `$finish` deterministically (counter/timeout). If async already launched and stuck: `sim_stop()`. |
| Run: `$fatal` / assertion from RTL or TB | An RTL `assert`/`$fatal` fired, or a TB self-check `` `MCP_ASSERT `` failed | `sim_get_report(detail_level=2)` for the time + message, `sim_probe` the relevant signals at that time, classify as TB-expectation vs real DUT bug, then fix the responsible side. |
| Pass but suspiciously fast / 0 tests | TB exits before exercising anything, or `` `MCP_INIT ``/`` `MCP_FINISH `` missing so no JSONL was produced | Check `tests=P/T`. If `T==0`, the TB ran no assertions — fix the TB to actually drive + check. A "pass" with zero assertions is **not** a pass. |

## Diagnose → fix → re-run loop (with STOP conditions)

```
1. RUN the current stage (sim_compile, then sim_run / sim_run_async+status).
2. READ the status token / verdict (fresh tool output, every iteration).
3. If clean and verdict = pass with tests > 0  -> go to Output (success path).
4. Else CLASSIFY via the table using stage-appropriate evidence
   (sim_get_compile_log / sim_get_report / sim_probe / sim_list_signals).
5. Apply ONE smallest-safe fix (config/TB before DUT RTL).
6. Re-run the SAME stage. Record before/after (status token, error count,
   tests P/T) so the change's effect is attributable.
7. Repeat.
```

**STOP and hand back to the human when:**

- The remaining fix requires a **DUT RTL or architectural change** — present the exact change, the evidence (probe/report), and the trade-off; let the user approve. Do not silently edit the DUT.
- A `FAIL`/`X`/`$fatal` could reflect a **real DUT bug** and the correct expected behavior is ambiguous — ask the user for the intended behavior rather than tuning the TB to mask it.
- Two consecutive iterations produce **no net improvement** (same error count, same failing test) — stop thrashing; report what you tried and what's left.
- You'd need to **delete/weaken the testbench's checks** (remove an assertion, loosen a comparison, shrink the run so a failing region never executes) to get green. That is a fake-pass — refuse and surface it.
- A prerequisite turns out to be missing mid-flow (project closed, connection dropped) — re-run prerequisites, don't paper over it.

## Safety rails (do not violate)

1. **Evidence before claims.** Never say "simulation passes" / "the DUT works" without a **fresh `sim_run`/`sim_get_sim_status` result** in this session showing `=== Simulation Completed ===`, `0 failed`, **and** `tests > 0`. A successful *compile* (`COMPILE_OK`) is **not** a passing simulation — it only proves it built.
2. **No fake-pass.** Do not get to green by deleting/weakening assertions, loosening `===` to `==`, shortening the run so a failing window is skipped, ignoring `$fatal`/`X`, or declaring a 0-assertion run a "pass." If a check is genuinely wrong, fix it transparently and say why.
3. **Smallest safe change first.** Order of preference: testbench/stimulus fix → compile/elab args & defines → file/fileset/compile-order fix → (only with user approval) DUT RTL change. Never jump to editing the DUT to chase a verdict.
4. **Recommend RTL edits, never silently apply them.** TB edits are in-scope. DUT/architectural edits get presented with evidence and a trade-off, then wait for the user.
5. **One change-class per iteration.** So you can attribute the effect. Re-measure after each change; show before/after.
6. **Behavioral ≠ signoff.** A passing behavioral sim says nothing about timing, CDC, DRC, or routability. Never imply otherwise; point to the appropriate signoff skill.
7. **Long runs go async.** Use `sim_run_async` + `sim_get_sim_status` for multi-minute sims; do not block. If a kernel is stuck or `SIM_LOCKED` appears, `sim_stop()` to recover — and note it kills *all* xsim kernels on the machine.
8. **Real tools only.** Use only the SynthPilot tool names above. If a needed capability (e.g., SDF/gate-level sim, UVM) isn't available, say so plainly rather than inventing a tool.

## Output

Report back in this shape:

```
SIMULATION BRING-UP — <tb_top> on <project>

Pipeline status:
  Compile/Elaborate : COMPILE_OK (files=<n>, vhdl=<n>, warnings=<n>)  | or COMPILE_ERROR/ELABORATE_ERROR/SIM_LOCKED
  Run               : Completed | Error | Hang(bounded)
  Verdict           : <P>/<T> tests passed, <F> failed   (tests=0 => NOT a pass)

Evidence (fresh, this session):
  - sim_run / sim_get_sim_status: <header line + tests line>
  - <sim_get_report / sim_probe / compile log excerpt for any failure>

Failures diagnosed (if any):
  - <symptom> -> <classified cause> -> <fix applied> (before: <metric>, after: <metric>)

Changes I made:
  - <testbench / fileset / compile-arg edits — list them>

Changes I recommend (NOT applied — need your call):
  - <DUT RTL / architectural edits, each with the probe/report evidence and trade-off>

Open questions / STOP reason (if handing back):
  - <ambiguous expected behavior, exhausted safe options, etc.>
```

State explicitly whether the simulation **passes with a non-trivial set of assertions** (the only thing that counts as success here) or whether it merely compiled. Never round a compile-clean-but-unrun design up to "working."
