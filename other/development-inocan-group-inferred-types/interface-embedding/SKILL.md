---
name: interface-embedding
description: Compose interfaces through embedding for flexible contracts
---

# Interface Embedding Patterns

Go interfaces can embed other interfaces to create larger contracts. Use this for composition, not inheritance.

## Basic Embedding

**CORRECT** - Compose small interfaces
```go
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

// Any type implementing both Reader and Closer satisfies ReadCloser
```

**WRONG** - Giant interface instead of composition
```go
type FileHandler interface {
    Read(p []byte) (n int, err error)
    Write(p []byte) (n int, err error)
    Close() error
    Seek(offset int64, whence int) (int64, error)
    // Kitchen sink approach
}
```

## Practical Patterns

**Progressive enhancement:**
```go
type BasicCache interface {
    Get(key string) ([]byte, error)
    Set(key string, val []byte) error
}

type ExpiringCache interface {
    BasicCache
    SetWithTTL(key string, val []byte, ttl time.Duration) error
}

func UseCache(c BasicCache) { /* Works with any cache */ }
func UseAdvanced(c ExpiringCache) { /* Needs TTL support */ }
```

**Optional behavior detection:**
```go
type Processor interface {
    Process(data []byte) error
}

type BatchProcessor interface {
    Processor
    ProcessBatch(items [][]byte) error
}

func Handle(p Processor, items [][]byte) error {
    if bp, ok := p.(BatchProcessor); ok {
        return bp.ProcessBatch(items) // Use batch if available
    }
    // Fallback to individual processing
    for _, item := range items {
        if err := p.Process(item); err != nil {
            return err
        }
    }
    return nil
}
```

## Guidelines

- Embed to compose small, focused interfaces
- Keep embedded interfaces from stdlib or well-known packages
- Use type assertions to detect optional capabilities
- Avoid deep embedding hierarchies (2-3 levels max)
