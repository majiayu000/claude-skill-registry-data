---
name: golangci-lint
description: Configure and run golangci-lint
---

# golangci-lint

Meta-linter that runs multiple linters in parallel.

## Install
```bash
go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest
```

## Usage
```bash
golangci-lint run
golangci-lint run ./...
golangci-lint run --fix
```

## Basic Configuration
```yaml
# .golangci.yml
run:
  timeout: 5m
  tests: true

linters:
  enable:
    - gofmt
    - govet
    - staticcheck
    - errcheck
    - gosimple
    - ineffassign
    - unused

linters-settings:
  errcheck:
    check-blank: true
  govet:
    check-shadowing: true
```

## Recommended Linters
```yaml
linters:
  enable:
    - gofmt       # Format check
    - govet       # Built-in analyzer
    - staticcheck # Comprehensive checks
    - errcheck    # Unchecked errors
    - gosimple    # Simplification
    - ineffassign # Ineffective assignments
    - unused      # Unused code
    - revive      # Fast configurable linter
    - gocyclo     # Cyclomatic complexity
    - misspell    # Spelling errors
```

## Exclude Patterns
```yaml
issues:
  exclude-rules:
    - path: _test\.go
      linters:
        - errcheck
        - gosec
    - text: "should have comment"
      linters:
        - revive
```

## CI Integration
```bash
# GitHub Actions
golangci-lint run --out-format=github-actions

# GitLab CI
golangci-lint run --out-format=code-climate > gl-code-quality-report.json
```

## Common Fixes

### errcheck: Unchecked Error
```go
// Bad
file.Close()

// Good
defer file.Close()
```

### gosimple: Redundant Code
```go
// Bad
for i, _ := range items

// Good
for i := range items
```

### ineffassign: Ineffective Assignment
```go
// Bad
result := compute()
result = other()

// Good
result := other()
```

## Performance Tuning
```yaml
run:
  concurrency: 4
  deadline: 5m
  skip-dirs:
    - vendor
    - third_party
```
