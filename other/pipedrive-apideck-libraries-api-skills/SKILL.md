---
name: pipedrive
description: |
  Pipedrive integration via Apideck's CRM unified API — same methods work across every connector in CRM, switch by changing `serviceId`. Use when the user wants to read, write, or search contacts, companies, leads, opportunities, activities, and pipelines in Pipedrive. Routes through Apideck with serviceId "pipedrive".
license: Apache-2.0
alwaysApply: false
metadata:
  author: apideck
  version: "1.0.0"
  serviceId: pipedrive
  unifiedApis: ["crm"]
  authType: oauth2
  tier: "1b"
  verified: true
---

# Pipedrive (via Apideck)

Access Pipedrive through Apideck's **CRM** unified API — one of 21 CRM connectors that share the same method surface. Code you write here ports to Odoo, Salesforce, HubSpot and 17 other CRM connectors by changing a single `serviceId` string. Apideck handles auth, pagination, rate limiting, and retries so you don't write per-tenant Pipedrive plumbing.

## Quick facts

- **Apideck serviceId:** `pipedrive`
- **Unified API:** CRM
- **Auth type:** oauth2
- **Gotchas:** [page](https://developers.apideck.com/apis/crm/pipedrive/gotchas)
- **Pipedrive docs:** https://developers.pipedrive.com
- **Homepage:** https://www.pipedrive.com/

## When to use this skill

Activate this skill when the user explicitly wants to work with **Pipedrive** — for example, "pull contacts in Pipedrive" or "sync leads in Pipedrive". This skill teaches the agent:

1. Which Apideck unified API covers Pipedrive (CRM)
2. The correct `serviceId` to pass on every call (`pipedrive`)
3. Pipedrive-specific auth and coverage caveats

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

// List contacts in Pipedrive
const { data } = await apideck.crm.contacts.list({
  serviceId: "pipedrive",
});
```

## Portable across 21 CRM connectors

The Apideck **CRM** unified API exposes the same methods for every connector in its catalog. Switching from Pipedrive to another CRM connector is a one-string change — no rewrite, no new SDK.

```typescript
// Today — Pipedrive
await apideck.crm.contacts.list({ serviceId: "pipedrive" });

// Tomorrow — same code, different connector
await apideck.crm.contacts.list({ serviceId: "odoo" });
await apideck.crm.contacts.list({ serviceId: "salesforce" });
```

This is the compounding advantage of using Apideck over integrating Pipedrive directly: code against the unified CRM API once, gain access to every connector in it. New connectors Apideck adds become available to your app without code changes.

## Pipedrive via Apideck CRM

Pipedrive is a sales-pipeline-focused CRM. Apideck maps its deal-centric model to the unified CRM API.

### Entity mapping

| Pipedrive entity | Apideck CRM resource |
|---|---|
| Person | `contacts` |
| Organization | `companies` |
| Deal | `opportunities` |
| Activity | `activities` |
| Note | `notes` |
| Stage / Pipeline | `pipelines` |
| Custom fields | `custom_fields[]` |
| Lead (pre-deal) | `leads` |

### Coverage highlights

- ✅ Full CRUD on persons, organizations, deals, activities
- ✅ Pipeline and stage metadata
- ✅ Custom fields as `custom_fields[]`
- ⚠️ Products (line items on deals) — partial coverage; use Proxy for full product catalog

### Auth

- **Type:** OAuth 2.0, managed by Apideck Vault
- **Company binding:** each connection is bound to one Pipedrive company. Multi-company = multi-connection.
- **API limits:** Pipedrive enforces per-company rate limits; Apideck backs off on 429.

### Example: list deals in a specific pipeline

```typescript
const { data } = await apideck.crm.opportunities.list({
  serviceId: "pipedrive",
  filter: { pipeline_id: "pipeline_1" },
});
```

## Escape hatch: Proxy API

When an endpoint isn't covered by the CRM unified API, use Apideck's Proxy to call Pipedrive directly — Apideck injects auth headers and handles token refresh. Set `x-apideck-downstream-url` to the target endpoint on Pipedrive's own API:

```bash
curl 'https://unify.apideck.com/proxy' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}" \
  -H "x-apideck-consumer-id: ${CONSUMER_ID}" \
  -H "x-apideck-service-id: pipedrive" \
  -H "x-apideck-downstream-url: <target endpoint on Pipedrive>" \
  -H "x-apideck-downstream-method: GET"
```

See [Pipedrive's API docs](https://developers.pipedrive.com) for available endpoints.

## Sibling connectors

Other **CRM** connectors that share this unified API surface (same method signatures, just change `serviceId`):

[`odoo`](../odoo/) *(beta)*, [`salesforce`](../salesforce/), [`hubspot`](../hubspot/), [`zoho-crm`](../zoho-crm/), [`activecampaign`](../activecampaign/), [`close`](../close/), [`microsoft-dynamics`](../microsoft-dynamics/), [`teamleader`](../teamleader/), and 12 more.

## See also

- [CRM OpenAPI spec](https://specs.apideck.com/crm.yml) · [API Explorer](https://developers.apideck.com/api-explorer?id=crm)
- [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) — programmatic coverage checks
- [`apideck-best-practices`](../../skills/apideck-best-practices/) — architecture, Vault, pagination, error handling
- [`apideck-node`](../../skills/apideck-node/) — TypeScript / Node SDK patterns
- [Pipedrive official docs](https://developers.pipedrive.com)
