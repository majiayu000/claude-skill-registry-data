---
name: constraints-authoring
description: >
  Author a correct Vivado XDC timing constraint set from scratch — primary
  clocks, generated (derived) clocks, input/output delays, and timing exceptions
  (clock groups / false paths / multicycle paths) — for a design that has no
  constraints yet, or whose constraints are incomplete (unconstrained ports,
  missing generated clocks, unrelated async clocks reported as failing paths).

  Invoke when the user says: "write constraints", "author xdc", "set up timing
  constraints", "no constraints yet", "constrain my clocks", "add input/output
  delays", "my clocks are asynchronous / I need clock groups", or whenever
  check_timing / report_timing_summary reports unconstrained clocks, ports, or
  combinational endpoints. This is the FIRST step before any timing-closure or
  signoff work — WNS/TNS numbers are meaningless until the design is correctly
  constrained.

  Requires the SynthPilot MCP server connected to an OPEN Vivado session with the
  Tcl server running (test_connection must pass) and a project that elaborates
  and synthesizes.
---

# Constraints Authoring (XDC from scratch)

A methodology playbook for writing a **correct, complete, and honest** XDC
constraint set. The goal of constraints is to tell the timing engine the truth
about the design's real timing requirements — not to make WNS look good. A
constraint that lies (a too-loose clock, a false_path on a real path) produces a
green report that does not survive on silicon. **Correctness first, optimism never.**

