---
name: zynq-bringup
description: >-
  Stand up a Zynq-7000 PS7-based SoC block design (Processing System bring-up).
  Invoke when the user says "build a zynq soc", "ps7", "zynq bring up",
  "add a processing system", "PS-PL design", "bring up the ARM cores",
  "wire AXI GP/HP to the PL", "generate the bd wrapper for a Zynq", or asks to
  create / configure / validate a Zynq-7000 block design (FCLK, DDR, MIO/UART/GPIO,
  AXI interconnect, address map, wrapper). Requires the SynthPilot MCP server
  (AI-driven Vivado control) with Vivado open and the tcl_server.tcl TCP bridge
  running, and a PRO/MAX license (Block Design tools are gated). Zynq-7000 (PS7)
  only — NOT Zynq UltraScale+ MPSoC (use the mpsoc skill). Stop conditions: stop
  and ASK on unknown hardware-critical config (DDR part / board / target FCLK on a
  bare part); stop and HAND OFF on timing/DRC that fails after correct constraints;
  declare DONE only when bd_validate_design is clean AND post-implementation
  report_timing_summary (setup WNS/TNS >= 0 AND hold/min-delay >= 0), check_timing
  (no unconstrained endpoints), report_cdc, report_drc, and report_methodology are
  all clean on fresh runs.
---

# Zynq-7000 (PS7) Bring-Up

A methodology playbook for standing up a Zynq-7000 SoC: create a block design,
instantiate and configure the PS7 Processing System, wire PS↔PL AXI fabric with
clean clock/reset, assign and verify the address map, validate, generate the
HDL wrapper, then prove it through synthesis/implementation/DRC. This is a
**build-and-verify** flow, not a fix-it flow — but the rigor is the same:
**every "it works" claim is backed by fresh tool output**, never by assumption.

The PS7 is a hard ARM Cortex-A9 block. You do not write RTL for it — you
*configure* it (FCLKs, DDR, MIO peripherals, PS-PL AXI ports) and *wire* the PL
side to it correctly. Most bring-up failures are wiring/clocking/address errors,
not logic errors, so this skill measures the graph state at each step.

A critical fact that shapes the whole flow: **many wrong-but-plausible mistakes
pass `bd_validate_design` and even synthesis, and surface only at
post-implementation `report_drc` / `check_timing` / `report_cdc`** (wrong DDR
part, polarity-mismatched reset, unconstrained PL-side IO, missing CDC
constraints). The graph being "valid" is therefore never sign-off — only fresh
post-implementation evidence is.

---

## When to use

- User wants a fresh Zynq-7000 SoC scaffold: "build a zynq soc", "ps7 bring up".
- An existing project needs a PS7 added to a (new or existing) block design.
- User needs PS↔PL AXI plumbing: hang an AXI peripheral (GPIO, UARTlite, BRAM
  controller, custom AXI IP) off `M_AXI_GP0`, or feed a PL master into `S_AXI_HP0`.
- User needs FCLK / reset / address-map set up correctly and *verified*.
- User needs the BD validated, the HDL wrapper generated, and the design taken
  through synth/impl/bitstream as a sanity sign-off.
- User wants `export_hardware` (XSA) output for a downstream software/BSP flow.

## When NOT to use

- **Zynq UltraScale+ MPSoC** (`zynq_ultra_ps_e`, A53/R5). Use the MPSoC bring-up
  skill and `bd_create_mpsoc` / `bd_apply_mpsoc_preset` family — PS7 tools do not
  apply.
- **Pure PL / RTL-only designs** with no Processing System. Use the standard
  project + synthesis/timing skills.
- **Timing closure** of an already-built design — that is the timing-closure
  skill. (This skill *checks* timing as sign-off, it does not *close* it.)
- **Software / firmware** (BSP, FSBL, bare-metal app, debug of ARM code). That is
  the embedded (`emb_*`) flow; this skill stops at hardware handoff (XSA).
