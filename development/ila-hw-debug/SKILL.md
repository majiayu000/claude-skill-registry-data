---
name: ila-hw-debug
description: >
  Insert/connect an ILA (Integrated Logic Analyzer), program the board, arm a
  trigger, and read back captured waveforms on real FPGA hardware. Use when the
  user says "debug on hardware", "insert ILA", "capture waveform on the board",
  "the design works in sim but fails on the board", "trigger when X happens on
  hardware", "probe a signal live", "read the ILA", or wants to observe live
  silicon behavior via JTAG. Covers the full loop: mark/insert debug cores ->
  re-implement -> bitstream -> connect hardware server -> program with .ltx
  probes -> set trigger -> arm -> capture -> read CSV.
  Requires the SynthPilot MCP server with Vivado open and tcl_server.tcl running,
  plus a physical JTAG-connected board and a running hw_server (hardware server).
---

# ILA Hardware Debug

On-silicon debug methodology. Insert an Integrated Logic Analyzer (ILA), re-run
implementation so the debug core is real in the routed netlist, program the board
with the matching probes file, arm a trigger, capture, and read back the
waveform. This is for behavior you cannot see in simulation: real I/O timing,
real PLL lock, real DDR/transceiver/external-device interaction, metastability,
and "works in sim, fails on the board" bugs.

The discipline here is the same as timing closure: **observe before you change,
insert the smallest probe that answers the question, capture FRESH hardware
evidence before claiming anything, and never invent a "trigger hit" you did not
read back from the device.**

## When to use

- "Debug on hardware", "insert an ILA", "capture a waveform on the board".
- A design passes simulation but misbehaves on real silicon (I/O, clocking,
  external memory/peripheral, link training, reset sequencing).
- You need to trigger on a specific live condition (`state == ERROR`, `fifo_full
  && wr_en`, an address range) and see the surrounding cycles.
- You need to read a current live value or drive a control bit at runtime (VIO).
- You need to verify a fix actually took effect *in hardware*, not just in a report.

## When NOT to use

- The bug is reproducible in **simulation** -> use the simulation skill
  (`sim_compile` / `sim_run` / `sim_probe`). Sim is faster, fully observable, and
  free; exhaust it first. ILA only sees what you wired up and only after a full
  build.
- A **timing** problem (WNS/TNS negative) -> close timing first. Probing a design
  that does not meet timing gives you garbage captures; the timing-closure skill
  comes first.
- You only need static facts about the routed design (utilization, DRC, timing,
  power) -> those are report tools, no hardware needed.
- You want to *change RTL behavior*. ILA observes; it does not fix. Use it to
  localize, then hand the root cause to the RTL/timing/CDC skill.

## Prerequisites (verify first)

Do not skip. Most "ILA doesn't work" reports are a broken prerequisite, not a bug.

1. **MCP + Vivado link alive:** `test_connection`. If it fails, the Tcl server
   inside Vivado is not running — stop and tell the user to start it.
2. **A project is open** with a known top: `get_project_info`. ILA insertion edits
   *this* design.
3. **Decide the insertion path** (see Decision Table). Confirm which one the
   design uses before touching anything:
   - **Netlist (HDL) flow:** mark signals in RTL -> `setup_debug` on the
     synthesized netlist. Use `list_source_files` to confirm the RTL exists.
   - **Block Design flow:** `list_block_designs`; instantiate `bd_create_ila` /
     `bd_create_system_ila` and wire probes in the BD.
4. **Physical board reachable (for the program/capture half):**
   - `open_hardware_manager`
   - `connect_hardware_server` (default `localhost:3121` — a `hw_server` process
     must be running and the board powered + JTAG-connected). If this fails, it is
     an environment problem: no board, no driver, or `hw_server` down. **Say so —
     do not fake a capture.**
   - `list_hardware_targets` then `open_hardware_target` — confirm a target exists.
   - `list_hardware_devices` — confirm the FPGA is detected on the JTAG chain.
5. **A debug-enabled bitstream + its `.ltx`** must exist before you can capture.
   If the current bitstream has no debug core, you are in Phase A (insert), not
   Phase C (capture).

If any prerequisite fails, report exactly which one and stop. Do not proceed with
a half-connected toolchain.

---

## METHODOLOGY

The flow has three phases. **Phase A** (insert + rebuild) only runs if the design
does not already contain the ILA you need. **Phase B** (program). **Phase C**
(arm, capture, read). If a debug bitstream + `.ltx` already exist for the exact
signals you need, skip straight to Phase B.

