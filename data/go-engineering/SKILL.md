---
name: go-engineering
description: Comprehensive Go engineering guidelines for writing production-quality Go code. This skill should be used when writing Go code, performing Go code reviews, working with Go tools (gopls, golangci-lint, gofmt), or answering questions about Go best practices and patterns. Applies to all Go programming tasks including implementation, refactoring, testing, and debugging.
---

# Go Engineering Excellence

This skill provides comprehensive Go engineering guidelines synthesized from authoritative sources including the Go team, Google, Uber, and experienced Go practitioners. Use this when writing or reviewing Go code for production systems.

## Core Philosophy

### Design Principles (Google Go Style)

1. **Clarity** - Code's purpose and rationale must be clear to readers
2. **Simplicity** - Accomplish goals in the simplest way possible
3. **Concision** - High signal-to-noise ratio
4. **Maintainability** - Easy for future programmers to modify correctly
5. **Consistency** - Consistent with the broader codebase

### Make Dependencies Explicit

- Never use package-level global state
- Avoid `func init()` - it exists only to modify global state
- Pass dependencies as constructor parameters, not globals
- All configuration should flow through explicit parameters

## Project Structure

### Repository Layout

```
github.com/org/project/
  cmd/
    server/
      main.go
    cli/
      main.go
  pkg/
    domain/
      domain.go
      domain_test.go
    api/
      api.go
      api_test.go
  Dockerfile
  go.mod
  go.sum
```

**Guidelines:**
- Library code goes under `pkg/` subdirectory
- Binaries go under `cmd/` subdirectory
- Always use fully-qualified import paths (never relative imports)
- Package names should be lowercase, single-word, domain-oriented
- Avoid package names like `util`, `common`, `helpers`, `models`

## Naming Conventions

### General Rules

- Use `MixedCaps` or `mixedCaps`, never `snake_case`
- Keep names proportional to scope size
- Short names (1-2 letters) acceptable for small scopes
- Longer, descriptive names for package/file scope

### Specific Conventions

**Constants:**
```go
// Good
const MaxPacketSize = 512
const (
    ExecuteBit = 1 << iota
    WriteBit
    ReadBit
)

// Bad - don't use
const MAX_PACKET_SIZE = 512  // Wrong
const kMaxBufferSize = 1024  // Wrong
```

**Functions/Methods:**
- Don't include type names: `user.ID()` not `user.GetUserID()`
- No `Get` prefix: `Owner()` not `GetOwner()`
- Avoid repetition with package: `buf.Reader` not `buf.BufReader`

**Receivers:**
- Short (1-2 letters), abbreviation of type name
- Consistent across all methods: always `u` for `User`, never mix `u` and `user`

**Initialisms:**
```go
// Good
var userID string        // ID not Id
var xmlAPI string        // API not Api
var urlPony string       // URL not Url

// Bad
var userId string
var xmlApi string
```

### Variables

**Scope-based naming:**
- Small scope (1-7 lines): `c`, `i`, `n`
- Medium scope (8-15 lines): `count`, `index`, `node`
- Large scope (15-25 lines): `userCount`, `requestIndex`
- Very large scope (>25 lines): Descriptive multi-word names

**Common conventions:**
- `r` for `io.Reader` or `*http.Request`
- `w` for `io.Writer` or `http.ResponseWriter`
- `ctx` for `context.Context`

## Code Organization

### Struct Initialization

```go
// Good - use field names, omit zero values
cfg := Config{
    Timeout: 5 * time.Second,
    MaxConn: 100,
}

// Good - inline for immediate use
client := New(Config{
    Timeout: 5 * time.Second,
    MaxConn: 100,
})

// Bad - piecemeal construction
cfg := Config{}
cfg.Timeout = 5 * time.Second
cfg.MaxConn = 100
```

### Constructor Patterns

```go
// Good - explicit dependencies
func NewService(
    logger *log.Logger,
    db *sql.DB,
    cache Cache,
) *Service {
    // Provide sensible defaults
    if logger == nil {
        logger = log.New(ioutil.Discard, "", 0)
    }

    return &Service{
        logger: logger,
        db:     db,
        cache:  cache,
    }
}

// Bad - hidden dependencies
var globalLogger *log.Logger

func NewService(db *sql.DB) *Service {
    return &Service{
        logger: globalLogger, // Hidden dependency!
        db:     db,
    }
}
```