- **Detailed simulation** of the SoC — PS7 has no behavioral RTL model in this
  flow; verify PL logic standalone with the simulation skill.

---

## Prerequisites (verify first)

Do not start building blind. Confirm the environment and the part with tools:

1. `test_connection` — confirm the Tcl bridge to Vivado is live. If it fails,
   STOP and tell the user to open Vivado and start `tcl_server.tcl`. Nothing
   below works without this.
2. `get_license_status` — **required precondition.** Block Design (`bd_*`) tools
   are PRO/MAX tier. If the license is FREE, the `bd_*` calls below are blocked;
   surface this **now** and stop, rather than failing opaquely mid-flow.
3. `get_project_info` — is a project open, and **what is the target part?**
   - PS7 bring-up requires a **Zynq-7000** part (`xc7z…`, e.g. `xc7z020clg484-1`)
     or a Zynq board part. If the part is **not** Zynq-7000, STOP and ask the
     user — PS7 will not instantiate on a non-Zynq part, and silently guessing a
     part is a destructive surprise.
   - If no project is open, `create_project` with the user-confirmed part/board.
     **Ask** for the exact part or board before creating one; never invent it.
4. `list_block_designs` — is there already a BD? Reuse it (`open_block_design`)
   rather than creating a duplicate; only `create_block_design` if none exists or
   the user wants a fresh one.

Record the **part**, **board (if any)**, and **target FCLK frequency** before
proceeding — these drive every later decision (DDR config, MIO, automation).

---

## Board-aware vs. board-agnostic: the first decision

The single most important branch in PS7 bring-up is whether a **board part** is
set on the project. It changes how DDR/MIO get configured and whether you can
trust automation.

| Condition (from `get_project_info`) | DDR + MIO strategy | Automation | Risk |
|---|---|---|---|
| **Board part set** (e.g. Zedboard, Cora, Pynq) | `bd_create_ps7(run_automation=True)` — this runs Vivado's PS block automation (the underlying `apply_bd_automation` Tcl command, invoked **for you** by the MCP tool; do not call `apply_bd_automation` directly — it is not an MCP tool), filling DDR part, MIO pinout and FIXED_IO from the board file | Trust `bd_run_block_automation` for the PS | Low — board file is authoritative |
| **Bare part only** (`xc7z…`, no board) | `bd_create_ps7(run_automation=False)`, then **inspect** with `bd_get_ps7_config` and **explicitly set** DDR part / bus width / MIO via `bd_configure_ps7`. DDR config MUST match the physical board's memory or hardware will not boot | Do NOT trust block automation for DDR/MIO — it has no board data | **High — wrong DDR = dead board.** Ask the user for the DDR part / board if unknown |

> **Tool-name note:** `bd_create_ps7(run_automation=True)` and
> `bd_run_block_automation` are the **MCP tools**. `apply_bd_automation` /
> `run_bd_automation` are native Vivado Tcl commands those tools wrap — never
> call them as if they were MCP tools.

> **Bare-part DDR safety rail (read this).** On a bare part, do **not** invent DDR
> timing/part numbers to make validation pass. Be explicit that the tooling will
> **not** catch a wrong DDR part for you:
> - `bd_validate_design` will pass with a wrong-but-plausible DDR part.
> - Synthesis will pass — the DDR/FIXED_IO are hard-pinned PS pins, not logic.
> - `bd_get_ps7_config` readback only confirms the value you *wrote*, not that it
>   matches the physical board — it **cannot** detect a wrong DDR part.
> - The **only** automated gate that catches a missing/wrong DDR + FIXED_IO
>   pinout is **post-implementation `report_drc`** (UCIO / FIXED_IO / DDR no-pin
>   errors). Therefore, whenever you configure DDR on a bare part, the §13
>   post-impl `report_drc` gate is **mandatory** and is the decision's
>   verification — never skip it.
> If the DDR part is unknown, state the assumption explicitly and ask the user
> before configuring it.

---

## METHODOLOGY

