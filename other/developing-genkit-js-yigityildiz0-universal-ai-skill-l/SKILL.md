---
name: developing-genkit-js
description: Build and troubleshoot Genkit applications in JavaScript or TypeScript with installed-version-first APIs, provider-neutral model configuration, flows.
license: MIT
---

# Genkit JavaScript and TypeScript

Genkit APIs and plugins evolve quickly. Use the project lockfile, installed package source/types, tests, and current official Genkit documentation as the source of truth.

## Guardrails

- Inspect `package.json`, lockfile, runtime, Genkit/CLI/plugin versions, imports, configured provider/model, flows, tools, and deployment target.
- Do not run global installs, `@latest`, network installers, or broad upgrades implicitly.
- Preserve the existing provider. If none exists, compare options by deployment, privacy, region, capability, latency, and cost; do not select one by default.
- Keep the exact model ID in validated configuration and verify that the installed plugin supports required tools, structured output, streaming, multimodal input, and embeddings.
- Keep secrets out of client bundles, source, logs, examples, and prompts.

## Implementation

1. Register only needed plugins and use symbols that exist in the installed version.
2. Define typed input/output schemas and validate application invariants after generation.
3. Keep prompts and untrusted user/retrieved data separated.
4. Give tools strict object schemas, least privilege, authorization, timeouts, idempotency, and approval for costly/destructive/external effects.
5. Bound tool rounds, retries, concurrency, tokens, time, and spend.
6. Keep HTTP/auth concerns outside model decisions and return safe errors.
7. Add telemetry that records flow/tool status, latency, usage, and request IDs without leaking sensitive payloads.

Conceptual configuration:

```ts
const modelId = process.env.GENKIT_MODEL_ID;
if (!modelId) throw new Error('GENKIT_MODEL_ID is required');
// Initialize the already selected provider plugin and pass modelId using
// the API supported by the installed Genkit version.
```

## Verify

Run typecheck/lint/tests, input/output schema tests, mocked provider/tool tests, cancellation/timeouts/retries, authorization and injection tests, and a Dev UI check when installed. A live provider smoke test requires authorized credentials/network/cost. Report installed versions, configured provider/model source, exact commands, and skipped checks.
