---
name: go-expert
description: Deep Go expertise for concurrent systems programming. Use when writing Go code, implementing goroutines and channels, designing interfaces, handling errors.
---

# Go Expert

Specialized expertise in Go programming, providing deep guidance on concurrency patterns with goroutines and channels, interface design, error handling idioms, and building performant, idiomatic Go applications.

## When to Use This Skill

Use this skill for:

- Implementing goroutines and channels
- Designing clean interfaces
- Error handling best practices
- Writing idiomatic Go code
- Performance optimization
- Building concurrent systems
- Understanding Go's memory model

**Trigger phrases**: "golang", "go language", "goroutine", "channel", "go error handling", "go interface", "go concurrency"

## What This Skill Does

Provides Go expertise including:

- **Concurrency**: Goroutines, channels, sync primitives
- **Interface Design**: Small interfaces, composition
- **Error Handling**: Error wrapping, custom errors
- **Performance**: Profiling, optimization, memory management
- **Idioms**: Go conventions and best practices
- **Testing**: Table-driven tests, benchmarks

## Instructions

### Step 1: Master Goroutines and Channels

**Goroutine Basics**:

```go
package main

import (
    "fmt"
    "sync"
    "time"
)

// Basic goroutine
func main() {
    go func() {
        fmt.Println("Hello from goroutine")
    }()
    time.Sleep(time.Millisecond) // Don't do this in production
}

// Proper synchronization with WaitGroup
func processItems(items []string) {
    var wg sync.WaitGroup

    for _, item := range items {
        wg.Add(1)
        go func(item string) {
            defer wg.Done()
            process(item)
        }(item) // Pass item to avoid closure capture issues
    }

    wg.Wait() // Wait for all goroutines to complete
}
```

**Channel Patterns**:

```go
// Unbuffered channel - synchronous communication
func main() {
    ch := make(chan string)

    go func() {
        ch <- "hello" // Blocks until received
    }()

    msg := <-ch // Blocks until sent
    fmt.Println(msg)
}

// Buffered channel - async up to buffer size
func main() {
    ch := make(chan int, 3) // Buffer of 3
    ch <- 1 // Doesn't block
    ch <- 2
    ch <- 3
    // ch <- 4 // Would block - buffer full
}

// Channel direction in function signatures
func send(ch chan<- int) { ch <- 42 }      // Send only
func receive(ch <-chan int) { <-ch }        // Receive only
func both(ch chan int) { ch <- 1; <-ch }   // Both

// Range over channel
func main() {
    ch := make(chan int)

    go func() {
        for i := 0; i < 5; i++ {
            ch <- i
        }
        close(ch) // Must close for range to terminate
    }()

    for num := range ch {
        fmt.Println(num)
    }
}
```

### Step 2: Implement Concurrency Patterns

**Worker Pool Pattern**:

```go
func workerPool(numWorkers int, jobs <-chan Job, results chan<- Result) {
    var wg sync.WaitGroup

    for i := 0; i < numWorkers; i++ {
        wg.Add(1)
        go func(workerID int) {
            defer wg.Done()
            for job := range jobs {
                result := processJob(job)
                results <- result
            }
        }(i)
    }

    wg.Wait()
    close(results)
}

// Usage
func main() {
    jobs := make(chan Job, 100)
    results := make(chan Result, 100)

    // Start workers
    go workerPool(5, jobs, results)

    // Send jobs
    go func() {
        for _, job := range allJobs {
            jobs <- job
        }
        close(jobs)
    }()

    // Collect results
    for result := range results {
        handleResult(result)
    }
}
```

**Fan-Out/Fan-In Pattern**:

```go
// Fan-out: multiple goroutines reading from same channel
func fanOut(input <-chan int, numWorkers int) []<-chan int {
    outputs := make([]<-chan int, numWorkers)

    for i := 0; i < numWorkers; i++ {
        outputs[i] = worker(input)
    }

    return outputs
}

// Fan-in: multiple channels into one
func fanIn(channels ...<-chan int) <-chan int {
    out := make(chan int)
    var wg sync.WaitGroup

    for _, ch := range channels {
        wg.Add(1)
        go func(c <-chan int) {
            defer wg.Done()
            for val := range c {
                out <- val
            }
        }(ch)
    }

    go func() {
        wg.Wait()
        close(out)
    }()

    return out
}
```

**Select for Multiplexing**:

```go
func process(ctx context.Context, input <-chan Data) error {
    for {
        select {
        case <-ctx.Done():
            return ctx.Err() // Context cancelled
        case data, ok := <-input:
            if !ok {
                return nil // Channel closed
            }
            handleData(data)
        case <-time.After(5 * time.Second):
            return errors.New("timeout waiting for data")
        }
    }
}
```

### Step 3: Design Clean Interfaces

**Interface Best Practices**:

