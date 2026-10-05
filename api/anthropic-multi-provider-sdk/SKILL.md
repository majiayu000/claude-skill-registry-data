---
name: anthropic-multi-provider-sdk
description: Design and verify Claude API access across Anthropic direct and supported cloud/platform integrations without hard-coded model IDs or silent failover. Use.
license: MIT
---

# Claude Multi-Provider SDK Routing

This is an integration-specific skill: the application intentionally uses Claude through one or more supported delivery platforms. It must not change the assistant's current host/provider.

## Discover

Inspect installed SDK packages/versions, existing clients, deployment cloud/region, credentials mechanism, model configuration, data residency/retention, quotas, billing, capabilities, and current tests. Verify current official Anthropic and cloud-platform documentation because package names, endpoints, model IDs, headers, and regional availability change.

## Configuration contract

Keep provider and model IDs in validated runtime configuration:

```text
AI_PROVIDER=<configured route>
AI_MODEL_ID=<exact ID verified for that route and region>
AI_REGION=<when required>
```

Never infer equivalence from a marketing family name. Build a capability record per route: tools, structured output, vision/files, streaming, context/output limits, caching, safety controls, beta headers, throughput, region, and pricing source/version.

## Abstraction

Normalize only application concepts that are truly common: request messages/content, tool schema, output events, usage, request ID, timeout/cancellation, and typed error categories. Preserve provider-specific fields behind explicit adapters rather than discarding them.

## Credentials and data

Use the platform's documented secret/IAM mechanism and least privilege. Do not print credentials or place them in prompts/config committed to git. Record where request data, logs, caches, and telemetry travel. A fallback to another platform is a data-boundary and billing change, not merely an error retry.

## Failover

Fail over only to an explicitly authorized route that supports the same required capabilities, region/privacy constraints, output contract, and cost ceiling. Use idempotency for external tool effects, bounded retries with jitter for proven transient errors, and circuit breakers. Never retry authentication, billing, invalid-request, or unsupported-capability errors indefinitely.

## Verification

Run adapter contract tests, model/config validation, tool/structured-output/stream tests, cancellation/timeouts, error mapping, usage reconciliation, region/fallback denial, and one bounded live smoke test when credentials/network/cost are authorized. Report exact installed versions and current documentation dates, not a static model table.
