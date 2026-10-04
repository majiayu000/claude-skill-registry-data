---
name: test-driven-development
description: Use when changing observable code behavior with a runnable automated test loop. Follow red-green-refactor; do not force TDD on configuration, generated files, exploratory spikes, or work without a meaningful test seam.
---

# Test-Driven Development

Use a meaningful red-green-refactor loop to change observable behavior with
confidence. Prefer repository-native tests and behavioral seams over a generic
test framework or mock-heavy implementation detail checks.

Keep test fixtures, logs, screenshots, and failure output free of secrets,
credentials, tokens, and unnecessary personal or confidential data. Redact
sensitive values in evidence rather than copying them into tests or reports.

## When TDD applies

Use TDD for new or changed behavior when the repository has a runnable test
loop and an observable seam. First inspect repository instructions, existing
tests, test commands, fixtures, and conventions.

Do not force a failing-test-first loop for:

- Documentation-only or comment-only changes.
- Configuration-only changes whose meaningful proof is parsing, schema checking,
  or a safe preview.
- Generated files where the source and generator are the test seam.
- Time-boxed exploratory spikes that will not become production behavior.
- Work with no runnable or meaningful automated test loop.

State the exception, why TDD is unsuitable, and the alternative verification
plan. Do not use an exception to skip available behavioral coverage.

## Red-green-refactor workflow

### 1. Find the smallest behavior seam

Describe the requested observable behavior, caller, inputs, outputs, errors,
and edge cases. Select the narrowest existing test level that can prove it:
unit, module, integration, contract, or end-to-end.

Use real collaborators when practical. Mock only a boundary that is expensive,
non-deterministic, externally owned, or unsafe to exercise; verify the mock
does not replace the behavior under test.

### 2. Red: add one focused failing test

With normal edit approval, add a test that expresses one behavior. Run the
narrowest test command and confirm it fails for the expected missing or
incorrect behavior—not because of setup, syntax, unrelated failures, or an
invalid assertion.

If the test unexpectedly passes, strengthen the assertion or reassess the
behavior before changing production code. Do not write the implementation first
and retrofit a passing test.

### 3. Green: make the smallest valid change

With normal edit approval, implement only enough behavior to make the focused
test pass. Avoid opportunistic abstractions, refactors, or unrelated cleanup.
Run the same targeted test again and inspect the result.

### 4. Refactor: improve without changing behavior

After green, remove duplication and improve names, structure, or interfaces
only when the passing test remains meaningful. Re-run the targeted test after
each material refactor. Keep production and test code understandable at the
public behavior seam.

### 5. Complete with evidence

Cover adjacent edge cases, error paths, and integration boundaries only where
the risk justifies them. Use `verification-before-completion` for fresh targeted
and broader checks, final diff review, and explicit untested-path reporting
when that companion skill is available; otherwise apply the same checks
directly.

Do not run tests, builds, browser tooling, installs, or external services
without repository-policy approval. If a check is unavailable or blocked, report
the limitation rather than claiming the behavior is verified.

## TDD record

```markdown
## Behavior and Test Seam

## Red Evidence

## Green Evidence

## Refactor Evidence

## Exception and Alternative Verification

## Remaining Risks and Required Approval
```

Mark a behavior verified only when the chosen test demonstrated its intended
failure and then passes after the final relevant implementation change.
