---
name: brokle-backend-dev
description: Use this skill when developing, implementing, or modifying Go backend code for the Brokle platform. This includes creating services, repositories, handlers, domain entities, API endpoints, middleware, workers, or any other Go backend components. Invoke this skill at the start of backend development tasks.
---

# Brokle Backend Development Skill

This skill provides comprehensive guidance for Go backend development following Brokle's scalable monolith architecture with Domain-Driven Design.

## Architecture Overview

### Scalable Monolith with Independent Scaling
- **Separate Binaries**: HTTP server (`cmd/server`) + Background workers (`cmd/worker`)
- **Shared Codebase**: Single codebase with modular DI container
- **Multi-Database Strategy**: PostgreSQL (transactional) + ClickHouse (analytics) + Redis (cache/queues)
- **Domain-Driven Design**: Clean layer separation with domain-driven architecture

### Application Structure
```
internal/
├── core/
│   ├── domain/{domain}/      # Entities, interfaces (see internal/core/domain/)
│   └── services/{domain}/    # Business logic implementations
├── infrastructure/
│   ├── database/
│   │   ├── postgres/repository/
│   │   └── clickhouse/repository/
│   └── repository/           # Main repository layer
├── transport/http/
│   ├── handlers/{domain}/
│   ├── middleware/
│   └── server.go
├── app/                      # DI container
└── workers/                  # Background jobs
```

### Domains

Primary domains in `internal/core/domain/`:
- **auth** - Authentication, sessions, API keys
- **billing** - Usage tracking, subscriptions
- **common** - Shared transaction patterns, utilities
- **gateway** - AI provider routing and management
- **observability** - Traces, spans, quality scores
- **organization** - Multi-tenant org management
- **user** - User management and profiles

**Pattern**: Each domain has entities.go, repository.go, service.go, errors.go
**Reference**: See `internal/core/domain/` directory for complete list and implementation status

## Critical Development Patterns

### 1. Domain Alias Pattern (MANDATORY)

Always use professional domain aliases for imports:

```go
// ✅ Correct
import (
    "context"
    "fmt"

    "gorm.io/gorm"

    authDomain "brokle/internal/core/domain/auth"
    orgDomain "brokle/internal/core/domain/organization"
    userDomain "brokle/internal/core/domain/user"
    "brokle/pkg/ulid"
)

// ❌ Incorrect
import (
    "brokle/internal/core/domain/auth"
)
```

**Standard Domain Aliases**:
| Domain | Alias | Usage |
|--------|-------|--------|
| auth | `authDomain` | `authDomain.User`, `authDomain.ErrNotFound` |
| organization | `orgDomain` | `orgDomain.Organization` |
| user | `userDomain` | `userDomain.User` |
| billing | `billingDomain` | `billingDomain.Subscription` |
| observability | `obsDomain` | `obsDomain.Trace` |

### 2. Industrial Error Handling (MANDATORY)

**Three-Layer Pattern**: Repository (Domain Errors) → Service (AppErrors) → Handler (HTTP Response)

**Repository Layer** (Standard Pattern - `errors.Is()` for GORM):

All repositories use `errors.Is()` for GORM error checking (standardized for wrapped error compatibility).

✅ **Standard Pattern**:
```go
import "errors"

if errors.Is(err, gorm.ErrRecordNotFound) {  // ✅ Standardized
    return nil, fmt.Errorf("context: %w", domainError)
}
```

❌ **Don't Use**:
```go
if err == gorm.ErrRecordNotFound {  // ❌ Old pattern - don't use
```

**Example**:
```go
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
```

**Service Layer**:
```go
func (s *userService) GetUser(ctx context.Context, id ulid.ULID) (*GetUserResponse, error) {
    user, err := s.userRepo.GetByID(ctx, id)
    if err != nil {
        if errors.Is(err, authDomain.ErrNotFound) {
            return nil, appErrors.NewNotFoundError("User not found")
        }
        return nil, appErrors.NewInternalError("Failed to retrieve user")
    }
    return &GetUserResponse{User: user}, nil
}
```

**Handler Layer**:
```go
func (h *userHandler) GetUser(c *gin.Context) {
    userID := c.Param("id")
    id, err := ulid.Parse(userID)
    if err != nil {
        response.Error(c, appErrors.NewValidationError("Invalid user ID format", "id must be a valid ULID"))
        return
    }

    resp, err := h.userService.GetUser(c.Request.Context(), id)
    if err != nil {
        response.Error(c, err)  // Automatic HTTP mapping
        return
    }

    response.Success(c, resp)
}
```

**Common AppError Constructors** (see `pkg/errors/errors.go` for complete list):
- `appErrors.NewValidationError(message, details string)`
- `appErrors.NewNotFoundError(resource string)`
- `appErrors.NewConflictError(message string)`
- `appErrors.NewUnauthorizedError(message string)`
- `appErrors.NewForbiddenError(message string)`
- `appErrors.NewInternalError(message string, err error)`
- `appErrors.NewRateLimitError(message string)`

### 3. Authentication Patterns

**Two Authentication Systems**:

**SDK Routes** (`/v1/*`): API Key Authentication
```go
// Middleware: SDKAuthMiddleware
// Extract context: middleware.GetSDKAuthContext(c)
// Rate limiting: API key-based

sdkRoutes := r.Group("/v1")
sdkRoutes.Use(sdkAuthMiddleware.RequireSDKAuth())
sdkRoutes.Use(rateLimitMiddleware.RateLimitByAPIKey())
```

