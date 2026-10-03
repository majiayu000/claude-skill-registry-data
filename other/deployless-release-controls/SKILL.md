---
name: deployless-release-controls
description: Runtime release controls for deployless repositories. Use when a repo needs feature flags, kill switches, capability gates, targeted rollout, remote config, routing rules, or a provider-neutral release-control facade independent of language and provider.
metadata:
  priority: 6
  pathPatterns:
    - "src/**"
    - "app/**"
    - "lib/**"
    - "config/**"
    - "docs/**"
  promptSignals:
    phrases:
      - "feature flag"
      - "kill switch"
      - "release control"
      - "runtime flag"
      - "remote config"
      - "targeted rollout"
    allOf:
      - [deployment, release]
      - [flag, rollout]
    anyOf:
      - "LaunchDarkly"
      - "Unleash"
      - "Statsig"
      - "ConfigCat"
      - "capability gate"
    noneOf: []
    minScore: 5
---

# Runtime Release Controls for Any-Language Repositories

## Purpose

Introduce runtime release controls so merging and deploying code does not automatically expose unfinished or risky behavior to users.

In a deployless workflow:

- deployment moves code into the runtime
- release exposes behavior
- release can be changed without a new deploy when practical
- risky behavior has a kill switch
- flags are observable, testable, owned, and eventually removed

## Control types

Choose one or more based on the repo's architecture.

| Control type | Use when |
| --- | --- |
| Feature flag | Product or behavior can be toggled per environment, user, cohort, tenant, request, or percentage |
| Kill switch | Behavior must be disabled quickly during incident response |
| Capability gate | Access depends on plan, permission, entitlement, tenant, role, or environment |
| Routing rule | Traffic must shift between implementations, versions, regions, or backends |
| Remote config | Parameters should change without redeploying code |
| Build-time guard | Runtime control is impossible; acceptable only with documented limitation |

Prefer runtime controls over build-time guards when the platform allows it.

## Inputs to inspect

- Existing flag or config providers
- Authentication and user/tenant context
- Request context or execution context type
- Dependency injection or service locator conventions
- Logging and tracing conventions
- Test framework
- Configuration loading
- Environment-variable usage
- Mobile or frontend remote-config system, if applicable
- Worker, CLI, batch, or background-job context

## Provider-neutral flag contract

Create a small release-control facade using the language's normal idioms.

The contract should support:

```text
is_enabled(flag_key, context, default=false) -> boolean
get_variant(flag_key, context, default_variant) -> variant
get_value(config_key, context, default_value) -> typed value
```

Where `context` can include:

```text
environment
service_name
service_version
request_id
trace_id
actor_id or anonymous stable key
tenant_id
role or plan
region
route or operation name
```

Do not include raw personally sensitive data in flag context. Prefer stable opaque IDs or hashed keys when needed.

## Recommended file layout

Use the repo's conventions, but these paths are good defaults:

```text
src/release-controls/
  client.*
  context.*
  provider.*
  local-provider.*
  test-provider.*
  README.md
config/
  flags.example.*
docs/
  release-controls.md
  flag-lifecycle.md
```

For languages without a `src` convention, place the module beside existing application infrastructure code.

## Language adaptation examples

Use native idioms:

- JavaScript/TypeScript: exported module, interface, dependency injection, middleware context
- Python: protocol/abstract base class, module-level provider, FastAPI/Flask/Django integration
- Go: interface plus context-aware client, `context.Context` integration
- Rust: trait plus typed context struct, feature-gated provider only if needed
- Java/Kotlin: interface plus DI bean/service, servlet/filter or framework interceptor context
- .NET: interface plus dependency injection service, middleware context
- Ruby: module/service object with request context
- PHP: service class registered in framework container
- Elixir: behaviour plus application config and plug context
- C/C++: abstraction header and provider implementation; keep runtime config reload explicit
- Mobile: remote config or backend-delivered flags with local cache and safe defaults

## Implementation procedure

### 1. Reuse existing provider when present

