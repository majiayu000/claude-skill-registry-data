---
name: code-design-guard
description: Pre-implementation design guard for non-trivial code changes. Use before feature work, bug fixes, refactors, compatibility changes, error-handling changes, fallback additions, helper extraction, or any code change where Codex should clarify intent, normal flow, required invariants, failure policy, helper boundaries, and fallback justification before editing.
---

# Code Design Guard

Use this skill before making a non-trivial code change. The goal is to prevent cosmetic abstraction, ungrounded defensive defaults, and silent masking of required failures.

Favor root-cause fixes. When a problem can be prevented through normal design, data flow, validation, typing, initialization, or caller behavior, prefer that prevention over patching over the symptom later. Do not use reward hacking, benchmark-specific shortcuts, or checker-shaped workarounds as substitutes for a real fix.

Design against the task contract and supported input classes. Use examples to identify real input classes, structural patterns, edge cases, and acceptance criteria. Avoid logic that depends on incidental traits that only identify the provided sample. Specialized logic is acceptable when it targets an input class that is actually in scope and is triggered by stable structural evidence.

## Workflow

1. State the design intent before editing code.
2. Inspect the actual repository, call paths, configuration, and tests.
3. Revise the design intent based on repository evidence.
4. Implement the change.
5. After implementation, use `code-review` to check structural clarity and failure policy.

Keep the design note short. It is a decision aid, not a separate design document.

## Pre-change design note

Before editing, write a short note covering:

```md
Goal:
- ...

Normal flow:
- ...

Required invariants:
- ...

Failure policy:
- Safe to continue:
- Must stop or report:

Helper and fallback plan:
- New helpers and why they help:
- New fallbacks and the evidence for them:
- Required values that must not be hidden by defaults:

Verification:
- ...
```

## Goal and success condition

Clarify what the change must accomplish.

- Identify the user-visible or caller-visible result.
- Identify the smallest verifiable completion signal: test, build, smoke run, output file, API response, UI behavior, or diff shape.
- Keep acceptance criteria tied to the user's request and repository evidence.

## Normal flow first

Identify the expected path before designing defensive branches.

- Name the common input and the intended execution path.
- Keep the normal path readable near the call site.
- Keep compatibility branches, guards, optional paths, and exception handling from dominating the main logic.
- If the normal path is only understandable by opening several helpers, reconsider the structure.

## Required invariants and failure policy

Separate values that may be absent from values that must exist.

Safe-to-continue failures often include:

- missing cache entries;
- optional feature failures;
- best-effort logging, analytics, or telemetry failures;
- external service failures where degraded behavior is an explicit product decision.
- values that may exist only in some supported environments, as long as the core operation is still safe without them.

Must-stop or must-report failures often include:

- missing required configuration;
- missing required data;
- failed security validation;
- broken authentication, authorization, billing, deletion, or move preconditions;
- environment-dependent values that are required for the core logic in this task;
- conditions that can corrupt output, persist wrong data, or make later debugging misleading.

Do not hide must-stop failures with empty strings, empty arrays, `null`, `false`, or weak defaults.

## Fallback criteria

Use fallback logic for grounded compatibility, legacy data, optional features, external dependency failure, or explicit user requirements.

A fallback is well-grounded when at least one of these is true:

- the user requested the fallback behavior;
- existing tests require it;
- real legacy data or existing persisted shape exists;
- runtime, operating-system, browser, library, API, or tool-version differences were confirmed;
- an optional feature can fail while the core operation remains safe;
- degraded behavior after an external-service failure matches product intent.

When adding fallback logic, verify:

- the first candidate is the normal path;
- later candidates have evidence or a clear compatibility reason;
- required values are not being hidden by defaults;
- the fallback can be tested, observed, or explained from repository evidence.

Avoid hiding fallback chains inside vague helpers:

```js
const value = resolveValue(a, b, c, d);
```

If `resolveValue` only contains a chain like this, it is wrapping patchwork:

```js
return a ?? b ?? c ?? d;
```

Prefer reducing candidates and making required-value failure visible:

```js
const value = explicitValue ?? configValue;

if (value == null) {
  throw new Error("Missing required value: ...");
}
```

If a constant or type-guaranteed value cannot be null by declaration, do not add a defensive null check for it:

```js
const value = explicitValue ?? DEFAULT_VALUE;
```

If a supposedly guaranteed value can break, treat that as an initialization, typing, or configuration-loading problem. Do not cover it with a fallback unless repository evidence shows a real compatibility need.

When a fallback has three or more candidates, pause and check:

- whether every candidate has evidence;
- whether priority follows a requirement or existing behavior;
- whether some candidates should be removed;
- whether a required value is being treated as optional;
- whether the priority can stay visible near the use site instead of being hidden in a vague helper.

After this review, keeping three or more fallback candidates is acceptable when that remains the most accurate behavior. Keep the evidence and priority order visible near the code that uses the value.

## Helper criteria

Create helpers when they improve comprehension, isolate change, or make behavior easier to verify.

Helpers are useful when they:

- remove meaningful repetition that is complex enough to be worth centralizing;
- name a domain concept;
- isolate file, network, process, environment-variable, time, external API, or similar boundary logic;
- separate a long condition or algorithm step from the main flow;
- match an existing repository pattern;
- create a valuable unit for focused tests.
- centralize a likely future extension point when that extension is credible and keeping the logic in one place clearly reduces future maintenance cost.

Use a leading underscore for new internal-only helpers.

Treat a helper as suspicious when it:

- wraps a one-off simple expression;
- extracts repeated logic that is still simple enough to read inline;
- hides a fallback chain;
- has a vague name such as `resolveValue`, `getData`, `handleThing`, `processInput`, or `normalizeInput`;
- forces readers to open the helper to understand the main flow;
- exists for hypothetical future flexibility without a credible extension path or clear maintenance benefit;
- exists only because the extracted code looked tidier as a separate function.

Do not delete suspicious helpers automatically. First identify their role. Keep helpers with clear value. Inline or rename helpers whose role remains unclear after reading the call site and implementation.

## Implementation guardrails

- Prefer preventing the problem at the source over compensating for it later.
- Keep the implementation grounded in the input class in scope and away from sample identity traits.
- Prefer explicit required-value failures over broad defaults.
- Prefer repository evidence over speculative compatibility branches.
- Prefer a visible priority order over a vague resolver helper.
- Preserve necessary fallbacks when tests, legacy data, or compatibility evidence supports them.
- Keep simple repeated logic inline when extraction would add unnecessary indirection.
- Prefix new internal-only helpers with `_`.
- Avoid broad `catch` blocks that convert serious failures into defaults.
- Keep comments focused on why a branch exists when the code cannot make that reason obvious.
