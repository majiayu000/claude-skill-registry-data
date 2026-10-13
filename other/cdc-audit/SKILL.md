---
name: cdc-audit
description: >-
  Audit and resolve clock-domain-crossing (CDC) risks on a design: enumerate every
  clock crossing, classify each by structure (synchronizer present/absent, single-bit
  vs bus, async reset, reconvergence), and apply the smallest safe fix (synchronizer
  RTL, set_clock_groups / set_max_delay -datapath_only / set_bus_skew constraints)
  without ever waiving a real crossing.
  Invoke when the user says "cdc analysis", "check clock domain crossings",
  "metastability review", "are my async crossings safe", "audit clock crossings",
  "fix CDC violations", "report_cdc is showing critical", "do I need a synchronizer
  here", or asks about gray-code, handshake, async FIFO, or reset-domain-crossing
  (RDC) safety.
  Requires the SynthPilot MCP server with Vivado open and the Tcl server running
  (TCP:9999); CDC reporting needs an elaborated or synthesized design.
---

# CDC Audit (Clock-Domain-Crossing Risk Review & Resolution)

A methodology playbook for finding, classifying, and safely resolving clock-domain
crossings using the SynthPilot MCP tools that drive Vivado. CDC bugs do not show up
as timing failures — a metastable crossing can pass STA and still fail silently in
silicon. This skill treats CDC as a **structural correctness** problem first and a
**constraint** problem second.

The governing rule for this entire skill: **a CDC constraint does not fix a CDC bug.**
`set_clock_groups`, `set_false_path`, and `set_max_delay -datapath_only` only tell
the timing engine to stop reporting a crossing — they do nothing to add the
synchronizer hardware that actually prevents metastability propagation. Constraints
are applied **only after** the crossing is confirmed to be structurally safe, or
explicitly waived with a stated assumption.

---

## When to use

- User asks for a "CDC analysis", "check clock domain crossings", "metastability
  review", or "reset domain crossing (RDC) check".
- A design has **two or more asynchronous (unrelated) clocks** and you need to prove
  every crossing is either synchronized or safely a quasi-static/false path.
- `report_cdc` / `check_cdc_lint` is reporting **Critical** or **Warning** severity
  items and the user wants them triaged and resolved.
- Pre-tapeout / pre-release signoff that must include a clean CDC report.
- A clock-crossing FIFO, handshake, or gray-code counter was just added and the user
  wants it verified.
- Intermittent / "works on the bench sometimes" hardware bugs where metastability is
  a suspect.

## When NOT to use

- **Single-clock design** (or all clocks synchronous/derived from one source with a
  known phase relationship). There are no async crossings to audit — confirm this
  with `get_all_clocks` / `report_clock_interaction` and stop.
- **Setup/hold timing failures within a single domain** → use the `timing-closure`
  skill. CDC is about *unrelated* clocks; intra-domain WNS violations are a different
  problem.
- **Functional logic bugs** that happen to be near a crossing → simulate first
  (`sim_run`); do not blame CDC without evidence of a real domain crossing.
- **Pure lint/style cleanup** with no async clocks → use the `lint` skill.
- You only have an RTL file and no project / no Vivado connection — CDC structural
  analysis needs an elaborated or synthesized netlist. Set the project up first.

---

## Prerequisites (verify first)

Run these before any analysis. Do not proceed on assumption.

1. **MCP/Vivado link is live** — `test_connection`. If it fails, the Tcl server
   inside Vivado is not running; stop and tell the user to start it. Optionally
   `vivado_version` to record the tool version in the report.
2. **A project is open with the design loaded** — `get_project_info` and
   `list_source_files`. If nothing is open, `open_project` (or `create_project` +
   `add_source_file` + `set_top_module`).
3. **Clocks are actually defined** — `get_all_clocks`. CDC analysis is meaningless
   without clock constraints; if clocks are missing (everything shows as one
   inferred clock, or `report_cdc` later says "no inter-clock paths"), the timing
   environment is incomplete. Note this and, before drawing conclusions, ensure
   primary clocks are constrained via `create_clock_constraint` /
   `create_generated_clock`. **A missing clock definition silently hides real
   crossings — treat an incomplete clock set as a blocker, not a pass.**
4. **A design exists to report on.** `report_cdc` needs an elaborated or synthesized
   design open. The cheapest entry point is structural lint (`check_cdc_lint`), which
   works on RTL. For the authoritative crossing-by-crossing report you need a
   synthesized design — if none exists, run `run_synthesis_async` and poll
   `get_run_status` (see Methodology step 2). Then `open_synthesized_design`.