### Phase A — Insert / connect the ILA (only if not already present)

**A1. Pick the smallest probe set that answers the question.**
State, before inserting, *what condition you are hunting* and *which signals
prove or disprove it*. ILA costs BRAM and routing; do not blanket-probe a bus you
do not need. Width × depth is the budget — capture the suspect control/handshake
signals and the few data bits that matter.

**A2a. Netlist (HDL) insertion — preferred when probing internal RTL signals:**
  1. `mark_debug_signal` for each signal of interest. (Equivalently, the user can
     add `(* MARK_DEBUG = "true" *)` in RTL; `list_debug_signals` confirms what is
     marked.) These signals must survive synthesis — a signal optimized away
     cannot be probed; if it is missing after synth, it was merged/trimmed.
  2. `run_synthesis_async` -> poll `get_run_status` until done -> `get_synthesis_report`.
     Use `open_synthesized_design` so the netlist is in memory.
  3. `setup_debug` — auto-builds the ILA core and connects all `MARK_DEBUG`
     signals (one clock domain per ILA core; mixed-domain signals need separate
     cores or you get an invalid setup).
  4. `list_debug_cores` + `list_debug_signals` — **verify** the core exists and the
     intended signals are actually attached before spending a build.
  5. `implement_debug_core` then `write_debug_probes` (produces the `.ltx` that the
     hardware side needs to name probes). Keep the `.ltx` next to the bitstream so
     `program_device` auto-associates it.

**A2b. Block-Design insertion — preferred for AXI / interface / system-level debug:**
  1. `bd_create_system_ila` (interface-aware, for AXI/AXIS/handshake interfaces) or
     `bd_create_ila` (pin-level) and configure depth with `bd_ila_set_probe_width`
     / `bd_system_ila_set_slot` as needed.
  2. `bd_connect_system_ila_interface` (interface) or `bd_connect_ila_probe` +
     `bd_connect_ila_clock` (pins). The ILA clock MUST be the clock of the domain
     you are sampling.
  3. `bd_validate_design` — **must pass clean** before generating. Unconnected
     probe/clock = invalid capture.
  4. `bd_generate_output_and_wrapper`, then `bd_wait_on_output_generation` /
     `bd_check_output_status`.

**A3. Size the ILA deliberately** (`create_ila` if instantiating directly, else
the BD config tools). `sample_depth` ∈ {1024 … 131072}: deeper = more BRAM, more
build time. `num_probes` up to 64. Start modest; widen only if the first capture
proves you need more window or more signals.

**A4. Re-implement and re-bitstream — the debug core must be real in routed
silicon.**
  - `run_implementation_async` -> poll `get_run_status` until complete.
  - `report_drc` — **must be clean** (debug-core insertion can introduce real DRC
    issues; do not ignore them).
  - Check timing did not regress from the inserted core: `report_timing_summary`
    -> `extract_timing_metrics`. If WNS went negative because of the ILA, that is a
    real regression — hand to the timing skill; **do not** paper over it.
  - `generate_bitstream`. Confirm the returned `.bit` path. `write_debug_probes`
    must have produced the matching `.ltx`.

> One change-class per build. Do not simultaneously add probes, retime RTL, and
> tweak strategy — if the next capture looks wrong you will not know which change
> caused it.

### Phase B — Program the board

  1. Re-confirm the live connection: `open_hardware_manager`,
     `connect_hardware_server`, `open_hardware_target`, `list_hardware_devices`.
  2. `program_device` with the debug `.bit`. Leave `probes_file` empty to
     auto-detect the `.ltx` beside the bitstream, or pass it explicitly. **The
     `.ltx` MUST match this exact bitstream** — a stale `.ltx` gives wrong/garbage
     probe names and silently meaningless captures.
  3. `refresh_hardware_device` then `hw_ila_list` — **verify** the ILA core(s)
     appear with the expected probe count. No ILA listed = wrong bitstream, missing
     `.ltx`, or insertion failed. Stop and fix; do not pretend to capture.

