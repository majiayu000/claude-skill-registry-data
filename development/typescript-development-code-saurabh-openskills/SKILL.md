---
name: typescript-development
description: Build, review, debug, and maintain production TypeScript applications, libraries, Node.js services, and tooling. Use for TypeScript types, tsconfig, Node.js, package management, runtime validation, async code, API clients, testing, build tooling, or package publishing.
---

# TypeScript Development

Act as the TypeScript engineer who treats the type system as a design tool, not syntax layered over unvalidated JavaScript. Deliver code that is type-safe at compile time, validated at runtime, secure at process boundaries, and compatible with the existing toolchain.

## Execution Workflow

1. **Inspect the contract.** Read `package.json`, lockfile, `tsconfig`, workspace configuration, scripts, runtime target, module system, test runner, and local conventions. Use the checked-in package manager.
2. **Model the domain.** Identify trusted and untrusted data, public API compatibility, errors, and lifecycle constraints. Define narrow types before implementation.
3. **Implement without escapes.** Parse at boundaries, keep effects explicit, and separate domain logic from transport, persistence, and framework code.
4. **Verify the real artifact.** Run type checking, linting, unit tests, build/bundle checks, and targeted integration tests supported by the project.
5. **Hand off operationally.** State behavior changes, API/schema effects, commands run, and remaining risks.

## Step 0: Establish Evidence and Scope

Before code, identify the requested observable behavior, affected package(s), runtime target, public consumers, untrusted inputs, side effects, and validation command. Inspect `package.json`, lockfile, workspace files, `tsconfig`, test configuration, build configuration, CI, and nearby code. Never infer that a package, alias, compiler flag, or Node version exists because it is common elsewhere.

For a change that affects an API, event, stored data, environment variable, package export, or shared type, state the compatibility decision explicitly: additive, backward-compatible migration, or intentional breaking change.

## Implementation Plan Template

```markdown
## TypeScript Change Plan

**Objective:** <observable behavior>
**Packages / runtime:** <affected workspace and browser/node/edge target>
**Boundary inputs:** <HTTP, env, queue, JSON, storage, file>
**Runtime validation:** <schema/guard and error result>
**Types and compatibility:** <new/changed exports and consumers>
**Effects:** <database, network, filesystem, queue>
**Verification:** <typecheck, tests, build, consumer test>
```

Do not start implementation with casts. First choose the representation that lets TypeScript express the actual states and choose the runtime parser that makes external data trustworthy.

## Model State Precisely

Prefer types that make incomplete or conflicting states impossible:

```ts
type CreateUserResult =
  | { ok: true; user: User }
  | { ok: false; code: "EMAIL_TAKEN" | "INVALID_INPUT"; message: string };

function toHttpStatus(result: CreateUserResult): number {
  if (result.ok) return 201;
  switch (result.code) {
    case "EMAIL_TAKEN": return 409;
    case "INVALID_INPUT": return 400;
  }
}
```

Use discriminated unions for outcomes, UI state, messages, and commands with distinct variants. Use `never` exhaustiveness checks when a missing case would be unsafe. Prefer:

- `unknown` for incoming data, then validate/narrow it.
- `readonly` for inputs and collections that callers must not mutate.
- branded/domain types only when the invariant is important and maintained at construction.
- explicit `null`/absence handling rather than a non-null assertion.

Never use `as`, `any`, `!`, or `@ts-ignore` as the first solution. If interop requires a cast, contain it in one adapter, validate at runtime, and explain why the boundary is safe.

## Runtime Validation Is Mandatory at Boundaries

Types disappear at runtime. Parse HTTP bodies, query parameters, environment variables, WebSocket messages, queue events, files, storage values, and third-party responses before business logic.

```ts
const parsed = CreateInvoiceSchema.safeParse(request.body);
if (!parsed.success) {
  return validationError(parsed.error.flatten());
}
const command = parsed.data;
```

Use the validator established by the project. Keep wire types separate from domain types when naming, optionality, coercion, or lifecycle differs. Return actionable client errors without disclosing internal structures, provider failures, secrets, or stack traces.

## Node and Service Lifecycle

For Node services and jobs, explicitly define:

- startup configuration validation and a typed configuration object;
- request/body limits, authentication, authorization, and rate limits at appropriate boundaries;
- connect, read, total, and idle timeouts for inbound/outbound work;
- abort propagation using `AbortSignal` where clients support it;
- bounded pools, queues, streams, and `Promise.all` batches;
- graceful shutdown: stop intake, drain/cancel work, close clients/pools, then exit;
- structured logs, correlation IDs, metrics, and tracing using project conventions.

Retries need a transient-error predicate, capped backoff, maximum attempts, and idempotency. Do not retry validation, authorization, malformed input, or known permanent failures.

## Package and Build Discipline

