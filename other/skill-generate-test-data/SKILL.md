---
name: Generate Test Data
description: Generate JSON or SQL fixture files populated with synthetic, non-PII data for a given model, shape, or endpoint. Triggers on 'make fixtures', 'generate test data', 'seed data'. Produces deterministic fixture files with a seed so runs are reproducible.
---

## Purpose

Produce reproducible, synthetic test data that matches a shape (Pydantic model, TS interface, or OpenAPI response) without copy-pasting production rows. Deterministic via a seed so CI is stable.

## When to Invoke

- Setting up a new integration test that needs realistic data volume.
- Seeding a local dev database with safe synthetic rows.
- Generating mock responses for an MSW handler or Storybook story.

## When NOT to Invoke

- For production seeds (those live under `infra/seeds/` and need ops review).
- For PII-sensitive models without manual review.
- As a substitute for `/skill-generate-factory` when a factory is reusable.

## Inputs

- **target**: symbol, file path, or OpenAPI operation id.
- **count**: number of records (default 10).
- **format**: `json` (default), `ndjson`, or `sql`.
- **seed** (optional): integer seed for reproducibility.

## Procedure

1. Resolve the target shape.
2. Seed the generator with the given seed (or the current date if absent) and record the seed in the output.
3. For each field, pick a synthetic value:
   - Strings → Faker provider matching the field semantics (name, address, title).
   - IDs → monotonic with a prefix (`TEST-000001`).
   - Dates → sensible defaults relative to today (2026-04-07 baseline).
   - Foreign keys → reuse a pool of 3 parent IDs to keep joins cheap.
   - PII-labeled fields → obviously-fake values only (`@example.test`, `555-01xx` phone ranges).
4. Emit to the chosen format; write to `api/tests/fixtures/` or `frontend/src/test-utils/fixtures/` depending on shape origin.
5. Write a `README` header comment noting seed, target, and count.

## Outputs

- Fixture file at the conventional path.
- Summary including seed, count, path, and any fields marked `TODO` where inference failed.

## Safety

- Deterministic: same seed → same output.
- Never includes real PII, real agency codes, or real award IDs.
- Never writes to production seed paths.
- Refuses to generate data for models tagged `# pii-review-required`.
- FedRAMP: uses the `@example.test` domain and `TEST-` prefix convention throughout.

## Examples

**Example 1 — Fixture JSON.** 50 synthetic opportunities for a search integration test, seed 42.

**Example 2 — SQL seed.** `count=20 format=sql` for local dev DB seeding.

**Example 3 — OpenAPI-derived.** Target `operationId=listOpportunities`, skill derives shape from spec and generates a realistic response body.

## Related

- `.cursor/skills/skill-generate-factory/` — reusable factories for code-level tests.
- `.cursor/skills/skill-generate-mock/` — mocks, not data files.
