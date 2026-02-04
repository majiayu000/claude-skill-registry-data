---
name: backend-go
description: Enforces Go backend best practices following clean architecture, dependency injection, and test-driven development. Automatically applied for Go backend implementation, API development, and microservices construction.
metadata:
  context: go, backend, api, microservices, clean-architecture
  auto-trigger: true
---

# Backend Go Development

## Overview

This skill provides best practices for Go backend development. It emphasizes clean architecture, dependency injection, and test-driven development to build scalable and maintainable codebases.

## Auto-Trigger Conditions

This skill is automatically applied when:

- Creating or editing Go files (`.go`)
- Working on backend API development
- Implementing microservices
- Database operations
- Keywords like "backend implementation", "API creation" are mentioned

## Project Structure (Clean Architecture)

```bash
project/
├── cmd/
│   └── api/                    # Application entry point
│       └── main.go
├── internal/                   # Private code (cannot be imported externally)
│   ├── domain/                 # Business logic layer (innermost)
│   │   ├── entity/            # Entities (business objects)
│   │   ├── repository/        # Repository interfaces
│   │   └── service/           # Domain services
│   ├── usecase/               # Application business rules
│   │   └── user/
│   │       ├── create.go
│   │       └── get.go
│   ├── handler/               # Presentation layer (outermost)
│   │   ├── http/              # HTTP handlers
│   │   └── grpc/              # gRPC handlers
│   ├── repository/            # Data access layer
│   │   ├── postgres/          # PostgreSQL implementation
│   │   └── redis/             # Redis implementation
│   └── infrastructure/        # External dependencies
│       ├── config/            # Configuration management
│       ├── database/          # DB connection
│       └── logger/            # Logger
├── pkg/                       # Public libraries (can be imported externally)
│   ├── validator/
│   ├── middleware/
│   └── errors/
├── test/                      # Integration tests
│   ├── integration/
│   └── e2e/
├── go.mod
├── go.sum
├── Makefile
└── README.md
```

## Layer Design Principles

### 1. Domain Layer (Innermost)

```go
// internal/domain/entity/user.go
package entity

import (
    "time"
    "github.com/google/uuid"
)

// User entity - business logic only
type User struct {
    ID        uuid.UUID
    Email     string
    Name      string
    CreatedAt time.Time
    UpdatedAt time.Time
}

// Validate domain validation
func (u *User) Validate() error {
    if u.Email == "" {
        return ErrInvalidEmail
    }
    if u.Name == "" {
        return ErrInvalidName
    }
    return nil
}

// internal/domain/repository/user.go
package repository

import (
    "context"
    "github.com/google/uuid"
    "yourproject/internal/domain/entity"
)

// UserRepository interface definition (implementation in outer layers)
type UserRepository interface {
    Create(ctx context.Context, user *entity.User) error
    GetByID(ctx context.Context, id uuid.UUID) (*entity.User, error)
    Update(ctx context.Context, user *entity.User) error
    Delete(ctx context.Context, id uuid.UUID) error
}
```

### 2. UseCase Layer (Business Rules)

```go
// internal/usecase/user/create.go
package user

import (
    "context"
    "github.com/google/uuid"
    "yourproject/internal/domain/entity"
    "yourproject/internal/domain/repository"
)

type CreateUserInput struct {
    Email string
    Name  string
}

type CreateUserUseCase struct {
    userRepo repository.UserRepository
}

func NewCreateUserUseCase(userRepo repository.UserRepository) *CreateUserUseCase {
    return &CreateUserUseCase{
        userRepo: userRepo,
    }
}

func (uc *CreateUserUseCase) Execute(ctx context.Context, input CreateUserInput) (*entity.User, error) {
    // 1. Create entity
    user := &entity.User{
        ID:    uuid.New(),
        Email: input.Email,
        Name:  input.Name,
    }

    // 2. Domain validation
    if err := user.Validate(); err != nil {
        return nil, err
    }

    // 3. Persist through repository
    if err := uc.userRepo.Create(ctx, user); err != nil {
        return nil, err
    }

    return user, nil
}
```

### 3. Handler Layer (Presentation)

```go
// internal/handler/http/user.go
package http

import (
    "net/http"
    "github.com/gin-gonic/gin"
    "yourproject/internal/usecase/user"
)

type UserHandler struct {
    createUserUseCase *user.CreateUserUseCase
}

func NewUserHandler(createUserUseCase *user.CreateUserUseCase) *UserHandler {
    return &UserHandler{
        createUserUseCase: createUserUseCase,
    }
}

type CreateUserRequest struct {
    Email string `json:"email" binding:"required,email"`
    Name  string `json:"name" binding:"required,min=1"`
}

func (h *UserHandler) CreateUser(c *gin.Context) {
    var req CreateUserRequest
    if err := c.ShouldBindJSON(&req); err != nil {
        c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
        return
    }

    user, err := h.createUserUseCase.Execute(c.Request.Context(), user.CreateUserInput{
        Email: req.Email,
        Name:  req.Name,
    })
    if err != nil {
        c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
        return
    }

    c.JSON(http.StatusCreated, user)
}
```

