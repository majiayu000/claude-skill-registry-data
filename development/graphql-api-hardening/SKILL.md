---
name: graphql-api-hardening
description: >-
  Use when editing an Apollo Server mock or any GraphQL resolver, error formatter, validation rule,
  or response shape, and when changing the pinned upstream API service version. Triggers include
  createUser or clientMutationId handling, formatError, validationRules, parseOptions,
  includeStacktraceInErrorResponses, "Cannot query field", a client-supplied id, page-size or
  query-depth limits, and edits under docker/apollo-server.
---

# GraphQL API hardening

## Profile keys consumed

- `make.test_unit_server`
- `framework.graphql_mock`

## Overview

The local Apollo mock is the shape every client in these repository shapes is written against, so an
unsafe default there ships as an unsafe assumption in production code. Four patterns are
non-negotiable when touching it: server-owned identity, allow-listed responses, a query budget, and
a single upstream version pin.

When `framework.graphql_mock` is `null` there is no local mock to harden — skip with a recorded
note. Likewise skip the server-side suite with a recorded note when `make.test_unit_server` maps to
`null`.

## When to use

- Adding or changing a resolver, especially a mutation that creates a record.
- Changing the error formatter or anything that decides what a client sees on failure.
- Adding or relaxing depth, cost, page-size or parse limits.
- Bumping the pinned upstream contract version.
- Reviewing a pull request that touches any of the above.
- Not for: client-side Apollo cache, link, or hook work.

## Applicability by repository shape

- **React SPA shape** (feature modules under the source root, a bootable app, an aggregate CI
  target): partial — the mock lives in `docker/apollo-server/` with `lib/resolvers.ts` and
  `lib/format-error.ts`, the target mapped by `make.test_unit_server` runs the server-side suite,
  and the upstream pin is a GraphQL-schema version variable plus an OpenAPI-spec version variable in
  `.env`, reconciled by the repository's codegen-check, contract-diff and contract-drift targets.
  Identity is already server-owned, but the mock creates records `confirmed: true`, and the query
  budget and the strict response allow-list are guidance here, not yet implemented.
- **Next.js app shape** (routed pages, no aggregate duplication gate): yes —
  `docker/apollo-server/` carries `resolvers.ts`, `user-input.ts`, `error-formatting.ts` and
  `query-guards.ts`; tests live in `src/test/apollo-server/`; a single upstream-version variable in
  `.env` and `.env.example` is the pin, refreshed by the repository's contract-update target and
  checked by its API-version lint target.
- **Component-library shape** (Storybook-first, no bootable app, published package): no — no server
  or resolvers.

Only `make.test_unit_server` has a logical key; the contract targets and the pin variables are named
by the repository. Concretely:

```bash # profile-example
# React SPA shape — pins GRAPHQL_SCHEMA_VERSION + OPENAPI_SPEC_VERSION in .env
make test-unit-server        # runs tests/apollo-server/
make codegen-check
make contract-diff
make check-contract-drift

# Next.js shape — single pin USER_SERVICE_VERSION in .env and .env.example
make update-contracts        # re-fetch the pinned artifacts
make lint-api-versions       # assert the pin and the artifacts agree
```

## The four patterns

### Server-owned identity

Generate the primary key in the resolver; never read it from input, and never derive it from a
client-supplied correlation value such as `clientMutationId`. A client-writable key lets an attacker
forge records, collide with an existing one, or overwrite it. Create records in the unconfirmed
state and let only a verified token flip that. Build the stored entity from an explicit allow-list
of input properties so a field like `id` or `confirmed` cannot be mass-assigned, and key the store
by a canonical form of the natural identifier (a normalised email) so a duplicate is rejected rather
than silently overwriting.

### No internal detail in responses

Rebuild the response field by field from an allow-list, at both levels — the error and its
extensions. A client sees a stable `code`, an authored generic `message`, a correlation id it can
quote to an operator, and an enumerated `reason` the resolver chose. Nothing derived from the caught
error leaves the process; log it internally against the correlation id instead. Pin the stacktrace
option off, and check extension values as well as keys, since a key-only allow-list still lets an
arbitrary object through under a permitted name. Spreading the framework's formatted error and then
overriding a field is the anti-pattern this replaces: it carries whatever a future dependency bump
adds.

### Query budget

Apply depth, cost and page-size validation rules, and bound the parser itself with a token limit —
validation runs after parsing, so a document large enough to exhaust the parser never reaches a
validation rule. Saturate at the ceiling and reject with a client error rather than crashing. Scope
page-size checks per operation, not globally, and re-check them after the operation resolves,
because a limit supplied through a variable is not visible while the document is being validated.

### Single version pin

One variable names the upstream API service release, and the GraphQL schema, the OpenAPI spec and
any mock fixture all interpolate it. Edit the pin in the environment file and its example only,
re-fetch the artifacts through the repository's contract target, and commit the refreshed artifacts
in the same change so the diff shows what moved upstream. Drift between two pinned versions makes
contract tests agree with nothing real.

## Common mistakes

- Returning the caught error's message "only in development" — the branch is one environment
  variable away from production, and the field is in the response type either way.
- Exporting the resolver's store so tests can seed it — that hands every in-process consumer the
  write path the input allow-list exists to close. Export read-only and reset helpers instead.
- Adding a resolver without extending the depth, cost and page-size coverage that guards it.
- Hardcoding a version tag next to the pin rather than interpolating it.
- Landing any of this without a server-side unit test asserting the response contains only the
  allow-listed fields.
