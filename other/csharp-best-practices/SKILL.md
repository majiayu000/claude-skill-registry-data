---
name: csharp-best-practices
description: C# best practices. Use when reading or editing any .cs file.
disable-model-invocation: true
---

# C# best practices

Apply the **type-system-discipline** principle skill first; this skill grounds it in C# syntax. Follow the repository's language version, analyzers, and libraries (Scrutor, MediatR, FluentValidation, OpenTelemetry) over the defaults below.

## Types

| Rule | Summary |
|------|---------|
| Nullable reference types | `<Nullable>enable</Nullable>` with `nullable` in `WarningsAsErrors`. `T?` means absent is a real case; `T` means never null. |
| No `!` | The null-forgiving operator is C#'s `as` cast. Prove non-null by narrowing, or change the type so null can't arrive. |
| Closed hierarchies | Model variants as an `abstract record` with a private constructor and nested `sealed record` cases. No optional-field bags, no `bool IsX` plus nullable payload. |
| Exhaustiveness | Enums: switch expression with no `_` arm, `CS8509` as an error, `CS8524` suppressed. Records: the compiler can't see the closure, so put an abstract member on the base that each case overrides, or use the repository's exhaustiveness analyzer. |
| Strongly typed ids | `readonly record struct OrderId` with a private constructor and a static `Parse`/`TryParse`. Validate once at creation. |
| Constructive modeling | Build the shape so the illegal value can't be constructed: `NonEmpty<T>(T Head, IReadOnlyList<T> Tail)`, start plus `TimeSpan` for a range. |
| Simplest total type | Keep `IReadOnlyList<T>` while every operation stays total. Strengthen only where the loose type forces `!`, `.First()`, or a "should never happen" throw. |
| No casts | `(T)x`, `x as T` followed by a dereference, and `dynamic` are runtime crashes waiting. Use pattern matching. |
| Narrowing hierarchy | Switch expression on a closed type > property pattern > `is T t` > `TryX(out)` > cast. |
| Try pattern | `bool TryX(..., [NotNullWhen(true)] out T? value)` is C#'s type guard. It must verify the claim it makes. |
| Boundary validation | Deserialize into a DTO, map once into domain types, trust types inside. DTOs and EF entities don't cross into the domain. See the **boundary-discipline** principle skill. |
| Schemas before guards | Use the repository's contract and validation stack (System.Text.Json with `RespectNullableAnnotations`, DataAnnotations, FluentValidation, generated clients) before hand-writing field checks. |
| Immutable by default | `record`, `init`, `required`, `IReadOnlyList<T>`. Mutate with `with`. |
| Named arguments | Same-typed or `bool` parameters get named arguments at the call site. Replace `bool` flags with an enum; past three parameters, pass a record. |

## Designing for decorators

| Rule | Summary |
|------|---------|
| Depend on the interface | Consumers take `IOrderService`, never `OrderService`. Register the concrete type only behind the interface. |
| Seal, don't subclass | Concrete services are `sealed`. Extend behavior by wrapping the interface, not with `virtual`/`protected` hooks. |
| Narrow interfaces | One operation or one cohesive group per interface, so a decorator forwards a few members, not twenty. For many similar operations, use a generic `ICommandHandler<TCommand, TResult>` and one open-generic decorator. |
| Async with cancellation | Every decorated member returns `Task`/`ValueTask` and takes `CancellationToken cancellationToken` last, so decorators can await, time, retry, and time out. |
| Outcomes in the return type | Expected failures are a closed result type, not exceptions or side-channel state, so decorators tag outcomes without catching. |
| No default interface members | A decorator that doesn't override a default member runs the default instead of forwarding to the inner service. Keep decorated interfaces abstract-only. |
| No hidden statics | Inject `TimeProvider`, `IMeterFactory`, and caches. Static state can't be wrapped or faked. |
| Core stays clean | The core class holds business logic only: no `Stopwatch`, `Meter`, catch-log-rethrow, or retry loops. Log from the core only when the message needs internal state a decorator can't see. |
| Transparent decorators | Same result, same exception (`throw;`), same `CancellationToken`. One concern per decorator. A decorator never disposes its inner service. |
| Deliberate order | The chain is written once at registration and is part of the design. Logging outermost sees the final outcome; metrics outside a retry measure caller latency, inside it measure attempts. |

## Logging and metrics

| Rule | Summary |
|------|---------|
| Structured templates | `logger.LogInformation("Placed {OrderId}", orderId)` with a constant template. No interpolation or concatenation in log calls (CA2254). No `Console.WriteLine` in shipped code. |
| Log context, not payloads | Ids, counts, durations, outcomes. No request bodies, tokens, or personal data. Stable PascalCase placeholder names, since they become query keys. |
| Exceptions once | Pass the exception as the `Exception` argument. One layer owns the error log: if a decorator logs and rethrows, the host must not log it again. |
| Instruments once | Inject `IMeterFactory`; create the `Meter` and its instruments in a singleton holder class, not per call or per scoped decorator. |
| Durations as histograms | `Histogram<double>` in seconds (`unit: "s"`), timed with `Stopwatch.GetTimestamp()`. A histogram already counts calls; skip the twin counter. |
| Bounded tags | Tag `outcome`, `operation`, `error.type`. Never ids, user input, or exception messages. |
| Record in `finally` | Failures and cancellations are measured too. |
| Correlate with `Activity` | Correlate through tracing (`ActivitySource`) and the logger's activity tracking, not hand-built per-call scopes. |

## Services and tests

| Rule | Summary |
|------|---------|
| Constructor injection | Constructors take dependencies and do no work. No `IServiceProvider` in business code. |
| Lifetimes | A singleton never captures a scoped service. Enable `ValidateScopes` and `ValidateOnBuild`. |
| Validated options | `AddOptions<T>().Bind(...).ValidateDataAnnotations().ValidateOnStart()`. Config is a boundary. |
| Async all the way | No `.Result`, `.Wait()`, or `async void` outside event handlers. Pass `cancellationToken` to every call that accepts one. |
| Real tests | `WebApplicationFactory`, a real database via the repository's test containers, `FakeTimeProvider`, `FakeLogger`, `MetricCollector<T>`. Mock only what you can't run locally. |

Examples: `references/patterns.md` (types, services) and `references/decorators.md` (decorators, logging, metrics).
