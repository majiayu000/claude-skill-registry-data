---
name: odoo
description: |
  Odoo integration via Apideck's CRM, Accounting unified API — same methods work across every connector in CRM, Accounting, switch by changing `serviceId`. Use when the user wants to read, write, or search contacts, companies, leads, opportunities, activities, and pipelines in Odoo. Routes through Apideck with serviceId "odoo".
license: Apache-2.0
alwaysApply: false
metadata:
  author: apideck
  version: "1.0.0"
  serviceId: odoo
  unifiedApis: ["crm", "accounting"]
  authType: basic
  tier: "1a"
  verified: true
  status: beta
  difficulty: moderate
  partnershipRequired: false
  sandboxAvailable: true
---

# Odoo (via Apideck)

Access Odoo through Apideck's **CRM, Accounting** unified API — one of 21 CRM connectors that share the same method surface. Code you write here ports to Salesforce, HubSpot, Pipedrive and 17 other CRM connectors by changing a single `serviceId` string. Apideck handles auth, pagination, rate limiting, and retries so you don't write per-tenant Odoo plumbing.

> **Beta connector.** Odoo is currently in beta on Apideck. Expect partial resource coverage and occasional mapping gaps. Always verify coverage (see below) and fall back to the Proxy API for unsupported operations.

## Quick facts