State explicitly which of these are satisfied before continuing.

---

## Methodology (measure → classify → smallest-safe-fix → re-measure)

Work the crossings in **severity order (Critical → Warning)**. Change **one
crossing-class per iteration** so cause and effect stay attributable.

### 1. Inventory the clock topology (understand the battlefield)

- `get_all_clocks` — list every clock, its period, and source.
- `get_clock_info` — per-clock detail (waveform, generated-vs-primary) where needed.
- `report_clock_networks` — physical clock network / buffering view.
- `report_clock_interaction` — **the key map**: which clock pairs have paths between
  them and whether each pair is timed, partial-false-path, or asynchronous. This is
  your ground truth for "which crossings exist." Note every pair flagged
  asynchronous or with inter-clock paths.

From this, build the set of **clock-pair crossings** you must account for. A crossing
not on this list does not exist; a crossing on this list must be classified before
you may close the audit.

### 2. Get an authoritative CDC report

- **RTL-level first pass (fast, no synth):** `check_cdc_lint` and/or
  `run_full_lint_check` → `get_lint_violations`. This catches missing synchronizers
  and obvious structural issues early and cheaply.
- **Netlist-level authoritative pass:** ensure a synthesized design is open. If not:
  - `run_synthesis_async`, then poll `get_run_status` until complete (multi-minute —
    do not block; use the async + poll pattern). On completion check
    `check_synthesis_issues` / `get_synthesis_warnings`.
  - `open_synthesized_design`.
  - `report_cdc` — the full crossing-by-crossing CDC report with severity
    (Critical / Warning / Info) and endpoint detail.
- For large reports, narrow with `report_cdc_filtered` (e.g., by clock pair or
  severity) and drill into specific endpoints with `report_cdc_details`.

Record the **raw counts** (Critical / Warning / Info) as the audit baseline. Do not
editorialize them yet.

### 3. Classify every Critical/Warning crossing (classification table below)

For each flagged crossing, identify: source clock, destination clock, signal
**width** (single-bit vs bus), whether a **synchronizer is present**, whether it is a
**control vs data** path, and whether **reconvergence** or **reset-domain-crossing**
is involved. Use `report_cdc_details` and, where you need to see the RTL,
`read_file` / `read_file_lines` on the relevant source. Map each to a structure type
using the table below.

### 4. Apply the smallest safe fix for that crossing class

Follow the **fix-precedence ladder** strictly:

1. **Already-safe → constrain only.** If a correct synchronizer already exists, the
   crossing is structurally fine; the only action is to make the timing tool treat it
   correctly (`set_clock_groups -asynchronous`, or `set_max_delay -datapath_only` /
   `set_bus_skew` for buses — see table). This is a constraint, not a design change.
2. **Missing/incorrect synchronizer → recommend RTL.** Do **not** silence it. Propose
   the specific RTL fix (2-FF synchronizer for single-bit control; async FIFO or
   gray-code + handshake for buses; reset synchronizer for RDC) and present it to the
   user. **Recommend the edit; do not silently apply RTL.** If the user approves, use
   `read_file` → `replace_in_file` / `update_file` (or `create_source_file` for a new
   synchronizer module), then add it to the project and re-elaborate.
