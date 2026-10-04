---
name: backend-change
description: Build or refine FastAPI use cases, endpoints, repositories, dependencies, jobs or operational scripts in backend/. Use when implementing, fixing or refactoring backend behavior after its scope is known. Frontend-only work, persistence migrations (schema-change) and read-only reviews (review-change) belong elsewhere.
---

# backend-change

Read `backend/AGENTS.md` (the backend constitution), the affected acceptance
criteria, a matching module exemplar and related tests. Use the project profile
when active capabilities or public contracts matter, and `backend/README.md`
for stack or entry-point questions. Commands run from the Git root; pytest
paths are relative to backend.

This workflow owns implementation order and refinement. Consult, without
restarting the loop:

- [backend-architecture](../backend-architecture/SKILL.md) and only its relevant
  reference for an architectural choice (ownership, interfaces, composition).
- [fastapi](../fastapi/SKILL.md) only for a concrete framework API question;
  project conventions in `backend/AGENTS.md` govern the implementation.
- The profile and installed exemplar for active capabilities and public contracts.
- [operational-scripts.md](references/operational-scripts.md) for a backfill,
  bootstrapper or other operational script.

## Build mode

1. Pick one observable vertical slice.
2. Write a test that fails for the intended reason ([TDD](../tdd/SKILL.md)).
   Use [schema-change](../schema-change/SKILL.md) for persistence changes.
3. Add the minimal implementation, including wiring and its consumer.
4. Run the test to green. Test authorization and scopes when active.
5. Coordinate API/BFF/DTO consumers on one acceptance contract, then repeat.

## Refinement mode

1. Take a concrete finding or objective and identify preserved invariants.
2. Start from green; improve interface, responsibility, query or wiring in small
   steps, rerunning affected checks after each.
3. Use codebase-design for a design seam, not a compulsory rewrite.

## Verify and hand off

Run `just backend check` and focused `just backend test unit <paths>`. When the
HTTP contract changed (routes, parameters, models, tags, summaries), refresh the
API reference snapshot with [openapi-sync](../openapi-sync/SKILL.md). API,
persistence and effects follow the impact matrix in
`docs/content/docs/equipo/verificacion.md`. Hand the exact revision, commands and results,
unresolved findings and public contract evidence to
[validate-change](../validate-change/SKILL.md).

## Gotchas

- Green checks alone do not close the change; validate-change does.
- Diagnose failures without weakening existing gates.
- Fix a known bug before unrelated refactoring.
- Performance claims need before/after measurement.
- A scope change returns to define-change instead of growing the slice.
- Preserve the persistence, blocking-call and rate-limit invariants in
  `backend/AGENTS.md`; consult backend-architecture
  `references/repositories.md` or `references/endpoints.md` when the change
  needs their implementation detail.
