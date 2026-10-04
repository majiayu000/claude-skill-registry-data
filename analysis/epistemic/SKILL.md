---
name: epistemic
description: Multi-framework epistemic analysis — compare, suggest, or pick frameworks
version: 0.1.0
---

# Multi-Framework Epistemic Analysis

Invoke the `epistemic-analyst` agent with the user's input.

Determine the mode from arguments:
- If `--compare` is present: use Compare mode (run all frameworks in parallel)
- If `--pick` is present: use Pick mode (let user choose frameworks)
- Otherwise: use Suggest mode (auto-recommend frameworks, ask user to confirm)

The user's input to analyze: $ARGUMENTS