```go
// Small interfaces are better
type Reader interface {
    Read(p []byte) (n int, err error)
}

type Writer interface {
    Write(p []byte) (n int, err error)
}

// Compose interfaces
type ReadWriter interface {
    Reader
    Writer
}

// Accept interfaces, return structs
func ProcessData(r Reader) (*Result, error) {
    // Accept any Reader implementation
    data, err := io.ReadAll(r)
    if err != nil {
        return nil, err
    }
    return &Result{Data: data}, nil
}

// Interface segregation
// Bad: Large interface
type Database interface {
    Query(sql string) ([]Row, error)
    Insert(table string, data map[string]any) error
    Update(table string, id int, data map[string]any) error
    Delete(table string, id int) error
    Transaction(fn func(Tx) error) error
    Migrate() error
    Backup() error
}

// Good: Small, focused interfaces
type Querier interface {
    Query(sql string) ([]Row, error)
}

type Inserter interface {
    Insert(table string, data map[string]any) error
}

// Use what you need
func GetUsers(q Querier) ([]User, error) {
    rows, err := q.Query("SELECT * FROM users")
    // ...
}
```

### Step 4: Handle Errors Idiomatically

**Error Handling Patterns**:

```go
import (
    "errors"
    "fmt"
)

// Sentinel errors
var (
    ErrNotFound = errors.New("not found")
    ErrInvalid  = errors.New("invalid")
)

// Error wrapping (Go 1.13+)
func getUser(id int) (*User, error) {
    user, err := db.FindUser(id)
    if err != nil {
        return nil, fmt.Errorf("getUser(%d): %w", id, err)
    }
    return user, nil
}

// Checking wrapped errors
if errors.Is(err, ErrNotFound) {
    // Handle not found
}

// Custom error types
type ValidationError struct {
    Field   string
    Message string
}

func (e *ValidationError) Error() string {
    return fmt.Sprintf("%s: %s", e.Field, e.Message)
}

// Check for custom error type
var validErr *ValidationError
if errors.As(err, &validErr) {
    fmt.Printf("Validation failed for %s\n", validErr.Field)
}

// Multiple error handling pattern
func processAll(items []Item) error {
    var errs []error

    for _, item := range items {
        if err := process(item); err != nil {
            errs = append(errs, fmt.Errorf("item %d: %w", item.ID, err))
        }
    }

    if len(errs) > 0 {
        return errors.Join(errs...) // Go 1.20+
    }
    return nil
}
```

### Step 5: Write Idiomatic Go

**Go Idioms**:

```go
// Defer for cleanup
func processFile(path string) error {
    f, err := os.Open(path)
    if err != nil {
        return err
    }
    defer f.Close() // Always executed when function returns

    // Process file...
    return nil
}

// Struct embedding for composition
type Logger struct{}
func (l *Logger) Log(msg string) { fmt.Println(msg) }

type Server struct {
    *Logger // Embedded - Server now has Log method
    port int
}

// Named return values (use sparingly)
func divide(a, b float64) (result float64, err error) {
    if b == 0 {
        err = errors.New("division by zero")
        return // Returns named values
    }
    result = a / b
    return
}

// Functional options pattern
type Server struct {
    host    string
    port    int
    timeout time.Duration
}

type Option func(*Server)

func WithPort(port int) Option {
    return func(s *Server) { s.port = port }
}

func WithTimeout(d time.Duration) Option {
    return func(s *Server) { s.timeout = d }
}

func NewServer(host string, opts ...Option) *Server {
    s := &Server{
        host:    host,
        port:    8080,           // Default
        timeout: 30 * time.Second, // Default
    }
    for _, opt := range opts {
        opt(s)
    }
    return s
}

// Usage
server := NewServer("localhost",
    WithPort(9000),
    WithTimeout(time.Minute),
)
```

### Step 6: Optimize Performance

**Performance Patterns**:

```go
// Pre-allocate slices when size is known
func processItems(items []Item) []Result {
    results := make([]Result, 0, len(items)) // Capacity hint
    for _, item := range items {
        results = append(results, process(item))
    }
    return results
}

// Use sync.Pool for frequent allocations
var bufPool = sync.Pool{
    New: func() any {
        return new(bytes.Buffer)
    },
}

func process(data []byte) {
    buf := bufPool.Get().(*bytes.Buffer)
    defer func() {
        buf.Reset()
        bufPool.Put(buf)
    }()

    buf.Write(data)
    // Use buffer...
}

// Avoid string concatenation in loops
func buildString(parts []string) string {
    var sb strings.Builder
    sb.Grow(estimatedSize) // Pre-allocate if known

    for _, part := range parts {
        sb.WriteString(part)
    }
    return sb.String()
}

// Use sync.Map for concurrent map access
var cache sync.Map

func get(key string) (value any, ok bool) {
    return cache.Load(key)
}

func set(key string, value any) {
    cache.Store(key, value)
}

// Benchmark your code
func BenchmarkProcess(b *testing.B) {
    data := generateTestData()
    b.ResetTimer()

    for i := 0; i < b.N; i++ {
        process(data)
    }
}
```