- **Apideck serviceId:** `odoo`
- **Unified APIs:** CRM, Accounting
- **Auth type:** basic
- **Status:** beta
- **Apideck setup guide:** [Connection guide](https://developers.apideck.com/connectors/odoo/docs/consumer+connection)
- **Gotchas:** [CRM](https://developers.apideck.com/apis/crm/odoo/gotchas) · [Accounting](https://developers.apideck.com/apis/accounting/odoo/gotchas)
- **Odoo docs:** https://www.odoo.com/documentation/
- **Homepage:** https://www.odoo.com/

## At a glance

- **Implementation difficulty:** moderate — API Key Authentication — Consumers Create Credentials Manually
- **Vendor partnership required:** no
- **Apideck-managed credentials:** not available — Odoo has no OAuth app concept; every consumer connects with their own Odoo instance and their own API key.
- **Account type required:** Odoo 14+ (Community or Enterprise); some resources need Enterprise-only modules (e.g. account_accountant for bank feeds/tracking categories)
- **Consumer access level:** Admin, or a user with permissions to generate an API key from their own Account Security preferences
- **Sandbox:** available ([signup](https://demo.odoo.com)) — Free, no-signup scratch database from demo.odoo.com; its /start call returns host, db, user and password (External API reference). Outside Odoo Online plans.
- **Costs:** No developer-side cost. Odoo Online requires the paid Custom plan; Odoo.sh/self-hosted (incl. free Community) have no plan restriction.
- **Rate limits:** No published numeric limit. Odoo's Acceptable Use Policy guideline: ~1 call/second, no parallel calls.
- **Authentication:** A manually generated API key over HTTP Basic; not OAuth.
- **Webhooks:** Virtual webhooks — created/updated events across CRM and Accounting resources.

**Important to know:**

- Odoo Online (SaaS) gates the External API to the Custom plan — consumers on One App Free or Standard cannot connect at all. Odoo.sh and self-hosted instances (including free Community) have no such restriction.
- Resource availability depends on installed Odoo modules — a missing module fails only that resource (e.g. Purchase Orders needs the Purchase module).
- A connection is scoped to one Odoo company: the API user's default company. Consumers with multiple companies need one connection per company, each using a user whose default company differs.

> Facts synced from Apideck's connector metadata API — `GET /connector/connectors/odoo` (`overview` field) is the live, authoritative version.

## When to use this skill

Activate this skill when the user explicitly wants to work with **Odoo** — for example, "pull contacts in Odoo" or "sync leads in Odoo". This skill teaches the agent:

1. Which Apideck unified API covers Odoo (CRM, Accounting)
2. The correct `serviceId` to pass on every call (`odoo`)
3. Odoo-specific auth and coverage caveats

For the full method surface (parameters, pagination, filtering), use your language SDK skill:

- [`apideck-node`](../../skills/apideck-node/), [`apideck-python`](../../skills/apideck-python/), [`apideck-dotnet`](../../skills/apideck-dotnet/), [`apideck-java`](../../skills/apideck-java/), [`apideck-go`](../../skills/apideck-go/), [`apideck-php`](../../skills/apideck-php/), or [`apideck-rest`](../../skills/apideck-rest/)

For the raw OpenAPI spec:

- **CRM:** [https://specs.apideck.com/crm.yml](https://specs.apideck.com/crm.yml) · [API Explorer](https://developers.apideck.com/api-explorer?id=crm)
- **Accounting:** [https://specs.apideck.com/accounting.yml](https://specs.apideck.com/accounting.yml) · [API Explorer](https://developers.apideck.com/api-explorer?id=accounting)

## Minimal example (TypeScript)

```typescript
import { Apideck } from "@apideck/unify";

const apideck = new Apideck({
  apiKey: process.env.APIDECK_API_KEY,
  appId: process.env.APIDECK_APP_ID,
  consumerId: "your-consumer-id",
});

// List contacts in Odoo
const { data } = await apideck.crm.contacts.list({
  serviceId: "odoo",
});
```

## Portable across 21 CRM connectors

The Apideck **CRM** unified API exposes the same methods for every connector in its catalog. Switching from Odoo to another CRM connector is a one-string change — no rewrite, no new SDK.

```typescript
// Today — Odoo
await apideck.crm.contacts.list({ serviceId: "odoo" });

// Tomorrow — same code, different connector
await apideck.crm.contacts.list({ serviceId: "salesforce" });
await apideck.crm.contacts.list({ serviceId: "hubspot" });
```

This is the compounding advantage of using Apideck over integrating Odoo directly: code against the unified CRM API once, gain access to every connector in it. New connectors Apideck adds become available to your app without code changes.

## Odoo via Apideck Accounting

Odoo is an open-source ERP with cloud (Odoo.com) and self-hosted deployments. Broad module coverage; Apideck targets the Accounting module.

### Entity mapping

| Odoo entity | Apideck Accounting resource |
|---|---|
| Customer Invoice (account.move with type "out_invoice") | `invoices` |
| Vendor Bill (account.move with type "in_invoice") | `bills` |
| Payment | `payments` |
| Bill Payment | `bill-payments` |
| Credit Note (refund) | `credit-notes` |
| Journal Item (account.move.line) | `journal-entries` |
| Account (account.account) | `ledger-accounts` |
| Partner (res.partner, customer) | `customers` |
| Partner (res.partner, supplier) | `suppliers` |
| Tax (account.tax) | `tax-rates` |
| Product | `invoice-items` |
| Analytic Account | `tracking-categories` |
| Company (res.company) | `companies`, `subsidiaries` |
| Bank Account | `bank-accounts` |
| Department | `departments` |
| Expense (hr.expense) | `expenses` |

### Coverage highlights

- ✅ Full CRUD on invoices, bills, payments, customers, suppliers
- ✅ Journal entries via account.move lines
- ✅ Analytic accounting (tracking categories)
- ✅ Multi-company (subsidiaries)
- ✅ Bank feeds for reconciliation
- ⚠️ Odoo has many custom modules (Studio, custom fields) — coverage varies per installation; use Proxy for module-specific models
- ❌ Other Odoo modules (Sales, CRM, HR, Manufacturing) — use Proxy or a module-specific connector

### Auth notes

- **Type:** Basic auth (username / API key), managed by Apideck Vault
- **Database binding:** Odoo users belong to one database (dbname). Multi-db setups require separate connections.
- **Self-hosted vs cloud:** Apideck connects to any reachable Odoo instance — works for self-hosted provided the URL is accessible.
- **Version sensitivity:** Odoo's model may change across versions (17 → 18 → 19). Apideck abstracts common operations; custom model access via Proxy.

### Example: list customer invoices

```typescript
const { data } = await apideck.accounting.invoices.list({
  serviceId: "odoo",
  filter: { status: "open" },
});
```

### Example: read custom Odoo model via Proxy

```bash
curl 'https://unify.apideck.com/proxy' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}" \
  -H "x-apideck-consumer-id: ${CONSUMER_ID}" \
  -H "x-apideck-service-id: odoo" \
  -H "x-apideck-downstream-url: /jsonrpc" \
  -H "x-apideck-downstream-method: POST"
```

## Sibling connectors

Other **CRM** connectors that share this unified API surface (same method signatures, just change `serviceId`):

[`salesforce`](../salesforce/), [`hubspot`](../hubspot/), [`pipedrive`](../pipedrive/), [`zoho-crm`](../zoho-crm/), [`activecampaign`](../activecampaign/), [`close`](../close/), [`microsoft-dynamics`](../microsoft-dynamics/), [`teamleader`](../teamleader/), and 12 more.

Other **Accounting** connectors that share this unified API surface (same method signatures, just change `serviceId`):

[`access-financials`](../access-financials/) *(beta)*, [`acumatica`](../acumatica/) *(beta)*, [`banqup`](../banqup/) *(beta)*, [`campfire`](../campfire/) *(beta)*, [`clearbooks-uk`](../clearbooks-uk/) *(beta)*, [`digits`](../digits/) *(beta)*, [`dualentry`](../dualentry/), [`exact-online`](../exact-online/), and 25 more.

## See also

- [Apideck connection guide for Odoo](https://developers.apideck.com/connectors/odoo/docs/consumer+connection)
- [CRM OpenAPI spec](https://specs.apideck.com/crm.yml) · [API Explorer](https://developers.apideck.com/api-explorer?id=crm)
- [Accounting OpenAPI spec](https://specs.apideck.com/accounting.yml) · [API Explorer](https://developers.apideck.com/api-explorer?id=accounting)
- [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) — programmatic coverage checks
- [`apideck-best-practices`](../../skills/apideck-best-practices/) — architecture, Vault, pagination, error handling
- [`apideck-node`](../../skills/apideck-node/) — TypeScript / Node SDK patterns
- [Odoo official docs](https://www.odoo.com/documentation/)
