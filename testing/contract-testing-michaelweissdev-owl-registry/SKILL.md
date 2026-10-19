---
name: contract-testing
description: >
  Prevent integration breakage between services with contract testing: consumer-driven contracts
  with Pact (consumer tests, provider states, provider verification, broker workflow, pending
  pacts, can-i-deploy) and schema-first contracts with OpenAPI (breaking-change diffing,
  schema-conformance testing with Schemathesis). Includes matcher strategy, versioning and
  deploy-gating, and when contracts are the wrong tool. Use when separately deployed consumers
  and providers (microservices, mobile apps vs API, event/message consumers) break each other
  in integration or when end-to-end tests are slow and flaky. Do NOT use for in-process
  integration tests (integration-testing), API design itself (api-design), gRPC schema
  evolution (grpc-protobuf), or browser E2E (playwright-testing).
compatibility: >
  Agent Skills-compatible coding agents. Pact (JS, JVM, Python, Go, others) with a Pact Broker
  or PactFlow; OpenAPI 3.x specs; Schemathesis CLI. Check your Pact library version for exact API names.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "contract-testing, pact, openapi, consumer-driven-contracts, schemathesis, microservices, can-i-deploy"
  topics: "software-development, testing, api, microservices"
---

# Contract Testing

A contract captures what a consumer actually needs from a provider (or what a provider promises in a schema), and is verified independently on each side without both running together. The goal: answer "is it safe to deploy this version?" in minutes, with no shared test environment.

Boundaries: `api-design` decides what the API should look like; `integration-testing` exercises real components together; `grpc-protobuf` covers protobuf compatibility rules; [property-based-testing](../property-based-testing/SKILL.md) is the engine behind schema-conformance fuzzers.

## Choose the approach

| Situation | Use |
|---|---|
| Known set of consumers you can coordinate with; need to know which fields each actually uses | Consumer-driven contracts (Pact) |
| Public API with unknown consumers | Provider-owned OpenAPI spec + breaking-change diff + schema-conformance tests |
| Both | Spec as source of truth for shape, Pact for real consumer usage and provider states |
| Async messaging (queues/events) | Pact message pacts or schema registry compatibility checks |
| One service, one team, one repo | Often an in-process integration test is enough; do not add a broker for this |

## Non-negotiable rules

1. A contract states only what the consumer depends on. Do not copy the whole provider response into the pact; over-specified contracts make providers brittle and defeat the purpose.
2. Contracts and provider states must not contain real personal data, secrets, or production tokens. Use fabricated fixtures. Pacts are published to a broker visible to many teams.
3. Provider verification runs against a locally started provider with stubbed downstreams and a test database seeded by provider states, never against production. Credentials for the broker come from CI secrets, never from files in the repository.
4. Do not "fix" a failing verification by editing the pact on the provider side or by loosening matchers without the consumer's agreement. The failure is the signal; resolve it by changing code or negotiating the contract.
5. Schema-conformance tools (Schemathesis) send malformed and unusual requests: point them only at environments you own and are authorized to test, usually a disposable test deployment, never production.
6. A green contract check is not a substitute for tests of business behavior; it verifies the interface only.

## Workflow A: Consumer-driven contracts with Pact

### 1. Write the consumer test

Pact describes each interaction as: provider state (precondition), expected request, minimal expected response. The test runs your real client code against a Pact mock server, then writes the pact file.

Sketch in Pact JS V3 style (names per the `@pact-foundation/pact` package; verify against your installed version, this snippet was not executed):

```js
const { PactV3, MatchersV3 } = require('@pact-foundation/pact');
const { like, eachLike } = MatchersV3;

const provider = new PactV3({ consumer: 'web-app', provider: 'orders-api' });

it('lists open orders', async () => {
  provider
    .given('user 42 has open orders')
    .uponReceiving('a request for open orders')
    .withRequest({ method: 'GET', path: '/users/42/orders', query: { status: 'open' } })
    .willRespondWith({
      status: 200,
      headers: { 'Content-Type': 'application/json' },
      body: { orders: eachLike({ id: like('o-1'), total: like(1999) }) },
    });

  await provider.executeTest(async (mockServer) => {
    const orders = await new OrdersClient(mockServer.url).listOpen(42);
    expect(orders[0].id).toBeDefined();
  });
});
```

