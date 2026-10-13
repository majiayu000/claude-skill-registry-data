---
name: bitstream-program
description: >
  Generate a bitstream and program a Xilinx FPGA over JTAG, or build an MCS
  image and burn it into SPI/BPI configuration flash for power-on boot.
  Invoke when the user says "program the board", "generate bitstream",
  "flash the device", "download to FPGA", "burn the flash", "load my design
  onto the board", "make a .mcs / .bit", or "why won't my board come up after
  power cycle". Covers the full hand-off from a routed implementation to live
  silicon: DRC + route + timing sign-off gating, .bit generation,
  hardware-server / JTAG connect, volatile JTAG download, and non-volatile
  flash programming (generate_mcs + add_flash_configuration + program_flash).
  Requires the SynthPilot MCP server with Vivado running and the Tcl server
  connected; flash / JTAG steps additionally require a physical board cabled to
  the host (or reachable through a remote hw_server).
---

# Bitstream Generation & Device Programming

A methodology playbook for taking a **routed implementation** all the way to
**live silicon** — either a volatile JTAG download (lost on power cycle) or a
non-volatile flash burn (boots on power-up). Programming hardware is a one-way,
physical action: this skill is deliberately conservative. It refuses to fabricate
a "programmed OK" claim, refuses to skip sign-off gates, and hands control back
to the human at every ambiguous fork (which device, which flash part, which
boot mode).

This skill is a **strategy layer** over the SynthPilot MCP server. It does not
write code; it decides which real tools to call, in what order, and when to STOP.

---

## When to use

- User wants a `.bit` produced from the current implemented design.
- User wants to **download** a design to a board over JTAG for a bench test
  (volatile — gone after power cycle).
- User wants to **flash** the design (`.mcs`/`.bin`) into SPI/BPI configuration
  memory so the FPGA boots it automatically on power-up.
- User reports a board that "doesn't come up after power cycle" (almost always a
  flash / boot-mode issue, not a JTAG issue).
- User wants an `.xsa` hand-off to Vitis (export hardware **with** bitstream).

## When NOT to use

- **Timing is not met / design is not routed.** A `.bit` from a design with
  setup/hold violations may program but will behave non-deterministically. Close
  timing first (use the **timing-closure** skill). Do not generate a sign-off
  bitstream over an open WNS violation without an explicit, stated user override.
- **Synthesis/implementation has not run** or is stale relative to the RTL.
  Generating a bitstream does not re-run P&R; it ships whatever is in the run.
  Run/refresh implementation first.
- **Debug-core insertion** (ILA/VIO) — that belongs to the debug/instrumentation
  skill. This skill only *consumes* an already-inserted `.ltx` probes file.
- **Pure simulation** requests — use the simulation skill.
- **Block-design / IP build** — use the block-design skill; come back here once a
  routed implementation exists.

---

## Prerequisites (verify first)

Do not assume state. Probe it with real tools before acting.

1. **MCP / Vivado / Tcl bridge alive** — `test_connection`. If this fails,
   nothing downstream can work; stop and tell the user to start Vivado and the
   Tcl server.
2. **A project is open and is the right one** — `get_project_info`. Confirm the
   part/board matches what the user intends to program. The wrong part silently
   produces a bitstream the device will reject.
3. **Implementation is complete and current** — `get_run_status`. The
   implementation run must be `route_design Complete` (or equivalent "routed").
   If it is `synth-only`, out of date, or failed, the design is **not ready** —
   go run/finish implementation (see Methodology step 1) before any bitstream.
4. **For any JTAG/flash step: a board is physically present.** This cannot be
   inferred from software state alone. The hardware-manager connect chain
   (Methodology step 5) is what discovers it; if no target appears, STOP and ask
   the user to plug in / power on the board and check the cable.

State everything you found before proceeding. If a prerequisite is missing,
report it and stop — do not improvise around a missing board or an unrouted run.

---

## Methodology (real tool calls, in order)

The flow has three phases: **(A) sign-off gate → (B) bitstream → (C) deliver to
device.** Phase C splits into a *volatile JTAG* lane and a *non-volatile flash*
lane. Pick the lane from the decision table below; do not run both blindly.

### Phase A — Sign-off gate (MUST pass before any bitstream)

A bitstream is only as trustworthy as the implemented design behind it. These are
**fresh-evidence** gates: read them now, do not trust a prior claim.

