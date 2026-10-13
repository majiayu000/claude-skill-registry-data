---
name: qor-report
description: >
  Produce a one-page FPGA design-health scorecard (QoR: timing, area, power,
  congestion, clocking, DRC/methodology). Invoke when the user asks for a
  "design health" check, a "QoR" report, "quality of results", a "scorecard",
  "how good is my design", "is this ready for signoff", or wants a single
  consolidated read on timing/area/power/congestion after synthesis or
  implementation. Requires the SynthPilot MCP server (Vivado open with the Tcl
  server running on TCP:9999). This is a READ-ONLY measurement-and-grading
  playbook: it gathers fresh tool evidence, grades each axis, and reports — it
  does not modify constraints, RTL, or strategy.
---

# QoR Report — Design-Health Scorecard

A QoR (Quality of Results) report is a **measurement task, not a fix task**. The
goal is one page that tells the user, with grades and hard numbers, how healthy
the design is across six axes — **Timing, Area/Utilization, Power, Congestion,
Clocking, and Rule-cleanliness (DRC/methodology/CDC)** — and what the single most
important problem is. Every number on the scorecard must come from a **fresh tool
call against the currently open design**, not from memory, not from a prior run,
and not inferred.

## When to use

- User says "design health", "qor", "quality of results", "scorecard", "how good
  is my design", "rate my implementation", "is this ready for signoff/tapeout".
- After a run (synthesis or implementation) completes and the user wants a single
  consolidated read instead of opening ten separate reports.
- Before a design review or sign-off gate, to get an objective snapshot.
- To compare two strategies/checkpoints: run this skill on each and diff the
  scorecards.

## When NOT to use

- **The user wants you to FIX something** (close timing, reduce area, cut power,
  relieve congestion). This skill diagnoses and grades only. Hand off to the
  timing-closure / area / power / congestion remediation skills. This skill may
  *recommend* those as next steps but must not apply constraints, strategy
  changes, or RTL edits.
- **No design is built yet** (no completed synthesis or implementation run). A
  scorecard on an empty/elaborated-only design is meaningless. Build first (see
  Prerequisites), or state clearly that you can only report a "pre-build" status.
- **The user wants deep root-cause on one axis** (e.g. "why is path X failing").
  Use the focused report tools / timing-closure skill, not a one-page summary.
- **Functional correctness questions** (does the RTL do the right thing). That is
  simulation/lint territory, not QoR.

## Prerequisites (verify first)

Do these in order. Do not skip — a scorecard built on the wrong design stage is
worse than no scorecard.

1. **MCP/Vivado alive.** Call `test_connection`. If it fails, stop and tell the
   user to open Vivado and start the Tcl server (TCP:9999). Optionally
   `vivado_version` to record the tool version on the scorecard.
2. **A project is open.** Call `get_project_info`. Capture **part/device**,
   project name, and top module — these go in the scorecard header. If no
   project is open, stop and ask the user to `open_project`.
3. **Determine the design stage — this decides what the scorecard can claim.**
   Call `get_run_status`.
   - **Implementation complete (placed + routed):** full scorecard is possible;
     all six axes are signoff-grade. This is the preferred input.
   - **Synthesis complete only:** you can grade Timing (estimated), Area, and
     Clocking, but you must **label them ESTIMATE / pre-route**. Power and
     congestion are not trustworthy. State this explicitly.
   - **Nothing built:** STOP. Offer to build (next step) or report pre-build only.
4. **Open the correct in-memory design** so the report tools have data:
   - If implemented: `open_implemented_design`.
   - If synthesized only: `open_synthesized_design`.
   - If nothing built and the user agrees to build, kick off a build with the
     **async pattern** (implementation runs are multi-minute):
     `run_implementation_async`, then poll `get_run_status` until complete, then
     `open_implemented_design`. (Use `run_synthesis_async` + poll if the user
     only wants a synthesis-stage card.) Never block on a synchronous multi-minute
     call when an async + poll path exists.
