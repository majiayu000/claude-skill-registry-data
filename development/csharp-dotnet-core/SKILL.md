---
name: csharp-dotnet-core
description: ".NET 8 / C# architecture, async/await ValueTask patterns, Entity Framework Core, and minimal APIs."
---

# .NET Core & Modern C# Protocol

Build high-throughput C# microservices.

---

## 1. Async & Allocation Hygiene

1. Always use `ConfigureAwait(false)` in library code.
2. Use `ValueTask<T>` for hot paths that frequently complete synchronously to eliminate Task allocations.

---

## 2. EF Core Query Tuning

Use `AsNoTracking()` for read-only query projections to avoid change-tracker overhead.