### Interface Design

```go
// Good - small, focused interfaces
type Reader interface {
    Read(p []byte) (n int, err error)
}

type Closer interface {
    Close() error
}

type ReadCloser interface {
    Reader
    Closer
}

// Good - accept interfaces, return concrete types
func ProcessData(r io.Reader) (*Result, error) {
    // ...
}

// Bad - large, unfocused interfaces
type DataStore interface {
    Get(key string) (interface{}, error)
    Set(key string, value interface{}) error
    Delete(key string) error
    List() ([]interface{}, error)
    Count() int
    Clear() error
    // ... many more methods
}
```

## Error Handling

### Error Types

```go
// Static errors - use errors.New
var ErrNotFound = errors.New("not found")
var ErrInvalidInput = errors.New("invalid input")

// Dynamic errors - use fmt.Errorf with %w
func Open(name string) error {
    return fmt.Errorf("open %s: %w", name, ErrNotFound)
}

// Custom error types for additional context
type ValidationError struct {
    Field string
    Value interface{}
}

func (e *ValidationError) Error() string {
    return fmt.Sprintf("invalid %s: %v", e.Field, e.Value)
}
```

### Error Handling Patterns

```go
// Good - handle errors once
func process() error {
    data, err := fetch()
    if err != nil {
        return fmt.Errorf("fetch data: %w", err)
    }
    return save(data)
}

// Bad - log and return
func process() error {
    data, err := fetch()
    if err != nil {
        log.Printf("error: %v", err) // Don't do this!
        return err                    // AND this!
    }
    return save(data)
}

// Good - add context when wrapping
return fmt.Errorf("process user %s: %w", userID, err)

// Bad - generic wrappers
return fmt.Errorf("failed to process: %w", err)
```

### Error String Conventions

```go
// Good - lowercase, no punctuation
errors.New("something went wrong")
fmt.Errorf("connection failed")

// Bad
errors.New("Something went wrong.")  // Capital and period
fmt.Errorf("Connection Failed!")     // Wrong capitalization
```

## Concurrency

### Goroutine Lifecycle

```go
// Good - explicit lifecycle management
type Server struct {
    wg     sync.WaitGroup
    ctx    context.Context
    cancel context.CancelFunc
}

func (s *Server) Start() {
    s.ctx, s.cancel = context.WithCancel(context.Background())

    s.wg.Add(1)
    go func() {
        defer s.wg.Done()
        s.worker(s.ctx)
    }()
}

func (s *Server) Stop() {
    s.cancel()
    s.wg.Wait()
}

// Bad - fire and forget
func process() {
    go doSomething() // How does it stop?
}
```

### Channel Patterns

**Channels should be unbuffered or size 1:**
```go
// Good
done := make(chan struct{})        // Unbuffered
results := make(chan Result, 1)    // Size 1

// Questionable - needs strong justification
queue := make(chan Task, 100)
```

**Futures/Async-Await:**
```go
// Future pattern
future := make(chan Result, 1)
go func() { future <- compute() }()
result := <-future

// Scatter-gather
results := make(chan Result, 10)
for i := 0; i < cap(results); i++ {
    go func() {
        results <- process()
    }()
}

for i := 0; i < cap(results); i++ {
    result := <-results
    // handle result
}
```

### Mutexes

```go
// Good - zero-value mutex is valid
type Counter struct {
    mu    sync.Mutex
    count int
}

// Bad - unnecessary pointer
type Counter struct {
    mu    *sync.Mutex
    count int
}

// Bad - embedded mutex exposes Lock/Unlock
type Counter struct {
    sync.Mutex
    count int
}
```

## Context Usage

### When to Use Context

