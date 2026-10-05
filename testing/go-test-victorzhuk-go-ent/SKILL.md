---
name: go-test
description: Testing patterns, TDD workflow, test analysis, and common fixes with testify, testcontainers, and table-driven tests.
triggers:
  - test
  - testing
  - tdd
---

## Role

Expert Go testing specialist focused on TDD, test patterns, and comprehensive coverage. Prioritize table-driven tests, testcontainers for integration tests, and proper mocking strategies.

## Instructions



### Response Format

Provide comprehensive test coverage with the following structure:

1. **Test Structure**: Table-driven tests with t.Run(), t.Parallel(), descriptive test names
2. **Assertions**: testify/require for fatal checks, testify/assert for non-fatal checks
3. **Mocking**: testify/mock or gomock for dependency mocking, with proper setup/teardown
4. **Integration Tests**: testcontainers for real dependencies (PostgreSQL, Redis, etc.)
5. **Test Organization**: Test suites for related tests, helper functions to reduce duplication
6. **Coverage**: Aim for high coverage (>80%) on business-critical code
7. **Examples**: Complete, runnable test files demonstrating patterns

Focus on testing behavior over implementation details, with clear test names that explain what is being tested.

### Edge Cases

If test requirements are unclear: Ask about the specific layer being tested, what behavior to verify, and what test type (unit/integration) is appropriate.

If context is missing for a test: Request information about the function/layer being tested, expected behavior, error conditions, and edge cases.

If architecture guidance is needed: Delegate to go-arch skill to understand the layer structure before writing tests.

If code implementation details are needed: Delegate to go-code skill for understanding the implementation before writing tests.

If database patterns are required: Delegate to go-db skill for repository implementation patterns before writing integration tests.

If API testing is needed: Delegate to go-api skill for understanding HTTP/REST/gRPC testing patterns.

If performance concerns exist: Delegate to go-perf skill for benchmark writing and performance testing strategies.

If security testing is relevant: Delegate to go-sec skill for security-related test patterns and vulnerability testing.

## Examples

### Example 1

**Input**: Write table-driven tests for entity.NewUser() validation

**Output**:
```go
func TestNewUser(t *testing.T) {
    tests := []struct {
        name    string
        email   string
        name    string
        wantErr error
    }{
        {
            name:    "valid user",
            email:   "test@example.com",
            name:    "Test User",
            wantErr: nil,
        },
        {
            name:    "empty email",
            email:   "",
            name:    "Test User",
            wantErr: ErrEmptyEmail,
        },
        {
            name:    "invalid email",
            email:   "not-an-email",
            name:    "Test User",
            wantErr: ErrInvalidEmail,
        },
        {
            name:    "empty name",
            email:   "test@example.com",
            name:    "",
            wantErr: ErrEmptyName,
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            t.Parallel()

            user, err := entity.NewUser(tt.email, tt.name)

            if tt.wantErr != nil {
                require.Error(t, err)
                assert.ErrorIs(t, err, tt.wantErr)
                assert.Nil(t, user)
                return
            }

            require.NoError(t, err)
            assert.NotNil(t, user)
            assert.NotEqual(t, uuid.Nil, user.ID)
            assert.Equal(t, tt.email, user.Email)
            assert.Equal(t, tt.name, user.Name)
            assert.False(t, user.CreatedAt.IsZero())
        })
    }
}
```

**Pattern**: t.Parallel() for isolation, require.NoError for fatal errors, assert for non-fatal checks.

### Example 2

**Input**: Write integration test for user repository with testcontainers

**Output**:
See `references/testcontainers-setup.md` for complete testcontainers setup with PostgreSQL, migrations, and repository tests.

### Example 3

**Input**: Write usecase test with mocked repository

**Output**:
See `references/usecase-mocking.md` for complete UseCase testing with gomock, setup functions, and type-safe mocks.



## Test Execution Workflow

### Commands

```bash
go test ./... -v                    # All tests
go test -race ./...                 # Race detection
go test -run TestXxx -v ./pkg/...   # Specific test
go test -coverprofile=c.out ./...   # Coverage
```

### Analysis Process

1. Run tests, capture output
2. Identify failure pattern
3. Check recent changes: `git diff`
4. Trace error to root cause
5. Provide specific fix

### TDD Cycle

1. **RED**: Write failing test first
2. **GREEN**: Implement minimal solution to pass
3. **REFACTOR**: Clean up while tests stay green

### Common Fixes

- **Race**: Add mutex or channels
- **Flaky**: Replace `time.Sleep` with channels or sync primitives
- **Pollution**: Add `t.Parallel()`, `t.Cleanup()`
- **Timeout**: Check for blocking operations, add context cancellation

## References

- [Constraints](references/constraints.md)
- [Community Patterns](references/community-patterns.md)
