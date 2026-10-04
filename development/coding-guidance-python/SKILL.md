---
name: coding-guidance-python
description: Python implementation and review skill. Use when writing, modifying, refactoring, or reviewing Python code, especially production Python that needs clear contracts, type safety, testability, and maintainable module boundaries. Portable across Python repos and tooling stacks.
---

# Python Coding Guidance

This skill adds portable Python implementation, refactoring, and review guidance.

## Adjacent Skills

This skill provides portable Python engineering principles. Compose with:

- **Workflow:** **thinking** (ambiguous decision framing),
  **recursive-thinking** (stress-testing),
  **security** (threat modeling)
- **Domain overlays:** **backend-guidance** (server-side code),
  **backend-systems-guidance** (stronger backend architecture, reliability, and
  trust-boundary work),
  **ui-guidance** (graphical UI/web frontend),
  **project-core-dev** (repo-specific completion discovery and reporting when
  needed)

Open bundled references only when the task needs that depth:

- [references/python-language-and-testing-rules.md](references/python-language-and-testing-rules.md)
  for typing, interface, test, data-state, module, and architecture decisions
- [references/python-packaging-and-layout.md](references/python-packaging-and-layout.md)
  for distribution, entrypoint, import-layout, or package-structure work
- [references/python-service-boundaries.md](references/python-service-boundaries.md)
  for async cancellation, subprocesses, workers, and real external I/O or
  service boundaries

## When Not to Lean on This Skill

- non-Python work
- notebook-first exploratory work where reproducibility and module design are
  not the main concern
- one-off throwaway scripts where the repo explicitly does not want production
  Python standards

## Implementation Workflow

1. Read the touched modules, entrypoints, tests, package metadata, and nearby
   docs before editing.
2. Infer intended behavior from existing code, imports, and tests when the
   request is only partially specified. Ask only when multiple plausible
   designs would change semantics.
3. Choose the narrowest change that keeps contracts, side effects, error
   handling, and public API shape explicit.
4. Implement with simple functions, clear module boundaries, explicit types
   where they improve the contract, and production-safe behavior at I/O
   boundaries.
5. Add or update tests close to the changed behavior using the repo's existing
   framework and conventions. Use fixtures or parameterization when they make
   setup and cases clearer rather than merely shorter.
6. Run the narrowest relevant formatter, linter, type checker, packaging check,
   and test targets the repo supports.

## Refactoring Workflow

Use this instead of the default implementation workflow when the task is
primarily cleanup or restructuring:

1. Capture current behavior, side effects, hidden globals, import shape, and
   mutation hotspots.
2. Break the refactor into small slices that preserve behavior.
3. Remove long functions, muddled responsibilities, implicit coupling, and
   anti-patterns one step at a time.
4. Keep tests passing after each slice; add characterization coverage first
   when behavior is unclear.
5. Stop when the code is simpler, more explicit, easier to test, and easier to
   operate.

## Review Workflow

When reviewing (not implementing), skip the implementation workflow and use this
instead:

1. Read the change in full before commenting.
2. Identify findings, ordered by severity: `Critical` > `Important` >
   `Suggestion`.
3. Prioritize bugs and regressions, exception or error-path holes, mutable
   shared-state mistakes, typing and interface mismatches, packaging or import
   breakage, performance mistakes with real impact, security risks, and missing
   tests. Add service-boundary observability, retry, and timeout findings when
   the change actually crosses a real external boundary.
4. State findings with concrete evidence and the likely consequence.

Do not edit code or require findings to be fixed unless the user also asks for
remediation.

## Python Rules

### First tier - causes bugs

- Keep module side effects minimal; avoid import-time network calls, filesystem
  mutation, or heavy initialization unless the module is explicitly an
  entrypoint
- Prefer explicit parameters and return values over hidden globals, ambient
  context, or mutation of module-level state
- Do not use mutable default arguments
- Treat `None` handling, optional fields, and missing keys as contract design,
  not cleanup for callers to guess
- Preserve exception context; do not catch broadly and discard the original
  failure without adding useful domain context
