---
name: flexmail
description: |
  Flexmail integration via Apideck's CRM unified API — same methods work across every connector in CRM, switch by changing `serviceId`. Use when the user wants to read, write, or search contacts, companies, leads, opportunities, activities, and pipelines in Flexmail. Routes through Apideck with serviceId "flexmail".
license: Apache-2.0
alwaysApply: false
metadata:
  author: apideck
  version: "1.0.0"
  serviceId: flexmail
  unifiedApis: ["crm"]
  authType: basic
  tier: "2"
  verified: true
  difficulty: moderate
  partnershipRequired: false
  sandboxAvailable: true
---

# Flexmail (via Apideck)

Access Flexmail through Apideck's **CRM** unified API — one of 21 CRM connectors that share the same method surface. Code you write here ports to Odoo, Salesforce, HubSpot and 17 other CRM connectors by changing a single `serviceId` string. Apideck handles auth, pagination, rate limiting, and retries so you don't write per-tenant Flexmail plumbing.

## Quick facts

- **Apideck serviceId:** `flexmail`
- **Unified API:** CRM
- **Auth type:** basic
- **Gotchas:** [page](https://developers.apideck.com/apis/crm/flexmail/gotchas)
- **Flexmail docs:** https://help.flexmail.eu
- **Homepage:** https://flexmail.be

## At a glance

- **Implementation difficulty:** moderate — Personal Access Token Authentication - Each Consumer Creates Their Own Token in Flexmail
- **Vendor partnership required:** no — Nothing has to be registered with Flexmail to use this connector.
- **Apideck-managed credentials:** not available — Flexmail has no app to register or share; each consumer connects their own account.
- **Account type required:** Flexmail account on a plan that includes API access.
- **Consumer access level:** A Flexmail user who can create personal access tokens in Settings.
- **Sandbox:** available ([signup](https://flexmail.be/en/signup)) — Free 30-day trial account with Pro features, the API and up to 1,000 contacts.
- **Costs:** API calls are included in Flexmail plans, up to a monthly API request cap set by plan.
- **Rate limits:** 60 requests per minute for each account, client IP address and endpoint.
- **Authentication:** Account ID as the username and a personal access token as the password.
- **Webhooks:** No webhooks - poll for changes.

**Important to know:**

- Flexmail has no built-in company field. Company name is read and written through a custom field each consumer selects when connecting, separately for contacts and leads, so that custom field must exist in their Flexmail account first.

> Facts synced from Apideck's connector metadata API — `GET /connector/connectors/flexmail` (`overview` field) is the live, authoritative version.

## When to use this skill

Activate this skill when the user explicitly wants to work with **Flexmail** — for example, "pull contacts in Flexmail" or "sync leads in Flexmail". This skill teaches the agent:

1. Which Apideck unified API covers Flexmail (CRM)
2. The correct `serviceId` to pass on every call (`flexmail`)
3. Flexmail-specific auth and coverage caveats

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

// List contacts in Flexmail
const { data } = await apideck.crm.contacts.list({
  serviceId: "flexmail",
});
```

## Portable across 21 CRM connectors

The Apideck **CRM** unified API exposes the same methods for every connector in its catalog. Switching from Flexmail to another CRM connector is a one-string change — no rewrite, no new SDK.

```typescript
// Today — Flexmail
await apideck.crm.contacts.list({ serviceId: "flexmail" });

// Tomorrow — same code, different connector
await apideck.crm.contacts.list({ serviceId: "odoo" });
await apideck.crm.contacts.list({ serviceId: "salesforce" });
```

This is the compounding advantage of using Apideck over integrating Flexmail directly: code against the unified CRM API once, gain access to every connector in it. New connectors Apideck adds become available to your app without code changes.

## Authentication

- **Type:** Basic auth (username/password)
- **Managed by:** Apideck Vault — credentials are collected through the Vault modal and stored encrypted server-side.
- **Note:** basic auth connectors often require manual rotation by the end user. If auth fails persistently, prompt them to re-enter credentials in Vault.

See [`apideck-best-practices`](../../skills/apideck-best-practices/) for Vault setup, connection lifecycle, and handling re-auth flows.

## Verifying coverage

Not every CRM operation is supported by every connector. Always verify before assuming a method works:

```bash
curl 'https://unify.apideck.com/connector/connectors/flexmail' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}"
```

See [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) for patterns around `UnsupportedOperationError` and connector-specific fallbacks.

## Escape hatch: Proxy API

When an endpoint isn't covered by the CRM unified API, use Apideck's Proxy to call Flexmail directly — Apideck injects auth headers and handles token refresh. Set `x-apideck-downstream-url` to the target endpoint on Flexmail's own API:

```bash
curl 'https://unify.apideck.com/proxy' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}" \
  -H "x-apideck-consumer-id: ${CONSUMER_ID}" \
  -H "x-apideck-service-id: flexmail" \
  -H "x-apideck-downstream-url: <target endpoint on Flexmail>" \
  -H "x-apideck-downstream-method: GET"
```

See [Flexmail's API docs](https://help.flexmail.eu) for available endpoints.

## Sibling connectors

Other **CRM** connectors that share this unified API surface (same method signatures, just change `serviceId`):

[`odoo`](../odoo/) *(beta)*, [`salesforce`](../salesforce/), [`hubspot`](../hubspot/), [`pipedrive`](../pipedrive/), [`zoho-crm`](../zoho-crm/), [`activecampaign`](../activecampaign/), [`close`](../close/), [`microsoft-dynamics`](../microsoft-dynamics/), and 12 more.

## See also

- [CRM OpenAPI spec](https://specs.apideck.com/crm.yml) · [API Explorer](https://developers.apideck.com/api-explorer?id=crm)
- [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) — programmatic coverage checks
- [`apideck-best-practices`](../../skills/apideck-best-practices/) — architecture, Vault, pagination, error handling
- [`apideck-node`](../../skills/apideck-node/) — TypeScript / Node SDK patterns
- [Flexmail official docs](https://help.flexmail.eu)
