---
name: go-tests
description: "How to write Go tests with table driven subtests, fakes over mocks, httptest, golden files and the race detector in CI. Use when writing, fixing or reviewing Go tests."
---

# Go tests

Procedure and conventions for adding tests to a Go module.

## When to use

- Adding a test, fixing a failing or flaky test, reviewing test coverage in a pull request.
- Load `go-conventions` first.

## Steps

1. Test beside the code in the same directory. Use a `_test` package suffix to pin the public
   surface, the same package to reach internals.
2. Write the case struct, then the cases, then one `t.Run` loop.
3. Add `t.Parallel()` on the outer and inner test, unless it uses `t.Setenv`, the working
   directory or a global.
4. Assert errors with `errors.Is` or `errors.As`, never on the message string. A refusal names
   the typed error or the code carried on it, never the message, even to name the mechanism.
   A reason or code returned as an ordinary value, not formatted into an error, is what to
   assert on. Where it is the only observable separating two mechanisms, asserting it is
   required.
5. Replace a dependency with a hand written fake that satisfies the consumer side interface.
6. HTTP: `httptest.NewServer` for a client, `httptest.NewRequest` plus `httptest.NewRecorder`
   for a handler. Exercise the real chain, including middleware.
7. Large expected output: a golden file under `testdata/`, refreshed behind a `-update` flag.
   Review a golden diff like code.
8. Run `go test ./...`, iterate with `-run 'TestName/case'`.
9. Finish with `go test -race -count=1 ./...`.

## Rules

### Test naming

- `TestFuncName` for a function, `TestType_Method` for a method.
- A subtest name describes the case, not the expectation: `"missing id"`, `"upstream times
  out"`.
- Case struct fields: `name`, `input`, `want`, `wantErr`.
- One behavior per case. A case that needs a comment should be split.

### Fakes over mocks

- No mock framework, no generated mock.
- A fake is a small struct with canned results and recorded calls, defined in the test file.
- Assert on observable behavior, not call counts or argument order.
- Prefer the real implementation when it is cheap and deterministic.

### What to test

- Every exported function: the happy path plus its primary failure.
- Cover explicitly: nil and empty input, zero values, boundaries, duplicates, out of order
  input, a cancelled context, a dependency error, a dependency timeout, concurrent access when
  concurrency is part of the contract.
- Test behavior, not implementation. A behavior preserving refactor must not change a test.

### CI

- The CI test job runs `go test -race -count=1 ./...` too, not only the local step before a
  pull request.

### Unit or integration

- Unit by default: the logic is local, dependencies fit a fake, the test runs in milliseconds.
- Integration only when the behavior under test is a dependency's own semantics, or only
  appears across a process boundary.
- Guard a slow test with `testing.Short()` so `go test -short ./...` stays fast.

### Coverage

- A signal, not a target. Never add a test only to move the number.
- Read it per file: `go test -coverprofile=cover.out ./...` then `go tool cover
  -func=cover.out`. An uncovered error branch is the useful finding.

## Guardrails

- Table driven with `t.Run`, case names describe the case, `t.Parallel()` or a stated reason
  not to.
- Errors asserted with `errors.Is` or `errors.As`.
- A refusal asserted on the typed error or its code, never the message.
- Hand written fakes, no mock framework.
- HTTP exercised through `httptest` against the real chain.
- Golden files in `testdata/`, diffs reviewed.
- Edge cases and failure paths explicit.
- `go test -race -count=1 ./...` passes locally and in CI.

## References

- `test` for detecting the runner and extending coverage for changed code.
- `testing-conventions` for when a test is written and what earns one.
- `httptest`: <https://pkg.go.dev/net/http/httptest>
