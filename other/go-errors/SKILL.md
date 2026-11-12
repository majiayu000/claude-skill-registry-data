---
name: go-errors
description: "Use when handling errors in Go: errors.Is, errors.As, error wrapping with fmt.Errorf %w, sentinel errors, typed error trees, panic/recover boundaries. Apply to .go files that return error or import the errors package."
version: 1.0.0
license: MIT
applies_when:
  files_contain:
    "**/*.go": '(errors\.(Is|As|New|Unwrap)|fmt\.Errorf.*%w)'
  language:
    - go
portability:
  level: universal
  tested_on:
    - claude-code
    - codex
  model_dependency: none
  domain_specificity: focused
produces:
  - code
consumes:
  - code
security:
  signature: ""
  sandbox: read-only
  network: none
---

# Go Error Handling Patterns

Go 에러 처리 패턴 및 best practices.

## Quick Reference

```
에러 처리 패턴
    │
    ├─ 에러 래핑 ────> fmt.Errorf("context: %w", err)
    │
    ├─ 에러 체크 ────> errors.Is() / errors.As()
    │
    ├─ Sentinel ────> var ErrNotFound = errors.New(...)
    │
    └─ Custom Type ─> Error() string 구현
```

---

## Error Wrapping

컨텍스트를 추가하여 에러 추적을 용이하게 합니다.

```go
// Good - 컨텍스트 추가
if err != nil {
    return fmt.Errorf("failed to get user %d: %w", userID, err)
}

// Bad - 컨텍스트 없음
if err != nil {
    return err
}
```

## Error Checking

```go
// errors.Is: 특정 에러 값 체크
if errors.Is(err, sql.ErrNoRows) {
    return nil, ErrUserNotFound
}

// errors.As: 에러 타입 체크
var validationErr *ValidationError
if errors.As(err, &validationErr) {
    return nil, validationErr
}
```

## Sentinel Errors

```go
// internal/domain/errors.go
var (
    ErrUserNotFound = errors.New("user not found")
    ErrInvalidInput = errors.New("invalid input")
    ErrUnauthorized = errors.New("unauthorized")
)
```

## Custom Error Types

```go
type ValidationError struct {
    Field   string
    Message string
}

func (e *ValidationError) Error() string {
    return fmt.Sprintf("validation error: %s - %s", e.Field, e.Message)
}

// 사용 예시
func ValidateUser(u *User) error {
    if u.Email == "" {
        return &ValidationError{Field: "email", Message: "required"}
    }
    return nil
}
```

## Anti-patterns

| Mistake | Correct | Why |
|---------|---------|-----|
| `_ = err` | `if err != nil { ... }` | 에러 무시 금지 |
| `return err` | `return fmt.Errorf("context: %w", err)` | 컨텍스트 추가 |
| `err.Error() == "..."` | `errors.Is(err, target)` | 문자열 비교 금지 |
| `err.(*MyError)` | `errors.As(err, &target)` | 래핑된 에러도 처리 |