```go
// Good - context as first parameter
func ProcessRequest(ctx context.Context, req *Request) error {
    // ...
}

// Good - pass through call chain
func (s *Service) Handle(ctx context.Context) error {
    return s.process(ctx)
}

// Bad - context in struct
type Handler struct {
    ctx context.Context  // Don't do this
}

// Exception - methods matching standard library
func (c *Client) Do(req *http.Request) (*http.Response, error) {
    // OK - matching http.Client.Do signature
}
```

### Context Values

```go
// Use context for request-scoped data
type contextKey string

const requestIDKey contextKey = "request-id"

func WithRequestID(ctx context.Context, id string) context.Context {
    return context.WithValue(ctx, requestIDKey, id)
}

func RequestID(ctx context.Context) string {
    if id, ok := ctx.Value(requestIDKey).(string); ok {
        return id
    }
    return ""
}

// Don't use context to pass optional parameters
// Don't create custom context types
```

## Configuration

### Use Flags

```go
// Good - flags in main
func main() {
    var (
        addr    = flag.String("addr", ":8080", "listen address")
        timeout = flag.Duration("timeout", 30*time.Second, "request timeout")
        debug   = flag.Bool("debug", false, "enable debug mode")
    )
    flag.Parse()

    cfg := Config{
        Addr:    *addr,
        Timeout: *timeout,
        Debug:   *debug,
    }

    // Use cfg...
}

// Bad - configuration via globals
var Config struct {
    Addr string
}

func init() {
    Config.Addr = os.Getenv("ADDR")  // Don't do this
}
```

### Config Objects

```go
// Good - zero values are useful
type Config struct {
    Logger  *log.Logger  // nil = discard
    Timeout time.Duration // 0 = no timeout
    Retries int          // 0 = no retries
}

func New(cfg Config) *Service {
    if cfg.Logger == nil {
        cfg.Logger = log.New(ioutil.Discard, "", 0)
    }
    if cfg.Timeout == 0 {
        cfg.Timeout = 30 * time.Second
    }
    // ...
}
```

## Testing

ALWAYS use the testify require library for test assertions.
Try avoid require.ErrorContains and use sentinel errors in the code instead, and require.Error{Is,As} in the test.

### Table-Driven Tests

```go
func TestProcess(t *testing.T) {
    testCases := []struct {
        name            string
        input           string
        expectedResult  string
        expectedErr     bool
    }{
        {
            name:           "valid input",
            input:          "test",
            expectedResult: "TEST",
        },
        {
            name:        "empty input",
            input:       "",
            expectedErr: true,
        },
    }

    for _, tc := range testCases {
        t.Run(tc.name, func(t *testing.T) {
            result, err := Process(tc.input)
            require.Equal(t, tc.expectedErr, err != nil)
            require.Equal(t, tc.expectedResult, result)
        })
    }
}
```

### Test Helpers

```go
// Good - test helpers using require (preferred over t.Fatal)
func mustConnect(t *testing.T, dsn string) *sql.DB {
    t.Helper()
    db, err := sql.Open("postgres", dsn)
    require.NoError(t, err, "failed to connect")
    return db
}

// Good - cleanup with t.Cleanup
func TestServer(t *testing.T) {
    db := mustConnect(t, testDSN)
    t.Cleanup(func() {
        db.Close()
    })
    // test code...
}

// Good - use t.TempDir() for automatic cleanup
func createTestFile(t *testing.T, content string) string {
    t.Helper()
    tmpDir := t.TempDir() // Automatically cleaned up
    path := tmpDir + "/test.txt"
    err := os.WriteFile(path, []byte(content), 0644)
    require.NoError(t, err, "failed to write test file")
    return path
}

// Bad - using t.Fatal directly
func mustConnect(t *testing.T, dsn string) *sql.DB {
    t.Helper()
    db, err := sql.Open("postgres", dsn)
    if err != nil {
        t.Fatalf("failed to connect: %v", err) // Don't use t.Fatal - use require
    }
    return db
}
```

**Test Helper Guidelines:**
- Always call `t.Helper()` at the start of test helpers
- Use `require` assertions instead of `t.Fatal` for consistency
- Use `t.TempDir()` for temporary directories (automatic cleanup)
- Use `t.Cleanup()` for resource cleanup
- Keep helpers focused and reusable

### Mocking

