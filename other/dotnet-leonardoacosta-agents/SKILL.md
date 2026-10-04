---
name: dotnet
description: C# / .NET / ASP.NET Core conventions for EF Core, dependency injection, typed HttpClient, controllers or minimal APIs, xUnit, and the Azure SDK. Trigger on backend work in .NET repositories.
allowed-tools: Read, Glob, Grep
---


# .NET / C#

The framework skill for C# / .NET repositories. When `/apply` detects a
`*.csproj` / `*.sln` project (stack token `dotnet`), this skill owns the phase model and routes
every phase to a single executing agent: **`dotnet-azure-specialist`**
(`agents/backend/dotnet-azure-specialist.md`).

Target stack: ASP.NET Core on .NET 8/9/10, EF Core, Azure SDK v12 (`Azure.Identity`,
`Azure.Storage.*`, `Azure.Security.KeyVault.*`), `Microsoft.Identity.Web` (MSAL),
`IHttpClientFactory` + `AddStandardResilienceHandler`, xUnit + `WebApplicationFactory`.

This file has two distinct jobs that don't share a reader: **Part A** is metadata `/apply`'s
stack-composition machinery consumes to orchestrate a build (phase model, gates, engineer
wiring) — you read it to understand how this skill plugs into the DB/API/UI/E2E pipeline, not to
find C# guidance. **Part B** is the navigation layer an engineer actually writing C# uses to find
the right reference file. Keep them separate — an engineer mid-task skims past Part A entirely.

## Part A: Framework Registration (how `/apply` orchestrates this skill)

**Collapse-to-one-engineer model.** Unlike a full-stack workflow with DB / API / UI / E2E fanned to four
specialist engineers), a headless C# service has one owner. All phases collapse to
`dotnet-azure-specialist`; the DB/API/UI/E2E state machine is retained but the display labels are
reinterpreted:

| Phase | Display label | Agent | Gate |
| --- | --- | --- | --- |
| DB  | Data     | `dotnet-azure-specialist` | `dotnet build` |
| API | Services | `dotnet-azure-specialist` | `dotnet build` |
| UI  | Web      | `dotnet-azure-specialist` | `dotnet build` |
| E2E | Tests    | `dotnet-azure-specialist` | `dotnet test`  |
| DOC | Docs     | `general-purpose`         | `openspec validate` |

There is no bundled DB/UI category owner (`bundles: []`). EF Core data patterns live inside this
skill's references, not a separate `drizzle`-equivalent — a headless API's data layer is part of
the same C# project the API lives in.

**Gate story.** C# has no separate typecheck step; the compiler is the type system:

| Gate | Command | Role |
| --- | --- | --- |
| Typecheck-equivalent | `dotnet build` | Compile is the correctness gate. Fails on type errors, missing refs, nullable violations. |
| E2E / test phase | `dotnet test` | Runs xUnit + integration tests. |
| Lint pre-gate (optional) | `dotnet format --verify-no-changes` | Style/whitespace parity with CI. Non-blocking pre-gate. |

Scope the build/test to a single project or solution when the repo root isn't the build root:
set `[stack.gates]` in `.claude/project.toml` (e.g. `dotnet build api/DC.Api/`). A full-solution
`dotnet build` is slower than `tsc` — scope it per project if the per-phase gate is too slow.

**Headless-API default vs full-stack override.** The default is a headless C# API — no
frontend skill, all phases to `dotnet-azure-specialist`. The `dotnet-next` alias resolves to this
same single `dotnet` skill. Full-stack C#+Next applications opt into a
frontend skill explicitly:

```toml
# .claude/project.toml
[stack.overrides]
add = ["nextjs-app-router"]
```

This routes UI-phase work to the frontend skill's engineer while C# phases stay with
`dotnet-azure-specialist`. Do not add a frontend skill unless the repository actually owns a frontend.

## Part B: Which Reference to Load (for the engineer writing C#)

Recognize the task/symptom on the left, load the file on the right — this skill body is a
router, not the encyclopedia:

| You're looking at... | Symptom / task signal | Load |
| --- | --- | --- |
| A `DbContext`, LINQ query, or migration | Slow query, N+1, `dotnet ef migrations` command, "the migration touches prod data" caution | `references/ef-core.md` |
| A constructor taking a service/client | `AddScoped`/`AddSingleton`/`AddTransient` mis-lifetime bug, `IHttpClientFactory` typed client, `DefaultAzureCredential` wiring, `IOptions<T>` not binding | `references/di-and-http.md` |
| An endpoint definition | Choosing Controller vs minimal API, model-binding/validation failure, malformed `ProblemDetails` error shape, API versioning | `references/controllers-and-apis.md` |
| A failing or missing test | xUnit structure, `WebApplicationFactory` integration test, Testcontainers vs real-DB choice, what to mock vs not | `references/testing.md` |
| Anything touching Azure services | Key Vault secret access, ADLS Gen2, App Insights/telemetry wiring | `references/azure-sdk.md` |

## NEVER

- **Inject a `Scoped` service into a `Singleton`** — the singleton captures the first request's
  scoped instance (stale `DbContext`, cross-request data bleed) and holds it for the app's whole
  lifetime, not just one request. `references/di-and-http.md` § Captive-dependency trap.
- **`try { } catch (Exception) { }` and swallow in a controller/service** — this bypasses the
  global `ProblemDetails` handler, so the caller gets whatever the empty catch leaves behind
  (often a malformed or missing error body) instead of a machine-readable RFC 7807 response. Let
  unhandled exceptions reach the middleware; catch only what you can meaningfully recover from.

The executing agent is **`dotnet-azure-specialist`**.
