---
name: personio
description: |
  Personio integration via Apideck's HRIS unified API — same methods work across every connector in HRIS, switch by changing `serviceId`. Use when the user wants to read or sync employees, departments, payrolls, and time-off records in Personio. Routes through Apideck with serviceId "personio".
license: Apache-2.0
alwaysApply: false
metadata:
  author: apideck
  version: "1.0.0"
  serviceId: personio
  unifiedApis: ["hris"]
  authType: oauth2
  tier: "1b"
  verified: true
  difficulty: moderate
  partnershipRequired: false
  sandboxAvailable: true
---

# Personio (via Apideck)

Access Personio through Apideck's **HRIS** unified API — one of 58 HRIS connectors that share the same method surface. Code you write here ports to BambooHR, Workday, Deel and 54 other HRIS connectors by changing a single `serviceId` string. Apideck handles auth, pagination, rate limiting, and retries so you don't write per-tenant Personio plumbing.

## Quick facts

- **Apideck serviceId:** `personio`
- **Unified API:** HRIS
- **Auth type:** oauth2
- **Apideck setup guide:** [Connection guide](https://developers.apideck.com/connectors/personio/docs/consumer+connection)
- **Gotchas:** [page](https://developers.apideck.com/apis/hris/personio/gotchas)
- **Personio docs:** https://developer.personio.de
- **Homepage:** https://www.personio.com/

## At a glance

- **Implementation difficulty:** moderate — Consumer-Supplied API Credentials Instead of a User-Consent OAuth Flow
- **Vendor partnership required:** no ([developer portal](https://www.personio.com/partner/tech/)) — Apideck is already an approved Personio iPaaS partner. Personio's free Tech Partner programme is optional and adds a Marketplace listing.
- **Apideck-managed credentials:** not available — Each consumer supplies their own Personio API credentials.
- **Account type required:** A Personio account on a plan that includes API access (Core Pro at the time of writing).
- **Consumer access level:** Administrator: only a Personio administrator can generate the API credentials.
- **Sandbox:** available ([signup](https://www.personio.com/partner-trial/)) — Free, self-service Partner Developer Account from Personio's partner trial. A Personio free trial or a consumer's own account also work for testing.
- **Costs:** No separate API fee; the API requires the Core Pro plan, whose pricing is quote-based.
- **Rate limits:** 2,000 requests/minute per IP overall, with tighter per-endpoint caps (300/minute on the employee list); HTTP 429 beyond either.
- **Authentication:** Each consumer's Personio administrator generates a Client ID and Secret in their own Personio account. Nothing for you to register.
- **Webhooks:** Virtual webhooks (Apideck polls for employee created, updated and terminated events)

**Important to know:**

- Access is scoped at credential creation: the administrator picks which resources are readable or writable and which employee attributes are exposed, so a credential created too narrowly returns partial or empty data.
- Personio can exclude individual employees from API transfer. An 'Include in transfer' field on each employee record governs whether that person is shared, so a consumer's own configuration can legitimately hide records from your integration.
- Personio's 1 December 2026 cutoff for passing API credentials as query-string parameters does not affect this connector: it already sends them in the request body, so nothing changes for you.

> Facts synced from Apideck's connector metadata API — `GET /connector/connectors/personio` (`overview` field) is the live, authoritative version.

## When to use this skill

Activate this skill when the user explicitly wants to work with **Personio** — for example, "sync employees in Personio" or "list time-off requests in Personio". This skill teaches the agent:

1. Which Apideck unified API covers Personio (HRIS)
2. The correct `serviceId` to pass on every call (`personio`)
3. Personio-specific auth and coverage caveats

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

// List employees in Personio
const { data } = await apideck.hris.employees.list({
  serviceId: "personio",
});
```

## Portable across 58 HRIS connectors

The Apideck **HRIS** unified API exposes the same methods for every connector in its catalog. Switching from Personio to another HRIS connector is a one-string change — no rewrite, no new SDK.

```typescript
// Today — Personio
await apideck.hris.employees.list({ serviceId: "personio" });

// Tomorrow — same code, different connector
await apideck.hris.employees.list({ serviceId: "bamboohr" });
await apideck.hris.employees.list({ serviceId: "workday" });
```

This is the compounding advantage of using Apideck over integrating Personio directly: code against the unified HRIS API once, gain access to every connector in it. New connectors Apideck adds become available to your app without code changes.

## Personio via Apideck HRIS

Personio is a European SMB HRIS. Apideck currently covers employees and time-off requests.

### Entity mapping

| Personio entity | Apideck HRIS resource |
|---|---|
| Employee | `employees` (with custom fields as attributes) |
| Time Off Request | `time-off-requests` |
| Absence Period | exposed via `time-off-requests` |
| Department, Office | derived from employee attributes |
| Company | ⚠️ coverage evolving |
| Payroll | ❌ not in scope |

### Coverage highlights

- ✅ Full employee list + details (51+ fields surfaced)
- ✅ Time-off request lifecycle (read, approve, reject)
- ⚠️ Departments/offices — derived from employee fields, not first-class
- ❌ Performance reviews, training — use Proxy

Always check `/connector/connectors/personio` for current coverage.

### Auth

- **Type:** API credentials (client ID + client secret), managed by Apideck Vault
- **Region:** Personio's API is region-sharded (EU). All accounts share the same base URL.
- **Permissions:** API credentials inherit the configured role. Admin credentials recommended for full sync.

### Example: list all employees with custom fields

```typescript
const { data } = await apideck.hris.employees.list({
  serviceId: "personio",
  fields: "id,first_name,last_name,email,department,custom_fields",
});
```

## Escape hatch: Proxy API

When an endpoint isn't covered by the HRIS unified API, use Apideck's Proxy to call Personio directly — Apideck injects auth headers and handles token refresh. Set `x-apideck-downstream-url` to the target endpoint on Personio's own API:

```bash
curl 'https://unify.apideck.com/proxy' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}" \
  -H "x-apideck-consumer-id: ${CONSUMER_ID}" \
  -H "x-apideck-service-id: personio" \
  -H "x-apideck-downstream-url: <target endpoint on Personio>" \
  -H "x-apideck-downstream-method: GET"
```

See [Personio's API docs](https://developer.personio.de) for available endpoints.

## Sibling connectors

Other **HRIS** connectors that share this unified API surface (same method signatures, just change `serviceId`):

[`bamboohr`](../bamboohr/), [`workday`](../workday/), [`deel`](../deel/) *(beta)*, [`hibob`](../hibob/), [`adp-ihcm`](../adp-ihcm/) *(beta)*, [`adp-workforce-now`](../adp-workforce-now/) *(beta)*, [`paychex`](../paychex/) *(beta)*, [`paylocity`](../paylocity/), and 49 more.

## See also

- [Apideck connection guide for Personio](https://developers.apideck.com/connectors/personio/docs/consumer+connection)
- [HRIS OpenAPI spec](https://specs.apideck.com/hris.yml) · [API Explorer](https://developers.apideck.com/api-explorer?id=hris)
- [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) — programmatic coverage checks
- [`apideck-best-practices`](../../skills/apideck-best-practices/) — architecture, Vault, pagination, error handling
- [`apideck-node`](../../skills/apideck-node/) — TypeScript / Node SDK patterns
- [Personio official docs](https://developer.personio.de)
