---
name: go-table-driven-tests
description: >
  Use this when writing unit tests for handlers, services, or repositories,
  structuring multi-scenario test cases for a single function, or setting up
  per-test gomock expectations. Covers test struct shape, t.Run subtests,
  t.Cleanup, t.Parallel, case naming, require vs assert, and gomock per-test
  controller setup.
  Triggers: table-driven, t.Run, t.Cleanup, t.Parallel, subtests, require, assert.
---



# Table-Driven Tests

Standardizes unit test structure across all microservices. Every handler,
service method, and repository function uses table-driven tests with
consistent naming, assertions, and mock setup.

## When to Activate
- When writing unit tests for handlers, services, or repositories
- When structuring test cases for a function with multiple scenarios
- When setting up gomock expectations per test case
- Used by: test-generator, code-generator, simulated-qa-engineer

## Test Struct Definition

Define a struct with name, inputs, expected output, and error flag.

```go
func TestCreateUser(t *testing.T) {
    tests := []struct {
        name      string
        input     CreateUserRequest
        setupMock func(m *mocks.MockUserRepository)
        wantErr   bool
        wantCode  errors.Code
    }{
        // test cases go here
    }
    for _, tc := range tests {
        t.Run(tc.name, func(t *testing.T) {
            // test body
        })
    }
}
```

## Subtest Loop Pattern

```go
for _, tc := range tests {
    t.Run(tc.name, func(t *testing.T) {
        ctrl := gomock.NewController(t)
        mockRepo := mocks.NewMockUserRepository(ctrl)

        if tc.setupMock != nil {
            tc.setupMock(mockRepo)
        }

        svc := service.NewUserService(mockRepo)
        got, err := svc.Create(context.Background(), tc.input)

        if tc.wantErr {
            require.Error(t, err)
            var appErr *apperrors.AppError
            require.ErrorAs(t, err, &appErr)
            assert.Equal(t, tc.wantCode, appErr.Code)
            return
        }
        require.NoError(t, err)
        assert.Equal(t, tc.input.Email, got.Email)
    })
}
```

## Setup, Teardown, and Parallel

Use `t.Cleanup` for deterministic teardown (runs in reverse registration order).
Use `t.Parallel()` only when test cases share no mutable state.

```go
func TestCalculatePrice_Scenarios(t *testing.T) {
    t.Parallel()
    tests := []struct {
        name string; quantity int; price, want float64
    }{
        {"single item", 1, 10.0, 10.0},
        {"bulk discount", 100, 10.0, 900.0},
    }
    for _, tc := range tests {
        t.Run(tc.name, func(t *testing.T) {
            t.Parallel()
            got := pricing.Calculate(tc.quantity, tc.price)
            assert.InDelta(t, tc.want, got, 0.01)
        })
    }
}
```

Do NOT use `t.Parallel()` when tests share a database, modify package-level variables, or depend on execution order.

## Naming Convention

Format: `Test<Function>_<Scenario>_<Expected>` for top-level functions.
Within table-driven tests, use lowercase descriptive `tc.name` values.

```go
func TestCreateUser_DuplicateEmail_ReturnsConflict(t *testing.T) { ... }
func TestGetUser_NotFound_Returns404(t *testing.T) { ... }
// tc.name examples: "valid input creates user", "duplicate email returns conflict"
```

## Error Assertions

```go
// Assert error exists
require.Error(t, err)

// Assert specific error type
var appErr *apperrors.AppError
require.ErrorAs(t, err, &appErr)
assert.Equal(t, apperrors.CodeConflict, appErr.Code)

// Assert sentinel error
assert.ErrorIs(t, err, domain.ErrAlreadyClosed)

// Assert no error
require.NoError(t, err)
```

## Full Example: 5 Test Cases

```go
func TestCreateUser(t *testing.T) {
    tenantID := uuid.New()
    ctx := tenant.WithID(context.Background(), tenantID)
    tests := []struct {
        name      string
        input     service.CreateUserInput
        setupMock func(m *mocks.MockUserRepository)
        wantErr   bool
        wantCode  apperrors.Code
    }{
        {"happy path creates user", service.CreateUserInput{Email: "new@example.com", Name: "New"},
            func(m *mocks.MockUserRepository) {
                m.EXPECT().FindByEmail(gomock.Any(), tenantID, "new@example.com").Return(nil, apperrors.NotFound("user", ""))
                m.EXPECT().Create(gomock.Any(), gomock.Any()).Return(nil)
            }, false, ""},
        {"empty email returns validation error", service.CreateUserInput{Email: "", Name: "X"},
            func(m *mocks.MockUserRepository) {}, true, apperrors.CodeValidation},
        {"lookup miss still creates", service.CreateUserInput{Email: "ghost@example.com", Name: "Ghost"},
            func(m *mocks.MockUserRepository) {
                m.EXPECT().FindByEmail(gomock.Any(), tenantID, "ghost@example.com").Return(nil, apperrors.NotFound("user", ""))
                m.EXPECT().Create(gomock.Any(), gomock.Any()).Return(nil)
            }, false, ""},
        {"duplicate email returns conflict", service.CreateUserInput{Email: "dup@example.com", Name: "Dup"},
            func(m *mocks.MockUserRepository) {
                m.EXPECT().FindByEmail(gomock.Any(), tenantID, "dup@example.com").Return(&model.User{}, nil)
            }, true, apperrors.CodeConflict},
        {"repo failure returns internal error", service.CreateUserInput{Email: "fail@example.com", Name: "Fail"},
            func(m *mocks.MockUserRepository) {
                m.EXPECT().FindByEmail(gomock.Any(), tenantID, "fail@example.com").Return(nil, apperrors.NotFound("user", ""))
                m.EXPECT().Create(gomock.Any(), gomock.Any()).Return(fmt.Errorf("connection refused"))
            }, true, apperrors.CodeInternal},
    }
    for _, tc := range tests {
        t.Run(tc.name, func(t *testing.T) {
            ctrl := gomock.NewController(t)
            mockRepo := mocks.NewMockUserRepository(ctrl)
            tc.setupMock(mockRepo)
            svc := service.NewUserService(mockRepo)
            user, err := svc.CreateUser(ctx, tc.input)
            if tc.wantErr {
                require.Error(t, err)
                var appErr *apperrors.AppError
                require.ErrorAs(t, err, &appErr)
                assert.Equal(t, tc.wantCode, appErr.Code)
                return
            }
            require.NoError(t, err)
            assert.Equal(t, tc.input.Email, user.Email)
        })
    }
}
```

## Common Mistakes

1. **Forgetting `setupMock` for the happy path** -- Even happy-path cases need mock expectations, otherwise `gomock` may not verify calls were made.
2. **Using `t.Fatal` inside goroutines** -- `t.Fatal` calls `runtime.Goexit`, which only exits the current goroutine. Use channels or `t.Error` + explicit return instead.
3. **Sharing `gomock.Controller` across parallel subtests** -- Create a new controller per subtest to avoid data races.
4. **Not testing the error code, only `wantErr`** -- Knowing "an error occurred" is not enough. Assert the specific `AppError.Code` to verify correct error classification.
5. **Hardcoding UUIDs** -- Generate fresh UUIDs with `uuid.New()` per test to avoid collision and make tests deterministic.
