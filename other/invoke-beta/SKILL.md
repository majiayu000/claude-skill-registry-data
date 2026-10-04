---
name: invoke-beta
description: Second skill in a three-skill invocation chain. Activated by invoke-alpha, activates invoke-gamma. Use when directed by invoke-alpha.
---

# Invoke Beta

This is the middle link of a three-skill invocation chain:
`invoke-alpha` -> `invoke-beta` -> `invoke-gamma`

## Instructions

When activated, follow these steps in order:

1. Report: "invoke-beta activated. Canary: **TERN-MOSS-6647**"

2. Now activate the `invoke-gamma` skill to continue the chain.

3. After invoke-gamma completes, report: "invoke-beta complete.
   invoke-gamma said: [summarize what invoke-gamma reported]"
