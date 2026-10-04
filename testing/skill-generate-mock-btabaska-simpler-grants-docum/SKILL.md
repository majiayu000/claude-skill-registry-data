---
name: Generate Mock
description: "Generate a mock or stub for an interface, service, or module so tests can isolate the unit under test. Triggers on 'mock this', 'stub the service', 'generate a mock for'. Produces a pytest `unittest.mock` stub, a Vitest `vi.mock`, or an MSW handler depending on context."
model: inherit
---

## Purpose

Provide deterministic, conventional mocks that match the test framework in use, with realistic synthetic return values and no accidental network calls.

## When to Invoke

- A unit test needs to isolate a service dependency.
- A frontend component test needs to mock a fetch client.
- An integration test needs an MSW handler for an outbound call.

## When NOT to Invoke

- For contract tests (use `/skill-api-contract-test`).
- For real integration tests where the dependency should actually run.
- For production code stubs.

## Inputs

- **target**: symbol or module path to mock.
- **framework**: `pytest`, `vitest`, or `msw`.
- **scenario** (optional): `success` (default), `error`, or `empty`.

## Procedure

1. Resolve the target and read its signature(s).
2. For `pytest`: generate a fixture under `api/tests/fixtures/` that patches the symbol with `unittest.mock.MagicMock` and sets a return value matching the Pydantic model.
3. For `vitest`: generate a `vi.mock(...)` block with a typed return value drawn from the existing builder or a literal.
4. For `msw`: generate a handler under `frontend/src/test-utils/msw/` returning a synthetic response.
5. Apply the `scenario` to choose return shape:
   - `success` → fully populated valid response.
   - `error` → raises / returns 4xx/5xx with a synthetic error body.
   - `empty` → empty list or null result.
6. Write the mock to the conventional location.

## Outputs

- New mock file at the conventional location, imported from the nearest test-utils barrel if one exists.
- Summary of the mocked symbol, framework, scenario, and return shape.

## Safety

- Never invokes the real dependency during generation.
- Never embeds real credentials or tokens in mock payloads.
- Never mocks security-sensitive modules (auth, audit logging) without a reminder that the mock must not be reused in integration tests.
- FedRAMP: all mock payloads use synthetic IDs and `@example.test` emails.

## Examples

**Example 1 — Pytest.** Mock `OpportunitySearchClient.query` with a 3-item success payload.

**Example 2 — Vitest.** Mock `fetchOpportunities` to return an empty list, exercising the empty-state component.

**Example 3 — MSW.** Add a handler for `GET /v1/opportunities/search` returning a 500 to test error UI.

## Related

- `.cursor/skills/skill-generate-factory/` — factories for shared return values.
- `.cursor/skills/skill-api-contract-test/` — contract tests, not mocks.
