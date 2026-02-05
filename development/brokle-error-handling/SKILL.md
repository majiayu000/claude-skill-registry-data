---
name: brokle-error-handling
description: Use this skill when implementing, reviewing, or debugging error handling in the Brokle codebase. This includes repository error mapping, service layer AppError constructors, handler response mapping, domain alias imports, or understanding the industrial error handling flow.
---

# Brokle Error Handling Skill

Expert guidance for implementing industrial error handling patterns across all layers.

## Industrial Error Handling Pattern

**Core Flow**:
```
Repository (Domain Errors) → Service (AppErrors) → Handler (HTTP Response)
```

**Three-Layer Clean Architecture**:
- **Repository Layer**: Domain errors with context wrapping
- **Service Layer**: AppError constructors for business logic
- **Handler Layer**: Centralized `response.Error()` handling
- **Zero Logging**: Core services focus on pure business logic

## Layer Responsibilities

| Layer | Responsibility | Error Pattern | Example |
|-------|---------------|---------------|---------|
| **Repository** | Data access, domain error wrapping | `fmt.Errorf("context: %w", domainError)` | `fmt.Errorf("get user by ID %s: %w", id, userDomain.ErrNotFound)` |
| **Service** | Business logic, AppError constructors | `appErrors.NewNotFoundError()` | `return nil, appErrors.NewNotFoundError("User not found")` |
| **Handler** | HTTP transport, response mapping | `response.Error(c, err)` | Automatic HTTP status code mapping |

## Domain Alias Pattern (MANDATORY)

```go
// ✅ Correct - Professional domain alias pattern
import (
    "context"
    "fmt"

    "gorm.io/gorm"

    authDomain "brokle/internal/core/domain/auth"
    orgDomain "brokle/internal/core/domain/organization"
    userDomain "brokle/internal/core/domain/user"
    "brokle/pkg/ulid"
)

// ❌ Incorrect - Direct domain imports
import (
    "brokle/internal/core/domain/auth"
)
```

**Standard Aliases**:
| Domain | Alias | Usage |
|--------|-------|--------|
| auth | `authDomain` | `authDomain.User`, `authDomain.ErrNotFound` |
| organization | `orgDomain` | `orgDomain.Organization` |
| user | `userDomain` | `userDomain.User` |
| billing | `billingDomain` | `billingDomain.Subscription` |
| observability | `obsDomain` | `obsDomain.Trace` |

## Repository Layer Pattern

```go
package auth

import (
    "context"
    "fmt"

    "gorm.io/gorm"

    authDomain "brokle/internal/core/domain/auth"
    "brokle/pkg/ulid"
)

type userRepository struct {
    db *gorm.DB
}

// ✅ Correct pattern
func (r *userRepository) GetByID(ctx context.Context, id ulid.ULID) (*authDomain.User, error) {
    var user authDomain.User
    err := r.db.WithContext(ctx).Where("id = ?", id).First(&user).Error
    if err != nil {
        if errors.Is(err, gorm.ErrRecordNotFound) {  // ✅ Standardized pattern
            return nil, fmt.Errorf("get user by ID %s: %w", id, authDomain.ErrNotFound)
        }
        return nil, fmt.Errorf("database query failed for user ID %s: %w", id, err)
    }
    return &user, nil
}

// ✅ Correct pattern
func (r *userRepository) Create(ctx context.Context, user *authDomain.User) error {
    if err := r.db.WithContext(ctx).Create(user).Error; err != nil {
        return fmt.Errorf("create user %s: %w", user.Email, err)
    }
    return nil
}
```

**Repository Requirements** (`internal/infrastructure/repository/user/user_repository.go:37-54`):

✅ **Required Pattern**:
```go
// 1. Professional domain alias imports
import (
    "errors"
    "fmt"
    "gorm.io/gorm"
    userDomain "brokle/internal/core/domain/user"
)

// 2. GORM error checking with errors.Is() (STANDARD PATTERN)
func (r *userRepository) GetByID(ctx context.Context, id ulid.ULID) (*userDomain.User, error) {
    var u userDomain.User
    err := r.db.WithContext(ctx).Where("id = ? AND deleted_at IS NULL", id).First(&u).Error
    if err != nil {
        if errors.Is(err, gorm.ErrRecordNotFound) {  // ✅ Standardized across all repos
            return nil, fmt.Errorf("get user by ID %s: %w", id, userDomain.ErrNotFound)
        }
        return nil, fmt.Errorf("database query failed for user ID %s: %w", id, err)
    }
    return &u, nil
}
```

**Standard**: All repositories use `errors.Is()` for GORM error checking (standardized across codebase for wrapped error compatibility).

## Service Layer Pattern

```go
package auth

import (
    "context"
    "errors"

    authDomain "brokle/internal/core/domain/auth"
    "brokle/pkg/apperrors"
    "brokle/pkg/ulid"
)

type userService struct {
    userRepo authDomain.UserRepository
}

// ✅ Correct pattern
func (s *userService) GetUser(ctx context.Context, id ulid.ULID) (*GetUserResponse, error) {
    user, err := s.userRepo.GetByID(ctx, id)
    if err != nil {
        // Check for domain errors and convert to AppErrors
        if errors.Is(err, authDomain.ErrNotFound) {
            return nil, appErrors.NewNotFoundError("User")  // resource string
        }
        return nil, appErrors.NewInternalError("Failed to retrieve user", err)
    }

    return &GetUserResponse{User: user}, nil
}

// ✅ Correct pattern with validation
func (s *userService) CreateUser(ctx context.Context, req *CreateUserRequest) (*CreateUserResponse, error) {
    // Input validation - NewValidationError(message, details string)
    if err := req.Validate(); err != nil {
        return nil, appErrors.NewValidationError("Invalid user data", err.Error())
    }

    // Check for existing user
    existingUser, err := s.userRepo.GetByEmail(ctx, req.Email)
    if err != nil && !errors.Is(err, authDomain.ErrNotFound) {
        return nil, appErrors.NewInternalError("Failed to check existing user", err)
    }
    if existingUser != nil {
        return nil, appErrors.NewConflictError("User already exists with this email")
    }

    // Create user
    user := &authDomain.User{
        ID:    ulid.New(),
        Email: req.Email,
        Name:  req.Name,
    }

    if err := s.userRepo.Create(ctx, user); err != nil {
        return nil, appErrors.NewInternalError("Failed to create user", err)
    }

    return &CreateUserResponse{User: user}, nil
}
```

