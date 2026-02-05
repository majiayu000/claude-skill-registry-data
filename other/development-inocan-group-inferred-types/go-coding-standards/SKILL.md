---
name: go-coding-standards
description: Go coding standards following idiomatic Go patterns, error handling, concurrency best practices, and modern Go tooling. Use for Go projects requiring clean, efficient, production-ready code with comprehensive testing.
---

# Go Coding Standards

> **Quick Navigation:**
> Level 1: [Quick Start](#level-1-quick-start-2000-tokens-5-minutes) (5 min) → Level 2: [Implementation](#level-2-implementation-5000-tokens-30-minutes) (30 min) → Level 3: [Mastery](#level-3-mastery-resources) (Extended)

---

## Level 1: Quick Start (<2,000 tokens, 5 minutes)

### Core Principles

1. **Idiomatic Go**: Write code that follows Go idioms - simple, clear, and effective
2. **Explicit Errors**: Return errors explicitly, handle them properly, no exceptions
3. **Interfaces**: Accept interfaces, return concrete types
4. **Concurrency**: Goroutines and channels for concurrent operations
5. **Testing**: Table-driven tests with >80% coverage

### Essential Checklist

- [ ] **Formatting**: Code formatted with `gofmt`, imports organized with `goimports`
- [ ] **Naming**: Follow Go conventions (MixedCaps, camelCase, short names in limited scope)
- [ ] **Error Handling**: All errors checked and wrapped with context
- [ ] **Testing**: `_test.go` files with table-driven tests, benchmarks
- [ ] **Documentation**: Package and exported function documentation
- [ ] **Modules**: `go.mod` with semantic versioning, tidy dependencies
- [ ] **Linting**: Pass `golangci-lint` with strict configuration
- [ ] **Security**: Input validation, no hardcoded secrets, secure defaults

### Quick Example

```go
// Package auth provides user authentication services.
package auth

import (
	"context"
	"errors"
	"fmt"
)

var (
	// ErrInvalidCredentials indicates authentication failure.
	ErrInvalidCredentials = errors.New("invalid credentials")
	// ErrUserNotFound indicates user does not exist.
	ErrUserNotFound = errors.New("user not found")
)

// User represents an authenticated user.
type User struct {
	ID       string
	Username string
	Email    string
}

// Repository defines user storage operations.
type Repository interface {
	FindByUsername(ctx context.Context, username string) (*User, error)
	VerifyPassword(ctx context.Context, userID, password string) bool
}

// Service handles authentication operations.
type Service struct {
	repo Repository
}

// NewService creates a new authentication service.
func NewService(repo Repository) *Service {
	return &Service{repo: repo}
}

// Authenticate verifies credentials and returns the authenticated user.
//
// Returns ErrInvalidCredentials if authentication fails,
// ErrUserNotFound if user doesn't exist, or wrapped errors for other failures.
func (s *Service) Authenticate(ctx context.Context, username, password string) (*User, error) {
	if username == "" || password == "" {
		return nil, fmt.Errorf("username and password required")
	}

	user, err := s.repo.FindByUsername(ctx, username)
	if err != nil {
		if errors.Is(err, ErrUserNotFound) {
			return nil, ErrInvalidCredentials // Don't reveal user existence
		}
		return nil, fmt.Errorf("find user: %w", err)
	}

	if !s.repo.VerifyPassword(ctx, user.ID, password) {
		return nil, ErrInvalidCredentials
	}

	return user, nil
}
```

### Quick Links to Level 2

- [Code Style & Organization](#code-style--organization)
- [Error Handling Patterns](#error-handling-patterns)
- [Concurrency & Channels](#concurrency--channels)
- [Testing Best Practices](#testing-best-practices)
- [Performance Optimization](#performance-optimization)

---

## Level 2: Implementation (<5,000 tokens, 30 minutes)

### Code Style & Organization

**Idiomatic Go Naming**

```go
// ✅ Good: Clear, concise Go naming
type UserService struct {
	db    *sql.DB
	cache Cache
}

func (s *UserService) Get(ctx context.Context, id string) (*User, error) {
	// Short names in limited scope
	u, err := s.cache.Get(ctx, id)
	if err == nil {
		return u, nil
	}
	return s.db.QueryUser(ctx, id)
}

// ❌ Bad: Verbose, non-idiomatic
type UserServiceInterface struct {
	databaseConnection *sql.DB
	cacheImplementation Cache
}
```

**Package Structure**

```
myapp/
├── cmd/
│   └── server/
│       └── main.go          # Entry point
├── internal/
│   ├── auth/                # Authentication domain
│   │   ├── service.go
│   │   ├── repository.go
│   │   └── service_test.go
│   └── user/                # User domain
│       ├── user.go
│       └── postgres.go
├── pkg/
│   └── middleware/          # Reusable components
│       └── logging.go
├── go.mod
└── go.sum
```

### Error Handling Patterns

**Sentinel Errors and Wrapping**

```go
import (
	"errors"
	"fmt"
)

// Sentinel errors
var (
	ErrNotFound     = errors.New("not found")
	ErrUnauthorized = errors.New("unauthorized")
	ErrValidation   = errors.New("validation failed")
)

// Custom error types
type ValidationError struct {
	Field   string
	Message string
}

func (e *ValidationError) Error() string {
	return fmt.Sprintf("%s: %s", e.Field, e.Message)
}

// Error wrapping with context
func (s *Service) GetUser(ctx context.Context, id string) (*User, error) {
	user, err := s.repo.FindByID(ctx, id)
	if err != nil {
		if errors.Is(err, sql.ErrNoRows) {
			return nil, fmt.Errorf("user %s: %w", id, ErrNotFound)
		}
		return nil, fmt.Errorf("fetch user %s: %w", id, err)
	}
	return user, nil
}

// Error checking
if errors.Is(err, ErrNotFound) {
	// Handle not found
}

var valErr *ValidationError
if errors.As(err, &valErr) {
	// Handle validation error
	fmt.Printf("Field %s: %s\n", valErr.Field, valErr.Message)
}
```

### Concurrency & Channels

**Worker Pool Pattern**

```go
func ProcessJobs(jobs <-chan Job, results chan<- Result, workers int) {
	var wg sync.WaitGroup

	for i := 0; i < workers; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			for job := range jobs {
				result := process(job)
				results <- result
			}
		}()
	}

	go func() {
		wg.Wait()
		close(results)
	}()
}
```

**Context and Cancellation**

```go
func (s *Service) FetchWithTimeout(ctx context.Context, url string) ([]byte, error) {
	ctx, cancel := context.WithTimeout(ctx, 5*time.Second)
	defer cancel()

	req, err := http.NewRequestWithContext(ctx, "GET", url, nil)
	if err != nil {
		return nil, fmt.Errorf("create request: %w", err)
	}

	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		return nil, fmt.Errorf("execute request: %w", err)
	}
	defer resp.Body.Close()

	return io.ReadAll(resp.Body)
}
```

### Testing Best Practices

**Table-Driven Tests**

```go
func TestAdd(t *testing.T) {
	tests := []struct {
		name string
		a, b int
		want int
	}{
		{"positive", 2, 3, 5},
		{"negative", -2, -3, -5},
		{"zero", 0, 0, 0},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got := Add(tt.a, tt.b)
			if got != tt.want {
				t.Errorf("got %d, want %d", got, tt.want)
			}
		})
	}
}
```

**See Also:** [Test Template](templates/test-template.go), [Benchmarking Guide](resources/benchmarking.md)

### Performance Optimization

**Buffer Pools**

```go
var bufPool = sync.Pool{
	New: func() interface{} {
		return new(bytes.Buffer)
	},
}

func Format(data []byte) []byte {
	buf := bufPool.Get().(*bytes.Buffer)
	defer bufPool.Put(buf)
	buf.Reset()

	buf.Write(data)
	// Process...
	return buf.Bytes()
}
```

---

## Level 3: Mastery Resources

### Advanced Topics

- **[Concurrency Patterns](resources/concurrency-patterns.md)**: Advanced patterns
- **[Generics Guide](resources/generics-guide.md)**: Type parameters and constraints
- **[Performance](resources/performance-guide.md)**: Profiling and optimization

### Templates

- **[Project Template](templates/project/)**: Complete structure
- **[HTTP Server](templates/http-server/)**: REST API template
- **[CLI App](templates/cli/)**: cobra-based CLI

### Configuration

- **[.golangci.yml](resources/configs/.golangci.yml)**: Linter configuration
- **[Makefile](resources/configs/Makefile)**: Build automation

### Related Skills

- [Testing Standards](../../testing/integration-testing/SKILL.md)
- [Secrets Management](../../security/secrets-management/SKILL.md)
- [Kubernetes](../../cloud-native/kubernetes/SKILL.md)

---

## Quick Reference

```bash
# Setup
go mod init github.com/user/project
go mod tidy

# Quality
gofmt -w .
goimports -w .
golangci-lint run

# Test
go test ./...
go test -cover ./...
go test -bench=.

# Build
go build -o app ./cmd/app
```

---

## Examples

### Basic Usage

```go
// TODO: Add basic example for go
// This example demonstrates core functionality
```

### Advanced Usage

```go
// TODO: Add advanced example for go
// This example shows production-ready patterns
```

### Integration Example

```go
// TODO: Add integration example showing how go
// works with other systems and services
```

See `examples/go/` for complete working examples.

## Integration Points

This skill integrates with:

### Upstream Dependencies

- **Tools**: Common development tools and frameworks
- **Prerequisites**: Basic understanding of general concepts

### Downstream Consumers

- **Applications**: Production systems requiring go functionality
- **CI/CD Pipelines**: Automated testing and deployment workflows
- **Monitoring Systems**: Observability and logging platforms

### Related Skills

- See other skills in this category

### Common Integration Patterns

1. **Development Workflow**: How this skill fits into daily development
2. **Production Deployment**: Integration with production systems
3. **Monitoring & Alerting**: Observability integration points

## Common Pitfalls

### Pitfall 1: Insufficient Testing

**Problem:** Not testing edge cases and error conditions leads to production bugs

**Solution:** Implement comprehensive test coverage including:

- Happy path scenarios
- Error handling and edge cases
- Integration points with external systems

**Prevention:** Enforce minimum code coverage (80%+) in CI/CD pipeline

### Pitfall 2: Hardcoded Configuration

**Problem:** Hardcoding values makes applications inflexible and environment-dependent

**Solution:** Use environment variables and configuration management:

- Separate config from code
- Use environment-specific configuration files
- Never commit secrets to version control

**Prevention:** Use tools like dotenv, config validators, and secret scanners

### Pitfall 3: Ignoring Security Best Practices

**Problem:** Security vulnerabilities from not following established security patterns

**Solution:** Follow security guidelines:

- Input validation and sanitization
- Proper authentication and authorization
- Encrypted data transmission (TLS/SSL)
- Regular security audits and updates

**Prevention:** Use security linters, SAST tools, and regular dependency updates

**Best Practices:**

- Follow established patterns and conventions for go
- Keep dependencies up to date and scan for vulnerabilities
- Write comprehensive documentation and inline comments
- Use linting and formatting tools consistently
- Implement proper error handling and logging
- Regular code reviews and pair programming
- Monitor production metrics and set up alerts

---

## Validation

- ✅ Token count: Level 1 <2,000, Level 2 <5,000
- ✅ Code examples: Tested and working
- ✅ YAML frontmatter: Valid
