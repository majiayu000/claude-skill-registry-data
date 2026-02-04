---
name: csharp-dotnet-debugging
description: |
  Expert .NET 10 Debugging Strategist using CLI-first diagnosis.
  
  Use when user encounters:
  - Bugs, errors, exceptions in .NET/C# applications
  - Performance issues (slow, high CPU, memory leaks)
  - Crashes, deadlocks, race conditions
  - Need root cause analysis
  
  Triggers: "debug", "error", "exception", "crash", "memory leak", "high CPU",
  "performance", "dotnet-dump", "dotnet-counters", "stack trace", "NullReferenceException",
  "deadlock", "race condition", "OutOfMemoryException", "slow", "timeout"
---

# .NET 10 Debugging Strategy Guide

CLI-first debugging for .NET 10 applications. Provide root cause analysis, not just fixes.

## Debugging Workflow

1. **Diagnose** - Identify the problem type
2. **Analyze** - Use appropriate CLI tools
3. **Fix** - Apply the correct solution
4. **Guard** - Prevent recurrence

## Quick Diagnosis Matrix

| Symptom | Tool | Command |
|---------|------|---------|
| High CPU | dotnet-counters | `dotnet-counters monitor -p <PID> --counters System.Runtime` |
| Memory Leak | dotnet-gcdump | `dotnet-gcdump collect -p <PID>` |
| Crash | dotnet-dump | `dotnet-dump collect -p <PID>` |
| Slow Response | dotnet-trace | `dotnet-trace collect -p <PID>` |
| Deadlock | dotnet-stack | `dotnet-stack report -p <PID>` |

## Common Exceptions & Fixes

### NullReferenceException

**Root Cause**: Accessing member on null object.

```csharp
// ❌ Problem
var name = user.Profile.DisplayName; // Profile could be null

// ✅ Fix: Null-conditional + null-coalescing
var name = user?.Profile?.DisplayName ?? "Anonymous";

// ✅ Guard: Required properties
public class User
{
    public required Profile Profile { get; init; }
}
```

### ObjectDisposedException

**Root Cause**: Using disposed resource, often from closure capturing.

```csharp
// ❌ Problem: Closure captures disposed DbContext
public async Task<List<User>> GetUsersAsync()
{
    using var db = new AppDbContext();
    return await Task.Run(() => db.Users.ToList()); // db disposed before Task runs
}

// ✅ Fix: Await inside using scope
public async Task<List<User>> GetUsersAsync()
{
    await using var db = new AppDbContext();
    return await db.Users.ToListAsync();
}
```

### InvalidOperationException (Collection Modified)

**Root Cause**: Modifying collection during enumeration.

```csharp
// ❌ Problem
foreach (var item in items)
{
    if (item.ShouldRemove)
        items.Remove(item);
}

// ✅ Fix: ToList() to create snapshot, or use RemoveAll
items.RemoveAll(x => x.ShouldRemove);

// Or filter to new list
items = items.Where(x => !x.ShouldRemove).ToList();
```

### TaskCanceledException

**Root Cause**: Operation cancelled or timed out.

```csharp
// ✅ Proper handling
try
{
    await httpClient.GetAsync(url, ct);
}
catch (TaskCanceledException) when (ct.IsCancellationRequested)
{
    logger.LogInformation("Operation cancelled by user");
    throw;
}
catch (TaskCanceledException)
{
    logger.LogWarning("Operation timed out");
    throw new TimeoutException($"Request to {url} timed out");
}
```

### Deadlock (async/await)

**Root Cause**: Blocking on async code in synchronization context.

```csharp
// ❌ Problem: .Result blocks, waiting for context
public string GetData()
{
    return GetDataAsync().Result; // DEADLOCK in ASP.NET/WinForms
}

// ✅ Fix: Async all the way
public async Task<string> GetDataAsync()
{
    return await httpClient.GetStringAsync(url);
}

// ✅ If sync required: ConfigureAwait(false)
public string GetData()
{
    return GetDataAsync().ConfigureAwait(false).GetAwaiter().GetResult();
}
```

## CLI Debugging Tools

### dotnet-counters (Real-time Metrics)

```bash
# Install
dotnet tool install -g dotnet-counters

# Monitor runtime metrics
dotnet-counters monitor -p <PID> --counters System.Runtime

# Key metrics to watch:
# - CPU Usage (%)
# - Working Set (MB)
# - GC Heap Size (MB)
# - Gen 0/1/2 GC Count
# - Exception Count
# - ThreadPool Queue Length
```

