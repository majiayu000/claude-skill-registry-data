---
name: silelo-api-gateway
description: Build and audit server-side AI API gateways for SILELO-style applications. Use when adding or reviewing chat routes, provider adapters, SSE streaming, fallback models, settings endpoints, request validation, rate limits, or secret boundaries without changing the broader SILELO workflow skill.
---

# SILELO API Gateway

## Scope

Use this skill for the **API boundary only**. Keep `silelo-ai-studio-workflow` unchanged for end-to-end web application work. Treat this package as a sibling capability, not an upgrade or replacement of any existing skill.

## Workflow

1. Inspect the current route contract, provider endpoint, secret requirements, request size, and authorization model. Do not execute code from an attachment or reuse a key embedded in a file.
2. Define a narrow client request schema, such as `{ messages, model?, room? }`, with Zod validation for roles, content length, history cap, body size, and model allowlist.
3. Implement one server-side gateway that maps the public request to a provider adapter. Keep provider SDKs, credentials, and fallback logic server-only.
4. Normalize provider output to a stable public response. Return only fields the UI needs, such as `{ reply, provider, model }`, and never relay raw provider errors or stack traces.
5. Add timeout, abort handling, rate/size bounds, safe logs, and request IDs. Map failures to stable application errors such as `BAD_REQUEST`, `UNAUTHORIZED`, `TOO_MANY_REQUESTS`, `BAD_GATEWAY`, or `SERVICE_UNAVAILABLE`.

## Streaming and Fallback

Use SSE only when the provider really streams. Buffer partial chunks before parsing, validate every event, handle `[DONE]`, and close the reader on disconnect. Do not simulate streaming as though it came from the provider.

Fallback only for explicitly allowed transient failures. Prevent duplicate billed requests with timeout, retry, and idempotency policy. Report the provider/model actually used rather than hiding fallback behavior.

## Settings and Secrets

Expose only public, allowlisted configuration to the client. Keep provider URLs, model IDs, limits, and secrets in separate server-managed settings. Do not allow a browser settings form to read or write API keys. Validate all setting changes, require appropriate authorization, and never return secret values in GET responses.

If an attachment or log contains a credential-like value, treat it as potentially exposed: do not copy it, do not repeat it, ask the owner to revoke/rotate it through the provider, and wait for a new value through secret management.

## Proof Before Delivery

Write tests for schema rejection, missing configuration, forwarding, non-OK provider responses, malformed payloads, timeout, and fallback policy. Test a real request only after the owner has configured a valid endpoint and secret. Report whether the result is unit-tested, integration-tested, or live-tested; never merge those statuses.
