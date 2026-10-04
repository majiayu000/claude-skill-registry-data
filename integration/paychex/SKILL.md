---
name: paychex
description: |
  Paychex integration via Apideck's HRIS unified API — same methods work across every connector in HRIS, switch by changing `serviceId`. Use when the user wants to read or sync employees, departments, payrolls, and time-off records in Paychex. Routes through Apideck with serviceId "paychex".
license: Apache-2.0
alwaysApply: false
metadata:
  author: apideck
  version: "1.0.0"
  serviceId: paychex
  unifiedApis: ["hris"]
  authType: oauth2
  tier: "1c"
  verified: true
  status: beta
  difficulty: moderate
  partnershipRequired: false
  sandboxAvailable: true
---

# Paychex (via Apideck)

Access Paychex through Apideck's **HRIS** unified API — one of 58 HRIS connectors that share the same method surface. Code you write here ports to BambooHR, Workday, Deel and 54 other HRIS connectors by changing a single `serviceId` string. Apideck handles auth, pagination, rate limiting, and retries so you don't write per-tenant Paychex plumbing.

> **Beta connector.** Paychex is currently in beta on Apideck. Expect partial resource coverage and occasional mapping gaps. Always verify coverage (see below) and fall back to the Proxy API for unsupported operations.

## Quick facts

- **Apideck serviceId:** `paychex`
- **Unified API:** HRIS
- **Auth type:** oauth2
- **Status:** beta
- **Apideck setup guide:** [Connection guide](https://developers.apideck.com/connectors/paychex/docs/consumer+connection)
- **Gotchas:** [page](https://developers.apideck.com/apis/hris/paychex/gotchas)
- **Paychex docs:** https://developer.paychex.com
- **Homepage:** https://www.paychex.com/

## At a glance

- **Implementation difficulty:** moderate — Consumer Creates the App Credentials by Hand in Paychex Flex
- **Vendor partnership required:** no ([Paychex Developer Partner programme](https://developer.paychex.com/partner)) — Joining gives a Paychex-provided sandbox and a production key and secret.
- **Apideck-managed credentials:** not available — Each Paychex client connects with its own app credentials.
- **Account type required:** A Paychex Flex client company.
- **Consumer access level:** Super Admin or Security Admin in Paychex Flex (permission to manage connected applications).
- **Sandbox:** available ([signup](https://developer.paychex.com/partner)) — Request it through the Developer Partner programme; Paychex provides it once approved.
- **Authentication:** Client ID and secret pasted in Vault; no OAuth sign-in.
- **Webhooks:** Virtual webhooks - employee created and updated events

**Important to know:**

- After connecting, the consumer must grant their company access to the credentials in Paychex. Until then the company list stays empty and the Company field cannot be selected.

> Facts synced from Apideck's connector metadata API — `GET /connector/connectors/paychex` (`overview` field) is the live, authoritative version.

## When to use this skill

Activate this skill when the user explicitly wants to work with **Paychex** — for example, "sync employees in Paychex" or "list time-off requests in Paychex". This skill teaches the agent:

1. Which Apideck unified API covers Paychex (HRIS)
2. The correct `serviceId` to pass on every call (`paychex`)
3. Paychex-specific auth and coverage caveats

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

// List employees in Paychex
const { data } = await apideck.hris.employees.list({
  serviceId: "paychex",
});
```

## Portable across 58 HRIS connectors

The Apideck **HRIS** unified API exposes the same methods for every connector in its catalog. Switching from Paychex to another HRIS connector is a one-string change — no rewrite, no new SDK.

```typescript
// Today — Paychex
await apideck.hris.employees.list({ serviceId: "paychex" });

// Tomorrow — same code, different connector
await apideck.hris.employees.list({ serviceId: "bamboohr" });
await apideck.hris.employees.list({ serviceId: "workday" });
```

This is the compounding advantage of using Apideck over integrating Paychex directly: code against the unified HRIS API once, gain access to every connector in it. New connectors Apideck adds become available to your app without code changes.

## Authentication

- **Type:** OAuth 2.0
- **Managed by:** Apideck Vault — Apideck handles the full OAuth dance (authorization code flow, token exchange, refresh). Never ask the user for API keys or tokens directly.
- **User setup:** Users authorize via the Vault modal. Connection state progresses `available → added → authorized → callable`.
- **Token refresh:** automatic. Expired tokens are refreshed transparently on the next API call.

**Setup guide:** Apideck publishes a step-by-step guide for registering an OAuth app / configuring credentials for Paychex — see [https://developers.apideck.com/connectors/paychex/docs/consumer+connection](https://developers.apideck.com/connectors/paychex/docs/consumer+connection). Use that as the authoritative source when walking users through connection setup.

See [`apideck-best-practices`](../../skills/apideck-best-practices/) for Vault setup, connection lifecycle, and handling re-auth flows.

## Verifying coverage

Not every HRIS operation is supported by every connector. Always verify before assuming a method works:

```bash
curl 'https://unify.apideck.com/connector/connectors/paychex' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}"
```

See [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) for patterns around `UnsupportedOperationError` and connector-specific fallbacks.

## Escape hatch: Proxy API

When an endpoint isn't covered by the HRIS unified API, use Apideck's Proxy to call Paychex directly — Apideck injects auth headers and handles token refresh. Set `x-apideck-downstream-url` to the target endpoint on Paychex's own API:

```bash
curl 'https://unify.apideck.com/proxy' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}" \
  -H "x-apideck-consumer-id: ${CONSUMER_ID}" \
  -H "x-apideck-service-id: paychex" \
  -H "x-apideck-downstream-url: <target endpoint on Paychex>" \
  -H "x-apideck-downstream-method: GET"
```

See [Paychex's API docs](https://developer.paychex.com) for available endpoints.

## Sibling connectors

Other **HRIS** connectors that share this unified API surface (same method signatures, just change `serviceId`):

[`bamboohr`](../bamboohr/), [`workday`](../workday/), [`deel`](../deel/) *(beta)*, [`hibob`](../hibob/), [`personio`](../personio/), [`adp-ihcm`](../adp-ihcm/) *(beta)*, [`adp-workforce-now`](../adp-workforce-now/) *(beta)*, [`paylocity`](../paylocity/), and 49 more.

## See also

- [Apideck connection guide for Paychex](https://developers.apideck.com/connectors/paychex/docs/consumer+connection)
- [HRIS OpenAPI spec](https://specs.apideck.com/hris.yml) · [API Explorer](https://developers.apideck.com/api-explorer?id=hris)
- [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) — programmatic coverage checks
- [`apideck-best-practices`](../../skills/apideck-best-practices/) — architecture, Vault, pagination, error handling
- [`apideck-node`](../../skills/apideck-node/) — TypeScript / Node SDK patterns
- [Paychex official docs](https://developer.paychex.com)