### dotnet-dump (Crash Analysis)

```bash
# Install
dotnet tool install -g dotnet-dump

# Collect dump
dotnet-dump collect -p <PID>

# Analyze
dotnet-dump analyze <dump-file>

# Useful SOS commands:
> clrstack          # Current thread stack
> clrthreads        # All managed threads
> dumpheap -stat    # Heap statistics
> dumpheap -type MyClass  # Find specific type instances
> gcroot <address>  # Find what's keeping object alive
```

### dotnet-gcdump (Memory Analysis)

```bash
# Install
dotnet tool install -g dotnet-gcdump

# Collect GC dump (lighter than full dump)
dotnet-gcdump collect -p <PID>

# Analyze with VS or dotnet-gcdump report
dotnet-gcdump report <gcdump-file>
```

### dotnet-trace (Performance Tracing)

```bash
# Install
dotnet tool install -g dotnet-trace

# Collect trace with default providers
dotnet-trace collect -p <PID> --duration 00:00:30

# Collect with specific providers
dotnet-trace collect -p <PID> --providers Microsoft-DotNETCore-SampleProfiler

# Convert to speedscope format
dotnet-trace convert <trace-file> --format speedscope
```

### dotnet-stack (Thread Stacks)

```bash
# Install
dotnet tool install -g dotnet-stack

# Report all thread stacks (great for deadlock detection)
dotnet-stack report -p <PID>
```

## Memory Leak Detection

### Step 1: Identify Growing Memory

```bash
dotnet-counters monitor -p <PID> --counters System.Runtime[gc-heap-size]
```

### Step 2: Capture GC Dumps

```bash
# Take baseline
dotnet-gcdump collect -p <PID> -o baseline.gcdump

# Wait for memory growth...

# Take second dump
dotnet-gcdump collect -p <PID> -o after.gcdump
```

### Step 3: Compare Dumps

```bash
# In dotnet-dump analyze
> dumpheap -stat
# Look for types with unexpectedly high counts/sizes
```

### Common Leak Patterns

```csharp
// ❌ Event handler not unsubscribed
button.Click += OnClick;
// Memory leak if button outlives subscriber

// ✅ Fix: Unsubscribe in Dispose
public void Dispose()
{
    button.Click -= OnClick;
}

// ❌ Static collection growing
static List<Request> _requests = new();

// ✅ Fix: Use bounded collection or clear periodically
static ConcurrentQueue<Request> _requests = new();
```

## High CPU Diagnosis

### Step 1: Identify CPU Usage

```bash
dotnet-counters monitor -p <PID> --counters System.Runtime[cpu-usage]
```

### Step 2: Collect Trace

```bash
dotnet-trace collect -p <PID> --profile cpu-sampling --duration 00:00:30
```

### Step 3: Analyze Hot Paths

Open trace file in Visual Studio, PerfView, or convert to speedscope:

```bash
dotnet-trace convert trace.nettrace --format speedscope
# Open https://speedscope.app and load the JSON
```

## Guard Patterns (Prevention)

### Result Pattern (Avoid Exceptions for Flow Control)

```csharp
public record Result<T>
{
    public bool IsSuccess { get; }
    public T? Value { get; }
    public string? Error { get; }
    
    private Result(bool success, T? value, string? error)
    {
        IsSuccess = success;
        Value = value;
        Error = error;
    }
    
    public static Result<T> Success(T value) => new(true, value, null);
    public static Result<T> Failure(string error) => new(false, default, error);
}
```

### Guard Clauses

```csharp
public class UserService(IUserRepository repo)
{
    public async Task<User> GetUserAsync(int id, CancellationToken ct)
    {
        ArgumentOutOfRangeException.ThrowIfNegativeOrZero(id);
        
        var user = await repo.GetByIdAsync(id, ct)
            ?? throw new NotFoundException($"User {id} not found");
        
        return user;
    }
}
```

### Defensive Async

```csharp
// Always pass CancellationToken
public async Task ProcessAsync(CancellationToken ct = default)
{
    ct.ThrowIfCancellationRequested();
    
    await using var connection = await OpenConnectionAsync(ct);
    // ...
}
```

## Resources

- **Detailed diagnosis workflows**: See `references/diagnosis-workflows.md`
- **Exception patterns**: See `references/exception-patterns.md`
