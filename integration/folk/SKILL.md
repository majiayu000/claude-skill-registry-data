---
name: folk
description: |
  Folk integration via Apideck's CRM unified API — same methods work across every connector in CRM, switch by changing `serviceId`. Use when the user wants to read, write, or search contacts, companies, leads, opportunities, activities, and pipelines in Folk. Routes through Apideck with serviceId "folk".
license: Apache-2.0
alwaysApply: false
metadata:
  author: apideck
  version: "1.0.0"
  serviceId: folk
  unifiedApis: ["crm"]
  authType: apiKey
  tier: "2"
  verified: true
  status: beta
  difficulty: moderate
  partnershipRequired: false
  sandboxAvailable: false
---

# Folk (via Apideck)

Access Folk through Apideck's **CRM** unified API — one of 21 CRM connectors that share the same method surface. Code you write here ports to Odoo, Salesforce, HubSpot and 17 other CRM connectors by changing a single `serviceId` string. Apideck handles auth, pagination, rate limiting, and retries so you don't write per-tenant Folk plumbing.

> **Beta connector.** Folk is currently in beta on Apideck. Expect partial resource coverage and occasional mapping gaps. Always verify coverage (see below) and fall back to the Proxy API for unsupported operations.

## Quick facts

- **Apideck serviceId:** `folk`
- **Unified API:** CRM
- **Auth type:** apiKey
- **Status:** beta
- **Apideck setup guide:** [Connection guide](https://developers.apideck.com/connectors/folk/docs/consumer+connection)
- **Gotchas:** [page](https://developers.apideck.com/apis/crm/folk/gotchas)
- **Folk docs:** https://developer.folk.app
- **Homepage:** https://www.folk.app/

## At a glance

- **Implementation difficulty:** moderate — API Key Authentication - Each Consumer Creates Their Own Key in Folk
- **Vendor partnership required:** no — Folk has no developer programme to join and no application review.
- **Apideck-managed credentials:** not available — Each consumer supplies their own Folk API key.
- **Account type required:** Folk workspace on the Premium plan.
- **Consumer access level:** Any workspace member can create an API key. Workspace admins can see every key that exists in the workspace.
- **Sandbox:** not available — A new workspace starts on a two-week trial that includes the Premium features and the API; there is no separate test environment.
- **Costs:** Premium costs $48 for each member a month billed yearly, or $60 billed monthly. Prices as at June 2026.
- **Rate limits:** 600 requests a minute. Folk applies the limit to the member who owns the key, so several keys belonging to one person share one budget.
- **Authentication:** Sent as a bearer token; not OAuth.
- **Webhooks:** Native (contact, company and note events for create, update and delete).

**Important to know:**

- An API key belongs to the member who created it: Folk states that when a member is removed from a workspace, the integrations they set up stop working, and documents no way to hand a key over. Restoring it means pasting a new key from somebody still in the workspace.
- Folk sets no expiry on a healthy webhook subscription, but it switches off one whose deliveries keep failing and emails the workspace about it. Reconnecting in Vault is what restores delivery.

> Facts synced from Apideck's connector metadata API — `GET /connector/connectors/folk` (`overview` field) is the live, authoritative version.

## When to use this skill

Activate this skill when the user explicitly wants to work with **Folk** — for example, "pull contacts in Folk" or "sync leads in Folk". This skill teaches the agent:

1. Which Apideck unified API covers Folk (CRM)
2. The correct `serviceId` to pass on every call (`folk`)
3. Folk-specific auth and coverage caveats

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

// List contacts in Folk
const { data } = await apideck.crm.contacts.list({
  serviceId: "folk",
});
```

## Portable across 21 CRM connectors

The Apideck **CRM** unified API exposes the same methods for every connector in its catalog. Switching from Folk to another CRM connector is a one-string change — no rewrite, no new SDK.

```typescript
// Today — Folk
await apideck.crm.contacts.list({ serviceId: "folk" });

// Tomorrow — same code, different connector
await apideck.crm.contacts.list({ serviceId: "odoo" });
await apideck.crm.contacts.list({ serviceId: "salesforce" });
```

This is the compounding advantage of using Apideck over integrating Folk directly: code against the unified CRM API once, gain access to every connector in it. New connectors Apideck adds become available to your app without code changes.

## Authentication

- **Type:** API Key
- **Managed by:** Apideck Vault — the user pastes their Folk API key into the Vault modal; Apideck stores it encrypted and injects it on every request.
- **Rotation:** if the user rotates their key, they re-enter it in Vault. No code changes needed.

**Setup guide:** Apideck publishes a step-by-step guide for registering an OAuth app / configuring credentials for Folk — see [https://developers.apideck.com/connectors/folk/docs/consumer+connection](https://developers.apideck.com/connectors/folk/docs/consumer+connection). Use that as the authoritative source when walking users through connection setup.

See [`apideck-best-practices`](../../skills/apideck-best-practices/) for Vault setup, connection lifecycle, and handling re-auth flows.

## Verifying coverage

Not every CRM operation is supported by every connector. Always verify before assuming a method works:

```bash
curl 'https://unify.apideck.com/connector/connectors/folk' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}"
```

See [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) for patterns around `UnsupportedOperationError` and connector-specific fallbacks.

## Escape hatch: Proxy API

When an endpoint isn't covered by the CRM unified API, use Apideck's Proxy to call Folk directly — Apideck injects auth headers and handles token refresh. Set `x-apideck-downstream-url` to the target endpoint on Folk's own API:

```bash
curl 'https://unify.apideck.com/proxy' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}" \
  -H "x-apideck-consumer-id: ${CONSUMER_ID}" \
  -H "x-apideck-service-id: folk" \
  -H "x-apideck-downstream-url: <target endpoint on Folk>" \
  -H "x-apideck-downstream-method: GET"
```

See [Folk's API docs](https://developer.folk.app) for available endpoints.

## Sibling connectors

Other **CRM** connectors that share this unified API surface (same method signatures, just change `serviceId`):

[`odoo`](../odoo/) *(beta)*, [`salesforce`](../salesforce/), [`hubspot`](../hubspot/), [`pipedrive`](../pipedrive/), [`zoho-crm`](../zoho-crm/), [`activecampaign`](../activecampaign/), [`close`](../close/), [`microsoft-dynamics`](../microsoft-dynamics/), and 12 more.

## See also

- [Apideck connection guide for Folk](https://developers.apideck.com/connectors/folk/docs/consumer+connection)
- [CRM OpenAPI spec](https://specs.apideck.com/crm.yml) · [API Explorer](https://developers.apideck.com/api-explorer?id=crm)
- [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) — programmatic coverage checks
- [`apideck-best-practices`](../../skills/apideck-best-practices/) — architecture, Vault, pagination, error handling
- [`apideck-node`](../../skills/apideck-node/) — TypeScript / Node SDK patterns
- [Folk official docs](https://developer.folk.app)
