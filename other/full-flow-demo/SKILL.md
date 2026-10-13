---
name: full-flow-demo
description: >-
  Drive a Xilinx FPGA design end-to-end through the complete build flow:
  RTL -> simulation -> synthesis -> implementation -> bitstream, with a
  verification gate after every stage so a downstream stage never runs on an
  upstream stage that silently regressed.
  Invoke this skill when the user says "rtl to bitstream", "end to end",
  "full flow", "run everything", "build the whole thing", "take this design
  all the way to a .bit", "complete build", or asks to drive a project from
  source files to a programmed/exportable bitstream in one orchestrated pass.
  Requires the SynthPilot MCP server connected to an open Vivado session with
  the Tcl server (tcl_server.tcl on TCP:9999) running. This is the
  ORCHESTRATION playbook: it sequences the real flow tools, gates each stage on
  fresh tool evidence, stops on the first real failure, and hands off to the
  specialist skills (timing-closure, cdc-analysis, lint, simulation-debug)
  instead of trying to fix violations itself.
---

# Full-Flow Demo: RTL -> Sim -> Synth -> Impl -> Bitstream

You are orchestrating a complete FPGA build. Your job is **sequencing and
gating**, not problem-solving. You run each stage, then **prove with a fresh
tool report that the stage actually passed** before unlocking the next stage.
The flow is a pipeline of gates: a green stage opens the next gate; a red stage
**stops the flow** and hands the specific failure to the right specialist
skill.

The single most important rule: **a bitstream is not "done" because
`generate_bitstream` returned. The implemented design must pass post-route
signoff — setup AND hold timing met, DRC clean, route status fully routed,
methodology clean — and that signoff must run on the open implemented design
*before* you write the bitstream.** Synthesis numbers are necessary but never
sufficient.

---

## When to use

- User wants a design taken from source files all the way to a `.bit` (or
  `.xsa` / `.mcs`) in one orchestrated pass: "rtl to bitstream", "full flow",
  "run everything", "end to end".
- You have (or will create) a Vivado **project** with sources, constraints, and
  a known top module and target part.
- The user wants stage-by-stage gating and a final signoff summary they can
  trust, rather than a single black-box `run_full_flow` call.

## When NOT to use

- **A single stage is the actual problem.** If the user says "fix my timing",
  "why does synthesis fail", "is my CDC clean", "my sim is wrong" — go straight
  to the specialist skill (timing-closure, synthesis-debug, cdc-analysis,
  simulation-debug, lint). This skill *calls into* those; it does not replace
  them.
- **No project / no Vivado connection yet.** Resolve prerequisites first.
- **The design is a Block Design / Zynq / MPSoC system** that has not yet been
  validated, generated, and wrapped. Do the BD bring-up first
  (`bd_validate_design` -> `bd_generate_output_and_wrapper` ->
  `set_top_module <wrapper>`), then return here for synth -> bitstream.
