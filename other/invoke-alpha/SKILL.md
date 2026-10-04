---
name: invoke-alpha
description: First skill in a three-skill invocation chain for testing cross-skill invocation, depth limits, and language sensitivity. Use when asked to start an invocation chain.
---

# Invoke Alpha

This is the entry point of a three-skill invocation chain:
`invoke-alpha` -> `invoke-beta` -> `invoke-gamma`

## Instructions

When activated, follow these steps in order:

1. Report: "invoke-alpha activated. Canary: **IBIS-RUST-3310**"

2. Now activate the `invoke-beta` skill to continue the chain.

3. After invoke-beta completes, report: "invoke-alpha complete.
   Chain result: [summarize what invoke-beta and invoke-gamma reported]"