If the repo already uses a provider, standardize access behind a facade rather than adding another provider.

Examples of existing providers:

- LaunchDarkly
- Unleash
- Statsig
- ConfigCat
- Flagsmith
- Split
- Flipt
- cloud platform remote config
- in-house entitlement or config service

### 2. Add a local provider if no provider exists

A local provider is acceptable as a first step. It should:

- read from environment variables, local config, or a checked-in example file
- default to safe values
- avoid secrets
- be easy to replace with a managed provider
- support tests deterministically

Do not add production credentials or vendor tokens.

### 3. Define flag metadata

Every flag should have metadata in docs or config:

```text
key
purpose
owner
created date
expected removal date
safe default
rollout plan
kill-switch behavior
metrics or logs to watch
cleanup issue or task
```

### 4. Add test provider

Add a deterministic test provider so tests can set flags explicitly.

Tests should cover:

- default-off behavior
- enabled behavior
- missing flag behavior
- variant behavior, if variants are supported
- kill-switch behavior
- context-sensitive behavior, if used

### 5. Wrap risky behavior at stable boundaries

Prefer flag checks at boundaries:

- route handler
- controller/action
- command handler
- use-case/service boundary
- frontend page or component boundary
- background job entrypoint
- external integration adapter
- infrastructure rollout module

Avoid scattering flag checks deep inside unrelated business logic unless the flag is truly local to that logic.

### 6. Add observability

Log or trace release-control decisions in a low-cardinality way:

```text
flag_key
flag_enabled
variant
provider
default_used
request_id
trace_id
service_version
```

Do not log sensitive user data.

### 7. Add lifecycle docs

Create or update `docs/flag-lifecycle.md`:

```markdown
# Release-control lifecycle

1. Create the flag with an owner and safe default.
2. Merge dormant code to main behind the flag.
3. Deploy automatically from main.
4. Enable for internal/test cohort.
5. Ramp gradually while watching metrics and traces.
6. Commit the change by setting the flag to default-on or 100%.
7. Remove stale flag branches and dead code.
8. Delete provider-side flag config.
```

## Naming rules

Use stable names:

```text
area.capability.behavior
checkout.payment.new_processor
search.ranking.v2
billing.invoice_pdf_renderer
worker.email_digest.v2
```

Avoid names tied to temporary ticket IDs only. Ticket IDs can appear in metadata.

## Defaults and failure behavior

- New user-facing behavior should usually default off.
- Safety fixes may default on with a kill switch.
- Missing provider should fail closed for risky behavior.
- Missing provider may fail open only for clearly safe maintenance behavior.
- Provider outages must be handled explicitly.
- Mobile clients should cache safe defaults and tolerate stale config.

## Release-control cleanup

A flag is stale when:

- rollout is permanently 100%
- old behavior no longer needs rollback
- associated migration is complete
- dependent clients have aged out
- compliance signoff is complete, if required

When stale:

1. Remove dead branches.
2. Remove tests for obsolete behavior unless needed for compatibility.
3. Keep regression tests for the final behavior.
4. Remove provider config.
5. Update docs.

## Output

Create or update:

- release-control facade/module using the repo's language and conventions
- local provider and deterministic test provider
- example config without secrets
- tests for default and enabled behavior
- `docs/release-controls.md`
- `docs/flag-lifecycle.md`
- `docs/deployless-mainline-plan.md`, appending release-control details

## Acceptance criteria

This skill is complete when:

- feature exposure can be changed independently from deployment for at least one representative path
- code uses a central release-control facade rather than scattered ad hoc environment checks
- safe defaults are defined
- tests can force enabled and disabled states
- flag decisions are observable
- lifecycle and cleanup rules are documented
- no provider secret is committed

## Anti-goals

- Do not replace all authorization or entitlement checks with feature flags.
- Do not put sensitive data in flag context.
- Do not add a paid/vendor dependency when a facade and local provider are enough for the first step.
- Do not use flags as a permanent substitute for deleting obsolete code.
- Do not use build-time flags as the primary release mechanism when runtime control is available.