**Service Requirements**:

✅ **Required** (with exact signatures):
```go
// 1. AppError constructors for business logic
if errors.Is(err, userDomain.ErrNotFound) {
    return nil, appErrors.NewNotFoundError("User")  // resource string
}

// 2. Validation errors (message, details string)
return nil, appErrors.NewValidationError("Invalid email format", "email must be valid")

// 3. Internal errors (message string, err error)
return nil, appErrors.NewInternalError("Failed to process request", err)
```

❌ **Prohibited**:
```go
// Don't use fmt.Errorf or errors.New in services
return nil, fmt.Errorf("user not found")  // ❌

// Don't include logging in core services
log.Error("Failed to create user")  // ❌
```

**AppError Constructors** (see `pkg/errors/errors.go:86-136` for complete list):

**Common constructors**:
```go
appErrors.NewValidationError(message, details string) *AppError
appErrors.NewNotFoundError(resource string) *AppError
appErrors.NewConflictError(message string) *AppError
appErrors.NewUnauthorizedError(message string) *AppError
appErrors.NewForbiddenError(message string) *AppError
appErrors.NewInternalError(message string, err error) *AppError
appErrors.NewRateLimitError(message string) *AppError

// Helper
appErrors.IsAppError(err error) (*AppError, bool)
```

**Reference**: See `pkg/errors/errors.go` for all constructors (BadRequest, ServiceUnavailable, NotImplemented, PaymentRequired, QuotaExceeded, AIProvider) and exact signatures

## Handler Layer Pattern

```go
package http

import (
    "github.com/gin-gonic/gin"

    authDomain "brokle/internal/core/domain/auth"
    "brokle/pkg/response"
    "brokle/pkg/ulid"
    "brokle/pkg/apperrors"
)

type userHandler struct {
    userService authDomain.UserService
}

// ✅ Correct pattern
func (h *userHandler) GetUser(c *gin.Context) {
    // 1. Validate input
    userID := c.Param("id")
    id, err := ulid.Parse(userID)
    if err != nil {
        response.Error(c, appErrors.NewValidationError("Invalid user ID format", "id must be a valid ULID"))
        return
    }

    // 2. Call service
    resp, err := h.userService.GetUser(c.Request.Context(), id)
    if err != nil {
        response.Error(c, err)  // Automatic HTTP status mapping
        return
    }

    // 3. Return success
    response.Success(c, resp)
}
```

**Handler Requirements**:

✅ **Required**:
```go
// 1. Structured response handling
resp, err := h.service.Method(c, req)
if err != nil {
    response.Error(c, err)  // Automatic status mapping
    return
}
response.Success(c, resp)

// 2. Input validation before service calls
if err := req.Validate(); err != nil {
    response.Error(c, appErrors.NewValidationError("Invalid request", err))
    return
}
```

❌ **Prohibited**:
```go
// Don't inspect or log errors manually
if errors.Is(err, apperrors.ErrNotFound) {  // ❌
    c.JSON(404, gin.H{"error": "Not found"})
}

// Always use response.Error()
response.Error(c, err)  // ✅
```

## HTTP Status Code Mapping

| AppError Type | HTTP Status | Description |
|---------------|-------------|-------------|
| ValidationError | 400 Bad Request | Invalid input data |
| UnauthorizedError | 401 Unauthorized | Authentication required |
| ForbiddenError | 403 Forbidden | Insufficient permissions |
| NotFoundError | 404 Not Found | Resource not found |
| ConflictError | 409 Conflict | Resource already exists |
| RateLimitError | 429 Too Many Requests | Rate limit exceeded |
| InternalError | 500 Internal Server Error | Unexpected server error |

## Standard Error Response Format

```json
{
  "error": {
    "type": "VALIDATION_ERROR",
    "message": "Validation failed",
    "details": {
      "email": "must be a valid email address",
      "password": "must be at least 8 characters"
    },
    "code": "INVALID_INPUT",
    "request_id": "req_01H4XJZQX3EXAMPLE"
  }
}
```

## Best Practices Checklist

**Repository Layer**:
- [ ] Use professional domain alias imports
- [ ] Convert GORM errors to domain errors with context
- [ ] No `errors.New()` or business logic
- [ ] All database operations include error context

**Service Layer**:
- [ ] Use AppError constructors only
- [ ] Convert domain errors to business errors
- [ ] No logging in core services
- [ ] Validate inputs with meaningful error messages

**Handler Layer**:
- [ ] Use `response.Error()` for all error responses
- [ ] Validate input before calling services
- [ ] No business logic in handlers
- [ ] Return appropriate HTTP status codes

## References

- `docs/development/ERROR_HANDLING_GUIDE.md` - Complete industrial patterns
- `docs/development/DOMAIN_ALIAS_PATTERNS.md` - Professional import patterns
- `docs/development/ERROR_HANDLING_QUICK_REFERENCE.md` - Developer cheat sheet