```go
// Good - small interfaces for easy mocking
type Store interface {
    Get(id string) (*User, error)
}

type mockStore struct {
    users map[string]*User
}

func (m *mockStore) Get(id string) (*User, error) {
    u, ok := m.users[id]
    if !ok {
        return nil, ErrNotFound
    }
    return u, nil
}

// Test code
func TestService(t *testing.T) {
    store := &mockStore{
        users: map[string]*User{
            "1": {ID: "1", Name: "Alice"},
        },
    }
    svc := NewService(store)
    // test svc...
}
```

## Performance

### Prefer strconv over fmt

```go
// Good - fast
i := 42
s := strconv.Itoa(i)

// Bad - slow
s := fmt.Sprintf("%d", i)
```

### Specify Capacity

```go
// Good
users := make([]User, 0, len(ids))
for _, id := range ids {
    users = append(users, User{ID: id})
}

cache := make(map[string]*Value, 1000)

// Also good - when size is known exactly
results := make([]Result, len(inputs))
for i, input := range inputs {
    results[i] = process(input)
}
```

### Avoid String-to-Byte Conversions

```go
// Good - reuse bytes
var buf bytes.Buffer
for _, s := range strings {
    buf.WriteString(s)
}
result := buf.Bytes()

// Bad - repeated conversions
var result []byte
for _, s := range strings {
    result = append(result, []byte(s)...)
}
```

## Common Patterns

### Defer for Cleanup

```go
// Good
func process(filename string) error {
    f, err := os.Open(filename)
    if err != nil {
        return err
    }
    defer f.Close()

    // Process file...
    return nil
}

// Also good - with error check
defer func() {
    if err := f.Close(); err != nil {
        log.Printf("failed to close: %v", err)
    }
}()
```

### Copying Slices and Maps

```go
// Good - defensive copying when receiving
func (d *Data) SetItems(items []Item) {
    d.items = make([]Item, len(items))
    copy(d.items, items)
}

// Good - defensive copying when returning
func (d *Data) Items() []Item {
    result := make([]Item, len(d.items))
    copy(result, d.items)
    return result
}
```

### Type Assertions

```go
// Good - check success
if val, ok := x.(string); ok {
    // use val
}

// Also good - type switch
switch v := x.(type) {
case string:
    // use v as string
case int:
    // use v as int
default:
    // handle unknown type
}

// Bad - will panic on wrong type
val := x.(string)
```

## Observability

### Structured Logging

```go
// Good - structured fields
logger.Info("processing request",
    "user_id", userID,
    "duration_ms", duration.Milliseconds(),
    "status", status,
)

// Bad - string formatting
log.Printf("processing request user=%s duration=%v status=%d",
    userID, duration, status)
```

### Metrics

```go
// Good - instrument at component boundaries
type Server struct {
    requests  prometheus.Counter
    errors    prometheus.Counter
    duration  prometheus.Histogram
}

func (s *Server) Handle(w http.ResponseWriter, r *http.Request) {
    start := time.Now()
    defer func() {
        s.requests.Inc()
        s.duration.Observe(time.Since(start).Seconds())
    }()

    // Handle request...
}
```

## Anti-Patterns to Avoid

### Don't Panic

```go
// Bad - panic in library code
func process(data []byte) {
    if len(data) == 0 {
        panic("empty data")  // Don't!
    }
}

// Good - return error
func process(data []byte) error {
    if len(data) == 0 {
        return errors.New("empty data")
    }
    return nil
}

// OK - panic in main for initialization
func main() {
    db, err := sql.Open("postgres", dsn)
    if err != nil {
        panic(err)  // OK in main
    }
}
```

### Avoid Naked Returns

```go
// Bad
func compute(x int) (result int) {
    result = x * 2
    return  // Naked return - unclear
}

// Good
func compute(x int) int {
    result := x * 2
    return result
}
```

### Don't Use Import Dot

```go
// Bad
import . "fmt"

func main() {
    Println("hello")  // Unclear where Println comes from
}

// Good
import "fmt"

func main() {
    fmt.Println("hello")  // Clear
}
```

## Documentation

### Package Comments

