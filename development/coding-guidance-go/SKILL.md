---
name: coding-guidance-go
description: Go implementation and review guidance for non-interactive CLIs, libraries, workers, and services; use `coding-guidance-go-tui` for interactive Bubble Tea and `go-testing-with-testify` for testify-focused test work. Covers errors, contexts, concurrency, package boundaries, standard tests, and measured performance.
---

# Go Coding Guidance

Portable Go implementation, refactoring, testing, optimization, and review
guidance.

## Adjacent Skills

Compose with:

- **Workflow:** `thinking` for ambiguous decision framing,
  `recursive-thinking` for
  stress-testing, `security` for threat modeling
- **Domain overlays:** `backend-guidance` for server-side code,
  `backend-systems-guidance` for deeper backend architecture/reliability/trust
  boundaries, `project-core-dev` for repo-specific completion discovery and
  reporting when needed, and
  `project-config-and-tests` for config contracts and deterministic tests at
  config or path seams
- **Testing:** `go-testing-with-testify` when the main artifact is testify-based
  Go test code, test review, or Go test flake triage
- **TUI specialization:** `coding-guidance-go-tui` when Bubble Tea state,
  Bubbles components, Lip Gloss layout, or an interactive terminal screen is
  the main concern

## When Not to Lean on This Skill

- non-Go work
- interactive Bubble Tea or Charmbracelet terminal screens; use
  `coding-guidance-go-tui`
- pure test strategy without implementation code or concrete Go test code; use
  `tester-mindset`
- testify-specific assertion, mock, suite, or flake work; use
  `go-testing-with-testify`
- security as the primary job; use `security` and compose this skill only for
  Go-specific implementation details
- repo-specific framework rules that should live in local docs, generated-code
  policy, linter config, or domain overlays

## Reference Map

Load references only when the task needs that depth:

- [go-concurrency-and-services.md](references/go-concurrency-and-services.md)
  for context, goroutine ownership, shared state, pipelines, backpressure,
  logging, REST/gRPC/CLI/worker boundaries, and transport error mapping
- [go-testing-and-validation.md](references/go-testing-and-validation.md) for
  standard Go tests, comparison choices, helpers, fuzzing, benchmarks, race
  checks, integration-test gating, and validation command selection
- [go-performance-and-modules.md](references/go-performance-and-modules.md)
  for package/module layout, `go.mod`/`go.sum`, `go.work`, vendoring,
  generated code, release metadata, dependency pressure, profiling, and hot-path
  allocation guidance
- [go-api-and-language-rules.md](references/go-api-and-language-rules.md) for
  naming, declarations, exported-contract stability, interface placement,
  generics, nil and collection semantics, and other detailed language rules

## Mode Selection

Use the narrowest mode that fits the task:

- **Routine edit:** follow the implementation workflow, then apply only relevant
  rule sections and validation commands.
- **Review:** use the review workflow first; consult references only to verify
  concrete findings.
- **Refactor:** use the refactoring workflow and preserve exported contracts
  unless the task explicitly changes them.
- **Concurrency:** load the concurrency/service reference and focus on context
  ownership, goroutine lifecycle, shared state, backpressure, race validation,
  and shutdown.
- **Service boundary:** use this skill for Go-specific context, error,
  transport, and handler mechanics; add `backend-guidance` or
  `backend-systems-guidance` for architecture, repositories, transactions,
  queues, or cross-service design.
- **Performance:** load the performance/modules reference and require benchmark,
  `pprof`, trace, or allocation evidence before performance-driven rewrites.

## Implementation Workflow

1. Read touched packages, call sites, tests, `go.mod`, `go.sum`, build tags,
   generated or vendored boundaries, and nearby docs before editing.
2. Identify the module Go version, formatter/import tool, linter/test commands,
   service boundary style such as REST, gRPC, CLI, or worker, and existing
   assertion, logging, DI, config, or framework conventions.
3. Infer intended behavior from existing code and tests when the request is
   partially specified. Ask only when multiple plausible Go designs would
   change semantics.
4. Choose the narrowest change that keeps package boundaries, error contracts,
   context ownership, resource lifetime, and concurrency behavior explicit.
5. Implement with small packages, simple functions, explicit dependencies,
   idiomatic error handling, useful zero values, externalized configuration,
   and goroutine ownership that can be tested.
6. Keep generated code, vendored code, API schemas, module paths, public JSON
   tags, CLI flags, and exported identifiers stable unless the task explicitly
   changes that contract.
7. Add or update tests close to the changed behavior. Prefer table-driven tests
   only when cases share the same setup and assertion path.
8. Run the narrowest relevant `gofmt`, `goimports`, `go test`, `go vet`, race,
   lint, module, benchmark, profile, and security commands the repo supports.

## Refactoring Workflow

Use this instead of the default implementation workflow when the task is
primarily cleanup or restructuring:

1. Capture current behavior, exported API shape, package dependencies, error
   values, context flow, goroutine ownership, shared state, and import graph.
2. Add characterization tests first when behavior is unclear or risk is high.
3. Break the refactor into small slices that preserve behavior and compile
   after each slice.
4. Remove circular dependencies, vague packages, hidden globals, duplicated
   error handling, and unclear interface seams one step at a time.
5. Keep tests passing after each slice and avoid changing public contracts as an
   incidental cleanup.
6. Stop when package responsibilities, call sites, and failure behavior are
   clearer without making abstractions larger than the code they protect.

## Review Workflow

When reviewing, skip the implementation workflow and use this instead:

