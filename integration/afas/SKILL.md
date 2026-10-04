---
name: afas
description: |
  AFAS Software integration via Apideck's HRIS unified API — same methods work across every connector in HRIS, switch by changing `serviceId`. Use when the user wants to read or sync employees, departments, payrolls, and time-off records in AFAS Software. Routes through Apideck with serviceId "afas".
license: Apache-2.0
alwaysApply: false
metadata:
  author: apideck
  version: "1.0.0"
  serviceId: afas
  unifiedApis: ["hris"]
  authType: apiKey
  tier: "2"
  verified: true
  status: beta
  difficulty: highly_complex
  partnershipRequired: false
  sandboxAvailable: false
---

# AFAS Software (via Apideck)

Access AFAS Software through Apideck's **HRIS** unified API — one of 58 HRIS connectors that share the same method surface. Code you write here ports to BambooHR, Workday, Deel and 54 other HRIS connectors by changing a single `serviceId` string. Apideck handles auth, pagination, rate limiting, and retries so you don't write per-tenant AFAS Software plumbing.

> **Beta connector.** AFAS Software is currently in beta on Apideck. Expect partial resource coverage and occasional mapping gaps. Always verify coverage (see below) and fall back to the Proxy API for unsupported operations.

## Quick facts

- **Apideck serviceId:** `afas`
- **Unified API:** HRIS
- **Auth type:** apiKey
- **Status:** beta
- **Apideck setup guide:** [Connection guide](https://developers.apideck.com/connectors/afas/docs/consumer+connection)
- **Gotchas:** [page](https://developers.apideck.com/apis/hris/afas/gotchas)
- **AFAS Software docs:** https://www.afas.nl
- **Homepage:** https://www.afas.nl/

## At a glance

- **Implementation difficulty:** highly complex — Non-OAuth Token Auth + Multi-Step Per-Consumer App Connector Setup
- **Vendor partnership required:** no ([AFAS Partner Program](https://partner.afas.nl/koppeling-registreren)) — Certifying your integration through the optional Partner Program adds 1-2 AFAS test environments on the Accept platform.
- **Apideck-managed credentials:** not available — Every consumer connects with their own AFAS environment name and App Connector token.
- **Account type required:** A licensed AFAS Profit or AFAS Online environment with the modules you need (HRM for HRIS; Financieel, Facturering and Inkoop for accounting).
- **Consumer access level:** AFAS administrator, to create the App Connector and issue the token.
- **Sandbox:** not available ([signup](https://connect.afas.nl/)) — Every AFAS environment is licensed; customers clone a Test copy. AFAS Connect (connect.afas.nl) freely builds and tests connector calls.
- **Costs:** No separate API or connector fee — REST access is included in an AFAS Profit or AFAS Online license. No free trial for non-customers.
- **Rate limits:** No published per-minute or per-day limit — AFAS applies a fair-use policy.
- **Authentication:** An AFAS App Connector token sent in the Authorization header, prefixed with AfasToken. Not OAuth.
- **Webhooks:** Virtual webhooks — polling-based created/updated events for 14 HRIS and accounting resource families (employees, customers, invoices, bills, and 10 more).

**Important to know:**

- One AFAS environment and token serves two unified APIs: HRIS (live) and Accounting (beta). Employees and departments are HRIS-only — those operations are disabled on the Accounting API — so which resources you get depends on the API you build against.
- A connection can authorize and still return no data: each consumer's AFAS administrator must first publish the named GetConnectors (and UpdateConnectors for writes) to the App Connector. Credit notes, payments and aged debtors/creditors need one the tenant authors itself.
- AFAS is retiring classic token authentication: tokens receive automatic end-dates on 15 February 2027 and stop working on 31 August 2027, when OAuth 2.1 replaces them. An administrator can also time-limit or revoke a token at any point, which silently breaks the connection.

> Facts synced from Apideck's connector metadata API — `GET /connector/connectors/afas` (`overview` field) is the live, authoritative version.

## When to use this skill

Activate this skill when the user explicitly wants to work with **AFAS Software** — for example, "sync employees in AFAS Software" or "list time-off requests in AFAS Software". This skill teaches the agent:

1. Which Apideck unified API covers AFAS Software (HRIS)
2. The correct `serviceId` to pass on every call (`afas`)
3. AFAS Software-specific auth and coverage caveats

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

// List employees in AFAS Software
const { data } = await apideck.hris.employees.list({
  serviceId: "afas",
});
```

## Portable across 58 HRIS connectors

The Apideck **HRIS** unified API exposes the same methods for every connector in its catalog. Switching from AFAS Software to another HRIS connector is a one-string change — no rewrite, no new SDK.

```typescript
// Today — AFAS Software
await apideck.hris.employees.list({ serviceId: "afas" });

// Tomorrow — same code, different connector
await apideck.hris.employees.list({ serviceId: "bamboohr" });
await apideck.hris.employees.list({ serviceId: "workday" });
```

This is the compounding advantage of using Apideck over integrating AFAS Software directly: code against the unified HRIS API once, gain access to every connector in it. New connectors Apideck adds become available to your app without code changes.

## Authentication

- **Type:** API Key
- **Managed by:** Apideck Vault — the user pastes their AFAS Software API key into the Vault modal; Apideck stores it encrypted and injects it on every request.
- **Rotation:** if the user rotates their key, they re-enter it in Vault. No code changes needed.

**Setup guide:** Apideck publishes a step-by-step guide for registering an OAuth app / configuring credentials for AFAS Software — see [https://developers.apideck.com/connectors/afas/docs/consumer+connection](https://developers.apideck.com/connectors/afas/docs/consumer+connection). Use that as the authoritative source when walking users through connection setup.

See [`apideck-best-practices`](../../skills/apideck-best-practices/) for Vault setup, connection lifecycle, and handling re-auth flows.

## Verifying coverage

Not every HRIS operation is supported by every connector. Always verify before assuming a method works:

```bash
curl 'https://unify.apideck.com/connector/connectors/afas' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}"
```

See [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) for patterns around `UnsupportedOperationError` and connector-specific fallbacks.

## Escape hatch: Proxy API

When an endpoint isn't covered by the HRIS unified API, use Apideck's Proxy to call AFAS Software directly — Apideck injects auth headers and handles token refresh. Set `x-apideck-downstream-url` to the target endpoint on AFAS Software's own API:

```bash
curl 'https://unify.apideck.com/proxy' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}" \
  -H "x-apideck-consumer-id: ${CONSUMER_ID}" \
  -H "x-apideck-service-id: afas" \
  -H "x-apideck-downstream-url: <target endpoint on AFAS Software>" \
  -H "x-apideck-downstream-method: GET"
```

See [AFAS Software's API docs](https://www.afas.nl) for available endpoints.

## Sibling connectors

Other **HRIS** connectors that share this unified API surface (same method signatures, just change `serviceId`):

[`bamboohr`](../bamboohr/), [`workday`](../workday/), [`deel`](../deel/) *(beta)*, [`hibob`](../hibob/), [`personio`](../personio/), [`adp-ihcm`](../adp-ihcm/) *(beta)*, [`adp-workforce-now`](../adp-workforce-now/) *(beta)*, [`paychex`](../paychex/) *(beta)*, and 49 more.

## See also

- [Apideck connection guide for AFAS Software](https://developers.apideck.com/connectors/afas/docs/consumer+connection)
- [HRIS OpenAPI spec](https://specs.apideck.com/hris.yml) · [API Explorer](https://developers.apideck.com/api-explorer?id=hris)
- [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) — programmatic coverage checks
- [`apideck-best-practices`](../../skills/apideck-best-practices/) — architecture, Vault, pagination, error handling
- [`apideck-node`](../../skills/apideck-node/) — TypeScript / Node SDK patterns
- [AFAS Software official docs](https://www.afas.nl)
