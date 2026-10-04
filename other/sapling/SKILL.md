---
name: sapling
description: |
  Sapling integration via Apideck's HRIS unified API — same methods work across every connector in HRIS, switch by changing `serviceId`. Use when the user wants to read or sync employees, departments, payrolls, and time-off records in Sapling. Routes through Apideck with serviceId "sapling".
license: Apache-2.0
alwaysApply: false
metadata:
  author: apideck
  version: "1.0.0"
  serviceId: sapling
  unifiedApis: ["hris"]
  authType: apiKey
  tier: "2"
  verified: true
  status: beta
  difficulty: moderate
  partnershipRequired: false
  sandboxAvailable: false
---

# Sapling (via Apideck)

Access Sapling through Apideck's **HRIS** unified API — one of 58 HRIS connectors that share the same method surface. Code you write here ports to BambooHR, Workday, Deel and 54 other HRIS connectors by changing a single `serviceId` string. Apideck handles auth, pagination, rate limiting, and retries so you don't write per-tenant Sapling plumbing.

> **Beta connector.** Sapling is currently in beta on Apideck. Expect partial resource coverage and occasional mapping gaps. Always verify coverage (see below) and fall back to the Proxy API for unsupported operations.

## Quick facts

- **Apideck serviceId:** `sapling`
- **Unified API:** HRIS
- **Auth type:** apiKey
- **Status:** beta
- **Gotchas:** [page](https://developers.apideck.com/apis/hris/sapling/gotchas)
- **Sapling docs:** https://developer.saplinghr.com
- **Homepage:** https://www.saplinghr.com/

## At a glance

- **Implementation difficulty:** moderate — API Key Authentication - Each Consumer Generates Their Own Key in Sapling
- **Vendor partnership required:** no
- **Apideck-managed credentials:** not available — Each consumer uses their own Sapling API key.
- **Account type required:** Sapling account (Kallidus suite); API access is restricted, so confirm with Kallidus that it is enabled for the tenant.
- **Consumer access level:** A Sapling admin who can generate API keys.
- **Sandbox:** not available — Test on an existing Sapling customer's tenant; no self-service sandbox is documented.
- **Rate limits:** Kallidus advises at most 100 requests per minute per API key.
- **Authentication:** Sent in the Authorization header.
- **Webhooks:** Virtual webhooks - employee created, updated and terminated events.

**Important to know:**

- The connector reaches US-hosted Sapling tenants on saplingapp.io. UK-hosted tenants (kallidus-suite.com) are not covered by the subdomain setting, so check where a customer's tenant is hosted before you commit.

> Facts synced from Apideck's connector metadata API — `GET /connector/connectors/sapling` (`overview` field) is the live, authoritative version.

## When to use this skill

Activate this skill when the user explicitly wants to work with **Sapling** — for example, "sync employees in Sapling" or "list time-off requests in Sapling". This skill teaches the agent:

1. Which Apideck unified API covers Sapling (HRIS)
2. The correct `serviceId` to pass on every call (`sapling`)
3. Sapling-specific auth and coverage caveats

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

// List employees in Sapling
const { data } = await apideck.hris.employees.list({
  serviceId: "sapling",
});
```

## Portable across 58 HRIS connectors

The Apideck **HRIS** unified API exposes the same methods for every connector in its catalog. Switching from Sapling to another HRIS connector is a one-string change — no rewrite, no new SDK.

```typescript
// Today — Sapling
await apideck.hris.employees.list({ serviceId: "sapling" });

// Tomorrow — same code, different connector
await apideck.hris.employees.list({ serviceId: "bamboohr" });
await apideck.hris.employees.list({ serviceId: "workday" });
```

This is the compounding advantage of using Apideck over integrating Sapling directly: code against the unified HRIS API once, gain access to every connector in it. New connectors Apideck adds become available to your app without code changes.

## Authentication

- **Type:** API Key
- **Managed by:** Apideck Vault — the user pastes their Sapling API key into the Vault modal; Apideck stores it encrypted and injects it on every request.
- **Rotation:** if the user rotates their key, they re-enter it in Vault. No code changes needed.

See [`apideck-best-practices`](../../skills/apideck-best-practices/) for Vault setup, connection lifecycle, and handling re-auth flows.

## Verifying coverage

Not every HRIS operation is supported by every connector. Always verify before assuming a method works:

```bash
curl 'https://unify.apideck.com/connector/connectors/sapling' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}"
```

See [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) for patterns around `UnsupportedOperationError` and connector-specific fallbacks.

## Escape hatch: Proxy API

When an endpoint isn't covered by the HRIS unified API, use Apideck's Proxy to call Sapling directly — Apideck injects auth headers and handles token refresh. Set `x-apideck-downstream-url` to the target endpoint on Sapling's own API:

```bash
curl 'https://unify.apideck.com/proxy' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}" \
  -H "x-apideck-consumer-id: ${CONSUMER_ID}" \
  -H "x-apideck-service-id: sapling" \
  -H "x-apideck-downstream-url: <target endpoint on Sapling>" \
  -H "x-apideck-downstream-method: GET"
```

See [Sapling's API docs](https://developer.saplinghr.com) for available endpoints.

## Sibling connectors

Other **HRIS** connectors that share this unified API surface (same method signatures, just change `serviceId`):

[`bamboohr`](../bamboohr/), [`workday`](../workday/), [`deel`](../deel/) *(beta)*, [`hibob`](../hibob/), [`personio`](../personio/), [`adp-ihcm`](../adp-ihcm/) *(beta)*, [`adp-workforce-now`](../adp-workforce-now/) *(beta)*, [`paychex`](../paychex/) *(beta)*, and 49 more.

## See also

- [HRIS OpenAPI spec](https://specs.apideck.com/hris.yml) · [API Explorer](https://developers.apideck.com/api-explorer?id=hris)
- [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) — programmatic coverage checks
- [`apideck-best-practices`](../../skills/apideck-best-practices/) — architecture, Vault, pagination, error handling
- [`apideck-node`](../../skills/apideck-node/) — TypeScript / Node SDK patterns
- [Sapling official docs](https://developer.saplinghr.com)
