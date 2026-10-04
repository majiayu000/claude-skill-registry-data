---
name: hcs-a02-computer-organization-lab
description: Build and verify computer organization labs for the HCS-A02 teaching FPGA board. Use when working on HCS-A02, Verilog/Vivado experiments, testbenches, simulation-first debugging, XDC pin constraints, seven-segment displays, LEDs, switches, buttons, traffic lights, or bitstream generation for computer organization coursework.
---

# HCS-A02 Computer Organization Lab

## Core Workflow

Follow this order for every experiment:

1. Understand the requirement and identify the observable behavior on switches, buttons, LEDs, traffic lights, or seven-segment displays.
2. Write the smallest clear Verilog implementation that satisfies the current experiment.
3. Write a testbench that covers the required behavior and the key boundary cases.
4. Run simulation and judge logic correctness from the waveform or self-checking output.
5. Only after simulation passes, add or update XDC pin constraints for HCS-A02.
6. Generate the Vivado bitstream and test on the board.

If simulation fails, return to the Verilog or testbench before editing constraints or generating a bitstream.

## Repository First

Prefer the existing project structure, module names, scripts, and Vivado project files in the current repository. Keep changes scoped to the current lab.

If no suitable structure exists, create a minimal lab from the bundled template:

```powershell
pwsh -File <skill-dir>\scripts\new_hcs_a02_lab.ps1 -Destination <lab-dir> -ModuleName top
```

Use `-Force` only when intentionally replacing generated template files.

## HCS-A02 Board Usage

Read `references/hcs-a02-board.md` when pin names, electrical polarity, or device layout matters.

Default assumptions:

- Switches `sw[35:0]`: up is `1`, down is `0`.
- Buttons `bt[7:0]`: pressed is `1`, released is `0`; hardware debounce is already present.
- LEDs and traffic lights: output `1` turns the light on.
- Seven-segment display: common-anode, template uses active-low digit select `an[7:0]`, active-low segments `seg[6:0]`, and active-low `dp`.
- Segment mapping: `seg[0] = CA`, `seg[1] = CB`, ..., `seg[6] = CG`.

## Implementation Guidance

Keep the design direct and maintainable:

- Use explicit module ports that match the board-level devices.
- Separate reusable display decode logic, such as hex-to-seven-segment, from experiment logic.
- Avoid speculative abstractions; only add helpers when they remove real duplication in the current lab.
- Validate necessary boundaries, such as counter rollover, display digit selection, ALU opcode coverage, or state-machine transitions.
- Do not over-validate inputs that are already physically constrained by the board.

For clocked logic from the 100 MHz clock, derive slow enables with counters instead of creating new fabric clocks unless the lab explicitly requires a divided clock output.

## Simulation Expectations

Make the testbench prove the requirement before board binding:

- Cover representative normal cases and the smallest meaningful edge cases.
- Prefer self-checking assertions or failure counters over purely visual wave inspection.
- For sequential circuits, test reset/initial state when the design has one, state transitions, and rollover behavior.
- For display circuits, test decode output and at least one scan state; do not rely on a full human-speed scan in simulation.

Common commands depend on the local toolchain. Use existing repo scripts first. If none exist, check for `iverilog`, `xvlog`, `xsim`, or Vivado batch flows and document any missing tool instead of pretending simulation passed.

## Constraints and Bitstream

Use `assets/templates/lab/constraints/hcs_a02_full.xdc` as the complete starting point for HCS-A02 ports. Remove unused constraints only if the Vivado project requires it, and keep names consistent with the top module:

- `clk100mhz`
- `sw[35:0]`
- `bt[7:0]`
- `ld[35:0]`
- `traffic_we_r`, `traffic_we_y`, `traffic_we_g`
- `traffic_sn_r`, `traffic_sn_y`, `traffic_sn_g`
- `an[7:0]`, `seg[6:0]`, `dp`

Do not generate a bitstream until simulation has passed.
