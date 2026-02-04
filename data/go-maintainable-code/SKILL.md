---
name: go-maintainable-code
description: Write clean, maintainable Go code following Clean Architecture, dependency injection, and ChecklistApplication patterns. Use when writing new Go code, refactoring, or implementing features.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# Go Maintainable Code Skill

This skill ensures all Go code follows Clean Architecture principles and project-specific patterns used in ChecklistApplication.

## Core Principles

### 1. Clean Architecture Layers (CRITICAL)

**Dependency Flow**: `server → service → repository`

```
internal/
├── server/           # HTTP layer (Gin, OpenAPI controllers)
│   └── Depends on: service (via interfaces)
├── core/
│   ├── service/      # Business logic (framework-independent)
│   │   └── Depends on: repository interfaces, domain
│   ├── domain/       # Entities, value objects (no dependencies)
│   └── repository/   # Repository interfaces (no implementation)
└── repository/       # PostgreSQL implementations
    └── Depends on: repository interfaces, domain
```

**Rules**:
- ✅ Server calls service interfaces
- ✅ Service calls repository interfaces
- ✅ Domain has NO external dependencies
- ❌ NEVER import concrete types across layers
- ❌ NEVER import `internal/repository` from `internal/core/service`

### 2. Interface-Based Design

**Pattern from codebase**:
```go
// Define interface in core/repository
package repository
type IChecklistService interface {
    DeleteChecklistById(ctx context.Context, id uint) domain.Error
}

// Implement in core/service
package service
type checklistService struct {
    repository repository.IChecklistRepository  // Interface, not concrete
}

// Wire provides concrete implementation
// internal/deployment/wire.go
```

### 3. Dependency Injection via Wire

**ALWAYS use Wire for dependencies**:
```go
// Add to internal/deployment/wire.go
func InitializeApp() (*App, error) {
    wire.Build(
        // ... existing providers ...
        NewMyService,           // Add your constructor
        wire.Bind(new(IMyService), new(*myService)),
    )
    return nil, nil
}
```

**Then run**:
```bash
./generate.sh  # Regenerates wire_gen.go
```

## Code Quality Standards

### Error Handling

**Use domain.Error (custom error type)**:
```go
// ✅ Good
func (s *service) Delete(ctx context.Context, id uint) domain.Error {
    if err := s.repo.Delete(ctx, id); err != nil {
        return domain.Wrap(err, "failed to delete", 500)
    }
    return nil
}

// ❌ Bad - using standard error
func (s *service) Delete(ctx context.Context, id uint) error {
    return errors.New("something failed")
}
```

**Error patterns**:
- Return `domain.Error` from service/repository methods
- Use `domain.NewError(message, statusCode)` for new errors
- Use `domain.Wrap(err, context, statusCode)` to wrap errors
- Guard rails return 404 for access denied (security pattern)

### Context Usage

**Extract user context**:
```go
// In service layer
userId, err := domain.GetUserIdFromContext(ctx)
if err != nil {
    return err
}

// Guard rail checks
if err := s.checklistOwnershipChecker.HasAccessToChecklist(ctx, checklistId); err != nil {
    return error.NewChecklistNotFoundError(checklistId)
}
```

**Extract client ID** (for SSE):
```go
// In controller
clientId := serverutils.GetClientIdFromContext(ctx)
```

### Transaction Handling

**Use connection.RunInTransaction**:
```go
runQueryFunction := func(tx pool.TransactionWrapper) (ResultType, error) {
    // Execute queries using tx, not connection
    result, err := tx.Exec(ctx, query, args)
    return processedResult, err
}

res, err := connection.RunInTransaction(connection.TransactionProps[ResultType]{
    Query:      runQueryFunction,
    Connection: r.connection,
    TxOptions:  pgx.TxOptions{IsoLevel: pgx.Serializable},
})
```

### Testing Requirements

**Every service method needs tests**:
```go
func TestMyService_MethodName_SuccessCase(t *testing.T) {
    // Arrange
    mockRepo := new(mockRepository)
    mockRepo.On("Method", mock.Anything, expectedArgs).Return(expectedResult, nil)

    svc := &myService{repository: mockRepo}

    // Act
    result, err := svc.Method(context.Background(), args)

    // Assert
    if err != nil {
        t.Fatalf("unexpected error: %v", err)
    }
    mockRepo.AssertExpectations(t)
}
```

**Test patterns**:
- Success case
- Error cases
- Guard rail failures
- Edge cases (nil, empty, boundary values)

See [testing-guide.md](testing-guide.md) for complete examples.

## Project-Specific Patterns

### 1. OpenAPI-First Development

**Workflow**:
1. Update `openapi/api_v1.yaml` with new operation
2. Run `./generate.sh` to generate server interfaces
3. Implement generated interface in controller
4. NEVER edit `*_gen.go` files manually

**Example**:
```yaml
# openapi/api_v1.yaml
paths:
  /api/v1/checklists/{checklistId}/archive:
    post:
      operationId: archiveChecklist
      # ... rest of spec
```

```go
// internal/server/v1/checklist/controller.go
// Implements generated ServerInterface
func (c *controller) ArchiveChecklist(ctx context.Context, req ArchiveChecklistRequestObject) (ArchiveChecklistResponseObject, error) {
    // Implementation
}
```

### 2. SSE Notifications