### 4. Repository Layer (Data Access)

```go
// internal/repository/postgres/user.go
package postgres

import (
    "context"
    "database/sql"
    "github.com/google/uuid"
    "yourproject/internal/domain/entity"
    "yourproject/internal/domain/repository"
)

type userRepository struct {
    db *sql.DB
}

func NewUserRepository(db *sql.DB) repository.UserRepository {
    return &userRepository{db: db}
}

func (r *userRepository) Create(ctx context.Context, user *entity.User) error {
    query := `
        INSERT INTO users (id, email, name, created_at, updated_at)
        VALUES ($1, $2, $3, $4, $5)
    `
    _, err := r.db.ExecContext(ctx, query,
        user.ID,
        user.Email,
        user.Name,
        user.CreatedAt,
        user.UpdatedAt,
    )
    return err
}

func (r *userRepository) GetByID(ctx context.Context, id uuid.UUID) (*entity.User, error) {
    query := `
        SELECT id, email, name, created_at, updated_at
        FROM users
        WHERE id = $1
    `
    var user entity.User
    err := r.db.QueryRowContext(ctx, query, id).Scan(
        &user.ID,
        &user.Email,
        &user.Name,
        &user.CreatedAt,
        &user.UpdatedAt,
    )
    if err != nil {
        return nil, err
    }
    return &user, nil
}
```

## Dependency Injection

```go
// cmd/api/main.go
package main

import (
    "database/sql"
    "log"

    "github.com/gin-gonic/gin"
    _ "github.com/lib/pq"

    "yourproject/internal/handler/http"
    "yourproject/internal/repository/postgres"
    "yourproject/internal/usecase/user"
)

func main() {
    // 1. Initialize infrastructure
    db, err := sql.Open("postgres", "postgresql://...")
    if err != nil {
        log.Fatal(err)
    }
    defer db.Close()

    // 2. Build repository layer
    userRepo := postgres.NewUserRepository(db)

    // 3. Build usecase layer
    createUserUseCase := user.NewCreateUserUseCase(userRepo)

    // 4. Build handler layer
    userHandler := http.NewUserHandler(createUserUseCase)

    // 5. Setup router
    r := gin.Default()
    r.POST("/users", userHandler.CreateUser)

    // 6. Start server
    if err := r.Run(":8080"); err != nil {
        log.Fatal(err)
    }
}
```

## Error Handling

```go
// pkg/errors/errors.go
package errors

import (
    "errors"
    "fmt"
)

type AppError struct {
    Code    string
    Message string
    Err     error
}

func (e *AppError) Error() string {
    if e.Err != nil {
        return fmt.Sprintf("%s: %v", e.Message, e.Err)
    }
    return e.Message
}

func (e *AppError) Unwrap() error {
    return e.Err
}

// Predefined errors
var (
    ErrNotFound      = &AppError{Code: "NOT_FOUND", Message: "resource not found"}
    ErrInvalidInput  = &AppError{Code: "INVALID_INPUT", Message: "invalid input"}
    ErrUnauthorized  = &AppError{Code: "UNAUTHORIZED", Message: "unauthorized"}
)

// Error wrapping
func Wrap(err error, message string) error {
    return &AppError{
        Message: message,
        Err:     err,
    }
}
```

## Testing Strategy

### Unit Tests

```go
// internal/usecase/user/create_test.go
package user_test

import (
    "context"
    "testing"

    "github.com/stretchr/testify/assert"
    "github.com/stretchr/testify/mock"

    "yourproject/internal/domain/entity"
    "yourproject/internal/usecase/user"
)

// Mock repository
type MockUserRepository struct {
    mock.Mock
}

func (m *MockUserRepository) Create(ctx context.Context, user *entity.User) error {
    args := m.Called(ctx, user)
    return args.Error(0)
}

func TestCreateUserUseCase_Execute(t *testing.T) {
    // Arrange
    mockRepo := new(MockUserRepository)
    useCase := user.NewCreateUserUseCase(mockRepo)

    input := user.CreateUserInput{
        Email: "test@example.com",
        Name:  "Test User",
    }

    mockRepo.On("Create", mock.Anything, mock.AnythingOfType("*entity.User")).Return(nil)

    // Act
    result, err := useCase.Execute(context.Background(), input)

    // Assert
    assert.NoError(t, err)
    assert.NotNil(t, result)
    assert.Equal(t, input.Email, result.Email)
    mockRepo.AssertExpectations(t)
}
```

