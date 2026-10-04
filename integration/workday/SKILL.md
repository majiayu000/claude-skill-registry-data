---
name: workday
description: |
  Workday integration via Apideck's Accounting, HRIS, ATS unified API — same methods work across every connector in Accounting, HRIS, ATS, switch by changing `serviceId`. Use when the user wants to read, write, or reconcile invoices, bills, payments, ledger accounts, and journal entries in Workday. Routes through Apideck with serviceId "workday".
license: Apache-2.0
alwaysApply: false
metadata:
  author: apideck
  version: "1.0.0"
  serviceId: workday
  unifiedApis: ["accounting", "hris", "ats"]
  authType: custom
  tier: "1a"
  verified: true
  difficulty: highly_complex
  partnershipRequired: false
  sandboxAvailable: false
---

# Workday (via Apideck)

Access Workday through Apideck's **Accounting, HRIS, ATS** unified API — one of 34 Accounting connectors that share the same method surface. Code you write here ports to Access Financials, Acumatica, banqUP and 30 other Accounting connectors by changing a single `serviceId` string. Apideck handles auth, pagination, rate limiting, and retries so you don't write per-tenant Workday plumbing.

## Quick facts

- **Apideck serviceId:** `workday`
- **Unified APIs:** Accounting, HRIS, ATS
- **Auth type:** custom
- **Apideck setup guide:** [Connection guide](https://developers.apideck.com/connectors/workday/docs/consumer+connection)
- **Gotchas:** [Accounting](https://developers.apideck.com/apis/accounting/workday/gotchas) · [HRIS](https://developers.apideck.com/apis/hris/workday/gotchas) · [ATS](https://developers.apideck.com/apis/ats/workday/gotchas)
- **Workday docs:** https://community.workday.com
- **Homepage:** https://workday.com

## At a glance

- **Implementation difficulty:** highly complex — Custom Auth + Manual Per-Consumer Setup + Complex Permissions
- **Vendor partnership required:** no ([Workday Partner Program](https://www.workday.com/en-us/company/partners/partner-program-overview.html)) — Apideck holds the Workday partnership; joining the Workday Partner Program yourself is optional.
- **Apideck-managed credentials:** not available — Authentication is per consumer rather than per application, so there are no app-level credentials for Apideck to provide.
- **Account type required:** Workday tenant with Web Services access
- **Consumer access level:** Administrator with privileges to create Integration System Users and manage security groups and domain security policies
- **Sandbox:** not available — Testing runs against a consumer's own Workday tenant — no free trial, and Development tenants are contract-gated to existing Workday customers.
- **Costs:** No additional platform fees from Workday.
- **Rate limits:** No published hard limits; Workday throttles under high tenant load.
- **Authentication:** A per-consumer Integration System User (ISU); not OAuth.
- **Webhooks:** Virtual webhooks — no native webhooks in Workday; Apideck polls employees, applicants, jobs, bills, suppliers, purchase orders, and customers.

**Important to know:**

- Permission setup differs per Unified API: the consumer's Workday admin grants domain security policies separately for HRIS (13+), ATS (11+) and Accounting (22+), plus Business Process Security Policy edits before any write succeeds.
- Accounting writes are worktag-gated: invoices and purchase orders reject line items without a cost-center worktag (tracking_categories.id), and journal entries silently fall back to draft without one.
- AP bills cannot be incrementally synced: Workday returns empty updated_at/created_at on Bills and rejects filter[updated_since] with an UnsupportedFiltersError, so plan full re-fetches.

> Facts synced from Apideck's connector metadata API — `GET /connector/connectors/workday` (`overview` field) is the live, authoritative version.

## When to use this skill

Activate this skill when the user explicitly wants to work with **Workday** — for example, "create an invoice in Workday" or "reconcile payments in Workday". This skill teaches the agent:

1. Which Apideck unified API covers Workday (Accounting, HRIS, ATS)
2. The correct `serviceId` to pass on every call (`workday`)
3. Workday-specific auth and coverage caveats

For the full method surface (parameters, pagination, filtering), use your language SDK skill:

- [`apideck-node`](../../skills/apideck-node/), [`apideck-python`](../../skills/apideck-python/), [`apideck-dotnet`](../../skills/apideck-dotnet/), [`apideck-java`](../../skills/apideck-java/), [`apideck-go`](../../skills/apideck-go/), [`apideck-php`](../../skills/apideck-php/), or [`apideck-rest`](../../skills/apideck-rest/)

For the raw OpenAPI spec:

- **Accounting:** [https://specs.apideck.com/accounting.yml](https://specs.apideck.com/accounting.yml) · [API Explorer](https://developers.apideck.com/api-explorer?id=accounting)
- **HRIS:** [https://specs.apideck.com/hris.yml](https://specs.apideck.com/hris.yml) · [API Explorer](https://developers.apideck.com/api-explorer?id=hris)
- **ATS:** [https://specs.apideck.com/ats.yml](https://specs.apideck.com/ats.yml) · [API Explorer](https://developers.apideck.com/api-explorer?id=ats)

## Minimal example (TypeScript)

```typescript
import { Apideck } from "@apideck/unify";

const apideck = new Apideck({
  apiKey: process.env.APIDECK_API_KEY,
  appId: process.env.APIDECK_APP_ID,
  consumerId: "your-consumer-id",
});

// List invoices in Workday
const { data } = await apideck.accounting.invoices.list({
  serviceId: "workday",
});
```

## Portable across 34 Accounting connectors

The Apideck **Accounting** unified API exposes the same methods for every connector in its catalog. Switching from Workday to another Accounting connector is a one-string change — no rewrite, no new SDK.

```typescript
// Today — Workday
await apideck.accounting.invoices.list({ serviceId: "workday" });

// Tomorrow — same code, different connector
await apideck.accounting.invoices.list({ serviceId: "access-financials" });
await apideck.accounting.invoices.list({ serviceId: "acumatica" });
```

This is the compounding advantage of using Apideck over integrating Workday directly: code against the unified Accounting API once, gain access to every connector in it. New connectors Apideck adds become available to your app without code changes.

## Workday via Apideck

Workday is an enterprise cloud platform covering HCM, Finance, and Recruiting. Apideck exposes Workday across **HRIS**, **Accounting**, and **ATS** unified APIs — one of only a handful of multi-API connectors in the catalog.

### Unified API coverage (verified via Connector API)

| Apideck API | Resources mapped | Notes |
|---|---|---|
| Accounting | 20 resources | invoices, bills, journal entries, GL accounts, customers, suppliers, more |
| HRIS | 3 resources | employees + org hierarchy |
| ATS | 2 resources | job requisitions + applicants (limited) |

Always verify current coverage with `GET /connector/connectors/workday`.

### Example: list employees (HRIS)

```typescript
const { data } = await apideck.hris.employees.list({
  serviceId: "workday",
});
```

### Example: list invoices (Accounting)

```typescript
const { data } = await apideck.accounting.invoices.list({
  serviceId: "workday",
});
```

### Example: list job requisitions (ATS)

```typescript
const { data } = await apideck.ats.jobs.list({
  serviceId: "workday",
});
```

### Auth notes

- **Type:** OAuth 2.0, managed by Apideck Vault
- **Tenant binding:** each connection is bound to one Workday tenant. Module access (HCM, Financials, Recruiting) depends on what's licensed in that tenant — a Financials-only tenant won't expose HRIS or ATS data regardless of Apideck setup.
- **Integration System User (ISU) required:** Workday access goes through a dedicated ISU account with scoped permissions, set up by the customer's Workday admin. Apideck cannot provision this; the user must coordinate with their admin before connection will work. Expect 1–2 weeks lead time for enterprise Workday onboarding.

## Verifying coverage

Not every Accounting operation is supported by every connector. Always verify before assuming a method works:

```bash
curl 'https://unify.apideck.com/connector/connectors/workday' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}"
```

See [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) for patterns around `UnsupportedOperationError` and connector-specific fallbacks.

## Escape hatch: Proxy API

When an endpoint isn't covered by the Accounting unified API, use Apideck's Proxy to call Workday directly — Apideck injects auth headers and handles token refresh. Set `x-apideck-downstream-url` to the target endpoint on Workday's own API:

```bash
curl 'https://unify.apideck.com/proxy' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}" \
  -H "x-apideck-consumer-id: ${CONSUMER_ID}" \
  -H "x-apideck-service-id: workday" \
  -H "x-apideck-downstream-url: <target endpoint on Workday>" \
  -H "x-apideck-downstream-method: GET"
```

See [Workday's API docs](https://community.workday.com) for available endpoints.

## Sibling connectors

Other **Accounting** connectors that share this unified API surface (same method signatures, just change `serviceId`):

[`access-financials`](../access-financials/) *(beta)*, [`acumatica`](../acumatica/) *(beta)*, [`banqup`](../banqup/) *(beta)*, [`campfire`](../campfire/) *(beta)*, [`clearbooks-uk`](../clearbooks-uk/) *(beta)*, [`digits`](../digits/) *(beta)*, [`dualentry`](../dualentry/), [`exact-online`](../exact-online/), and 25 more.

Other **HRIS** connectors that share this unified API surface (same method signatures, just change `serviceId`):

[`bamboohr`](../bamboohr/), [`deel`](../deel/) *(beta)*, [`hibob`](../hibob/), [`personio`](../personio/), [`adp-ihcm`](../adp-ihcm/) *(beta)*, [`adp-workforce-now`](../adp-workforce-now/) *(beta)*, [`paychex`](../paychex/) *(beta)*, [`paylocity`](../paylocity/), and 49 more.

Other **ATS** connectors that share this unified API surface (same method signatures, just change `serviceId`):

[`greenhouse`](../greenhouse/), [`lever`](../lever/), [`workable`](../workable/) *(beta)*, [`bullhorn-ats`](../bullhorn-ats/) *(beta)*, [`teamtailor`](../teamtailor/) *(beta)*, [`freshteam`](../freshteam/), [`jobadder`](../jobadder/) *(beta)*, [`recruitee`](../recruitee/), and 2 more.

## See also

- [Apideck connection guide for Workday](https://developers.apideck.com/connectors/workday/docs/consumer+connection)
- [Accounting OpenAPI spec](https://specs.apideck.com/accounting.yml) · [API Explorer](https://developers.apideck.com/api-explorer?id=accounting)
- [HRIS OpenAPI spec](https://specs.apideck.com/hris.yml) · [API Explorer](https://developers.apideck.com/api-explorer?id=hris)
- [ATS OpenAPI spec](https://specs.apideck.com/ats.yml) · [API Explorer](https://developers.apideck.com/api-explorer?id=ats)
- [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) — programmatic coverage checks
- [`apideck-best-practices`](../../skills/apideck-best-practices/) — architecture, Vault, pagination, error handling
- [`apideck-node`](../../skills/apideck-node/) — TypeScript / Node SDK patterns
- [Workday official docs](https://community.workday.com)
