---
name: edge-case-test-planner
description: Identifies edge-case test scenarios for features, APIs, components, and workflows. Use when the user asks to plan tests for unusual states, malformed inputs, boundary values, race conditions, lifecycle problems, retries, rollbacks, recovery paths, or failure handling before or during implementation.
license: MIT
compatibility: Portable Agent Skill. Can be copied into an Agent Skills-compatible environment with repository file access unless stated otherwise.
metadata:
  category: project-planning
  task_type: planner
  audience: software-engineers
  tags:
    - testing
    - edge-cases
    - failure-states
    - race-conditions
    - recovery
    - quality-assurance
  status: draft
  side_effects: none
---

# Edge Case Test Planner

## Purpose

Plan targeted edge-case tests for a feature, API, component, workflow, or system change before test implementation begins, focusing on unusual states, malformed inputs, timing hazards, lifecycle transitions, and recovery behavior.

## When to use this skill

Use this skill when:

- The user asks for edge cases, negative tests, QA scenarios, failure scenarios, or test coverage ideas.
- A feature has user input, external data, asynchronous behavior, state transitions, persistence, retries, or cleanup logic.
- A change could fail under unusual timing, lifecycle, environment, permission, quota, or dependency conditions.
- The user wants a test plan rather than finished test code.

Do not use this skill when:

- The user only wants a generic explanation of testing concepts.
- The user asks to write executable tests immediately and the edge-case plan is already clear.
- A more specific domain skill covers the target, such as accessibility, release readiness, or package publishing.

## Inputs to inspect

Inspect the smallest relevant set of inputs, such as:

- The feature request, bug report, acceptance criteria, or implementation plan.
- Related source files, API handlers, components, state machines, validators, schemas, and service boundaries.
- Existing tests, fixtures, mocks, factories, and test utilities.
- Error handling, retry, timeout, cancellation, cleanup, migration, or rollback code.
- Documentation describing supported inputs, limits, permissions, lifecycle behavior, or external integrations.

## Workflow

1. Define the target behavior, invariants, and success criteria in one or two sentences.
2. Identify the primary happy path only as a reference point, then focus the plan on what can go wrong.
3. Map the system surfaces involved: inputs, outputs, state, persistence, network or service dependencies, user actions, permissions, clocks, queues, caches, and cleanup.
4. Generate edge cases across these categories:
   - Boundary values: empty, minimum, maximum, off-by-one, duplicate, missing, huge, tiny, old, future, and timezone-sensitive values.
   - Malformed or hostile input: wrong type, invalid encoding, unexpected shape, injection-like strings, unsupported enum values, partial objects, and inconsistent combinations.
   - Unusual state: first run, empty state, stale state, corrupted state, migrated state, disabled state, feature-flag mismatch, and partially completed workflows.
   - Lifecycle transitions: mount, unmount, initialization, teardown, navigation away, refresh, resume, session expiry, cancellation, retry, rollback, and cleanup.
   - Timing and concurrency: rapid repeated actions, out-of-order responses, duplicate submissions, race conditions, slow dependencies, timeouts, simultaneous edits, and idempotency.
   - Dependency failure: unavailable network, failed service, partial response, rate limit, permission denial, quota exhaustion, disk or storage failure, and inconsistent third-party data.
   - Recovery scenarios: retry success, retry exhaustion, manual correction, undo, rollback, fallback UI, saved progress, and safe re-entry after interruption.
5. Convert relevant cases into concrete test scenarios with setup, action, expected result, and the risk each test covers.
6. Prioritize scenarios by impact, likelihood, past bugs, complexity, and whether the behavior protects data integrity, security, or user trust.
7. Separate must-test blockers from useful follow-up coverage, and note assumptions or missing product decisions that block precise expectations.
8. Recommend the appropriate test level for each case: unit, integration, component, end-to-end, contract, property-based, load, chaos, or manual exploratory.

## Output format

Return the result using this structure:

```md
## Summary

Briefly describe the target behavior and the main risk themes.

## Edge-case test matrix

| Priority | Scenario | Setup | Action | Expected result | Test level | Risk covered |
|---|---|---|---|---|---|---|

## Must-test blockers

- ...

## Follow-up coverage

- ...

## Open questions

- ...

## Validation checklist

- [ ] Boundary values are covered.
- [ ] Malformed inputs are covered.
- [ ] Unusual states are covered.
- [ ] Lifecycle transitions are covered.
- [ ] Race conditions or timing hazards are covered where relevant.
- [ ] Dependency failures and recovery paths are covered.
- [ ] Each scenario has a concrete expected result.
```

If the user asks for implementation, add a final section named `Suggested test files` with proposed file names and test groupings, but do not write code unless explicitly asked.

## Quality bar

The task is complete only when:

- Each proposed test scenario is specific enough for another agent or engineer to implement.
- Expected results distinguish correct recovery, safe failure, and blocked behavior.
- Race conditions, lifecycle problems, and recovery scenarios are considered when relevant, not treated as optional afterthoughts.
- Priority reflects risk, not just ease of implementation.
- Open questions identify missing product or technical decisions instead of inventing hidden requirements.
- No file changes, commands, or external side effects are performed unless the user separately asks for implementation.

## Edge cases

- If the target behavior is underspecified, produce a provisional matrix and mark assumptions explicitly.
- If the existing system has no tests, recommend the minimum test harness or test level needed before listing extensive scenarios.
- If a scenario would be flaky, restate it in terms of controllable clocks, mocked services, deterministic scheduling, or idempotent assertions.
- If the feature touches user data, authentication, billing, permissions, or destructive actions, prioritize safe failure and recovery tests above cosmetic cases.
- If the user provides only a bug report, include regression tests that reproduce the bug and adjacent cases that could share the same root cause.

## Related skills

- `implementation-checkpoint-planner`
- `requirements-gap-finder`
- `user-recovery-flow-planner`