One change-class per step, then **measure** before moving on. The recurring
verbs are: *configure → inspect (`bd_get_*` / `bd_list_*`) → connect →
re-inspect (`bd_get_unconnected_pins`) → validate*.

### 1. Open or create the block design
- `create_block_design(name=...)` (or `open_block_design` if reusing).
- Note the design name for `bd_generate_*` later.

### 2. Instantiate the PS7
- `bd_list_ps7_presets` — see available presets (`minimal`, `ddr_enabled`,
  `hp_slave`, `multi_clock`).
- `bd_create_ps7(name="ps7_0", preset=<chosen>, run_automation=<board-aware>)`:
  - **Board part set** → `run_automation=True` (exports DDR + FIXED_IO from board
    via the wrapped block automation).
  - **Bare part** → `run_automation=False` (you will configure DDR/MIO yourself).
- `bd_get_ps7_config(cell="ps7_0")` — **read back the actual state** (DDR, clocks,
  MIO/peripheral I/O, interrupts, PS-PL interfaces). This is your ground truth
  for *what was written* — but remember it does **not** prove DDR matches the
  board (see safety rail). Do not assume the preset did what its name implies;
  confirm it here.

### 3. Configure DDR and MIO (bare-part path only)
Skip if board automation already populated DDR/FIXED_IO (verify via
`bd_get_ps7_config` that DDR is configured before skipping).
- `bd_configure_ps7(cell="ps7_0", config="{...}")` to set the **board-correct**
  DDR part, bus width, and any MIO peripheral pinout the design needs.
- Re-run `bd_get_ps7_config` to confirm the writes landed. If a parameter is
  read-only or silently ignored, you will see it here — surface it, don't paper
  over it.
- **Remember:** this readback only confirms the write, not correctness. The real
  verdict for the DDR/FIXED_IO config is the **mandatory post-impl `report_drc`**
  gate in §13. Do not declare DDR "done" until that gate is clean.

### 4. Set the PL clock(s) — FCLK
The PS provides the PL clock; get this right before wiring anything.
- `bd_ps7_set_fclk(cell="ps7_0", fclk_id=0, freq_mhz=<target>, enable=True)` for
  the primary PL clock. Add more FCLKs only if the design needs multiple clock
  domains.
- `bd_get_ps7_config(cell="ps7_0")` — confirm the FCLK is enabled at the
  requested frequency. The requested vs. actually-realizable frequency can
  differ (PLL granularity); note the **actual** value — it is your real timing
  constraint later.
- **Multi-FCLK note:** if you enable more than one FCLK, you have created an
  intrinsic clock-domain boundary. Flag it now — it forces the CDC checks in §13
  and may require an `axi_clock_converter` (see step 7/8 and Safety rails).

### 5. Enable the PS-PL AXI port(s) you actually need
Only enable ports the design uses; spurious ports create unconnected-pin noise.
- PS as master to PL peripherals → enable a general-purpose master:
  `bd_ps7_enable_axi_port(cell="ps7_0", ...)` for `M_AXI_GP0`
  (or use the `minimal` preset which already exposes `M_AXI_GP0`).
- PL master needs high-bandwidth path to DDR → enable a high-perf slave
  `S_AXI_HP0` (or the `hp_slave` preset).
- `bd_get_ps7_config(cell="ps7_0")` — verify which PS-PL interfaces are now live.

