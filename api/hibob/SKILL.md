---
name: hibob
description: |
  Hibob integration via Apideck's HRIS unified API — same methods work across every connector in HRIS, switch by changing `serviceId`. Use when the user wants to read or sync employees, departments, payrolls, and time-off records in Hibob. Routes through Apideck with serviceId "hibob".
license: Apache-2.0
alwaysApply: false
metadata:
  author: apideck
  version: "1.0.0"
  serviceId: hibob
  unifiedApis: ["hris"]
  authType: basic
  tier: "1b"
  verified: true
---

# Hibob (via Apideck)

Access Hibob through Apideck's **HRIS** unified API — one of 58 HRIS connectors that share the same method surface. Code you write here ports to BambooHR, Workday, Deel and 54 other HRIS connectors by changing a single `serviceId` string. Apideck handles auth, pagination, rate limiting, and retries so you don't write per-tenant Hibob plumbing.

## Quick facts

- **Apideck serviceId:** `hibob`
- **Unified API:** HRIS
- **Auth type:** basic
- **Apideck setup guide:** [Connection guide](https://developers.apideck.com/connectors/hibob/docs/consumer+connection)
- **Gotchas:** [page](https://developers.apideck.com/apis/hris/hibob/gotchas)
- **Hibob docs:** https://apidocs.hibob.com
- **Homepage:** https://www.hibob.com/

## When to use this skill

Activate this skill when the user explicitly wants to work with **Hibob** — for example, "sync employees in Hibob" or "list time-off requests in Hibob". This skill teaches the agent:

1. Which Apideck unified API covers Hibob (HRIS)
2. The correct `serviceId` to pass on every call (`hibob`)
3. Hibob-specific auth and coverage caveats

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

// List employees in Hibob
const { data } = await apideck.hris.employees.list({
  serviceId: "hibob",
});
```

## Portable across 58 HRIS connectors

The Apideck **HRIS** unified API exposes the same methods for every connector in its catalog. Switching from Hibob to another HRIS connector is a one-string change — no rewrite, no new SDK.

```typescript
// Today — Hibob
await apideck.hris.employees.list({ serviceId: "hibob" });

// Tomorrow — same code, different connector
await apideck.hris.employees.list({ serviceId: "bamboohr" });
await apideck.hris.employees.list({ serviceId: "workday" });
```

This is the compounding advantage of using Apideck over integrating Hibob directly: code against the unified HRIS API once, gain access to every connector in it. New connectors Apideck adds become available to your app without code changes.

## HiBob via Apideck HRIS

HiBob (Bob) is a modern HRIS for fast-growing companies. Apideck surfaces 101+ employee fields — the deepest employee coverage in the catalog.

### Entity mapping

| Bob entity | Apideck HRIS resource |
|---|---|
| Employee | `employees` (101+ fields) |
| Department | `departments` |
| Time Off Request | `time-off-requests` |
| Company | ⚠️ evolving |
| Sites / Locations | derived from employee attributes |

### Coverage highlights

- ✅ Very deep employee coverage (101+ fields including employment, personal, about, work, compensation sections)
- ✅ Departments
- ✅ Time-off requests
- ❌ Performance management, Docs, Tasks — use Proxy

### Auth

- **Type:** Basic auth (service user ID + API token generated in Bob admin), managed by Apideck Vault
- **Service user:** Bob recommends creating a dedicated service user for API access with scoped permissions.
- **Permissions:** the service user's role determines which fields are readable. Sensitive fields (comp, sensitive personal) require explicit access.

### Example: list employees with compensation fields

```typescript
const { data } = await apideck.hris.employees.list({
  serviceId: "hibob",
  fields: "id,first_name,last_name,email,department,job_title,compensation",
});
```

## Escape hatch: Proxy API

When an endpoint isn't covered by the HRIS unified API, use Apideck's Proxy to call Hibob directly — Apideck injects auth headers and handles token refresh. Set `x-apideck-downstream-url` to the target endpoint on Hibob's own API:

```bash
curl 'https://unify.apideck.com/proxy' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}" \
  -H "x-apideck-consumer-id: ${CONSUMER_ID}" \
  -H "x-apideck-service-id: hibob" \
  -H "x-apideck-downstream-url: <target endpoint on Hibob>" \
  -H "x-apideck-downstream-method: GET"
```

See [Hibob's API docs](https://apidocs.hibob.com) for available endpoints.

## Sibling connectors

Other **HRIS** connectors that share this unified API surface (same method signatures, just change `serviceId`):

[`bamboohr`](../bamboohr/), [`workday`](../workday/), [`deel`](../deel/) *(beta)*, [`personio`](../personio/), [`adp-ihcm`](../adp-ihcm/) *(beta)*, [`adp-workforce-now`](../adp-workforce-now/) *(beta)*, [`paychex`](../paychex/) *(beta)*, [`paylocity`](../paylocity/), and 49 more.

## See also

- [Apideck connection guide for Hibob](https://developers.apideck.com/connectors/hibob/docs/consumer+connection)
- [HRIS OpenAPI spec](https://specs.apideck.com/hris.yml) · [API Explorer](https://developers.apideck.com/api-explorer?id=hris)
- [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) — programmatic coverage checks
- [`apideck-best-practices`](../../skills/apideck-best-practices/) — architecture, Vault, pagination, error handling
- [`apideck-node`](../../skills/apideck-node/) — TypeScript / Node SDK patterns
- [Hibob official docs](https://apidocs.hibob.com)
