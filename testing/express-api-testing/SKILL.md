---
name: express-api-testing
description: Use when writing or modifying tests for Express routes ג€” webhook handlers, Claude API mocking, integration tests with supertest. Covers `tests/routes/` patterns.
---

# Express API Testing skill

## When to invoke

- Adding a new route in `src/routes/`
- Modifying webhook handlers (Make, WhatsApp, Gmail callbacks)
- Refactoring Master Orchestrator entry points
- Reproducing a production bug as a regression test

## Stack

- **Test runner**: vitest
- **HTTP**: supertest
- **Claude API mock**: `tests/helpers/mock-anthropic.ts` ג€” returns canned tool_use / text responses
- **Integration mocks**: each `src/integrations/*/mock.ts` is the default in tests

## Hard rules

1. **No real network calls in tests** ג€” every external client (Anthropic, Make, Gmail, Calendar, Drive, WhatsApp, CRM, OCR) must be mocked. CI has no outbound network
2. **Test the route, not the orchestrator internals** ג€” for route tests, mock the orchestrator response; orchestrator has its own unit tests
3. **Signature verification must be tested** ג€” at least one passing case + one failing-signature case per webhook
4. **Idempotency must be tested** ג€” send same `event_id` twice, second response must be 200 + "duplicate" marker, no side effects
5. **Hebrew payloads in fixtures** ג€” store real-shape Hebrew strings in `tests/fixtures/`, do not inline-escape unicode in test files

## Standard test layout

```ts
describe("POST /webhooks/whatsapp", () => {
  it("acks valid signed payload", async () => { });
  it("rejects bad signature with 401", async () => { });
  it("deduplicates by event_id", async () => { });
  it("returns 400 on schema mismatch", async () => { });
  it("responds within 3s", async () => { });
});
```

## Coverage expectations

- Every route handler: happy path + bad signature + bad schema + duplicate event
- Every tool handler: happy path + each documented error mode
- Orchestrator routing: one test per routing rule in the decision tree

## Running

`npm test` runs all. `npm test -- routes` filters. `npm run test:watch` for TDD. CI gate: tests + typecheck + lint must all pass.