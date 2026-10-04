---
name: go-samber-ro
description: "Reactive programming in Go with samber/ro. Covers streams, observables, observers, and type-safe operators."
metadata:
  model: models/gemini-3.1-pro-preview
  last_modified: Wed, 06 May 2026 07:30:00 GMT
---

## Core Philosophy

`samber/ro` is a Go implementation of **ReactiveX** (Reactive Extensions). It provides a way to compose asynchronous and event-based programs using observable sequences.

- **Asynchronous**: Handles streams of data that arrive over time (e.g., WebSockets, tickers).
- **Type-safe**: Uses Go Generics for all operators.
- **Composable**: Chain operators to filter, transform, and combine streams.
- **Backpressure**: Built-in mechanisms to handle producers that are faster than consumers.

## Core Components

1. **Observable**: The data source that emits a sequence of items.
2. **Observer**: The consumer that reacts to items (`OnNext`), errors (`OnError`), and completion (`OnComplete`).
3. **Operators**: Functions like `Map`, `Filter`, `Merge`, and `Debounce` that transform the stream.
4. **Subscription**: Represents the connection between an observer and an observable. Use it to cancel the stream.

## Basic Usage

### Creating a Stream
```go
import "github.com/samber/ro"

observable := ro.Pipe2(
    ro.FromSlice([]int{1, 2, 3, 4, 5}),
    ro.Filter(func(x int) bool { return x%2 == 0 }),
    ro.Map(func(x int) string { return fmt.Sprintf("value: %d", x) }),
)
```

### Subscribing
```go
observable.Subscribe(ro.NewObserver(
    func(s string) { fmt.Println(s) },       // OnNext
    func(err error) { log.Fatal(err) },      // OnError
    func() { fmt.Println("Completed!") },    // OnComplete
))
```

## Common Operators

| Category | Operators |
| --- | --- |
| **Creation** | `Just`, `FromSlice`, `FromChannel`, `Interval`, `Range`. |
| **Filtering** | `Filter`, `Distinct`, `Debounce`, `Throttle`, `Take`, `Skip`. |
| **Transformation** | `Map`, `FlatMap`, `Scan`, `Buffer`. |
| **Combination** | `Merge`, `Zip`, `CombineLatest`, `Concat`. |
| **Error Handling** | `Catch`, `Retry`, `OnErrorReturn`. |

## Why use `ro`?

- **Declarative**: Focus on *what* should happen to the data rather than *how* to manage goroutines and channels.
- **Complex Coordination**: Easily combine multiple async sources (e.g., "Wait for both a DB result and an API response before proceeding").
- **Time-Aware**: Operators like `Debounce` and `Interval` make handling time-based logic trivial.
- **Consistency**: Follows a well-known pattern used in many other languages (RxJS, RxJava, etc.).

## Best Practices

1. **Always Handle Errors** — Use `NewObserver` with all three callbacks to ensure errors don't go unnoticed.
2. **Unsubscribe** — Always clean up subscriptions (or use `TakeUntil`) to prevent goroutine leaks.
3. **Cold vs Hot** — Understand that by default, each subscriber gets a fresh execution. Use `Share()` to multicasts a single execution to multiple subscribers.
4. **Use Typed Pipes** — Prefer `Pipe2`, `Pipe3`, etc., for better compile-time type checking.
5. **Context Integration** — Use `ContextWithTimeout` to automatically terminate streams when a Go context expires.

## Anti-patterns

- ❌ **Using `ro` for simple Slices** — If your data is finite and already in memory, use `samber/lo`. `ro` is for data over time.
- ❌ **Ignoring `OnComplete`** — Some operators or logic might depend on the stream finishing; don't forget to implement the completion callback.
- ❌ **Manual Channel Management** — If you're using `ro`, try to stay within its ecosystem rather than manually piping channels in and out.
- ❌ **Deep Nesting** — Keep your pipelines readable by breaking them into smaller, named observables.