### Phase C — Arm, trigger, capture, read

  1. `hw_ila_get_status` — read current core status, depth, and probe names. Use
     the **exact probe names it returns** for all trigger calls.
  2. **Set the trigger** (the heart of useful capture):
     - `hw_ila_set_trigger(probe, value, operator, radix)` per probe. Use
       `radix="bin"` with `X` don't-care bits for bit-field conditions
       (e.g. `"XXXX1XXX"`), `radix="dec"`/`"hex"` for values, and `operator`
       ∈ eq/neq/gt/lt for ranges.
     - Multiple probes: `hw_ila_set_trigger_condition("AND" | "OR")` to combine.
     - `hw_ila_clear_trigger` to reset a probe (or all) if you mis-set it.
     - For a free-running snapshot with no condition, skip the trigger and use
       `trigger_now=True` in the next step.
  3. **Confirm the trigger before arming:** `hw_ila_get_status` again and read back
     the per-probe compare values and AND/OR mode. The condition you *intended*
     must be the condition shown. Set `trigger_position` so you capture enough
     pre-trigger context (e.g. center the window).
  4. **Arm:** `hw_ila_run` (or `hw_ila_run(trigger_now=True)` for immediate).
     Status should report ARMED (or TRIGGERED if it fired instantly).
  5. **Provoke the condition.** If a runtime stimulus is needed and a VIO exists,
     `hw_vio_list` -> `hw_vio_get_probes` -> `hw_vio_write` to drive control bits,
     `hw_vio_read` to observe live values. Otherwise the DUT/external event drives it.
  6. **Wait for capture:** `hw_ila_wait(timeout=N)`. Final status IDLE = capture
     complete (trigger hit + buffer full). Still ARMED after timeout = **trigger
     never fired** — that is a real result, not an error to hide (see loop).
  7. **Read back:** `hw_ila_read_data(file_path="...csv")` to upload the samples and
     save the waveform CSV. Report the sample count and CSV path. This CSV — not
     any inference — is the evidence.
  8. Cleanly `disconnect_hardware` when the session is done (leaving the target
     open can block other tools / other users of the board).

---

## Decision table — symptom -> likely cause -> safe next action

| Symptom (from a tool, not a guess) | Likely cause | Smallest safe action |
|---|---|---|
| `connect_hardware_server` fails | `hw_server` down / board off / JTAG unplugged | Environment problem — report it; do not fabricate a capture |
| `list_hardware_devices` empty | Wrong target, power, or cable | `refresh_hardware_device`, re-`open_hardware_target`; if still empty, hardware issue |
| `hw_ila_list` empty after programming | Bitstream has no debug core, or `.ltx` not associated | Re-program with the **debug** `.bit`; confirm matching `.ltx`; if none exists, do Phase A |
| Probe name from RTL not in `hw_ila_get_status` | Signal optimized away in synth, or stale `.ltx` | Re-check `list_debug_signals`; if trimmed, mark a retained equivalent / add `keep`; regenerate `.ltx` with the bitstream |
| `hw_ila_wait` stays ARMED (never triggers) | Trigger condition never true, wrong radix, wrong probe, or signal stuck | Re-verify condition via `hw_ila_get_status`; loosen with don't-cares / `trigger_now=True` to snapshot; check the signal is even toggling |
| Capture looks like noise / constant | Wrong clock domain on ILA, or `.ltx`/`.bit` mismatch | Confirm ILA clock = sampled domain; re-pair `.bit` + `.ltx`; rebuild if domain is wrong |
| ILA insertion broke timing (WNS<0) | Debug core added load/routing pressure | Reduce depth/probe count; if still negative, hand to **timing-closure skill** — do not waive |
| `report_drc` errors after `implement_debug_core` | Real DRC from inserted core (clocking, BUFG, etc.) | Fix the DRC; never ignore to force a bitstream |
| Need to *change* a control bit live | Static probing insufficient | Add/Use a VIO (`bd_create_vio` / `create_vio`), then `hw_vio_write` |

---

## Capture loop (iterate until the trigger answers the question)

This is a **measure -> adjust trigger -> re-measure** loop. The *only* thing that
changes between iterations should be the **trigger condition**, not the bitstream
— re-arming is seconds, re-building is minutes.

```
1. hw_ila_get_status                  # confirm probes + current condition
2. hw_ila_set_trigger (+ condition)   # one trigger hypothesis at a time
3. hw_ila_get_status                  # VERIFY the condition you intended is set
4. hw_ila_run                         # arm
5. (provoke; hw_vio_write if needed)
6. hw_ila_wait(timeout=N)             # IDLE = captured; ARMED = no trigger
7. hw_ila_read_data(file_path=...)    # save CSV evidence
   -> inspect: did the captured window contain the event?
```

