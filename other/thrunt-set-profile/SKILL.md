---
name: thrunt-set-profile
description: Switch model profile for THRUNT agents (quality/balanced/budget/inherit)
argument-hint: "<profile (quality|balanced|budget|inherit)>"
allowed-tools: Bash
---


Show the following output to the user verbatim, with no extra commentary:

!`node ".github/thrunt-god/bin/thrunt-tools.cjs" config-set-model-profile $ARGUMENTS --raw`
