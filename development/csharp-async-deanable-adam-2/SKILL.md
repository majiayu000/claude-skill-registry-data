---
name: csharp-async
description: >
  Best practices and patterns for C# async/await programming including Task and ValueTask usage,
  CancellationToken propagation, IAsyncDisposable and await using, ConfigureAwait, async streams
  (IAsyncEnumerable), parallel task execution, and common pitfalls like deadlocks and async void.
  Use this skill whenever writing, reviewing, or refactoring asynchronous C# code — including when
  the user mentions async methods, Task-returning APIs, cancellation, deadlocks, blocking on async
  code, or resource disposal in async contexts, even if they do not explicitly say "async best
  practices."
user-invocable: false
---

# C# Async Programming Best Practices

Apply these practices when writing, reviewing, or refactoring asynchronous C# code.

## Naming Conventions

- Suffix all async methods with `Async` (e.g., `GetDataAsync` for a synchronous `GetData`)
- Match names with synchronous counterparts when both exist

## Return Types

- Return `Task<T>` when the method produces a value
- Return `Task` when the method has no return value
- Use `ValueTask<T>` when the method frequently completes synchronously (e.g., cache hits, short-circuit returns) — this avoids a `Task` heap allocation on the hot path
- Never return `async void` except in event handlers — `async void` methods swallow exceptions and cannot be awaited, making errors invisible to the caller

## CancellationToken Propagation

CancellationTokens are the cooperative cancellation mechanism in .NET. Dropping a token silently means the user loses the ability to cancel an operation that might be long-running or expensive.

- Accept `CancellationToken` as the **last parameter** in every async method signature
- Always forward the token through the entire call chain — never silently drop it
- Pass tokens to every framework method that accepts one (`HttpClient`, `Stream`, `DbCommand`, `Channel`, EF Core queries, etc.)
- Use `token.ThrowIfCancellationRequested()` inside long-running CPU loops to make them responsive to cancellation
- Catch `OperationCanceledException` at boundary layers (API controllers, hosted service entry points) — do not swallow it or rethrow as a different exception type
- Use `CancellationTokenSource.CreateLinkedTokenSource()` to combine scopes — for instance, merging a request-scoped token with a user-initiated cancel:

```csharp
using var linkedCts = CancellationTokenSource.CreateLinkedTokenSource(requestToken, userCancelToken);
await ProcessAsync(linkedCts.Token);
```

## Exception Handling

- Wrap `await` expressions in try/catch to handle faulted tasks
- Do not swallow exceptions — log and rethrow or convert to a domain-specific error
- Use `Task.FromException<T>()` (or `ValueTask.FromException`) to return a pre-faulted task instead of throwing before the first `await` in a task-returning method — this keeps the caller's exception-handling path consistent
- In library code, use `ConfigureAwait(false)` after every `await` to avoid capturing the synchronization context (see ConfigureAwait section below)

## ConfigureAwait

The `ConfigureAwait` decision depends on where your code runs:

- **Library code** (NuGet packages, shared class libraries): use `.ConfigureAwait(false)` on every `await`. Library code should not assume a synchronization context exists, and capturing one unnecessarily can cause deadlocks when callers block with `.Result` or `.Wait()`.
- **Application-level code** (ASP.NET Core controllers, Blazor components, console apps): omit `ConfigureAwait(false)`. ASP.NET Core has no `SynchronizationContext`, so it is a no-op there, but in UI frameworks (WPF, WinForms, MAUI) the default behavior of resuming on the UI thread is what you want.

## Parallel and Concurrent Execution

- Use `Task.WhenAll()` to run independent tasks concurrently and await all of them
- Use `Task.WhenAny()` for racing tasks (e.g., timeout patterns, first-response-wins)
- Avoid unnecessary `async`/`await` when the method simply returns another task — just return the `Task` directly (but keep `async` if you need try/catch or `using` around the await)
- Use `Task.Run()` only to offload CPU-bound work to the thread pool — never wrap purely async I/O in `Task.Run()`

## Async Streams (IAsyncEnumerable)

Use `IAsyncEnumerable<T>` to produce or consume sequences of data asynchronously (e.g., database cursor results, paginated API calls, streaming file reads):

```csharp
async IAsyncEnumerable<Item> GetItemsAsync(
    [EnumeratorCancellation] CancellationToken ct = default)
{
    await foreach (var row in db.QueryAsync(ct))
    {
        yield return Map(row);
    }
}
```

- Apply `[EnumeratorCancellation]` to the `CancellationToken` parameter so callers can pass a token via `WithCancellation()`
- Use `await foreach` to consume async streams

## Resource Disposal (IAsyncDisposable)

When a resource performs I/O during cleanup (flushing buffers, closing network connections), use async disposal to avoid blocking a thread:

- Implement `IAsyncDisposable` on classes that hold async resources (database connections, HTTP clients, streams)
- Prefer `await using` over `using` whenever the type implements `IAsyncDisposable`:

```csharp
await using var connection = new SqlConnection(connectionString);
await connection.OpenAsync(cancellationToken);
```

- If a class implements both `IDisposable` and `IAsyncDisposable`, `await using` will call `DisposeAsync()` — which is the one you want in async code paths

## Async Synchronization

Standard locks (`lock`, `Monitor`) cannot be held across an `await` because the continuation may run on a different thread. Use async-aware synchronization primitives instead:

- Use `SemaphoreSlim` (with `await semaphore.WaitAsync(ct)`) as an async-compatible mutex or throttle
- Use `Channel<T>` for async producer-consumer patterns — it is allocation-efficient and back-pressure-aware

## Common Pitfalls

| Anti-pattern | Why it is dangerous |
|---|---|
| `.Wait()`, `.Result`, `.GetAwaiter().GetResult()` | Blocks the calling thread and can deadlock when a `SynchronizationContext` exists. Use `await` instead. |
| `async void` methods (non-event-handler) | Exceptions go unobserved and crash the process. Return `Task` so the caller can await and catch. |
| Mixing sync and async | Calling async from sync (or vice versa) introduces deadlock risk and thread-pool starvation. Keep the call chain consistently async. |
| Forgetting to await a Task | The task runs fire-and-forget; exceptions are silently lost and execution order becomes unpredictable. |
| `Task.Run()` wrapping async I/O | Wastes a thread-pool thread that just waits on I/O. Call the async method directly. |

## Implementation Patterns

- **TAP (Task-based Asynchronous Pattern)**: the standard for public async APIs in .NET — return `Task`/`Task<T>` and accept a `CancellationToken`
- **Async command pattern**: for long-running operations that need progress reporting and cancellation
- **Async factory methods**: when construction requires async work (e.g., opening a connection), expose a static `CreateAsync()` method rather than doing async work in the constructor

When reviewing C# code, identify async anti-patterns from this guide and suggest concrete improvements with corrected code.
