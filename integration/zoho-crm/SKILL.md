---
name: zoho-crm
description: |
  Zoho CRM integration via Apideck's CRM unified API — same methods work across every connector in CRM, switch by changing `serviceId`. Use when the user wants to read, write, or search contacts, companies, leads, opportunities, activities, and pipelines in Zoho CRM. Routes through Apideck with serviceId "zoho-crm".
license: Apache-2.0
alwaysApply: false
metadata:
  author: apideck
  version: "1.0.0"
  serviceId: zoho-crm
  unifiedApis: ["crm"]
  authType: oauth2
  tier: "1b"
  verified: true
  difficulty: straightforward
  partnershipRequired: false
  sandboxAvailable: true
---

# Zoho CRM (via Apideck)

Access Zoho CRM through Apideck's **CRM** unified API — one of 21 CRM connectors that share the same method surface. Code you write here ports to Odoo, Salesforce, HubSpot and 17 other CRM connectors by changing a single `serviceId` string. Apideck handles auth, pagination, rate limiting, and retries so you don't write per-tenant Zoho CRM plumbing.

## Quick facts

- **Apideck serviceId:** `zoho-crm`
- **Unified API:** CRM
- **Auth type:** oauth2
- **Gotchas:** [page](https://developers.apideck.com/apis/crm/zoho-crm/gotchas)
- **Zoho CRM docs:** https://www.zoho.com/crm/developer/docs/api/
- **Homepage:** https://www.zoho.com/crm/

## At a glance

- **Implementation difficulty:** straightforward — Self-Service OAuth Client + Free Edition for Testing, No Review or Partnership
- **Vendor partnership required:** no ([Zoho API console](https://api-console.zoho.com/)) — No partner programme and no app review: you register a Server-based client yourself.
- **Apideck-managed credentials:** available — The Zoho consent screen shows "Apideck"; use your own Zoho client in production.
- **Account type required:** Any Zoho CRM edition, including Free
- **Consumer access level:** Any user whose profile has the Zoho CRM API Access permission (Administrators have it by default)
- **Sandbox:** available ([signup](https://www.zoho.com/crm/developer/developer-edition.html)) — A Free edition org for your own testing, or a Developer Edition org by invitation from a sandbox-enabled customer.
- **Costs:** None. Registering a Zoho API client is free and API calls draw on the consumer's own edition credits.
- **Rate limits:** Daily credits per org by edition: 5,000 (Free) to 50,000 plus 250 to 2,000 per user (paid); 5 to 25 concurrent calls; HTTP 429 on excess
- **Authentication:** Authorization Code flow via Zoho Accounts.
- **Webhooks:** No webhooks — Zoho CRM changes are not surfaced as Apideck events; sync by polling the CRM and Lead APIs

**Important to know:**

- Zoho runs nine data centres (US, EU, India, Australia, Japan, China, Canada, Saudi Arabia, UK). Your client needs Multi-DC enabled for every data centre your consumers' accounts live in, or their authorisation fails; the connector detects each consumer's data centre itself.
- Zoho keeps at most 20 refresh tokens per user per client and 15 live access tokens per refresh token: a 21st authorisation by the same user silently invalidates the oldest connection. Refresh tokens otherwise never expire unless revoked.
- Your consumers' other Zoho apps draw on the same daily credit pool as your integration, so a busy organisation can throttle your sync well before its edition's headline limit.
- Zoho's Sandbox feature is included only from the Enterprise edition up, so a consumer on a lower edition has no test copy of their org.

> Facts synced from Apideck's connector metadata API — `GET /connector/connectors/zoho-crm` (`overview` field) is the live, authoritative version.

## When to use this skill

Activate this skill when the user explicitly wants to work with **Zoho CRM** — for example, "pull contacts in Zoho CRM" or "sync leads in Zoho CRM". This skill teaches the agent:

1. Which Apideck unified API covers Zoho CRM (CRM)
2. The correct `serviceId` to pass on every call (`zoho-crm`)
3. Zoho CRM-specific auth and coverage caveats

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

// List contacts in Zoho CRM
const { data } = await apideck.crm.contacts.list({
  serviceId: "zoho-crm",
});
```

## Portable across 21 CRM connectors

The Apideck **CRM** unified API exposes the same methods for every connector in its catalog. Switching from Zoho CRM to another CRM connector is a one-string change — no rewrite, no new SDK.

```typescript
// Today — Zoho CRM
await apideck.crm.contacts.list({ serviceId: "zoho-crm" });

// Tomorrow — same code, different connector
await apideck.crm.contacts.list({ serviceId: "odoo" });
await apideck.crm.contacts.list({ serviceId: "salesforce" });
```

This is the compounding advantage of using Apideck over integrating Zoho CRM directly: code against the unified CRM API once, gain access to every connector in it. New connectors Apideck adds become available to your app without code changes.

## Zoho CRM via Apideck

Zoho CRM is a popular CRM in the SMB and international market. Apideck covers the core modules.

### Entity mapping

| Zoho CRM module | Apideck CRM resource |
|---|---|
| Contacts | `contacts` |
| Accounts | `companies` |
| Leads | `leads` |
| Deals | `opportunities` |
| Tasks, Events, Calls | `activities` |
| Notes | `notes` |
| Pipeline / Stage | `pipelines` |
| Custom modules | use Proxy |

### Coverage highlights

- ✅ Full CRUD on contacts, accounts, leads, deals
- ✅ Activities (tasks, events, calls) as unified `activities`
- ⚠️ Custom modules and custom layouts — not in unified; use Proxy
- ❌ Zoho CRM Plus (analytics, projects) — separate products; not covered here

### Auth

- **Type:** OAuth 2.0, managed by Apideck Vault
- **Data center:** Zoho is region-sharded (US, EU, IN, AU, CN, JP). The user's data center is determined during OAuth. If writes hit a "wrong DC" error, the connection needs re-authorization.
- **API limits:** Zoho enforces per-org credit-based rate limits. Apideck backs off on 429.

### Example: list deals sorted by close date

```typescript
const { data } = await apideck.crm.opportunities.list({
  serviceId: "zoho-crm",
  sort: { by: "close_date", direction: "asc" },
});
```

## Escape hatch: Proxy API

When an endpoint isn't covered by the CRM unified API, use Apideck's Proxy to call Zoho CRM directly — Apideck injects auth headers and handles token refresh. Set `x-apideck-downstream-url` to the target endpoint on Zoho CRM's own API:

```bash
curl 'https://unify.apideck.com/proxy' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}" \
  -H "x-apideck-consumer-id: ${CONSUMER_ID}" \
  -H "x-apideck-service-id: zoho-crm" \
  -H "x-apideck-downstream-url: <target endpoint on Zoho CRM>" \
  -H "x-apideck-downstream-method: GET"
```

See [Zoho CRM's API docs](https://www.zoho.com/crm/developer/docs/api/) for available endpoints.

## Sibling connectors

Other **CRM** connectors that share this unified API surface (same method signatures, just change `serviceId`):

[`odoo`](../odoo/) *(beta)*, [`salesforce`](../salesforce/), [`hubspot`](../hubspot/), [`pipedrive`](../pipedrive/), [`activecampaign`](../activecampaign/), [`close`](../close/), [`microsoft-dynamics`](../microsoft-dynamics/), [`teamleader`](../teamleader/), and 12 more.

## See also

- [CRM OpenAPI spec](https://specs.apideck.com/crm.yml) · [API Explorer](https://developers.apideck.com/api-explorer?id=crm)
- [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) — programmatic coverage checks
- [`apideck-best-practices`](../../skills/apideck-best-practices/) — architecture, Vault, pagination, error handling
- [`apideck-node`](../../skills/apideck-node/) — TypeScript / Node SDK patterns
- [Zoho CRM official docs](https://www.zoho.com/crm/developer/docs/api/)