- **The user wants speed over safety** ("just slam it through, I don't care about
  checks"). You may use `run_full_flow` as a fast path, but you must still run
  the **post-route signoff gate** (Stage 5) before claiming success. Never skip
  that gate.

---

## Prerequisites (verify first)

Run these **before touching the flow**. Do not assume; confirm with tool output.

1. **MCP / Vivado / Tcl server alive** — `test_connection`. If it fails, stop and
   tell the user to open Vivado and start `tcl_server.tcl` (TCP:9999). Nothing
   below works without this.
2. **A project is open with a known target part** — `get_project_info`. Confirm
   project name, **part number**, and current top module are what the user
   expects. If no project is open: `open_project` (existing) or `create_project`
   + `add_source_file` / `add_constraint_file` (new).
3. **Top module is set and correct** — confirm via `get_project_info`; fix with
   `set_top_module` if wrong. A wrong top silently synthesizes the wrong thing.
4. **Sources and constraints are present and in order** — `list_source_files`,
   `list_constraint_files`. **A flow with zero constraint files will "pass"
   timing vacuously** (no clocks defined) — treat "0 constraints" as a hard
   stop, not a pass. If compile order is suspect, `check_compile_order`.
5. **License tier permits the full flow** — `get_license_status`. Async runs,
   advanced reports, and some IP/BD tools are PRO/MAX. If FREE, fall back to the
   synchronous basic path and tell the user which gates you cannot run.

Record the **baseline**: part, top, clock constraints present (`get_all_clocks`
after a design is open), and intended target frequency. You will measure the
final result against this.

---

## Methodology (numbered, gated)

Run stages **in order**. After each stage, the **gate** must pass on fresh tool
output or you **STOP** and route to the specialist. One stage at a time so
cause -> effect stays attributable.

**Stage ordering is signoff-before-bitstream.** The post-route signoff gate
(Stage 5) runs on the open implemented design and proves setup/hold timing,
routing, DRC, and methodology are all clean **before** `generate_bitstream` is
ever called (Stage 6). You never write a bitstream on an unverified implemented
design. After the bitstream is written, a short re-confirmation read (Stage 6's
gate) checks the write itself and that signoff still holds.

> **Fast path note:** `run_full_flow` runs synthesis -> implementation ->
> bitstream in one call with per-stage timing and early-stop-on-failure. It is
> acceptable when the user wants speed AND the design has already passed
> lint/sim. **It does not replace the post-route signoff gate.** Because
> `run_full_flow` writes the bitstream inside the same call, if you use it you
> must immediately `open_implemented_design` and run the full Stage 5 signoff
> evidence gate afterward; only a green Stage 5 result licenses a PASS verdict.

### Stage 0 — Static checks (cheap, before any long run)

Catch dumb errors before burning minutes on synthesis.

- `check_syntax` (or `check_syntax_file` per file) — must be clean.
- `run_quick_lint` for a fast structural pass; escalate to `run_full_lint_check`
  if the user wants thoroughness. Triage with `get_lint_violations`.
- Targeted structural checks as relevant: `check_latches` (unintended latches),
  `check_async_reset`, `check_fsm`, `check_port_width_mismatch`,
  `check_unconnected_ports`, `check_black_box`.

**GATE 0:** No syntax errors. No **error-severity** lint/structural findings
(unintended latch, width mismatch, missing module / black box, broken compile
order). Warnings may pass with a noted assumption.
- **If it fails:** STOP. Hand to the **lint** skill. Do **not** `waive_lint_violation`
  or `disable_lint_rule` to make the count go green — see Safety rails.

### Stage 1 — Functional simulation (does the RTL do the right thing?)

Synthesizing functionally-broken RTL wastes an hour. Simulate first when a
testbench exists.

- Confirm the TB: `list_simulation_files`; set the sim top with
  `set_simulation_top` if needed.
- Compile: `sim_compile` (pass `top_module`). On failure read
  `sim_get_compile_log`.
- Run. **Multi-minute sims: use the async pattern** — `sim_run_async`, then poll
  `sim_get_sim_status` until COMPLETED (or `sim_stop` to abort). Short sims:
  `sim_run`.
- Read results with `sim_get_report`. Inspect waveforms/values via
  `sim_list_signals` + `sim_probe` if the pass/fail is ambiguous.

**GATE 1:** Testbench reports PASS (self-checking TB, expected `$finish`, no
assertion/`$error`/mismatch). If there is no testbench, **state that explicitly**
as a risk ("proceeding to synthesis without functional verification") and ask the
user whether to continue.
- **If it fails:** STOP. Hand to the **simulation-debug** skill. A failing sim is
  an RTL bug; do not "fix" it by changing constraints downstream.

### Stage 2 — CDC sanity (before committing to a build)

Clock-domain-crossing bugs do not show up in timing or DRC and survive to silicon.

- `check_cdc_lint` as an early RTL-level pass. A fuller `report_cdc` needs an
  elaborated/synthesized design and is run again — and gated — in Stage 3.

**GATE 2:** No **critical** (unsynchronized / glitch-prone) CDC findings at the
RTL level.
- **If it fails:** STOP. Hand to the **cdc-analysis** skill. Do **not**
  `set_false_path` across a crossing to silence it unless you can state the
  assumption that it is genuinely async-safe and the user agrees — silencing a
  real CDC is a fake-pass.

### Stage 3 — Synthesis

- (Optional) pick a strategy with `set_synthesis_strategy` — default is fine for
  a first pass; smallest change first.
- Run. **Multi-minute: async** — `run_synthesis_async`, poll `get_run_status`
  until the synth run STATUS shows complete (watch PROGRESS reach 100%). Short:
  `run_synthesis`.
- Open the result for analysis: `open_synthesized_design`.
- Evidence: `get_synthesis_report`, `get_synthesis_warnings`,
  `check_synthesis_issues` (needs the design open). Confirm clocks exist:
  `get_all_clocks`. Sanity-check `report_utilization` (a synth util that already
  exceeds 100% of any resource means impl cannot succeed — stop early).
- **Re-run `report_cdc` now that there is a real netlist** — synthesis can
  introduce or expose crossings the RTL-level `check_cdc_lint` did not see.

**GATE 3:** All of the following on fresh output:
- Synth run COMPLETE (not ERROR), no error-level synth warnings.
- **At least one clock constraint present** (`get_all_clocks` non-empty).
- Utilization physically fits the part (`report_utilization` under 100% on every
  resource).
- **Post-netlist CDC clean** — `report_cdc` shows **no critical / unsafe
  (unsynchronized, glitch-prone, fan-out) crossings**. A crossing introduced or
  revealed by synthesis is a STOP, not a warning to skip.

Post-synth *timing* is *indicative only* — do **not** claim "timing met" here.
- **If it fails:** STOP. Synth errors -> **synthesis-debug** skill. Post-netlist
  CDC findings -> **cdc-analysis** skill. Util overflow -> tell the user the
  design does not fit this part (architectural, not a constraint fix).

### Stage 4 — Implementation (opt -> place -> route)

- (Optional) `set_implementation_strategy` (e.g., a Performance/Explore strategy)
  only if a first default pass missed timing — smallest change first, so do the
  default first.
- Run. **Almost always multi-minute: async** — `run_implementation_async`, poll
  `get_run_status` until impl_1 STATUS shows route_design Complete. Short
  designs: `run_implementation`.
- `open_implemented_design` so the Stage 5 signoff reports read the routed design.

**GATE 4:** Impl run COMPLETE (route_design did not error or abort).
- **If it fails to route / errors:** STOP. Capture `get_implementation_warnings`
  and `report_congestion`; route placement/congestion/timing-driven-routing
  failures to the **timing-closure** skill (it owns strategy/floorplan/RTL
  remediation). Do not blindly bump strategies in a loop.

### Stage 5 — Post-route SIGNOFF gate (the gate that licenses "done") — runs BEFORE the bitstream

**This gate must pass on the open implemented design BEFORE any bitstream is
written.** A failure here means the design is not signoff-clean; writing a
bitstream is pointless (and `generate_bitstream` would re-run DRC and refuse
anyway). Run on the **open implemented design** (`open_implemented_design`) with
**fresh** reports:

- **Timing:** `extract_timing_metrics` (WNS/TNS/WHS/THS, failing endpoints) — you
  need **both** setup (WNS/TNS) and hold (WHS/THS) numbers across all clock
  groups. `check_timing` to confirm there are no unconstrained paths or
  missing-clock issues hiding the real picture.
- **Routing:** `report_route_status` — design must be **100% routed**, zero
  unrouted nets.
- **DRC:** `report_drc` — zero **error/critical** violations. (DRC must be clean
  here, before the bitstream, because `generate_bitstream` reruns DRC and will
  refuse to write on errors.)
- **Methodology:** `report_methodology` — no critical methodology warnings
  (these flag CDC/timing-exception abuse the other reports miss).
- **(Recommended) Power:** `report_power` for a thermal/budget sanity number.

**GATE 5 (signoff):** ALL of the following must be true **simultaneously** on
fresh post-route output, or you STOP:
- **Setup met on every clock group:** WNS ≥ 0 (equivalently TNS = 0).
- **AND hold met on every clock group:** WHS ≥ 0 (equivalently THS = 0).
  Setup-clean does not excuse a hold failure and vice-versa — **both** must pass
  at the same time.
- **AND** route status is 100% routed (zero unrouted nets).
- **AND** DRC clean (no error/critical violations).
- **AND** methodology clean (no critical warnings).

Only when every one of these is green on fresh output may you proceed to write
the bitstream.
- **If timing fails (setup OR hold < 0):** STOP. Hand to the **timing-closure**
  skill with the `extract_timing_metrics` / `analyze_critical_paths` evidence.
  Do **not** `set_false_path` / `set_multicycle_path` to clear a real violation.
- **If DRC/methodology fails:** STOP and surface the specific rule IDs. Do not
  waive without an explicit user-approved assumption.

### Stage 6 — Bitstream generation + final re-confirmation

Reach this stage **only after Stage 5's signoff gate is fully green.** The design
is already proven signoff-clean; this stage writes the artifact and re-confirms
nothing regressed in the write.

- `generate_bitstream` (synchronous; it launches `impl_1 -to_step
  write_bitstream` and waits). If you took the `run_full_flow` fast path, the
  bitstream was written inside that call — in which case you ran Stage 5's
  signoff gate *after* the call; treat that signoff result as Stage 5 and this
  stage's re-confirmation together.

**GATE 6 (write + re-confirm):**
- Bitstream write reported success and a `.bit` path is returned.
- A final read still shows the implemented design signoff-clean: re-confirm with
  `report_route_status` (still 100% routed) and `report_drc` (still 0 errors)
  on the open implemented design. (`generate_bitstream` runs its own DRC; a
  successful write plus these reads is the final proof.)
- **If the write fails (e.g., DRC blocks it):** STOP. This is a real signoff
  failure — return to Stage 5's DRC handling, not a workaround. (This should be
  rare, since Stage 5 already verified DRC.)

