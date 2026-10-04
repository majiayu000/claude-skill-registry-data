---
name: embedded-framework-libs
description: Use when integrating, evaluating, configuring, or debugging embedded C framework libraries such as PLOOC, Avem, or PowerManagement
---

# Embedded Framework Libs

## Overview

Use this skill for framework-style embedded libraries that shape project architecture rather than one feature. Cover PLOOC, Avem, PowerManagement, and similar libraries by focusing on ownership, lifecycle, configuration, coupling, and migration risk.

## When To Use

Use this skill when:

- The user wants to add or evaluate PLOOC, Avem, PowerManagement, or a similar embedded framework.
- The task involves object-oriented C patterns, module architecture, power-management framework integration, lifecycle hooks, or broad project restructuring.
- The user is unsure whether a framework is appropriate for a small MCU project.

Do not use this skill for small single-purpose utility libraries that can be integrated locally without architecture impact.

## First Questions

Ask for:

- Library/framework name and source.
- Existing project architecture and target MCU/RTOS.
- Problem the framework is meant to solve.
- Code size, RAM, timing, safety, and team familiarity constraints.
- Whether this is greenfield, migration, or partial adoption.

## Integration Checklist

1. Validate need.
   Confirm the framework solves a real recurring problem and is not added for style alone.

1. Define boundary.
   Decide which modules use the framework and which remain plain C.

1. Check lifecycle.
   Init, start, stop, suspend, resume, and deinit order must be explicit.

1. Keep platform hooks isolated.
   Hardware, RTOS, allocator, timebase, and logging hooks should not leak across application modules.

1. Migrate incrementally.
   Wrap one small module first and verify behavior before broad adoption.

## Common Failures

- Applying an OOP-in-C framework to every file and increasing complexity.
- Hidden dynamic allocation in a no-heap project.
- Power-management hooks conflict with drivers or RTOS idle.
- Initialization order becomes implicit and fragile.
- Framework abstractions hide timing-critical hardware operations.

## Verification

Before claiming framework integration works:

- State the specific problem solved and the modules in scope.
- Confirm init/lifecycle order and platform hooks.
- Confirm code size/RAM impact if relevant.
- Confirm one migrated module works and rollback is possible.

## Example

User:

```text
想在老项目里引入 PLOOC 整理模块。
```

Agent:

1. Asks what module complexity PLOOC should solve and which modules are in scope.
1. Recommends one pilot module instead of whole-project migration.
1. Verifies code size, init order, and whether the abstraction improves testing/debugging.
