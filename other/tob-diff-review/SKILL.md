---
name: tob-diff-review
description: Performs security-focused differential review of code changes
user-invocable: true
argument-hint: "<pr-url|commit-sha|diff-path> [--baseline <ref>]"
---

# Differential Security Review

**Arguments:** $ARGUMENTS

Parse arguments:
1. **Target** (required): PR URL, commit SHA, or diff path
2. **Baseline** (optional): `--baseline <ref>` for comparison reference

Invoke the `differential-review` skill with these arguments for the full workflow.
