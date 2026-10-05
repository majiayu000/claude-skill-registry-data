---
name: go-cleanup
description: Apply gofmt, remove unused packages, improve error handling, and clean up Go codebases. Use when cleaning up Go projects, removing unused imports, applying.
---

# Go Code Cleanup

Systematically identify and remove dead code, apply idiomatic Go patterns, and use standard Go tooling to maintain a clean, maintainable codebase.

## When to Use This Skill

Use this skill when you need to:

- Remove unused imports and packages
- Apply gofmt and goimports
- Fix go vet and staticcheck warnings
- Apply idiomatic Go patterns
- Improve error handling
- Clean up before code review

**Trigger phrases**: "cleanup Go", "gofmt", "remove dead code Go", "fix go vet", "Go refactor", "idiomatic Go"

## What This Skill Does

### Cleanup Areas

1. **Dead Code Removal**
   - Unused imports
   - Unused variables and functions
   - Unreachable code
   - Redundant code

2. **Style Compliance**
   - gofmt formatting
   - golint/staticcheck rules
   - Effective Go patterns

3. **Modernization**
   - Error wrapping (Go 1.13+)
   - Generics (Go 1.18+)
   - Build tags (Go 1.17+)

## Instructions

### Step 1: Run Standard Go Tools

```bash
# Format all files
gofmt -w .

# Organize imports
goimports -w .

# Run vet for suspicious constructs
go vet ./...

# Run staticcheck for additional issues
staticcheck ./...

# Run tests
go test ./...

# Clean up modules
go mod tidy
```

### Step 2: Fix Common Issues

#### Import Organization

```go
// Standard order: stdlib, external, internal
import (
    // Standard library
    "context"
    "fmt"
    "time"

    // External packages
    "github.com/pkg/errors"
    "go.uber.org/zap"

    // Internal packages
    "myproject/internal/config"
    "myproject/pkg/utils"
)
```

#### Unused Variables

```go
// Before - unused variable
func process(data []byte) error {
    result, err := parse(data)
    if err != nil {
        return err
    }
    // result is never used
    return nil
}

// After - use blank identifier or remove
func process(data []byte) error {
    _, err := parse(data)
    if err != nil {
        return err
    }
    return nil
}
```

### Step 3: Apply Idiomatic Patterns

#### Error Handling

```go
// Before - generic error
if err != nil {
    return err
}

// After - wrapped error with context (Go 1.13+)
if err != nil {
    return fmt.Errorf("failed to process user %s: %w", userID, err)
}

// Error checking with errors.Is and errors.As
if errors.Is(err, ErrNotFound) {
    return nil
}

var pathErr *os.PathError
if errors.As(err, &pathErr) {
    log.Printf("path error: %s", pathErr.Path)
}
```

#### Named Returns (Use Sparingly)

```go
// Avoid naked returns in long functions
// Before
func getData() (result []byte, err error) {
    // ... many lines ...
    return // naked return - hard to follow
}

// After
func getData() ([]byte, error) {
    // ... many lines ...
    return result, nil // explicit return
}

// Named returns OK for short functions with defer
func (f *File) Read(buf []byte) (n int, err error) {
    defer func() {
        if err != nil {
            err = fmt.Errorf("read failed: %w", err)
        }
    }()
    n, err = f.file.Read(buf)
    return
}
```

#### Context Usage

```go
// Context should be first parameter
func GetUser(ctx context.Context, id string) (*User, error) {
    // ...
}

// Pass context through the call chain
func ProcessRequest(ctx context.Context, req *Request) error {
    user, err := GetUser(ctx, req.UserID)
    if err != nil {
        return err
    }
    return SendNotification(ctx, user)
}

// Use context for cancellation
func LongOperation(ctx context.Context) error {
    select {
    case <-ctx.Done():
        return ctx.Err()
    case result := <-doWork():
        return process(result)
    }
}
```

#### Interface Design

```go
// Accept interfaces, return structs
// Before
func ProcessData(s *Service) *Result {
    // tightly coupled to concrete type
}

// After
type DataProcessor interface {
    Process(data []byte) ([]byte, error)
}

func ProcessData(p DataProcessor) (*Result, error) {
    // accepts any implementation
}

// Small, focused interfaces
type Reader interface {
    Read(p []byte) (n int, err error)
}

type Writer interface {
    Write(p []byte) (n int, err error)
}

// Compose interfaces as needed
type ReadWriter interface {
    Reader
    Writer
}
```

#### Receiver Names

```go
// Use consistent, short receiver names
// Before
func (service *UserService) GetUser(id string) (*User, error)
func (us *UserService) UpdateUser(u *User) error

// After - consistent 1-2 char names
func (s *UserService) GetUser(id string) (*User, error)
func (s *UserService) UpdateUser(u *User) error
```

