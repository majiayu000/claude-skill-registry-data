---
name: payfit
description: |
  PayFit integration via Apideck's HRIS unified API — same methods work across every connector in HRIS, switch by changing `serviceId`. Use when the user wants to read or sync employees, departments, payrolls, and time-off records in PayFit. Routes through Apideck with serviceId "payfit".
license: Apache-2.0
alwaysApply: false
metadata:
  author: apideck
  version: "1.0.0"
  serviceId: payfit
  unifiedApis: ["hris"]
  authType: oauth2
  tier: "2"
  verified: true
  difficulty: involved
  partnershipRequired: true
  sandboxAvailable: true
---

# PayFit (via Apideck)

Access PayFit through Apideck's **HRIS** unified API — one of 58 HRIS connectors that share the same method surface. Code you write here ports to BambooHR, Workday, Deel and 54 other HRIS connectors by changing a single `serviceId` string. Apideck handles auth, pagination, rate limiting, and retries so you don't write per-tenant PayFit plumbing.

## Quick facts

- **Apideck serviceId:** `payfit`
- **Unified API:** HRIS
- **Auth type:** oauth2
- **Gotchas:** [page](https://developers.apideck.com/apis/hris/payfit/gotchas)
- **PayFit docs:** https://developers.payfit.com
- **Homepage:** https://payfit.com/

## At a glance

- **Implementation difficulty:** involved — Required PayFit Product Partnership + Per-Partner Scope Approval
- **Vendor partnership required:** yes ([PayFit Developer Portal](https://developers.payfit.io/docs/how-to-become-a-partner)) — Joining gives you a client ID and secret plus a test company; PayFit validates each use case first.
- **Apideck-managed credentials:** not available — PayFit issues client credentials only to its own product partners.
- **Account type required:** A PayFit company in France, the UK or Spain; some endpoints exist only in specific markets.
- **Consumer access level:** A PayFit admin of the company, since only an admin can approve access.
- **Sandbox:** available ([signup](https://developers.payfit.io/docs/how-to-become-a-partner)) — Test company credentials are issued to accepted partners; PayFit documents no self-serve signup.
- **Rate limits:** 50 requests per second for reads and 20 per second for writes, per client application.
- **Authentication:** Authorization Code flow.
- **Webhooks:** Virtual webhooks - employee created, updated and terminated events

**Important to know:**

- PayFit has temporarily stopped accepting new API integration requests and gives no reopening date. If you are not yet a PayFit product partner, you cannot start the partner process until PayFit reopens intake.
- PayFit whitelists the scopes each partner may request, and a request outside that whitelist is rejected. Settle your use cases with PayFit up front, because the connector can only read what your approved scopes allow.

> Facts synced from Apideck's connector metadata API — `GET /connector/connectors/payfit` (`overview` field) is the live, authoritative version.

## When to use this skill

Activate this skill when the user explicitly wants to work with **PayFit** — for example, "sync employees in PayFit" or "list time-off requests in PayFit". This skill teaches the agent:

1. Which Apideck unified API covers PayFit (HRIS)
2. The correct `serviceId` to pass on every call (`payfit`)
3. PayFit-specific auth and coverage caveats

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

// List employees in PayFit
const { data } = await apideck.hris.employees.list({
  serviceId: "payfit",
});
```

## Portable across 58 HRIS connectors

The Apideck **HRIS** unified API exposes the same methods for every connector in its catalog. Switching from PayFit to another HRIS connector is a one-string change — no rewrite, no new SDK.

```typescript
// Today — PayFit
await apideck.hris.employees.list({ serviceId: "payfit" });

// Tomorrow — same code, different connector
await apideck.hris.employees.list({ serviceId: "bamboohr" });
await apideck.hris.employees.list({ serviceId: "workday" });
```

This is the compounding advantage of using Apideck over integrating PayFit directly: code against the unified HRIS API once, gain access to every connector in it. New connectors Apideck adds become available to your app without code changes.

## Authentication

- **Type:** OAuth 2.0
- **Managed by:** Apideck Vault — Apideck handles the full OAuth dance (authorization code flow, token exchange, refresh). Never ask the user for API keys or tokens directly.
- **User setup:** Users authorize via the Vault modal. Connection state progresses `available → added → authorized → callable`.
- **Token refresh:** automatic. Expired tokens are refreshed transparently on the next API call.

See [`apideck-best-practices`](../../skills/apideck-best-practices/) for Vault setup, connection lifecycle, and handling re-auth flows.

## Verifying coverage

Not every HRIS operation is supported by every connector. Always verify before assuming a method works:

```bash
curl 'https://unify.apideck.com/connector/connectors/payfit' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}"
```

See [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) for patterns around `UnsupportedOperationError` and connector-specific fallbacks.

## Escape hatch: Proxy API

When an endpoint isn't covered by the HRIS unified API, use Apideck's Proxy to call PayFit directly — Apideck injects auth headers and handles token refresh. Set `x-apideck-downstream-url` to the target endpoint on PayFit's own API:

```bash
curl 'https://unify.apideck.com/proxy' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}" \
  -H "x-apideck-consumer-id: ${CONSUMER_ID}" \
  -H "x-apideck-service-id: payfit" \
  -H "x-apideck-downstream-url: <target endpoint on PayFit>" \
  -H "x-apideck-downstream-method: GET"
```

See [PayFit's API docs](https://developers.payfit.com) for available endpoints.

## Sibling connectors

Other **HRIS** connectors that share this unified API surface (same method signatures, just change `serviceId`):

[`bamboohr`](../bamboohr/), [`workday`](../workday/), [`deel`](../deel/) *(beta)*, [`hibob`](../hibob/), [`personio`](../personio/), [`adp-ihcm`](../adp-ihcm/) *(beta)*, [`adp-workforce-now`](../adp-workforce-now/) *(beta)*, [`paychex`](../paychex/) *(beta)*, and 49 more.

## See also

- [HRIS OpenAPI spec](https://specs.apideck.com/hris.yml) · [API Explorer](https://developers.apideck.com/api-explorer?id=hris)
- [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) — programmatic coverage checks
- [`apideck-best-practices`](../../skills/apideck-best-practices/) — architecture, Vault, pagination, error handling
- [`apideck-node`](../../skills/apideck-node/) — TypeScript / Node SDK patterns
- [PayFit official docs](https://developers.payfit.com)
