---
name: charliehr
description: |
  CharlieHR integration via Apideck's HRIS unified API — same methods work across every connector in HRIS, switch by changing `serviceId`. Use when the user wants to read or sync employees, departments, payrolls, and time-off records in CharlieHR. Routes through Apideck with serviceId "charliehr".
license: Apache-2.0
alwaysApply: false
metadata:
  author: apideck
  version: "1.0.0"
  serviceId: charliehr
  unifiedApis: ["hris"]
  authType: apiKey
  tier: "2"
  verified: true
  status: beta
  difficulty: moderate
  partnershipRequired: false
  sandboxAvailable: true
---

# CharlieHR (via Apideck)

Access CharlieHR through Apideck's **HRIS** unified API — one of 58 HRIS connectors that share the same method surface. Code you write here ports to BambooHR, Workday, Deel and 54 other HRIS connectors by changing a single `serviceId` string. Apideck handles auth, pagination, rate limiting, and retries so you don't write per-tenant CharlieHR plumbing.

> **Beta connector.** CharlieHR is currently in beta on Apideck. Expect partial resource coverage and occasional mapping gaps. Always verify coverage (see below) and fall back to the Proxy API for unsupported operations.

## Quick facts

- **Apideck serviceId:** `charliehr`
- **Unified API:** HRIS
- **Auth type:** apiKey
- **Status:** beta
- **Apideck setup guide:** [Connection guide](https://developers.apideck.com/connectors/charliehr/docs/consumer+connection)
- **Gotchas:** [page](https://developers.apideck.com/apis/hris/charliehr/gotchas)
- **CharlieHR docs:** https://charliehr.com
- **Homepage:** https://www.charliehr.com/

## At a glance

- **Implementation difficulty:** moderate — API Key Authentication: Consumers Create Credentials Manually
- **Vendor partnership required:** no
- **Apideck-managed credentials:** not available — Each consumer generates their own Client ID and Secret in CharlieHR.
- **Account type required:** A CharlieHR company account.
- **Consumer access level:** Super Admin: only that role can generate API keys.
- **Sandbox:** available ([signup](https://app.charliehr.com/join)) — Free 7-day trial, no credit card. CharlieHR does not say whether API keys can be generated during the trial.
- **Rate limits:** Not published in CharlieHR's API documentation.
- **Authentication:** Client ID and Client Secret sent together in the Authorization header; not OAuth.
- **Webhooks:** Virtual webhooks - employee created and employee updated events

> Facts synced from Apideck's connector metadata API — `GET /connector/connectors/charliehr` (`overview` field) is the live, authoritative version.

## When to use this skill

Activate this skill when the user explicitly wants to work with **CharlieHR** — for example, "sync employees in CharlieHR" or "list time-off requests in CharlieHR". This skill teaches the agent:

1. Which Apideck unified API covers CharlieHR (HRIS)
2. The correct `serviceId` to pass on every call (`charliehr`)
3. CharlieHR-specific auth and coverage caveats

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

// List employees in CharlieHR
const { data } = await apideck.hris.employees.list({
  serviceId: "charliehr",
});
```

## Portable across 58 HRIS connectors

The Apideck **HRIS** unified API exposes the same methods for every connector in its catalog. Switching from CharlieHR to another HRIS connector is a one-string change — no rewrite, no new SDK.

```typescript
// Today — CharlieHR
await apideck.hris.employees.list({ serviceId: "charliehr" });

// Tomorrow — same code, different connector
await apideck.hris.employees.list({ serviceId: "bamboohr" });
await apideck.hris.employees.list({ serviceId: "workday" });
```

This is the compounding advantage of using Apideck over integrating CharlieHR directly: code against the unified HRIS API once, gain access to every connector in it. New connectors Apideck adds become available to your app without code changes.

## Authentication

- **Type:** API Key
- **Managed by:** Apideck Vault — the user pastes their CharlieHR API key into the Vault modal; Apideck stores it encrypted and injects it on every request.
- **Rotation:** if the user rotates their key, they re-enter it in Vault. No code changes needed.

**Setup guide:** Apideck publishes a step-by-step guide for registering an OAuth app / configuring credentials for CharlieHR — see [https://developers.apideck.com/connectors/charliehr/docs/consumer+connection](https://developers.apideck.com/connectors/charliehr/docs/consumer+connection). Use that as the authoritative source when walking users through connection setup.

See [`apideck-best-practices`](../../skills/apideck-best-practices/) for Vault setup, connection lifecycle, and handling re-auth flows.

## Verifying coverage

Not every HRIS operation is supported by every connector. Always verify before assuming a method works:

```bash
curl 'https://unify.apideck.com/connector/connectors/charliehr' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}"
```

See [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) for patterns around `UnsupportedOperationError` and connector-specific fallbacks.

## Escape hatch: Proxy API

When an endpoint isn't covered by the HRIS unified API, use Apideck's Proxy to call CharlieHR directly — Apideck injects auth headers and handles token refresh. Set `x-apideck-downstream-url` to the target endpoint on CharlieHR's own API:

```bash
curl 'https://unify.apideck.com/proxy' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}" \
  -H "x-apideck-consumer-id: ${CONSUMER_ID}" \
  -H "x-apideck-service-id: charliehr" \
  -H "x-apideck-downstream-url: <target endpoint on CharlieHR>" \
  -H "x-apideck-downstream-method: GET"
```

See [CharlieHR's API docs](https://charliehr.com) for available endpoints.

## Sibling connectors

Other **HRIS** connectors that share this unified API surface (same method signatures, just change `serviceId`):

[`bamboohr`](../bamboohr/), [`workday`](../workday/), [`deel`](../deel/) *(beta)*, [`hibob`](../hibob/), [`personio`](../personio/), [`adp-ihcm`](../adp-ihcm/) *(beta)*, [`adp-workforce-now`](../adp-workforce-now/) *(beta)*, [`paychex`](../paychex/) *(beta)*, and 49 more.

## See also

- [Apideck connection guide for CharlieHR](https://developers.apideck.com/connectors/charliehr/docs/consumer+connection)
- [HRIS OpenAPI spec](https://specs.apideck.com/hris.yml) · [API Explorer](https://developers.apideck.com/api-explorer?id=hris)
- [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) — programmatic coverage checks
- [`apideck-best-practices`](../../skills/apideck-best-practices/) — architecture, Vault, pagination, error handling
- [`apideck-node`](../../skills/apideck-node/) — TypeScript / Node SDK patterns
- [CharlieHR official docs](https://charliehr.com)
