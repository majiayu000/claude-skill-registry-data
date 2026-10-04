---
name: senior-developer
description: "Enforces senior developer coding standards: simple readable code, spec compliance, testability, and strict coverage. Use this skill when writing, fixing, refactoring, or testing code in any language."
---
# Senior Developer Coding Standards

Apply these principles when writing or modifying code in any language.
These are the language-neutral standards; a language skill such as go-developer or python-test-automation adds to them and does not override them.

## Simplicity and Readability

- Write the simplest code that solves the problem correctly.
- Prefer explicit over clever.
  If a reader needs to pause to understand a line, simplify it.
- Functions do one thing.
  If a function needs a comment explaining its sections, split it.
- Flat is better than nested; reduce indentation depth by returning early, extracting helpers, or inverting conditions.
- Name variables and functions to reveal intent.
  Avoid abbreviations unless they are universal in the domain (`ctx`, `err`, `id`, `req`, `resp`).
- Avoid premature abstraction.
  Duplication is cheaper than the wrong abstraction.
- Remove dead code, commented-out blocks, and unreachable branches.
  Version control is the archive.

## Spec Compliance

- Implementation must trace back to specifications or requirements documents.
- Before coding, locate the relevant spec.
  If none exists, ask before proceeding.
- If behavior contradicts or is absent from the spec, halt and surface the gap.
- Do not modify specs to match implementation.
  Specs lead; code follows.
- Prefer linking to spec sections over duplicating design rationale in code comments.
- When writing or editing tech specs: "Traces To" subsections MUST be the **last** subsection under their parent Spec Item heading and MUST contain **only** a list of requirement links - no prose or other content.

## Testability-First Design

Write code that is easy to test from the start:

- Accept dependencies via constructor arguments or function parameters, not global state.
- Define small interfaces at the consumer site for mockability.
- Keep side effects at the edges; pure logic in the core.
- Avoid hidden dependencies (singletons, package-level vars, init functions that mutate state).
- Separate I/O from computation so the computation can be tested without I/O.

## Code Coverage Discipline

### Non-Negotiable Rules

- **NEVER lower coverage thresholds.**
  If coverage drops, add tests -- do not adjust the bar.
- **NEVER skip, disable, or mark tests as expected-to-fail** to work around a broken change.
  Fix the code or the test.
- **NEVER use coverage exclusion annotations** (e.g. `//nolint`, `# pragma: no cover`, `istanbul ignore`) to hide untested code.
  If code exists, it must be tested.
- Target >= 90% unit test coverage on new and changed code.
- Untestable code is a design signal; refactor to make it testable rather than excluding it.

### Test Quality Matters More Than the Number

- Cover the happy path, error paths, edge cases, and boundary conditions.
- Table-driven / parameterized tests for functions with multiple input combinations.
- Test behavior and contracts, not implementation details.
- Tests must be deterministic; no flaky assertions on timing, order, or external state.

## Linting Discipline - Non-Negotiable Rules

- **NEVER suppress, disable, or bypass linter warnings.**
  Fix the underlying issue.
- **NEVER add linter suppression comments** (`//nolint`, `# noqa`, `// eslint-disable`, etc.) unless the linter is provably wrong about a specific line and a senior human has approved it.
- **NEVER weaken linter configuration** (raising thresholds, removing rules, widening exclusions).
- All code must pass the project's configured linters before considering work complete.
- Treat linter warnings as errors during development; address them immediately, not later.

## Code Change Discipline

- Preserve existing working code.
  Make the minimum change necessary.
- No opportunistic refactoring; stay focused on the task at hand.
- If you find a pre-existing issue unrelated to your task, note it separately; do not fix it in the same change.
- Run the project's lint, test, and CI checks after every substantive change.
- Conventional commit messages: type(scope): concise description of why.

## Error Handling

- Handle every error.
  Never silently discard failures.
- Wrap errors with context so the caller knows where and why something failed.
- Fail fast on invalid inputs and precondition violations.
- Log errors with structured context, not string interpolation of sensitive data.

## Anti-Patterns to Flag

Halt or raise a concern if you observe yourself or others doing any of the following:

- Reducing a coverage threshold to make CI pass.
- Adding `nolint`, `noqa`, `eslint-disable`, or equivalent to silence a finding.
- Writing a test that asserts on implementation internals rather than behavior.
- Leaving `TODO` / `FIXME` without a tracking reference.
- Committing commented-out code.
- Adding a dependency for something trivially implementable.
- Guessing or simulating output from tools, APIs, or databases instead of using real results.
