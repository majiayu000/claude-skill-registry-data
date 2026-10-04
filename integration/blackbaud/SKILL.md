---
name: blackbaud
description: |
  Blackbaud integration via Apideck's CRM unified API — same methods work across every connector in CRM, switch by changing `serviceId`. Use when the user wants to read, write, or search contacts, companies, leads, opportunities, activities, and pipelines in Blackbaud. Routes through Apideck with serviceId "blackbaud".
license: Apache-2.0
alwaysApply: false
metadata:
  author: apideck
  version: "1.0.0"
  serviceId: blackbaud
  unifiedApis: ["crm"]
  authType: oauth2
  tier: "2"
  verified: true
  status: beta
  difficulty: involved
  partnershipRequired: true
  sandboxAvailable: true
---

# Blackbaud (via Apideck)

Access Blackbaud through Apideck's **CRM** unified API — one of 21 CRM connectors that share the same method surface. Code you write here ports to Odoo, Salesforce, HubSpot and 17 other CRM connectors by changing a single `serviceId` string. Apideck handles auth, pagination, rate limiting, and retries so you don't write per-tenant Blackbaud plumbing.

> **Beta connector.** Blackbaud is currently in beta on Apideck. Expect partial resource coverage and occasional mapping gaps. Always verify coverage (see below) and fall back to the Proxy API for unsupported operations.

## Quick facts

- **Apideck serviceId:** `blackbaud`
- **Unified API:** CRM
- **Auth type:** oauth2
- **Status:** beta
- **Gotchas:** [page](https://developers.apideck.com/apis/crm/blackbaud/gotchas)
- **Blackbaud docs:** https://developer.blackbaud.com
- **Homepage:** https://blackbaud.com

## At a glance

- **Implementation difficulty:** involved — ISV Partner Status Needed Beyond 10 Environments + Subscription Key and Admin Connect Step
- **Vendor partnership required:** yes ([Blackbaud Partner Program (ISV)](https://www.blackbaud.com/become-a-partner)) — Needed to scale past the per-application environment cap; ISV Partner status gives unlimited environment connections and a Marketplace listing.
- **Apideck-managed credentials:** not available — Each Apideck customer registers their own SKY application and uses their own SKY API subscription key.
- **Account type required:** A Blackbaud Raiser's Edge NXT environment.
- **Consumer access level:** An organisation admin, or a user with Marketplace permission, connects the application first; the consenting user's permissions then limit the data.
- **Sandbox:** available ([signup](https://developer.blackbaud.com/skyapi/docs/getting-started/cohort)) — Email skyapi@blackbaud.com to request a SKY Developer Cohort sandbox and name Raiser's Edge NXT. Shared environment, read-only at first, test data only.
- **Costs:** Free tier has no fee; quota upgrades $5,000 a year (100,000 calls/day) or $10,000 (250,000), for Blackbaud customers and ISV Partners only. Subject to change.
- **Rate limits:** 10 calls per second; daily quota of 1,000 calls on Free, 25,000 on Standard and 100,000 per connection on Partner.
- **Authentication:** Authorization Code flow, plus a SKY API subscription key sent in the Bb-Api-Subscription-Key header.
- **Webhooks:** No webhooks - data is read by polling.

**Important to know:**

- One application connects up to 10 consumer environments without Partner status; an eleventh needs ISV Partner status for the application owner.
- Outside the Partner tier the daily call quota is shared by every connected environment, so each new consumer draws on the same fixed ceiling. Size sync frequency to all consumers together, not to one account.

> Facts synced from Apideck's connector metadata API — `GET /connector/connectors/blackbaud` (`overview` field) is the live, authoritative version.

## When to use this skill

Activate this skill when the user explicitly wants to work with **Blackbaud** — for example, "pull contacts in Blackbaud" or "sync leads in Blackbaud". This skill teaches the agent:

1. Which Apideck unified API covers Blackbaud (CRM)
2. The correct `serviceId` to pass on every call (`blackbaud`)
3. Blackbaud-specific auth and coverage caveats

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

// List contacts in Blackbaud
const { data } = await apideck.crm.contacts.list({
  serviceId: "blackbaud",
});
```

## Portable across 21 CRM connectors

The Apideck **CRM** unified API exposes the same methods for every connector in its catalog. Switching from Blackbaud to another CRM connector is a one-string change — no rewrite, no new SDK.

```typescript
// Today — Blackbaud
await apideck.crm.contacts.list({ serviceId: "blackbaud" });

// Tomorrow — same code, different connector
await apideck.crm.contacts.list({ serviceId: "odoo" });
await apideck.crm.contacts.list({ serviceId: "salesforce" });
```

This is the compounding advantage of using Apideck over integrating Blackbaud directly: code against the unified CRM API once, gain access to every connector in it. New connectors Apideck adds become available to your app without code changes.

## Authentication

- **Type:** OAuth 2.0
- **Managed by:** Apideck Vault — Apideck handles the full OAuth dance (authorization code flow, token exchange, refresh). Never ask the user for API keys or tokens directly.
- **User setup:** Users authorize via the Vault modal. Connection state progresses `available → added → authorized → callable`.
- **Token refresh:** automatic. Expired tokens are refreshed transparently on the next API call.

See [`apideck-best-practices`](../../skills/apideck-best-practices/) for Vault setup, connection lifecycle, and handling re-auth flows.

## Verifying coverage

Not every CRM operation is supported by every connector. Always verify before assuming a method works:

```bash
curl 'https://unify.apideck.com/connector/connectors/blackbaud' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}"
```

See [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) for patterns around `UnsupportedOperationError` and connector-specific fallbacks.

## Escape hatch: Proxy API

When an endpoint isn't covered by the CRM unified API, use Apideck's Proxy to call Blackbaud directly — Apideck injects auth headers and handles token refresh. Set `x-apideck-downstream-url` to the target endpoint on Blackbaud's own API:

```bash
curl 'https://unify.apideck.com/proxy' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}" \
  -H "x-apideck-consumer-id: ${CONSUMER_ID}" \
  -H "x-apideck-service-id: blackbaud" \
  -H "x-apideck-downstream-url: <target endpoint on Blackbaud>" \
  -H "x-apideck-downstream-method: GET"
```

See [Blackbaud's API docs](https://developer.blackbaud.com) for available endpoints.

## Sibling connectors

Other **CRM** connectors that share this unified API surface (same method signatures, just change `serviceId`):

[`odoo`](../odoo/) *(beta)*, [`salesforce`](../salesforce/), [`hubspot`](../hubspot/), [`pipedrive`](../pipedrive/), [`zoho-crm`](../zoho-crm/), [`activecampaign`](../activecampaign/), [`close`](../close/), [`microsoft-dynamics`](../microsoft-dynamics/), and 12 more.

## See also

- [CRM OpenAPI spec](https://specs.apideck.com/crm.yml) · [API Explorer](https://developers.apideck.com/api-explorer?id=crm)
- [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) — programmatic coverage checks
- [`apideck-best-practices`](../../skills/apideck-best-practices/) — architecture, Vault, pagination, error handling
- [`apideck-node`](../../skills/apideck-node/) — TypeScript / Node SDK patterns
- [Blackbaud official docs](https://developer.blackbaud.com)
