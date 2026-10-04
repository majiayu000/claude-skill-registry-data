---
name: hubspot
description: |
  HubSpot integration via Apideck's CRM unified API — same methods work across every connector in CRM, switch by changing `serviceId`. Use when the user wants to read, write, or search contacts, companies, leads, opportunities, activities, and pipelines in HubSpot. Routes through Apideck with serviceId "hubspot".
license: Apache-2.0
alwaysApply: false
metadata:
  author: apideck
  version: "1.0.0"
  serviceId: hubspot
  unifiedApis: ["crm"]
  authType: oauth2
  tier: "1b"
  verified: true
  difficulty: straightforward
  partnershipRequired: false
  sandboxAvailable: true
---

# HubSpot (via Apideck)

Access HubSpot through Apideck's **CRM** unified API — one of 21 CRM connectors that share the same method surface. Code you write here ports to Odoo, Salesforce, Pipedrive and 17 other CRM connectors by changing a single `serviceId` string. Apideck handles auth, pagination, rate limiting, and retries so you don't write per-tenant HubSpot plumbing.

## Quick facts

- **Apideck serviceId:** `hubspot`
- **Unified API:** CRM
- **Auth type:** oauth2
- **Gotchas:** [page](https://developers.apideck.com/apis/crm/hubspot/gotchas)
- **HubSpot docs:** https://developers.hubspot.com
- **Homepage:** https://www.hubspot.com/

## At a glance

- **Implementation difficulty:** straightforward — Self-Service OAuth + Free Developer Tooling — No Partnership or App Review
- **Vendor partnership required:** no ([HubSpot App Marketplace](https://developers.hubspot.com/docs/apps/developer-platform/list-apps/apply-for-certification/certification-requirements)) — Listing in the App Marketplace makes you a HubSpot Technology Partner and adds a free listing page; developer test accounts need no partnership.
- **Apideck-managed credentials:** available — For testing: OAuth shows "Apideck" as the requesting application; production integrations use your own HubSpot app.
- **Account type required:** Any HubSpot edition, including the free CRM.
- **Consumer access level:** The authorizing user needs the App Marketplace Access permission (super admins have it by default).
- **Sandbox:** available ([signup](https://developers.hubspot.com/docs/getting-started/account-types)) — Free developer test accounts, self-service from your regular HubSpot account (up to 10).
- **Costs:** None — HubSpot developer tooling and public apps are free to build and distribute.
- **Rate limits:** 110 requests per 10 seconds per connected account for publicly-distributed OAuth apps; the CRM Search API is separate at 5 requests/second.
- **Authentication:** Authorization Code flow.
- **Webhooks:** Native — contact, company and opportunity created/updated/deleted events; no engagement (activity or note) events.

**Important to know:**

- The scopes configured on your HubSpot app must match exactly the scopes Apideck requests during OAuth. Any mismatch fails consumer authorization with an insufficient-scopes error, so update the app whenever the connector's scope set changes.
- HubSpot retired its legacy app-building flow in 2026 — legacy developer accounts began migrating on March 9, 2026, and legacy public app creation was disabled for all accounts on June 23, 2026. New apps are built on the Projects-based platform; existing apps keep working.
- Webhook subscriptions are app-level, not per-connection: one set, registered manually in your HubSpot app, delivers events for every connected consumer — you cannot vary event coverage per consumer.

> Facts synced from Apideck's connector metadata API — `GET /connector/connectors/hubspot` (`overview` field) is the live, authoritative version.

## When to use this skill

Activate this skill when the user explicitly wants to work with **HubSpot** — for example, "pull contacts in HubSpot" or "sync leads in HubSpot". This skill teaches the agent:

1. Which Apideck unified API covers HubSpot (CRM)
2. The correct `serviceId` to pass on every call (`hubspot`)
3. HubSpot-specific auth and coverage caveats

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

// List contacts in HubSpot
const { data } = await apideck.crm.contacts.list({
  serviceId: "hubspot",
});
```

## Portable across 21 CRM connectors

The Apideck **CRM** unified API exposes the same methods for every connector in its catalog. Switching from HubSpot to another CRM connector is a one-string change — no rewrite, no new SDK.

```typescript
// Today — HubSpot
await apideck.crm.contacts.list({ serviceId: "hubspot" });

// Tomorrow — same code, different connector
await apideck.crm.contacts.list({ serviceId: "odoo" });
await apideck.crm.contacts.list({ serviceId: "salesforce" });
```

This is the compounding advantage of using Apideck over integrating HubSpot directly: code against the unified CRM API once, gain access to every connector in it. New connectors Apideck adds become available to your app without code changes.

## HubSpot via Apideck CRM

HubSpot is Apideck's most-installed SMB CRM connector. Strong coverage for contacts, companies, deals (opportunities), and activities.

### Entity mapping

| HubSpot entity | Apideck CRM resource |
|---|---|
| Contact | `contacts` |
| Company | `companies` |
| Deal | `opportunities` |
| Engagement (email, call, meeting, note, task) | `activities` / `notes` |
| Pipeline / Deal Stage | `pipelines` |
| Owner | `users` |
| Custom properties | `custom_fields[]` |
| Lists (static/dynamic) | not in unified API — use Proxy |

### Coverage highlights

- ✅ Full CRUD on contacts, companies, deals
- ✅ Activity engagements (reads and writes)
- ✅ Custom properties surfaced as `custom_fields[]`
- ✅ Associations (contact → company, deal → contact) exposed as ID references
- ⚠️ HubSpot Marketing Hub (forms, workflows, campaigns) — not in CRM unified; use Proxy
- ❌ HubSpot Lists API — use Proxy with `/crm/v3/lists`
- ❌ HubSpot Timeline events — use Proxy

### HubSpot auth notes

- **Type:** OAuth 2.0, managed by Apideck Vault
- **Scopes:** Apideck Vault requests the CRM scopes needed for objects and associations. Exact scope set is configured in the Vault app.
- **Portal binding:** each connection is bound to one HubSpot portal (`hubId`). Multi-portal = multi-connection.
- **API limits:** HubSpot enforces per-portal daily and 10-second burst limits. Apideck respects 429 with backoff.

### Example: list open deals with pipeline and owner

```typescript
const { data } = await apideck.crm.opportunities.list({
  serviceId: "hubspot",
  filter: { status: "open" },
  fields: "id,name,amount,close_date,pipeline,owner_id,company_id",
});
```

### Example: create a contact with associations

```typescript
const { data } = await apideck.crm.contacts.create({
  serviceId: "hubspot",
  contact: {
    first_name: "Alex",
    last_name: "Rivera",
    emails: [{ email: "alex@example.com", type: "primary" }],
    company_id: "hs_company_123",
  },
});
```

## Escape hatch: Proxy API

When an endpoint isn't covered by the CRM unified API, use Apideck's Proxy to call HubSpot directly — Apideck injects auth headers and handles token refresh. Set `x-apideck-downstream-url` to the target endpoint on HubSpot's own API:

```bash
curl 'https://unify.apideck.com/proxy' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}" \
  -H "x-apideck-consumer-id: ${CONSUMER_ID}" \
  -H "x-apideck-service-id: hubspot" \
  -H "x-apideck-downstream-url: <target endpoint on HubSpot>" \
  -H "x-apideck-downstream-method: GET"
```

See [HubSpot's API docs](https://developers.hubspot.com) for available endpoints.

## Sibling connectors

Other **CRM** connectors that share this unified API surface (same method signatures, just change `serviceId`):

[`odoo`](../odoo/) *(beta)*, [`salesforce`](../salesforce/), [`pipedrive`](../pipedrive/), [`zoho-crm`](../zoho-crm/), [`activecampaign`](../activecampaign/), [`close`](../close/), [`microsoft-dynamics`](../microsoft-dynamics/), [`teamleader`](../teamleader/), and 12 more.

## See also

- [CRM OpenAPI spec](https://specs.apideck.com/crm.yml) · [API Explorer](https://developers.apideck.com/api-explorer?id=crm)
- [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) — programmatic coverage checks
- [`apideck-best-practices`](../../skills/apideck-best-practices/) — architecture, Vault, pagination, error handling
- [`apideck-node`](../../skills/apideck-node/) — TypeScript / Node SDK patterns
- [HubSpot official docs](https://developers.hubspot.com)