1. **Ensure a complete implementation exists.**
   - `get_run_status` → if not routed, run it. For multi-minute P&R prefer the
     async pattern: `run_implementation_async`, then poll `get_run_status` until
     complete. (`run_implementation` is the synchronous fallback for short runs.)
   - On completion, `open_implemented_design` so the reports below read the
     routed netlist, not synthesis.

2. **Route completeness** — `report_route_status`. Every net must be fully
   routed. Any unrouted / partially-routed / conflict nets ⇒ **not signable** —
   stop and route (or report the failure). A `.bit` over an incomplete route is
   invalid.

3. **DRC** — `report_drc`. Resolve (or consciously, with the user, accept)
   **Critical Warnings/Errors** before programming. Bitstream-relevant DRCs
   (e.g. `DRC BIVRT`, unconstrained I/O, config-bank/voltage, BUFGCE/clock
   placement) can produce a `.bit` that damages or refuses to configure the part.
   Do **not** waive a config/IO DRC just to get a green light — see Safety rails.

4. **Timing sign-off** — `report_timing_summary`. Read WNS/TNS/WHS fresh.
   - WNS ≥ 0 and WHS ≥ 0 (no setup/hold failures) ⇒ pass the timing gate.
   - WNS < 0 or WHS < 0 ⇒ the design is **not signed off**. Do not silently
     proceed. Report the violation and hand back to timing-closure. Only generate
     a bitstream over open violations if the user explicitly says "I know timing
     fails, build it anyway for a quick bench test" — and then label the artifact
     as **not sign-off quality** in the Output.

> Gate rule: a "ready to program" claim REQUIRES fresh `report_route_status` +
> `report_drc` + `report_timing_summary` output in this session. Never infer it.

### Phase B — Generate the bitstream

5. **Generate** — `generate_bitstream` (synchronous; `jobs` defaults to 4).
   - This step embeds the routed configuration and (if debug cores were inserted)
     emits a `.ltx` probes file next to the `.bit`.
   - On return, capture the reported `.bit` path. If generation **fails**, read
     the error summary it returns — common causes are config-bank voltage
     (`CONFIG_VOLTAGE`/`CFGBVS`) or `BITSTREAM.*` property DRCs surfaced only at
     write time. Fix the property/constraint (smallest safe change), re-run the
     Phase-A DRC, and regenerate. Do not retry blindly.

### Phase C — Deliver to the device

Choose the lane from the **Decision table**. Establish the hardware connection
(common to both lanes) first.

6. **Connect to hardware** (JTAG/flash both need this):
   - `open_hardware_manager`
   - `connect_hardware_server` (defaults to `localhost:3121`; pass a `url` for a
     remote `hw_server`).
   - `open_hardware_target` (empty arg auto-selects the first target).
   - `list_hardware_devices` — **confirm the discovered device matches the
     project part** from step (Prereq 2). If the chain is empty, STOP: no board /
     bad cable / hw_server not running. If the part mismatches, STOP and ask —
     programming the wrong device is a hardware risk.

   > Shortcut: `quick_program` auto-connects and downloads the current project
   > bitstream in one call (and auto-skips Zynq `arm_*` debug devices). Prefer it
   > **only** when the chain is unambiguous (single FPGA, default hw_server) and
   > Phase A has already passed. For multi-device chains, remote servers, or any
   > ambiguity, use the explicit connect chain above so you can verify the device
   > before committing.

#### Lane 1 — Volatile JTAG download (bench test; lost on power cycle)

7. **Program over JTAG** — `program_device`.
   - Leave `bitstream_path` empty to use the project default, or pass the path
     captured in step 5.
   - It auto-associates a `.ltx` probes file found beside the bitstream and
     refreshes the device afterward.
   - If you need a fresh status snapshot, `refresh_hardware_device`.
   - **Verify, don't assume:** report the tool's success/DONE status as the
     evidence. A volatile download is *not* persistent — say so explicitly so the
     user knows a power cycle wipes it.

#### Lane 2 — Non-volatile flash (boots on power-up)

7. **Pick the flash part — ask, don't guess.** The configuration-memory part
   number and interface (SPI x1/x2/x4, QSPI, BPI) are **board-specific**. The
   wrong part/width burns a non-bootable image. If the user hasn't named the
   exact part, ask. Then `add_flash_configuration` with the correct
   `flash_type` (e.g. a `s25fl…`, `mt25q…`, etc. part string).

