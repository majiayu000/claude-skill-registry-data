---
name: Generate Factory
description: "Generate a test-data factory (factory-boy for Python, a plain TS builder for frontend) for a given model or type. Triggers on 'make factory', 'generate factory for', 'test builder for'. Produces a factory file placed next to existing siblings, using sensible synthetic defaults."
model: inherit
---

## Purpose

Eliminate the copy-paste tax of writing test factories by generating one that matches the repo's existing factory conventions (factory-boy on the API side, hand-written builders on the frontend) with safe synthetic defaults.

## When to Invoke

- A new SQLAlchemy model or Pydantic DTO is added and needs a factory for tests.
- A new TypeScript interface representing an API response needs a test builder.
- An existing factory is missing fields after a schema change.

## When NOT to Invoke

- For models handling PII where the factory must meet data-privacy review (do it manually).
- For non-test data (fixtures destined for production seeds).

## Inputs

- **target**: fully-qualified symbol (e.g. `api.src.db.models.OpportunityModel`) or file path + class name.
- **side**: `api` or `frontend`.

## Procedure

1. Resolve the target symbol and read its fields.
2. For `api`: pick up sibling factory style from `api/tests/factories/` (factory-boy with `Faker` providers and sequence helpers).
3. For `frontend`: pick up builder style from the nearest `__factories__` or `test-utils/` directory.
4. For each field, generate a default:
   - Primitive types → Faker providers (`pystr`, `pyint`, `email`) or TS literals.
   - Foreign keys → `SubFactory(OtherFactory)` or `build(OtherBuilder)`.
   - PII-labeled fields (`email`, `phone`, `ssn`, `ein`) → Faker providers scoped to obviously-fake domains (e.g. `@example.test`).
   - Enum fields → cycle through valid values.
5. Write the factory file in the conventional location.
6. Run the relevant test module once to confirm the factory constructs cleanly.

## Outputs

- New factory file at `api/tests/factories/<model>_factory.py` or `frontend/src/test-utils/factories/<type>.ts`.
- A short summary of fields, generators used, and any fields left as `# TODO` where the type is ambiguous.

## Safety

- Never emits real PII; always uses `@example.test` and obviously synthetic IDs.
- Never writes to production fixture directories.
- Refuses to generate factories for models tagged with a PII review marker (`# pii-review-required`).
- FedRAMP: factory defaults never include real agency codes; uses `TEST-###` series.

## Examples

**Example 1 — API.** `OpportunityModel` → `opportunity_factory.py` with `SubFactory(AgencyFactory)` and a synthetic title sequence.

**Example 2 — Frontend.** `OpportunityResponse` → `opportunity.ts` builder with partial-override support.

**Example 3 — Schema backfill.** Existing factory is missing `closed_at` after a migration; skill adds the field and re-runs.

## Related

- `.cursor/skills/skill-generate-test-data/` — generate fixture JSON rather than factories.
- `.cursor/skills/skill-generate-mock/` — generate mocks rather than factories.
