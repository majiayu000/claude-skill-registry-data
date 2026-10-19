---
name: mcu-portability-audit
description: Audit AVR dependencies and classify build, API, pin, ABI, timing, and electrical blockers for a proposed MCU target.
---

# MCU Portability Audit

## Use when

Adding or evaluating a PlatformIO board, MCU family, Arduino core, or platform abstraction.

## Procedure

1. Identify the exact MCU board ID, platform/core version, FC hardware revision, and selected features. If missing, classify conclusions as board-independent or unresolved.
2. Search for AVR headers/registers/ISRs/timers, `PROGMEM`, watchdog, EEPROM, direct port access, `SoftwareSerial`, pin constants, ADC/PWM assumptions, and native struct persistence.
3. Run one representative compile per new architecture and capture the first source-level blockers.
4. Classify each item: unconditional compile blocker, selected-feature blocker, target-dependent API, runtime/timing risk, electrical/safety risk, or portable.
5. Add evidence and a proposed discriminator to `docs/platformio-mcu-compatibility.md` and the workbook.

## Constraints

- A PlatformIO board profile proves only that PlatformIO recognizes a board definition.
- Never generalize one development board's pinout, voltage tolerance, ADC, PWM, UART, EEPROM, or interrupt mapping to an MCU family.
- Do not mark a family supported from config parsing or compilation alone.
- Do not invent pin numbers or hardware specifications.

## Done when

Every claim has a source/build/specification reference and its evidence level is clear. Unsupported families remain explicitly unsupported.