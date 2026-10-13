---
name: power-optimization
description: >
  Analyze and reduce dynamic and static power on a Xilinx Vivado design (total
  power, junction temperature, thermal margin). Use when the user says "reduce
  power", "power optimization", "lower power consumption", "power report",
  "report_power", "too hot / junction temp too high", "battery / thermal
  budget", "cut dynamic power", "static/leakage power", or asks why a design
  draws too much current. Requires the SynthPilot MCP server with Vivado open
  and the tcl_server.tcl TCP bridge running.
---

# Power Optimization

A measurement-driven playbook for analyzing and reducing FPGA power. Power is a
**physical, post-implementation property**: it depends on placement, routing,
clock enables, switching activity, and I/O drive — not just RTL. Every claim of
power reduction MUST be backed by a fresh `report_power` from an
**implemented** design. Synthesis-stage estimates are directional only.

## When to use

- User asks to "reduce power", "optimize power", "lower power consumption",
  "cut dynamic power", or "fix leakage / static power".
- User reports the device runs too hot: high junction temperature, thermal
  margin warnings, fan/heatsink concerns, or a battery/thermal budget.
- User wants a power report (`report_power`) explained, or a confidence-level
  / breakdown analysis (clocks vs logic vs signals vs BRAM vs DSP vs I/O vs
  static).
- User wants power compared before/after a change, or wants to know whether a
  strategy/constraint change moved the power number.

## When NOT to use

- **Timing is failing (negative WNS/TNS).** Power optimization can lengthen
  paths and make timing worse. Close timing FIRST (use the timing-closure
  skill), then optimize power. Refuse to trade away met timing for power
  without explicit user sign-off.
- **The design has not been implemented yet.** Power on a pre-implementation
  design is a wild guess. If only synthesis exists, say so and run
  implementation first (or state the estimate is low-confidence).
- **Pure functional bugs, CDC, lint, or bitstream-generation problems** — use
  the matching skill. Power is downstream of a working, routed design.
- **The user wants a custom XPE/spreadsheet pre-silicon power budget** before
  any RTL exists. This skill operates on a real design in the project.

## Prerequisites (verify first)

Run these BEFORE any analysis. Do not assume state.

1. `test_connection` — confirm the Tcl bridge to Vivado is live. If it fails,
   stop and tell the user to start Vivado + paste `tcl_server.tcl`.
2. `get_project_info` — confirm a project is open and learn the **target part**
   (power is part- and speed-grade-specific) and the active run.
3. `get_run_status` — confirm whether implementation is complete. `report_power`
   is only meaningful on an **implemented** (placed + routed) design.
   - If implementation is NOT done: run it via `run_implementation_async`, then
     poll `get_run_status` until complete. Do NOT block.
   - If only synthesis exists and the user wants a quick directional number,
     `open_synthesized_design` + `report_power` is allowed but you MUST label
     the result "synthesis estimate, low confidence — not signoff."
4. `open_implemented_design` — load the routed design into memory so power and
   utilization queries reflect real placement/routing.
5. Capture the **baseline** before touching anything:
   - `report_power` (total W, dynamic vs static split, per-category breakdown,
     junction temperature, thermal margin, and the **confidence level**).
   - `report_utilization` (LUT/FF/BRAM/DSP/IO/CLK counts — power scales with
     these and with clock count).
   Record these numbers. Every later iteration is compared against this
   baseline.

## Power-report literacy (read before acting)

`report_power` is only as good as its switching-activity assumptions. Know
which mode you are in:

- **Vectorless estimation (default):** Vivado guesses toggle rates from a
  default primary-clock activity and a default toggle rate (often ~12.5%). The
  report's **Confidence level** will read **Low** or **Medium**. Treat the
  absolute watts as approximate; treat the **relative** before/after delta and
  the **category breakdown** as the actionable signal.
- **SAIF-driven (high confidence):** real switching activity from a gate-level
  simulation SAIF is annotated onto the netlist. This is the only path to a
  **High** confidence number and to trustworthy *dynamic* power. SynthPilot
  cannot annotate a SAIF for you through these tools — if the user needs
  signoff-grade dynamic power, tell them to run a post-implementation timing
  simulation, dump a SAIF, and annotate it in Vivado directly; this skill then
  consumes the resulting `report_power`.

Always read and report the **confidence level**. Never present a Low/Medium
vectorless number as a guaranteed result.

## Methodology

Work in a strict **measure → classify → smallest-safe-change → re-measure**
loop. One change-class per iteration so cause and effect are attributable.

### 1. Establish the baseline and the goal

- Read the baseline `report_power`. Identify total power, the **dynamic/static
  split**, and the **dominant categories** (sort the breakdown: Clocks, Logic,
  Signals, BRAM, DSP, I/O, GTs/MMCM/PLL, Static/Device).
- Read junction temperature and thermal margin. If thermal margin is negative
  or near zero, this is a **thermal** problem (cooling/ambient/derating), not
  just a logic-power problem — flag it explicitly.