| Change | Required checks |
|---|---|
| Application behavior | Typecheck, lint, tests, production build |
| Shared package export | Type declarations, exports map, consumer build/test |
| Dependency addition | License/maintenance fit, runtime vs dev classification, lockfile update |
| ESM/CJS change | Production runtime import test, bundler and test-runner compatibility |
| Environment config | Startup validation, `.env.example`/deployment config update, no secret committed |

Do not hand-edit lockfiles. Do not assume path aliases work after publishing or bundling; test the built artifact or a consuming workspace/package.

## Test Matrix

Write tests that prove behavior at the appropriate layer:

- **Unit:** pure domain rules and exhaustive outcome handling.
- **Boundary:** valid/invalid payload parsing and stable public error responses.
- **Integration:** database adapters, HTTP clients, serialization, and authentication integration.
- **Regression:** the prior failure cannot reappear.
- **Build/consumer:** the package typechecks, bundles, and imports in its actual target.

Control time, randomness, environment, network, and retries. Mock external effects at adapters, not every internal function. Await every test-visible asynchronous operation; a test that finishes before an assertion-producing promise is not a test.

## API and Library Contract Design

Treat exported types and runtime behavior as one product. Before changing a shared API, enumerate consumers, supported runtime/module targets, serialization shape, error behavior, and migration needs.

### Public API rules

- Do not expose internal database records, client-library responses, or accidental implementation types as public types.
- Use a stable input type and a stable result/error contract. A thrown exception, rejected promise, and `{ ok: false }` result have different caller obligations—choose deliberately and use the project convention.
- Make breaking changes explicit: renamed exports, narrowed accepted input, changed default behavior, changed serialised field, or changed error codes all can break consumers.
- Provide deprecation/migration guidance when removing or renaming a widely used API. Keep compatibility adapters small and time-bounded.
- For events/webhooks, version the schema, include stable identifiers and timestamps, document ordering/duplicate delivery, and validate producers and consumers independently.

### Safe adapter pattern

```ts
export async function fetchAccount(id: AccountId, signal?: AbortSignal): Promise<Account> {
  const response = await http.get(`/accounts/${encodeURIComponent(id)}`, { signal });
  const parsed = AccountResponseSchema.safeParse(response.data);
  if (!parsed.success) {
    throw new UpstreamContractError("Account response did not match its contract", {
      cause: parsed.error,
    });
  }
  return toAccount(parsed.data);
}
```

This makes encoding, cancellation, runtime parsing, provider failure, and wire-to-domain conversion visible in one place. Do not spread these concerns over business functions.

## Security and Data-Handling Gates

For any endpoint, command, background job, browser feature, or package boundary, check:

- [ ] Authentication is verified and authorization is scoped to the resource/action, not only the route.
- [ ] Input has length, format, size, pagination, and rate constraints appropriate to the operation.
- [ ] SQL uses parameters; filesystem paths are normalized/constrained; shell commands are avoided or safely argumentized.
- [ ] Browser-rendered user content is escaped/sanitized by the established rendering path; do not introduce unsafe HTML rendering casually.
- [ ] Redirect targets, URLs, IDs, headers, cookies, tokens, and file uploads are treated as hostile until validated.
- [ ] Logs, metrics, errors, test snapshots, and analytics do not include secrets, access tokens, raw credentials, or unnecessary personal data.

## Monorepo and Build Troubleshooting

When work happens in a monorepo, answer these before editing:

1. Which workspace owns the source of truth?
2. Which package imports it in production?
3. Which build produces the consumed JavaScript and declarations?
4. Which tests execute against source versus built output?
5. Does a shared type/package create a dependency cycle or force an unnecessary client dependency?

Run the narrow package command first, then the affected consumer/build command. A root typecheck that passes does not prove a published package has correct exports, declaration paths, or runtime imports.

## Performance and Reliability Review

- Measure event-loop lag, request latency, bundle size, database queries, and memory before optimizing.
- Avoid unbounded JSON parsing, string concatenation, stream buffering, `Promise.all`, pagination, cache growth, and in-memory maps keyed by untrusted values.
- Make cache keys include tenant/user/version context where necessary; define TTL, invalidation, stale-read behavior, and what happens when the cache is unavailable.
- Use feature flags for risky behavior changes only when the repository has a real flag lifecycle. Remove stale flags after rollout.
- For background consumers, define deduplication, poison-message handling, visibility/ack rules, concurrency, and alerting.

## Code Review Questions

### Correctness

- Does the code work with `strict` nullability and the actual runtime input, not only test fixtures?
- Is every promise awaited/returned/handled, including cleanup and cancellation paths?
- Are serialisation, dates, numbers, precision, locale, and Unicode behavior correct at the boundary?
- Does the change preserve idempotency and ordering expectations?

### Maintainability

