---
name: architecture-fitness-tests
description: Turns the Architecture Profile into executable architecture tests (NetArchTest or ArchUnitNET) and defines the required test strategy per module recipe — dependency direction, module boundaries, Contracts purity, slice hygiene, domain purity, naming, visibility, schema ownership. Use when creating or changing profile.yml, adding a module, after architecture decisions, when asked what tests a change needs, or when architecture rules are only documented but not enforced.
user-invocable: false
---
# Architecture Fitness Tests

A rule that is not tested is a suggestion. This skill maps profile → tests and recipe → test strategy.

## 1. Profile → rules mapping
| Profile source | Generated test |
|---|---|
| `topology: modular-monolith` + modules | each module's assemblies do not reference other modules' non-Contracts assemblies |
| `modules[].exposes.contracts_project` | Contracts assembly depends only on SharedKernel/BCL |
| `modules[].consumes` | actual references ⊆ declared `consumes` (fail with the undeclared dependency) |
| `recipe: clean-sliced` | Domain ↛ Application/Infrastructure/EF/AspNetCore; Application ↛ Infrastructure |
| `recipe: sliced-domain` | namespace `.Domain` ↛ `.Features`, `.Infrastructure`, EF, AspNetCore |
| `recipe: hexagonal-integration` | `.Adapters.*.Dtos` types used only within `.Adapters` |
| `organization: vertical-slices` | no type in `.Features` depends on a `*Handler` from a different use-case namespace |
| `request_dispatch: direct` | no reference to MediatR/Mediator packages |
| `error_model: result` | handlers return `Result`/`Result<T>` or a response type (reflection check on `Handle`) |
| `conventions.time: timeprovider` | no use of `DateTime.Now/UtcNow` in Domain/Application/Features (Roslyn-based or IL scan) |
| `shared_kernel.allowed` | SharedKernel contains only listed type families (naming allow-list) |
| visibility | only `{M}Module` and Contracts types are public in module assemblies |
| `db_schema` | each DbContext model uses only its schema (runtime test builds the model) |
| `rules[]` with `enforce: test` | one test per rule id, test name starts with the id |
| `exceptions[]` | test excludes exactly the scope; fails after `expires` |

## 2. Implementation
- Template: `assets/ArchitectureTests.cs.template` (NetArchTest.Rules + xUnit). Copy it with a shell command (`Copy-Item`/`cp`), replace `{Root}` with one edit — never retype it. For ArchUnitNET keep the same test names.
- Tests load `profile.yml` at runtime (YamlDotNet) so adding a module requires no test edits.
- Failure messages must name the offending type and the profile rule id.

## 3. Test strategy per recipe
| Recipe | Required | Optional |
|---|---|---|
| clean-sliced | aggregate unit tests for every invariant & transition; one integration test per slice (happy path + main failure) | handler unit tests only for complex orchestration |
| sliced-domain | same as clean-sliced | — |
| pure-slices | integration test per slice against real SQL Server (happy path + each business rule) | unit tests for pure calculations |
| hexagonal-integration | mapper contract tests from recorded payloads; adapter tests against a fake server (WireMock.Net); resilience test for timeouts | end-to-end sandbox test (manual/CI nightly) |
| cross-module | publisher test (event written to outbox with expected payload); consumer idempotency test | contract snapshot test for event schema |

## 4. Integration test harness (SQL Server)
- `Testcontainers.MsSql` with one container per test run; database per test class via `CREATE DATABASE` + migrations.
- `Respawn` to reset between tests within a class.
- `WebApplicationFactory<Program>` with module registrations untouched; replace only external adapters.
- Freeze time with `FakeTimeProvider`.

## 5. Output
```
RULES: <rule id → test name>; …
UNENFORCED: <rule — reason it cannot be tested — review rule added>
```
