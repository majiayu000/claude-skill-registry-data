---
name: loket-nl
description: |
  Loket.nl integration via Apideck's HRIS unified API — same methods work across every connector in HRIS, switch by changing `serviceId`. Use when the user wants to read or sync employees, departments, payrolls, and time-off records in Loket.nl. Routes through Apideck with serviceId "loket-nl".
license: Apache-2.0
alwaysApply: false
metadata:
  author: apideck
  version: "1.0.0"
  serviceId: loket-nl
  unifiedApis: ["hris"]
  authType: oauth2
  tier: "2"
  verified: true
  difficulty: involved
  partnershipRequired: true
  sandboxAvailable: true
---

# Loket.nl (via Apideck)

Access Loket.nl through Apideck's **HRIS** unified API — one of 58 HRIS connectors that share the same method surface. Code you write here ports to BambooHR, Workday, Deel and 54 other HRIS connectors by changing a single `serviceId` string. Apideck handles auth, pagination, rate limiting, and retries so you don't write per-tenant Loket.nl plumbing.

## Quick facts

- **Apideck serviceId:** `loket-nl`
- **Unified API:** HRIS
- **Auth type:** oauth2
- **Gotchas:** [page](https://developers.apideck.com/apis/hris/loket-nl/gotchas)
- **Loket.nl docs:** https://developer.loket.nl
- **Homepage:** https://www.loket.nl/

## At a glance

- **Implementation difficulty:** involved — Required Loket Partner Application + Production Approval
- **Vendor partnership required:** yes ([Koppelen met Loket](https://loket.nl/koppelen-met-loket/)) — Apply as an integration partner; approval gives a development account (OAuth client and test user) on the acceptance environment.
- **Apideck-managed credentials:** not available — Loket issues OAuth clients to each integration partner, so you register with Loket and use your own client.
- **Account type required:** Loket employer account; accountants can also manage employers through a provider account.
- **Consumer access level:** A Loket user authorised for the employer, with the rights the integration needs.
- **Sandbox:** available ([signup](https://loket.nl/koppelen-met-loket/)) — Acceptance environment with a limited set of test data; issued once Loket accepts your application.
- **Rate limits:** No explicit usage limits are enforced; Loket monitors usage and may contact you about extreme volumes such as many error calls.
- **Authentication:** Authorization Code flow; the only supported scope is all.
- **Webhooks:** Virtual webhooks - employee created and updated events

**Important to know:**

- Production access is granted per API activity: Loket asks for the list of operations your integration uses when you request production access, and a production client can only call those.
- Loket registers every redirect URI by hand and matches it exactly, so plan one shared redirect URI for all your customers; a separate URI per customer is impractical.

> Facts synced from Apideck's connector metadata API — `GET /connector/connectors/loket-nl` (`overview` field) is the live, authoritative version.

## When to use this skill

Activate this skill when the user explicitly wants to work with **Loket.nl** — for example, "sync employees in Loket.nl" or "list time-off requests in Loket.nl". This skill teaches the agent:

1. Which Apideck unified API covers Loket.nl (HRIS)
2. The correct `serviceId` to pass on every call (`loket-nl`)
3. Loket.nl-specific auth and coverage caveats

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

// List employees in Loket.nl
const { data } = await apideck.hris.employees.list({
  serviceId: "loket-nl",
});
```

## Portable across 58 HRIS connectors

The Apideck **HRIS** unified API exposes the same methods for every connector in its catalog. Switching from Loket.nl to another HRIS connector is a one-string change — no rewrite, no new SDK.

```typescript
// Today — Loket.nl
await apideck.hris.employees.list({ serviceId: "loket-nl" });

// Tomorrow — same code, different connector
await apideck.hris.employees.list({ serviceId: "bamboohr" });
await apideck.hris.employees.list({ serviceId: "workday" });
```

This is the compounding advantage of using Apideck over integrating Loket.nl directly: code against the unified HRIS API once, gain access to every connector in it. New connectors Apideck adds become available to your app without code changes.

## Authentication

- **Type:** OAuth 2.0
- **Managed by:** Apideck Vault — Apideck handles the full OAuth dance (authorization code flow, token exchange, refresh). Never ask the user for API keys or tokens directly.
- **User setup:** Users authorize via the Vault modal. Connection state progresses `available → added → authorized → callable`.
- **Token refresh:** automatic. Expired tokens are refreshed transparently on the next API call.

See [`apideck-best-practices`](../../skills/apideck-best-practices/) for Vault setup, connection lifecycle, and handling re-auth flows.

## Verifying coverage

Not every HRIS operation is supported by every connector. Always verify before assuming a method works:

```bash
curl 'https://unify.apideck.com/connector/connectors/loket-nl' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}"
```

See [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) for patterns around `UnsupportedOperationError` and connector-specific fallbacks.

## Escape hatch: Proxy API

When an endpoint isn't covered by the HRIS unified API, use Apideck's Proxy to call Loket.nl directly — Apideck injects auth headers and handles token refresh. Set `x-apideck-downstream-url` to the target endpoint on Loket.nl's own API:

```bash
curl 'https://unify.apideck.com/proxy' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}" \
  -H "x-apideck-consumer-id: ${CONSUMER_ID}" \
  -H "x-apideck-service-id: loket-nl" \
  -H "x-apideck-downstream-url: <target endpoint on Loket.nl>" \
  -H "x-apideck-downstream-method: GET"
```

See [Loket.nl's API docs](https://developer.loket.nl) for available endpoints.

## Sibling connectors

Other **HRIS** connectors that share this unified API surface (same method signatures, just change `serviceId`):

[`bamboohr`](../bamboohr/), [`workday`](../workday/), [`deel`](../deel/) *(beta)*, [`hibob`](../hibob/), [`personio`](../personio/), [`adp-ihcm`](../adp-ihcm/) *(beta)*, [`adp-workforce-now`](../adp-workforce-now/) *(beta)*, [`paychex`](../paychex/) *(beta)*, and 49 more.

## See also

- [HRIS OpenAPI spec](https://specs.apideck.com/hris.yml) · [API Explorer](https://developers.apideck.com/api-explorer?id=hris)
- [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) — programmatic coverage checks
- [`apideck-best-practices`](../../skills/apideck-best-practices/) — architecture, Vault, pagination, error handling
- [`apideck-node`](../../skills/apideck-node/) — TypeScript / Node SDK patterns
- [Loket.nl official docs](https://developer.loket.nl)
