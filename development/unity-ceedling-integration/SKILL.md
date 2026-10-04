---
name: unity-ceedling-integration
description: Use when adding, configuring, or debugging Unity, Ceedling, CMock, or embedded C unit tests, mocks, fixtures, build variants, or CI test runs
---

# Unity Ceedling Integration

## Overview

Use this skill to add embedded C tests with Unity assertions, Ceedling builds, and CMock-generated mocks while keeping hardware code behind clear seams. Good embedded tests isolate logic from registers, clocks, and interrupts without pretending the hardware does not exist.

## When To Use

Use this skill when:

- The user wants unit tests for C firmware, drivers, protocol parsers, state machines, or business logic.
- The issue involves Ceedling project setup, include paths, mocks, fixtures, test runners, coverage, or CI.
- The codebase uses vendor HALs, RTOS wrappers, static functions, compile-time flags, or hardware registers.

Do not use this skill for hardware-in-the-loop validation alone. Pair it with the relevant hardware or protocol skill.

## First Questions

Ask for:

- Toolchain, host OS, Ceedling version, compiler, and CI environment.
- Code under test, dependencies, include paths, and hardware/HAL boundaries.
- Whether mocks, fakes, or real modules should be used.
- Build variants, configuration headers, and preprocessor flags.
- Current failing command and full test output.

## Integration Checklist

1. Identify testable units.
   Start with pure logic, parsers, state machines, and error handling before register-level code.

1. Define hardware boundaries.
   Wrap HAL calls, RTOS calls, time, logging, and storage behind interfaces that can be mocked or faked.

1. Configure Ceedling deliberately.
   Set source paths, include paths, defines, vendor files, and plugins in `project.yml`.

1. Write tests around behavior.
   Prefer input/output and state transitions over checking private implementation details.

1. Use CMock where it clarifies intent.
   Mock external collaborators, but use small fakes for stateful dependencies when expectations become brittle.

1. Add CI and coverage last.
   Keep the command non-interactive and fast enough to run on every change.

## Common Failures

- Tests include vendor headers that require target-only compiler extensions.
- Static functions are tested directly instead of through behavior.
- Mocks over-specify call order and make refactors painful.
- Configuration macros differ between tests and firmware builds.
- Global state is not reset in `setUp` or `tearDown`.
- CI uses a different Ruby, compiler, or path layout than local runs.

## Verification

Before claiming tests are useful:

- State the Ceedling command and compiler used.
- Confirm at least one passing test for normal behavior and one edge/error case.
- Confirm mocks or fakes match the intended hardware boundary.
- Confirm CI can run the same command non-interactively.

## Example

User:

```text
想给驱动状态机加 Ceedling 测试。
```

Agent:

1. Separates register access from state transition logic.
1. Adds Unity tests for events, retries, timeout, and invalid transitions.
1. Uses CMock only for external HAL/time dependencies.
