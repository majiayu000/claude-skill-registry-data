---
name: lucca-hr
description: |
  Lucca integration via Apideck's HRIS unified API — same methods work across every connector in HRIS, switch by changing `serviceId`. Use when the user wants to read or sync employees, departments, payrolls, and time-off records in Lucca. Routes through Apideck with serviceId "lucca-hr".
license: Apache-2.0
alwaysApply: false
metadata:
  author: apideck
  version: "1.0.0"
  serviceId: lucca-hr
  unifiedApis: ["hris"]
  authType: apiKey
  tier: "2"
  verified: true
  difficulty: moderate
  partnershipRequired: false
  sandboxAvailable: true
---

# Lucca (via Apideck)

Access Lucca through Apideck's **HRIS** unified API — one of 58 HRIS connectors that share the same method surface. Code you write here ports to BambooHR, Workday, Deel and 54 other HRIS connectors by changing a single `serviceId` string. Apideck handles auth, pagination, rate limiting, and retries so you don't write per-tenant Lucca plumbing.

## Quick facts

- **Apideck serviceId:** `lucca-hr`
- **Unified API:** HRIS
- **Auth type:** apiKey
- **Gotchas:** [page](https://developers.apideck.com/apis/hris/lucca-hr/gotchas)
- **Lucca docs:** https://developers.lucca.fr
- **Homepage:** https://www.lucca-hr.com/

## At a glance

- **Implementation difficulty:** moderate — API Key Authentication - Each Consumer Creates Their Own Key in Lucca
- **Vendor partnership required:** no — Nothing has to be registered with Lucca to use this connector.
- **Apideck-managed credentials:** not available — Each consumer creates their own Lucca API key.
- **Account type required:** A Lucca account on the consumer's own Lucca domain.
- **Consumer access level:** Access to the 'Authentification, SSO et API' administration interface, where Lucca API keys are managed.
- **Sandbox:** available — Ask Lucca for a Test environment (ilucca-test) on the customer account, one per customer. Snapshot-restorable sandboxes are a paid Lucca feature.
- **Rate limits:** 50 requests a minute for each Lucca domain, shared by every integration connected to that domain.
- **Authentication:** Sent in the Authorization header.
- **Webhooks:** Virtual webhooks - employee created, updated and terminated events.

**Important to know:**

- Use an API key created in the same Lucca environment as the subdomain you enter.

> Facts synced from Apideck's connector metadata API — `GET /connector/connectors/lucca-hr` (`overview` field) is the live, authoritative version.

## When to use this skill

Activate this skill when the user explicitly wants to work with **Lucca** — for example, "sync employees in Lucca" or "list time-off requests in Lucca". This skill teaches the agent:

1. Which Apideck unified API covers Lucca (HRIS)
2. The correct `serviceId` to pass on every call (`lucca-hr`)
3. Lucca-specific auth and coverage caveats

For the full method surface (parameters, pagination, filtering), use your language SDK skill:

- [`apideck-node`](../../skills/apideck-node/), [`apideck-python`](../../skills/apideck-python/), [`apideck-dotnet`](../../skills/apideck-dotnet/), [`apideck-java`](../../skills/apideck-java/), [`apideck-go`](../../skills/apideck-go/), [`apideck-php`](../../skills/apideck-php/), or [`apideck-rest`](../../skills/apideck-rest/)

For the raw OpenAPI spec:

- **HRIS:** [https://specs.apideck.com/hris.yml](https://specs.apideck.com/hris.yml) · [API Explorer](https://developers.apideck.com/api-explorer?id=hris)

## Minimal example (TypeScript)

```typescript
import { Apideck } from "@apideck/unify";

const apideck = new Apideck({
  apiKey: process.env.APIDECK_API_KEY,
  appId: process.env.APIDECK_APP_ID,
  consumerId: "your-consumer-id",
});

// List employees in Lucca
const { data } = await apideck.hris.employees.list({
  serviceId: "lucca-hr",
});
```

## Portable across 58 HRIS connectors

The Apideck **HRIS** unified API exposes the same methods for every connector in its catalog. Switching from Lucca to another HRIS connector is a one-string change — no rewrite, no new SDK.

```typescript
// Today — Lucca
await apideck.hris.employees.list({ serviceId: "lucca-hr" });

// Tomorrow — same code, different connector
await apideck.hris.employees.list({ serviceId: "bamboohr" });
await apideck.hris.employees.list({ serviceId: "workday" });
```

This is the compounding advantage of using Apideck over integrating Lucca directly: code against the unified HRIS API once, gain access to every connector in it. New connectors Apideck adds become available to your app without code changes.

## Authentication

- **Type:** API Key
- **Managed by:** Apideck Vault — the user pastes their Lucca API key into the Vault modal; Apideck stores it encrypted and injects it on every request.
- **Rotation:** if the user rotates their key, they re-enter it in Vault. No code changes needed.

See [`apideck-best-practices`](../../skills/apideck-best-practices/) for Vault setup, connection lifecycle, and handling re-auth flows.

## Verifying coverage

Not every HRIS operation is supported by every connector. Always verify before assuming a method works:

```bash
curl 'https://unify.apideck.com/connector/connectors/lucca-hr' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}"
```

See [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) for patterns around `UnsupportedOperationError` and connector-specific fallbacks.

## Escape hatch: Proxy API

When an endpoint isn't covered by the HRIS unified API, use Apideck's Proxy to call Lucca directly — Apideck injects auth headers and handles token refresh. Set `x-apideck-downstream-url` to the target endpoint on Lucca's own API:

```bash
curl 'https://unify.apideck.com/proxy' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}" \
  -H "x-apideck-consumer-id: ${CONSUMER_ID}" \
  -H "x-apideck-service-id: lucca-hr" \
  -H "x-apideck-downstream-url: <target endpoint on Lucca>" \
  -H "x-apideck-downstream-method: GET"
```

See [Lucca's API docs](https://developers.lucca.fr) for available endpoints.

## Sibling connectors

Other **HRIS** connectors that share this unified API surface (same method signatures, just change `serviceId`):

[`bamboohr`](../bamboohr/), [`workday`](../workday/), [`deel`](../deel/) *(beta)*, [`hibob`](../hibob/), [`personio`](../personio/), [`adp-ihcm`](../adp-ihcm/) *(beta)*, [`adp-workforce-now`](../adp-workforce-now/) *(beta)*, [`paychex`](../paychex/) *(beta)*, and 49 more.

## See also

- [HRIS OpenAPI spec](https://specs.apideck.com/hris.yml) · [API Explorer](https://developers.apideck.com/api-explorer?id=hris)
- [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) — programmatic coverage checks
- [`apideck-best-practices`](../../skills/apideck-best-practices/) — architecture, Vault, pagination, error handling
- [`apideck-node`](../../skills/apideck-node/) — TypeScript / Node SDK patterns
- [Lucca official docs](https://developers.lucca.fr)
