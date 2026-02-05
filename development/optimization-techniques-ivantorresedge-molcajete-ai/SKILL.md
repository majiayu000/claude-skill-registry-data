---
name: optimization-techniques
description: Performance optimization strategies. Use ONLY after profiling identifies bottlenecks.
---

# Optimization Techniques Skill

Performance optimization strategies for Go. **ONLY use after profiling!**

## When to Use

Use ONLY after profiling identifies actual bottlenecks. **NEVER optimize prematurely (KISS principle).**

## Pre-allocate Slices

```go
// Good - pre-allocate when size known
items := make([]Item, 0, expectedSize)

// Bad - repeated allocations
var items []Item
```

## Use strings.Builder

```go
// Good
var b strings.Builder
for _, s := range strings {
    b.WriteString(s)
}
result := b.String()

// Bad - repeated allocations
result := ""
for _, s := range strings {
    result += s
}
```

## sync.Pool for Reusable Objects

```go
var bufferPool = sync.Pool{
    New: func() interface{} {
        return new(bytes.Buffer)
    },
}

buf := bufferPool.Get().(*bytes.Buffer)
defer bufferPool.Put(buf)
buf.Reset()
// use buf
```

## Minimize Allocations

```go
// Good - reuse buffer
buf := make([]byte, 1024)
for {
    n, _ := r.Read(buf)
    process(buf[:n])
}

// Bad - allocate each time
for {
    buf := make([]byte, 1024)
    n, _ := r.Read(buf)
    process(buf[:n])
}
```

## Golden Rules

1. **Profile first** - Don't guess
2. **Measure impact** - Benchmark before/after
3. **KISS principle** - Simple first, optimize later
4. **Maintain readability** - Don't sacrifice clarity
5. **Focus on hot paths** - 80/20 rule
