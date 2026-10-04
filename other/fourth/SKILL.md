---
name: fourth
description: |
  Fourth integration via Apideck's HRIS unified API — same methods work across every connector in HRIS, switch by changing `serviceId`. Use when the user wants to read or sync employees, departments, payrolls, and time-off records in Fourth. Routes through Apideck with serviceId "fourth".
license: Apache-2.0
alwaysApply: false
metadata:
  author: apideck
  version: "1.0.0"
  serviceId: fourth
  unifiedApis: ["hris"]
  authType: basic
  tier: "2"
  verified: true
  status: beta
  difficulty: involved
  partnershipRequired: false
  sandboxAvailable: true
---

# Fourth (via Apideck)

Access Fourth through Apideck's **HRIS** unified API — one of 58 HRIS connectors that share the same method surface. Code you write here ports to BambooHR, Workday, Deel and 54 other HRIS connectors by changing a single `serviceId` string. Apideck handles auth, pagination, rate limiting, and retries so you don't write per-tenant Fourth plumbing.

> **Beta connector.** Fourth is currently in beta on Apideck. Expect partial resource coverage and occasional mapping gaps. Always verify coverage (see below) and fall back to the Proxy API for unsupported operations.

## Quick facts

- **Apideck serviceId:** `fourth`
- **Unified API:** HRIS
- **Auth type:** basic
- **Status:** beta
- **Gotchas:** [page](https://developers.apideck.com/apis/hris/fourth/gotchas)
- **Fourth docs:** https://www.fourth.com
- **Homepage:** https://www.fourth.com/

## At a glance

- **Implementation difficulty:** involved — Credentials Only Via a Mutual Fourth Customer + Basic Auth With Vendor-Issued Keys
- **Vendor partnership required:** no ([developer portal](https://developer.fourth.com/en-gb/docs/getting-started)) — No partner programme to join.
- **Apideck-managed credentials:** not available — Fourth issues credentials against each customer account.
- **Account type required:** A Fourth UK Employee API account, with Fourth as employee master record and payroll system.
- **Consumer access level:** A Fourth account admin able to request API keys from Fourth.
- **Sandbox:** available ([signup](https://developer.fourth.com/en-gb/docs/getting-started)) — Test credentials come from the Fourth consultant assigned to the mutual customer's project; not self-serve.
- **Rate limits:** No numeric limit published; Fourth advises at most one retry a minute on 5xx errors.
- **Authentication:** Organisation ID, API key and secret key, all issued by Fourth.
- **Webhooks:** Virtual webhooks - employee created and updated events

**Important to know:**

- Fourth does not sell or issue API access directly: live credentials are linked to a customer account, so a mutual Fourth customer requests them, and Fourth does not publish the API host, so you also obtain it from Fourth.
- This connector runs on Fourth's UK Employee API, so it serves Fourth customers in the United Kingdom only.

> Facts synced from Apideck's connector metadata API — `GET /connector/connectors/fourth` (`overview` field) is the live, authoritative version.

## When to use this skill

Activate this skill when the user explicitly wants to work with **Fourth** — for example, "sync employees in Fourth" or "list time-off requests in Fourth". This skill teaches the agent:

1. Which Apideck unified API covers Fourth (HRIS)
2. The correct `serviceId` to pass on every call (`fourth`)
3. Fourth-specific auth and coverage caveats

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

// List employees in Fourth
const { data } = await apideck.hris.employees.list({
  serviceId: "fourth",
});
```

## Portable across 58 HRIS connectors

The Apideck **HRIS** unified API exposes the same methods for every connector in its catalog. Switching from Fourth to another HRIS connector is a one-string change — no rewrite, no new SDK.

```typescript
// Today — Fourth
await apideck.hris.employees.list({ serviceId: "fourth" });

// Tomorrow — same code, different connector
await apideck.hris.employees.list({ serviceId: "bamboohr" });
await apideck.hris.employees.list({ serviceId: "workday" });
```

This is the compounding advantage of using Apideck over integrating Fourth directly: code against the unified HRIS API once, gain access to every connector in it. New connectors Apideck adds become available to your app without code changes.

## Authentication

- **Type:** Basic auth (username/password)
- **Managed by:** Apideck Vault — credentials are collected through the Vault modal and stored encrypted server-side.
- **Note:** basic auth connectors often require manual rotation by the end user. If auth fails persistently, prompt them to re-enter credentials in Vault.

See [`apideck-best-practices`](../../skills/apideck-best-practices/) for Vault setup, connection lifecycle, and handling re-auth flows.

## Verifying coverage

Not every HRIS operation is supported by every connector. Always verify before assuming a method works:

```bash
curl 'https://unify.apideck.com/connector/connectors/fourth' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}"
```

See [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) for patterns around `UnsupportedOperationError` and connector-specific fallbacks.

## Escape hatch: Proxy API

When an endpoint isn't covered by the HRIS unified API, use Apideck's Proxy to call Fourth directly — Apideck injects auth headers and handles token refresh. Set `x-apideck-downstream-url` to the target endpoint on Fourth's own API:

```bash
curl 'https://unify.apideck.com/proxy' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}" \
  -H "x-apideck-consumer-id: ${CONSUMER_ID}" \
  -H "x-apideck-service-id: fourth" \
  -H "x-apideck-downstream-url: <target endpoint on Fourth>" \
  -H "x-apideck-downstream-method: GET"
```

See [Fourth's API docs](https://www.fourth.com) for available endpoints.

## Sibling connectors

Other **HRIS** connectors that share this unified API surface (same method signatures, just change `serviceId`):

[`bamboohr`](../bamboohr/), [`workday`](../workday/), [`deel`](../deel/) *(beta)*, [`hibob`](../hibob/), [`personio`](../personio/), [`adp-ihcm`](../adp-ihcm/) *(beta)*, [`adp-workforce-now`](../adp-workforce-now/) *(beta)*, [`paychex`](../paychex/) *(beta)*, and 49 more.

## See also

- [HRIS OpenAPI spec](https://specs.apideck.com/hris.yml) · [API Explorer](https://developers.apideck.com/api-explorer?id=hris)
- [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) — programmatic coverage checks
- [`apideck-best-practices`](../../skills/apideck-best-practices/) — architecture, Vault, pagination, error handling
- [`apideck-node`](../../skills/apideck-node/) — TypeScript / Node SDK patterns
- [Fourth official docs](https://www.fourth.com)