3. **Genuinely a non-crossing (quasi-static, same effective domain, tied constant) →
   waive with a stated assumption.** Only here may you use `set_false_path` /
   `set_clock_groups` / `waive_lint_violation`, and only after explicitly stating the
   assumption (e.g., "config register is written once at reset, never while the
   destination clock is active"). **If the path could be real and you are unsure, ask
   the user before waiving.**

Apply exactly one crossing-class of change, then `save_constraints` (for constraint
changes).

### 5. Re-measure on the same evidence source

Re-run the **same** tool you measured with: `report_cdc` (and `report_clock_interaction`
to confirm the pair is now correctly treated) for netlist changes;
`check_cdc_lint` / `get_lint_violations` for RTL changes. Confirm the targeted
crossing's severity dropped **and that no new Critical/Warning appeared elsewhere**.
RTL changes require re-synthesis (step 2) before the netlist CDC report is valid
again — synthesis warnings alone are necessary-not-sufficient.

### 6. (Signoff) Prove it on the implemented design

For a **signoff claim** that "CDC is clean," constraints must hold through place &
route. Run `run_implementation_async`, poll `get_run_status`, then
`open_implemented_design` and:
- `report_cdc` (final, post-implementation) — the authoritative clean/not-clean
  verdict.
- `report_clock_interaction` — confirm every async pair is correctly grouped.
- `report_drc` and `report_methodology` — catch CDC-adjacent methodology violations
  (e.g., `CDC-*`, `TIMING-*` rule hits) that the CDC report alone may not surface.
- For bus crossings constrained with `set_bus_skew`, confirm the skew constraint
  **passed** in `report_timing_summary` (a skew constraint that fails routing is not
  a fix).

A success claim **requires fresh post-implementation tool output**, never inference
from RTL or synthesis.

---

## Classification table (symptom → structure → safe fix)

| # | Symptom from report_cdc / report_cdc_details | Structural cause | Smallest safe fix (in precedence order) |
|---|---|---|---|
| C1 | **1-bit control crossing, no synchronizer** (direct reg→reg between async clocks) | Missing 2-FF synchronizer — true metastability risk | **RTL:** recommend a 2-flop synchronizer on the destination clock. Do NOT false-path. After fix + re-synth, optionally `set_max_delay -datapath_only` src→sync-FF1. |
| C2 | **1-bit crossing WITH a recognized 2-FF synchronizer** | Already safe; tool just needs to be told it's async | **Constraint only:** `set_clock_groups -asynchronous` between the two clocks (or `set_max_delay -datapath_only` on the input to FF1). No RTL change. |
| C3 | **Multi-bit bus crossing, all bits sampled by a synchronizer** | Bus bits can skew → recombine to a wrong value (data coherency hazard) | **RTL:** recommend gray-code (counters), or async FIFO, or a handshake-gated MUX-capture (req/ack). A per-bit 2-FF synchronizer on a bus is a BUG, not a fix — call it out. |
| C4 | **Bus crossing via async FIFO / handshake-qualified capture** | Already coherent by construction | **Constraint:** `set_bus_skew` on the bus (bound inter-bit skew) and/or `set_max_delay -datapath_only`; `set_clock_groups -asynchronous` for the clock pair. No RTL change. |
| C5 | **Reset asserted in one domain, deasserted into another (RDC)** | Reset deassertion not synchronized → metastable release, partial reset | **RTL:** recommend an async-assert / sync-deassert reset synchronizer per destination domain. Verify with `check_async_reset`. |
| C6 | **Reconvergence:** two synchronized signals from the same source recombine downstream | Independent 2-FF synchronizers resolve on different cycles → glitch/illegal combo | **RTL:** recommend re-architecting to cross a single encoded bus (gray/handshake) once, then decode in the destination domain. Constraints cannot fix this. |
| C7 | **"Quasi-static" / config-register crossing** (written once, static thereafter) | Not a dynamic crossing — but only if the "written once" assumption holds | **Waive with stated assumption:** `set_false_path` (or `waive_lint_violation`). State the assumption explicitly; **ask the user to confirm** the register is truly static during destination-clock operation. |
| C8 | **Clocks reported as crossing but actually synchronous/related** (common divider, known phase) | Not an async crossing at all | **Constraint:** define the relationship (`create_generated_clock`) so STA times it normally; do NOT `set_clock_groups -asynchronous` (that would hide a real timed path). |
| C9 | **Crossing into/out of an IP** (clk-wiz, async FIFO IP, AXI clock converter) | IP handles CDC internally if configured correctly | Verify IP config (`get_fifo_config` / `get_clocking_wizard_config` / `report_ip_status`); apply the IP's recommended `set_*` constraints. Don't hand-synchronize an IP boundary that's already safe. |

**Rule of thumb:** single-bit control → 2-FF synchronizer; multi-bit data → FIFO /
gray-code / handshake; reset → async-assert+sync-deassert. **A bank of independent
2-FF synchronizers on a bus is itself a defect (C3), not a remedy.**

---

## Resolution loop & STOP conditions

```
for each crossing in (Critical first, then Warning), one class at a time:
    measure   → report_cdc / report_cdc_details (or check_cdc_lint for RTL)
    classify  → map to C1..C9 above
    fix       → smallest safe change in the precedence ladder
                (constraint-only > recommend-RTL > waive-with-assumption)
    re-measure→ same tool; confirm THIS crossing dropped AND nothing new appeared
    (RTL change ⇒ re-synthesize before the netlist CDC report is valid again)
```

**STOP and hand back to the human when ANY of:**

- **Clean:** `report_cdc` on the **implemented** design shows **0 Critical, 0
  unexplained Warning**, every remaining waiver has a written assumption, and
  `report_methodology` shows no open `CDC-*` violations. Report the fresh evidence.
- **RTL change required:** the safe fix is a synchronizer / FIFO / re-architecture.
  Present the exact recommended RTL and **wait for user approval** before editing.
  Never silently rewrite RTL to make a number go green.
- **Ambiguous quasi-static waiver:** a crossing *might* be real and you cannot prove
  it is static from the design alone — present it and **ask the user** before waiving.
- **Missing clock definitions:** crossings are hidden because clocks aren't
  constrained. Stop, report the gap, and ask for / propose the clock constraints
  first — do not declare "clean" on an under-constrained design.
- **Constraint can't make a bus crossing meet skew** even though the structure is
  correct (C4): present the options (tighter floorplan, deeper FIFO, slower crossing
  clock) with their costs and stop. Do not relax/remove the `set_bus_skew` just to
  pass.
- **Two adversarial iterations with no net reduction** in Critical/unexplained
  Warning: stop thrashing; summarize remaining items with options and trade-offs.

Do not loop forever and do not "resolve" by deletion of evidence (removing waivers'
assumptions, false-pathing real crossings, disabling lint rules).

---

## Safety rails (do not violate)

- **No fake-pass.** Never apply `set_false_path`, `set_clock_groups -asynchronous`,
  `set_max_delay`, `disable_lint_rule`, or `waive_lint_violation` to a crossing that
  could be a real, unsynchronized metastability path **just to clear the report**. A
  constraint silences STA; it adds no hardware. Waivers/false-paths are allowed ONLY
  for confirmed non-crossings (C7/C8) **with a written assumption**, and if there's
  any doubt the path is real, **ask the user first.**
- **Constraint ≠ correctness.** `set_clock_groups -asynchronous` is correct ONLY when
  a real synchronizer already protects the crossing (C2/C4). Applying it to an
  unsynchronized crossing (C1/C3) hides a live bug. Confirm the synchronizer exists
  (`report_cdc_details` / `read_file`) before grouping.
- **Smallest safe change first.** Constraints/strategy before RTL. Only escalate to
  RTL when no safe constraint exists, and then **recommend, do not silently apply.**
- **Recommend RTL, never sneak it.** Synchronizer insertion, FIFO swap-in, and reset
  re-architecture change design behavior. Present the diff and get approval.
- **One crossing-class per iteration** so cause→effect is attributable; re-measure
  after each.
- **Evidence before claims.** "CDC clean," "metastability-safe," and "crossings
  resolved" each REQUIRE fresh tool output — and for **signoff**, fresh
  **post-implementation** `report_cdc` + `report_methodology`. Synthesis-level or
  lint-level results are necessary-not-sufficient. Never infer cleanliness from a
  source edit.
- **A bus is not single bits.** Never recommend per-bit 2-FF synchronizers on a
  multi-bit data bus (C3) — that is a coherency bug. Use FIFO / gray-code / handshake.
- **Don't hide real timing.** Don't `set_clock_groups -asynchronous` on clocks that
  are actually related (C8); define the generated-clock relationship instead so the
  timed path stays timed.
- **Bounded effort.** When safe options are exhausted, surface the remaining items
  with trade-offs and hand back. Do not thrash.

---

## Output (report format)

Produce a CDC audit report with:

1. **Environment** — Vivado version, project, top module, clock list (from
   `get_all_clocks`), and which design stage the verdict is based on (RTL-lint /
   synthesized / **implemented**). State it plainly if no post-implementation
   evidence was collected — then the verdict is "preliminary," not "signoff."
2. **Crossing inventory** — table of clock-pair crossings from
   `report_clock_interaction`, each marked async / synchronous / handled-by-IP.
3. **Baseline counts** — Critical / Warning / Info from the first `report_cdc`
   (or `check_cdc_lint`), quoted from tool output.
4. **Per-crossing findings** — for each Critical/Warning: source→dest clock, width,
   classification (C1–C9), structural diagnosis, and the action taken or recommended.
5. **Changes applied** — constraints added (with the exact `set_*` rationale) and any
   RTL edits **the user approved**, each tied to its crossing.
6. **Waivers** — every `set_false_path` / `set_clock_groups` / `waive_lint_violation`
   with its **explicit stated assumption** and whether the user confirmed it.
7. **Final verdict with fresh evidence** — post-implementation `report_cdc` counts +
   `report_methodology` CDC-rule status (and `report_timing_summary` for any
   `set_bus_skew`). Quote the numbers. **If post-implementation evidence is absent,
   say "NOT signed off"** and list exactly what remains.
8. **Open items / trade-offs** — anything requiring a human decision (RTL approval,
   ambiguous waiver, structural re-architecture), with options and costs.
