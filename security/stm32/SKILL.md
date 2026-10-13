---
name: stm32
description: "Architect bare-metal and HAL-driven STM32 firmware with direct register manipulation, DMA, and NVIC controllers."
type: procedural
category: embedded
domain: embedded
version: 1.0.0
author: "All-Skills Canonical Engineering Team"
license: "MIT"
risk: low
level: intermediate
triggers:
  - "stm32 arm cortex firmware"
  - "stm32 hal dma interrupt"
keywords:
  - "stm32"
  - "arm"
  - "cortex-m"
  - "hal"
provenance:
  source_repository: "all-skills/canonical"
  source_commit: "HEAD"
  source_path: "skills/embedded/stm32"
  imported_at: "2026-09-22T05:32:00.563103+00:00"
  license: "MIT"
  trust:
    level: trusted
    security_scan: passed
    behavioral_eval: passed
---

# STM32 ARM Cortex-M Firmware Engineering

## Purpose

Architect bare-metal and HAL-driven STM32 firmware with direct register manipulation, DMA, and NVIC controllers.

This canonical skill provides deterministic, production-grade operational directives for AI agents executing autonomous engineering and verification tasks within the `embedded` domain.

## When to Use

- When designing, developing, optimizing, or debugging within `embedded` tasks.
- When an autonomous agent requires deterministic execution patterns for `stm32`.
- When verifying compliance, architecture, or performance standards in this domain.

## When NOT to Use

- When operating outside the scope of `embedded` engineering.
- When a more specialized sub-skill or external toolchain is explicitly requested by the user.

## Capabilities

- Structural design and implementation for STM32 ARM Cortex-M Firmware Engineering.
- Automated verification, schema compliance, and diagnostic troubleshooting.
- Performance profiling, security posture hardening, and error recovery.

## Inputs

- Project source files, configuration manifests, or task instructions.
- Target runtime environment parameters and toolchain dependencies.

## Workflow

1. **Pre-flight Assessment**: Inspect existing configuration and environment preconditions.
2. **Implementation & Transformation**: Apply focused, AST-aware structural modifications.
3. **Verification & Audit**: Execute domain-specific test suites, syntax checks, or simulation passes.
4. **Resolution**: Resolve any detected regressions or failure modes prior to completion.

## Tools

- Project-approved terminal tools, file editors, and verification test harnesses.

## Examples

- Standard operational execution pattern for `stm32`:
  ```bash
  # Verify environment readiness and execute task workflow
  allskills route "stm32"
  ```

## Safety

- Maintain strict workspace boundary sandboxing.
- Prevent unvetted credential exposure and destructive disk operations.
- Ensure all modifications are verified before concluding execution.

## Source

All-Skills Canonical Engineering Framework.

## Notes

- Pairs with relevant testing, linting, and architecture verification skills across the platform.
