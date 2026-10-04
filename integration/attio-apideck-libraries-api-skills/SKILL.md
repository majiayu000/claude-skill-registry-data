---
name: attio
description: |
  Attio integration via Apideck's CRM unified API — same methods work across every connector in CRM, switch by changing `serviceId`. Use when the user wants to read, write, or search contacts, companies, leads, opportunities, activities, and pipelines in Attio. Routes through Apideck with serviceId "attio".
license: Apache-2.0
alwaysApply: false
metadata:
  author: apideck
  version: "1.0.0"
  serviceId: attio
  unifiedApis: ["crm"]
  authType: oauth2
  tier: "2"
  verified: true
  status: beta
  difficulty: straightforward
  partnershipRequired: false
  sandboxAvailable: true
---

# Attio (via Apideck)

Access Attio through Apideck's **CRM** unified API — one of 21 CRM connectors that share the same method surface. Code you write here ports to Odoo, Salesforce, HubSpot and 17 other CRM connectors by changing a single `serviceId` string. Apideck handles auth, pagination, rate limiting, and retries so you don't write per-tenant Attio plumbing.

> **Beta connector.** Attio is currently in beta on Apideck. Expect partial resource coverage and occasional mapping gaps. Always verify coverage (see below) and fall back to the Proxy API for unsupported operations.

## Quick facts

- **Apideck serviceId:** `attio`
- **Unified API:** CRM
- **Auth type:** oauth2
- **Status:** beta
- **Gotchas:** [page](https://developers.apideck.com/apis/crm/attio/gotchas)
- **Attio docs:** https://developers.attio.com
- **Homepage:** https://attio.com/

## At a glance

- **Implementation difficulty:** straightforward — Self-Service OAuth + Free Plan, No Partnership or App Review Required
- **Vendor partnership required:** no
- **Apideck-managed credentials:** available — For testing: the consent screen shows Apideck; production needs your own Attio app.
- **Account type required:** Any Attio workspace, including the Free plan.
- **Consumer access level:** Workspace admin; a non-admin can only send an install request for an admin to approve.
- **Sandbox:** available ([signup](https://app.attio.com/welcome/sign-in)) — Test in a free workspace or a 14-day Pro trial; Attio support also provides development workspaces on request.
- **Costs:** No API add-on or fee is listed by Attio.
- **Rate limits:** 100 requests per second for reads and 25 per second for writes, across the whole API.
- **Authentication:** Authorization Code flow.
- **Webhooks:** Native - company, contact, opportunity, user and note events (created, updated, deleted)

**Important to know:**

- The connection acts as the whole workspace, not as the person who connects. Attio workspace-level tokens are independent of any one member, so what the integration can see is set by the app's scopes rather than that person's own permissions.

> Facts synced from Apideck's connector metadata API — `GET /connector/connectors/attio` (`overview` field) is the live, authoritative version.

## When to use this skill

Activate this skill when the user explicitly wants to work with **Attio** — for example, "pull contacts in Attio" or "sync leads in Attio". This skill teaches the agent:

1. Which Apideck unified API covers Attio (CRM)
2. The correct `serviceId` to pass on every call (`attio`)
3. Attio-specific auth and coverage caveats

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

// List contacts in Attio
const { data } = await apideck.crm.contacts.list({
  serviceId: "attio",
});
```

## Portable across 21 CRM connectors

The Apideck **CRM** unified API exposes the same methods for every connector in its catalog. Switching from Attio to another CRM connector is a one-string change — no rewrite, no new SDK.

```typescript
// Today — Attio
await apideck.crm.contacts.list({ serviceId: "attio" });

// Tomorrow — same code, different connector
await apideck.crm.contacts.list({ serviceId: "odoo" });
await apideck.crm.contacts.list({ serviceId: "salesforce" });
```

This is the compounding advantage of using Apideck over integrating Attio directly: code against the unified CRM API once, gain access to every connector in it. New connectors Apideck adds become available to your app without code changes.

## Authentication

- **Type:** OAuth 2.0
- **Managed by:** Apideck Vault — Apideck handles the full OAuth dance (authorization code flow, token exchange, refresh). Never ask the user for API keys or tokens directly.
- **User setup:** Users authorize via the Vault modal. Connection state progresses `available → added → authorized → callable`.
- **Token refresh:** automatic. Expired tokens are refreshed transparently on the next API call.

See [`apideck-best-practices`](../../skills/apideck-best-practices/) for Vault setup, connection lifecycle, and handling re-auth flows.

## Verifying coverage

Not every CRM operation is supported by every connector. Always verify before assuming a method works:

```bash
curl 'https://unify.apideck.com/connector/connectors/attio' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}"
```

See [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) for patterns around `UnsupportedOperationError` and connector-specific fallbacks.

## Escape hatch: Proxy API

When an endpoint isn't covered by the CRM unified API, use Apideck's Proxy to call Attio directly — Apideck injects auth headers and handles token refresh. Set `x-apideck-downstream-url` to the target endpoint on Attio's own API:

```bash
curl 'https://unify.apideck.com/proxy' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}" \
  -H "x-apideck-consumer-id: ${CONSUMER_ID}" \
  -H "x-apideck-service-id: attio" \
  -H "x-apideck-downstream-url: <target endpoint on Attio>" \
  -H "x-apideck-downstream-method: GET"
```

See [Attio's API docs](https://developers.attio.com) for available endpoints.

## Sibling connectors

Other **CRM** connectors that share this unified API surface (same method signatures, just change `serviceId`):

[`odoo`](../odoo/) *(beta)*, [`salesforce`](../salesforce/), [`hubspot`](../hubspot/), [`pipedrive`](../pipedrive/), [`zoho-crm`](../zoho-crm/), [`activecampaign`](../activecampaign/), [`close`](../close/), [`microsoft-dynamics`](../microsoft-dynamics/), and 12 more.

## See also

- [CRM OpenAPI spec](https://specs.apideck.com/crm.yml) · [API Explorer](https://developers.apideck.com/api-explorer?id=crm)
- [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) — programmatic coverage checks
- [`apideck-best-practices`](../../skills/apideck-best-practices/) — architecture, Vault, pagination, error handling
- [`apideck-node`](../../skills/apideck-node/) — TypeScript / Node SDK patterns
- [Attio official docs](https://developers.attio.com)
