---
name: go-tdd-patterns
description: >
  Use this for the Go-specific realization of the SKELETON→RED→GREEN→REFACTOR
  TDD cycle — interface skeletons returning `errNotImplemented` stubs,
  table-driven failing tests with `*testing.T` + `t.Run` + `t.Parallel`, gomock
  controller setup, assertion-first test shape, `errors.Is`/`require.NoError`
  conventions, and compile-time interface assertions via `var _ I = (*T)(nil)`.
  Pairs with the language-neutral `tdd-patterns` skill (cycle + agent
  coordination); this skill is the Go syntax layer.
  Triggers: testing.T, t.Run, t.Parallel, t.Cleanup, gomock.NewController, errNotImplemented, table-driven, *_test.go, errors.Is, require.NoError, var _ Interface.
version: 1.0.0
last-evolved-in-run: v0.6.0-rc.0-sanitization
status: stable
tags: [go, tdd, testing]
---

# go-tdd-patterns (v1.0.0)

## Scope

Realizes the cycle defined in shared-core `tdd-patterns` for Go targets. The agent coordination (which agent writes the skeleton, which writes the RED test, etc.) is language-neutral and lives there. Everything below is Go syntax.

## SKELETON — compilable stubs that tests can import

```go
// internal/ports/repository.go
package ports

import "context"

// Repository defines persistence operations for an entity.
type Repository[T any] interface {
    Create(ctx context.Context, entity *T) (*T, error)
    GetByID(ctx context.Context, id string) (*T, error)
}
```

```go
// internal/application/service.go
package application

import (
    "context"
    "errors"
)

var errNotImplemented = errors.New("not implemented")

type Service struct {
    repo ports.Repository[domain.Entity]
}

func NewService(repo ports.Repository[domain.Entity]) *Service {
    return &Service{repo: repo}
}

// CreateEntity creates an entity. STUB — returns not-implemented error.
func (s *Service) CreateEntity(ctx context.Context, cmd CreateEntityCommand) (*domain.Entity, error) {
    return nil, errNotImplemented
}
```

Skeleton rules:
- All exported interfaces fully defined (every method signature)
- All structs have correct fields and tags
- Constructors return real instances
- Method stubs return `nil, errNotImplemented` or zero values
- Compile-time interface assertion: `var _ ports.Repository[domain.Entity] = (*Impl)(nil)` somewhere in the impl package — catches missing methods at build time

## RED — assertion-first failing tests

```go
func TestCreateEntity_ValidInput_ReturnsEntityWithID(t *testing.T) {
    ctrl := gomock.NewController(t)
    defer ctrl.Finish()

    mockRepo := mocks.NewMockRepository(ctrl)
    mockRepo.EXPECT().
        Create(gomock.Any(), gomock.Any()).
        DoAndReturn(func(ctx context.Context, e *domain.Entity) (*domain.Entity, error) {
            assert.NotEmpty(t, e.ID, "ID should be generated before persistence")
            return e, nil
        })

    svc := application.NewService(mockRepo)
    entity, err := svc.CreateEntity(context.Background(), application.CreateEntityCommand{
        Name: "test",
    })

    require.NoError(t, err)
    require.NotNil(t, entity)
    assert.NotEmpty(t, entity.ID)
}
```

Conventions:
- Start with what you want to assert; work backward to setup.
- `require` short-circuits the test on failure; `assert` continues. Use `require` for preconditions, `assert` for behavior verification.
- `gomock` controller per test; `defer ctrl.Finish()` (or `t.Cleanup(ctrl.Finish)`).
- Use `gomock.Any()` for arguments you don't care about; `DoAndReturn` to verify shape and return.

## RED — table-driven tests

```go
func TestCreateEntity_Validation(t *testing.T) {
    tests := []struct {
        name    string
        cmd     application.CreateEntityCommand
        wantErr bool
        errType error // sentinel for errors.Is match
    }{
        {"empty name", application.CreateEntityCommand{Name: ""}, true, domain.ErrInvalidName},
        {"valid", application.CreateEntityCommand{Name: "x"}, false, nil},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            t.Parallel()
            ctrl := gomock.NewController(t)
            mockRepo := mocks.NewMockRepository(ctrl)
            if !tt.wantErr {
                mockRepo.EXPECT().Create(gomock.Any(), gomock.Any()).
                    Return(&domain.Entity{ID: "e1"}, nil)
            }

            svc := application.NewService(mockRepo)
            _, err := svc.CreateEntity(context.Background(), tt.cmd)

            if tt.wantErr {
                require.Error(t, err)
                if tt.errType != nil {
                    assert.True(t, errors.Is(err, tt.errType),
                        "expected %v, got %v", tt.errType, err)
                }
            } else {
                require.NoError(t, err)
            }
        })
    }
}
```

`t.Parallel()` inside a subtest opts the subtest into parallel execution. Race-detector friendly when each subtest owns its own `gomock.Controller`. Don't share state across subtests.

## GREEN — implementation rules

After tests are RED, code-generator reads ALL test files and writes the minimum impl to make them pass:

- Read every `*_test.go` in the package first
- If a test expects a specific sentinel via `errors.Is`, return that exact sentinel (or wrap it with `fmt.Errorf("...: %w", sentinel)`)
- If a test asserts a generated UUID is non-empty, generate one (don't return zero-value)
- Run `go test ./... -race -count=1` after each significant change
- Don't add behavior that isn't tested

## Anti-patterns

**1. Weak assertions that pass on stubs.** `func TestX(t *testing.T) { svc.Do(); }` — no assertion, passes immediately. Always assert at least one observable outcome.

**2. Testing implementation details.** `mockRepo.EXPECT().Create(gomock.Eq(specificStruct))` — brittle to refactor. Use `DoAndReturn` to assert behavioral properties of the argument, not exact equality.

**3. Skipping error-path tests.** Every error path the impl has must have a test that exercises it. If you can't write the test, you don't know the behavior.

## Cross-references

- shared-core `tdd-patterns` — agent cycle and orchestration (what this skill realizes)
- `go-table-driven-tests` — deeper conventions on table layout, `t.Cleanup`, `t.Parallel`
- `go-mock-patterns` — gomock vs fake vs stub decision tree
- `go-error-handling-patterns` — sentinel definition + `errors.Is` discipline
- `go-testing-patterns` — broader Go testing toolkit
