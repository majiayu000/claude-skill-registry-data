---
name: backend-architecture
description: Resolve backend architecture placement and interface questions using the installed Clean Architecture conventions. Use for a concrete choice about module ownership, ports, adapters or dependency wiring, including standalone architecture questions; backend-change owns implementation.
---

# Backend architecture conventions

Use this reference to decide where backend behavior belongs and how its
interfaces connect. Read `backend/AGENTS.md` for the binding invariants. Inspect a
matching installed module for the question at hand; consult the project
profile for active capabilities or contracts and `backend/README.md` for stack
or entry-point questions. Code paths in these references are relative to
`backend/`.

## Authority

Preserve `backend/AGENTS.md` and the active public contract. The references
below explain how the existing code satisfies those constraints; they do not
introduce optional services, bypass scope checks or establish a new module
shape. `backend/pyproject.toml` and architecture tests enforce selected rules.

## Sources of truth

References explain rules and point to installed exemplars instead of copying
code. Open the cited file to see the current shape. When a reference and the
code disagree, check `backend/AGENTS.md`, enforced gates and the relevant ADR,
then resolve the inconsistency in the affected change. Do not illustrate a rule
with a module that is not installed.

| Concept | Exemplar |
| --- | --- |
| Full module | `src/tenants/` (roles: `application/use_cases/role/`) |
| Thin modules | `src/profile/` (presentation only), `src/admin/`, `src/assets/` |
| Use case + load mixin | `src/tenants/application/use_cases/role/creator.py`, `mixins.py` |
| Repository port + SQL adapter | `src/tenants/domain/repositories/tenant_role.py`, `src/tenants/infrastructure/repositories/sql_tenant_role.py` |
| Builder (ORM → domain) | `src/common/infrastructure/builders/tenants/tenant_role.py` |
| Endpoint, presenter, router | `src/tenants/presentation/endpoints/tenant_roles.py`, `presenters/tenant_role.py`, `router.py` |
| Command/query handler + wiring | `src/tenants/application/command/persist_tenant.py`, `src/tenants/infrastructure/bus_wiring.py` |

## Read for the architectural question

| Question | Reference |
| --- | --- |
| Module ownership, layers and allowed imports | [layers.md](references/layers.md) |
| Use-case interface, naming and composition | [use-cases.md](references/use-cases.md) |
| Repository interfaces, SQL adapters, builders and transactions | [repositories.md](references/repositories.md) |
| Dependency construction and request/session lifetime | [dependency-injection.md](references/dependency-injection.md) |
| HTTP input, presenters and router composition | [endpoints.md](references/endpoints.md) |
| Domain errors and their HTTP translation | [errors.md](references/errors.md) |
| Connections to inspect when assembling a module | [feature-checklist.md](references/feature-checklist.md) |

Open only the reference needed to resolve the current question.

## Conditional integration patterns

These references explain how an already selected capability fits the architecture:

- [cqrs-buses.md](references/cqrs-buses.md): existing cross-module protocols and
  async dispatch; ordinary local CRUD uses repository interfaces.
- [auth-multi-tenant.md](references/auth-multi-tenant.md): active identity,
  authorization and tenant scoping.
- [pagination.md](references/pagination.md): the cursor `Page` contract used by
  paginated list endpoints.
- [background-jobs.md](references/background-jobs.md): the RabbitMQ worker, its
  delivery guarantees and independent session lifecycle.
- [config-bootstrap.md](references/config-bootstrap.md): the composition root,
  settings and lifetime of the services the profile actually enables.

## Workflow owners

[backend-change](../backend-change/SKILL.md) owns building/refining a change and
[operational scripts](../backend-change/references/operational-scripts.md).
[schema-change](../schema-change/SKILL.md) owns migrations and data evolution.
[verify-change](../verify-change/SKILL.md) owns check selection and evidence, using
python-testing for pytest conventions; tests exercise the interface of the layer
whose behavior changes (entity, `UseCase.execute()`, repository against real
PostgreSQL, or HTTP endpoint). Commands and environments come from the project
profile and verification guide. Resolving an architectural question here does not
start another development loop or establish acceptance.