**Dashboard Routes** (`/api/v1/*`): JWT Authentication
```go
// Middleware: Authentication()
// Extract user: middleware.GetUserID(c)
// Rate limiting: IP + user-based

// Middleware instances injected via DI (server.go:219-223)
protected := router.Group("")
protected.Use(s.authMiddleware.RequireAuth())           // Instance method - JWT validation
protected.Use(s.csrfMiddleware.ValidateCSRF())          // Instance method - CSRF protection
protected.Use(s.rateLimitMiddleware.RateLimitByUser()) // Instance method - User rate limiting
```

**API Key Format**: `bk_{40_char_random}` with SHA-256 hashing

### 4. Testing Philosophy (CRITICAL)

**Test Business Logic, Not Framework Behavior**

✅ **What to Test**:
- Complex business logic and calculations
- Batch operations and orchestration workflows
- Error handling patterns and retry mechanisms
- Analytics, aggregations, and metrics
- Multi-step operations with dependencies

❌ **What NOT to Test**:
- Simple CRUD operations without business logic
- Field validation (already in domain layer)
- Trivial constructors and getters
- Framework behavior (ULID, time.Now(), errors.Is)
- Static constant definitions

**Test Pattern** (Table-Driven):
```go
func TestUserService_CreateUser(t *testing.T) {
    tests := []struct {
        name        string
        input       *CreateUserRequest
        mockSetup   func(*MockUserRepository)
        expectedErr error
        checkResult func(*testing.T, *CreateUserResponse)
    }{
        {
            name: "success - valid user",
            input: &CreateUserRequest{
                Email: "test@example.com",
                Name:  "Test User",
            },
            mockSetup: func(repo *MockUserRepository) {
                repo.On("Create", mock.Anything, mock.Anything).Return(nil)
            },
            expectedErr: nil,
            checkResult: func(t *testing.T, resp *CreateUserResponse) {
                assert.NotNil(t, resp)
                assert.NotEqual(t, ulid.ULID{}, resp.User.ID)
            },
        },
        // More test cases...
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            mockRepo := new(MockUserRepository)
            tt.mockSetup(mockRepo)

            service := NewUserService(mockRepo)
            result, err := service.CreateUser(context.Background(), tt.input)

            if tt.expectedErr != nil {
                assert.ErrorIs(t, err, tt.expectedErr)
            } else {
                assert.NoError(t, err)
            }

            if tt.checkResult != nil {
                tt.checkResult(t, result)
            }

            mockRepo.AssertExpectations(t)
        })
    }
}
```

## Code Templates

See `code-templates.md` for complete repository, service, and handler templates.

## Development Commands

```bash
# Start development stack
make dev                    # Full stack (server + worker)
make dev-server            # HTTP server only
make dev-worker            # Workers only

# Testing
make test                  # All tests
make test-unit            # Unit tests only
make test-integration     # Integration tests

# Database
make migrate-up           # Run migrations
make migrate-status       # Check status
make seed-dev            # Load dev data

# Code quality
make lint                # Lint all code
make fmt                 # Format code
```

## Key References

When working on specific areas, invoke these specialized skills:
- **Domain Architecture**: Use `brokle-domain-architecture` skill
- **API Routes**: Use `brokle-api-routes` skill
- **Error Handling**: Use `brokle-error-handling` skill
- **Testing**: Use `brokle-testing` skill
- **Migrations**: Use `brokle-migration-workflow` skill

## Documentation

- **Architecture Overview**: `CLAUDE.md`
- **Error Handling**: `docs/development/ERROR_HANDLING_GUIDE.md`
- **Domain Patterns**: `docs/development/DOMAIN_ALIAS_PATTERNS.md`
- **API Development**: `docs/development/API_DEVELOPMENT_GUIDE.md`
- **Testing Guide**: `docs/TESTING.md`

## Development Workflow

1. **Analyze First**: Use Read, Grep, Glob to understand existing patterns
2. **Find Similar Code**: Search for existing implementations
3. **Follow Patterns**: Match the established architecture
4. **Test Business Logic**: Write pragmatic tests for complex logic only
5. **Review Errors**: Ensure proper error handling across all layers

## Multi-Tenant Scoping

**All entities must be organization-scoped**:
```go
type Project struct {
    ID             ulid.ULID
    OrganizationID ulid.ULID  // Required for multi-tenancy
    Name           string
    // ... other fields
}
```

## Enterprise Edition Pattern

Use build tags for enterprise features:
```bash
# OSS build
go build ./cmd/server

# Enterprise build
go build -tags="enterprise" ./cmd/server
```

Enterprise features go in `internal/ee/` with stub implementations for OSS.

## Quick Decision Tree

**Creating new functionality?**
1. Is it a new domain? → Use `brokle-domain-architecture` skill
2. Is it an API endpoint? → Use `brokle-api-routes` skill
3. Is it complex business logic? → Follow service layer pattern + write tests
4. Does it need database schema? → Use `brokle-migration-workflow` skill

**Debugging errors?**
1. Check error handling layer (repo vs service vs handler)
2. Verify domain alias imports
3. Ensure AppError constructors in services
4. Confirm `response.Error()` in handlers

**Adding tests?**
1. Is it complex business logic? → Write tests
2. Is it simple CRUD? → Skip tests
3. Use table-driven test pattern
4. Mock complete interfaces
5. Verify expectations with `AssertExpectations(t)`
