---
name: cloudflare-deploy
description: Prepare, preview, deploy, and verify a Cloudflare application with environment-aware configuration, migrations, secrets, domains, observability, and.
license: MIT
---

# Deploy to Cloudflare

Deployment is an external mutation. A request to prepare configuration does not by itself authorize a production deploy.

## Preflight

1. Identify project type, installed package manager/Wrangler version, account/project, target environment, branch, config files, bindings, compatibility date/flags, build command/output, routes/domains, secrets names, and data migrations.
2. Preserve dirty work and verify build/test/lint/typecheck locally.
3. Compare current config and generated deployment plan with current official docs and installed CLI help.
4. Confirm who owns DNS, secrets, databases/storage, billing, and rollback.

Do not install/upgrade Wrangler automatically. Never print or copy secret values. Do not create/delete resources, apply migrations, change routes/DNS, or deploy to production outside explicit scope.

## Plan and execute

Use separate preview/staging and production configuration. Make data migrations forward/backward compatible, back up critical data, and define a rollback that accounts for schema changes. For AI bindings/gateway, use the project's validated configuration; model/provider/fallback changes require separate review of capability, privacy, region, and cost.

Run the exact deployment command only after preflight passes. Capture version/deployment ID and output without secrets.

## Verify

Test health, representative routes, auth, bindings, cache, logs/metrics, errors, latency, headers, redirects, and version identity from the deployed environment. Verify domain/DNS only when in scope. Roll back when predefined checks fail and report any irreversible migration.

Return target, commands, build/tests, resources/migrations, deployment ID/URL, smoke evidence, observability, cost/limits, and rollback status.