### Stage 7 — Handoff artifacts (only after Gate 6 is green)

Produce what the user actually asked for:

- **Program a board now:** `open_hardware_manager` -> `connect_hardware_server`
  -> `open_hardware_target` -> `program_device`.
- **Hand to embedded/Vitis (Zynq/MPSoC):** `export_hardware`
  (`include_bitstream=True`) -> `.xsa`.
- **Flash boot:** `generate_mcs` / `program_flash` / `add_flash_configuration`.

---

## Decision table — failed gate -> cause -> safe action -> owner

| Failed gate | Likely cause | Smallest safe action | Hand off to |
|---|---|---|---|
| 0 syntax/lint | Typo, latch, width/port mismatch, black box, compile order | Report violations; recommend RTL/file-order fix (do not waive) | **lint** skill |
| 1 simulation | Functional RTL bug | Report failing TB checks via `sim_get_report`/`sim_probe` | **simulation-debug** skill |
| 2 CDC (RTL) | Unsynchronized async crossing | Report `check_cdc_lint` findings; recommend synchronizer | **cdc-analysis** skill |
| 3 synth error | Unsupported construct, missing file/param | `get_synthesis_warnings`, `check_synthesis_issues`; recommend RTL fix | **synthesis-debug** skill |
| 3 CDC (netlist) | Crossing introduced/exposed by synthesis | Report `report_cdc` findings; recommend synchronizer | **cdc-analysis** skill |
| 3 util overflow | Design too big for part | Report `report_utilization`; this is architectural, not a constraint | user (part/arch decision) |
| 3 no clocks | Missing/empty XDC | Add real `create_clock_constraint`; **never** proceed with 0 clocks | user / constraints author |
| 4 route fail / congestion | Routing/placement pressure | `report_congestion`; try ONE stronger impl strategy, else escalate | **timing-closure** skill |
| 5 timing (WNS or WHS < 0) | Real setup or hold failure | `extract_timing_metrics`+`analyze_critical_paths`; constraints/strategy before RTL | **timing-closure** skill |
| 5 route not 100% | Unrouted nets | `report_route_status`; congestion/strategy via timing-closure | **timing-closure** skill |
| 5 DRC | Real rule violation (IO, config, etc.) | Report rule IDs from `report_drc`; fix root cause | user (confirm before any waiver) |
| 5 methodology | Exception/CDC abuse | Report `report_methodology`; remove improper exceptions | **cdc-analysis** / **timing-closure** |
| 6 bitstream write blocked | DRC regression at write | Report `report_drc` rule IDs; fix root cause (return to Stage 5) | user (confirm before any waiver) |

