---
name: utilization-reduction
description: >
  Diagnose and reduce FPGA resource/area pressure when a design is too big for
  the part. Use when the user says the design is "running out of LUTs", "too big
  for the part", "over 100% utilization", "won't fit", "out of BRAM/DSP/FF",
  "reduce utilization", "shrink area", "implementation failed: placement
  infeasible / overutilized", or asks to fit a design into a smaller/cheaper
  device. Requires the SynthPilot MCP server (AI-controlled Xilinx Vivado) with
  the Tcl server running inside an open Vivado session and a project loaded.
---

# Utilization Reduction

Reduce resource/area pressure so a design fits the target part. Area work is
**resource-typed**: LUTs, FFs, BRAM/RAMB, DSP, URAM, carry chains, and control
sets each have different root causes and different safe fixes. You must measure
*which* resource is the bottleneck before touching anything, fix the dominant
resource first, and re-measure after every single change so cause and effect
stay attributable.

The cheapest, safest levers are settings (synthesis area strategy, IP
right-sizing, RAM/DSP inference thresholds, BRAM ECC/output regs). The
expensive, design-altering levers are RTL/architecture (resource sharing, time
multiplexing, narrower datapaths, dropping features). Always exhaust the cheap
levers first, recommend the expensive ones rather than silently rewriting RTL,
and surface the trade-off (area vs. Fmax vs. functionality) before handing back.

---

## When to use

- Synthesis or implementation reports a resource over (or near) 100%:
  "over-utilized", "placement infeasible", "insufficient sites".
- `report_utilization` shows any resource column at high % (LUT, FF, BRAM,
  DSP, URAM, carry, control sets) and the user wants headroom.
- The user wants to fit the design into a smaller / cheaper device or free up
  room for a debug core (ILA/VIO) or a future feature.
- A single resource type is the gate (e.g. design fits except BRAM at 140%).
- Implementation aborts at placement with overutilization errors.

## When NOT to use

- **Timing is the problem, not area** (WNS negative but utilization < ~80%).
  That is timing-closure work, not this skill.
- **Routing congestion with comfortable utilization.** Congestion at moderate
  utilization is a placement/floorplan problem; use `report_congestion` /
  `report_design_analysis` under a congestion playbook, not area reduction.
- **The design simply does not fit any available part.** If the smallest
  necessary resource already exceeds 100% after all safe levers, that is an
  architecture decision (bigger part / drop features) — surface it and stop.
- **Power, DRC, lint, or CDC** are the actual complaint. Different skills.
- You have no fresh utilization numbers and cannot run synthesis. Get numbers
  first; never guess at area.

---

## Prerequisites (verify first)

Run these and confirm before any analysis. Do not proceed on assumption.

1. `test_connection` — Tcl server inside Vivado is reachable. If it fails,
   stop: nothing below works without the bridge.
2. `get_project_info` — a project is open; note the **target part** and its
   resource ceilings. "Too big" is always relative to a specific part.
3. `get_license_status` — confirm the report/strategy tools you intend to call
   are available in the current tier (hierarchical utilization, design
   analysis, QoR suggestions may be PRO).
4. Establish you have **real numbers**, not estimates:
   - If an implemented or synthesized design is already open, you can read
     utilization directly.
   - Otherwise run synthesis (step 1 of the methodology) to get a post-synth
     baseline. Post-synth is enough to *find* the dominant resource; **only
     post-implementation numbers are signoff-grade for "it fits"** (synthesis
     under-counts after place opt, and over-counts LUTs that later merge).

State the target part and the resource ceilings before you start fixing.

---

## Methodology (measure -> classify -> smallest safe fix -> re-measure)

### Step 1 — Establish a fresh utilization baseline

- If no design is open, run synthesis to get post-synth numbers. For a
  multi-minute run prefer the async pattern:
  `run_synthesis_async`, then poll `get_run_status` until complete, then
  `get_synthesis_report` and `check_synthesis_issues`. (`run_synthesis`
  synchronously is fine for small designs.)