**After mutations, publish events**:
```go
func (s *service) Delete(ctx context.Context, id uint) domain.Error {
    if err := s.repository.Delete(ctx, id); err != nil {
        return err
    }

    // Publish SSE event
    s.notifier.NotifyItemDeleted(ctx, checklistId, id)
    return nil
}
```

**SSE patterns**:
- Events filtered by Client ID (no echo to originating client)
- Non-blocking publish with buffered channels
- Guard rail check on subscribe

### 3. Database Patterns

**Doubly-linked list ordering**:
```go
// Items use NEXT_ITEM_ID/PREV_ITEM_ID
// Use recursive CTE view: CHECKLIST_ITEMS_ORDERED_VIEW
// Phantom items: IS_PHANTOM = true, filtered in queries
```

**CASCADE constraints**:
```sql
FOREIGN KEY (parent_id) REFERENCES parent(id) ON DELETE CASCADE
```

**Named arguments** (pgx):
```go
args := pgx.NamedArgs{
    "checklist_id": id,
    "user_id":      userId,
}
result, err := tx.Exec(ctx, "DELETE FROM t WHERE id = @checklist_id", args)
```

### 4. Struct Constructors

**Private structs with public interfaces**:
```go
// Public interface
type IMyService interface {
    DoSomething(ctx context.Context) error
}

// Private implementation
type myService struct {
    repo repository.IMyRepository
}

// Public constructor for Wire
func NewMyService(repo repository.IMyRepository) IMyService {
    return &myService{repo: repo}
}
```

## Anti-Patterns to Avoid

### ❌ Don't Do This

```go
// ❌ Importing concrete types across layers
import "com.raunlo.checklist/internal/repository"

// ❌ Business logic in controllers
func (c *controller) Delete(ctx context.Context, req Request) Response {
    // Validating, processing here - NO!
}

// ❌ SQL in service layer
func (s *service) Find(ctx context.Context) {
    rows, _ := db.Query("SELECT ...") // NO!
}

// ❌ Not using guard rails
func (s *service) Delete(ctx context.Context, id uint) {
    return s.repo.Delete(ctx, id) // Missing access check!
}

// ❌ Hardcoded dependencies
type service struct {
    repo *postgresRepo  // Should be interface
}

// ❌ Ignoring errors
s.repo.Delete(ctx, id)  // No error handling

// ❌ Empty error messages
return domain.NewError("", 500)
```

### ✅ Do This Instead

```go
// ✅ Interface imports only
import "com.raunlo.checklist/internal/core/repository"

// ✅ Thin controllers
func (c *controller) Delete(ctx context.Context, req Request) Response {
    domainCtx := serverutils.CreateContext(ctx)
    if err := c.service.DeleteById(domainCtx, req.Id); err != nil {
        return mapError(err)
    }
    return success()
}

// ✅ SQL in repository layer
func (r *repo) Find(ctx context.Context) ([]Entity, domain.Error) {
    rows, err := r.connection.Query(ctx, query)
    // ...
}

// ✅ Guard rail checks
func (s *service) Delete(ctx context.Context, id uint) domain.Error {
    if err := s.guardrail.HasAccessToChecklist(ctx, id); err != nil {
        return error.NewChecklistNotFoundError(id)
    }
    return s.repo.Delete(ctx, id)
}

// ✅ Interface dependencies
type service struct {
    repo repository.IMyRepository  // Interface
}

// ✅ Proper error handling
if err := s.repo.Delete(ctx, id); err != nil {
    return domain.Wrap(err, "failed to delete checklist", 500)
}

// ✅ Descriptive errors
return domain.NewError("Checklist is not empty", 400)
```

## Checklist for New Code

Before submitting code, verify:

- [ ] Follows Clean Architecture (correct layer separation)
- [ ] Uses interfaces for dependencies
- [ ] Added to Wire configuration if new service/repo
- [ ] Ran `./generate.sh` if OpenAPI changed
- [ ] Proper error handling (domain.Error)
- [ ] Guard rail checks for authorization
- [ ] SSE notifications for mutations (if applicable)
- [ ] Unit tests with mocks (testify)
- [ ] No magic numbers or strings
- [ ] Context passed through all layers
- [ ] Ran `go test ./...` and all pass
- [ ] Ran `go build ./...` successfully
- [ ] No TODO comments without issue number

See [code-review-checklist.md](code-review-checklist.md) for complete review guide.

## Quick Reference

**Common commands**:
```bash
./generate.sh           # OpenAPI + Wire code generation
go test ./...          # Run all tests
go build ./...         # Build all packages
go test ./internal/core/service -v -run TestMyTest  # Run specific test
```

**File locations**:
- Controllers: `internal/server/v1/`
- Services: `internal/core/service/`
- Service interfaces: `internal/core/repository/`
- Repository impls: `internal/repository/`
- Domain entities: `internal/core/domain/`
- SQL queries: `internal/repository/query/`
- Wire config: `internal/deployment/wire.go`
- OpenAPI spec: `openapi/api_v1.yaml`

## Related Documentation

- [Go Patterns](go-patterns.md) - Language-specific best practices
- [Testing Guide](testing-guide.md) - Comprehensive testing examples
- [Code Review Checklist](code-review-checklist.md) - Quality checklist
- Project: [CLAUDE.md](../../../CLAUDE.md) - Full architecture guide
