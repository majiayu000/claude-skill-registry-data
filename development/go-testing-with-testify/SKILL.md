---
name: go-testing-with-testify
description: Write, review, or harden Go tests using stretchr/testify assert, require, mock, or suite. Use for assertion choice, test doubles, subtests, concurrency, and flake triage in an existing Go test setup. Use coding-guidance-go for production code or non-testify tests and tester-mindset for test strategy without concrete test code.
---

# Go Testing With Testify

Turn a concrete behavior claim into useful Go test evidence. Preserve the
repository's Go version, test framework, and supported execution environment.

## Route And Select Activity

- **Implement or harden:** edit the requested tests and any explicitly covered
  production seam. A test request does not automatically authorize an unrelated
  production refactor, new dependency, or external service.
- **Review:** inspect tests and report prioritized findings, evidence, and
  consequences. Do not edit files or require remediation to complete a review.
- **Diagnose:** reproduce the named failure in scope, distinguish a product
  defect from a test-apparatus defect, then fix it when the request includes repair.

Use `coding-guidance-go` for production Go or non-testify tests. Preserve
Ginkgo, Gomega, go-cmp-only, and other intentional stacks. Module bootstrap or
test-tool installation is separate from test authoring.

Add `tester-mindset` when claims, oracles, or test strategy are still unclear.
Add `backend-guidance` or `backend-systems-guidance` only when a service,
repository, queue, or other backend boundary needs that design guidance.
Use `security` first for a security-led review and add
`security-identity-access` when its identity scope applies. Routine tests of an
already-defined permission rule can remain here.

## Workflow

1. Read the scoped tests, implementation, `go.mod`, fixtures, and relevant
   repository instructions. Identify the Go and testify versions, local test
   command, helpers, and available dependencies.
2. Name the behavior claim, oracle, and smallest seam that can reveal a defect.
   Pure logic needs a unit check; protocol, query, serialization, or lifecycle
   behavior may need a real boundary. Passing checks support only their scope.
3. Preserve the existing test shape when it is clear. Use table-driven subtests
   when cases share setup and assertions; use separate tests when they do not.
   Introduce helpers, fakes, mocks, or suites only for a concrete benefit.
4. For implementation, exercise the real code and assert the behavior being
   claimed. For review, assess these choices without rewriting the tests.
5. Validate the narrowest changed test or package, for example
   `go test ./path/to/pkg -run '^TestName$' -count=1`. Add race checks,
   repetition, shuffle, or integration runs when the failure mode needs them.
6. Inspect failures before changing assertions, retry counts, or timeouts.
   Report the exact evidence and remaining uncertainty.

## Assertions And Oracles

- Put expected before actual in testify comparisons.
- Use `require` for prerequisites whose failure makes later checks unsafe or
  meaningless; use `assert` for independent checks. A fatal failure in a
  subtest stops that subtest, not its siblings.
- Call `require.*`, `t.Fatal`, and `t.FailNow` only on the test goroutine.
  Return observations or errors from HTTP handlers and workers through a
  synchronized channel or result, then assert on the test goroutine.
- Use `ErrorIs` or `ErrorAs` when error identity or type is the contract.
  Error presence alone is sufficient when that is all the contract promises.
  Assert text only when it is intended to be stable.
- Use equality, unordered comparison, identity, structural JSON, or tolerances
  according to the contract. Exact float equality is valid for exact expected
  values; approximate computations need justified tolerances.
- Check fields the behavior promises, including generated IDs, defaults, or
  timestamps when relevant. Whole-struct equality is valid when the full value
  is the contract; do not discard meaningful fields merely to avoid failures.
- A success-only test can be meaningful. Add separate failure cases where they
  protect required behavior; do not require every individual test to exercise
  both success and failure.
- Call `t.Helper()` in helpers whose failures should identify their caller.