5. **Record the stage label** ("post-route signoff" vs "post-synth estimate") at
   the top of the scorecard. Every grade inherits this caveat.

## Methodology (gather → grade → report)

This skill is **single-pass and read-only**. There is no fix loop. The loop, if
any, is only "build if not built, then measure". Collect each axis's evidence
with the listed tool, grade it against the rubric, then assemble the one-pager.

### 1. Timing
- `report_timing_summary` — the authoritative WNS/TNS/WHS/THS, failing endpoint
  count, and number of timing-violating paths across all clocks.
- `extract_timing_metrics` — structured WNS/TNS/TPWS and per-clock margins for the
  scorecard table (easier to parse than the raw summary).
- If WNS < 0 or the user wants detail, `report_worst_timing_paths` (top N) to name
  the worst path and its clock — but only to *report* it, not to fix it.
- `check_timing` — flags unconstrained / problematic timing setup (no-clock,
  partial input/output delays, combo loops). A design that "meets timing" with
  large unconstrained sections is a **false green**; surface the unconstrained
  count prominently.

### 2. Area / Utilization
- `report_utilization` — LUT, FF, CARRY, DSP, BRAM, URAM, IO percentages.
- `report_utilization_hierarchical` — only if a module is over budget and the user
  wants to know *which* block is the hog (still reporting, not fixing).
- Record both **absolute counts and % of device**. The % drives the grade; the
  hierarchy explains it.

### 3. Power
- `report_power` (post-implementation only for a real number) — total on-chip
  watts, dynamic vs static split, thermal margin / junction temp, and **the
  confidence level Vivado reports** (High/Medium/Low). A "Low confidence" power
  number must be labeled as such on the card — do not present it as signoff power.
- If synthesis-stage only, mark power **N/A (requires implementation)** rather than
  reporting a misleading estimate.

### 4. Congestion (placement/routing pressure)
- `report_congestion` (post-place/route only) — per-direction congestion levels and
  the worst window. This is the leading indicator of why routing/timing struggle.
- `report_route_status` — routed vs unrouted/partially-routed nets, conflicts. Any
  non-zero unrouted or conflict count is a **hard fail** on the routing axis; the
  design is not actually built even if other numbers look fine.

