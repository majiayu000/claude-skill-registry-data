---
name: hardware-interface-debug
description: Use when debugging embedded board-level power, reset, clock, pin, connector, signal integrity, logic analyzer, oscilloscope, or hardware interface issues
---

# Hardware Interface Debug

## Overview

Use this skill when firmware symptoms may actually come from board-level signals. Verify power, reset, clocks, pin mapping, voltage levels, and measured waveforms before treating the issue as a software bug.

## When To Use

Use this skill when:

- The issue involves power rails, reset, crystals, boot pins, connectors, level shifters, pull-ups, or signal integrity.
- A peripheral or debug interface has no signal, wrong voltage, ringing, stuck line, or intermittent behavior.
- The user has a schematic, board photo, oscilloscope capture, logic analyzer trace, or pinout question.

Do not use this skill when the hardware path has already been verified and the issue is clearly inside firmware logic.

## First Questions

Ask for:

- Board/chip, revision, and affected interface.
- Schematic snippet or pin mapping if available.
- Expected signal and observed measurement.
- Measurement tool: multimeter, oscilloscope, logic analyzer, current probe.
- Power source and voltage levels.
- Whether the issue is reproducible across boards.

## Workflow

1. Start with power and ground.
   Confirm rail voltage, sequencing, ripple, current limit, ground reference, and target voltage for debug probes.

1. Check reset and clock.
   Verify reset release, boot strap states, oscillator startup, clock output, and brownout/watchdog conditions.

1. Trace the signal path.
   Map MCU pin, package pin, board net, connector, level shifter, external device, and pull components.

1. Measure at the right points.
   Compare near-MCU and near-peripheral signals to catch level shifter, connector, or routing issues.

1. Compare against firmware configuration.
   Pin mux, open-drain/push-pull, drive strength, alternate function, and analog mode must match the hardware.

1. Avoid destructive experiments.
   Do not short pins, force rails, remove protections, or bypass regulators without explicit user approval.

## Signal Checks

- Voltage level matches both devices.
- Ground reference is shared.
- Pull-up/down values are appropriate.
- Rise/fall time fits bus speed.
- No two outputs fight on the same net.
- Boot strap resistors match intended mode.
- Debug pins are not overloaded by external circuits.
- Reset pulse width and polarity match datasheet.

## Measurement Guidance

- Use a multimeter for static rails and reset state.
- Use an oscilloscope for clocks, reset edges, ripple, ringing, and analog behavior.
- Use a logic analyzer for decoded UART/SPI/I2C timing.
- Use current-limited bench supply for bring-up when safe.
- Capture before and after reset or transaction start when timing matters.

## Verification

Before claiming hardware evidence:

- State measurement location, tool, voltage/time scale when relevant, and observed value.
- Map the measured net to MCU pin and external device pin.
- State whether the measurement supports or contradicts the firmware assumption.
- List unsafe hardware actions avoided or awaiting approval.

## Common Failures

- Measuring only at the connector and not at the MCU pin.
- Forgetting common ground for UART/debug adapters.
- Treating an open-drain bus as push-pull.
- Ignoring boot strap resistors or reset timing.
- Debugging firmware while the rail is current-limited or brownout-resetting.

## Example

User:

```text
SPI 读出来全是 0xFF，代码看起来没问题。
```

Agent:

1. Asks for schematic, pins, voltage, SPI mode, and logic analyzer capture.
1. Checks CS/SCK/MOSI/MISO near both MCU and slave.
1. Verifies MISO is not floating, voltage levels match, and CS timing reaches the device.