#### Range Loops

```go
// Value copy in range (be aware of this)
for _, user := range users {
    // user is a copy
}

// Use index for modification
for i := range users {
    users[i].Processed = true
}

// Use blank identifier when not needed
for range items {
    count++
}
```

### Step 4: Performance Patterns

#### Slice Preallocation

```go
// Before - grows slice dynamically
func processUsers(ids []string) []User {
    var users []User
    for _, id := range ids {
        users = append(users, getUser(id))
    }
    return users
}

// After - preallocate capacity
func processUsers(ids []string) []User {
    users := make([]User, 0, len(ids))
    for _, id := range ids {
        users = append(users, getUser(id))
    }
    return users
}
```

#### String Building

```go
// Before - inefficient string concatenation
func buildQuery(params []string) string {
    result := ""
    for _, p := range params {
        result += p + ","
    }
    return result
}

// After - use strings.Builder
func buildQuery(params []string) string {
    var b strings.Builder
    for i, p := range params {
        if i > 0 {
            b.WriteString(",")
        }
        b.WriteString(p)
    }
    return b.String()
}

// Or use strings.Join for simple cases
func buildQuery(params []string) string {
    return strings.Join(params, ",")
}
```

#### Map Preallocation

```go
// Before
result := make(map[string]int)

// After - preallocate when size is known
result := make(map[string]int, len(items))
```

### Step 5: Modern Go Features

#### Generics (Go 1.18+)

```go
// Before - type-specific functions
func MinInt(a, b int) int {
    if a < b {
        return a
    }
    return b
}

// After - generic function
func Min[T constraints.Ordered](a, b T) T {
    if a < b {
        return a
    }
    return b
}

// Generic slice operations
func Filter[T any](slice []T, predicate func(T) bool) []T {
    result := make([]T, 0, len(slice))
    for _, v := range slice {
        if predicate(v) {
            result = append(result, v)
        }
    }
    return result
}
```

#### Build Tags (Go 1.17+)

```go
// Before (old style)
// +build linux

// After (new style)
//go:build linux

// Multiple conditions
//go:build linux && amd64
//go:build !windows
```

#### Error Wrapping (Go 1.13+)

```go
// Wrap errors for context
return fmt.Errorf("failed to open file %s: %w", filename, err)

// Check wrapped errors
if errors.Is(err, os.ErrNotExist) {
    // handle not found
}

// Extract wrapped error type
var pathErr *os.PathError
if errors.As(err, &pathErr) {
    fmt.Println("Failed path:", pathErr.Path)
}
```

### Step 6: Module Cleanup

```bash
# Remove unused dependencies
go mod tidy

# Verify modules
go mod verify

# Check for updates
go list -u -m all

# Update specific dependency
go get -u github.com/pkg/errors@latest

# Vendor dependencies (if using)
go mod vendor
```

## Tools

- **gofmt**: Standard formatting
- **goimports**: Import organization
- **go vet**: Suspicious constructs
- **staticcheck**: Additional checks
- **golangci-lint**: Meta linter
- **errcheck**: Error checking
- **ineffassign**: Ineffectual assignments
- **gosec**: Security issues

## Quality Checklist

- [ ] gofmt applied (no changes)
- [ ] goimports applied (no changes)
- [ ] go vet passes
- [ ] staticcheck passes
- [ ] Unused imports removed
- [ ] Unused variables removed
- [ ] Error handling follows patterns
- [ ] Context used correctly
- [ ] go mod tidy applied
- [ ] Tests pass

## Common Issues and Solutions

### Issue: Unused import
**Solution**: Remove the import or use blank identifier for side effects:
```go
import _ "github.com/lib/pq" // side effect import
```

### Issue: Error not checked
**Solution**: Either handle the error or explicitly ignore it:
```go
// Handle error
if err != nil {
    return err
}

// Explicitly ignore (rare cases)
_ = file.Close()
```

### Issue: Shadow variable
**Solution**: Use different variable name or explicit assignment:
```go
// Before - shadows outer err
err := doSomething()
if err != nil {
    err := doSomethingElse() // shadows!
}

// After
err := doSomething()
if err != nil {
    err = doSomethingElse() // assigns to outer err
}
```

## Related Skills

- `code-review-quality` - Code quality assessment
- `security-review` - Security analysis

---

**Version**: 1.0.0
**Last Updated**: December 2025
**Based on**: AI Templates code_cleanup/go_cleanup.md


### Iterative Refinement Strategy
This skill is optimized for an iterative approach:
1. **Execute**: Perform the core steps defined above.
2. **Review**: Critically analyze the output (coverage, quality, completeness).
3. **Refine**: If targets aren't met, repeat the specific implementation steps with improved context.
4. **Loop**: Continue until the definition of done is satisfied.
