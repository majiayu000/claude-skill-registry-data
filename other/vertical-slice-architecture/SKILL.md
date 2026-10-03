---
name: vertical-slice-architecture
description: How to build and maintain Vertical Slice Architecture in .NET — slice anatomy (single-file and folder variants), direct handler dispatch without a mediator, cross-cutting concerns, what slices may share, how slices interact with a domain model or Clean layers, and slice-level testing. Use when adding or modifying a use case/endpoint/feature in any module organized by vertical-slices, or when duplication between slices is discussed.
user-invocable: false
---
# Vertical Slice Architecture

## Principle
Organize by **change**, not by technical kind. Everything a use case needs to change together lives
together. Coupling inside a slice is high on purpose; coupling between slices is minimized.

## Slice anatomy
A slice = one use case = one request type → one handler → one response, plus its endpoint,
validation and (for queries) its read model.

**Folder variant** (clean-sliced, sliced-domain, larger slices):
```
Features/Invoices/IssueInvoice/
  IssueInvoiceCommand.cs     record, primitives + ids only
  IssueInvoiceValidator.cs   shape validation only (required, lengths, formats)
  IssueInvoiceHandler.cs     load aggregate → call domain method → save → return Result
  IssueInvoiceResponse.cs
  IssueInvoiceEndpoint.cs    route, auth policy, maps Result → HTTP
```
**Single-file variant** (pure-slices, < ~200 lines): nested types in `IssueInvoice.cs`.
Generate with `scripts/New-Slice.ps1` (skill `feature-scaffold`); template index: `references/slice-templates.md`.

## Dispatch without a mediator (default `request_dispatch: direct`)
- Handlers are concrete classes registered by convention (scan `*Handler` in the module assembly).
- Endpoints receive the handler via DI parameter injection.
- Cross-cutting behavior:
  - validation → endpoint filter that resolves `IValidator<TRequest>`
  - transactions → handler owns `SaveChangesAsync` (one per use case); no ambient unit-of-work layer
  - logging/tracing → OpenTelemetry + endpoint filters
  - authorization → endpoint `.RequireAuthorization(policy)`
- Background jobs and event consumers call handlers the same way — they are just other driving adapters.

Use a mediator only if the profile says `mediator` (ADR required). Do not mix.

## What slices may share
| Shared thing | Where | OK? |
|---|---|---|
| Domain model (aggregates, value objects, domain services) | Domain | ✅ that is its purpose |
| DbContext, connection factory | Infrastructure/Data | ✅ |
| Validation rules reused ≥ 3 times | extension methods near Domain value objects | ✅ after third use |
| Response DTOs | — | ❌ each slice owns its response, even if identical today |
| Handlers | — | ❌ never inject another slice's handler |
| "Base handler" / generic CRUD handler | — | ❌ reintroduces layers |
| Query fragments (e.g. partner projection) | module-internal `Queries/` static helpers | ⚠️ after third use, keep them dumb |

**Slice needs another slice's behavior?** The behavior is either a domain rule (move to aggregate or
domain service) or a module capability (extract an internal service with a narrow interface). If it
belongs to another module, use its Contracts.

## Commands vs queries inside slices
- Command handlers: load aggregate(s) by id → invoke behavior → persist → return id/Result. Never
  return rich read models from commands; the client re-queries (or return a minimal response).
- Query handlers: never load aggregates. Project straight to the response (`AsNoTracking().Select`,
  Dapper, view, SP). See `cqrs`.

## With other styles
- **+ Clean**: slices live in Application; endpoints in slice or Host per `endpoint_placement`.
  Domain stays feature-agnostic — no `IssueInvoice` folder in Domain.
- **+ Domain model without Clean (sliced-domain)**: `Domain/` folder guarded by architecture tests.
- **+ Hexagonal**: slices are driving adapters; driven ports live at module level.

## Testing a slice
One integration test class per slice: HTTP (or handler) in → real database → assert response and
persisted state/emitted events. Unit tests go to the domain, not to handlers.

## Anti-patterns
- Folder named `Features` containing `Controllers/`, `Services/`, `Dtos/` → technical layers renamed.
- Slices grouped by entity with CRUD names only (`CreateInvoice`, `UpdateInvoice`) where the business
  has real verbs (`IssueInvoice`, `CancelInvoice`, `CorrectInvoice`). Use business verbs.
- `Update{Entity}` slice accepting the whole entity → hides intent, breaks invariants. Split by intent.
- Shared `Common/Dtos` folder growing with every slice.

## Frontend analog
Feature folders mirroring backend slices; see `architecture-composition/references/frontend-composition.md`.