Matching strategy (from Pact's matching guidance): be exact on what you *send* (you control it), and as loose as possible on what you *receive*: match types (`like`), arrays with element shape (`eachLike`), regexes for formats you rely on. Only include fields your client reads. Avoid random data in pacts; it makes identical pacts look changed to the broker.

One interaction per distinct behavior, not per endpoint variant. Test error responses the consumer handles (404, 409 conflict, 422), not only the happy path.

### 2. Publish the pact with version and branch

With the Pact CLI: `pact-broker publish <pact dir> --broker-base-url <url> --consumer-app-version <sha> --branch <branch>` (also `--auto-detect-version-properties` in CI). Use the commit SHA as the version. Configure the consumer's main branch in the broker.

### 3. Provider verification

The provider test replays each interaction against the real provider, calling provider state handlers first. A verification passes if each response contains at least the expected data. Typical config (Pact JS `Verifier` options; verify names for your language/version): provider name, base URL of the locally running provider, `stateHandlers`, broker URL and token from env, `providerVersion` (commit SHA), `providerVersionBranch`, `consumerVersionSelectors`, `enablePending`, `publishVerificationResult` (only in CI).

Consumer version selectors tell the provider which pacts to verify. A sensible start from the docs: `[{ mainBranch: true }, { deployedOrReleased: true }]`, plus `{ matchingBranch: true }` when consumer and provider feature branches share a name. This ensures the provider is checked against what is on the consumer's main branch and against what is live.

Provider state handlers: each named state (`'user 42 has open orders'`) maps to code that arranges data. Keep them small, idempotent, and independent; reset between interactions.

### 4. Pending pacts and the deploy gate

- Enable pending pacts on the provider so a *new or changed* consumer expectation that the provider does not yet meet does not break the provider's own build; the failed result is still published to the broker, so the consumer cannot deploy until the provider catches up. Per the docs a pact is pending until a successful verification is published, and requires Broker support (the docs cite OSS Broker 2.60.0 or later).
- Gate deploys on `pact-broker can-i-deploy --pacticipant <name> --version <sha> --to-environment <env>` (exit code 0 means safe, nonzero not). After deploying run `pact-broker record-deployment --pacticipant <name> --version <sha> --environment <env>`. The broker needs recorded deployments to know what is live; without them `can-i-deploy` and `deployedOrReleased` are blind.
- Use a webhook on `contract_requiring_verification_published` to trigger provider verification when a consumer publishes a changed pact (`pact-broker create-webhook ... --contract-requiring-verification-published`).
- Check `can-i-deploy` on both sides: the consumer must not deploy ahead of the provider, and the provider must not deploy a breaking change that live consumers depend on.

### 5. Evolving safely

Provider adding fields: safe. Removing/renaming fields, changing types, tightening validation, new required request fields: breaking; use expand-then-contract: add new alongside old, migrate consumers (watch `can-i-deploy` and broker matrix), then remove old.

## Workflow B: Schema-first (OpenAPI)

1. Keep the OpenAPI document in the provider repository as the source of truth, validated in CI by a linter of your choice.
2. Breaking-change gate: diff the PR spec against the main branch spec in CI. Tools such as oasdiff provide `breaking`/`changelog` style commands (I did not verify its CLI flags; check its current README). Fail the PR on breaking changes unless explicitly approved and versioned.
3. Conformance: run Schemathesis against a disposable test instance. Verified CLI (reference docs): `st run SCHEMA --url BASE_URL --checks not_a_server_error,response_schema_conformance --max-examples 100`; exit code 1 means a check failed, 2 means it could not run (bad schema, no operations tested). Add auth via `--header`/`--auth` using CI secrets. Each finding comes with a reproducer; turn real bugs into explicit regression tests.
4. Consumers generate clients or types from the spec and test with a mock server from the same spec to avoid drift.

OpenAPI conformance checks the provider honors its own schema; it does not tell you which fields consumers actually use. That is Pact's job.

## Worked example: field rename

`orders-api` wants to rename `total` to `totalCents`. Web-app's pact has `total: like(1999)`.

1. Provider PR renames the field; provider verification against `mainBranch` and `deployedOrReleased` pacts fails (response lacks `total`). The failure appears on the provider PR because the pact is not pending: it was already verified.
2. Provider adds `totalCents` and keeps `total` (deprecated); verification passes.
3. Web-app updates its pact to `totalCents`, publishes; the pact is pending for the provider until verified; the provider already satisfies it, so verification succeeds and `can-i-deploy` goes green for the web-app.
4. After web-app (and other consumers) are deployed and recorded, provider removes `total`; verification against deployed consumers confirms it is safe.

## Anti-patterns

- Using Pact as a functional test of provider logic ("returns correct tax") instead of interface shape.
- Whole-body exact matching of responses.
- Contracts generated from the provider's response (provider-driven recordings) and called "consumer-driven".
- Using shared mutable test data in provider states, or states that depend on order.
- Omitting `record-deployment`, then trusting `can-i-deploy`.
- Treating the broker as optional once there is more than one consumer: pacts passed around by hand rot.
- Fuzzing a production API "to check the schema".

## Verification checklist

- [ ] Each pact interaction names a provider state and includes only fields the consumer uses
- [ ] Matchers are strict on requests, type-based on responses; no random data
- [ ] Pacts and fixtures contain no real data or secrets
- [ ] Provider verification runs in CI with stubbed dependencies and publishes results with version and branch
- [ ] Pending pacts enabled; consumer version selectors reviewed
- [ ] `can-i-deploy` gates deploys and `record-deployment` runs after deploy
- [ ] OpenAPI diff and conformance steps target owned, non-production environments

## References

- [Pact setup notes and CI recipe](references/pact-ci.md)
- [Scenarios for evaluating this skill](references/scenarios.md)
- [Sources and provenance](references/sources.md)