- Confirm the user's target: a watt budget, a temperature limit, or "as low as
  reasonable." Without a target, optimize the largest movable category and stop
  when changes get risky.
- **Static power** is dominated by silicon (part, speed grade, junction temp)
  and is mostly fixed for a given device. The only real levers are: a
  lower-power/slower speed grade, a smaller device, lower Vccint (device/board
  decision), or reducing junction temperature (which lowers leakage). Surface
  these as decisions; do not pretend RTL changes will move static power much.

### 2. Classify the dominant power source

Use the breakdown to pick ONE target category, then consult the table below.
Attack the biggest movable contributor first.

### 3. Apply the SMALLEST SAFE change first (constraints/strategy before RTL)

Ordered by safety:
1. **Tool strategy** — power-aware implementation strategy. Set
   `set_implementation_strategy` (e.g. `Area_Explore` to shrink logic/route, or
   `Flow_RuntimeOptimized` only for quick iteration). Vivado's
   power_opt_design (intelligent clock gating) is enabled inside power-oriented
   strategies; this is the safest single lever because it does not touch RTL.
   Re-run implementation and re-measure.
2. **Constraints / I/O properties** — for I/O-dominated power, the fix is in the
   XDC (slew, drive strength, on-chip termination, lower-power I/O standard via
   `create_io_constraint` / editing the constraint file). For unused clocks,
   removing or gating the source.
3. **IP reconfiguration** — for BRAM/DSP/MMCM/PLL-dominated power, reconfigure
   the offending IP (e.g. BRAM cascade/sleep, fewer MMCM/PLL outputs, lower
   clock frequency in `configure_clocking_wizard` / `create_clocking_wizard`).
4. **RTL / architecture (recommend, do not silently apply)** — clock-enable
   gating, reducing active clock domains, operand isolation, RAM enable gating,
   downclocking idle logic. Propose the edit, show the file/line via `read_file`
   / `read_file_lines`, and let the user approve before `update_file` /
   `replace_in_file`.

Apply exactly ONE change-class, then go to step 4. Never stack a strategy
change, an I/O change, and an RTL change in one pass — you will not know what
worked.

### 4. Re-implement and re-measure (the only proof)

- Re-run with `run_implementation_async`; poll `get_run_status` until done.
  (Never claim a power result from a stale run.)
- `open_implemented_design`, then `report_power` again. Compare against the
  previous iteration: total W, the targeted category, AND the confidence level.
- **Guardrail check every iteration:** `report_timing_summary` (WNS/TNS must not
  have gone negative) and `report_drc` (no new violations). A power win that
  breaks timing or DRC is not a win — revert it.
- Record the before/after delta. If the change did not help (or hurt timing),
  revert it and pick the next item from the table.

### 5. Loop or stop (see STOP conditions)

Repeat steps 2–4. Stop when a STOP condition is met, then produce the Output.

## Classification table — symptom → likely cause → smallest safe fix

| Dominant category in `report_power` | Likely root cause | Smallest safe fix first | Tools |
|---|---|---|---|
| **Clocks** high | Too many/high-freq clock nets always toggling; ungated clock trees; redundant MMCM/PLL outputs | Power-aware impl strategy (enables clock gating); reduce clock frequency where spec allows; remove unused generated clocks; consolidate clock domains | `report_clock_networks`, `report_clock_utilization`, `set_implementation_strategy`, `configure_clocking_wizard`, then re-impl + `report_power` |
| **Logic / Signals** high | High average toggle rate; large always-active combinational/sequential mass; high-fanout nets driving wide loads | Power-aware impl strategy + power_opt clock gating; then RECOMMEND clock-enable gating / operand isolation in RTL | `report_high_fanout_nets`, `report_utilization_hierarchical` (find the hot module), `set_implementation_strategy`, then RECOMMEND RTL via `read_file_lines` |
| **BRAM** high | Memories with enable always asserted; over-wide/over-deep RAMs; no sleep/cascade | Reconfigure memory IP (narrower/cascade/sleep); RECOMMEND RAM enable gating so unused banks idle | `report_utilization`, `get_memory_config`, `configure_memory`, then re-impl + `report_power` |
| **DSP** high | DSP slices clocked/active when idle; no operand isolation | Strategy that reduces/area-optimizes DSP (`Flow_AreaMultThresholdDSP` synth); RECOMMEND operand isolation / DSP enable gating | `set_synthesis_strategy`, `report_utilization`, then RECOMMEND RTL |
| **I/O** high | Excess slew rate, high drive strength, power-hungry I/O standard, unnecessary on-chip termination, high-toggle outputs | Edit XDC: lower SLEW (SLOW), reduce DRIVE, choose lower-power IOSTANDARD, remove needless termination | `report_io`, `create_io_constraint` / edit constraint file via `read_file`+`replace_in_file`, then re-impl + `report_power` |
| **MMCM / PLL / GT** high | More clock outputs or transceiver lanes than used; high VCO; unused GT channels powered | Reduce MMCM/PLL outputs & VCO; disable unused GT lanes (IP reconfigure) | `report_clock_utilization`, `configure_clocking_wizard`, IP reconfigure, then re-impl + `report_power` |
| **Static / Device** high (large share) | Silicon leakage: high junction temp, hot speed grade, oversized device | Mostly a device/thermal DECISION: lower junction temp (cooling/ambient), lower-power speed grade, smaller part. Surface as options — do NOT expect RTL to move it | `report_power` (junction temp, thermal margin), then present options + STOP |
| **Junction temp / thermal margin** critical | Inadequate cooling, high ambient, or genuinely high total power | Reduce dynamic power (rows above) AND flag cooling/ambient/derating; recompute margin after | `report_power`, then iterate dynamic-power rows + surface thermal trade-off |

