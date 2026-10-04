---
name: deel
description: |
  Deel integration via Apideck's HRIS unified API — same methods work across every connector in HRIS, switch by changing `serviceId`. Use when the user wants to read or sync employees, departments, payrolls, and time-off records in Deel. Routes through Apideck with serviceId "deel".
license: Apache-2.0
alwaysApply: false
metadata:
  author: apideck
  version: "1.0.0"
  serviceId: deel
  unifiedApis: ["hris"]
  authType: oauth2
  tier: "1b"
  verified: true
  status: beta
  difficulty: moderate
  partnershipRequired: true
  sandboxAvailable: true
---

# Deel (via Apideck)

Access Deel through Apideck's **HRIS** unified API — one of 58 HRIS connectors that share the same method surface. Code you write here ports to BambooHR, Workday, Hibob and 54 other HRIS connectors by changing a single `serviceId` string. Apideck handles auth, pagination, rate limiting, and retries so you don't write per-tenant Deel plumbing.

> **Beta connector.** Deel is currently in beta on Apideck. Expect partial resource coverage and occasional mapping gaps. Always verify coverage (see below) and fall back to the Proxy API for unsupported operations.

## Quick facts

- **Apideck serviceId:** `deel`
- **Unified API:** HRIS
- **Auth type:** oauth2
- **Status:** beta
- **Gotchas:** [page](https://developers.apideck.com/apis/hris/deel/gotchas)
- **Deel docs:** https://developer.deel.com
- **Homepage:** https://www.deel.com/

## At a glance

- **Implementation difficulty:** moderate — OAuth App Store Review Required
- **Vendor partnership required:** yes ([developer portal](https://developer.deel.com/api/partners/publishing-to-app-store)) — Once Deel approves your app for its App Store, it is available to all Deel customers and may be promoted as a Deel integration.
- **Apideck-managed credentials:** available — Covers testing against the Deel sandbox only; production needs your own Deel OAuth app.
- **Account type required:** Deel organisation account.
- **Consumer access level:** Org Admin or IT Developer Admin on Deel.
- **Sandbox:** available ([signup](https://developer.deel.com/api/quickstart)) — Self-service from the Developer Center API Sandbox tab after a Deel sign-up, with sample workers and organisations and no cap on test records.
- **Rate limits:** 5 requests per second for each organisation, shared across all its tokens.
- **Authentication:** Authorization Code flow.
- **Webhooks:** Virtual webhooks - employee created, updated and terminated events

**Important to know:**

- While Deel reviews your OAuth app for its App Store, the app stays accessible only to your own organisation, so plan for that review before other Deel organisations need to connect.

> Facts synced from Apideck's connector metadata API — `GET /connector/connectors/deel` (`overview` field) is the live, authoritative version.

## When to use this skill

Activate this skill when the user explicitly wants to work with **Deel** — for example, "sync employees in Deel" or "list time-off requests in Deel". This skill teaches the agent:

1. Which Apideck unified API covers Deel (HRIS)
2. The correct `serviceId` to pass on every call (`deel`)
3. Deel-specific auth and coverage caveats

For the full method surface (parameters, pagination, filtering), use your language SDK skill:

- [`apideck-node`](../../skills/apideck-node/), [`apideck-python`](../../skills/apideck-python/), [`apideck-dotnet`](../../skills/apideck-dotnet/), [`apideck-java`](../../skills/apideck-java/), [`apideck-go`](../../skills/apideck-go/), [`apideck-php`](../../skills/apideck-php/), or [`apideck-rest`](../../skills/apideck-rest/)

For the raw OpenAPI spec:

- **HRIS:** [https://specs.apideck.com/hris.yml](https://specs.apideck.com/hris.yml) · [API Explorer](https://developers.apideck.com/api-explorer?id=hris)

## Minimal example (TypeScript)

```typescript
import { Apideck } from "@apideck/unify";

const apideck = new Apideck({
  apiKey: process.env.APIDECK_API_KEY,
  appId: process.env.APIDECK_APP_ID,
  consumerId: "your-consumer-id",
});

// List employees in Deel
const { data } = await apideck.hris.employees.list({
  serviceId: "deel",
});
```

## Portable across 58 HRIS connectors

The Apideck **HRIS** unified API exposes the same methods for every connector in its catalog. Switching from Deel to another HRIS connector is a one-string change — no rewrite, no new SDK.

```typescript
// Today — Deel
await apideck.hris.employees.list({ serviceId: "deel" });

// Tomorrow — same code, different connector
await apideck.hris.employees.list({ serviceId: "bamboohr" });
await apideck.hris.employees.list({ serviceId: "workday" });
```

This is the compounding advantage of using Apideck over integrating Deel directly: code against the unified HRIS API once, gain access to every connector in it. New connectors Apideck adds become available to your app without code changes.

## Deel via Apideck HRIS

Deel is a global payroll and contractor management platform. Apideck covers the HRIS-adjacent surface (employees, time-off).

### Entity mapping

| Deel entity | Apideck HRIS resource |
|---|---|
| Employee | `employees` (57+ fields surfaced) |
| Contractor | also `employees` (distinguished via `employment_type`) |
| Time Off Request | `time-off-requests` |
| Department | `departments` |
| Company entity | `companies` |
| Payroll runs | ❌ use Proxy |

### Coverage highlights

- ✅ Employee list + details (full- and part-time, contractor)
- ✅ Time-off requests
- ✅ Company + department metadata
- ❌ Invoicing for contractors — separate Deel API surface; use Proxy
- ❌ Contract lifecycle (offer, signing) — use Proxy

### Auth

- **Type:** API key, managed by Apideck Vault
- **Org binding:** each connection = one Deel organization.
- **Permissions:** API key inherits the generating user's role.

### Example: list all workers (employees + contractors)

```typescript
const { data } = await apideck.hris.employees.list({
  serviceId: "deel",
});
```

## Escape hatch: Proxy API

When an endpoint isn't covered by the HRIS unified API, use Apideck's Proxy to call Deel directly — Apideck injects auth headers and handles token refresh. Set `x-apideck-downstream-url` to the target endpoint on Deel's own API:

```bash
curl 'https://unify.apideck.com/proxy' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}" \
  -H "x-apideck-consumer-id: ${CONSUMER_ID}" \
  -H "x-apideck-service-id: deel" \
  -H "x-apideck-downstream-url: <target endpoint on Deel>" \
  -H "x-apideck-downstream-method: GET"
```

See [Deel's API docs](https://developer.deel.com) for available endpoints.

## Sibling connectors

Other **HRIS** connectors that share this unified API surface (same method signatures, just change `serviceId`):

[`bamboohr`](../bamboohr/), [`workday`](../workday/), [`hibob`](../hibob/), [`personio`](../personio/), [`adp-ihcm`](../adp-ihcm/) *(beta)*, [`adp-workforce-now`](../adp-workforce-now/) *(beta)*, [`paychex`](../paychex/) *(beta)*, [`paylocity`](../paylocity/), and 49 more.

## See also

- [HRIS OpenAPI spec](https://specs.apideck.com/hris.yml) · [API Explorer](https://developers.apideck.com/api-explorer?id=hris)
- [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) — programmatic coverage checks
- [`apideck-best-practices`](../../skills/apideck-best-practices/) — architecture, Vault, pagination, error handling
- [`apideck-node`](../../skills/apideck-node/) — TypeScript / Node SDK patterns
- [Deel official docs](https://developer.deel.com)