### Step 7: Write Effective Tests

**Table-Driven Tests**:

```go
func TestAdd(t *testing.T) {
    tests := []struct {
        name     string
        a, b     int
        expected int
    }{
        {"positive", 2, 3, 5},
        {"negative", -1, -1, -2},
        {"zero", 0, 0, 0},
        {"mixed", -1, 1, 0},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            result := Add(tt.a, tt.b)
            if result != tt.expected {
                t.Errorf("Add(%d, %d) = %d; want %d",
                    tt.a, tt.b, result, tt.expected)
            }
        })
    }
}

// Testing with subtests and parallel execution
func TestParallel(t *testing.T) {
    tests := []struct{ name, input, want string }{
        // test cases...
    }

    for _, tt := range tests {
        tt := tt // Capture range variable
        t.Run(tt.name, func(t *testing.T) {
            t.Parallel() // Run in parallel
            got := Process(tt.input)
            if got != tt.want {
                t.Errorf("got %q; want %q", got, tt.want)
            }
        })
    }
}

// Test helpers
func setupTest(t *testing.T) (*DB, func()) {
    t.Helper() // Mark as test helper

    db := createTestDB()
    cleanup := func() {
        db.Close()
    }
    return db, cleanup
}

func TestWithHelper(t *testing.T) {
    db, cleanup := setupTest(t)
    defer cleanup()

    // Use db...
}
```

## Best Practices

- **Accept interfaces, return structs** - Flexibility in, concrete out
- **Small interfaces** - Prefer single-method interfaces
- **Handle errors immediately** - Don't ignore them
- **Use context for cancellation** - Pass context as first param
- **Avoid naked returns** - Except for short functions
- **Don't overuse goroutines** - They have overhead
- **Close channels from sender** - Never from receiver
- **Use go vet and staticcheck** - Catch common mistakes

## Common Patterns

### Pattern 1: Context Propagation

```go
func handler(w http.ResponseWriter, r *http.Request) {
    ctx := r.Context()

    result, err := doWork(ctx)
    if err != nil {
        if errors.Is(err, context.Canceled) {
            return // Client disconnected
        }
        http.Error(w, err.Error(), 500)
        return
    }

    json.NewEncoder(w).Encode(result)
}

func doWork(ctx context.Context) (*Result, error) {
    ctx, cancel := context.WithTimeout(ctx, 5*time.Second)
    defer cancel()

    resultCh := make(chan *Result, 1)
    errCh := make(chan error, 1)

    go func() {
        result, err := expensiveOperation()
        if err != nil {
            errCh <- err
            return
        }
        resultCh <- result
    }()

    select {
    case <-ctx.Done():
        return nil, ctx.Err()
    case err := <-errCh:
        return nil, err
    case result := <-resultCh:
        return result, nil
    }
}
```

### Pattern 2: Graceful Shutdown

```go
func main() {
    srv := &http.Server{Addr: ":8080"}

    // Start server
    go func() {
        if err := srv.ListenAndServe(); err != http.ErrServerClosed {
            log.Fatalf("Server error: %v", err)
        }
    }()

    // Wait for interrupt
    quit := make(chan os.Signal, 1)
    signal.Notify(quit, os.Interrupt, syscall.SIGTERM)
    <-quit

    // Graceful shutdown
    ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
    defer cancel()

    if err := srv.Shutdown(ctx); err != nil {
        log.Fatalf("Shutdown error: %v", err)
    }
    log.Println("Server stopped gracefully")
}
```

## Quality Checklist

- [ ] All errors handled (no _ = err)
- [ ] Context passed and respected
- [ ] Goroutines properly synchronized
- [ ] Channels closed by sender
- [ ] go vet passes
- [ ] staticcheck passes
- [ ] Tests are table-driven
- [ ] Benchmarks for hot paths

## Related Skills

- `performance-testing` - Go benchmarking
- `cicd-architect` - Go CI/CD pipelines
- `code-quality` - Go code standards
- `kubernetes-expert` - Go microservices on K8s

---

**Version**: 1.0.0
**Last Updated**: January 2026
**Based on**: Effective Go, awesome-claude-code-subagents patterns


### Iterative Refinement Strategy
This skill is optimized for an iterative approach:
1. **Execute**: Perform the core steps defined above.
2. **Review**: Critically analyze the output (coverage, quality, completeness).
3. **Refine**: If targets aren't met, repeat the specific implementation steps with improved context.
4. **Loop**: Continue until the definition of done is satisfied.
