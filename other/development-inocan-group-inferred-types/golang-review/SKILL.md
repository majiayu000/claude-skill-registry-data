---
name: golang-review
description: Go code standards enforcing idiomatic patterns, safety, and maintainability. Use when writing, generating, or reviewing Go code.
---

# Go Code Review Skill

Rules ensuring maintainability, safety, and developer velocity. **MUST** rules enforced by CI/review; **SHOULD** rules are strong recommendations; **CAN** rules allowed without extra approval.

## 1 — Before Coding
- **BP-1 (MUST)**: Ask clarifying questions for ambiguous requirements
- **BP-2 (MUST)**: Draft and confirm approach before coding
- **BP-3 (SHOULD)**: List pros/cons when multiple approaches exist
- **BP-4 (SHOULD)**: Define testing strategy and observability signals upfront

## 2 — Modules & Dependencies
- **MD-1 (SHOULD)**: Prefer stdlib; introduce dependencies with clear justification
- **MD-2 (CAN)**: Use govulncheck for updates

## 3 — Code Style
- **CS-1 (MUST)**: Enforce gofmt, go vet
- **CS-2 (MUST)**: Avoid name stutter in packages
- **CS-3 (SHOULD)**: Small interfaces near consumers; prefer composition
- **CS-4 (SHOULD)**: Avoid reflection on hot paths; prefer generics
- **CS-5 (MUST)**: Use input structs for functions with >2 arguments
- **CS-6 (SHOULD)**: Declare input structs before consuming functions

## 4 — Errors
- **ERR-1 (MUST)**: Wrap with %w and context
- **ERR-2 (MUST)**: Use errors.Is/As for control flow
- **ERR-3 (SHOULD)**: Define sentinel errors in package
- **ERR-4 (CAN)**: Use context.WithCancelCause for error propagation

## 5 — Concurrency
- **CC-1 (MUST)**: Sender closes channels; receivers never close
- **CC-2 (MUST)**: Tie goroutine lifetime to context.Context
- **CC-3 (MUST)**: Protect shared state with sync.Mutex/atomic
- **CC-4 (SHOULD)**: Use errgroup for fan-out work
- **CC-5 (CAN)**: Buffered channels only with rationale

## 6 — Contexts
- **CTX-1 (MUST)**: ctx must be first parameter; never store in structs
- **CTX-2 (MUST)**: Propagate non-nil ctx; honor Done/deadlines
- **CTX-3 (CAN)**: Expose WithX helpers deriving deadlines from config

## 7 — Testing
- **T-1 (MUST)**: Table-driven, deterministic, hermetic tests
- **T-2 (MUST)**: Run with -race flag in CI; use t.Cleanup
- **T-3 (SHOULD)**: Mark safe tests with t.Parallel()

## 8 — Logging & Observability
- **OBS-1 (MUST)**: Structured logging with slog, levels, consistent fields
- **OBS-2 (SHOULD)**: Correlate logs/metrics/traces via request IDs
- **OBS-3 (CAN)**: Provide debug/pprof endpoints with auth guards

## 9 — Performance
- **PERF-1 (MUST)**: Measure before optimizing using pprof, benchmarks
- **PERF-2 (SHOULD)**: Avoid allocations on hot paths; reuse buffers
- **PERF-3 (CAN)**: Add microbenchmarks for critical functions

## 10 — Configuration
- **CFG-1 (MUST)**: Config via env/flags; validate on startup; fail fast
- **CFG-2 (MUST)**: Treat config as immutable after initialization
- **CFG-3 (SHOULD)**: Provide sensible defaults and clear documentation
- **CFG-4 (CAN)**: Support hot-reload only with correctness guarantees

## 11 — APIs & Boundaries
- **API-1 (MUST)**: Document exported items; minimize exported surface
- **API-2 (MUST)**: Accept interfaces where variation needed; return concrete types
- **API-3 (SHOULD)**: Keep functions small, orthogonal, composable
- **API-5 (CAN)**: Use constructor options pattern for extensibility

## 12 — Security
- **SEC-1 (MUST)**: Validate inputs; set explicit I/O timeouts; prefer TLS
- **SEC-2 (MUST)**: Never log secrets; manage outside code
- **SEC-3 (SHOULD)**: Limit filesystem/network access by default
- **SEC-4 (CAN)**: Add fuzz tests for untrusted inputs

## 13 — CI/CD
- **CI-1 (MUST)**: Lint, vet, test (-race), build on every PR
- **CI-2 (MUST)**: Reproducible builds with -trimpath; embed version via -ldflags
- **CI-3 (SHOULD)**: Require review sign-off for MUST rules
- **CI-4 (CAN)**: Publish SBOM; run govulncheck/license checks

## 14 — Tooling Gates
- **G-1 (MUST)**: go vet ./... passes
- **G-2 (MUST)**: golangci-lint run passes with project config
- **G-3 (MUST)**: go test -race ./... passes

## Review Checklist

When reviewing Go code:

1. **Readability**: Is the code clear and self-documenting?
2. **Complexity**: Is cyclomatic complexity reasonable?
3. **Data structures**: Are appropriate structures/algorithms used?
4. **Dependencies**: Are hidden dependencies factored out?
5. **Naming**: Is function/variable naming consistent?
6. **Error handling**: Are errors wrapped with context?
7. **Concurrency**: Are goroutines properly managed?
8. **Testing**: Are tests table-driven and comprehensive?
