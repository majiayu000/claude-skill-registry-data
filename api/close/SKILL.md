---
name: close
description: |
  Close integration via Apideck's CRM unified API — same methods work across every connector in CRM, switch by changing `serviceId`. Use when the user wants to read, write, or search contacts, companies, leads, opportunities, activities, and pipelines in Close. Routes through Apideck with serviceId "close".
license: Apache-2.0
alwaysApply: false
metadata:
  author: apideck
  version: "1.0.0"
  serviceId: close
  unifiedApis: ["crm"]
  authType: basic
  tier: "1c"
  verified: true
  difficulty: moderate
  partnershipRequired: false
  sandboxAvailable: true
---

# Close (via Apideck)

Access Close through Apideck's **CRM** unified API — one of 21 CRM connectors that share the same method surface. Code you write here ports to Odoo, Salesforce, HubSpot and 17 other CRM connectors by changing a single `serviceId` string. Apideck handles auth, pagination, rate limiting, and retries so you don't write per-tenant Close plumbing.

## Quick facts

- **Apideck serviceId:** `close`
- **Unified API:** CRM
- **Auth type:** basic
- **Gotchas:** [page](https://developers.apideck.com/apis/crm/close/gotchas)
- **Close docs:** https://developer.close.com
- **Homepage:** https://close.com/

## At a glance

- **Implementation difficulty:** moderate — API Key Authentication - Each Consumer Creates Their Own Key in Close
- **Vendor partnership required:** no
- **Apideck-managed credentials:** not available — Each consumer creates their own Close API key.
- **Account type required:** Any Close account, paid or on trial.
- **Consumer access level:** A Close user who can create an API key in their settings; Close does not name a required role.
- **Sandbox:** available ([signup](https://app.close.com/signup/)) — Test with a free trial account, which runs 14 days and needs no credit card; Close documents no separate sandbox.
- **Costs:** Nothing extra: every Close plan includes API access.
- **Rate limits:** No single published figure; Close limits requests per endpoint group, per organisation and, lower, per API key.
- **Authentication:** Sent as the username in HTTP Basic authentication.
- **Webhooks:** No webhooks - Close events are not delivered to Apideck; data is read by polling the API.

**Important to know:**

- The key acts as the Close user who created it, with that user's full access and no way to narrow it. If that key is deleted, the connection stops working immediately and cannot be undone, so have each consumer create a dedicated key for the integration rather than reusing one.

> Facts synced from Apideck's connector metadata API — `GET /connector/connectors/close` (`overview` field) is the live, authoritative version.

## When to use this skill

Activate this skill when the user explicitly wants to work with **Close** — for example, "pull contacts in Close" or "sync leads in Close". This skill teaches the agent:

1. Which Apideck unified API covers Close (CRM)
2. The correct `serviceId` to pass on every call (`close`)
3. Close-specific auth and coverage caveats

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

// List contacts in Close
const { data } = await apideck.crm.contacts.list({
  serviceId: "close",
});
```

## Portable across 21 CRM connectors

The Apideck **CRM** unified API exposes the same methods for every connector in its catalog. Switching from Close to another CRM connector is a one-string change — no rewrite, no new SDK.

```typescript
// Today — Close
await apideck.crm.contacts.list({ serviceId: "close" });

// Tomorrow — same code, different connector
await apideck.crm.contacts.list({ serviceId: "odoo" });
await apideck.crm.contacts.list({ serviceId: "salesforce" });
```

This is the compounding advantage of using Apideck over integrating Close directly: code against the unified CRM API once, gain access to every connector in it. New connectors Apideck adds become available to your app without code changes.

## Authentication

- **Type:** Basic auth (username/password)
- **Managed by:** Apideck Vault — credentials are collected through the Vault modal and stored encrypted server-side.
- **Note:** basic auth connectors often require manual rotation by the end user. If auth fails persistently, prompt them to re-enter credentials in Vault.

See [`apideck-best-practices`](../../skills/apideck-best-practices/) for Vault setup, connection lifecycle, and handling re-auth flows.

## Verifying coverage

Not every CRM operation is supported by every connector. Always verify before assuming a method works:

```bash
curl 'https://unify.apideck.com/connector/connectors/close' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}"
```

See [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) for patterns around `UnsupportedOperationError` and connector-specific fallbacks.

## Escape hatch: Proxy API

When an endpoint isn't covered by the CRM unified API, use Apideck's Proxy to call Close directly — Apideck injects auth headers and handles token refresh. Set `x-apideck-downstream-url` to the target endpoint on Close's own API:

```bash
curl 'https://unify.apideck.com/proxy' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}" \
  -H "x-apideck-consumer-id: ${CONSUMER_ID}" \
  -H "x-apideck-service-id: close" \
  -H "x-apideck-downstream-url: <target endpoint on Close>" \
  -H "x-apideck-downstream-method: GET"
```

See [Close's API docs](https://developer.close.com) for available endpoints.

## Sibling connectors

Other **CRM** connectors that share this unified API surface (same method signatures, just change `serviceId`):

[`odoo`](../odoo/) *(beta)*, [`salesforce`](../salesforce/), [`hubspot`](../hubspot/), [`pipedrive`](../pipedrive/), [`zoho-crm`](../zoho-crm/), [`activecampaign`](../activecampaign/), [`microsoft-dynamics`](../microsoft-dynamics/), [`teamleader`](../teamleader/), and 12 more.

## See also

- [CRM OpenAPI spec](https://specs.apideck.com/crm.yml) · [API Explorer](https://developers.apideck.com/api-explorer?id=crm)
- [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) — programmatic coverage checks
- [`apideck-best-practices`](../../skills/apideck-best-practices/) — architecture, Vault, pagination, error handling
- [`apideck-node`](../../skills/apideck-node/) — TypeScript / Node SDK patterns
- [Close official docs](https://developer.close.com)
