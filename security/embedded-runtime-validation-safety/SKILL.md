---
name: embedded-runtime-validation-safety
description: Design bounded, evidence-preserving runtime validation for embedded firmware with read-only defaults, explicit budgets, and no automatic retries. Use after static analysis when live behavior must be checked safely.
---

# Embedded Runtime Validation Safety

Use this skill to turn a static hypothesis into the smallest controlled
runtime observation while protecting embedded devices from lockout, reboot,
configuration loss, or request floods.

## Guardrails

1. Define the exact target, interface, operation, expected evidence, and stop conditions.
2. Default to dry-run and offline self-validation. Preserve originals and write timestamped evidence.
3. Use one request stream, conservative timeouts, explicit pacing, and no automatic retries after send or timeout.
4. Prefer read-only probes. Require exact target checks and typed confirmation immediately before any destructive action.
5. Capture only the target/protocol scope. Record request count, timing, response, reachability, and state transitions.
6. Stop on lockout/rate-limit signals, unexpected state changes, ambiguous authorization, or any privileged result without expected proof.

## Classifications

Use precise outcomes such as `DRY_RUN_NOT_SENT`, `RESPONSE_RECEIVED`,
`NO_RESPONSE`, `REJECTED`, `PROBABLE_STATE_CHANGE`, and `UNKNOWN`. Distinguish
packet transmission from handler acceptance and acceptance from observed
state change. A missing response is never success by itself.

## Evidence handoff

Store metadata, raw request/response, capture hash, timeline, pre/post state,
and a concise result report. Record capture failures explicitly. Do not add
stealth, source rotation, lockout bypass, fuzzing, or target discovery.
