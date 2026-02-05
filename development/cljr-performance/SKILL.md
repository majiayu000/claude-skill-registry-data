---
name: cljr-performance
description: Optimize Cljr compiler and runtime performance. Use when optimizing emitter output, runtime collections, REPL evaluation, or leveraging .NET 10/C# 14 features. Covers Span<T>, FrozenDictionary, AggressiveInlining, benchmarking, and allocation reduction strategies.
---

# Cljr Performance Optimization

This skill guides performance optimization for the Cljr Clojure-to-.NET compiler, targeting .NET 10 with C# 14 preview features.

## When to use this skill

- Optimizing emitter-generated C# code
- Improving runtime collection performance
- Reducing memory allocations
- Leveraging .NET 10 / C# 14 performance features
- Writing or analyzing benchmarks
- Optimizing REPL evaluation performance

## Project Performance Profile

### Target Framework
- **Runtime**: .NET 10 (LTS)
- **Language**: C# 14 preview (Runtime, CLI, REPL) / C# 12 (Compiler, SourceGenerator)

### Existing Optimizations

| Optimization | Status | Location |
|--------------|--------|----------|
| `Span<T>` / `ReadOnlySpan<T>` | ✓ | PersistentVector |
| `FrozenDictionary` | ✓ | Protocol, MethodImplCache |
| `[AggressiveInlining]` | ✓ | Hot paths throughout |
| Symbol/Keyword interning | ✓ | Symbol.cs, Keyword.cs |
| HAMT with SIMD PopCount | ✓ | PersistentHashMap |
| 32-way trie | ✓ | PersistentVector |
| Transient collections | ✓ | Vector, HashMap batch ops |
| Method dispatch caching | ✓ | MultiFn, Protocol |
| BenchmarkDotNet suite | ✓ | tests/Cljr.Benchmarks/ |

### Opportunities for Further Optimization

| Optimization | Status | Potential Use |
|--------------|--------|---------------|
| `stackalloc` | ✗ | Small temp arrays in hot paths |
| `ArrayPool<T>` | ✗ | Reusable buffer arrays |
| `SearchValues<T>` | ✗ | Character/byte searching |
| `CompositeFormat` | ✗ | String formatting |
| C# 14 implicit span conversions | ✗ | Cleaner span APIs |
| AVX10.2 intrinsics | ✗ | SIMD operations |

## Performance Optimization Workflow

### Step 1: Measure First

**Never optimize without benchmarks.** Run existing benchmarks:

```bash
cd tests/Cljr.Benchmarks
dotnet run -c Release -- --filter "*"
```

Or specific benchmarks:

```bash
dotnet run -c Release -- --filter "VectorBenchmarks"
dotnet run -c Release -- --filter "*Conj*"
```

### Step 2: Identify Hot Paths

Use profiling or benchmark results to identify:
- High-frequency operations
- Allocation-heavy code paths
- Cache miss patterns

### Step 3: Apply Optimizations

See reference files for specific patterns:
- [.NET 10 / C# 14 Features](dotnet10-csharp14.md)
- [Emitter Patterns](emitter-patterns.md)
- [Benchmarking Guide](benchmarking.md)

### Step 4: Verify Improvement

Re-run benchmarks and compare:

```bash
dotnet run -c Release -- --filter "YourBenchmark" --runtimes net10.0
```

## Quick Reference: Key Optimizations

### AggressiveInlining

For small, frequently-called methods:

```csharp
[MethodImpl(MethodImplOptions.AggressiveInlining)]
public T GetValue() => _value;
```

### Span<T> for Zero-Copy

```csharp
// Instead of creating arrays
public ReadOnlySpan<object?> ArrayFor(int i) => _tail.AsSpan();

// Span-based construction (already in PersistentVector)
public static PersistentVector Create(ReadOnlySpan<object?> items)
```

### FrozenDictionary for Read-Heavy Lookups

```csharp
using System.Collections.Frozen;

// Mutable during construction
private readonly ConcurrentDictionary<Type, Cache> _impls = new();
// Frozen for fast reads
private volatile FrozenDictionary<Type, Cache>? _frozen;

public void Freeze() => _frozen = _impls.ToFrozenDictionary();
```

### Symbol/Keyword Interning

Already implemented - ensures reference equality:

```csharp
// Good: reference equality after interning
if (ReferenceEquals(sym1, sym2)) { ... }

// Avoid: value equality is slower
if (sym1.Equals(sym2)) { ... }
```

### Transients for Batch Operations

```csharp
// Slow: O(n²) allocations
var vec = PersistentVector.Empty;
foreach (var item in items)
    vec = vec.Conj(item);

// Fast: O(n) with transient
var transient = PersistentVector.Empty.AsTransient();
foreach (var item in items)
    transient.ConjBang(item);
return transient.Persistent();
```

## Key Files

| Area | Files |
|------|-------|
| Runtime Collections | `src/Cljr.Runtime/Collections/PersistentVector.cs`, `PersistentHashMap.cs` |
| Protocol Dispatch | `src/Cljr.Runtime/Protocol.cs`, `MultiFn.cs` |
| Symbol Interning | `src/Cljr.Runtime/Symbol.cs`, `Keyword.cs` |
| Emitter | `src/Cljr.Compiler/Emitter/CSharpEmitter.cs` |
| Benchmarks | `tests/Cljr.Benchmarks/CollectionBenchmarks.cs` |

## References

- [.NET 10 / C# 14 Features](dotnet10-csharp14.md) - Latest platform features
- [Emitter Patterns](emitter-patterns.md) - Optimized C# code generation
- [Benchmarking Guide](benchmarking.md) - How to measure and compare

## External Resources

- [What's new in .NET 10](https://learn.microsoft.com/en-us/dotnet/core/whats-new/dotnet-10/overview)
- [What's new in C# 14](https://learn.microsoft.com/en-us/dotnet/csharp/whats-new/csharp-14)
- [.NET 10 Runtime Improvements](https://learn.microsoft.com/en-us/dotnet/core/whats-new/dotnet-10/runtime)