1. Read the change in full before commenting.
2. Check mechanical issues first: formatting, imports, generated-code drift,
   module changes, build tags, and obvious compile/test breakage.
3. Identify findings, ordered by severity: `Critical` > `Important` >
   `Suggestion`.
4. Prioritize bugs and regressions, data races, goroutine leaks, context misuse,
   resource leaks, error wrapping or sentinel mismatches, nil pointer or nil map
   hazards, interface overreach, package-cycle pressure, security risks,
   performance mistakes with real impact, and missing tests.
5. Do not spend review budget on nits that `gofmt`, `goimports`, or the repo's
   linter will settle unless they hide a real readability or behavior issue.
6. State findings with concrete evidence and the likely consequence.

Do not edit code or require findings to be fixed unless the user also asks for
remediation.

## Core Go Rules

- Always run `gofmt`; run `goimports` when the repo uses or provides it and
  imports changed.
- Handle every error deliberately. Do not discard errors with `_` unless the
  call cannot fail meaningfully or a comment explains why it is safe to ignore.
- Return `error` for an operation's failure result and avoid typed-nil errors.
  A constructor whose purpose is to create an error value may return a concrete
  type; distinguish that API from an operation reporting success or failure.
- Wrap errors with context callers do not already have. Preserve
  machine-checkable causes with `%w` when callers should use `errors.Is` or
  `errors.As`; avoid leaking internals across process, API, or trust
  boundaries.
- Propagate `context.Context` as the first parameter through request-scoped
  blocking work. Do not store contexts in structs or use them for optional
  parameters.
- Always call cancel functions returned by `context.WithCancel`,
  `WithTimeout`, or `WithDeadline` when the current scope owns them.
- Close response bodies, files, and rows on every owned path; stop timers and
  tickers when cancellation or shutdown requires it. Follow the target Go
  version's timer semantics. Check close errors that can affect persisted data.
- Do not launch goroutines without a clear owner, cancellation path, error
  propagation path, and testable shutdown behavior.
- Protect shared mutable state with a clear synchronization rule. Do not copy
  values containing `sync.Mutex`, `sync.WaitGroup`, `bytes.Buffer`, or similar
  pointer-owned state after first use.
- Use `crypto/rand` for keys, tokens, and security-sensitive randomness. Never
  use `math/rand` for secrets.
- Do not hardcode environment-specific configuration in libraries or deep
  packages. Parse env, flags, and config files at process boundaries, validate
  once, and pass typed configuration inward.
- Keep `panic`, `log.Fatal`, and `os.Exit` out of libraries and non-main code.
  Return errors for ordinary failures; panic only for programmer errors,
  impossible states, or startup failures where recovery is not expected.

Detailed naming, declaration, interface, compatibility, collection, and
generics guidance lives in
[go-api-and-language-rules.md](references/go-api-and-language-rules.md). Load it
when those choices are material; do not spend routine task context on a full
style catalog.

## Decision Heuristics

- **Package pressure:** if a package name becomes vague or exported names need
  stuttering to make sense, split responsibilities or rename the package.
- **Interface pressure:** if a new interface mirrors one concrete type exactly,
  it may be a mock seam rather than a design seam.
- **Generics pressure:** if only one concrete type exists today, write concrete
  code first unless the generic API is already part of the public contract.
- **Options pressure:** if optional constructor arguments are few and internal,
  prefer a config struct or explicit parameters; if they are public,
  extensible, and mostly defaulted, prefer functional options.
- **Error pressure:** if callers need to branch on errors, make that contract
  stable with sentinels, typed errors, or predicates before adding more string
  checks.
- **Context pressure:** if a function can block on I/O, locks, remote systems,
  or queues, pass context unless the repo has a narrower convention.
- **Goroutine pressure:** if you cannot say who cancels a goroutine, who waits
  for it, and who observes its error, do not start it yet.
- **Service-boundary pressure:** if a handler, RPC method, or CLI command is
  accumulating business rules, split transport decoding from domain behavior
  before adding more branches.
- **Test-shape pressure:** if a table test needs conditionals for setup or
  assertions, split it; table tests should reduce duplication, not hide logic.
- **Profile pressure:** if a performance change cannot name the measured
  bottleneck, the benchmark/profile used, and the before/after signal, treat it
  as speculative cleanup rather than optimization.
- **Dependency pressure:** if adding a module changes licenses, binary size,
  supply-chain risk, or transitive surface, justify it against standard library
  or repo-local alternatives.
- **Narrowness vs. quality:** implement the narrowest change that solves the
  problem. When narrowness conflicts with correctness, resource safety, or race
  safety, prefer correctness.
- **Adjacent issues:** do not modify unrelated issues unless they are required
  for the requested change's correctness, resource safety, or race safety;
  report them separately.

## Validation

For implementation, a change is done when:

- `gofmt` or the repo's formatter has run on touched Go files
- `goimports` or the repo's import formatter has run when imports changed
- touched packages compile and affected tests pass
- new or changed behavior has tests, or the lack of tests is called out with a
  concrete reason
- `go vet`, `staticcheck`, `golangci-lint`, or the repo's static analysis path
  reports no new findings when available
- `go test -race` is run for touched packages when concurrency, shared state,
  or goroutine lifetime changed
- benchmarks, `pprof`, traces, or allocation profiles back performance-driven
  changes
- module, generated-code, build-tag, and wire-format changes are verified with
  the repo's established commands
- security-sensitive code gets the repo's security scan, such as `gosec`, when
  available

For review, completion means `Critical` and `Important` findings are reported
with concrete evidence, likely consequence, and any validation gap. Unfixed
findings do not make the review incomplete.