---

## Orchestration loop + STOP conditions

```
for stage in [0:static, 1:sim, 2:cdc, 3:synth, 4:impl, 5:signoff, 6:bitstream+reconfirm]:
    run stage
    pull FRESH evidence with the gate's tools
    if gate PASS:
        continue
    else:
        STOP. Do not advance. Hand the specific evidence to the owner skill.
```

Note the ordering: **signoff (Stage 5) gates the implemented design before the
bitstream is written (Stage 6).** You never advance to `generate_bitstream`
until setup AND hold timing, routing, DRC, and methodology are all green.

**Hard STOP conditions (do not advance, do not retry blindly):**
- Any gate fails on fresh tool output.
- A long async run shows STATUS = ERROR / aborted in `get_run_status` /
  `sim_get_sim_status`.
- You would have to **silence a real violation** (false_path / multicycle /
  waiver / disable_rule) to make a gate go green.
- You have tried **one** safe strategy/constraint change at a stage and it did not
  cross the gate — escalate, do **not** loop through strategy permutations.

**Do not thrash:** at most one safe remediation attempt per stage *within this
skill* (e.g., default impl strategy missed timing -> try one Performance
strategy). Beyond that, present options + costs and hand to the specialist.
Constraint/strategy changes come **before** any RTL change, and RTL changes are
**recommended to the user, never silently applied**.

