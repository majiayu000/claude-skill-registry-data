---
name: esp32
description: "Applies ESP32 rules for GPIO, boot states, relays, sensors, connectivity, firmware safety, and validation."
---

# Skill: esp32

## Purpose

Apply hardware-aware engineering rules to ESP32-based systems, firmware, GPIO, boot behavior, relays, sensors, and connectivity.

## Safety First

Physical devices fail differently than web apps. They can get hot, lock doors, flood rooms, or annoy the nearest human until civilisation collapses into support tickets.

Do not recommend GPIO pins, wiring, voltage levels, current limits, or power behavior unless verified from:

- the exact board documentation;
- project schematics;
- user-provided hardware details;
- existing repository configuration;
- official component datasheets.

## Inspect First

Before changing ESP32 behavior, inspect:

- exact board/module;
- GPIO usage;
- strapping pins;
- relay/transistor wiring;
- pull-ups/pull-downs;
- boot state;
- power supply assumptions;
- brownout behavior;
- Wi-Fi/BLE usage;
- sleep mode;
- flash write patterns;
- watchdog behavior;
- connected loads.

## GPIO Rules

- Be careful with strapping pins.
- Be careful with boot logs on UART pins.
- Avoid unsafe relay activation during boot.
- Consider default pin state before firmware starts.
- Do not assume pins are safe across ESP32 variants.
- Preserve existing known-good pin assignments unless explicitly changing them.

## Reliability Rules

Consider:

- brownouts;
- watchdog resets;
- Wi-Fi loss;
- reconnect loops;
- offline behavior;
- sensor failures;
- debouncing;
- noisy ADC readings;
- flash wear;
- task starvation;
- memory fragmentation.

## Power and Loads

Do not assume the ESP32 can directly drive loads.

For relays, motors, LEDs, pumps, valves, and high-current devices, verify:

- driver/transistor/relay module behavior;
- flyback protection where needed;
- common ground assumptions;
- current draw;
- isolation;
- safe default state.

If hardware details are missing, state that they are missing.

## Firmware Behavior

- Avoid blocking critical loops.
- Keep ISR work minimal.
- Avoid unbounded dynamic allocation in long-running firmware.
- Use timeouts for external operations.
- Define safe fallback behavior.
- Avoid repeated flash writes.

## Validation

Validation may include:

- compile/build;
- config validation;
- static analysis;
- hardware bench test plan;
- manual safety checklist.

Never claim hardware behavior was verified unless it was actually verified.
## Shared Cross-Ecosystem Style


Apply the shared engineering style from:

- `../../engineering/05_design_principles.md`
- `../../engineering/06_responsibility_model.md`
- `../../engineering/07_complexity_budget.md`
- `../../engineering/12_naming_bible.md`

Language-specific idioms control syntax and ecosystem details, but they must not weaken the core rules: small cohesive units, explicit boundaries, honest validation, no dumping grounds, and no fake placeholders.
