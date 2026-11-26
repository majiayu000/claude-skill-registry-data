---
name: go-lint
description: "How to format Go code with gofumpt through golangci-lint fmt, run and fix golangci-lint, pick the linter set and pin the version in mise.toml. Use when lint fails, when setting up linting, or before opening a Go pull request."
---

# Go lint

Format and lint a Go module and resolve the findings.

## When to use

- `golangci-lint` reports a finding or CI fails on lint.
- Adding linting to a module.
- Final step before opening a Go pull request.

## Steps

1. Format first with `golangci-lint fmt`, which runs `gofumpt` under the configured settings.
   Use the repository's pinned version.
2. Confirm `.golangci.yaml` exists in the repository root. Add it with the linter set below if
   not.
3. Run `golangci-lint run ./...`, or the repository's task runner target if one exists, so
   local matches CI.
4. Group the findings. Most trace to an unchecked error, a shadowed variable, missing context
   propagation or dead code.
5. Fix the cause. An unchecked error gets handled, or ignored as `_` with a comment. Unused
   code gets deleted, not exported. A `gosec` finding gets fixed or documented as not a risk.
6. Apply autofixes with `golangci-lint run --fix ./...` and review the diff.
7. Add an exception only when the finding is wrong or every alternative is worse.
8. Commit the formatting change separately from the behavior change.

## Rules

### Config

- One `.golangci.yaml` in the repository root. No per directory config.
- Enable linters explicitly. Do not rely on the default set.
- Pin `golangci-lint` in `mise.toml`. A `golangci-lint` binary is built with a Go toolchain at
  least as new as the `go` directive in `go.mod`, so the pinned `golangci-lint` and the pinned
  Go version move together, and an upgrade is a deliberate commit.
- Exclude generated code by path (`zz_generated.*`, `*.pb.go`), not with an inline comment.
- Lint test files too.

### Linter set

- Correctness: `errcheck`, `govet`, `staticcheck`, `ineffassign`, `unused`.
- Errors and context: `errorlint`, `noctx`, `bodyclose`.
- Style and logging: `revive`, `misspell`, `sloglint`.
- Security: `gosec`.

### Exceptions

- Always inline, always names the linter, always carries a reason:

```go
//nolint:gosec // path comes from validated config, not user input
data, err := os.ReadFile(cfg.CertPath)
```

- A bare `//nolint` is rejected.
- Never disable a linter repository wide to silence one finding.
- A repository wide disable is justified in the pull request, and only when the repository
  rejects the rule itself.
- A config exclusion is for a category, never for one individual finding.
- "False positive" is not a reason on its own.

### Other tooling

- `gofumpt` is a superset of `gofmt`. Never run both.
- `go vet ./...` and `go build ./...` must also pass.
- Use the repository's pre-commit setup or CI workflow if one exists.

## Guardrails

- `golangci-lint fmt` run, no formatting diff left.
- `.golangci.yaml` present, linters explicit, test files included.
- `golangci-lint run ./...` clean.
- Findings fixed at the cause, not suppressed.
- Each `nolint` names its linter and gives a reason, no repository wide disable hiding one
  finding.
- Generated code excluded by path.
- Formatting committed separately from behavior.
- `golangci-lint` pinned in `mise.toml`, built with a Go toolchain at least as new as the `go`
  directive in `go.mod`.

## References

- `lint` for detecting the repository's tooling and running the formatter and linter together.
- <https://golangci-lint.run/usage/linters/>