---

## Safety rails (do not violate)

1. **Evidence before claims.** "Bitstream is valid / timing met / DRC clean /
   CDC clean" requires **fresh post-implementation tool output** in THIS session
   (`extract_timing_metrics`, `report_route_status`, `report_drc`,
   `report_methodology`). A returned `generate_bitstream` or a green
   `run_full_flow` line is **not** proof of signoff. Synthesis numbers never
   prove signoff.
2. **Signoff before bitstream.** The post-route signoff gate (Stage 5) runs on
   the open implemented design **before** `generate_bitstream`. Never write a
   bitstream on an unverified design; never reorder these.
3. **No fake-pass.** Never apply `set_false_path`, `set_multicycle_path`,
   `set_max_delay`, `waive_lint_violation`, `disable_lint_rule`, or
   `set_clock_groups` to make a violation disappear. Exceptions are legal only
   when the path is *genuinely* exempt — state the assumption explicitly, and if
   the item could be real (a CDC, an actual long path), **ask the user first**.
4. **Smallest safe change first.** Constraints/strategy before RTL. Default
   strategy before exotic strategy. One change-class per iteration so the next
   measurement attributes cause to effect.
5. **Never proceed on a vacuous pass.** Zero constraint files / zero clocks /
   no testbench are NOT passes — they are missing verification. Call them out
   and get user direction.
6. **Recommend RTL edits; do not silently rewrite the design.** Use
   `read_file`/`read_file_lines` to cite the issue; propose the edit; let the
   user (or an explicit instruction) approve `update_file`/`replace_in_file`.
7. **Long flows use async + poll.** Synthesis, implementation, and long
   simulation go through `*_async` + `get_run_status` / `sim_get_sim_status`,
   never a blocking call that risks a timeout mid-build.
8. **Real tools only.** Use only the exact SynthPilot tool names. If a needed
   capability (e.g., explicit checkpoint export, or automated incremental
   compile) is not in the catalog, say so rather than inventing a tool. Vivado
   runs persist their own state on disk, and `open_synthesized_design` /
   `open_implemented_design` reopen a run for analysis — you do not need (and
   must not invent) a separate checkpoint-write tool.
9. **Surface trade-offs then stop.** When safe options are exhausted, present the
   options and their costs (area/power/effort/risk) and hand back to the human.

---

## Output format

Report the flow as a **gate table**, then a verdict. Show before/after where a
remediation was attempted.

```
=== FULL-FLOW DEMO — <project> @ <part>, top=<top> ===

Prereqs:  connection OK | project OK | top OK | constraints=<N clocks> | tier=<...>

Stage gates (fresh evidence):
  [PASS] 0 Static     syntax clean; lint: 0 err / <w> warn
  [PASS] 1 Sim        TB PASS (<runtime>, self-checking)
  [PASS] 2 CDC (RTL)  0 critical crossings (check_cdc_lint)
  [PASS] 3 Synth      COMPLETE; clocks=<list>; util fits (LUT x%/FF y%); report_cdc 0 critical
  [PASS] 4 Impl       route_design COMPLETE
  [PASS] 5 SIGNOFF    WNS=<+ns> AND WHS=<+ns> (all clocks) | 100% routed | DRC 0 err | methodology clean
  [PASS] 6 Bitstream  written -> <path/to.bit>; re-confirm: 100% routed, DRC 0 err
Artifacts:   <.bit> [, <.xsa> / <.mcs> / programmed device]

VERDICT: PASS — signoff gate (Stage 5) met on fresh post-route evidence; bitstream written and re-confirmed.
         (or) STOPPED at Stage <n>: <one-line failure> -> handed to <skill> with <evidence>.
```

Rules for the report:
- Every `[PASS]` must cite the **tool** that proved it; an unproven stage is
  `[UNVERIFIED]`, never `[PASS]`.
- The final **VERDICT: PASS** is permitted **only** when Gate 5 is green —
  setup (WNS ≥ 0 / TNS = 0) **and** hold (WHS ≥ 0 / THS = 0) across all clocks,
  100% routed, DRC 0 errors, methodology clean — on fresh
  `extract_timing_metrics` + `report_route_status` + `report_drc` +
  `report_methodology` output, **and** Gate 6 confirms the bitstream was written
  with signoff still holding. Otherwise report exactly which gate stopped the
  flow and which specialist skill now owns it.
