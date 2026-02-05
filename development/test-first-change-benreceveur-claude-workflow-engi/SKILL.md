---
name: test-first-change
description: Reduce regressions by discovering tests, running them, then editing code
version: 1.0.0
tags: [testing, tdd, quality, regression]
---

# Test-First Change Skill

## Purpose
Ensure code changes don't introduce regressions by forcing test discovery and execution before modifications.

## Process
1. Discover existing tests for target code
2. Run tests to establish baseline
3. Make code changes
4. Re-run tests to verify
5. Log changes to memory

## Scripts
- `run_tests.sh`: Execute test suite with coverage
- `diff_summary.py`: Generate change summary for memory

## Safety
- Never edit code before running tests
- Quarantine flaky tests
- Require 80%+ coverage on changes

*Test-First Change v1.0.0*
