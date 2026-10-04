---
name: avem-integration
description: Use when integrating, evaluating, configuring, or debugging Avem embedded C framework modules, event-driven components, drivers, middleware, or application architecture
---

# Avem Integration

## Overview

Use this skill when the user explicitly works with an embedded framework or library named Avem. Because public references can be sparse or project-specific, first confirm the exact repository and then treat Avem as an architecture-level dependency with explicit platform hooks and module boundaries.

## When To Use

Use this skill when:

- The user mentions Avem in an MCU, embedded C, firmware framework, middleware, or application architecture context.
- The task involves adapting Avem modules, drivers, event loops, services, or platform hooks.
- The user wants to evaluate whether Avem fits a project.

Do not use this skill when "Avem" refers to an unrelated product, service, or non-embedded codebase.

## First Questions

Ask for:

- Exact Avem repository/source and version.
- Target MCU/SoC, RTOS/bare-metal runtime, compiler, and build system.
- Which Avem modules are needed.
- Required platform hooks: timebase, allocator, logging, storage, drivers, event loop, or RTOS primitives.
- Current goal: evaluation, first port, compile fix, runtime bug, or migration.

## Integration Checklist

1. Confirm identity and scope.
   Read the project's own docs/source layout before assuming Avem behavior.

1. Identify platform hooks.
   Time, memory, logging, synchronization, drivers, and initialization order must be mapped to the target.

1. Start with one module.
   Bring up the smallest useful Avem module before importing the full framework.

1. Keep boundaries explicit.
   Application code should not depend on hidden globals or framework internals unnecessarily.

1. Verify resource impact.
   Measure flash, RAM, stack, heap, and scheduler impact if Avem becomes a core dependency.

## Common Failures

- Assuming Avem's API from another framework with a similar pattern.
- Importing the entire framework before one module works.
- Platform hooks silently use unavailable malloc, file I/O, or RTOS functions.
- Initialization order depends on undocumented global state.
- Framework callbacks block timing-sensitive driver paths.

## Verification

Before claiming Avem integration works:

- State the exact Avem source and modules used.
- Confirm platform hooks and initialization order.
- Confirm one minimal module works on target.
- Confirm resource impact or state that it has not been measured.
- List assumptions that came from source inspection rather than public docs.

## Example

User:

```text
我想把 Avem 接到一个裸机项目里。
```

Agent:

1. Asks for the exact Avem repository and target platform.
1. Identifies required hooks and chooses one minimal module.
1. Verifies init, runtime behavior, and resource impact before broader migration.
