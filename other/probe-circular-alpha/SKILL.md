---
name: probe-circular-alpha
description: First of a pair of skills that reference each other, for testing circular invocation handling. Use when asked to probe circular dependencies.
---

# Circular Alpha Probe

This skill and `probe-circular-beta` reference each other, creating a
circular dependency. This tests whether the platform detects and prevents
circular invocation loops.

## Instructions

When activated:

1. Report: "probe-circular-alpha activated. Canary: **KITE-ONYX-2251**"

2. Report: "Activating probe-circular-beta as directed."

3. Now activate the `probe-circular-beta` skill.

4. After probe-circular-beta completes (if it does), report what happened.
