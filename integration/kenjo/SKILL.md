---
name: kenjo
description: |
  Kenjo integration via Apideck's HRIS unified API — same methods work across every connector in HRIS, switch by changing `serviceId`. Use when the user wants to read or sync employees, departments, payrolls, and time-off records in Kenjo. Routes through Apideck with serviceId "kenjo".
license: Apache-2.0
alwaysApply: false
metadata:
  author: apideck
  version: "1.0.0"
  serviceId: kenjo
  unifiedApis: ["hris"]
  authType: oauth2
  tier: "2"
  verified: true
  status: beta
  difficulty: moderate
  partnershipRequired: false
  sandboxAvailable: true
---

# Kenjo (via Apideck)

Access Kenjo through Apideck's **HRIS** unified API — one of 58 HRIS connectors that share the same method surface. Code you write here ports to BambooHR, Workday, Deel and 54 other HRIS connectors by changing a single `serviceId` string. Apideck handles auth, pagination, rate limiting, and retries so you don't write per-tenant Kenjo plumbing.

> **Beta connector.** Kenjo is currently in beta on Apideck. Expect partial resource coverage and occasional mapping gaps. Always verify coverage (see below) and fall back to the Proxy API for unsupported operations.

## Quick facts

- **Apideck serviceId:** `kenjo`
- **Unified API:** HRIS
- **Auth type:** oauth2
- **Status:** beta
- **Gotchas:** [page](https://developers.apideck.com/apis/hris/kenjo/gotchas)
- **Kenjo docs:** https://developers.kenjo.io
- **Homepage:** https://www.kenjo.io/

## At a glance

- **Implementation difficulty:** moderate — Kenjo Customer Success Must Activate API Access
- **Vendor partnership required:** no ([developer portal](https://www.kenjo.io/partner-program-kenjo)) — Kenjo's software partner programme offers co-marketing and referral bonuses; API access does not depend on it.
- **Apideck-managed credentials:** not available — Each consumer generates their own Kenjo API key.
- **Account type required:** A Kenjo account on which Kenjo has activated API access.
- **Consumer access level:** Kenjo admin, since only admins can generate API keys.
- **Sandbox:** available ([signup](https://kenjo.readme.io/reference/generate-the-api-key)) — Ask Kenjo Customer Success to activate the API on a sandbox instead of production.
- **Costs:** Kenjo lists APIs and integrations under its Connect plan.
- **Rate limits:** Not published by Kenjo.
- **Authentication:** The consumer's Kenjo API key, not an OAuth consent flow.
- **Webhooks:** No webhooks - changes are picked up by polling.

**Important to know:**

- Keys are limited to five per Kenjo organisation. Deleting or regenerating a key, or changing its permissions, invalidates its tokens, so the connection stops until the new key is entered.

> Facts synced from Apideck's connector metadata API — `GET /connector/connectors/kenjo` (`overview` field) is the live, authoritative version.

## When to use this skill

Activate this skill when the user explicitly wants to work with **Kenjo** — for example, "sync employees in Kenjo" or "list time-off requests in Kenjo". This skill teaches the agent:

1. Which Apideck unified API covers Kenjo (HRIS)
2. The correct `serviceId` to pass on every call (`kenjo`)
3. Kenjo-specific auth and coverage caveats

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

// List employees in Kenjo
const { data } = await apideck.hris.employees.list({
  serviceId: "kenjo",
});
```

## Portable across 58 HRIS connectors

The Apideck **HRIS** unified API exposes the same methods for every connector in its catalog. Switching from Kenjo to another HRIS connector is a one-string change — no rewrite, no new SDK.

```typescript
// Today — Kenjo
await apideck.hris.employees.list({ serviceId: "kenjo" });

// Tomorrow — same code, different connector
await apideck.hris.employees.list({ serviceId: "bamboohr" });
await apideck.hris.employees.list({ serviceId: "workday" });
```

This is the compounding advantage of using Apideck over integrating Kenjo directly: code against the unified HRIS API once, gain access to every connector in it. New connectors Apideck adds become available to your app without code changes.

## Authentication

- **Type:** OAuth 2.0
- **Managed by:** Apideck Vault — Apideck handles the full OAuth dance (authorization code flow, token exchange, refresh). Never ask the user for API keys or tokens directly.
- **User setup:** Users authorize via the Vault modal. Connection state progresses `available → added → authorized → callable`.
- **Token refresh:** automatic. Expired tokens are refreshed transparently on the next API call.

See [`apideck-best-practices`](../../skills/apideck-best-practices/) for Vault setup, connection lifecycle, and handling re-auth flows.

## Verifying coverage

Not every HRIS operation is supported by every connector. Always verify before assuming a method works:

```bash
curl 'https://unify.apideck.com/connector/connectors/kenjo' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}"
```

See [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) for patterns around `UnsupportedOperationError` and connector-specific fallbacks.

## Escape hatch: Proxy API

When an endpoint isn't covered by the HRIS unified API, use Apideck's Proxy to call Kenjo directly — Apideck injects auth headers and handles token refresh. Set `x-apideck-downstream-url` to the target endpoint on Kenjo's own API:

```bash
curl 'https://unify.apideck.com/proxy' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}" \
  -H "x-apideck-consumer-id: ${CONSUMER_ID}" \
  -H "x-apideck-service-id: kenjo" \
  -H "x-apideck-downstream-url: <target endpoint on Kenjo>" \
  -H "x-apideck-downstream-method: GET"
```

See [Kenjo's API docs](https://developers.kenjo.io) for available endpoints.

## Sibling connectors

Other **HRIS** connectors that share this unified API surface (same method signatures, just change `serviceId`):

[`bamboohr`](../bamboohr/), [`workday`](../workday/), [`deel`](../deel/) *(beta)*, [`hibob`](../hibob/), [`personio`](../personio/), [`adp-ihcm`](../adp-ihcm/) *(beta)*, [`adp-workforce-now`](../adp-workforce-now/) *(beta)*, [`paychex`](../paychex/) *(beta)*, and 49 more.

## See also

- [HRIS OpenAPI spec](https://specs.apideck.com/hris.yml) · [API Explorer](https://developers.apideck.com/api-explorer?id=hris)
- [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) — programmatic coverage checks
- [`apideck-best-practices`](../../skills/apideck-best-practices/) — architecture, Vault, pagination, error handling
- [`apideck-node`](../../skills/apideck-node/) — TypeScript / Node SDK patterns
- [Kenjo official docs](https://developers.kenjo.io)