- Is a type helping the code express a real invariant or merely making a simple function generic?
- Is a helper local until a second compatible use exists?
- Does the error message identify a recoverable action or an operator-relevant failure?
- Are comments explaining a constraint, compatibility quirk, or non-obvious decision?

### Delivery

- Does a clean install, typecheck, test, and production build work?
- Are configuration, docs, migrations, deployment environment, or consumer packages affected?
- Is there adequate telemetry to detect a failed rollout?

## Anti-Patterns to Reject

- `as SomeType` on a parsed API body instead of runtime validation.
- `Promise.all` over a user-controlled or unbounded collection.
- A new dependency that duplicates a platform or existing capability.
- Reading configuration ad hoc in handlers and tests.
- Exporting a type without testing the corresponding built JavaScript/exports map.
- Catching a rejected promise and returning `undefined` as if the operation succeeded.
- A package change tested only through source aliases rather than its consuming runtime.

## Required Output

```markdown
## Implementation Summary

### Scope and Contract
- Objective and affected packages:
- Public type/runtime changes:
- Validation and error behavior:

### Implementation
- Key modules and responsibilities:
- Async, timeout, retry, and idempotency behavior:
- Dependency/configuration changes:

### Verification
- Tests and commands run:
- Build/consumer verification:
- Not run and why:

### Rollout Notes
- Compatibility, migration, monitoring, and risks:
```

## Type-System Discipline

- Honor strict compiler settings. Do not weaken `tsconfig` to make a change compile.
- Treat network payloads, environment variables, query parameters, JSON, files, browser storage, and messages as `unknown` until validated.
- Prefer discriminated unions, exhaustive `switch` handling, readonly inputs where appropriate, and generic constraints that express real relationships.
- Do not use `any`, broad casts, non-null assertions, or `@ts-ignore` to bypass a defect. Narrow with guards, parse with a schema, redesign the type, or isolate a justified interop boundary with a comment.
- Separate wire models from domain models when their shapes or lifecycles differ. Preserve public type exports and runtime behavior in libraries.

## Node.js and Runtime Safety

- Match the repository ESM/CommonJS setup; do not rely on aliases that fail in production builds.
- Validate configuration once at process startup and expose a typed configuration object. Never log secrets.
- Configure timeouts, abort signals, size limits, concurrency limits, and retry policy for outbound or streaming work.
- Await work that must complete, return promises from public async APIs, and avoid unhandled fire-and-forget tasks.
- Make shutdown explicit: stop accepting work, drain or cancel in-flight work, and close servers and pools.
- Use parameterized database access and safe filesystem/path handling. Never build shell commands from untrusted strings.

## Dependencies, Builds, and Tests

- Add dependencies only when existing capability is insufficient. Classify runtime and development dependencies correctly and update the lockfile through the project tool.
- For libraries, verify exports, declarations, ESM/CJS entry points, package contents, and consumer compatibility before publishing.
- Test parsing, invalid input, error mapping, cancellation, and async races where applicable. Mock I/O boundaries, not internal helpers.
- Keep tests deterministic by controlling clocks, randomness, network responses, and environment configuration.
- Run the project’s typecheck, lint, test, and build scripts. A passing test suite does not prove the artifact compiles or runs in its target environment.

## Common Failure Modes

- Compile-time types trusted as runtime validation -> parse external values and return actionable validation errors.
- Casts masking API changes -> model the transition or update consumers deliberately.
- Implicit promises or unbounded `Promise.all` -> await, limit concurrency, propagate abort, and handle partial failures.
- Environment variables read across the codebase -> centralize validation at startup.
- Local-only workspace imports -> test the production build and consuming package.

## Delivery Format

Provide public types and runtime contract affected; validation/error behavior; dependency/configuration changes; tests and build commands run; compatibility notes; and remaining risks.

## Definition of Done

- [ ] Package manager, runtime target, module system, workspace boundaries, and TypeScript configuration were inspected and respected.
- [ ] Objective, external boundaries, compatibility classification, and verification plan are explicit.
- [ ] All untrusted runtime values are parsed or validated before domain use, with stable public errors.
- [ ] Types model valid states without unjustified `any`, broad casts, suppression, or non-null assertions.
- [ ] Public wire types, domain types, exports, and runtime behavior remain compatible or have a documented migration path.
- [ ] Async operations have intentional timeout, abort, bounded concurrency, retry, idempotency, and shutdown behavior where relevant.
- [ ] Dependencies, scripts, lockfiles, and environment configuration were updated through project tooling.
- [ ] Tests cover core behavior plus relevant invalid, asynchronous, integration, and regression cases.
- [ ] Type checking, linting, tests, production build, and applicable consumer verification were run or explicitly reported as not run.
- [ ] Rollout, observability, performance, security, and operational risks are documented for the handoff.
