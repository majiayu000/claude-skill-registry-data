---
name: timing-closure
description: >-
  Close FPGA timing on a Vivado design driven by the SynthPilot MCP — iterate
  synthesis/implementation, diagnose critical paths, and apply the safest
  constraint/strategy fix until worst negative slack (WNS) and total negative
  slack (TNS) reach ≥ 0. Use when the user wants to close timing, fix negative
  WNS/TNS, resolve setup/hold violations, or asks why a design "doesn't meet
  timing". Requires the SynthPilot MCP (Vivado + Tcl server on :9999).
argument-hint: "[run name, target clock, or constraint to focus on (optional)]"
---

# Timing Closure

A disciplined loop that drives a Vivado design to timing closure using the SynthPilot
MCP tools. You are the conductor: measure → diagnose → classify → apply the *safest*
fix → re-measure → repeat. **Never make a number go green by hiding a real violation.**

## When to use
- "close timing", "fix WNS/TNS", "why doesn't this meet timing", "resolve setup violations"
- After synthesis or implementation reports negative slack.

## When NOT to use
- No project open / no design to analyze → set the project up first (or use `full-flow-demo`).
- The user wants a one-shot report only, not iteration → just call `report_timing_summary`.
- Hold (min-delay) violations dominate and routing is already done → these usually need
  Vivado's own hold-fix; surface that rather than looping.

## Prerequisites (verify first)
- `test_connection` succeeds (Vivado + Tcl server up).
- A project is open (`get_project_info`). If only RTL exists, run synthesis first.

## The loop

### Step 0 — Baseline (measure, don't guess)
1. Ensure a timed design exists. If none, `run_synthesis` (or `run_synthesis_async` +
   poll `get_run_status` for large designs). Synthesis WNS is optimistic — true signoff is
   post-implementation, but synth WNS is a fast first signal.
2. Read the numbers: `report_timing_summary`, then `extract_timing_metrics` for structured
   WNS/TNS/WHS/THS, failing-endpoint count, and per-clock breakdown.
3. Record the baseline (WNS, TNS, #failing endpoints, clocks involved). Every later
   iteration is compared against this. **State it to the user.**

If WNS ≥ 0 **post-implementation**: report closed, show the margin, stop. (Post-synth
positive is necessary but not sufficient — confirm with `run_implementation`.)

### Step 1 — Diagnose the worst paths
- `analyze_critical_paths` and `report_worst_timing_paths` → the top failing paths.
- For the worst path, `report_timing_path` / `report_datapath_delay` to split delay into
  **logic vs net vs clock-skew/uncertainty**.
- `report_high_fanout_nets` → fanout-driven net delay.
- `get_all_clocks` / `analyze_clock_domain_timing` / `report_clock_interaction` → is the
  failing path **intra-clock**, or a **cross-clock / async** path that shouldn't be timed
  at all?

### Step 2 — Classify the failure (this decides the fix)
Map the worst paths to one of these, in this priority order:

| # | Signature | Likely cause | Safe fix |
|---|---|---|---|
| A | Failing path crosses **unrelated/async clocks**, or is a config/quasi-static reg | Missing exception | `set_false_path` or `set_clock_groups` (async) / `set_multicycle_path` (multi-cycle) — **only if genuinely valid** |
| B | I/O path failing, no/incorrect input/output delay | Missing I/O constraint | `set_input_delay` / `set_output_delay` from the real interface spec |
| C | Big **net** delay, high fanout | Placement/fanout | implementation strategy (Performance_*), or recommend register duplication / `max_fanout` |
| D | Big **logic** delay, deep combinational path, intra-clock | Real logic depth | recommend RTL pipelining/retiming — do NOT fake-pass with exceptions |
| E | Small negative, close to met | Last-mile | `set_implementation_strategy` Performance_Explore / phys-opt; tighten nothing |

### Step 3 — Apply the smallest safe change
- **Constraints (A/B):** apply the specific exception, then `save_constraints`. Before any
  `set_false_path`/`set_multicycle_path`, **state the assumption** ("treating CDC path
  reg_a→reg_b as async; valid only if a synchronizer exists") and get confirmation if the
  path could be real.
- **Strategy (C/E):** `set_implementation_strategy` (e.g. Performance_ExplorePostRoutePhysOpt)
  / `set_synthesis_strategy`. Cheapest lever, try before touching RTL.
- **RTL (D):** describe the pipelining/retiming change and the expected slack gain;
  **recommend, don't silently rewrite** — hand back to the user to approve RTL edits.
- Apply **one class of change per iteration** so cause→effect is attributable.

### Step 4 — Re-measure
- Re-run the affected stage (`run_implementation` for signoff; `run_synthesis` if you
  changed RTL/synth strategy). Use the async variants + `get_run_status` for long runs.
- Re-read WNS/TNS via `extract_timing_metrics`. Compare to baseline and to the previous
  iteration. Did it improve, regress, or stall?

### Step 5 — Loop or stop
Repeat Steps 1–4 until **one** stop condition:
- ✅ **Closed:** WNS ≥ 0 (and WHS ≥ 0) post-implementation → report margin, list the
  changes applied, save constraints, stop.
- ⛔ **No safe move left:** remaining failures are class D (real logic depth) or require
  risky exceptions → stop, present the options + trade-offs, hand to the human.
- ⛔ **Stalled:** 2 consecutive iterations with no WNS improvement → stop, don't thrash.
- ⛔ **Budget:** a caller-specified max iterations reached.

## Safety rails (do not violate)
1. **No fake-pass.** Never apply `set_false_path`/`set_multicycle_path`/waivers to a path
   that could be real just to clear a violation. If unsure it's safe, ask.
2. **Evidence before claims.** "Timing met" requires a fresh post-implementation
   `extract_timing_metrics` showing WNS ≥ 0 — never infer it.
3. **Show your work.** Each iteration: report what you changed, why (which class), and the
   before/after WNS/TNS. Keep a running summary table.
4. **One change class per loop** so a regression is traceable.
5. **Hands off RTL** unless the user approves the specific edit.

## Output (each iteration + final)
```
Iter N | change: <what> (class <X>) | WNS <before> → <after> ns | TNS <before> → <after> | failing <n>→<m>
```
Final: closed/not-closed verdict, the ordered list of changes that worked, remaining risks,
and (if not closed) the recommended RTL/architectural next step.
