---
name: modular-monolith
description: Designing and enforcing a Modular Monolith in .NET — module anatomy, public Contracts, internal visibility, module registration, synchronous query contracts vs integration events, transactional outbox, schema-per-module data ownership, cross-module transactions, reporting across modules, and the path to extracting a service. Use when topology is modular-monolith, when a change crosses modules, when adding a module, or when someone wants to reference another module's internals or join across schemas.
user-invocable: false
---
# Modular Monolith

## Module anatomy
- `{Root}.Modules.{M}.Contracts` — public: integration events, exposed query interfaces + DTOs.
- `{Root}.Modules.{M}[.*]` — everything else, `internal` by default (recipe decides project split).
- `{M}Module.cs` — `Add{M}Module` / `Map{M}Module` / optional `Use{M}Module` for background services.
- Own `DbContext` with `HasDefaultSchema("{db_schema}")` and own migrations history table.

## Communication — choose per interaction
| Need | Mechanism | Rules |
|---|---|---|
| Read data owned by another module, immediately | query contract (`IPartnerLookup`) implemented inside the owner | returns DTOs from Contracts; no `IQueryable`; cacheable; bulk methods to avoid N+1 |
| React to something that happened | integration event via outbox | publisher does not know consumers; consumers idempotent; at-least-once |
| Command another module to do something now | ⚠️ avoid; prefer event. If unavoidable, command contract in owner's Contracts with explicit ADR | never inside the caller's transaction |
| Show combined data (screens/reports) | composition in the UI/BFF, or Reporting module views | never join schemas in write paths |

## Transactional outbox (in-process)
1. Aggregate raises domain event → interceptor maps to integration event → `outbox.Messages` row in
   the same transaction as the business change.
2. Dispatcher (hosted service) polls, publishes to in-process bus, marks processed; retries with backoff;
   poison messages to a dead-letter table with alerting.
3. Consumers record `ProcessedEvents(EventId)` in their own schema, in the same transaction as their change.
4. Same contract works with a broker later; only the dispatcher changes.

## Data ownership
- One schema per module; the module is the only writer.
- Foreign keys across schemas: **no**. Store the id; validate via query contract or event-carried state.
- Cross-module reporting: dedicated Reporting module with read-only views/SPs over other schemas,
  granted SELECT only — recorded as a profile exception with ADR.

## Cross-module consistency
No distributed transactions. Use: event → consumer → compensating event on failure (saga in the
module that owns the process). Name the process owner explicitly in the ADR.

## Enforcement (architecture tests)
- No module references another module's non-Contracts assembly.
- Contracts reference nothing but SharedKernel.
- Public types outside Contracts: only `{M}Module` extension class.
- `consumes` in profile matches actual references (test reads profile.yml).
- Each DbContext touches only its schema (test inspects model metadata).

## Extraction path to a service (when forces appear)
1. Module already communicates only via Contracts + events → replace in-proc bus with broker.
2. Replace query contracts with HTTP/gRPC clients implementing the same interfaces.
3. Move schema to its own database; Reporting switches from views to event-fed read store.
If step 1 is not true, you are not ready — fix boundaries first.

Deeper patterns (sagas, event versioning, module-level auth): `references/advanced.md`.
