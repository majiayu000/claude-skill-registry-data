---
name: paylocity
description: |
  Paylocity integration via Apideck's HRIS unified API — same methods work across every connector in HRIS, switch by changing `serviceId`. Use when the user wants to read or sync employees, departments, payrolls, and time-off records in Paylocity. Routes through Apideck with serviceId "paylocity".
license: Apache-2.0
alwaysApply: false
metadata:
  author: apideck
  version: "1.0.0"
  serviceId: paylocity
  unifiedApis: ["hris"]
  authType: oauth2
  tier: "1c"
  verified: true
  difficulty: involved
  partnershipRequired: true
  sandboxAvailable: true
---

# Paylocity (via Apideck)

Access Paylocity through Apideck's **HRIS** unified API — one of 58 HRIS connectors that share the same method surface. Code you write here ports to BambooHR, Workday, Deel and 54 other HRIS connectors by changing a single `serviceId` string. Apideck handles auth, pagination, rate limiting, and retries so you don't write per-tenant Paylocity plumbing.

## Quick facts

- **Apideck serviceId:** `paylocity`
- **Unified API:** HRIS
- **Auth type:** oauth2
- **Gotchas:** [page](https://developers.apideck.com/apis/hris/paylocity/gotchas)
- **Paylocity docs:** https://developer.paylocity.com
- **Homepage:** https://www.paylocity.com/

## At a glance

- **Implementation difficulty:** involved — Vendor-Issued Credentials + Partner Agreement Needed for a Sandbox
- **Vendor partnership required:** yes ([Paylocity Technology Partner programme](https://www.paylocity.com/contact/partner-form/)) — Signing the Marketplace Partner Agreement unlocks sandbox credentials and, later, a Paylocity Marketplace listing.
- **Apideck-managed credentials:** not available — Each consumer supplies the credentials Paylocity issues to their own company.
- **Account type required:** A Paylocity customer company with API access enabled.
- **Consumer access level:** A company admin of the consumer's Paylocity company.
- **Sandbox:** available ([signup](https://www.paylocity.com/contact/partner-form/)) — Open to existing Paylocity customers, or to partners once the agreement is signed.
- **Costs:** Not published; Paylocity quotes integration and API pricing through the Paylocity account executive.
- **Rate limits:** Set per endpoint by Paylocity; no single headline figure is published.
- **Authentication:** Client credentials flow; each connection also needs the consumer's Paylocity Company ID.
- **Webhooks:** Virtual webhooks - employee created and updated events

**Important to know:**

- Paylocity issues API credentials by hand: each consumer requests a Client ID and Secret through their Paylocity account executive or webservices@paylocity.com, so when a connection can go live depends on Paylocity, not on you.

> Facts synced from Apideck's connector metadata API — `GET /connector/connectors/paylocity` (`overview` field) is the live, authoritative version.

## When to use this skill

Activate this skill when the user explicitly wants to work with **Paylocity** — for example, "sync employees in Paylocity" or "list time-off requests in Paylocity". This skill teaches the agent:

1. Which Apideck unified API covers Paylocity (HRIS)
2. The correct `serviceId` to pass on every call (`paylocity`)
3. Paylocity-specific auth and coverage caveats

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

// List employees in Paylocity
const { data } = await apideck.hris.employees.list({
  serviceId: "paylocity",
});
```

## Portable across 58 HRIS connectors

The Apideck **HRIS** unified API exposes the same methods for every connector in its catalog. Switching from Paylocity to another HRIS connector is a one-string change — no rewrite, no new SDK.

```typescript
// Today — Paylocity
await apideck.hris.employees.list({ serviceId: "paylocity" });

// Tomorrow — same code, different connector
await apideck.hris.employees.list({ serviceId: "bamboohr" });
await apideck.hris.employees.list({ serviceId: "workday" });
```

This is the compounding advantage of using Apideck over integrating Paylocity directly: code against the unified HRIS API once, gain access to every connector in it. New connectors Apideck adds become available to your app without code changes.

## Authentication

- **Type:** OAuth 2.0
- **Managed by:** Apideck Vault — Apideck handles the full OAuth dance (authorization code flow, token exchange, refresh). Never ask the user for API keys or tokens directly.
- **User setup:** Users authorize via the Vault modal. Connection state progresses `available → added → authorized → callable`.
- **Token refresh:** automatic. Expired tokens are refreshed transparently on the next API call.

See [`apideck-best-practices`](../../skills/apideck-best-practices/) for Vault setup, connection lifecycle, and handling re-auth flows.

## Verifying coverage

Not every HRIS operation is supported by every connector. Always verify before assuming a method works:

```bash
curl 'https://unify.apideck.com/connector/connectors/paylocity' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}"
```

See [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) for patterns around `UnsupportedOperationError` and connector-specific fallbacks.

## Escape hatch: Proxy API

When an endpoint isn't covered by the HRIS unified API, use Apideck's Proxy to call Paylocity directly — Apideck injects auth headers and handles token refresh. Set `x-apideck-downstream-url` to the target endpoint on Paylocity's own API:

```bash
curl 'https://unify.apideck.com/proxy' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}" \
  -H "x-apideck-consumer-id: ${CONSUMER_ID}" \
  -H "x-apideck-service-id: paylocity" \
  -H "x-apideck-downstream-url: <target endpoint on Paylocity>" \
  -H "x-apideck-downstream-method: GET"
```

See [Paylocity's API docs](https://developer.paylocity.com) for available endpoints.

## Sibling connectors

Other **HRIS** connectors that share this unified API surface (same method signatures, just change `serviceId`):

[`bamboohr`](../bamboohr/), [`workday`](../workday/), [`deel`](../deel/) *(beta)*, [`hibob`](../hibob/), [`personio`](../personio/), [`adp-ihcm`](../adp-ihcm/) *(beta)*, [`adp-workforce-now`](../adp-workforce-now/) *(beta)*, [`paychex`](../paychex/) *(beta)*, and 49 more.

## See also

- [HRIS OpenAPI spec](https://specs.apideck.com/hris.yml) · [API Explorer](https://developers.apideck.com/api-explorer?id=hris)
- [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) — programmatic coverage checks
- [`apideck-best-practices`](../../skills/apideck-best-practices/) — architecture, Vault, pagination, error handling
- [`apideck-node`](../../skills/apideck-node/) — TypeScript / Node SDK patterns
- [Paylocity official docs](https://developer.paylocity.com)
