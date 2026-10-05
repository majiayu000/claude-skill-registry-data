---
name: testing-go
description: Writes tests following TDD (using go test, testify, and rapid) best practices. Use when writing unit tests, integration tests, or table-driven tests in Go.
compatibility: Designed for Claude Code
metadata:
  allowed-tools: Read, Grep, Glob, Edit, Write, Bash
  argument-hint: [test-scope or component-name]
  stability: stable
  content-hash: sha256:4ff8b1bda32cad71300ab72691e0df08e7d8e991ea8bcb20b764b98d55e5d353
---

# Go Testing

**Target**: $ARGUMENTS

Writes **focused, behavior-driven tests** following project testing strategy.

## Quick Reference

**TDD methodology** (language-agnostic): See `tdd-core` plugin (`testing-tdd` skill)

**Go-specific documentation**: `references/`

- `references/testing-strategy.md` — Go tools (go test, testify, rapid, gomock)
- `references/tdd-best-practices.md` — Go TDD examples (extends tdd-core)

## Quick Decision

**go test (default)**: Use table-driven tests for known cases. Works at unit/integration levels.

**rapid (edge cases)**: Use for invariants that must hold for ALL inputs.

See `references/testing-strategy.md` for full methodology comparison.

## TDD Essentials (Quick Reference)

**Cycle**: RED (failing test / compile error) -> GREEN (minimal pass) -> REFACTOR (clean up)

**Structure**: Arrange-Act-Assert (AAA)

```go
func TestOrderCalculator_Total_SumsItemPrices(t *testing.T) {
    // ARRANGE
    calc := NewOrderCalculator()
    items := []Item{{Price: 10.00, Qty: 2}, {Price: 5.00, Qty: 1}}

    // ACT
    total := calc.Total(items)

    // ASSERT
    assert.Equal(t, 25.00, total)
}
```

## Table-Driven Tests (Go Idiom)

```go
func TestValidateEmail(t *testing.T) {
    tests := []struct {
        name    string
        email   string
        wantErr bool
    }{
        {name: "valid", email: "user@example.com", wantErr: false},
        {name: "missing @", email: "userexample.com", wantErr: true},
        {name: "empty", email: "", wantErr: true},
    }
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            err := ValidateEmail(tt.email)
            if tt.wantErr {
                require.Error(t, err)
            } else {
                require.NoError(t, err)
            }
        })
    }
}
```

## What to Test (KISS/DRY/YAGNI)

**High-Value**: Business logic, error paths, integration points, contracts

**Avoid**: Stdlib behavior, trivial getters, default zero values, type existence

See `references/testing-strategy.md` -> "Patterns to Remove" for full list.

## Naming Convention

**Format**: `Test{Type}_{Method}_{Behavior}`

```go
TestUserService_Create_ReturnsIDOnSuccess
TestValidateEmail_MissingAt
TestCalculateTotal_EmptyItems
```

## Execution

```bash
go test ./...                           # All tests
go test -run TestUserService ./...      # Filter by name
go test -race ./...                     # Race detector
go test -v -run TestValidateAge ./...   # Verbose single test
```

## Quality Gates

- [ ] All tests pass (`go test ./...`)
- [ ] TDD Red-Green-Refactor followed
- [ ] Arrange-Act-Assert structure used
- [ ] Table-driven tests for multiple cases
- [ ] Behavior-focused (not implementation)
- [ ] No stdlib behavior tested
- [ ] Interface fakes use `var _ Interface = (*fake)(nil)` compile check
