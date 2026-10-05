---
name: eval-case-generation
description: Use to generate high-signal evaluation cases for PonyBunny changes, including success paths, failure modes, edge cases, and regression-sensitive behaviours.
---

# Eval Case Generation

## Use this skill when
- adding a feature
- changing runtime behaviour
- fixing a bug that could recur
- validating a migration phase

## Goals
- generate useful eval cases
- cover both success and failure
- protect likely regression areas
- make verification concrete

## Case categories
- normal success path
- invalid input
- missing dependency
- contract mismatch
- retry path
- partial failure
- resume after interruption
- traceability check
- audit/logging check
- state transition integrity check

## Output contract
For each eval case return:
- case name
- scenario
- setup/input
- expected behaviour
- expected evidence
- regression risk it protects against
