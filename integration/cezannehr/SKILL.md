---
name: cezannehr
description: |
  Cezanne HR integration via Apideck's HRIS unified API — same methods work across every connector in HRIS, switch by changing `serviceId`. Use when the user wants to read or sync employees, departments, payrolls, and time-off records in Cezanne HR. Routes through Apideck with serviceId "cezannehr".
license: Apache-2.0
alwaysApply: false
metadata:
  author: apideck
  version: "1.0.0"
  serviceId: cezannehr
  unifiedApis: ["hris"]
  authType: oauth2
  tier: "2"
  verified: true
  status: beta
  difficulty: moderate
  partnershipRequired: false
  sandboxAvailable: false
---

# Cezanne HR (via Apideck)

Access Cezanne HR through Apideck's **HRIS** unified API — one of 58 HRIS connectors that share the same method surface. Code you write here ports to BambooHR, Workday, Deel and 54 other HRIS connectors by changing a single `serviceId` string. Apideck handles auth, pagination, rate limiting, and retries so you don't write per-tenant Cezanne HR plumbing.

> **Beta connector.** Cezanne HR is currently in beta on Apideck. Expect partial resource coverage and occasional mapping gaps. Always verify coverage (see below) and fall back to the Proxy API for unsupported operations.

## Quick facts

- **Apideck serviceId:** `cezannehr`
- **Unified API:** HRIS
- **Auth type:** oauth2
- **Status:** beta
- **Apideck setup guide:** [Connection guide](https://developers.apideck.com/connectors/cezannehr/docs/consumer+connection)
- **Gotchas:** [page](https://developers.apideck.com/apis/hris/cezannehr/gotchas)
- **Cezanne HR docs:** https://cezannehr.com
- **Homepage:** https://cezannehr.com/

## At a glance

- **Implementation difficulty:** moderate — Client Credentials Created Manually by Each Consumer's Cezanne Admin
- **Vendor partnership required:** no — Cezanne's API documentation describes adding an API application with no partner step.
- **Apideck-managed credentials:** not available — Each consumer creates their own API application in Cezanne.
- **Account type required:** A Cezanne HR customer subscription with API access enabled.
- **Consumer access level:** A Cezanne system administrator; the connection then runs with the permissions of the chosen service account user.
- **Sandbox:** not available — Testing needs a real Cezanne tenant, as no self-service sandbox is documented.
- **Costs:** The API is listed among the features included in the Cezanne subscription; no separate API fee is published.
- **Authentication:** Client credentials grant, with no user sign-in step.
- **Webhooks:** No webhooks - changes are picked up by polling.

**Important to know:**

- If the service account user's password expires, the connection stops working until the password is changed, so choose a user whose password never expires.

> Facts synced from Apideck's connector metadata API — `GET /connector/connectors/cezannehr` (`overview` field) is the live, authoritative version.

## When to use this skill

Activate this skill when the user explicitly wants to work with **Cezanne HR** — for example, "sync employees in Cezanne HR" or "list time-off requests in Cezanne HR". This skill teaches the agent:

1. Which Apideck unified API covers Cezanne HR (HRIS)
2. The correct `serviceId` to pass on every call (`cezannehr`)
3. Cezanne HR-specific auth and coverage caveats

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

// List employees in Cezanne HR
const { data } = await apideck.hris.employees.list({
  serviceId: "cezannehr",
});
```

## Portable across 58 HRIS connectors

The Apideck **HRIS** unified API exposes the same methods for every connector in its catalog. Switching from Cezanne HR to another HRIS connector is a one-string change — no rewrite, no new SDK.

```typescript
// Today — Cezanne HR
await apideck.hris.employees.list({ serviceId: "cezannehr" });

// Tomorrow — same code, different connector
await apideck.hris.employees.list({ serviceId: "bamboohr" });
await apideck.hris.employees.list({ serviceId: "workday" });
```

This is the compounding advantage of using Apideck over integrating Cezanne HR directly: code against the unified HRIS API once, gain access to every connector in it. New connectors Apideck adds become available to your app without code changes.

## Authentication

- **Type:** OAuth 2.0
- **Managed by:** Apideck Vault — Apideck handles the full OAuth dance (authorization code flow, token exchange, refresh). Never ask the user for API keys or tokens directly.
- **User setup:** Users authorize via the Vault modal. Connection state progresses `available → added → authorized → callable`.
- **Token refresh:** automatic. Expired tokens are refreshed transparently on the next API call.

**Setup guide:** Apideck publishes a step-by-step guide for registering an OAuth app / configuring credentials for Cezanne HR — see [https://developers.apideck.com/connectors/cezannehr/docs/consumer+connection](https://developers.apideck.com/connectors/cezannehr/docs/consumer+connection). Use that as the authoritative source when walking users through connection setup.

See [`apideck-best-practices`](../../skills/apideck-best-practices/) for Vault setup, connection lifecycle, and handling re-auth flows.

## Verifying coverage

Not every HRIS operation is supported by every connector. Always verify before assuming a method works:

```bash
curl 'https://unify.apideck.com/connector/connectors/cezannehr' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}"
```

See [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) for patterns around `UnsupportedOperationError` and connector-specific fallbacks.

## Escape hatch: Proxy API

When an endpoint isn't covered by the HRIS unified API, use Apideck's Proxy to call Cezanne HR directly — Apideck injects auth headers and handles token refresh. Set `x-apideck-downstream-url` to the target endpoint on Cezanne HR's own API:

```bash
curl 'https://unify.apideck.com/proxy' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}" \
  -H "x-apideck-consumer-id: ${CONSUMER_ID}" \
  -H "x-apideck-service-id: cezannehr" \
  -H "x-apideck-downstream-url: <target endpoint on Cezanne HR>" \
  -H "x-apideck-downstream-method: GET"
```

See [Cezanne HR's API docs](https://cezannehr.com) for available endpoints.

## Sibling connectors

Other **HRIS** connectors that share this unified API surface (same method signatures, just change `serviceId`):

[`bamboohr`](../bamboohr/), [`workday`](../workday/), [`deel`](../deel/) *(beta)*, [`hibob`](../hibob/), [`personio`](../personio/), [`adp-ihcm`](../adp-ihcm/) *(beta)*, [`adp-workforce-now`](../adp-workforce-now/) *(beta)*, [`paychex`](../paychex/) *(beta)*, and 49 more.

## See also

- [Apideck connection guide for Cezanne HR](https://developers.apideck.com/connectors/cezannehr/docs/consumer+connection)
- [HRIS OpenAPI spec](https://specs.apideck.com/hris.yml) · [API Explorer](https://developers.apideck.com/api-explorer?id=hris)
- [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) — programmatic coverage checks
- [`apideck-best-practices`](../../skills/apideck-best-practices/) — architecture, Vault, pagination, error handling
- [`apideck-node`](../../skills/apideck-node/) — TypeScript / Node SDK patterns
- [Cezanne HR official docs](https://cezannehr.com)
