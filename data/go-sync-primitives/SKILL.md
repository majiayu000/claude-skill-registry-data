---
name: go-sync-primitives
description: sync.WaitGroup and sync.Mutex patterns
---

# Sync Primitives

## sync.WaitGroup - Wait for Goroutines

### CORRECT
```go
func processBatch(items []string) {
    var wg sync.WaitGroup

    for _, item := range items {
        wg.Add(1) // BEFORE launching goroutine
        go func(item string) {
            defer wg.Done()
            process(item)
        }(item)
    }

    wg.Wait() // Block until all done
}
```

### WRONG - Add inside goroutine
```go
func processBatch(items []string) {
    var wg sync.WaitGroup

    for _, item := range items {
        go func(item string) {
            wg.Add(1) // WRONG: race condition
            defer wg.Done()
            process(item)
        }(item)
    }

    wg.Wait() // May return early
}
```

### WRONG - Missing variable capture
```go
func processBatch(items []string) {
    var wg sync.WaitGroup

    for _, item := range items {
        wg.Add(1)
        go func() {
            defer wg.Done()
            process(item) // WRONG: captures loop variable
        }()
    }

    wg.Wait()
}
```

## sync.Mutex - Protect Shared State

### CORRECT
```go
type Counter struct {
    mu    sync.Mutex
    value int
}

func (c *Counter) Increment() {
    c.mu.Lock()
    defer c.mu.Unlock()
    c.value++
}

func (c *Counter) Value() int {
    c.mu.Lock()
    defer c.mu.Unlock()
    return c.value
}
```

### WRONG - Unlocked access
```go
type Counter struct {
    mu    sync.Mutex
    value int
}

func (c *Counter) Increment() {
    c.mu.Lock()
    c.value++ // What if panic happens?
    c.mu.Unlock()
}

func (c *Counter) Value() int {
    return c.value // WRONG: race condition
}
```

## sync.RWMutex - Multiple Readers

```go
type Cache struct {
    mu   sync.RWMutex
    data map[string]string
}

func (c *Cache) Get(key string) (string, bool) {
    c.mu.RLock() // Multiple readers OK
    defer c.mu.RUnlock()
    val, ok := c.data[key]
    return val, ok
}

func (c *Cache) Set(key, value string) {
    c.mu.Lock() // Exclusive writer
    defer c.mu.Unlock()
    c.data[key] = value
}
```

## Rules

### WaitGroup
1. Call `Add()` before `go` statement
2. Always use `defer wg.Done()`
3. Pass loop variables as function parameters
4. One `Add(n)` can count multiple goroutines

### Mutex
1. Always use `defer mu.Unlock()`
2. Keep critical sections small
3. Don't hold locks during I/O or slow operations
4. Use RWMutex for read-heavy workloads
5. Never copy a mutex (pass by pointer)

## sync.Once - Run Exactly Once
```go
var (
    instance *Singleton
    once     sync.Once
)

func GetInstance() *Singleton {
    once.Do(func() {
        instance = &Singleton{}
    })
    return instance
}
```

## Race Detection
```bash
go test -race ./...
go run -race main.go
```
