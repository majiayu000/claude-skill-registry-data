---
name: go-lint
description: "Golang linting best practices and golangci-lint configuration. Covers running linters, suppressing warnings, and CI integration."
metadata:
  model: models/gemini-3.1-pro-preview
  last_modified: Wed, 06 May 2026 05:35:00 GMT
---

## Core Tool: golangci-lint

`golangci-lint` is the industry-standard tool that aggregates 100+ Go linters into one fast binary.

### Key Commands

```bash
# Run all configured linters
golangci-lint run ./...

# Auto-fix issues where possible
golangci-lint run --fix ./...

# List all available linters
golangci-lint linters
```

## Recommended Linters

Enable these for a high-quality production codebase:
- **Correctness**: `govet`, `staticcheck`, `errcheck`.
- **Security**: `gosec`, `bodyclose`, `sqlclosecheck`.
- **Style**: `gofmt`, `goimports`, `revive`, `misspell`.
- **Performance**: `gocritic`, `prealloc`.

## Suppressing Warnings

Use `//nolint` sparingly. Always specify the linter and provide a reason.

```go
// ✅ Good: Specific linter and justification
//nolint:errcheck // error is not actionable in this specific cleanup context
_ = logger.Sync()

// ❌ Bad: Blanket suppression with no explanation
//nolint
_ = logger.Sync()
```

## Configuration (.golangci.yml)

Every Go project should have a `.golangci.yml` file to ensure consistent rules across the team and CI.

```yaml
linters:
  enable:
    - govet
    - errcheck
    - staticcheck
    - revive
    - bodyclose
    - gosec

run:
  timeout: 5m
  tests: true
```

## Best Practices

1. **Lint on Every Commit** — Catch issues early in the dev cycle.
2. **Auto-fix** — Use `--fix` to handle mechanical changes like formatting and simple refactors.
3. **Fail the Build** — CI should fail if there are any lint violations.
4. **Specific Nolints** — Never use a blanket `//nolint`. It hides too much.
5. **Incremental Adoption** — For legacy code, use `issues.new-from-rev` to only lint new changes.

## Anti-patterns

- ❌ **Ignoring `errcheck`** — Swallowing errors leads to silent failures and hard-to-debug crashes.
- ❌ **No lint configuration** — Leads to "works on my machine" style debates.
- ❌ **Suppessing security linters** — Don't disable `gosec` or `bodyclose` just to "be done".
- ❌ **Too many linters** — Enabling 100+ linters can create too much noise and slow down development. Pick a high-value subset.
- ❌ **Outdated golangci-lint** — New Go versions often require newer linter versions to work correctly.
