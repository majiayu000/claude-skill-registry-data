---
name: regression-check
description: Use to identify likely regression areas after a PonyBunny change, especially around contracts, transitions, traces, retries, and observability.
---

# Regression Check

## Use this skill when
- reviewing a change before merge
- evaluating a refactor
- modifying runtime-critical code
- changing schemas, statuses, or behaviour

## Goals
- expose hidden breakage risk
- protect existing behaviour
- define follow-up checks clearly

## Regression areas to inspect
- public contracts
- cross-module contracts
- state transitions
- event ordering
- retry behaviour
- resume behaviour
- trace completeness
- audit/logging
- tool or MCP payloads

## Output contract
Return:
- likely regression areas
- why each is at risk
- recommended checks
- confidence level