This skill stops at a **timed, sane, signed-off constraint set** plus a clear
list of any assumptions you had to make. It does NOT attempt timing closure
(that is the timing-closure skill's job). It hands off once timing is *defined*,
not *met*.

---

## When to use

- A project has **no XDC** at all, or no timing constraints (only pin/IO
  assignments) — the classic "no constraints yet".
- `check_timing` / `report_timing_summary` reports **unconstrained** clocks,
  ports, or combinational endpoints (e.g. "There are N input/output ports with
  no input/output delay specified").
- The design has **PLL/MMCM/clock-divider outputs** that are missing
  **generated-clock** definitions (derived clocks defaulting to the source
  period, or showing up as unconstrained).
- Multiple **asynchronous clock domains** exist and inter-clock paths are being
  analyzed (and failing) when they should be cut with `set_clock_groups`.
- You need to add **I/O timing budgets** (`set_input_delay` / `set_output_delay`)
  for a board interface.
- A legitimate **multicycle** or **false** relationship exists that the tool
  cannot infer and is currently over-constraining.

## When NOT to use

- **Timing is already fully constrained and you are trying to close it**
  (improve WNS/TNS). Use the **timing-closure** skill — do NOT "fix" timing by
  adding exceptions here.
- **CDC is the question** ("is my clock crossing safe?"). Constraining async
  clocks with `set_clock_groups` *silences* the cross-domain timing report; it
  does **not** make the crossing safe. Use the **cdc-analysis** skill to verify
  synchronizers exist before/after you group clocks. (This skill will tell you
  when to stop and call it.)
- **Pure pin/placement assignment** (LOC/IOSTANDARD only, no timing). Those are
  `create_io_constraint`; that part is in-scope here but if there is no timing
  question at all this skill is overkill.
- **You don't know the board/interface timing numbers.** Do not invent input/
  output delays. Ask the user for the datasheet/board numbers, or state the
  assumption explicitly and flag it.

---

## Prerequisites (verify first)

Run these BEFORE writing anything. Do not skip — a wrong period or a clock on a
non-existent port wastes a full synthesis.

1. `test_connection` — confirm the MCP↔Vivado Tcl bridge is alive. If this
   fails, stop: nothing below will work.
2. `get_project_info` — confirm a project is open and know the **target part**
   (speed grade matters; constraints are part-agnostic but I/O delay budgets are
   not).
3. `list_source_files` + `set_top_module` (if not set) — you must constrain the
   *top-level* ports. Constraining ports that aren't on top is a silent no-op.
4. `list_constraint_files` — find what already exists. If there is an XDC, you
   are **editing**, not creating from scratch; `read_file` it first and do not
   duplicate clock definitions.
5. **Establish the design intent** — from the user and/or `read_file` on the top
   module: every clock port and its frequency, which clocks are generated (PLL/
   MMCM/divider), which clock domains are asynchronous to each other, and the
   board-level I/O timing (source-synchronous vs system-synchronous). If any of
   these is unknown, **ask the user** — do not guess clock periods.

> You author constraints **at elaboration/RTL level** (against port and pin
> names), but you VERIFY them against a real **synthesized netlist** where pin
> paths (`pll/CLKOUT0`, `reg[*]/C`) actually exist. Authoring uses port names;
> verification needs `open_synthesized_design`.

---

## Methodology

Author in **dependency order**: clocks → generated clocks → I/O delays →
exceptions. Each later layer references names defined by an earlier one, so order
is not optional. **One constraint class per step**, then re-measure, so you can
attribute every change in the timing report to exactly one edit.

### 1. Inventory what exists and what's missing

- `check_timing` — the single most important diagnostic. It reports unconstrained
  clocks, missing input/output delays, combinational loops, and (critically)
  appends the **full port inventory** so you can cross-reference which ports still
  lack constraints. Read it carefully; it is your worklist.
- `get_all_clocks` — what clocks (if any) Vivado has already inferred. Empty =
  truly from scratch. Non-empty = some clocks exist (maybe from IP); do not
  redefine them.
- If clocks already exist, `get_clock_info(<name>)` per clock to see period and
  source — confirm they match intent before building generated clocks on top.

> If `check_timing` cannot run because nothing is elaborated, run
> `run_synthesis_async` once to get a netlist, poll `get_run_status`, then
> `open_synthesized_design`. You need a netlist to see real clock pins anyway.

### 2. Define PRIMARY clocks (the foundation)

For every **physical clock input port** (an oscillator/board clock entering the
FPGA), one `create_clock_constraint`:

- `create_clock_constraint(clock_port="<top clock port>", period_ns=<period>, name="<clk_name>")`
- Period = `1000 / freq_MHz`. Use the **real** board frequency from intent, not a
  hopeful one. A 100 MHz oscillator is `period_ns=10.0`.
- **Only create primary clocks on true clock inputs**, never on internal PLL/MMCM
  outputs — those are *generated* clocks (Step 3). Defining a primary clock on a
  PLL output double-counts and corrupts analysis.
- Give every clock an explicit `name` so later steps and reports are readable.

After defining all primary clocks, `get_all_clocks` to confirm each appears with
the intended period.

### 3. Define GENERATED clocks (PLL/MMCM/divider outputs)

Any clock **derived inside the FPGA** needs an explicit generated clock so the
engine knows the true frequency/phase relationship:

- PLL/MMCM outputs: `create_generated_clock(name="<clk_out>", source="<pll>/CLKIN1", target="<pll>/CLKOUT0", multiply_by=M, divide_by=D)`
  — M/D from the IP's actual configuration (e.g. 100→200 MHz is `multiply_by=2`).
- RTL clock dividers: `create_generated_clock(name="clk_div2", source="<clk_in port>", target="<div_reg>/Q", divide_by=2)`.
- Phase-shifted outputs: add `phase=<deg>` (e.g. a 90° clock for source-sync DDR).
- Inverted/negedge-derived clocks: `invert=True`.
- Use `multiply_by`/`divide_by` for simple ratios; `edges`/`edge_shift` only for
  genuinely non-integer or asymmetric waveforms.

**Source/target are PIN paths, not ports** — they only exist on the synthesized
netlist. Author them, then **prove** them in Step 7 with `report_clock_networks` /
`get_all_clocks`. If a generated clock shows up with the wrong period after
synthesis, the M/D or the target pin is wrong — fix it, don't paper over it.

> Many IP cores (Clocking Wizard, MIG, transceivers) ship their OWN generated
> clocks in their `.xdc`. Check `report_clock_networks` / the IP's constraints
> first; **do not redefine** a clock the IP already constrains, or you create a
> conflicting double definition.

### 4. Relate or separate the clocks (groups / uncertainty)

Now that all clocks exist, declare their **relationships** — this is where most
"failing paths" on a fresh design come from, and where the biggest honesty risk
lives.

- **Asynchronous domains** (clocks from independent sources / unrelated PLLs):
  `set_clock_groups(group1="<clkA>", group2="<clkB>", relationship="asynchronous")`.
  This tells timing not to analyze paths between them.
  **HARD GATE:** only do this for a crossing that is **genuinely asynchronous AND
  has a proper CDC synchronizer**. Grouping clocks does not synchronize them — it
  hides the report. See the classification table and Safety rails. If unsure
  whether a synchronizer exists, **stop and ask / run cdc-analysis**; do not
  group blindly.
- **Mux-selected / never-simultaneous clocks**: use `relationship="exclusive"`
  (or `logically_exclusive`/`physically_exclusive`) — not `asynchronous`.
- **Synchronous, related clocks** (e.g. PLL outputs that are integer multiples of
  the same source): do **NOT** group them — they must be analyzed together. Only
  add `set_clock_uncertainty(<jitter_ns>, clock="<clk>")` to model PLL jitter/
  board skew if you have a real number; otherwise leave the tool's default.

### 5. Budget the I/O timing (input/output delays)

For every top-level data port that crosses the chip boundary and isn't a clock,
add a delay so timing knows the external budget:

- Inputs: `set_input_delay(port_name="<port>", delay_ns=<board_delay>, clock_name="<launch clk>")`.
- Outputs: `set_output_delay(port_name="<port>", delay_ns=<board_delay>, clock_name="<capture clk>")`.
- Numbers come from the **interface spec / board**: trace delay + external device
  tco/tsu (system-synchronous), or the source-synchronous skew window. **Do not
  fabricate these.** If the user can't supply them, either (a) state an explicit
  placeholder assumption and flag it loudly in the Output, or (b) ask. A
  guessed-zero delay is a silent lie that passes in the lab and fails in the field.
- Pure asynchronous control inputs with no real launch edge (some resets,
  push-buttons) are NOT given a meaningful I/O delay — they're handled as false
  paths in Step 6.
- Pin location / IOSTANDARD (separate from timing) via
  `create_io_constraint(port_name, pin, io_standard)` if the board pinout isn't
  already in a pin XDC.

### 6. Add genuine exceptions — narrowly, with a stated reason

Exceptions tell the tool to relax analysis. Each one is a claim about the
design's behavior. **Every exception requires a one-line justification, and if
the path could be real, ask the user before adding it.** Prefer the narrowest
tool.

- **Async reset distribution** (reset asserted async, deasserted synchronously
  through a reset synchronizer): `set_false_path(from_signal="<rst>", from_type="port")`.
  Justification: "reset is recovered through a synchronizer; the async assert edge
  has no timing requirement." If there is NO reset synchronizer, this is a bug —
  do not false_path it; flag it.
- **Static / quasi-static config registers** read by a faster clock but written
  rarely: `set_multicycle_path(N, from_signal="<src_reg>[*]/C", to_signal="<dst_reg>[*]/D")`
  with a justification of why N cycles are guaranteed by the protocol. Hold MCP is
  auto-adjusted; verify it.
- **CDC datapath that's already synchronized** but you want a bounded skew instead
  of fully cutting it: `set_max_delay(<period_ns>, from_node, to_node, datapath_only=True)`
  (and/or `set_bus_skew` for a multi-bit bus through a handshake/gray-code). This
  is safer than `set_clock_groups` because it still bounds the path.
- Single mux-exclusive clock structures: prefer `set_clock_groups
  relationship="logically_exclusive"` over a pile of false paths.

**Never** add an exception merely because a path is failing setup/hold. A failing
*real* path is a timing-closure problem, not a constraints problem.

### 7. VERIFY against a synthesized netlist (mandatory)

Constraints written against RTL are unproven until checked against real clock
networks and pins. Do this every time:

- `save_constraints(file_name="timing.xdc")` then ensure it's in the project
  (`add_constraint_file` / `list_constraint_files`). Or author the file directly
  with `create_constraint_file(file_name, content)` for full control of ordering.
- `run_synthesis_async` → poll `get_run_status` until done → `open_synthesized_design`.
- `check_timing` — **the unconstrained-objects count must drop to the intended
  set** (zero, except objects you deliberately left as no-timing async). Any
  remaining "no clock"/"no input delay" is an unfinished constraint, not a pass.
- `get_all_clocks` + `report_clock_networks` — confirm **every** clock (primary
  and generated) appears with the **correct period and source**. A generated
  clock at the wrong frequency = wrong M/D.
- `report_clock_interaction` — the clock-pair matrix. Confirm: related clocks are
  **Timed**, intentionally-async pairs are **Ignored/partial** *because you grouped
  them on purpose*, and no pair you expected to be timed is silently ignored. This
  is the honesty check on Step 4.
- `report_timing_summary` — sanity only. At this stage you care that paths are
  *being analyzed correctly*, not that WNS is positive. **Do not** declare success
  on WNS here; that's closure/signoff.

### 8. Finalize

- `save_constraints` the verified file; confirm it's the one in the project.
- Produce the Output report (below): every clock, every delay, every exception
  with its justification, and every assumption you had to make.
- If real timing analysis is now needed → hand off to **timing-closure**. If any
  async grouping was added → hand off to **cdc-analysis** to verify the
  synchronizers. State the handoff explicitly.

---

## Classification: symptom → likely cause → smallest correct constraint

Use this to decide *which* constraint, not just *that* a constraint is needed.

| Symptom (from check_timing / clock reports) | Likely cause | Smallest correct fix | Honesty gate |
|---|---|---|---|
| "Clock <port> has no create_clock" | Primary clock undefined | `create_clock_constraint` with real period | Period must be the **real** board freq, not a wish |
| PLL/MMCM output clock missing or at source period | Generated clock undefined | `create_generated_clock(multiply_by/divide_by from IP config)` | M/D must match the IP's actual config |
| N input/output ports "no input/output delay" | I/O unbudgeted | `set_input_delay`/`set_output_delay` from interface spec | Numbers from datasheet/board — never fabricated |
| Inter-clock paths failing between unrelated clocks | Async domains analyzed as if related | `set_clock_groups(... asynchronous)` | ONLY if a real CDC synchronizer exists — else CDC bug, do not group |
| Mux-selected clocks both timed against each other | Tool can't infer mutual exclusivity | `set_clock_groups(... logically_exclusive)` | The mux must truly make them mutually exclusive |
| Path from slow config reg to fast logic fails setup | Real multicycle relationship | `set_multicycle_path(N, ...)` | N must be guaranteed by the protocol, justified |
| Async reset/async input path fails | Async assert with sync recovery | `set_false_path(from_signal=rst, from_type=port)` | A reset **synchronizer must exist**; else flag bug |
| Generated clock at wrong frequency after synth | Wrong M/D or wrong target pin | Fix `create_generated_clock` args | Re-verify with `report_clock_networks` — do not waive |
| Combinational loop reported | RTL bug, not a constraint | **Do not constrain around it** | Report to user — this is an RTL fix |

---

## Iterate: author → synthesize → verify → refine (LOOP)

Constraints are correct only when proven on a netlist. Loop **one constraint
class at a time**:

1. **MEASURE** — `check_timing` + `report_clock_interaction` + `report_clock_networks`.
   Record: unconstrained-object count, which clock pairs are Timed/Ignored,
   generated-clock periods.
2. **CLASSIFY** — use the table to pick the single smallest correct constraint for
   the top remaining gap.
3. **APPLY ONE CLASS** — add only that class of constraint this iteration
   (all primary clocks, OR all generated clocks, OR I/O delays, OR one exception
   family). Save.
4. **RE-SYNTHESIZE & RE-MEASURE** — `run_synthesis_async` → `get_run_status` →
   `open_synthesized_design` → repeat Step 1's measurements.
5. **SHOW YOUR WORK** — before/after for this iteration: unconstrained count
   went X→Y, clock pair Z went Ignored→Timed (or the reverse, on purpose).

### STOP conditions (stop looping and report)

- **DONE:** `check_timing` shows **zero unintended** unconstrained objects; every
  clock present at correct period/source in `report_clock_networks`; every clock
  pair in `report_clock_interaction` is Timed-or-intentionally-Ignored with a
  stated reason. → Finalize (Step 8). Note: this is **constraints complete**, not
  **timing met**.
- **NEEDS HUMAN INPUT:** a clock period, an I/O delay number, or an async/CDC
  relationship is unknown and cannot be derived. → Present what's known, list the
  exact unknowns, **stop and ask**. Do not guess.
- **NOT A CONSTRAINTS PROBLEM:** the gap is an RTL/architecture issue (combinational
  loop, missing synchronizer, a genuinely failing real path). → Present the
  finding, recommend the RTL/CDC fix, hand off — do **not** add an exception to
  hide it.
- **THRASHING:** two consecutive iterations don't reduce unintended-unconstrained
  count or you're toggling a constraint back and forth. → Stop, surface the
  trade-off (e.g. "this crossing is either a real CDC bug or needs a synchronizer
  before I can group it"), hand back to the human.

---

## Safety rails (do not violate)

- **No fake-pass / no silencing.** Never add `set_false_path`,
  `set_clock_groups(asynchronous)`, `set_multicycle_path`, or
  `waive_lint_violation` to make a *real* path's violation disappear. An exception
  is a factual claim about the hardware; if it could be false, **ask the user
  first** and record the assumption. WNS going green because you cut a path is not
  closure — it's a hidden bug.
- **Async grouping ≠ CDC safety.** `set_clock_groups(asynchronous)` removes the
  cross-domain path from analysis; it does NOT add a synchronizer. Only group
  domains that already have proper CDC structures. When you add any async group,
  you MUST flag it for cdc-analysis in the Output.
- **Real numbers only.** Clock periods come from the actual oscillator/IP; I/O
  delays come from the interface spec/board. Never fabricate a period or a delay
  to make a report look good. If unknown → ask or flag a stated assumption.
- **Smallest safe change, in order.** Constraints/strategy before RTL. Define
  clocks before exceptions. Prefer the narrowest tool: bound a CDC path with
  `set_max_delay(datapath_only=True)` rather than wholesale `set_clock_groups`
  when you only need a skew bound.
- **Primary vs generated discipline.** Never `create_clock_constraint` on a PLL/
  MMCM output or a derived clock — that double-defines and corrupts analysis. Those
  are always `create_generated_clock`.
- **Don't redefine IP-owned clocks.** If a Clocking Wizard / MIG / transceiver IP
  already constrains a clock (check `report_clock_networks` / its XDC), do not add
  a conflicting definition.
- **Recommend RTL, don't silently rewrite it.** If the correct fix is a reset
  synchronizer, a CDC FIFO, or a logic change, *report it* and let the human
  decide. This skill edits constraints, not source.
- **Evidence before claims.** "Constraints complete" REQUIRES fresh
  post-synthesis `check_timing` + `report_clock_networks` + `report_clock_interaction`
  output in this session — never inferred from the RTL or from a prior run. Any
  signoff-level timing claim (timing met) requires post-**implementation**
  evidence and belongs to the timing-closure/signoff flow, not here.
- **One change-class per iteration** so cause→effect in the timing report is
  attributable.

---

## Output

Return a concise, evidence-backed report:

1. **Scope** — created from scratch vs. completed an existing XDC; target part.
2. **Clocks defined** — table of every clock: name, type (primary/generated),
   source, period (ns) / frequency (MHz), M/D or phase for generated, **verified
   period from `report_clock_networks`** (proves it, doesn't just assert it).
3. **Clock relationships** — every `set_clock_groups` / uncertainty, with the
   relationship and a one-line reason; the relevant rows of
   `report_clock_interaction` showing the matrix is as intended.
4. **I/O delays** — table of port → delay → reference clock, and the **source** of
   each number (datasheet / board / **assumed (flagged)**).
5. **Exceptions** — every false_path / multicycle / max_delay with its one-line
   **justification** and whether the user confirmed it.
6. **Verification evidence** — fresh `check_timing` unconstrained-object count
   (before → after, ideally → 0 unintended), confirmation all clocks appear
   correctly, and that the clock-pair matrix matches intent. Quote the numbers.
7. **Assumptions & open questions** — every value you had to assume or guess,
   called out explicitly for the user to confirm.
8. **Handoff** — explicit next step: timing-closure (to actually meet timing) and/
   or **cdc-analysis** (mandatory if any async clock group was added) — naming the
   skill, not silently ending.

> Honesty footer to include verbatim when relevant: *"Constraints are complete
> and verified against the synthesized netlist. This means timing is now correctly
> DEFINED — it does not mean timing is MET. Any async clock groups I added assume a
> working CDC synchronizer exists; verify with cdc-analysis before signoff."*