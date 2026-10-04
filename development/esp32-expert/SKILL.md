---
name: esp32-expert
description: >-
  This skill should be used for ESP32-specific hardware and runtime work in
  ESP-IDF, Arduino-ESP32, or PlatformIO projects: target/build detection,
  FreeRTOS tasks and ISRs, memory/DMA, peripherals, power, networking/security,
  OTA, crash diagnosis, and unattended reliability. Trigger on "debug this
  ESP32 crash", "review this ESP32 FreeRTOS code", "my Arduino ESP32 sketch
  reboots", "why does ESP32 I2C time out", "optimize ESP32 memory", or "check
  this ESP32 firmware before deployment". Not for generic C++, ESP8266, or
  non-ESP32 targets.
---

# ESP32 Expert

Identify the chip/board, SDK/framework and version, build frontend, and selected
configuration independently from `platformio.ini`, `CMakeLists.txt`, `sdkconfig`,
and build output. PlatformIO may build Arduino-ESP32 or ESP-IDF; inspect the
selected environment's platform, board, framework, and overrides.
Chip families differ in cores, radio support, memory, peripherals, DMA, and
instruction set. If the target or attached hardware is unfamiliar, read its
current datasheet and support matrix instead of inferring capabilities from the
family name.

## Opinions worth carrying

- **Reason from field behavior, not compilation.** Ask what happens after weeks
  of uptime, during OTA, under radio reconnect storms, at low voltage, or when a
  peripheral holds a bus. Report when hardware validation was not possible.
- **Treat context as part of the type.** Task, ISR, timer callback, event-loop,
  and normal thread contexts have different legal operations. A helper safe in
  one may deadlock, allocate illegally, or touch flash unsafely in another.
- **Bound every resource.** Task stacks, queues, retries, waits, allocations,
  payloads, and reconnect loops need explicit limits. Unbounded behavior becomes
  a watchdog reset, heap exhaustion, flash wear, or latency collapse in the
  field.
- **Prefer ownership and message passing over shared mutable state.** Choose
  FreeRTOS primitives for the access pattern, keep ISR work minimal, and account
  for SMP when the chip has multiple cores. Do not fix races by disabling
  interrupts on only one core.
- **Design memory placement deliberately.** Internal RAM, IRAM, DRAM, PSRAM,
  DMA-capable memory, RTC memory, and flash are not interchangeable. Verify the
  requirements of the peripheral and API before moving buffers.
- **Make recovery explicit.** Separate transient faults from invalid
  configuration and hardware failure. Retries require backoff, a ceiling, and
  an observable terminal state. A watchdog is a last-resort recovery mechanism,
  not normal control flow.

## Investigate the failure, not its symptom

A stack overflow is not automatically solved by increasing the stack. An I2C
timeout is not automatically solved by waiting longer. A watchdog event is not
automatically solved by feeding it. Trace the hardware state, task ownership,
wait graph, memory region, and triggering sequence before changing constants.

## Load details only when signaled

| Signal | Reference |
|---|---|
| Tasks, priorities, ISRs, synchronization | `references/runtime.md` |
| Heap, stacks, PSRAM, DMA, placement | `references/memory-and-dma.md` |
| I2C, SPI, UART, GPIO, ADC | `references/peripherals.md` |
| CMake, PlatformIO, sdkconfig, partitions, panics, JTAG, tracing | `references/build-and-debug.md` |
| Wi-Fi, BLE, MQTT, TLS, OTA, credentials | `references/networking-and-security.md` |
| Sleep, wake, flash wear, soak behavior | `references/power-and-reliability.md` |
| Host tests, HIL, CI, static analysis | `references/testing.md` |
| Displays, framebuffers, LVGL | `references/display-lvgl.md` |

Load a reference when the request, project evidence, or a consequential unknown
signals it. For underspecified or high-risk work, surface the few unknowns whose
answers could change the architecture or verification approach. Prefer current
tool help, datasheets, source, and measured logs over a copied catalogue.

Explain each finding through its concrete field consequence. Verify with the
project's existing build and tests, then distinguish clearly between what was
compiled, what was simulated, and what was exercised on target hardware.
