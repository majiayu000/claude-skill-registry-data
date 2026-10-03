---
name: code-quality
description: Mechanical, line-level code quality checklist for C# and T-SQL with stable rule ids (time semantics, usings, accessibility, nullability, async, errors, logging, LINQ/EF, suppressions, hygiene). Mandatory for every changed file in a review and for the implementer's self-check before reporting a step. Use whenever reviewing or finishing code changes, even small ones.
user-invocable: false
---
# Code quality checklist

Apply to **every changed file, reading the whole file**, top to bottom. Cite the rule id in each finding.
Severity: **B** blocker · **M** major · **m** minor. A red build or another BLOCKER never shortens this pass.

## CQ-BUILD — the change is actually compiled
| Check | Sev |
|---|---|
| Changed source file not compiled by any project in the solution (outside project folders, excluded by `Compile Remove`, wrong extension). Verify: `dotnet msbuild <project> -getItem:Compile` lists the file, or the file sits under a project directory with default globs | B |
| "green" claimed while build/tests did not cover the changed files | B |

## CQ-TIME — time semantics
| Check | Sev |
|---|---|
| `DateTime.Now`, `DateTime.UtcNow`, `DateTime.Today`, `DateTimeOffset.Now`, `DateTimeOffset.UtcNow` outside tests | M |
| `TimeProvider.GetLocalNow()`, `DateTime.ToLocalTime()`, `DateTimeKind.Local` in domain, application, persistence or integration code — result depends on server time zone and DST | M |
| Local time outside a presentation boundary; the boundary must convert explicitly with a named zone from configuration (`TimeZoneInfo.FindSystemTimeZoneById`) | M |
| `DateTime` used for an instant (use `DateTimeOffset` in UTC); date-only values not `DateOnly` | m |
| Comparing a date with an instant without explicit conversion | M |

## CQ-USING — usings and namespaces
| Check | Sev |
|---|---|
| `using` already covered by implicit usings (`System`, `System.Collections.Generic`, `System.IO`, `System.Linq`, `System.Net.Http`, `System.Threading`, `System.Threading.Tasks`) or a `global using`. Verify `<ImplicitUsings>` in the csproj/`Directory.Build.props`; if no project exists, still report with "verify ImplicitUsings" | m |
| Unused `using` | m |
| Block-scoped namespace (convention: file-scoped) | m |
| Namespace does not match folder/placement rule | M |

## CQ-ACCESS — accessibility and type shape
| Check | Sev |
|---|---|
| Member declared `internal` inside an `internal` type: adds nothing. Members forming the type's API are `public`; `internal`/`private` only to restrict below the type | m |
| Accessibility modifier omitted | m |
| Class not `sealed` and not designed for inheritance | m |
| Field never reassigned but not `readonly`; mutable public state | m |
| Mutable command/query/response/event/value object (must be `record`/init-only) | m |

## CQ-NULL — nullability
| Check | Sev |
|---|---|
| `!` suppression without a comment stating the invariant | M |
| `#nullable disable` or `<Nullable>` not enabled | M |

## CQ-ASYNC — async
| Check | Sev |
|---|---|
| `.Result`, `.Wait()`, `.GetAwaiter().GetResult()` | M |
| `async void` outside event handlers | M |
| `CancellationToken` accepted but not passed on, or not accepted by an I/O method | M |
| Missing `Async` suffix on an async method | m |

## CQ-ERR — errors
| Check | Sev |
|---|---|
| Exception thrown for an expected business failure when profile `error_model: result` | M |
| Empty/catch-all `catch` that swallows; `throw ex;` | M |

## CQ-LOG — logging
| Check | Sev |
|---|---|
| Personal data (CNP, patient data, IBAN, credentials) in logs | B |
| Interpolated string as log template | m |

## CQ-DATA — LINQ / EF / Dapper
| Check | Sev |
|---|---|
| `ToList()`/`AsEnumerable()` before filtering; entities materialized for read models; query inside a loop (N+1) | M |
| String-concatenated SQL | B |

## CQ-SUPPRESS — suppressions
| Check | Sev |
|---|---|
| `#pragma warning disable`, `[SuppressMessage]`, `NoWarn` added without a justification comment | M |

## CQ-HYGIENE
| Check | Sev |
|---|---|
| `TODO(ai)` left, commented-out code, dead code | M |
| Magic number/string carrying business meaning | m |
| Method > ~40 lines or nesting > 3 levels | m |
| Name not in the module's business language; `Helper`/`Manager`/`Util` suffix | m |

## SQL — T-SQL quick pass (full rules: skill `sql-server-data-access`)
| Check | Sev |
|---|---|
| `SELECT *`, `NOLOCK`, missing `SET NOCOUNT ON; SET XACT_ABORT ON;` in procedures | M |
| Implicit conversion (parameter type ≠ column type), function on an indexed column in `WHERE` | M |
| Dynamic SQL without `sp_executesql` parameters | B |

## Example findings (format)
```
M src/…/Probe.cs:7 | CQ-TIME | GetLocalNow() makes result depend on server time zone | use timeProvider.GetUtcNow()
m src/…/Probe.cs:1 | CQ-USING | System is an implicit using | remove line
m src/…/Probe.cs:7 | CQ-ACCESS | internal member in internal type | make it public
```
