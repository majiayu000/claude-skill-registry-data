---
name: copper
description: |
  Copper integration via Apideck's CRM unified API — same methods work across every connector in CRM, switch by changing `serviceId`. Use when the user wants to read, write, or search contacts, companies, leads, opportunities, activities, and pipelines in Copper. Routes through Apideck with serviceId "copper".
license: Apache-2.0
alwaysApply: false
metadata:
  author: apideck
  version: "1.0.0"
  serviceId: copper
  unifiedApis: ["crm"]
  authType: apiKey
  tier: "2"
  verified: true
  difficulty: moderate
  partnershipRequired: false
  sandboxAvailable: true
---

# Copper (via Apideck)

Access Copper through Apideck's **CRM** unified API — one of 21 CRM connectors that share the same method surface. Code you write here ports to Odoo, Salesforce, HubSpot and 17 other CRM connectors by changing a single `serviceId` string. Apideck handles auth, pagination, rate limiting, and retries so you don't write per-tenant Copper plumbing.

## Quick facts

- **Apideck serviceId:** `copper`
- **Unified API:** CRM
- **Auth type:** apiKey
- **Gotchas:** [page](https://developers.apideck.com/apis/crm/copper/gotchas)
- **Copper docs:** https://developer.copper.com
- **Homepage:** https://www.copper.com/

## At a glance

- **Implementation difficulty:** moderate — API Key Authentication - Each Consumer Generates Their Own Key in Copper
- **Vendor partnership required:** no
- **Apideck-managed credentials:** not available — Each consumer generates their own Copper API key.
- **Account type required:** Copper account. The API sees only the records the key owner's Team Permissions allow.
- **Consumer access level:** A Copper Admin, since only Admin users can generate API keys.
- **Sandbox:** available ([signup](https://www.copper.com/signup)) — Free 14-day trial on the Business plan, no credit card; sign-up needs a Google or Gmail account.
- **Rate limits:** 180 requests a minute; bulk APIs also allow 3 requests a second.
- **Authentication:** Sent in request headers.
- **Webhooks:** No webhooks - read the resources to detect changes.

**Important to know:**

- Copper requires the API key together with the email address of the user who generated it, so the consumer supplies both when connecting.

> Facts synced from Apideck's connector metadata API — `GET /connector/connectors/copper` (`overview` field) is the live, authoritative version.

## When to use this skill

Activate this skill when the user explicitly wants to work with **Copper** — for example, "pull contacts in Copper" or "sync leads in Copper". This skill teaches the agent:

1. Which Apideck unified API covers Copper (CRM)
2. The correct `serviceId` to pass on every call (`copper`)
3. Copper-specific auth and coverage caveats

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

// List contacts in Copper
const { data } = await apideck.crm.contacts.list({
  serviceId: "copper",
});
```

## Portable across 21 CRM connectors

The Apideck **CRM** unified API exposes the same methods for every connector in its catalog. Switching from Copper to another CRM connector is a one-string change — no rewrite, no new SDK.

```typescript
// Today — Copper
await apideck.crm.contacts.list({ serviceId: "copper" });

// Tomorrow — same code, different connector
await apideck.crm.contacts.list({ serviceId: "odoo" });
await apideck.crm.contacts.list({ serviceId: "salesforce" });
```

This is the compounding advantage of using Apideck over integrating Copper directly: code against the unified CRM API once, gain access to every connector in it. New connectors Apideck adds become available to your app without code changes.

## Authentication

- **Type:** API Key
- **Managed by:** Apideck Vault — the user pastes their Copper API key into the Vault modal; Apideck stores it encrypted and injects it on every request.
- **Rotation:** if the user rotates their key, they re-enter it in Vault. No code changes needed.

See [`apideck-best-practices`](../../skills/apideck-best-practices/) for Vault setup, connection lifecycle, and handling re-auth flows.

## Verifying coverage

Not every CRM operation is supported by every connector. Always verify before assuming a method works:

```bash
curl 'https://unify.apideck.com/connector/connectors/copper' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}"
```

See [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) for patterns around `UnsupportedOperationError` and connector-specific fallbacks.

## Escape hatch: Proxy API

When an endpoint isn't covered by the CRM unified API, use Apideck's Proxy to call Copper directly — Apideck injects auth headers and handles token refresh. Set `x-apideck-downstream-url` to the target endpoint on Copper's own API:

```bash
curl 'https://unify.apideck.com/proxy' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}" \
  -H "x-apideck-consumer-id: ${CONSUMER_ID}" \
  -H "x-apideck-service-id: copper" \
  -H "x-apideck-downstream-url: <target endpoint on Copper>" \
  -H "x-apideck-downstream-method: GET"
```

See [Copper's API docs](https://developer.copper.com) for available endpoints.

## Sibling connectors

Other **CRM** connectors that share this unified API surface (same method signatures, just change `serviceId`):

[`odoo`](../odoo/) *(beta)*, [`salesforce`](../salesforce/), [`hubspot`](../hubspot/), [`pipedrive`](../pipedrive/), [`zoho-crm`](../zoho-crm/), [`activecampaign`](../activecampaign/), [`close`](../close/), [`microsoft-dynamics`](../microsoft-dynamics/), and 12 more.

## See also

- [CRM OpenAPI spec](https://specs.apideck.com/crm.yml) · [API Explorer](https://developers.apideck.com/api-explorer?id=crm)
- [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) — programmatic coverage checks
- [`apideck-best-practices`](../../skills/apideck-best-practices/) — architecture, Vault, pagination, error handling
- [`apideck-node`](../../skills/apideck-node/) — TypeScript / Node SDK patterns
- [Copper official docs](https://developer.copper.com)
