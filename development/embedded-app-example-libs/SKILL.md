---
name: embedded-app-example-libs
description: Use when studying, adapting, porting, or debugging embedded application example projects such as ESP32-IoT-Platform, HomeAutomation, CanBus-Triple, or TinyGameEngine
---

# Embedded App Example Libs

## Overview

Use this skill for application-level example projects and demo frameworks. Treat them as reference implementations to extract patterns from, not as drop-in libraries, unless the target platform and product requirements match closely.

## When To Use

Use this skill when:

- The user wants to adapt ESP32-IoT-Platform, HomeAutomation, CanBus-Triple, TinyGameEngine, or a similar example project.
- The task involves extracting architecture, drivers, protocols, UI/game loops, CAN logic, automation flows, or platform services from a demo.
- The user wants to port an example to a different board, RTOS, SDK, or product.

Do not use this skill for small standalone libraries with clear APIs. Use the relevant integration skill instead.

## First Questions

Ask for:

- Example project name, source, and target board.
- What should be reused: architecture, driver, protocol, UI, game engine, automation flow, or build system.
- Current target platform and differences from the example.
- Dependencies: SDK, RTOS, network, display, storage, CAN, sensors, or cloud.
- Whether this is learning, prototype, or production work.

## Adaptation Checklist

1. Identify reusable layer.
   Separate product idea, app logic, drivers, middleware, and build system.

1. Compare platform assumptions.
   SDK version, pin mapping, memory, RTOS, filesystem, network, and peripherals must match or be adapted.

1. Avoid wholesale copy.
   Extract the smallest pattern or module that solves the user's problem.

1. Replace secrets and endpoints.
   Remove demo credentials, hardcoded cloud endpoints, keys, and private IDs.

1. Verify one scenario.
   Run a minimal app flow on the target before adding features.

## Common Failures

- Copying an entire demo and inheriting unused dependencies.
- Keeping board-specific pin maps or credentials.
- Treating example timing and memory as production-ready.
- Porting cloud or home automation flows without defining security and update policy.
- Adapting game/UI loops without measuring frame time and input latency.

## Verification

Before claiming adaptation works:

- State what was reused and what was intentionally not reused.
- Confirm target board, SDK, dependencies, and pin/config changes.
- Confirm one end-to-end scenario on target or simulator.
- Confirm secrets/private endpoints were not copied.

## Example

User:

```text
想参考一个 ESP32-IoT-Platform 做自己的家居控制。
```

Agent:

1. Asks which parts to reuse: Wi-Fi provisioning, MQTT, device model, UI, or storage.
1. Separates reusable architecture from board-specific code.
1. Checks secrets, OTA/update policy, and one minimal control flow before expanding.