Reject tautologies, mocks that replace the behavior being proved, and assertions
that cannot detect a plausible defect in the stated claim. A no-error assertion
can prove a narrow validation contract but does not prove that a user was stored
or a file's contents are correct. Logs can be the oracle when logging itself is
the requested behavior.

## Boundary And Double Choice

Prefer an existing cheap real harness when the risk is at that boundary:

- HTTP protocol behavior: `httptest.NewServer`;
- filesystem behavior: `t.TempDir()`;
- database queries or transactions: a disposable dialect-appropriate harness;
- time or async behavior: explicit synchronization, injected time, or supported
  virtual-time testing.

Use a fake for a simple owned collaborator; use `testify/mock` when argument,
call-count, failure, or ordering expectations improve the test. Respect existing
test seams. Do not introduce wrappers or containers solely to satisfy a generic
mock rule, and do not contact live or metered services without authority.

Wire the double into the subject under test. Assert mock expectations after
owned asynchronous calls finish, using cleanup when it must also run after a
fatal test failure. Keep matchers specific to the promised interaction and
avoid retaining mutable pointer arguments as if they were immutable snapshots.

## Concurrency, Time, And Cleanup

- Add `t.Parallel()` only after checking shared state, database schemas, ports,
  temporary paths, environment, current directory, and goroutine lifetimes.
  `t.Setenv` and `t.Chdir` cannot be used in parallel tests or with parallel
  ancestors; check helper availability against the supported Go version.
- Testify `suite` does not support parallel tests. Keep suites when their
  scenario and lifecycle organization helps; do not migrate them for style alone.
- Go 1.22+ loop semantics depend on the module language version. Rebind loop
  variables where older semantics require it, not as mandatory modern boilerplate.
- Register cleanup next to acquisition. Own cancellation and wait for workers
  before test teardown; a deadline limits waiting but does not itself join work.
  `t.Context()` is available from Go 1.24 and cancels before cleanup.
- Prefer completion signals to polling. Use bounded `Eventually` only for a
  genuinely eventual observable state and synchronize shared reads.
- On Go 1.25+, consider `testing/synctest` for compatible in-process concurrent
  code. Virtual time is not a replacement for real network or external-system
  evidence. Sleeps inside its virtual-time bubble differ from wall-clock delays.
- Keep each operation's timeout and cleanup bounded. A slow polling callback can
  outlive the assertion budget if its own I/O has no cancellation.

## Flake Triage And Completion

Reproduce one failing test with its original environment, then vary a relevant
dimension: ordering, workers, parallelism, timing, or shared state. Use
`-race` for suspected races and `-count=N` or `-shuffle=on` for repetition
and order dependence; choose the package and run budget from the risk.
A finite passing sample does not prove that a flake is impossible.

Distinguish a data race, product defect, fixture bug, resource leak, unsupported
runtime, and external dependency failure. Fix causes without weakening the
oracle. Quarantine only under the repo's accepted policy with a reason, owner,
tracking reference, and revisit condition.

Stop when the changed claim has proportionate evidence and further similar
tests would add little confidence. Report material untested behavior and the
next useful check. A completed review may contain unresolved findings.

Return the claim, seam, cases, oracles, exact commands/results, and residual risk
when they help assess the work; collapse these into a short note for a small edit.

## References

Load only the detail relevant to the task:

- [Assertion patterns](references/assertion-patterns.md): equality, errors,
  async assertions, and helpers.
- [Mocking patterns](references/mocking-patterns.md): fakes, expectations,
  argument matching, pointer mutation, and ordering.
- [Real boundaries](references/real-boundary-patterns.md): HTTP, database,
  filesystem, clocks, and worker lifecycle examples.
- [Suites and parallelism](references/suite-and-parallelism.md): lifecycle,
  subtests, Go-version constraints, and process-wide state.
- [Pressure scenarios](references/pressure-tests.md): maintainer or contentious
  review cases; distinguish static assessment from observed behavior.
- [Coverage and validation](references/coverage-and-validation.md): maintainer
  source map, routing boundaries, and evidence limitations.
