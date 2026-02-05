---
name: backend-code-organisation
description: Kotlin backend layering and packaging guidelines
license: MIT
---

## Mission
- Keep backend services modular: resources handle transport, managers own business logic, and data access stays isolated.
- Maintain clean dependency flow across modules (`service` → `core` → `models`) to encourage reuse and testability.

## Layering Principles
- **Resources**: Only translate HTTP/storage inputs to domain calls. No database or cross-service logic. Convert `SecurityContext` early.
- **Managers**: Encapsulate business rules; coordinate helpers, other managers, workflows, and DAL components. Break cycles by separating read/write responsibilities or introducing controllers.
- **Helpers/Services**: Reusable integrations (feature flags, external clients). Centralize external service calls to simplify retries and upgrades.
- **Repos/DAL/DAO**: Keep database interactions single-purpose. Compose multi-step transactions in repos/DAL; keep DAO calls single query.
- **Utils/Validators/Transformers**: Pure functions and extensions only; avoid hidden state.
- **Cache Managers**: Inject Redis/Lettuce clients, expose typed `get`/`invalidate` helpers.

## Package & Module Structure
- Enforce lowercase package names without underscores; avoid versioned package hierarchies (`v2` folders). Prefer `managers.slots` over `managers.slots.v2`.
- Organize by responsibility: `managers`, `helpers`, `utils`, `dao`, `workflows`, etc. Mirror structure in tests.
- Module boundaries:
  - `core`: managers, helpers, data access, transient models. May depend on `models`.
  - `service`: Dropwizard resources, configuration, application wiring; no direct DB access.
  - `console-service`: Console-specific resources/auth; depends on `core`.
  - `client`: Outbound clients; depend only on `models`.
  - `models`: Shared API/data contracts; no dependencies.

## Dependency Injection & Config
- Add new Redis/Cosmos/DB configs across all environments (`db-test`, `db-dev`, `db-warehouse-prod`) and run the service locally to validate.
- Annotate injectable classes with `@Singleton` when appropriate.
- Only use `@Named` when multiple bindings of the same type exist; otherwise default bindings suffice.
- Centralize client construction in DI modules to enforce consistent timeouts and hosts.

## Review Checklist
- Check that new features land in the correct layer and module (e.g., resources calling managers, not DAOs).
- Ensure helpers/managers do not introduce cyclic dependencies; suggest splitting read/write flows or using controller orchestrators.
- Verify repos/DAL enforce validation and error translation before returning data.
- Confirm new package or module names remain lowercase and idiomatic; flag attempts to create `v2` package forks.
- Audit DI modules for duplicate provider methods and proper scoping.

## Tooling Tips
- `Glob` for `*.kt` within `service/` or `core/` to inspect layer usage.
- `Read` DI modules when new bindings appear to ensure wiring matches guidelines.
- `Grep` for `@Named` or direct DAO usage inside resources to catch misplaced logic.
