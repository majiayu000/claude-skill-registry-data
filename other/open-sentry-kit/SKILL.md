---
name: open-sentry-kit
description: Configure and operate authorized Sentry organizations, projects, SDKs, releases, source maps, alerts, issues, performance, tracing, and deployment health. Use for observability setup, incident diagnosis, release verification, or noise reduction.
---

# Open Sentry Kit

Operate through the connected Sentry API and project SDK. Separate public DSNs from server-side auth tokens.

## Workflow

1. Confirm organization, project, platform, environment, release naming, and data requirements.
2. Inspect SDK configuration, integrations, releases, alerts, ownership, quotas, and issues.
3. Add only missing SDK/CI configuration; set environment, release, tracing, profiling, and scrubbing.
4. Upload source maps or debug artifacts through CI with scoped server credentials.
5. Create release/deploy markers and send a controlled test event.
6. Verify ingestion, symbolication, release mapping, traces, alerts, and commit/deployment links.

## Guardrails

Never transmit passwords, tokens, cookies, private keys, or unnecessary personal data. Do not resolve/delete issues or change quotas, sampling, alerts, membership, or security without approval. Avoid duplicate projects, SDK initialization, releases, and alerts.