8. **Build the flash image** — `generate_mcs`.
   - Inputs: `bitstream_path` (from step 5), an output `mcs_path`, and
     `flash_size` (MB) that **matches the physical flash density** (default 128).
     A size larger than the device, or a wrong start address, yields a
     non-bootable image.
   - For QSPI boot, confirm the design's `BITSTREAM.CONFIG.SPI_BUSWIDTH` /
     `CONFIG.CONFIGRATE` match the flash wiring; a x4 image into x1 wiring won't
     boot. If these properties are unset, raise it before burning.

9. **Burn the flash** — `program_flash` with the `mcs_file` from step 8.
   - This writes (and the tool verifies) the configuration memory. Report the
     tool's verify result as evidence.

10. **Prove it boots from flash — the only real test of a flash burn.** A
    successful *write+verify* proves the bytes are in flash; it does **not** prove
    the FPGA will configure from them. Instruct the user to set the board to the
    correct **boot mode** (e.g. QSPI/Master-SPI strap or `MODE[2:0]` pins),
    **power-cycle**, and confirm the DONE LED / design behavior. Then
    `refresh_hardware_device` / `list_hardware_devices` to see the device now
    re-configured from flash. If it doesn't come up, this is the classic
    "won't come up after power cycle" failure — go to the troubleshooting table.

### Optional — Hand off to embedded software

11. If the user wants Vitis / bare-metal / Linux work, `export_hardware`
    (`include_bitstream=True`) to emit the `.xsa`, then hand off to the embedded
    skill. Do not attempt the software build here.

---

## Decision table — which lane and which fix

| Symptom / request                                              | Likely cause                                           | Smallest safe action (in order)                                                                 |
|----------------------------------------------------------------|--------------------------------------------------------|-------------------------------------------------------------------------------------------------|
| "Just test it on the bench now"                                | Volatile download is fine                              | Lane 1: `program_device` (or `quick_program` if chain is unambiguous)                            |
| "It must boot by itself on power-up"                           | Needs non-volatile config memory                       | Lane 2: `add_flash_configuration` → `generate_mcs` → `program_flash` → verify boot              |
| `generate_bitstream` fails with `CFGBVS`/`CONFIG_VOLTAGE` DRC  | Config bank voltage not declared                       | Add/correct `CFGBVS`/`CONFIG_VOLTAGE` in XDC (constraint, not RTL), re-run `report_drc`, regen   |
| `generate_bitstream` fails with unconstrained-I/O DRC          | Pins/IOSTANDARD missing                                | Add I/O constraints (`create_io_constraint`), re-run `report_drc`, regenerate                    |
| `list_hardware_devices` returns empty                          | No board / cable / hw_server down                      | STOP. Ask user to connect & power the board; check JTAG cable; confirm `hw_server` running       |
| Discovered device ≠ project part                               | Wrong board, wrong target, or wrong project open       | STOP. Do **not** program. Reconcile target vs part with the user                                 |
| Zynq: extra `arm_*` targets on chain                           | PS debug devices appear alongside the PL               | Program the PL FPGA device; `quick_program` auto-skips `arm_*`                                    |
| JTAG download works, but dead after power cycle                | Design was only in volatile SRAM config, not in flash  | Lane 2: program flash + set correct boot-mode straps + power-cycle                               |
| Flash burned + verified, still won't boot from flash           | Wrong boot mode, wrong flash part/size, or bus width   | Re-check `flash_type` & `flash_size` vs board; check boot-mode pins & `SPI_BUSWIDTH`; re-burn    |
| WNS < 0 but user wants a bitstream                              | Design not signed off                                  | Report violation; default = refuse sign-off `.bit`; build only on explicit "bench test anyway"   |
| Need Vitis / software image                                    | Hardware hand-off                                      | `export_hardware(include_bitstream=True)` → embedded skill                                       |

---

## Programming loop + STOP conditions

Programming is iterative only on **failure-to-configure**; a clean program is a
single pass. The loop exists to converge a *non-booting* device, one change-class
per iteration so cause→effect is attributable.

```
[Phase A gates] → generate_bitstream → connect HW → verify device==part
        → program (Lane 1 or Lane 2) → READ device status (fresh)
                │
          configured/DONE asserted? ──yes──► STOP (success, with evidence)
                │ no
                ▼
  Classify ONE failure class (boot mode | flash part/size | bus width |
                              config DRC | wrong device) → apply ONE fix
                              → re-verify with a tool → loop
```

