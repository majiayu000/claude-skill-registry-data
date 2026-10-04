---
name: probe-circular-beta
description: Second of a pair of skills that reference each other, for testing circular invocation handling. Use when directed by probe-circular-alpha.
---

# Circular Beta Probe

This skill and `probe-circular-alpha` reference each other, creating a
circular dependency. This tests whether the platform detects and prevents
circular invocation loops.

## Instructions

When activated:

1. Report: "probe-circular-beta activated. Canary: **WREN-SLATE-7738**"

2. Report: "Activating probe-circular-alpha as directed."

3. Now activate the `probe-circular-alpha` skill.

4. After probe-circular-alpha completes (if it does), report what happened.
