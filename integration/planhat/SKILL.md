---
name: planhat
description: |
  Planhat integration via Apideck's CRM unified API — same methods work across every connector in CRM, switch by changing `serviceId`. Use when the user wants to read, write, or search contacts, companies, leads, opportunities, activities, and pipelines in Planhat. Routes through Apideck with serviceId "planhat".
license: Apache-2.0
alwaysApply: false
metadata:
  author: apideck
  version: "1.0.0"
  serviceId: planhat
  unifiedApis: ["crm"]
  authType: apiKey
  tier: "2"
  verified: true
  difficulty: moderate
  partnershipRequired: false
  sandboxAvailable: false
---

# Planhat (via Apideck)

Access Planhat through Apideck's **CRM** unified API — one of 21 CRM connectors that share the same method surface. Code you write here ports to Odoo, Salesforce, HubSpot and 17 other CRM connectors by changing a single `serviceId` string. Apideck handles auth, pagination, rate limiting, and retries so you don't write per-tenant Planhat plumbing.

## Quick facts

- **Apideck serviceId:** `planhat`
- **Unified API:** CRM
- **Auth type:** apiKey
- **Gotchas:** [page](https://developers.apideck.com/apis/crm/planhat/gotchas)
- **Planhat docs:** https://docs.planhat.com
- **Homepage:** https://planhat.com

## At a glance

- **Implementation difficulty:** moderate — Manual API Token Created by Each Consumer in a Planhat Private App
- **Vendor partnership required:** no ([developer portal](https://www.planhat.com/partners)) — Joining the Technology Partner track gives a listing on Planhat's website and in-app marketplace.
- **Apideck-managed credentials:** not available — Each consumer generates their own Planhat API access token.
- **Account type required:** Planhat tenant with Private Apps (Service Accounts) enabled.
- **Consumer access level:** A Planhat user with the ServiceAccount data-model permission, typically an admin.
- **Sandbox:** not available
- **Rate limits:** 200 calls a minute (soft quota); hard limit of 150 requests a second, with bursts of up to 50 parallel requests.
- **Authentication:** Access token from a Planhat Private App, sent as a bearer token; not OAuth.
- **Webhooks:** No webhooks - changes are picked up by polling the Planhat API.

**Important to know:**

- Planhat API tokens now expire: a new token defaults to 30 days and can be set to at most 365. At expiry the connection stops working until the consumer generates a new token in Planhat and updates it in Vault; Apideck cannot renew it.

> Facts synced from Apideck's connector metadata API — `GET /connector/connectors/planhat` (`overview` field) is the live, authoritative version.

## When to use this skill

Activate this skill when the user explicitly wants to work with **Planhat** — for example, "pull contacts in Planhat" or "sync leads in Planhat". This skill teaches the agent:

1. Which Apideck unified API covers Planhat (CRM)
2. The correct `serviceId` to pass on every call (`planhat`)
3. Planhat-specific auth and coverage caveats

For the full method surface (parameters, pagination, filtering), use your language SDK skill:

- [`apideck-node`](../../skills/apideck-node/), [`apideck-python`](../../skills/apideck-python/), [`apideck-dotnet`](../../skills/apideck-dotnet/), [`apideck-java`](../../skills/apideck-java/), [`apideck-go`](../../skills/apideck-go/), [`apideck-php`](../../skills/apideck-php/), or [`apideck-rest`](../../skills/apideck-rest/)

For the raw OpenAPI spec:

- **CRM:** [https://specs.apideck.com/crm.yml](https://specs.apideck.com/crm.yml) · [API Explorer](https://developers.apideck.com/api-explorer?id=crm)

## Minimal example (TypeScript)

```typescript
import { Apideck } from "@apideck/unify";

const apideck = new Apideck({
  apiKey: process.env.APIDECK_API_KEY,
  appId: process.env.APIDECK_APP_ID,
  consumerId: "your-consumer-id",
});

// List contacts in Planhat
const { data } = await apideck.crm.contacts.list({
  serviceId: "planhat",
});
```

## Portable across 21 CRM connectors

The Apideck **CRM** unified API exposes the same methods for every connector in its catalog. Switching from Planhat to another CRM connector is a one-string change — no rewrite, no new SDK.

```typescript
// Today — Planhat
await apideck.crm.contacts.list({ serviceId: "planhat" });

// Tomorrow — same code, different connector
await apideck.crm.contacts.list({ serviceId: "odoo" });
await apideck.crm.contacts.list({ serviceId: "salesforce" });
```

This is the compounding advantage of using Apideck over integrating Planhat directly: code against the unified CRM API once, gain access to every connector in it. New connectors Apideck adds become available to your app without code changes.

## Authentication

- **Type:** API Key
- **Managed by:** Apideck Vault — the user pastes their Planhat API key into the Vault modal; Apideck stores it encrypted and injects it on every request.
- **Rotation:** if the user rotates their key, they re-enter it in Vault. No code changes needed.

See [`apideck-best-practices`](../../skills/apideck-best-practices/) for Vault setup, connection lifecycle, and handling re-auth flows.

## Verifying coverage

Not every CRM operation is supported by every connector. Always verify before assuming a method works:

```bash
curl 'https://unify.apideck.com/connector/connectors/planhat' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}"
```

See [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) for patterns around `UnsupportedOperationError` and connector-specific fallbacks.

## Escape hatch: Proxy API

When an endpoint isn't covered by the CRM unified API, use Apideck's Proxy to call Planhat directly — Apideck injects auth headers and handles token refresh. Set `x-apideck-downstream-url` to the target endpoint on Planhat's own API:

```bash
curl 'https://unify.apideck.com/proxy' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}" \
  -H "x-apideck-consumer-id: ${CONSUMER_ID}" \
  -H "x-apideck-service-id: planhat" \
  -H "x-apideck-downstream-url: <target endpoint on Planhat>" \
  -H "x-apideck-downstream-method: GET"
```

See [Planhat's API docs](https://docs.planhat.com) for available endpoints.

## Sibling connectors

Other **CRM** connectors that share this unified API surface (same method signatures, just change `serviceId`):

[`odoo`](../odoo/) *(beta)*, [`salesforce`](../salesforce/), [`hubspot`](../hubspot/), [`pipedrive`](../pipedrive/), [`zoho-crm`](../zoho-crm/), [`activecampaign`](../activecampaign/), [`close`](../close/), [`microsoft-dynamics`](../microsoft-dynamics/), and 12 more.

## See also

- [CRM OpenAPI spec](https://specs.apideck.com/crm.yml) · [API Explorer](https://developers.apideck.com/api-explorer?id=crm)
- [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) — programmatic coverage checks
- [`apideck-best-practices`](../../skills/apideck-best-practices/) — architecture, Vault, pagination, error handling
- [`apideck-node`](../../skills/apideck-node/) — TypeScript / Node SDK patterns
- [Planhat official docs](https://docs.planhat.com)