**STOP immediately (do not iterate) when:**

- **No board / chain empty** → hand back to user (physical action required).
- **Discovered device ≠ project part** → never program a mismatched device.
- **A DRC/timing gate is failing** and the user has not explicitly authorized a
  non-sign-off build → hand back to the relevant skill.
- **Success:** the device reports configured / DONE asserted (JTAG lane), or the
  board re-configures from flash after a power cycle (flash lane), confirmed by a
  fresh `refresh_hardware_device` / `list_hardware_devices`.

**STOP and present options (don't thrash) when:**

- You've tried the obvious fix in a failure class (e.g. corrected `flash_type`
  once) and it still won't boot. Surface the remaining hypotheses (boot-mode
  straps, flash density, bus width, board power) **with their costs**, and hand
  back to the human. Do not loop on flash parts blindly — each burn wears the
  device and may not be the real cause.

---

## Safety rails (do not violate)

1. **No fake-pass on the sign-off gate.** Never waive a route/DRC/timing failure
   — or apply `set_false_path` / `waive_lint_violation` / disable a DRC — purely
   to make `generate_bitstream` succeed or to declare the design "ready". A
   config-bank, I/O, or clocking DRC can mean the bitstream will *not configure*
   or could *electrically stress* the part. If a violation might be real, fix it
   or ask the user; state any assumption explicitly.

2. **Evidence before claims — always.** "Bitstream generated", "device
   programmed", "flash verified", "boots from flash" each REQUIRE the
   corresponding fresh tool output *in this session*
   (`generate_bitstream` path, `program_device`/`program_flash` status,
   `refresh_hardware_device`/`list_hardware_devices`). Never infer success from a
   prior step, and never report a flash burn as "boots" until a power-cycle
   re-config is observed.

3. **Confirm the target device before you commit.** Always reconcile
   `list_hardware_devices` against the project part before `program_device` /
   `program_flash`. Programming the wrong device or wrong flash part is a physical
   hazard, not a software typo.

4. **Ask before destructive / board-specific choices.** Flash part number, flash
   size, bus width, and boot mode are board facts you cannot derive from the
   project. If unknown, ask — do not pick a plausible default and burn it.

5. **Smallest safe change first.** Bitstream-write DRC failures are almost always
   *constraint/property* fixes (XDC: `CFGBVS`, `CONFIG_VOLTAGE`, IOSTANDARD,
   `BITSTREAM.*`), not RTL. Fix constraints first. Recommend — never silently
   apply — any RTL change; that re-opens synth/impl and a new sign-off.

6. **Volatile vs non-volatile must be stated.** Always tell the user whether what
   you just did survives a power cycle. A JTAG `program_device` does **not**; only
   a flash burn does.

7. **One change-class per iteration.** When chasing a non-booting board, change
   exactly one thing (boot mode *or* flash part *or* bus width) and re-measure, so
   the fix that worked is unambiguous.

---

## Output

Report concisely, with **evidence quoted from tool output**, not narration:

- **Readiness gate** — route status (fully routed?), DRC (Critical count and any
  un-waived items), and timing (WNS / WHS / TNS), each with the tool that
  produced it. State pass/fail explicitly. If any gate failed and you proceeded
  anyway, label the artifact **NOT sign-off quality** and name the override.
- **Bitstream** — the `.bit` path returned by `generate_bitstream`, and whether a
  `.ltx` probes file accompanied it.
- **Target** — the discovered device(s) from `list_hardware_devices` and explicit
  confirmation it matches the project part.
- **Programming result** —
  - *Lane 1:* `program_device` status (DONE asserted / configured), and a clear
    note that **this is volatile (lost on power cycle).**
  - *Lane 2:* `flash_type`, `flash_size`, the `.mcs` path, the `program_flash`
    write+verify result, and the **boot-mode + power-cycle instruction** the user
    must perform — plus the post-power-cycle `list_hardware_devices` evidence if
    obtained.
- **If stopped:** the exact blocking condition (no board / device mismatch /
  failing gate / exhausted safe options) and the specific decision or physical
  action handed back to the user — with options + costs, not a guess.

Never end with an unverified "done." End with the evidence, or with the precise
reason you stopped.