- Use context managers for files, locks, subprocess pipes, and other resources
  with lifetime rules
- Be explicit about text vs. bytes boundaries, timezone-aware vs. naive
  datetimes, and sync vs. async call paths
- Do not block the event loop with synchronous I/O in async code
- Do not mix sync and async APIs inside one path without a clear boundary

### Design and verification rules

- Prefer small functions and plain data flow before classes or framework
  indirection; introduce abstractions only when they clarify a real state or
  behavior boundary.
- Use typing syntax supported by the repository's minimum Python version. Add
  types where they clarify public or non-trivial contracts, and keep `Any` as an
  explicit escape hatch rather than a default.
- Follow the repository's existing test framework and conventions. Do not
  migrate `unittest` to pytest merely because new tests are needed.
- Mock external boundaries rather than the behavior under test, and add
  integration coverage when a change crosses package, transport, persistence,
  or subprocess seams.
- Keep validation, serialization, persistence, and business rules separable;
  replace long-lived dict-shaped data or hidden mutation with named contracts.
- Keep module dependencies directed, public package APIs deliberate, and CLI,
  transport, persistence, and domain logic testable at their own seams.
- Keep sync and async entrypoints distinct, own background tasks and their
  cancellation, and protect shared invariants rather than individual fields.
- Make retry, timeout, fallback, observability, and resilience first-class only
  when the task crosses a real external boundary.

Load the references above for the detailed language, testing, packaging, async,
subprocess, and service-boundary rules.

## Decision Heuristics

Use these when the right choice is not obvious:

- **Scope check:** if a change crosses several modules, public entrypoints, or
  import contracts, stop and plan the compatibility and dependency effects
  before continuing.
- **State visibility:** if mutation or side effects are hard to see from the
  function signature, redesign the interface or add a one-line contract comment.
- **Typing pressure:** if `Any`, untyped dicts, or loose tuples start spreading,
  introduce a clearer type boundary before adding more code.
- **Async boundary:** if a change crosses sync and async code, name the boundary
  explicitly and keep adaptation local.
- **Packaging pressure:** if the change affects imports, entrypoints, package
  layout, or published metadata, treat that as a compatibility boundary rather
  than a refactor detail.
- **I/O boundary pressure:** if an external boundary can fail, time out, retry,
  or degrade, make the ownership and diagnostics explicit; local helper code
  usually does not need the same instrumentation.
- **Repo conventions:** if the repo has established formatter, linter, typing,
  or framework conventions, follow them unless they create a correctness or
  maintainability problem.
- **Narrowness vs. quality:** implement the narrowest change that solves the
  problem. When narrowness conflicts with correctness or clarity, prefer
  correctness. When it conflicts with style alone, prefer narrowness unless the
  task is explicitly a cleanup.
- **Adjacent issues:** do not modify unrelated issues unless they are required
  for the requested change's correctness or safety; report them separately.
- **Abstraction threshold:** three similar code blocks or repeated data-shaping
  pain is a pattern; before extracting, check whether a helper function, named
  type, or boundary cleanup is the simpler move.
- **Performance rule:** optimize only after measurement, except for obvious
  algorithmic, allocation, or I/O mistakes on hot paths.
- **Framework pressure:** if a framework convenience hides control flow, data
  ownership, or test seams, prefer the plainer construct.
- **Language-fit check:** if the problem is mostly shell orchestration, keep it
  in shell; if the problem needs rich data shaping, type-safe contracts, or
  non-trivial retry and observability logic, prefer Python over stretching shell
  too far.

## Validation

For implementation, a change is done when:

- the code passes the repo's formatter or format-check
- lint and static analysis report no new findings
- type checking reports no new regressions where the repo uses type checking
- existing tests pass
- new or changed behavior has test coverage, or the lack of coverage is called
  out with a concrete reason
- changed CLI, import, or service entrypoints have a narrow smoke path
- packaging metadata and import paths are verified when the change affects a
  distributable library or CLI

For review, completion means `Critical` and `Important` findings are reported
with concrete evidence, likely consequence, and any validation gap. Unfixed
findings do not make the review incomplete.
