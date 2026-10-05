---
name: go-unit-tests
description: Write or fix Go unit tests in this repo. Use when creating/editing *_test.go files, adding test coverage for Go code (usecases, repositories, services, handlers), or when the user asks to write, refactor, or fix Go unit tests. Enforces table-driven tests, testify + testify/mock, AAA, and the conventions below.
---

# Go Unit Tests

Authoritative style for unit tests in this codebase. Follow it exactly — these rules
override generic Go testing habits. Existing test files may predate this style; when you
touch a test, bring it into compliance.

## When to use

- Writing tests for a new function/method/usecase/repository.
- Adding cases to existing tests or fixing failing tests.
- Reviewing test code for style compliance.

## Non-negotiable rules

**Structure**
- Test package is `package <feature>_test` (external test package), placed in the **same
  directory** as the code under test.
- Follow the Uber Go Style Guide.
- One table-driven test per function under test. Use the subtest map below — never write
  sequential standalone assertions for variations of the same function.
- **No conditional statements in tests** — no `if`, `switch`, or branching in the test body.
  Every case goes through the identical Arrange/Act/Assert path. If a case needs different
  behavior, encode it in the table, not in control flow.

**Table format**
- The table is `map[string]struct{...}` where the **key is the test name**.
- Test names are descriptive: `should ... when ...` / `expects ... when ...`.
  e.g. `"should return ErrNotFound when movement does not exist"`.
- Group struct fields into three commented sections and predeclare named types for them:

  ```go
  type (
      input struct { /* args passed to the function */ }
      expected struct { /* expectedOutput, expectedErr, ... */ }
  )
  ```

  The case struct holds: `// input`, `// mocks` (a `mockSetup` closure), `// expected`.
- Always put expected values in the table (`expected.output`, `expected.err`), never inline
  in the Assert section.

**AAA pattern**
- Mark every section with a comment: `// Arrange`, `// Act`, `// Assert`.
- Group multiple locals in Arrange with a single `var (...)` block.

**Mocks (testify/mock)**
- Use `testify/mock`. Define mocks in `mock_test.go` in the same package.
- **Before creating a mock, check whether it already exists** (`mock_test.go`, `mocks.go`,
  or a `mock.go` next to the interface) and reuse it.
- Create mock instances with the address-of operator: `mockRepo := &MockRepo{}`.
- **Do not use `mock.Anything`.** Match on the real expected argument values.
- In the mock method, **ignore `ctx`** when calling `m.Called(...)` — pass only the
  meaningful args: `func (m *Mock) X(_ context.Context, id uuid.UUID) ... { args := m.Called(id); ... }`.
- Always call `mockX.AssertExpectations(t)` (defer it right after constructing the mock).

**Assertions (testify)**
- Use `testify/assert`.
- Compare errors with `assert.ErrorIs(t, err, tc.expected.err)` **always** — including the
  success case. `errors.Is(nil, nil)` is true, so a single uniform call covers both success
  and failure **without any `if`**. Never write `assert.NoError` / `assert.Nil(err)` /
  `err == nil`.
- Use `assert.AnError` (testify's sentinel) when a test needs an arbitrary error from a mock.
- Naming: `expectedOutput`, `expectedErr`, etc.

## Canonical template

Copy this and adapt. It already encodes every rule above.

```go
package usecase_test

import (
	"context"
	"testing"

	"github.com/google/uuid"
	"github.com/stretchr/testify/assert"

	"personal-finance/internal/domain"
	"personal-finance/internal/usecase"
)

// fixtureID is a shared test fixture (declare real fixtures in a fixture package).
var fixtureID = uuid.New()

func TestService_GetByID(t *testing.T) {
	type (
		input struct {
			id uuid.UUID
		}
		expected struct {
			output domain.Movement
			err    error
		}
	)

	tests := map[string]struct {
		// input
		input input
		// mocks
		mockSetup func(mockRepo *MockMovementRepository)
		// expected
		expected expected
	}{
		"should return movement when it exists": {
			input: input{id: fixtureID},
			mockSetup: func(mockRepo *MockMovementRepository) {
				mockRepo.On("FindByID", fixtureID).
					Return(domain.Movement{ID: fixtureID}, nil)
			},
			expected: expected{
				output: domain.Movement{ID: fixtureID},
				err:    nil,
			},
		},
		"should return error when repository fails": {
			input: input{id: fixtureID},
			mockSetup: func(mockRepo *MockMovementRepository) {
				mockRepo.On("FindByID", fixtureID).
					Return(domain.Movement{}, assert.AnError)
			},
			expected: expected{
				output: domain.Movement{},
				err:    assert.AnError,
			},
		},
	}

	for name, tc := range tests {
		t.Run(name, func(t *testing.T) {
			// Arrange
			var (
				mockRepo = &MockMovementRepository{}
				svc      = usecase.NewService(mockRepo)
			)
			defer mockRepo.AssertExpectations(t)
			tc.mockSetup(mockRepo)

			// Act
			output, err := svc.GetByID(context.Background(), tc.input.id)

			// Assert
			assert.ErrorIs(t, err, tc.expected.err)
			assert.Equal(t, tc.expected.output, output)
		})
	}
}
```

## Mock template (`mock_test.go`)

```go
package usecase_test

import (
	"context"

	"github.com/google/uuid"
	"github.com/stretchr/testify/mock"

	"personal-finance/internal/domain"
)

type MockMovementRepository struct {
	mock.Mock
}

// ctx is ignored in m.Called.
func (m *MockMovementRepository) FindByID(_ context.Context, id uuid.UUID) (domain.Movement, error) {
	args := m.Called(id)
	return args.Get(0).(domain.Movement), args.Error(1)
}
```

## Anti-patterns (reject these)

| Don't | Do |
|---|---|
| `if tc.expectedErr != nil { assert.Error(...) }` | `assert.ErrorIs(t, err, tc.expected.err)` (uniform, no `if`) |
| `assert.NoError(t, err)` / `err == nil` | `assert.ErrorIs(t, err, tc.expected.err)` with `err: nil` in table |
| `mockRepo.On("X", mock.Anything)` | match the real arg: `mockRepo.On("X", fixtureID)` |
| `m.Called(ctx, id)` in the mock method | `m.Called(id)` — ignore ctx |
| `errors.New("boom")` for a throwaway error | `assert.AnError` |
| New mock when one already exists | grep first, reuse |
| Slice-of-structs table | `map[string]struct{...}` keyed by name |

## Run & verify

```bash
go test ./internal/path/to/package/...   # single package
make test                                # full suite with race + coverage
```

Always run the relevant package's tests after writing them and confirm they pass before
reporting done.
