---
name: Impact Analysis
description: "Analyze the blast radius of a proposed change across the simpler-grants-gov monorepo. Triggers on phrases like 'impact analysis', 'what does this break', 'who depends on', or before merging changes that touch shared modules, API schemas, database models, or frontend hooks. Reports downstream callers, cross-service contracts, and FedRAMP-relevant boundaries with file:line citations."
model: inherit
---

## Purpose

Give engineers a deterministic, read-only view of what a change touches before they merge. The skill identifies direct callers, transitive consumers, schema-coupled artifacts (OpenAPI, Alembic, frontend types), and crosses the API/frontend boundary so reviewers do not have to grep blind.

## When to Invoke

- Before refactoring a shared util, base class, SQLAlchemy model, or API schema.
- When a PR touches `api/src/db/models/`, `api/openapi.generated.yml`, or `frontend/src/types/`.
- When the author asks "what does this break" or "who depends on `<symbol>`".
- During reviewer triage to size scope and request additional eyes.

## When NOT to Invoke

- For pure documentation changes under `documentation/`.
- As a substitute for running the actual test suite — pair with `skill-run-relevant-tests`.
- For changes confined to a single file with no exports.

## Inputs

- **target**: a file path, symbol (`module.Class.method`), or git ref range (default: staged + unstaged).
- **scope** (optional): `api`, `frontend`, `infra`, or `all` (default).
- **depth** (optional): integer 1–3, transitive call depth (default: 2).

## Procedure

1. Resolve target. If a git range, run `git diff --name-only <range>`; if a file, treat as the only changed file; if a symbol, locate definition via ripgrep.
2. For each changed file, classify it: `api-model`, `api-route`, `api-schema`, `openapi`, `alembic`, `frontend-component`, `frontend-hook`, `frontend-type`, `infra`, `shared-util`, `other`.
3. Build the dependency set:
   - Direct importers via `rg -l "from <module>" api/ frontend/`.
   - Symbol callers via `rg -n "\b<symbol>\b"` filtered to non-definition matches.
   - For `api-model` changes, locate dependent factories under `api/tests/factories/` and routes under `api/src/api/`.
   - For `api-schema` or `openapi` changes, locate frontend type generation outputs and any `frontend/src/services/` clients.
   - For `alembic` changes, locate sibling migrations referencing the same table.
4. Walk the graph up to `depth` levels. Deduplicate.
5. Tag each downstream node with risk: `HIGH` (cross-service contract, DB model, public API), `MED` (shared util, factory), `LOW` (test-only, internal helper).
6. Cross-reference `documentation/rules/api-*.md` and `documentation/rules/frontend-*.md` for any MUST directives implicated.
7. Emit the Output Format. Do not modify files.

## Outputs

```
Impact Analysis — feature/opportunity-status-filter
Changed files (3):
  api/src/db/models/opportunity_models.py
  api/src/api/opportunities_v1/opportunity_schemas.py
  api/openapi.generated.yml

Downstream impact (depth=2):
  HIGH  api/src/api/opportunities_v1/opportunity_routes.py        (direct)
  HIGH  frontend/src/types/opportunity.ts                          (openapi-coupled)
  HIGH  frontend/src/services/fetch/fetchers/opportunityFetcher.ts (openapi-coupled)
  MED   api/tests/src/api/opportunities_v1/test_opportunity_routes.py
  MED   api/tests/src/db/factories/opportunity_factory.py
  LOW   frontend/tests/services/fetchOpportunity.test.ts

Cross-service contracts touched: 1 (OpenAPI)
FedRAMP boundary touched: no
Suggested reviewers: api-team, frontend-team

Recommended follow-ups:
  - Run skill-openapi-sync after merge.
  - Run skill-run-relevant-tests scope=all.
  - Update CHANGELOG under "Changed".
```

## Safety

- Read-only. Never modifies files.
- Never claims completeness — reports are graph-based and will miss reflective/dynamic dispatch.
- Does not execute code or migrations.
- Does not emit PII or secrets even if encountered in source comments.
- Caps walk at `depth=3` to avoid combinatorial blowup.

## Examples

**Example 1 — Model rename**
Author renames `Opportunity.status` → `Opportunity.opportunity_status`. Skill reports the route handler, schema, frontend type, and 4 test files; flags HIGH on the OpenAPI and frontend type.

**Example 2 — Shared util tweak**
Touch `api/src/util/datetime_util.format_iso`. Skill returns 17 callers; suggests a focused unit-test run via `skill-run-relevant-tests`.

**Example 3 — Alembic migration**
New migration adds an index. Skill confirms no model field changes, flags as LOW, recommends `skill-migration-safety-check` next.

## Related

- `.cursor/skills/skill-run-relevant-tests/` — execute the affected tests.
- `.cursor/skills/skill-openapi-sync/` — regenerate types when contracts move.
- `.cursor/skills/skill-migration-safety-check/` — pair for DB-touching PRs.
- `.cursor/agents/codemod.md` — when impact suggests a mechanical refactor.
