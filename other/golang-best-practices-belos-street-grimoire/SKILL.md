---
name: golang-best-practices
description: MUST be used for Go tasks. Covers Go 1.21+, standard library, Go modules, concurrency, performance optimization, testing, and WebAssembly (GOOS=js, GOARCH=wasm). Load for any .go files work.
license: MIT
metadata:
  author: github.com/belos-street
  version: "1.0.0"
---

Go best practices, common gotchas, and performance optimization. Includes WebAssembly development.

### Project & Package
- Standard Go project layout → See [standard-go-project-layout](references/standard-go-project-layout.md)
- Go modules and dependency management → See [go-mod-dependency-management](references/go-mod-dependency-management.md)
- Go naming conventions → See [go-naming-conventions](references/go-naming-conventions.md)

### Error Handling
- Go-style error handling patterns → See [error-handling-patterns](references/error-handling-patterns.md)
- Sentinel errors and error wrapping → See [error-sentinel-wrapping](references/error-sentinel-wrapping.md)
- Recover and panic best practices → See [error-recover-panic](references/error-recover-panic.md)

### Types & Memory
- Value types vs pointers → See [value-type-vs-pointer](references/value-type-vs-pointer.md)
- Understanding nil in Go → See [go-nil-handling](references/go-nil-handling.md)
- Memory management and GC → See [memory-management-gc](references/memory-management-gc.md)
- Escape analysis → See [escape-analysis](references/escape-analysis.md)

### Concurrency
- Goroutine lifecycle management → See [goroutine-lifecycle](references/goroutine-lifecycle.md)
- Channel patterns → See [channel-patterns](references/channel-patterns.md)
- Sync primitives (Mutex, RWMutex, Atomic) → See [sync-primitives](references/sync-primitives.md)
- Common concurrency pitfalls → See [concurrency-pitfalls](references/concurrency-pitfalls.md)

### Interfaces
- Interface design principles → See [interface-design](references/interface-design.md)
- Dependency injection → See [dependency-injection](references/dependency-injection.md)
- Interface and nil → See [interface-nil](references/interface-nil.md)

### Performance
- String and []byte optimization → See [string-byte-optimization](references/string-byte-optimization.md)
- Slice tips and tricks → See [slice-optimization](references/slice-optimization.md)
- Map optimization → See [map-optimization](references/map-optimization.md)
- Profiling with pprof → See [pprof-usage](references/pprof-usage.md)

### Testing
- Table-driven tests → See [table-driven-tests](references/table-driven-tests.md)
- Mocking techniques → See [go-mocking](references/go-mocking.md)
- Benchmarking → See [benchmarking](references/benchmarking.md)

### Tooling
- Linting and formatting → See [linting-formatting](references/linting-formatting.md)
- Documentation with godoc → See [godoc-best-practices](references/godoc-best-practices.md)
- Build tags and conditional compilation → See [build-tags](references/build-tags.md)

### WebAssembly
- WASM basics and compilation → See [wasm-basics](references/wasm-basics.md)
- JS interop with wasm_exec → See [wasm-js-interop](references/wasm-js-interop.md)
- DOM manipulation → See [wasm-dom-manipulation](references/wasm-dom-manipulation.md)
- Memory management in WASM → See [wasm-memory-management](references/wasm-memory-management.md)
- Callbacks and async → See [wasm-callbacks-async](references/wasm-callbacks-async.md)
- WASM performance considerations → See [wasm-performance](references/wasm-performance.md)
- Debugging WASM → See [wasm-debugging](references/wasm-debugging.md)
- Practical WASM use cases → See [wasm-use-cases](references/wasm-use-cases.md)

### Common Gotchas
- Loop variable closure → See [loop-variable-closure](references/loop-variable-closure.md)
- Slice append behavior → See [slice-append-behavior](references/slice-append-behavior.md)
- time.After memory leak → See [time-after-leak](references/time-after-leak.md)
- HTTP client timeouts → See [http-client-timeouts](references/http-client-timeouts.md)
