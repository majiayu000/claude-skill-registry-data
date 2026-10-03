---
name: nestjs-e2e-practices
description: >
  Design, implement, review, and repair real HTTP end-to-end tests for source-accessible NestJS
  applications. Use when working on NestJS E2E suites, production-like test bootstrap, Jest
  discovery, main or feature orchestrators, deterministic execution, isolated real databases,
  migrations, HTTP-created fixtures, real authentication, public API contracts, teardown, or
  controlled doubles for external services such as email providers. Do not use for unit tests,
  repository-only integration tests, black-box tests against deployed APIs without NestJS source
  access, non-NestJS E2E tests, or browser-only UI testing.
license: MIT
metadata:
  author: AutanaSoft
  version: '0.1.0'
---

# NestJS E2E Practices

Build E2E suites that prove the delivered NestJS system through its public HTTP boundary. Load only
the cards needed for the current decision; the cards own detailed rules, examples, exceptions, and
sources.

## When to Apply

- Create, extend, review, or repair NestJS HTTP E2E tests.
- Design Jest discovery, a main orchestrator, feature orchestrators, shared context, or teardown.
- Configure a production-like NestJS test application and isolated database lifecycle.
- Create fixtures, validation cases, authentication flows, and public contract assertions.
- Isolate an external email, payment, SMS, webhook, or similar out-of-process dependency.

Do not apply this skill to unit tests, repository-only integration tests, black-box tests against
deployed APIs without NestJS source access, non-NestJS APIs, or browser-only UI testing.

## Rule Categories by Priority

### CRITICAL — Execution and lifecycle

Select the orchestration card for runner discovery, lifecycle ownership, shared state, ordered
flows, or teardown.

### CRITICAL — Runtime and infrastructure

Select the runtime card for production-derived bootstrap, real HTTP and persistence, isolated
infrastructure, migrations, or authentication.

### CRITICAL — External service boundaries

Select the external-boundary card for controlled substitution of out-of-process dependencies while
keeping the application internals real.

### HIGH — Data and public contracts

Select the data and contracts card for fixtures, seeds, payload variants, observable effects, or
public API assertions.

## Quick Reference

- `e2e-orchestrate-execution-and-lifecycle` - Own discovery, lifecycle scope, typed flow context,
  registration, and teardown.
- `e2e-run-real-application-and-infrastructure` - Run the production-like NestJS application with
  real, isolated infrastructure.
- `e2e-build-data-and-assert-contracts` - Select HTTP setup or deterministic bounded seeds and
  verify public contracts or persisted effects.
- `e2e-isolate-external-service-boundaries` - Substitute only justified out-of-process adapters.

## Workflow

1. Identify whether the task concerns orchestration, runtime infrastructure, data/contracts, or an
   external boundary.
2. Inspect the production root module and bootstrap, including adapter, global pipes, filters,
   interceptors, prefix, logging, and request ID behavior.
3. Inspect Jest or the active runner's discovery, concurrency, setup, teardown, and project
   commands.
4. Inspect database administration, migrations, authentication, and external provider boundaries.
5. Load only the matching cards from How to Use.
6. Design shared main/feature ownership or a genuinely isolated suite owner before implementing
   suites.
7. Run the focused verification and then the applicable complete E2E owner when commands exist.
8. Report the Output Contract without exposing credentials, tokens, or secrets.

## How to Use

Load only the card that owns the decision being made; load more than one only when the same suite
crosses those boundaries.

- For runner discovery, lifecycle ownership, shared application or database state, intentional
  ordered flows, typed contexts, feature registration, or teardown, load
  [Orchestrate E2E execution and lifecycle explicitly](references/e2e-orchestrate-execution-and-lifecycle.md).
- For production-derived bootstrap, real HTTP, isolated databases, migrations, providers, or
  authentication, load
  [Run the real application and isolated infrastructure](references/e2e-run-real-application-and-infrastructure.md).
- For HTTP-created fixtures, bounded real-persistence seeds, payload variants, public errors,
  headers, effects, or forbidden fields, load
  [Build realistic E2E data and assert public contracts](references/e2e-build-data-and-assert-contracts.md).
- For email, payment, SMS, webhooks, or another out-of-process dependency, load
  [Isolate only external service boundaries in E2E tests](references/e2e-isolate-external-service-boundaries.md).

## Verification

- Discover the project's official command for the applicable E2E lifecycle owner.
- Run the smallest supported focused target without bypassing its lifecycle.
- Run the complete E2E project when the environment is available.
- Run repository-defined lint, formatting, and validation for changed artifacts.
- If infrastructure is unavailable, report the exact blocked command and unverified behavior.

## Output Contract

Report all of the following:

- Cards applied and files created or modified.
- Applicable lifecycle owner, imported orchestrators or suites, and any explicit registration order.
- Real HTTP flows and internal providers exercised.
- Isolated database, migration, and teardown strategy.
- Data created through HTTP and every justified seed.
- Canonical constants or factories reused and invalid variants derived.
- Public contracts, headers, effects, and forbidden fields asserted.
- External adapters substituted, why, and which real flow remains covered.
- Commands executed, results, and residual verification gaps.
