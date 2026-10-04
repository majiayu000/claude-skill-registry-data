---
name: alexishr
description: |
  Simployer One integration via Apideck's HRIS unified API — same methods work across every connector in HRIS, switch by changing `serviceId`. Use when the user wants to read or sync employees, departments, payrolls, and time-off records in Simployer One. Routes through Apideck with serviceId "alexishr".
license: Apache-2.0
alwaysApply: false
metadata:
  author: apideck
  version: "1.0.0"
  serviceId: alexishr
  unifiedApis: ["hris"]
  authType: apiKey
  tier: "2"
  verified: true
  status: beta
  difficulty: moderate
  partnershipRequired: false
  sandboxAvailable: false
---

# Simployer One (via Apideck)

Access Simployer One through Apideck's **HRIS** unified API — one of 58 HRIS connectors that share the same method surface. Code you write here ports to BambooHR, Workday, Deel and 54 other HRIS connectors by changing a single `serviceId` string. Apideck handles auth, pagination, rate limiting, and retries so you don't write per-tenant Simployer One plumbing.

> **Beta connector.** Simployer One is currently in beta on Apideck. Expect partial resource coverage and occasional mapping gaps. Always verify coverage (see below) and fall back to the Proxy API for unsupported operations.

## Quick facts

- **Apideck serviceId:** `alexishr`
- **Unified API:** HRIS
- **Auth type:** apiKey
- **Status:** beta
- **Apideck setup guide:** [Connection guide](https://developers.apideck.com/connectors/alexishr/docs/consumer+connection)
- **Gotchas:** [page](https://developers.apideck.com/apis/hris/alexishr/gotchas)
- **Simployer One docs:** https://www.simployer.com
- **Homepage:** https://www.simployer.com/

## At a glance

- **Implementation difficulty:** moderate — API Token Authentication: Each Consumer's Owner Generates a Token
- **Vendor partnership required:** no
- **Apideck-managed credentials:** not available — Each consumer generates their own access token in Simployer One.
- **Account type required:** A Simployer One company account.
- **Consumer access level:** Owner permission: only Owners can create access tokens.
- **Sandbox:** not available — Ask Simployer for a test account; there is no free trial.
- **Authentication:** Access token, sent as a bearer token.
- **Webhooks:** Virtual webhooks - employee created, updated and terminated events

**Important to know:**

- The token is tied to the Owner who created it. If that person's permissions change or they are removed from Simployer One, the token becomes invalid and the consumer has to generate a new one and reconnect.
- Simployer describes its public API as in preview, so small backward-incompatible changes can be introduced; the vendor says they will be documented and communicated.

> Facts synced from Apideck's connector metadata API — `GET /connector/connectors/alexishr` (`overview` field) is the live, authoritative version.

## When to use this skill

Activate this skill when the user explicitly wants to work with **Simployer One** — for example, "sync employees in Simployer One" or "list time-off requests in Simployer One". This skill teaches the agent:

1. Which Apideck unified API covers Simployer One (HRIS)
2. The correct `serviceId` to pass on every call (`alexishr`)
3. Simployer One-specific auth and coverage caveats

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

// List employees in Simployer One
const { data } = await apideck.hris.employees.list({
  serviceId: "alexishr",
});
```

## Portable across 58 HRIS connectors

The Apideck **HRIS** unified API exposes the same methods for every connector in its catalog. Switching from Simployer One to another HRIS connector is a one-string change — no rewrite, no new SDK.

```typescript
// Today — Simployer One
await apideck.hris.employees.list({ serviceId: "alexishr" });

// Tomorrow — same code, different connector
await apideck.hris.employees.list({ serviceId: "bamboohr" });
await apideck.hris.employees.list({ serviceId: "workday" });
```

This is the compounding advantage of using Apideck over integrating Simployer One directly: code against the unified HRIS API once, gain access to every connector in it. New connectors Apideck adds become available to your app without code changes.

## Authentication

- **Type:** API Key
- **Managed by:** Apideck Vault — the user pastes their Simployer One API key into the Vault modal; Apideck stores it encrypted and injects it on every request.
- **Rotation:** if the user rotates their key, they re-enter it in Vault. No code changes needed.

**Setup guide:** Apideck publishes a step-by-step guide for registering an OAuth app / configuring credentials for Simployer One — see [https://developers.apideck.com/connectors/alexishr/docs/consumer+connection](https://developers.apideck.com/connectors/alexishr/docs/consumer+connection). Use that as the authoritative source when walking users through connection setup.

See [`apideck-best-practices`](../../skills/apideck-best-practices/) for Vault setup, connection lifecycle, and handling re-auth flows.

## Verifying coverage

Not every HRIS operation is supported by every connector. Always verify before assuming a method works:

```bash
curl 'https://unify.apideck.com/connector/connectors/alexishr' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}"
```

See [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) for patterns around `UnsupportedOperationError` and connector-specific fallbacks.

## Escape hatch: Proxy API

When an endpoint isn't covered by the HRIS unified API, use Apideck's Proxy to call Simployer One directly — Apideck injects auth headers and handles token refresh. Set `x-apideck-downstream-url` to the target endpoint on Simployer One's own API:

```bash
curl 'https://unify.apideck.com/proxy' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}" \
  -H "x-apideck-consumer-id: ${CONSUMER_ID}" \
  -H "x-apideck-service-id: alexishr" \
  -H "x-apideck-downstream-url: <target endpoint on Simployer One>" \
  -H "x-apideck-downstream-method: GET"
```

See [Simployer One's API docs](https://www.simployer.com) for available endpoints.

## Sibling connectors

Other **HRIS** connectors that share this unified API surface (same method signatures, just change `serviceId`):

[`bamboohr`](../bamboohr/), [`workday`](../workday/), [`deel`](../deel/) *(beta)*, [`hibob`](../hibob/), [`personio`](../personio/), [`adp-ihcm`](../adp-ihcm/) *(beta)*, [`adp-workforce-now`](../adp-workforce-now/) *(beta)*, [`paychex`](../paychex/) *(beta)*, and 49 more.

## See also

- [Apideck connection guide for Simployer One](https://developers.apideck.com/connectors/alexishr/docs/consumer+connection)
- [HRIS OpenAPI spec](https://specs.apideck.com/hris.yml) · [API Explorer](https://developers.apideck.com/api-explorer?id=hris)
- [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) — programmatic coverage checks
- [`apideck-best-practices`](../../skills/apideck-best-practices/) — architecture, Vault, pagination, error handling
- [`apideck-node`](../../skills/apideck-node/) — TypeScript / Node SDK patterns
- [Simployer One official docs](https://www.simployer.com)
