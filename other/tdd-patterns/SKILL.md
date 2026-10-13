---
name: tdd-patterns
description: >
  Use this when running the multi-agent SKELETON→RED→GREEN→REFACTOR TDD cycle,
  designing interface-driven tests against compilable stubs, or coordinating
  mock-based TDD between code-generator and test-spec-generator. Covers the
  three-agent cycle, interface skeletons, failing-test design, impl-to-pass,
  and refactor-with-tests-green discipline.
  Triggers: TDD, RED, GREEN, REFACTOR, skeleton, failing test, interface-driven.
version: 1.1.0
last-evolved-in-run: v0.6.0-rc.0-sanitization
status: stable
tags: [tdd, testing, agent-cycle]
---

# tdd-patterns (v1.1.0)

## Scope

Defines the language-neutral SKELETON→RED→GREEN→REFACTOR cycle and the agent coordination around it. Language-specific syntax (test-runner conventions, mock libraries, sentinel-discrimination idioms) lives in language-pack siblings: `go-tdd-patterns`, `python-tdd-patterns`.

## The cycle in the agent system

The pipeline runs TDD as a four-step cycle per package or feature:

1. **code-generator (SKELETON)** writes compilable stubs — interfaces, struct shapes, constructors that return real instances, method bodies that explicitly signal "not implemented" via the language-native idiom. Tests can import the package and reference its surface.
2. **test-spec-generator (RED)** writes failing tests against the skeleton. Each test asserts at least one observable outcome that the skeleton cannot satisfy. Tests define WHAT the implementation must do — they are the specification.
3. **code-generator (GREEN)** reads ALL test files first, then writes the minimum impl to make them pass. It does not add behavior that isn't tested.
4. **refactoring-agent (REFACTOR)** improves shape without breaking the GREEN state. Tests stay green throughout.

## SKELETON rules (language-neutral)

- All exported interfaces / Protocols / abstract bases fully defined — every method signature with parameter and return types.
- Structs / dataclasses have correct fields and serialization annotations.
- Constructors return real instances (not nil/None).
- Method stubs explicitly signal "not implemented" via the language-native idiom (sentinel error, raised exception, etc. — see language packs).
- Package structure matches the design exactly.

## RED rules (language-neutral)

- **Assertion-first**: start with what you want to verify, work backward to setup.
- **Behavior, not implementation**: tests should still pass after a refactor that doesn't change observable behavior.
- **Error paths matter**: every error condition the impl should handle gets a test that exercises it.
- **Typed discrimination**: when a test cares about a specific failure mode, it must check via the language's typed-error mechanism (sentinel identity, exception class), not a substring of the error message.

## GREEN rules (language-neutral)

- Read every test file in the package before writing impl code.
- Write the MINIMUM code to make tests pass — do not add features no test expects.
- If a test expects a specific failure type, return that exact type.
- After each significant change, run the active language adapter's test command (`toolchain.test` from the package manifest).

## REFACTOR rules (language-neutral)

- Tests must remain green throughout. If you must change a test, justify it.
- Refactor for: clarity, extracted abstractions where 3+ duplicates exist, naming alignment with sibling packages.
- Do NOT add new untested behavior in the refactor pass.

## Verification cycle

After GREEN, the phase lead runs the active toolchain's test command. Outcomes:
- **ALL PASS** → proceed to next package or to refactor.
- **SOME FAIL** → code-generator gets failure output, fixes, re-verify (max 2 retries per package).
- **COMPILATION ERROR / IMPORT ERROR** → code-generator fixes, re-verify.

After 2 failures, the package is flagged BLOCKED in the run manifest; pipeline continues with other packages in parallel.

## Anti-patterns (language-neutral)

1. **Weak assertions** — tests that pass on the skeleton (no real assertion). Always assert at least one observable outcome.
2. **Testing implementation details** — exact-equality on mock arguments breaks any refactor. Assert behavioral properties.
3. **Skipping error-path tests** — every documented error must be exercised in at least one test.

## Coverage strategy

- Every public method on application services (happy path + error paths) gets a RED test.
- Every domain constructor and validation method gets a RED test.
- Tenant / scoping isolation in repositories where applicable.
- Wire-protocol publishing on state changes.
- Target ≥60-70% coverage in the RED phase; remaining 15-25% to reach the package's coverage gate is filled by unit-test-agent in the cross-cutting testing phase.

## Language realizations

- `go-tdd-patterns` — Go realization (test runner setup, mock controllers, table-driven subtests, sentinel-discrimination idiom, compile-time interface assertions).
- `python-tdd-patterns` — Python realization (test framework setup, async test markers, Protocol-spec mocks, parametrize tables, exception-raising assertions, fixture composition).

## Cross-references

- shared-core `decision-logging` — agent cycle steps logged as lifecycle entries
- shared-core `review-fix-protocol` — what happens when verification fails
- shared-core `spec-driven-development` — how TPRD §7 symbols map to tests