## Loop and STOP conditions

Iterate the measure→fix→re-measure loop. **STOP and hand back to the human**
when any of:

- **Goal met.** Fresh post-implementation `report_power` meets the user's watt
  or temperature target AND `report_timing_summary` shows WNS ≥ 0 (or unchanged
  from baseline) AND `report_drc` is clean. Report the confidence level with the
  number.
- **Diminishing returns.** Two consecutive iterations each yield < ~2% total
  power improvement. Further squeezing isn't worth the risk; present remaining
  options.
- **Safe options exhausted.** Strategy, constraints, and IP-config levers are
  used up and only RTL/architectural rewrites or a device/speed-grade/board
  change remain. Present those options + their costs (timing risk, redesign
  effort, BOM change) and STOP. Do not start large RTL surgery autonomously.
- **A trade-off threshold is hit.** A power win would require degrading timing
  below the user's margin, changing the device/part, or waiving a real DRC.
  Stop, state the trade-off, ask the user.
- **Static-power wall.** The remaining gap is dominated by static/leakage power
  that only a device/thermal decision can move. Present device/cooling options
  and STOP.
- **Low-confidence ceiling.** All numbers are vectorless Low/Medium confidence
  and the user needs signoff-grade dynamic power. Stop and request a SAIF from
  post-implementation simulation; do not present the estimate as final.

Never thrash: if a change doesn't help, revert it and move to the next table
row rather than re-trying variants of the same lever.

## Safety rails (do not violate)

- **Evidence before claims.** "Power reduced from X W to Y W" REQUIRES a fresh
  `report_power` from a completed implementation run — never inferred from
  synthesis, never from a stale run, never extrapolated. Always state the
  **confidence level** of the number you quote.
- **Timing and DRC are gates, not afterthoughts.** Every iteration MUST verify
  `report_timing_summary` (no new negative slack) and `report_drc` (no new
  violations). A lower power number on a now-failing design is a regression.
- **No fake-pass.** Do NOT make the power number "look good" by switching the
  report to an optimistic activity assumption, lowering the default toggle
  rate, or quoting a Low-confidence vectorless estimate as final. Do NOT silence
  a real DRC/methodology violation to clear the path. If you must assume a
  switching activity, state the assumption explicitly.
- **Smallest safe change first.** Strategy/constraints/IP-config before RTL.
  Recommend RTL and architectural edits (clock gating, operand isolation,
  enable gating) — show the file and lines, and get user approval before
  `update_file` / `replace_in_file`. Never silently rewrite RTL for power.
- **Never trade away met timing or correctness for power** without explicit user
  sign-off. Lowering frequency, gating clocks, or shrinking memories can change
  functional behavior or break timing — surface the consequence first.
- **Static power honesty.** Do not claim RTL or constraint changes will
  meaningfully reduce static/leakage power. State plainly that static power is a
  device/speed-grade/junction-temperature property and route those to a human
  decision.
- **One change-class per iteration** so the before/after delta is attributable.
- **Real tools only.** Use only the SynthPilot tool names referenced here. If a
  capability is missing (e.g. automated SAIF annotation), say so rather than
  inventing a tool.

## Output

Produce a concise power report, not a narrative:

1. **Baseline:** total power (W), dynamic/static split, top 3 categories with
   their watts/percent, junction temp + thermal margin, target part, and the
   report **confidence level**.
2. **Findings:** the dominant movable category and its root cause (per the
   classification table).
3. **Change log (per iteration):** what change-class was applied (strategy /
   constraint / IP / recommended-RTL), and the before→after numbers for total
   power, the targeted category, WNS, and DRC status. Show your work.
4. **Result:** final total power and dynamic/static split from the LAST
   implemented `report_power`, with confidence level, plus confirmation that
   `report_timing_summary` and `report_drc` are still clean. Quantify the
   reduction vs baseline (W and %).
5. **Remaining options (if stopped before goal):** the exhausted-safe-options
   list — RTL/architectural edits, device/speed-grade/board changes, cooling
   changes, or a SAIF-driven re-measure for signoff — each with its cost and
   risk. Hand back to the human; do not proceed unilaterally.
6. **Caveat:** if numbers are vectorless Low/Medium confidence, state that
   dynamic-power figures are estimates and signoff requires a SAIF-annotated
   re-measure.