---
name: bamboohr
description: |
  BambooHR integration via Apideck's HRIS unified API — same methods work across every connector in HRIS, switch by changing `serviceId`. Use when the user wants to read or sync employees, departments, payrolls, and time-off records in BambooHR. Routes through Apideck with serviceId "bamboohr".
license: Apache-2.0
alwaysApply: false
metadata:
  author: apideck
  version: "1.0.0"
  serviceId: bamboohr
  unifiedApis: ["hris"]
  authType: basic
  tier: "1a"
  verified: true
  difficulty: moderate
  partnershipRequired: false
  sandboxAvailable: true
---

# BambooHR (via Apideck)

Access BambooHR through Apideck's **HRIS** unified API — one of 58 HRIS connectors that share the same method surface. Code you write here ports to Workday, Deel, Hibob and 54 other HRIS connectors by changing a single `serviceId` string. Apideck handles auth, pagination, rate limiting, and retries so you don't write per-tenant BambooHR plumbing.

## Quick facts

- **Apideck serviceId:** `bamboohr`
- **Unified API:** HRIS
- **Auth type:** basic
- **Apideck setup guide:** [Connection guide](https://developers.apideck.com/connectors/bamboohr/docs/consumer+connection)
- **Gotchas:** [page](https://developers.apideck.com/apis/hris/bamboohr/gotchas)
- **BambooHR docs:** https://documentation.bamboohr.com/docs
- **Homepage:** https://www.bamboohr.com

## At a glance

- **Implementation difficulty:** moderate — API key authentication, with no partnership or app review
- **Vendor partnership required:** no ([BambooHR Apps Marketplace Program](https://www.bamboohr.com/partner-programs/marketplace-program)) — Joining the optional BambooHR Marketplace Program adds a sandbox account and a Marketplace listing.
- **Apideck-managed credentials:** not available — Each consumer generates and supplies their own API key and subdomain.
- **Account type required:** Any BambooHR account (Core, Pro or Elite).
- **Consumer access level:** Account Owner recommended, otherwise a custom access level carrying the permissions your integration needs.
- **Sandbox:** available ([signup](https://www.bamboohr.com/signup/)) — Sign up for a free BambooHR trial and test against it. Joining the Marketplace Program additionally provides a dedicated sandbox account.
- **Costs:** No separate API fee, and no cost to you — API access is included in each consumer's own BambooHR subscription.
- **Rate limits:** Not published. BambooHR throttles at its discretion and returns Retry-After; from 14 September 2026 that response changes from 503 to 429.
- **Authentication:** The consumer's API key over HTTP Basic, not OAuth, plus their BambooHR subdomain.
- **Webhooks:** Virtual webhooks (Apideck polls BambooHR for employee created, updated and terminated events)

**Important to know:**

- An API key carries the permissions of the BambooHR user who created it. An under-privileged key returns a narrower set of employees and blank fields instead of an error, so missing data reads as a mapping bug rather than a permissions problem.
- BambooHR has retired its custom-report endpoint in favour of its Datasets API. This matters only if you planned to pull report-shaped data; the unified HRIS resources are unaffected.

> Facts synced from Apideck's connector metadata API — `GET /connector/connectors/bamboohr` (`overview` field) is the live, authoritative version.

## When to use this skill

Activate this skill when the user explicitly wants to work with **BambooHR** — for example, "sync employees in BambooHR" or "list time-off requests in BambooHR". This skill teaches the agent:

1. Which Apideck unified API covers BambooHR (HRIS)
2. The correct `serviceId` to pass on every call (`bamboohr`)
3. BambooHR-specific auth and coverage caveats

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

// List employees in BambooHR
const { data } = await apideck.hris.employees.list({
  serviceId: "bamboohr",
});
```

## Portable across 58 HRIS connectors

The Apideck **HRIS** unified API exposes the same methods for every connector in its catalog. Switching from BambooHR to another HRIS connector is a one-string change — no rewrite, no new SDK.

```typescript
// Today — BambooHR
await apideck.hris.employees.list({ serviceId: "bamboohr" });

// Tomorrow — same code, different connector
await apideck.hris.employees.list({ serviceId: "workday" });
await apideck.hris.employees.list({ serviceId: "deel" });
```

This is the compounding advantage of using Apideck over integrating BambooHR directly: code against the unified HRIS API once, gain access to every connector in it. New connectors Apideck adds become available to your app without code changes.

## BambooHR via Apideck HRIS

BambooHR is the reference SMB HRIS connector on Apideck. Full employee and org coverage; payroll coverage is read-only (BambooHR doesn't run payroll itself — it integrates with providers like TRAXPayroll).

### Entity mapping

| BambooHR entity | Apideck HRIS resource |
|---|---|
| Employee | `employees` |
| Department | `departments` (derived from employee dept field) |
| Time Off Request | `time-off-requests` |
| Time Off Policy | `time-off-policies` |
| Employment Status | `employments` (historical employment records) |
| Company | `companies` |
| Job | exposed via `employees[].jobs[]` |
| Custom fields | exposed as `employees[].custom_fields[]` |

### Coverage highlights

- ✅ Full CRUD on employees (incl. custom fields)
- ✅ Time-off requests — read, approve, reject
- ✅ Employee photos via `employees/{id}/photo`
- ✅ Sensitive fields (SSN, DOB) — requires elevated permissions on the API key
- ⚠️ Departments are derived from employee records, not a first-class BambooHR entity
- ⚠️ Payroll data — read-only; BambooHR surfaces summaries from integrated payroll providers
- ❌ Benefits enrollment — use Proxy
- ❌ Performance reviews — use Proxy
- ❌ Hiring / ATS-adjacent data — use a dedicated ATS connector

### BambooHR-specific auth notes

- **Auth type:** API key (not OAuth). The user generates a key from BambooHR under "API Keys" in their account settings and pastes it into the Vault modal.
- **Subdomain required:** BambooHR API keys are bound to a company subdomain (e.g., `acme.bamboohr.com`). The user provides the subdomain alongside the key during Vault setup. Changing subdomain = reconfigure the connection.
- **Key permissions = user permissions:** the API key inherits the generating user's role. Sensitive fields (SSN, DOB, compensation) require admin-level access — limited keys get 403s on those fields. If sensitive data is missing from responses, check whether the key-generating user is an admin.

### Common BambooHR quirks handled by Apideck

- **Field naming** — BambooHR uses camelCase (`firstName`, `hireDate`); Apideck normalizes to snake_case (`first_name`, `hire_date`).
- **Custom fields** — BambooHR custom fields are prefixed `custom` in the raw API. Apideck exposes them as a structured `custom_fields[]` array with `id`, `name`, `value`.
- **Historical data** — employment history surfaced as `employments[]` ordered by `effective_date`.
- **Photo URLs** — signed URLs that expire. Fetch-through rather than cache.

### Example: sync all employees with custom fields

```typescript
let cursor;
const all = [];

do {
  const { data, pagination } = await apideck.hris.employees.list({
    serviceId: "bamboohr",
    cursor,
    fields: "id,first_name,last_name,email,department,job_title,custom_fields",
  });
  all.push(...data);
  cursor = pagination?.cursors?.next;
} while (cursor);

console.log(`Synced ${all.length} employees`);
```

### Example: approve a time-off request

The time-off-request endpoint is nested under employee (`/hris/time-off-requests/employees/{employee_id}/time-off-requests/{id}`). Check [`apideck-node`](../../skills/apideck-node/) for the canonical method signature.

```typescript
await apideck.hris.timeOffRequests.update({
  serviceId: "bamboohr",
  employeeId: "emp_001",
  id: "req_123",
  timeOffRequest: { status: "approved" },
});
```

## Escape hatch: Proxy API

When an endpoint isn't covered by the HRIS unified API, use Apideck's Proxy to call BambooHR directly — Apideck injects auth headers and handles token refresh. Set `x-apideck-downstream-url` to the target endpoint on BambooHR's own API:

```bash
curl 'https://unify.apideck.com/proxy' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}" \
  -H "x-apideck-consumer-id: ${CONSUMER_ID}" \
  -H "x-apideck-service-id: bamboohr" \
  -H "x-apideck-downstream-url: <target endpoint on BambooHR>" \
  -H "x-apideck-downstream-method: GET"
```

See [BambooHR's API docs](https://documentation.bamboohr.com/docs) for available endpoints.

## Sibling connectors

Other **HRIS** connectors that share this unified API surface (same method signatures, just change `serviceId`):

[`workday`](../workday/), [`deel`](../deel/) *(beta)*, [`hibob`](../hibob/), [`personio`](../personio/), [`adp-ihcm`](../adp-ihcm/) *(beta)*, [`adp-workforce-now`](../adp-workforce-now/) *(beta)*, [`paychex`](../paychex/) *(beta)*, [`paylocity`](../paylocity/), and 49 more.

## See also

- [Apideck connection guide for BambooHR](https://developers.apideck.com/connectors/bamboohr/docs/consumer+connection)
- [HRIS OpenAPI spec](https://specs.apideck.com/hris.yml) · [API Explorer](https://developers.apideck.com/api-explorer?id=hris)
- [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) — programmatic coverage checks
- [`apideck-best-practices`](../../skills/apideck-best-practices/) — architecture, Vault, pagination, error handling
- [`apideck-node`](../../skills/apideck-node/) — TypeScript / Node SDK patterns
- [BambooHR official docs](https://documentation.bamboohr.com/docs)