### Table-Driven Tests

```go
func TestValidate(t *testing.T) {
    tests := []struct {
        name    string
        user    *entity.User
        wantErr bool
    }{
        {
            name:    "valid user",
            user:    &entity.User{Email: "test@example.com", Name: "Test"},
            wantErr: false,
        },
        {
            name:    "empty email",
            user:    &entity.User{Email: "", Name: "Test"},
            wantErr: true,
        },
        {
            name:    "empty name",
            user:    &entity.User{Email: "test@example.com", Name: ""},
            wantErr: true,
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            err := tt.user.Validate()
            if tt.wantErr {
                assert.Error(t, err)
            } else {
                assert.NoError(t, err)
            }
        })
    }
}
```

## Performance Optimization

### 1. Context Management

```go
func (h *Handler) Handle(c *gin.Context) {
    // Set timeout
    ctx, cancel := context.WithTimeout(c.Request.Context(), 5*time.Second)
    defer cancel()

    result, err := h.useCase.Execute(ctx)
    // ...
}
```

### 2. Connection Pooling

```go
func NewDB(connStr string) (*sql.DB, error) {
    db, err := sql.Open("postgres", connStr)
    if err != nil {
        return nil, err
    }

    db.SetMaxOpenConns(25)                 // Maximum open connections
    db.SetMaxIdleConns(5)                  // Maximum idle connections
    db.SetConnMaxLifetime(5 * time.Minute) // Maximum connection lifetime

    return db, nil
}
```

### 3. Goroutines and Channels

```go
func (s *Service) ProcessBatch(ctx context.Context, items []Item) error {
    errCh := make(chan error, len(items))
    sem := make(chan struct{}, 10) // Limit concurrency

    for _, item := range items {
        sem <- struct{}{} // Acquire semaphore

        go func(item Item) {
            defer func() { <-sem }() // Release semaphore

            if err := s.processItem(ctx, item); err != nil {
                errCh <- err
            }
        }(item)
    }

    // Wait for all goroutines to complete
    for i := 0; i < cap(sem); i++ {
        sem <- struct{}{}
    }
    close(errCh)

    // Collect errors
    for err := range errCh {
        if err != nil {
            return err
        }
    }

    return nil
}
```

## Implementation Checklist

### Design Phase
- [ ] Define each layer of clean architecture
- [ ] Identify entities and business rules
- [ ] Clearly define interfaces
- [ ] Verify dependency direction (no dependency on inner layers)

### Implementation Phase
- [ ] Domain layer: Entities and repository interfaces
- [ ] UseCase layer: Business logic implementation
- [ ] Repository layer: Data access implementation
- [ ] Handler layer: HTTP handler implementation
- [ ] Error handling implementation
- [ ] Add logging

### Testing Phase
- [ ] Create unit tests (target 80%+ coverage)
- [ ] Isolate dependencies using mocks
- [ ] Apply table-driven tests
- [ ] Create integration tests

### Pre-Production Deployment
- [ ] Conduct performance tests
- [ ] Security review
- [ ] Update documentation
- [ ] Verify log levels

## Best Practices

### DO ✅
- Follow clean architecture
- Use interfaces for loose coupling
- Practice test-driven development (TDD)
- Handle errors appropriately
- Use context for cancellation
- Use pointer receivers for structs

### DON'T ❌
- Don't use global variables
- Don't overuse panic (return errors instead)
- Don't leak goroutines
- Don't skip nil checks
- Don't create large functions (keep functions small)
- Don't create circular dependencies

## Security

```go
// 1. SQL Injection prevention: Use placeholders
query := "SELECT * FROM users WHERE id = $1"
db.QueryContext(ctx, query, userID)

// 2. Password hashing
import "golang.org/x/crypto/bcrypt"

hashedPassword, _ := bcrypt.GenerateFromPassword([]byte(password), bcrypt.DefaultCost)

// 3. Rate limiting
import "golang.org/x/time/rate"

limiter := rate.NewLimiter(rate.Limit(10), 100) // 10 req/sec, burst 100
if !limiter.Allow() {
    return ErrTooManyRequests
}
```

## Summary

This skill ensures:

- 🏗️ **Clean Architecture**: Layer separation and dependency inversion
- 🧪 **Testability**: High coverage and maintainability
- ⚡ **Performance**: Efficient concurrency
- 🔒 **Security**: Secure code implementation
- 📦 **Scalability**: Microservice-ready
- 📚 **Maintainability**: Readable and extensible code
