---
name: csharp
description: "Apply these opinionated C# conventions whenever writing or reviewing C# 12 / .NET 8+ code: nullable enabled with warnings as errors, records and primary constructors, pattern matching over cast chains, the Result pattern for expected failures, async all the way with CancellationToken, IOptions config, IHttpClientFactory, and never returning EF entities from an API."
---

# C# Conventions

House conventions for C# 12 / .NET 8+. Apply them to code you are writing or changing — don't rewrite untouched files to match unless asked.

## Conventions

- **`<Nullable>enable</Nullable>` and warnings as errors.** The nullable annotations only pay off if the warnings block the build; ignored, they become decoration that lies about which references can be null.
- **C# 12 defaults:** file-scoped namespaces, primary constructors, collection expressions, `required` members. Records for DTOs and value objects — value equality is what you want when comparing data, and hand-written `Equals`/`GetHashCode` pairs drift apart.
- **Pattern matching over type-test-and-cast chains.** Switch expressions on a closed hierarchy let the compiler warn about unhandled cases; an `if`/`else if` ladder just falls through silently when a new type appears.
- **Result pattern for expected failures**, exceptions for genuinely exceptional ones. "Not found" and "invalid input" are ordinary outcomes and belong in the return type where the caller must deal with them; using exceptions for control flow hides them from the signature and costs a stack unwind per occurrence. A closed record hierarchy gives you exhaustive `switch` over the outcomes:

  ```csharp
  public abstract record Result<T>
  {
      public sealed record Ok(T Value) : Result<T>;
      public sealed record Fail(string Error) : Result<T>;
  }

  var message = GetUser(id) switch
  {
      Result<User>.Ok(var user) => $"Found {user.Name}",
      Result<User>.Fail(var error) => error,
  };
  ```

- **Async all the way down.** `.Result` and `.Wait()` deadlock under a synchronisation context and burn a thread pool thread everywhere else. If a call chain has to be async at the bottom, it is async at the top.
- **Accept and pass a `CancellationToken` on every async public method.** Without it a cancelled request keeps its database query and HTTP call running to completion, and the work is charged to a caller who has already gone.
- **Never expose EF entities from an API.** Project to a DTO with `Select` — otherwise you ship whatever the schema grows next, and lazy loading turns serialisation into an N+1 query storm.
- **EF specifics that show up as production incidents rather than test failures:** `AsNoTracking()` on every read-only query, since change tracking on a large result set is pure overhead; `AsSplitQuery()` when `Include`-ing more than one collection, because a single join multiplies rows cartesian-style; `ExecuteUpdateAsync`/`ExecuteDeleteAsync` (.NET 7+) for bulk changes rather than loading entities to modify them; a global `HasQueryFilter` for soft deletes so no query can forget the flag.
- **Keyed services when one interface has several implementations** (.NET 8): register with `AddKeyedScoped<INotifier, EmailNotifier>("email")` and resolve with `[FromKeyedServices("email")]`. It beats an enum-switching factory because the container still owns the lifetimes.
- **`IOptions<T>` with validated, strongly-typed config.** `configuration["Some:Key"]` fails at the call site, at runtime, on a typo. A bound options class with `ValidateOnStart` fails at boot with the field named.
- **`IHttpClientFactory`, never `new HttpClient()` per call** — socket exhaustion from lingering TIME_WAIT connections is the classic failure, and it only appears under load.
- **`Span<T>`/`Memory<T>` and pooling where a profiler says allocations matter.** They complicate the code, so spend that complexity where there is a measurement, not on principle.