### 6. Add PL-side peripherals (only what the user asked for)
Examples (use the exact tool; `bd_search_ip` / `ToolSearch` to confirm a specific
IP's tool name if unsure):
- AXI GPIO → `bd_create_axi_gpio` (then `bd_gpio_set_width` / `bd_gpio_set_direction`).
- AXI UARTlite → `bd_create_axi_uartlite` (then `bd_uartlite_set_baudrate`).
- AXI BRAM controller → `bd_create_axi_bram_ctrl`.
- A custom packaged AXI IP → `bd_add_ip`.
- `bd_list_ips` — confirm every block you expect is present, named as you expect.

### 7. Wire clocks and resets correctly (the #1 source of bring-up bugs)
The PS does NOT provide a synchronized PL reset by itself — you need a
Processor System Reset block driven by FCLK0 and the PS reset.
- `bd_create_proc_sys_reset(name="rst_ps7_0_<freq>")`.
- **Confirm reset polarity BEFORE wiring `aresetn`.** A polarity mismatch
  validates clean and passes DRC but breaks function on silicon (peripherals held
  in reset, or never reset). Call `bd_proc_sys_reset_get_config(...)` and confirm:
  - `peripheral_aresetn` is **active-low** — it is by design, and matches what every
    downstream AXI IP's `s_axi_aresetn` expects (AXI uses active-low reset). No action
    needed if you drive AXI resets from it.
  - `ext_reset_in` is fed by the PS `FCLK_RESET0_N` (active-low). Its polarity
    (`C_EXT_RESET_HIGH`) is **fixed at IP creation and read-only** — in the standard
    PS7/board-automation flow it is already correct. `bd_proc_sys_reset_set_polarity`
    does **not** change `ext_reset_in`; it only sets the **auxiliary** reset
    (`aux_reset_active_low`, used only if you wire `aux_reset_in`). If `ext_reset_in`
    polarity is genuinely wrong, **recreate the proc_sys_reset block** with the right
    setting — do not wire-and-hope.
- Connect:
  - PS `FCLK_CLK0` → proc_sys_reset `slowest_sync_clk` **and** every AXI IP's
    `s_axi_aclk` **and** the interconnect/smartconnect clocks
    (`bd_connect_pins` / `bd_connect_interfaces`).
  - PS `FCLK_RESET0_N` → proc_sys_reset `ext_reset_in`.
  - proc_sys_reset `peripheral_aresetn` → every AXI IP's `s_axi_aresetn` and
    interconnect reset.
- Every AXI clock pin in the design must come from the **same FCLK domain** as the
  master driving it (unless you deliberately insert an `axi_clock_converter` for a
  CDC — see Safety rails). Mixing FCLK0 and FCLK1 across a single AXI link without
  a converter is a silent functional bug.

### 8. Build the AXI fabric and connect master → slaves
- For one or a few AXI-Lite slaves: `bd_create_smartconnect`
  (auto width/clock conversion, preferred for new designs) or
  `bd_create_axi_interconnect`.
- Connect PS master to the interconnect slave port, and each interconnect master
  port to a peripheral's `S_AXI`:
  `bd_connect_interfaces(src="ps7_0/M_AXI_GP0", dst="<sc>/S00_AXI")`,
  then `<sc>/M0x_AXI` → `<periph>/S_AXI`.
- **Alternative (let Vivado wire it):** `bd_run_block_automation(cell="ps7_0")`
  for the PS itself, and/or `bd_run_automation` to auto-connect AXI/clk/reset for
  a peripheral. If you use automation, **still** run step 9 — automation can
  mis-guess clock domains.

### 9. Verify connectivity BEFORE address assignment
- `bd_get_unconnected_pins` — **must be empty** (or contain only pins you have a
  documented reason to leave open, e.g. an intentionally-external interrupt). If
  it lists clock/reset/AXI pins, go back to step 7/8. **Do not proceed with
  dangling AXI clocks/resets** — they produce a design that validates the graph
  but is functionally broken.
- `bd_list_nets` / `bd_get_info` if you need to see how something actually wired.

### 10. Assign and verify the address map
- `bd_assign_addresses` — auto-assign AXI addresses.
- `bd_get_address_map` — **inspect the result and confirm it is sane**:
  - Every AXI slave the PS master reaches has a non-zero-size, non-overlapping
    range inside the PS GP address window.
  - No peripheral landed at an unintended/overlapping address. Overlaps =
    silently broken software access later. If anything looks wrong, fix and
    re-assign; do not hand off a questionable map.

### 11. Validate the block design
- `bd_validate_design` — **must return clean** (errors include the offending
  pin/net path). Treat any ERROR as a hard stop; fix the specific net/pin it
  names, then re-validate. Warnings: read each one — distinguish benign
  (e.g. board-flow info) from real (unconnected interface, clock mismatch).
- **Validation is NOT sign-off.** It does not check DDR correctness, reset
  polarity correctness, PL-side IO constraints, CDC, or timing. Those are §13.
- `save_block_design`.

### 12. Generate output products + HDL wrapper, set top (long op — bounded poll)
- `bd_generate_output_and_wrapper(...)` to produce IP output products and the
  top-level HDL wrapper.
- **Long op — use a bounded poll, never an unbounded one.** For large designs
  this is multi-minute. Poll `bd_check_output_status` (and/or
  `bd_wait_on_output_generation`) **with an explicit ceiling**: pick a sane wall-
  clock budget (e.g. 15 min) and a max poll count; if generation has not
  completed by then, STOP and report it as a stalled long-op rather than looping
  forever. Do not assume success; confirm status is complete before proceeding.
- **Set and confirm the wrapper as top — do not assume it.**
  - `set_top_module(<wrapper>)`.
  - Then **confirm** it actually took, with `get_project_info` and/or
    `list_source_files`: the active top in the synthesis fileset must equal the
    generated wrapper module. If the fileset top is still an old/placeholder
    module, synthesis will build the wrong thing. Do not start synthesis until
    this is confirmed.
- `report_ip_status` — confirm no IP is locked/out-of-date. If locked, the design
  is not buildable as-is; surface it (an `upgrade_ip` may be needed) rather than
  proceeding.

### 13. Hardware sign-off (necessary — graph-clean is not enough)
A valid BD that won't implement is not a bring-up. Prove it with **fresh,
post-implementation** evidence. Synthesis success is **necessary, not
sufficient** — it proves neither timing, nor routability, nor pin legality.

**13a. Constrain PL-side IO before trusting timing.** Any PL-side top-level port
made external in the BD (e.g. a UART/GPIO pin, a PL clock/reset, an LED) is an
unconstrained endpoint until you constrain it. Unconstrained IO produces an
**optimistic / false WNS ≥ 0**. Where the design has PL-side IO:
  - set `set_input_delay` / `set_output_delay` on those ports against the
    relevant clock, and
  - add the pin-location/io-standard constraints (board XDC, or
    `create_io_constraint`).
The PS DDR/FIXED_IO pins are handled by the PS (do not constrain those by hand);
this step is about the **PL** ports.

**13b. Run the flow (bounded async poll).**
  - `run_synthesis_async`, then poll `get_run_status` **with an explicit max-poll
    / timeout ceiling** (same bounded-poll rule as §12 — a poll loop with no
    ceiling can hang). On completion: `check_synthesis_issues` +
    `get_synthesis_warnings`.
  - `run_implementation_async`, poll `get_run_status` the same bounded way until
    done.

**13c. Sign-off evidence — ALL must be fresh and post-implementation:**
  - **`check_timing`** — run this **first**, before trusting any WNS. It surfaces
    unconstrained endpoints / no-clock / missing input-output-delay problems. A
    clean `report_timing_summary` WNS is meaningless if `check_timing` shows
    unconstrained paths producing a false positive. There must be **no
    unconstrained-endpoint / no-clock issues** here.
  - **`report_timing_summary`** — assert BOTH:
    - **setup** WNS ≥ 0 **and** TNS ≥ 0 on all paths, **and**
    - **hold / min-delay** (WHS / THS) ≥ 0 on all paths.
    Reporting setup-only is not "timing met". A design can have setup slack and
    still fail hold. If either setup or hold is negative, hand off to the
    timing-closure skill; do not claim "works".
  - **`report_cdc`** — for any PS-PL crossing or **multi-FCLK** design, run
    `report_cdc` (and, pre-synth, `check_cdc_lint`). The PS-PL boundary is an
    intrinsic clock crossing; multiple FCLKs add more. There must be **no unsafe
    / missing-constraint CDC paths**. `report_methodology` alone does NOT catch
    every missing CDC constraint — `report_cdc` is the dedicated check and is
    required here.
  - **`report_drc`** — no critical DRC violations. **This is the mandatory gate
    for the bare-part DDR/FIXED_IO decision** (UCIO / FIXED_IO / DDR no-pin
    errors): if you configured DDR on a bare part, this gate is what proves the
    pinout is real. It is non-optional.
  - **`report_methodology`** — no critical methodology violations (catches
    additional clock/CDC/structural issues; complements, does not replace,
    `report_cdc`).
  - **`report_utilization`** → fits the device.
- Only after **check_timing (clean), setup AND hold WNS/TNS ≥ 0, report_cdc
  (clean), report_drc (clean), report_methodology (clean)** all pass on fresh
  post-impl runs may you say the SoC is brought up.

### 14. (Optional) Bitstream + hardware export
- `generate_bitstream` (or `run_full_flow` end-to-end if the user wants one shot —
  but still verify §13 reports afterward; `run_full_flow` does not exempt you from
  evidence).
- `export_hardware` to produce the XSA for the downstream software/BSP flow.

---

## Connectivity decision table (symptom → cause → safe fix)

| Symptom (from a tool) | Likely cause | Smallest safe fix |
|---|---|---|
| `bd_validate_design` ERROR naming an AXI `s_axi_aclk` pin | AXI clock unconnected or wrong FCLK domain | Connect that pin to the correct FCLK in step 7; re-validate. |
| `bd_get_unconnected_pins` lists `*aresetn` | Missing proc_sys_reset wiring | Add/connect `bd_create_proc_sys_reset` outputs (step 7). |
| Peripheral held in reset / never resets, but graph validates clean | proc_sys_reset wiring/polarity | `bd_proc_sys_reset_get_config`: confirm `ext_reset_in` is fed by active-low `FCLK_RESET0_N` (its polarity is fixed at creation — **recreate** the block if wrong) and `peripheral_aresetn` (active-low by design) drives the AXI resets. `set_polarity` only changes the aux reset (step 7). |
| `bd_get_address_map` shows a slave with no range | Slave not reachable from the PS master / not assigned | Confirm master→slave interface path (step 8), re-run `bd_assign_addresses`. |
| Address ranges overlap | Manual/partial assignment | Re-run `bd_assign_addresses`; if still overlapping, inspect and set non-overlapping ranges; never ship an overlap. |
| `check_timing` shows unconstrained endpoints / no-clock | PL-side IO has no input/output delay or no clock | Add `set_input_delay`/`set_output_delay` + IO constraints (§13a); re-run. A WNS taken before this is false. |
| FCLK realized freq ≠ requested | PLL granularity | Accept the realized value and **use it** as the timing constraint; note it to the user. Do not over-constrain a clock the PS cannot produce. |
| `report_timing_summary` setup WNS ≥ 0 but hold (WHS) < 0 | Hold violation (short paths / clock skew) | This is a real failure, not "timing met" — hand off to timing-closure; do not report success. |
| `report_timing_summary` WNS < 0 on a PS-PL AXI path | PL too slow for FCLK, or a true CDC across FCLK domains | First confirm it's a real same-domain path (run `report_clock_interaction` / `report_cdc`). If real same-domain → timing-closure skill. If genuinely async across two FCLKs (proven by `report_clock_interaction` / `report_cdc`) → insert `bd_create_axi_clock_converter` (a real CDC fix), not a blanket `set_false_path`. |
| `report_cdc` flags an unsafe/unconstrained crossing | PS-PL or multi-FCLK crossing without synchronizer/constraint | Add the correct CDC structure (`axi_clock_converter` for AXI, proper synchronizer for single bits) — never paper over with `set_false_path` unprovenly. |
| `report_ip_status` shows a locked IP | Version mismatch | `upgrade_ip` / regenerate output products; re-validate. Surface to user if it changes behavior. |
| `report_drc` UCIO/no-pin errors on FIXED_IO/DDR | DDR/FIXED_IO not exported (bare-part path) or board automation skipped | Run PS `bd_run_block_automation` / configure DDR+FIXED_IO (steps 2–3); these are hard-pinned by the PS and must be present. This DRC IS the bare-part DDR gate. |
| Synthesis built the wrong/old top | Wrapper not actually set as top in fileset | `set_top_module(<wrapper>)`, then confirm via `get_project_info`/`list_source_files` (§12) before re-synth. |

---

## Build → verify → re-measure loop (with STOP conditions)

Each step's `bd_get_*` / `report_*` is the "measure". Iterate **only** the failing
sub-step, change **one class of thing**, then re-measure. STOP and act when:

- **STOP-DONE:** `bd_validate_design` clean **and**, on **fresh** post-impl runs:
  `check_timing` clean (no unconstrained endpoints), `report_timing_summary`
  setup WNS/TNS ≥ 0 **and** hold/min-delay ≥ 0, `report_cdc` clean, `report_drc`
  clean, and `report_methodology` clean → declare bring-up complete with the
  metrics shown.
- **STOP-ASK (config unknown):** DDR part / board / target FCLK unknown on a bare
  part → stop and ask the user. Do not guess hardware-critical config.
- **STOP-ASK (could-be-real violation):** a timing/DRC/CDC/methodology violation
  that might be a genuine bug (real same-domain path failing, real CDC) → present
  it and ask before waiving. Never `set_false_path` / `set_multicycle_path` /
  `waive_lint_violation` a path that could be real just to turn a number green.
- **STOP-HANDOFF:** timing fails after correct constraints (PL-side IO delays set,
  clocks defined, `check_timing` clean) → this is the timing-closure skill's job;
  hand off with the report, don't thrash on RTL here.
- **STOP-TRADEOFF:** safe options exhausted (e.g. utilization over-budget, or a
  PS-PL bandwidth shortfall needing HP-port/architecture change) → present
  options + costs (e.g. "add S_AXI_HP for DMA bandwidth vs. lower FCLK vs. smaller
  part") and hand back to the human. Do not loop.
- **STOP-STALLED-LONGOP:** a long op (output generation, synthesis, or
  implementation) exceeds its poll ceiling / wall-clock budget → stop the poll
  loop and report it as stalled, rather than polling forever.
- **Anti-thrash:** if the same validation/timing/CDC/DRC error persists after 2
  distinct fix attempts, STOP and present what you tried + what's left. Don't keep
  poking.

---

## Safety rails (do not violate)

- **Evidence before claims.** "BD valid", "addresses assigned", "timing met",
  "no CDC issues", "bitstream generated" each require **fresh** output from the
  corresponding tool (`bd_validate_design`, `bd_get_address_map`, post-impl
  `check_timing` + `report_timing_summary`, `report_cdc`, `generate_bitstream`).
  Never infer success from a prior step or from a tool *running without error*.
  Synthesis numbers never substitute for post-implementation sign-off.
- **"Timing met" means setup AND hold.** Always assert both setup (WNS/TNS) and
  hold (WHS/THS) ≥ 0, and only after `check_timing` shows no unconstrained
  endpoints. Setup-only is not sign-off.
- **CDC is its own gate.** For any PS-PL or multi-FCLK design, `report_cdc`
  (and pre-synth `check_cdc_lint`) is required; `report_methodology` does not
  replace it.
- **No fake-pass — and async exceptions need PROOF, not a verbal assumption.**
  Do not apply `set_false_path` / `set_multicycle_path` / `set_clock_groups` /
  `waive_lint_violation` to silence a violation that could be real. A true
  asynchronous PS-PL crossing (different FCLKs, or PS clock vs. a separately-
  generated PL clock) is the *only* place an exception is legitimate — and you
  must **prove** it is genuinely asynchronous with **fresh** `report_clock_interaction`
  and/or `report_cdc` evidence showing the two clocks have no timed relationship,
  **before** applying `set_clock_groups -asynchronous` or inserting
  `bd_create_axi_clock_converter`. A self-declared "assume it's async" is not
  acceptable. If the evidence is unclear, **ask first.**
- **Don't brick the board.** Never invent DDR part/timing or MIO pinout to make
  validation pass on a bare part. Wrong DDR/MIO passes `bd_validate_design`,
  `bd_get_ps7_config` readback, AND synthesis — it is caught only by
  post-impl `report_drc` (UCIO/FIXED_IO/DDR no-pin). State the assumption and ask
  the user for the board/DDR if unknown; treat the §13 `report_drc` gate as the
  decision's verification.
- **Confirm reset polarity before wiring.** Polarity mismatch validates clean and
  passes DRC but breaks silicon. Use `bd_proc_sys_reset_get_config` before connecting
  `aresetn`: `peripheral_aresetn` is active-low by design; `ext_reset_in` polarity is
  fixed at creation (recreate the block if wrong — `set_polarity` only affects the aux
  reset). See step 7.
- **Confirm the wrapper is actually top.** After `set_top_module`, verify via
  `get_project_info` / `list_source_files` before synthesis (step 12).
- **Smallest safe change first.** Prefer configuration and wiring fixes
  (FCLK, reset, interconnect, address) over editing or generating RTL. The PS7 is
  hard IP — you configure it, you do not rewrite it. For PL-side RTL issues,
  **recommend** the edit; do not silently rewrite user RTL.
- **One change-class per iteration** so cause→effect is attributable (clocks, then
  resets, then fabric, then addresses — not all at once).
- **Verify connectivity before address/validate, validate before generate,
  generate before build.** Skipping the `bd_get_unconnected_pins` check produces
  designs that validate but are functionally dead.
- **Right device family.** PS7 tools are Zynq-7000 only. If the part is MPSoC or
  non-Zynq, stop — do not force it.
- **Long ops use bounded async + poll.** Output-product generation, synthesis, and
  implementation are multi-minute: use `bd_wait_on_output_generation` /
  `bd_check_output_status` / `*_async` + `get_run_status`, **each with an explicit
  poll-count / wall-clock ceiling** so the poll loop cannot hang indefinitely.
  Confirm completion before the next stage.

---

## Output (report back to the user)

Report, with the tool output backing each line:

1. **Configuration realized** — part/board, BD name, PS7 instance, FCLK(s) at
   their **actual realized** frequency (from `bd_get_ps7_config`), DDR status,
   reset polarity confirmed (`bd_proc_sys_reset_get_config`), enabled PS-PL ports,
   PL peripherals added.
2. **Connectivity** — `bd_get_unconnected_pins` result (empty, or the documented
   exceptions).
3. **Address map** — the `bd_get_address_map` table (slave → base/range), noted as
   non-overlapping.
4. **Validation** — `bd_validate_design` result verbatim (clean / the errors).
5. **Top confirmed** — wrapper module set as top and verified in the fileset
   (`get_project_info` / `list_source_files`).
6. **Sign-off evidence (fresh, post-implementation)** — `check_timing` (no
   unconstrained endpoints), `report_timing_summary` **setup WNS/TNS AND hold
   (WHS/THS) ≥ 0**, `report_cdc` (clean / flagged crossings), `report_drc`
   (clean — explicitly note this is the DDR/FIXED_IO gate on a bare part),
   `report_methodology`, `report_utilization`. If any failed, say so plainly and
   route to the right next step (timing-closure / user decision) — **do not**
   report a partial build as a success. Never report setup-only timing as "met".
7. **Artifacts** — wrapper module set as top, bitstream (if generated), XSA path
   (if `export_hardware` was run).
8. **Open items / trade-offs** — anything that needs a human decision (DDR config
   to confirm, timing shortfall, bandwidth trade-off), stated explicitly.

If a STOP-ASK or STOP-TRADEOFF condition was hit, the output is the question or
the options table — not a claim of completion.