```go
// Package auth provides authentication and authorization utilities.
//
// It supports multiple authentication backends including OAuth2,
// JWT tokens, and API keys.
package auth
```

### Function Comments

```go
// Process validates and transforms the input data.
// It returns an error if validation fails.
//
// Example usage:
//
//	result, err := Process(data)
//	if err != nil {
//		log.Fatal(err)
//	}
func Process(data []byte) (*Result, error) {
    // ...
}
```

### Guard Clauses and Early Returns

Use guard clauses (early returns) to reduce nesting and improve readability.

```go
// Good - guard clauses with early returns
func process(data []byte) error {
  if len(data) == 0 {
      return errors.New("empty data")
  }

  if !isValid(data) {
      return errors.New("invalid data")
  }

  // Main logic at base indentation level
  result := transform(data)
  return save(result)
}

// Bad - nested conditionals
func process(data []byte) error {
  if len(data) > 0 {
      if isValid(data) {
          result := transform(data)
          return save(result)
      } else {
          return errors.New("invalid data")
      }
  } else {
      return errors.New("empty data")
  }
}
```

**In loops - use early continue:**

```go
// Good - early continue
for _, item := range items {
  if item == nil {
      continue
  }
  if !item.IsValid() {
      continue
  }

  // Process valid item
  process(item)
}

// Bad - nested ifs
for _, item := range items {
  if item != nil {
      if item.IsValid() {
          process(item)
      }
  }
}
```

**Benefits:**
- Keeps happy path at minimal indentation
- Reduces cognitive load
- Makes error conditions obvious
- Easier to read top-to-bottom

**This is commonly called the "happy path" or "guard clause" pattern in Go.**

## Tooling

### Language Server

- **ALWAYS use the gopls MCP server** (`mcp-gopls`) for all Go development
- Leverage gopls capabilities: diagnostics, symbol search, file context, package API, references
- Use `go_workspace` to understand workspace structure
- Use `go_diagnostics` to check for build and analysis errors after code changes
- Use `go_file_context` to understand a file's dependencies within its package
- Use `go_symbol_references` to find all references before modifying symbol definitions

### Code Formatting

- **ALWAYS run `gofmt` after making any code changes** - this is non-negotiable
- Use `goimports` as an alternative to gofmt that also manages imports
- Format before running any other checks

### Linting with golangci-lint

**ALWAYS run golangci-lint after making code changes** before considering the work complete.

**When to run:**
- After implementing new features or bug fixes
- Before creating commits
- After refactoring
- During code review

**How to run:**
```bash
# Run on entire project
golangci-lint run

# Run on specific directory
golangci-lint run ./pkg/...

# Run on specific files
golangci-lint run path/to/file.go
```

**Handling linter output:**
1. Fix all errors - these are non-negotiable
2. Fix warnings unless there's a strong technical reason not to (document why)
3. Review info messages and apply fixes when they improve code quality
4. Never ignore linter feedback without understanding what it's flagging

**Common linters enforced:**
- `errcheck` - Unchecked errors
- `gosimple` - Simplification opportunities
- `govet` - Suspicious constructs
- `ineffassign` - Ineffectual assignments
- `staticcheck` - Advanced static analysis
- `unused` - Unused code
- `gofmt` - Formatting issues
- And many more...

### Complete Pre-commit Workflow

Run these commands in order before committing:

```bash
# 1. Format code
go fmt ./...

# 2. Run linter
golangci-lint run

# 3. Run tests
go test -v ./... -tags=sqlite -failfast

# 4. Check for build errors (if applicable)
go build ./...
```

All checks must pass before code is ready for review.

## Additional Resources

- [Effective Go](https://go.dev/doc/effective_go)
- [Go Code Review Comments](https://go.dev/wiki/CodeReviewComments)
- [Google Go Style Guide](https://google.github.io/styleguide/go/)
- [Uber Go Style Guide](https://github.com/uber-go/guide/blob/master/style.md)
- [Go Proverbs](https://go-proverbs.github.io/)

---

**Remember:** These guidelines are not absolute rules. Use judgment and adapt them to your specific context, but always favor explicitness, simplicity, and maintainability.
