---
name: cloudflare
description: Design, implement, or troubleshoot applications on current Cloudflare products using project configuration and official documentation. Use for Workers.
license: MIT
---

# Cloudflare Engineering

## Discover

Inspect repository instructions, `wrangler` configuration, package/lock versions, bindings, environments, routes/domains, migrations, secrets references, compatibility date/flags, tests, and deployment history. Verify behavior from current official Cloudflare docs and installed CLI help; product APIs and compatibility rules change.

## Route by requirement

- stateless request logic: Workers;
- static/full-stack deployment: Pages or the project's current Workers framework path;
- relational data: D1 with migrations and transaction limits;
- objects/blobs: R2;
- cache/config-like key-value: KV with consistency tradeoffs;
- strongly coordinated per-entity state: Durable Objects;
- asynchronous delivery: Queues;
- durable multi-step jobs: Workflows when currently supported;
- AI inference/gateway: only the configured authorized provider/model and current product support.

Do not choose a product by convenience alone. Compare consistency, region, limits, pricing, latency, retention, and operational ownership.

## Safety

Keep secrets in documented secret stores, not config/source/logs. Validate untrusted requests, enforce auth at the boundary, limit CPU/memory/body/concurrency, use idempotency for retried effects, and avoid leaking platform metadata. AI Gateway fallback/routing must not silently change provider, model, region, privacy, or cost.

Do not run global installs, `@latest`, DNS/domain changes, migrations, secret writes, deployments, or production data operations without authorization.

## Verify

Run config parsing, typecheck/lint/tests, local emulator/dev checks, binding/migration validation, failure/limit tests, and a bounded staging smoke test. Report installed versions, compatibility date, environment, bindings, commands, observed platform limits, deployment steps, rollback, and any unverified production behavior.
