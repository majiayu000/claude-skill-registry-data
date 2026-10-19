---
name: firmware-safety-review
description: Review changes affecting throttle, brake, PAS, speed, power stage, reset, watchdog, ADC, PWM, interrupts, or persistence.
---

# Firmware Safety Review

## Use when

A change may affect actuation, sensor interpretation, limits, reset/shutdown, timing, or persistent state.

## Procedure

1. Read the relevant findings and gates in `docs/mcu-port-project-workbook.md`.
2. Trace the complete path from input and configuration through state transitions to the physical-output API/register.
3. Enumerate startup, normal, invalid-input, missing-sensor, timeout, brownout, watchdog, shutdown, and recovery states as applicable.
4. Separate source-confirmed behavior, inferred risk, software test evidence, and hardware evidence.
5. Add or update targeted host checks where they can test a deterministic code contract.
6. State the exact board/configuration and any untested hardware assumptions.

## Constraints

- Do not infer that raw zero or `motor_offset` is torque-free without controller electrical specifications and measurement.
- Do not change FET polarity, startup enable, brake polarity, pin mapping, ADC scaling, PWM frequency, watchdog recovery, or shutdown order based on guesswork.
- Do not power a motor as part of an ordinary coding test. Board tests require isolated/current-limited fixtures, emergency stop, and qualified supervision.
- A successful compile is not a safety case or regulatory approval.

## Done when

The changed paths, failure states, validation evidence, residual risks, and explicit qualification limits are recorded. Unverified hardware behavior remains open.