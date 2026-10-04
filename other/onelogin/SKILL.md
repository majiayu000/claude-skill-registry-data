---
name: onelogin
description: |
  OneLogin integration via Apideck's HRIS unified API — same methods work across every connector in HRIS, switch by changing `serviceId`. Use when the user wants to read or sync employees, departments, payrolls, and time-off records in OneLogin. Routes through Apideck with serviceId "onelogin".
license: Apache-2.0
alwaysApply: false
metadata:
  author: apideck
  version: "1.0.0"
  serviceId: onelogin
  unifiedApis: ["hris"]
  authType: oauth2
  tier: "2"
  verified: true
  status: beta
  difficulty: moderate
  partnershipRequired: false
  sandboxAvailable: true
---

# OneLogin (via Apideck)

Access OneLogin through Apideck's **HRIS** unified API — one of 58 HRIS connectors that share the same method surface. Code you write here ports to BambooHR, Workday, Deel and 54 other HRIS connectors by changing a single `serviceId` string. Apideck handles auth, pagination, rate limiting, and retries so you don't write per-tenant OneLogin plumbing.

> **Beta connector.** OneLogin is currently in beta on Apideck. Expect partial resource coverage and occasional mapping gaps. Always verify coverage (see below) and fall back to the Proxy API for unsupported operations.

## Quick facts

- **Apideck serviceId:** `onelogin`
- **Unified API:** HRIS
- **Auth type:** oauth2
- **Status:** beta
- **Apideck setup guide:** [Connection guide](https://developers.apideck.com/connectors/onelogin/docs/consumer+connection)
- **Gotchas:** [page](https://developers.apideck.com/apis/hris/onelogin/gotchas)
- **Homepage:** https://www.onelogin.com/

## At a glance

- **Implementation difficulty:** moderate — API Credentials - Each Consumer Creates a Client ID and Secret in OneLogin
- **Vendor partnership required:** no — Nothing has to be registered with OneLogin to use this connector.
- **Apideck-managed credentials:** not available — Each consumer creates their own OneLogin API credentials.
- **Account type required:** Any OneLogin account where the consumer can open Developers > API Credentials.
- **Consumer access level:** A OneLogin account owner or administrator, since only those roles can create API credentials.
- **Sandbox:** available — Start a OneLogin free trial to get a test account, then create API credentials in it the same way as in production.
- **Authentication:** Client credentials grant, using a client ID and secret.

**Important to know:**

- OneLogin ties API credentials to the user who created them. If that user is later deleted, the credentials fail with HTTP 500 and the consumer must create a new pair and reconnect, so have them create the pair from a long-lived admin account.

> Facts synced from Apideck's connector metadata API — `GET /connector/connectors/onelogin` (`overview` field) is the live, authoritative version.

## When to use this skill

Activate this skill when the user explicitly wants to work with **OneLogin** — for example, "sync employees in OneLogin" or "list time-off requests in OneLogin". This skill teaches the agent:

1. Which Apideck unified API covers OneLogin (HRIS)
2. The correct `serviceId` to pass on every call (`onelogin`)
3. OneLogin-specific auth and coverage caveats

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

// List employees in OneLogin
const { data } = await apideck.hris.employees.list({
  serviceId: "onelogin",
});
```

## Portable across 58 HRIS connectors

The Apideck **HRIS** unified API exposes the same methods for every connector in its catalog. Switching from OneLogin to another HRIS connector is a one-string change — no rewrite, no new SDK.

```typescript
// Today — OneLogin
await apideck.hris.employees.list({ serviceId: "onelogin" });

// Tomorrow — same code, different connector
await apideck.hris.employees.list({ serviceId: "bamboohr" });
await apideck.hris.employees.list({ serviceId: "workday" });
```

This is the compounding advantage of using Apideck over integrating OneLogin directly: code against the unified HRIS API once, gain access to every connector in it. New connectors Apideck adds become available to your app without code changes.

## Authentication

- **Type:** OAuth 2.0
- **Managed by:** Apideck Vault — Apideck handles the full OAuth dance (authorization code flow, token exchange, refresh). Never ask the user for API keys or tokens directly.
- **User setup:** Users authorize via the Vault modal. Connection state progresses `available → added → authorized → callable`.
- **Token refresh:** automatic. Expired tokens are refreshed transparently on the next API call.

**Setup guide:** Apideck publishes a step-by-step guide for registering an OAuth app / configuring credentials for OneLogin — see [https://developers.apideck.com/connectors/onelogin/docs/consumer+connection](https://developers.apideck.com/connectors/onelogin/docs/consumer+connection). Use that as the authoritative source when walking users through connection setup.

See [`apideck-best-practices`](../../skills/apideck-best-practices/) for Vault setup, connection lifecycle, and handling re-auth flows.

## Verifying coverage

Not every HRIS operation is supported by every connector. Always verify before assuming a method works:

```bash
curl 'https://unify.apideck.com/connector/connectors/onelogin' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}"
```

See [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) for patterns around `UnsupportedOperationError` and connector-specific fallbacks.

## Escape hatch: Proxy API

When an endpoint isn't covered by the HRIS unified API, use Apideck's Proxy to call OneLogin directly — Apideck injects auth headers and handles token refresh. Set `x-apideck-downstream-url` to the target endpoint on OneLogin's own API:

```bash
curl 'https://unify.apideck.com/proxy' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}" \
  -H "x-apideck-consumer-id: ${CONSUMER_ID}" \
  -H "x-apideck-service-id: onelogin" \
  -H "x-apideck-downstream-url: <target endpoint on OneLogin>" \
  -H "x-apideck-downstream-method: GET"
```

See [OneLogin's API docs](#) for available endpoints.

## Sibling connectors

Other **HRIS** connectors that share this unified API surface (same method signatures, just change `serviceId`):

[`bamboohr`](../bamboohr/), [`workday`](../workday/), [`deel`](../deel/) *(beta)*, [`hibob`](../hibob/), [`personio`](../personio/), [`adp-ihcm`](../adp-ihcm/) *(beta)*, [`adp-workforce-now`](../adp-workforce-now/) *(beta)*, [`paychex`](../paychex/) *(beta)*, and 49 more.

## See also

- [Apideck connection guide for OneLogin](https://developers.apideck.com/connectors/onelogin/docs/consumer+connection)
- [HRIS OpenAPI spec](https://specs.apideck.com/hris.yml) · [API Explorer](https://developers.apideck.com/api-explorer?id=hris)
- [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) — programmatic coverage checks
- [`apideck-best-practices`](../../skills/apideck-best-practices/) — architecture, Vault, pagination, error handling
- [`apideck-node`](../../skills/apideck-node/) — TypeScript / Node SDK patterns
