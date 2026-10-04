---
name: api-integration
description: Use this skill whenever a task requires integrating with an external or internal API — HTTP clients, SDK calls, gRPC stubs, webhooks, or any network boundary. Verifies that an API spec (OpenAPI/Swagger, GraphQL schema, Protobuf, AsyncAPI, or equivalent) is configured and referenced in the plan or design artifact, then probes the endpoint to confirm reachability in the current environment. If the spec is missing or the connection is unavailable, this skill warns and offers to scaffold a mock (MSW, Prism, WireMock, a local fake, or a typed fixture layer) rather than letting silent stubs leak into the diff. Trigger proactively in Design and Build whenever the plan's in-scope files include HTTP clients, SDKs, `openapi.yaml`, `schema.graphql`, `.proto` files, `fetch`/`axios`/`httpx`/`requests` usage, or any phrase like "integrate with <service>", "call the <service> API", "webhook", "third-party".
---

# API Integration

Confirm the integration contract is real and reachable before code depends on it. Silent stubs are the failure mode this skill prevents — code that "works" locally and surprises in staging/prod because the real endpoint was never exercised.

## When this skill runs

- **Design phase** — when the tech spec describes an API boundary. Confirms a spec exists (or needs to be written) and is referenced.
- **Build phase** — when in-scope files include integration code. Probes the endpoint; offers a mock if unreachable.

This is a **warn + offer** skill. It does not block. The human decides whether to proceed with a mock, a real endpoint, or to pause the build to fix the integration environment.

## The two checks

### 1. Spec check

Look for an API contract artifact in the repo (or referenced by URL in the design):

- OpenAPI / Swagger (`openapi.yaml`, `swagger.json`)
- GraphQL schema (`schema.graphql`, introspection output)
- Protobuf (`*.proto`)
- AsyncAPI / JSON Schema / Avro for event contracts
- A published SDK with typed clients

If **no spec** is found and the plan doesn't explicitly justify its absence:

> ⚠️  No API spec found for the integration with `<service>`. Options:
>   1. Point me at an existing spec (path or URL) and I'll wire types from it
>   2. I can draft an OpenAPI/GraphQL/Proto stub for the endpoints this task needs — you review before code depends on it
>   3. Proceed without a spec (not recommended — types will be hand-written and drift is likely). Document the choice in the design.
>
> Which would you like?

Wait for the human's decision. Do not write integration code in the meantime.

### 2. Reachability check

Probe the endpoint in the current environment using the tool configured in `config/tools.json` (curl, the SDK's health call, or a project-specific probe). Suitable probes:

- `GET /health`, `/status`, `/.well-known/...` if the spec advertises one
- An introspection query for GraphQL
- A listed-allowed read endpoint with no side effects

If **unreachable** (timeout, DNS failure, 5xx, auth wall that can't be satisfied locally):

> ⚠️  Cannot reach `<service>` at `<url>` from this environment.
>   Possible reasons: VPN required, credentials missing, staging is down, sandbox not provisioned yet.
>
>   Rather than hardcoding stubs inline, I recommend scaffolding a mock so the contract stays explicit:
>     • MSW (browser/Node fetch interception) — good for frontend & SDK-level tests
>     • Prism (spins up a server from the OpenAPI spec) — good when the code calls the network directly
>     • WireMock / LocalStack — good for AWS-like or enterprise services
>     • A typed fixture layer (hand-rolled, driven by the spec types) — good for a few calls in a small service
>
> Want me to scaffold one of these? If so, which? Or can you unblock the real endpoint and I'll re-probe?

Wait for the decision. If the human chooses a mock, the mock goes in a clearly labeled test-scope location (`tests/mocks/`, `src/mocks/`, or the framework's conventional path) — never inline with production code paths.

## What NOT to do

- Do **not** create mocks unprompted. Offer; wait for approval.
- Do **not** hardcode response shapes inline "for now." That is the anti-pattern this skill exists to prevent.
- Do **not** treat the mock as the source of truth. The spec is the source; the mock is a projection of it.
- Do **not** bypass this skill via `/fix-fast`. If a fix genuinely requires touching an API boundary without a spec, that's a scope change — open a change request.

## Gracefully degrading

- No `curl` / no network tooling configured? Report the spec check, skip the probe, and note the gap in the design artifact.
- Spec exists but is in a format the project's codegen can't consume? Flag it, offer to convert or to hand-roll types — do not silently skip.

## Artifact hooks

- The **design artifact** should list: spec location, endpoint URL per environment (dev/staging/prod), auth mechanism, and mock strategy (if any).
- The **build artifact** should record: which probe was run, its result, and — if a mock was scaffolded — its location and the spec version it tracks.

## Related

- `skills/design/SKILL.md` — invokes this skill when the tech spec describes an API
- `skills/build/SKILL.md` — invokes this skill when in-scope files touch an integration boundary
- `skills/surgical-edit/SKILL.md` — mocks count as their own scope; list them in the plan alongside production files