- Open the design so the report tools have a netlist:
  `open_synthesized_design` (post-synth) — or, for signoff numbers,
  `open_implemented_design` after implementation.
- `report_utilization` — capture the **flat** numbers: used / available / % for
  LUT (logic vs. memory/LUTRAM split), FF, BRAM (RAMB36/RAMB18), URAM, DSP,
  carry/CARRY chains, and **control sets**. Record this as the baseline.

Do not act yet. Numbers first.

### Step 2 — Identify the dominant resource and where it lives

- From the baseline, pick the **single highest-% resource** that exceeds (or
  threatens) 100%. That is your target. Fixing a resource at 40% buys nothing.
- `report_utilization_hierarchical` (start `depth=2`, drill deeper as needed) —
  find *which module/instance* dominates that resource. Area reduction is
  almost always concentrated; attack the top contributors, not the whole tree.
- `report_ip_status` and `list_project_ips` — IP cores (FIFOs, memories,
  clocking, AXI infra, DSP-heavy IP) are common silent hogs and are often the
  **cheapest** thing to right-size (see classification table).
- Optional context: `report_design_analysis` (logic-level / complexity) and
  `report_qor_suggestions` (Vivado's own area/strategy hints — may be empty).

Now you can classify.

### Step 3 — Classify the bottleneck (see table) and pick the SMALLEST safe fix

Map dominant resource + where-it-lives to a cause, then to the cheapest fix
class that addresses it. **Order of preference, always:**

1. **Settings / IP right-sizing** — synthesis area strategy, IP depth/width,
   BRAM output-register / ECC, RAM/DSP inference thresholds. No RTL change.
2. **Inference-directing constraints / attributes** — recommend
   `ram_style` / `rom_style` / `use_dsp` / `max_fanout` style attributes in
   RTL. These are RTL edits — *recommend*, do not silently apply.
3. **RTL / architectural change** — resource sharing, time-multiplexing,
   narrower datapaths, feature removal. Highest cost, highest risk —
   **recommend and explain; never silently rewrite.**

Apply exactly **one change-class per iteration** so the re-measured delta is
attributable. Use `set_synthesis_strategy` (e.g. `Flow_AreaOptimized_high`,
or `Flow_AreaMultThresholdDSP` for DSP pressure) and
`set_implementation_strategy` (`Area_Explore`) for the settings lever.

### Step 4 — Re-measure (mandatory)

- Re-run synthesis (async pattern) → re-open design → `report_utilization` and
  `report_utilization_hierarchical`. Compare against the previous baseline,
  resource by resource. **Show the before/after delta.**
- A settings/strategy or inference change can move *other* resources (e.g.
  forcing BRAM→distributed trades BRAM for LUTRAM/LUTs; lowering `use_dsp`
  moves multiplies into LUTs). Re-read *all* resources, not just the one you
  targeted, to catch a regression where you robbed Peter to pay Paul.
- **Timing guard:** area strategies and resource sharing usually *cost* Fmax.
  If the design had a timing target, after the area change re-check timing
  (`report_timing_summary` / `extract_timing_metrics`) so you don't trade an
  area failure for a timing failure. Report both numbers.

### Step 5 — Signoff (only when claiming "it fits")

A "fits the part" claim requires **fresh post-implementation evidence**, never
post-synth inference:

- Run implementation (`run_implementation_async` → poll `get_run_status` →
  `get_implementation_warnings`), then `open_implemented_design`.
- `report_utilization` on the **implemented** design — every gating resource
  must be < 100% with real headroom.
- `report_drc` — confirm no overutilization / placement DRC violations remain.
- If a timing target exists, `report_timing_summary` must still pass.

If implementation still over-utilizes, you are not done — loop back to Step 2
with the new dominant resource, or escalate per the STOP conditions.

---

## Classification: dominant resource -> likely cause -> smallest safe fix

| Dominant resource (from `report_utilization` / hierarchical) | Likely cause | Smallest safe fix first | Escalation (recommend, do not auto-apply) |
|---|---|---|---|
| **LUT (logic)** high, FF moderate | Combinational logic bloat; replicated logic; wide muxes/comparators; unshared arithmetic | `set_synthesis_strategy Flow_AreaOptimized_high`; right-size oversized IP | Recommend resource sharing / time-multiplexing of duplicated datapaths; narrow over-wide buses; fold parallel units |
| **LUTRAM / memory-LUT** high | Small/shallow RAMs/ROMs inferred into distributed RAM instead of BRAM | Recommend `(* ram_style = "block" *)` / `rom_style = "block"` on the offending arrays (found via hierarchical) to push them to BRAM | If BRAM is also tight, this is a true capacity wall → present part/architecture trade-off |
| **BRAM (RAMB36/18)** high | Over-deep/over-wide memories; FIFOs/IP sized larger than needed; ECC or output regs adding banks; many small RAMs not packed | `report_ip_status` then right-size FIFO/Block-Memory IP depth/width; disable BRAM ECC if not required; cut over-provisioned FIFO depth | Recommend merging small RAMs, moving rarely-touched tables to distributed (LUTRAM) or off-chip; consider URAM if part has it |
| **DSP** high | Multipliers/MACs each mapped to DSP48; large multiplies split across multiple DSPs | `set_synthesis_strategy Flow_AreaMultThresholdDSP` to push small mults to fabric; right-size DSP-heavy IP | Recommend `(* use_dsp = "no" *)` on small/low-rate multiplies, time-shared MAC, or reduced precision — note this *adds LUTs*, re-measure |
| **FF (registers)** high | Deep pipelining; wide registered datapaths; auto-replication; SRL-able shift regs as FFs | Allow tool to infer SRLs (`srl_style`); reduce unnecessary pipeline depth via settings where possible | Recommend trimming pipeline stages (costs Fmax) or narrowing registered width; confirm with user — this is functional/timing-affecting |
| **Control sets** high (drives LUT/placement pressure even at moderate FF%) | Too many distinct (clock, enable, reset) groups → poor slice packing | Reduce gated/async resets and per-bit enables via settings/attributes where safe | Recommend uniform synchronous reset / fewer enable domains in RTL — surface as design guidance |
| **CARRY chains** high | Many wide adders/counters/comparators | `Flow_AreaOptimized_high` lets tool restructure | Recommend sharing adders or restructuring wide arithmetic |
| **IO** over | Pin count exceeds package | (Not fabric area) — `report_io`; this is a packaging/part problem | Recommend bus muxing, serialization, or a larger package — present, do not auto-change pinout |

If the dominant resource is an **IP core**, prefer right-sizing the IP
(`get_fifo_config` / `get_memory_config` / `get_ip_config` to read it, then the
matching `configure_*` / `set_ip_property`) **before** any RTL change — it is
usually the single biggest, lowest-risk win.

---

## Reduction loop and STOP conditions

```
baseline = report_utilization (+ hierarchical)        # Step 1-2
while (gating resource >= 100% OR user wants more headroom):
    classify dominant resource (table)                # Step 3
    apply ONE smallest-safe change-class
    re-synth -> report_utilization (+ hierarchical)    # Step 4
    re-check OTHER resources + timing for regressions
    show before/after delta
    -- STOP if any condition below --
sign off with implementation evidence                  # Step 5
```

**STOP (and report) immediately when any of these hold:**

- **It fits with headroom** — every gating resource < 100% on a **fresh
  implemented** design, DRC clean, timing still met. → Sign off (Step 5).
- **No progress** — a change moved the gating resource < ~1–2% (or moved it
  the wrong way). Do not pile on more of the same lever; reclassify or escalate.
- **Whack-a-mole** — fixing resource A pushed resource B over 100%. Stop tuning;
  present the genuine trade-off (the design's resource *balance* is the issue).
- **Safe levers exhausted** — area strategies + IP right-sizing applied, and the
  only remaining moves are RTL/architecture rewrites or a bigger part. **Hand
  back to the human** with concrete options + costs (below). Do not thrash, and
  do not start rewriting RTL on your own.
- **Area vs. timing collision** — the area fix that makes it fit breaks the
  timing target (or vice versa). Present both numbers and let the human pick the
  operating point.

When you stop at "levers exhausted", give the user a ranked options list, e.g.:
*(a)* right-size IP X (frees ~N BRAM, no Fmax cost) — recommended;
*(b)* push array Y to BRAM via `ram_style` (RTL edit, frees ~M LUTRAM);
*(c)* time-multiplex the K parallel MAC units (frees ~P DSP, costs throughput
+RTL work); *(d)* move to part Z (bigger, +cost). Then stop.

---

## Safety rails (do not violate)

- **Evidence before claims.** "It fits" / "we have headroom" REQUIRES fresh
  **post-implementation** `report_utilization` + clean `report_drc`. Never claim
  fit from post-synth numbers or from inference — synthesis utilization is
  *necessary but not sufficient*. No tool output, no claim.
- **No fake-pass.** Do not make a resource go green by removing real
  functionality, disabling a needed feature (e.g. turning off BRAM ECC the
  design actually needs), waiving a real overutilization DRC, or shrinking an IP
  below its required depth/width. If a reduction could break function, **ask the
  user first** and state the assumption.
- **Smallest safe change first.** Settings/strategy and IP right-sizing before
  any RTL. Always.
- **Recommend RTL, never silently rewrite.** Resource sharing, time-muxing,
  precision/width reduction, dropping pipeline stages, and `ram_style`/`use_dsp`
  attributes are *recommendations*. Read with `read_file` / `read_file_lines`,
  explain the change and its cost, and apply edits (`update_file` /
  `replace_in_file`) **only after the user agrees**. Functional or
  throughput-changing edits ALWAYS need explicit user sign-off.
- **One change-class per iteration.** So every before/after delta is
  attributable. No batching multiple levers in one pass.
- **Watch for displaced resources.** Many area fixes *move* area (BRAM→LUTRAM,
  DSP→LUT, FF→SRL). Re-read **all** resources after each change; a "win" that
  overflows another resource is not a win.
- **Guard timing.** Area strategies (`Flow_AreaOptimized_high`, `Area_Explore`)
  and resource sharing typically cost Fmax. If a timing target exists, re-check
  `report_timing_summary` after the area change and report both.
- **Real tools only.** Use only the SynthPilot tool names. If a needed lever
  isn't exposed as a tool (e.g. a specific synth directive), say so and give the
  user the manual step rather than inventing a tool.

---

## Output

Report back in this shape:

1. **Target part & ceilings** — device, and the available count for each
   resource (so % means something).
2. **Baseline utilization** — table of used / available / % for LUT(logic),
   LUT(mem), FF, BRAM, URAM, DSP, carry, control sets. Mark the **gating**
   resource.
3. **Diagnosis** — dominant resource, where it lives
   (`report_utilization_hierarchical` top contributors), and the classification
   (cause) from the table.
4. **Change applied** — exactly one change-class, what it was, and *why it's the
   smallest safe fix*.
5. **Before → After** — per-resource delta table, including resources you did
   *not* target (to prove no regression) and timing if a target exists.
6. **Status** — one of: `FITS (signed off, impl evidence)` /
   `IMPROVED, still over` / `LEVERS EXHAUSTED — decision needed`. Cite the
   exact tool output backing the status.
7. **If stopped:** the ranked options + costs list, then hand back to the human.
   No further autonomous RTL changes.

Never assert that the design fits without quoting fresh post-implementation
`report_utilization` and a clean `report_drc`.
