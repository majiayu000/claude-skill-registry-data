---
name: zephyr
description: "Architect modular embedded systems using Zephyr RTOS, devicetree hardware descriptions, and Kconfig options."
type: procedural
category: embedded
domain: embedded
version: 1.0.0
author: "All-Skills Canonical Engineering Team"
license: "MIT"
risk: low
level: intermediate
triggers:
  - "zephyr rtos devicetree"
  - "zephyr kconfig firmware"
keywords:
  - "zephyr"
  - "rtos"
  - "devicetree"
  - "kconfig"
provenance:
  source_repository: "all-skills/canonical"
  source_commit: "HEAD"
  source_path: "skills/embedded/zephyr"
  imported_at: "2026-09-22T05:32:00.564096+00:00"
  license: "MIT"
  trust:
    level: trusted
    security_scan: passed
    behavioral_eval: passed
---

# Zephyr RTOS Enterprise Firmware

## Purpose

Architect modular embedded systems using Zephyr RTOS, devicetree hardware descriptions, and Kconfig options.

This canonical skill provides deterministic, production-grade operational directives for AI agents executing autonomous engineering and verification tasks within the `embedded` domain.

## When to Use

- When designing, developing, optimizing, or debugging within `embedded` tasks.
- When an autonomous agent requires deterministic execution patterns for `zephyr`.
- When verifying compliance, architecture, or performance standards in this domain.

## When NOT to Use

- When operating outside the scope of `embedded` engineering.
- When a more specialized sub-skill or external toolchain is explicitly requested by the user.

## Capabilities

- Structural design and implementation for Zephyr RTOS Enterprise Firmware.
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

- Standard operational execution pattern for `zephyr`:
  ```bash
  # Verify environment readiness and execute task workflow
  allskills route "zephyr"
  ```

## Safety

- Maintain strict workspace boundary sandboxing.
- Prevent unvetted credential exposure and destructive disk operations.
- Ensure all modifications are verified before concluding execution.

## Source

All-Skills Canonical Engineering Framework.

## Notes

- Pairs with relevant testing, linting, and architecture verification skills across the platform.