### 5. Clocking
- `report_clock_utilization` — BUFG/MMCM/PLL usage and headroom.
- `get_all_clocks` / `report_clock_networks` — confirm every intended clock exists
  and is driven. A primary clock that Vivado did not create (typo'd `create_clock`)
  silently makes huge swaths of logic unconstrained — cross-check against the
  `check_timing` unconstrained finding from axis 1.
- `report_clock_interaction` — for multi-clock designs, which clock pairs are
  related/unrelated/asynchronous, so the timing grade can be read in context.

### 6. Rule-cleanliness (DRC / methodology / CDC)
- `report_drc` — design-rule violations. Categorize by severity. Any **Error**-level
  DRC is a hard fail for signoff.
- `report_methodology` — methodology (TIMING-*, etc.) checks that DRC misses; these
  are the strongest signal that a green timing number is real vs accidental.
- `report_cdc` — clock-domain-crossing safety. CDC criticals are a signoff blocker
  even when timing/area/power are perfect. (Run on the synthesized or implemented
  design; report counts by severity.)

### 7. Suggestions (Vivado's own QoR opinion)
- `report_qor_suggestions` — Vivado's built-in QoR analysis and recommendations.
  Include the top suggestions verbatim as "Vivado recommends", clearly separated
  from your own grading. Do **not** auto-apply any suggestion.
- `report_design_analysis` — complexity/congestion/timing characterization to back
  up the grades with second-source evidence where available.

### 8. Assemble the one-pager
Collapse the evidence into the scorecard (see Output). Compute an overall
verdict from the worst axis, not the average — a single Error DRC or an unrouted
net caps the whole design at FAIL regardless of how good timing looks.

## Grading rubric (symptom → grade → meaning)

Grade each axis PASS / MARGINAL / FAIL using **post-route** numbers. Thresholds
are engineering defaults; state them on the card so the user can recalibrate for
their device/process.

| Axis | PASS (green) | MARGINAL (amber) | FAIL (red) | Source tool |
|------|--------------|------------------|------------|-------------|
| Timing (setup) | WNS ≥ 0 **and** 0 unconstrained paths | 0 ≤ WNS < ~5% of period, or WNS≥0 but unconstrained paths exist | WNS < 0 (TNS < 0) | `report_timing_summary`, `extract_timing_metrics`, `check_timing` |
| Timing (hold) | WHS ≥ 0 | WHS ≥ 0 small margin | WHS < 0 (THS < 0) | `report_timing_summary` |
| Utilization | every resource < 80% | any resource 80–90% | any resource > 90% (or any over 100% = won't fit) | `report_utilization` |
| Power | within thermal budget, confidence High/Med | near thermal limit, or Low confidence | exceeds thermal/junction limit | `report_power` |
| Congestion | levels low (≤ ~level 4 / Vivado's "low") | medium congestion windows | high congestion / unroutable region | `report_congestion` |
| Routing | 100% routed, 0 conflicts | — (routing is binary) | any unrouted net or conflict | `report_route_status` |
| Clocking | all clocks created+driven, clock-region/BUFG headroom OK | tight BUFG/MMCM headroom | missing/undriven clock, or over-subscribed clocking | `report_clock_utilization`, `get_all_clocks`, `check_timing` |
| DRC / methodology | 0 Errors, warnings reviewed | Warnings only | any Error-severity DRC, or TIMING-* methodology error | `report_drc`, `report_methodology` |
| CDC | 0 Critical, 0 unsafe | warnings/cautions only | any Critical / unsafe crossing | `report_cdc` |

**Overall verdict = the worst single axis.** Any FAIL ⇒ overall **NOT READY FOR
SIGNOFF**. All PASS ⇒ **HEALTHY**. Mix of PASS/MARGINAL ⇒ **CONDITIONAL — review
amber items**.

## Build-if-needed loop (the only loop) + STOP conditions

This skill does not iterate on fixes. The only loop is producing a valid input:

```
Loop:
  status = get_run_status
  if implementation complete  -> open_implemented_design ; MEASURE ; STOP
  if synthesis complete only  -> ask: want post-synth ESTIMATE card, or build impl?
       - estimate card        -> open_synthesized_design ; MEASURE (labeled estimate) ; STOP
       - build impl           -> run_implementation_async ; poll get_run_status ; (next loop)
  if nothing built            -> ask user to build; if yes run_synthesis_async/run_implementation_async + poll
  if a build is RUNNING        -> poll get_run_status (async pattern); do not start another run
```

**Hard STOP conditions (stop and hand back to the human):**
- A requested build **errors** (`get_run_status` reports failure) — surface
  `get_implementation_warnings` / `get_synthesis_warnings` and stop. Do not retry
  blindly or change strategy to force a pass.
- Any **Error-severity DRC**, **unrouted net/conflict**, or **CDC Critical** is
  found — the scorecard is complete (it correctly reports FAIL); stop, do not
  "fix" it to make the card green.
- Evidence is **internally inconsistent** (e.g. timing summary says met but
  `report_route_status` shows unrouted nets) — report the contradiction and stop;
  do not paper over it.
- The user only wanted a report — once the one-pager is delivered, **STOP**.

## Safety rails (do not violate)

- **Read-only.** This skill measures and grades. It MUST NOT call
  `set_false_path`, `set_multicycle_path`, `set_max_delay`,
  `set_clock_groups`, `waive_lint_violation`, `set_synthesis_strategy`,
  `set_implementation_strategy`, or edit RTL/constraints. The only allowed
  mutating action is *building the design itself* (`run_synthesis_async` /
  `run_implementation_async`) and only with the user's agreement.
- **No fake-pass / no green-washing.** Never waive a DRC, false-path a violation,
  or suppress a CDC/methodology finding to improve a grade. If a violation could
  be real, it stays on the card as a FAIL. Hiding a real problem to produce a
  prettier scorecard is the single worst failure mode of this skill.
- **Evidence before claims.** Every cell of the scorecard must trace to a tool
  call made **this session, against the currently open design**. Never reuse
  numbers from earlier in the conversation, never infer a number you didn't
  measure, never claim "timing met"/"DRC clean"/"CDC clean" without the fresh
  output in hand. Signoff-grade claims require **post-implementation** evidence;
  synthesis-stage numbers are necessary-but-not-sufficient and must be labeled
  ESTIMATE.
- **State the stage and the caveats.** A post-synth card must say so on every
  estimated axis. A "Low confidence" power number must say so. An unconstrained-
  paths count must be shown next to the timing grade.
- **Smallest-safe-change framing for recommendations only.** When you list "next
  steps", order them constraints/strategy before RTL, and present RTL/architectural
  changes as *recommendations to the human*, never as actions you will take here.
- **Surface trade-offs, then stop.** When you've reported the worst axis and the
  safe options to address it, present options + costs and hand back. Do not loop
  or thrash trying to drive a number green.
- **Real tools only.** Use only the tool names above. If the user wants something
  not covered by an available tool, say so plainly rather than inventing one.

## Output

Deliver a **single one-page scorecard** in this shape (fill from fresh tool
output; never leave a grade unsupported by a cited tool):

```
================ DESIGN HEALTH SCORECARD ================
Project : <name>        Top: <top_module>
Device  : <part>        Vivado: <version>
Stage   : POST-ROUTE (signoff) | POST-SYNTH (ESTIMATE)   <- caveat-bearing
Overall : HEALTHY | CONDITIONAL | NOT READY FOR SIGNOFF   <- = worst axis

AXIS            GRADE     KEY NUMBERS (with source)
-------------   -------   --------------------------------------------
Timing setup    PASS/..   WNS <ns>, TNS <ns>, <N> failing eps; <U> unconstrained
Timing hold     PASS/..   WHS <ns>, THS <ns>
Utilization     PASS/..   LUT <%>, FF <%>, DSP <%>, BRAM <%>, URAM <%>, IO <%>
Power           PASS/..   <W> total (dyn <W> / static <W>), Tj <C>, conf=<H/M/L>
Congestion      PASS/..   worst level <L> dir <H/V>; (post-route only)
Routing         PASS/..   <100%/partial> routed, <N> unrouted, <N> conflicts
Clocking        PASS/..   <N> clocks (all driven? y/n), BUFG <u/avail>, MMCM <u/avail>
DRC/Methodology PASS/..   <E> errors, <W> warnings (top: <code> ...)
CDC             PASS/..   <C> critical, <W> warning crossings

TOP PROBLEM   : <the single worst finding, one sentence, with its number>
VIVADO SAYS   : <top 1-3 report_qor_suggestions items, verbatim, not applied>
RECOMMENDED NEXT STEPS (not performed here):
  1. <constraint/strategy-level option + cost>
  2. <RTL/architectural option + cost — recommendation only>
EVIDENCE      : <list the tool calls this card is built from>
========================================================
```

Rules for the output:
- If a number could not be measured at this stage, write **N/A (requires
  implementation)** — never guess.
- Mark every estimated value with **(est.)** when the stage is post-synth.
- The **Overall** verdict equals the worst axis, never an average.
- Keep it to one screen. Detail lives in the underlying reports; offer to drill
  into any axis on request (and route fixes to the appropriate remediation skill,
  not this one).