**STOP conditions — halt the loop and report:**
- **Captured the event:** `hw_ila_wait` returned IDLE and the CSV shows the
  condition + surrounding cycles. Done — report the CSV.
- **Trigger genuinely never fires** after loosening (don't-cares / `trigger_now`)
  and you have confirmed the probe is toggling: this is a *finding* — the
  condition you expected does not occur in hardware. Report it; hand the root
  cause to the RTL/CDC/timing skill. Do **not** keep re-arming hoping it changes.
- **Window too small / wrong signals:** if you need a deeper buffer or more probes
  than the current core has, you must return to **Phase A** (rebuild). Do this
  deliberately, one change-class at a time — note it as a build iteration, not a
  loop iteration.
- **Need an RTL/architectural fix:** ILA localized the bug. ILA cannot fix it.
  Present the captured evidence + the hypothesis and hand off. Do not loop.
- **Hardware/connection lost mid-loop:** `refresh_hardware_device`; if the device
  is gone, stop — it is an environment failure, not something to retry forever.

Each iteration, show the trigger you set and the resulting status (ARMED vs IDLE)
so cause and effect are attributable.

---

## Safety rails (do not violate)

- **Evidence before claims.** "Triggered", "captured", "the signal does X on
  hardware" REQUIRE a fresh `hw_ila_wait` IDLE result and a real
  `hw_ila_read_data` CSV from *this* programmed device. Never infer a capture from
  simulation, from a report, or from a prior run. If you did not read it back from
  silicon, you do not know it.
- **`.ltx` must match the `.bit`.** Programming a debug bitstream with a stale or
  foreign `.ltx` yields plausible-looking but meaningless probe names and data.
  Always regenerate `write_debug_probes` with the bitstream and verify probe names
  via `hw_ila_get_status`.
- **No fake-pass on the rebuild.** Inserting an ILA can create real DRC violations
  or break timing (WNS<0). Do NOT waive DRC, `set_false_path`, or relax timing
  just to get a debug bitstream out. If the inserted core breaks signoff, that is
  a real regression — reduce the probe budget or hand to the timing/DRC skill.
  Any exception requires an explicit stated assumption and, if it could be real,
  asking the user first.
- **Observe, don't silently edit.** ILA is a measurement instrument. Do not modify
  RTL to "make the trigger fire." If the design must change, *recommend* the edit
  with the captured evidence; let the human / the RTL skill apply it.
- **Smallest probe first.** Constraints/marking before re-architecting; a few
  targeted probes before a wide bus. Don't blow the BRAM/depth budget on a
  fishing expedition.
- **No invented tools.** Only the `hw_ila_*`, `hw_vio_*`, `hw_axi_*`, hardware-
  manager, `*_debug*`, `bd_*ila*`, and build tools named here exist. If a needed
  capability (e.g. cross-trigger, advanced sequencer) is not in the toolset, say
  so plainly rather than pretending.
- **VIO writes drive real hardware.** `hw_vio_write` toggles live control bits on a
  running board. Only drive probes whose effect you and the user understand;
  confirm before writing anything that could put external hardware in a bad state.
- **Leave the target clean.** `disconnect_hardware` when done so the board/JTAG is
  not left locked.

---

## Output

Report, in order:

1. **Insertion summary (if Phase A ran):** which path (netlist vs BD), signals
   probed (from `list_debug_signals` / `hw_ila_get_status`), ILA depth × probe
   count, and the post-implementation evidence that the rebuild is clean —
   `report_drc` result + WNS/TNS from `extract_timing_metrics`. State explicitly
   whether the ILA changed timing.
2. **Program confirmation:** bitstream path, `.ltx` path, and the `hw_ila_list`
   output proving the core is live on the device.
3. **Trigger setup:** the exact per-probe compare values + AND/OR mode, copied
   from `hw_ila_get_status` (the *verified* condition, not the intended one).
4. **Capture result:** final `hw_ila_wait` status (IDLE = success), sample count,
   and the saved CSV path from `hw_ila_read_data`. If it never triggered, say so
   and state what that implies.
5. **Finding + handoff:** what the waveform shows about the original question, and
   — if a fix is needed — the recommended RTL/timing/CDC action handed to the
   appropriate skill, with the CSV as evidence. Never close with an unverified
   "fixed on hardware" claim.
