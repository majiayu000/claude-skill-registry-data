---
name: go-testing
description: "Use when writing or refactoring Go tests: table-driven tests, t.Run subtests, testify/require, testcontainers integration tests, golden files, t.Parallel safety, race detector. Skip for non-_test.go files."
version: 1.0.0
license: MIT
applies_when:
  files_present:
    - "**/*_test.go"
  files_contain:
    "**/*_test.go": '(testing\.[TBM]|stretchr/testify|testcontainers|^func Test[A-Z])'
  language:
    - go
  frameworks:
    - go-test
portability:
  level: universal
  tested_on:
    - claude-code
    - codex
  model_dependency: none
  domain_specificity: focused
produces:
  - unit-test
  - integration-test
consumes:
  - code
security:
  signature: ""
  sandbox: read-only
  network: none
---

# Go Testing Patterns

Go 테스트 패턴 및 best practices.

## Quick Reference

```
테스트 패턴 선택
    │
    ├─ 단위 테스트 ────> Table-Driven + t.Run()
    │
    ├─ Mock 생성 ─────> gomock 또는 mockery
    │
    ├─ HTTP 테스트 ───> httptest + gin.TestMode
    │
    └─ 커버리지 ──────> go test -cover ./...
```

---

## Table-Driven Tests

```go
func TestUserService_GetByID(t *testing.T) {
    tests := []struct {
        name    string
        userID  int64
        mockFn  func(*mocks.MockUserRepository)
        want    *domain.User
        wantErr error
    }{
        {
            name:   "success",
            userID: 1,
            mockFn: func(m *mocks.MockUserRepository) {
                m.EXPECT().FindByID(gomock.Any(), int64(1)).
                    Return(&domain.User{ID: 1, Name: "test"}, nil)
            },
            want:    &domain.User{ID: 1, Name: "test"},
            wantErr: nil,
        },
        {
            name:   "not found",
            userID: 999,
            mockFn: func(m *mocks.MockUserRepository) {
                m.EXPECT().FindByID(gomock.Any(), int64(999)).
                    Return(nil, domain.ErrUserNotFound)
            },
            want:    nil,
            wantErr: domain.ErrUserNotFound,
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            ctrl := gomock.NewController(t)
            defer ctrl.Finish()

            mockRepo := mocks.NewMockUserRepository(ctrl)
            tt.mockFn(mockRepo)

            svc := service.NewUserService(mockRepo)
            got, err := svc.GetByID(context.Background(), tt.userID)

            if !errors.Is(err, tt.wantErr) {
                t.Errorf("GetByID() error = %v, wantErr %v", err, tt.wantErr)
                return
            }
            if !reflect.DeepEqual(got, tt.want) {
                t.Errorf("GetByID() = %v, want %v", got, tt.want)
            }
        })
    }
}
```

## Naming Convention

```go
// Pattern: Test{Type}_{Method}[_{Scenario}]
func TestUserService_GetByID(t *testing.T) {}
func TestUserService_GetByID_NotFound(t *testing.T) {}
func TestUserHandler_GetUser_InvalidID(t *testing.T) {}
```

## Test Commands

```bash
# Run all tests
go test ./...

# With coverage
go test -cover ./...

# Coverage report
go test -coverprofile=coverage.out ./...
go tool cover -html=coverage.out

# Specific package
go test ./internal/service/...

# Specific test
go test -run TestUserService_GetByID ./...

# Verbose
go test -v ./...

# Race detection
go test -race ./...
```

## Mock Generation

```bash
# gomock
mockgen -source=internal/repository/user_repository.go \
    -destination=internal/mocks/mock_user_repository.go

# mockery
mockery --name=UserRepository --dir=internal/repository --output=internal/mocks
```

## HTTP Handler Testing

```go
func TestUserHandler_GetUser(t *testing.T) {
    gin.SetMode(gin.TestMode)

    ctrl := gomock.NewController(t)
    defer ctrl.Finish()

    mockService := mocks.NewMockUserService(ctrl)
    mockService.EXPECT().GetByID(gomock.Any(), int64(1)).
        Return(&domain.User{ID: 1, Name: "test"}, nil)

    handler := NewUserHandler(mockService, zap.NewNop())

    w := httptest.NewRecorder()
    c, _ := gin.CreateTestContext(w)
    c.Params = gin.Params{{Key: "id", Value: "1"}}

    handler.GetUser(c)

    assert.Equal(t, http.StatusOK, w.Code)
}
```

## Test File Structure

```
internal/
├── service/
│   ├── user_service.go
│   └── user_service_test.go    # Same directory
└── handler/
    ├── user_handler.go
    └── user_handler_test.go
```

## Anti-patterns

| Mistake | Correct | Why |
|---------|---------|-----|
| Test without subtests | Use `t.Run()` | 개별 케이스 격리 |
| Shared state between tests | Each test independent | 테스트 순서 의존성 제거 |
| No error case testing | Test both success and failure | 에러 경로도 검증 |
| Hardcoded time values | Use time mocking | 비결정적 테스트 방지 |
