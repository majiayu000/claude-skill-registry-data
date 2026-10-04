---
name: API Contract Test
description: "Generate a contract test that validates an API endpoint's request and response shapes against the OpenAPI spec and the frontend's TypeScript types. Triggers on phrases like 'contract test', 'validate endpoint against OpenAPI', 'schema drift test'. Produces a pytest file under api/tests/contracts/ or a Vitest file under frontend/tests/contracts/, depending on the caller."
model: inherit
---

## Purpose

Catch schema drift between the API implementation, the OpenAPI spec, and frontend consumers before it reaches integration testing. The skill generates deterministic fixture-based contract tests that fail fast when any of the three surfaces diverges.

## When to Invoke

- A new endpoint was just added or modified in `api/src/api/`.
- The OpenAPI spec at `api/openapi.generated.yml` was regenerated and the frontend types may lag.
- A consumer in `frontend/src/services/` calls an endpoint that lacks a contract test.
- Before merging a PR that changes any request/response model.

## When NOT to Invoke

- For pure internal service-layer tests (use unit tests).
- For endpoints still under active design (schema will churn; contract tests become noise).
- For streaming or long-polling endpoints where fixtures cannot capture behavior.

## Inputs

- **endpoint**: HTTP method + path, e.g. `GET /v1/opportunities/search`.
- **side**: `api` (pytest) or `frontend` (Vitest). Default: `api`.
- **sample payload** (optional): JSON fixture; if absent, skill generates one from the OpenAPI schema.

## Procedure

1. Locate the endpoint handler in `api/src/api/` and its Pydantic request/response models.
2. Parse `api/openapi.generated.yml` and extract the operation schema for the endpoint.
3. If `side=api`, generate a pytest that:
   - Loads the OpenAPI schema via `openapi-spec-validator`.
   - POSTs/GETs against the test client with a fixture payload.
   - Asserts status, JSON schema, and required fields.
4. If `side=frontend`, generate a Vitest that imports the TS client from `frontend/src/services/`, mocks `fetch`, and asserts the client call shape matches the OpenAPI operation.
5. Place the file under `api/tests/contracts/test_<resource>_contract.py` or `frontend/tests/contracts/<resource>.contract.test.ts`.
6. Run the generated test once to confirm it passes (or fails with a meaningful drift message).

## Outputs

- New test file at the conventional path.
- Console summary listing: endpoint, side, fixtures used, test names, first-run result.
- If drift is detected on first run, a structured diff between spec and implementation.

## Safety

- Never modifies the OpenAPI spec or the handler — only generates test files.
- Never writes fixtures containing real PII; uses synthetic values (`"agency_code": "TEST-001"`).
- Fails loudly if the endpoint is not found; does not guess.
- FedRAMP: generated tests must not emit real API keys or tokens in fixtures.

## Examples

**Example 1 — API-side, new endpoint.** `POST /v1/applications`. Skill reads the handler + `ApplicationCreate` model, writes `test_applications_contract.py`, runs it, reports pass.

**Example 2 — Frontend-side, drift detected.** `GET /v1/opportunities/search`. Generated Vitest fails because the frontend service omits the `pagination_token` field added to the spec. Skill outputs the diff and recommends regenerating types.

**Example 3 — Custom fixture.** Caller provides a payload matching a real rejection case; skill uses it verbatim after scrubbing obvious PII keys (`email`, `ssn`, `ein`).

## Related

- `.cursor/skills/skill-openapi-sync/` — regenerate types after spec changes.
- `.cursor/agents/new-endpoint.md` — authoring flow for net-new endpoints.
