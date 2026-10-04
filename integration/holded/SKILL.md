---
name: holded
description: |
  Holded integration via Apideck's HRIS unified API — same methods work across every connector in HRIS, switch by changing `serviceId`. Use when the user wants to read or sync employees, departments, payrolls, and time-off records in Holded. Routes through Apideck with serviceId "holded".
license: Apache-2.0
alwaysApply: false
metadata:
  author: apideck
  version: "1.0.0"
  serviceId: holded
  unifiedApis: ["hris"]
  authType: apiKey
  tier: "2"
  verified: true
  difficulty: moderate
  partnershipRequired: false
  sandboxAvailable: true
---

# Holded (via Apideck)

Access Holded through Apideck's **HRIS** unified API — one of 58 HRIS connectors that share the same method surface. Code you write here ports to BambooHR, Workday, Deel and 54 other HRIS connectors by changing a single `serviceId` string. Apideck handles auth, pagination, rate limiting, and retries so you don't write per-tenant Holded plumbing.

## Quick facts

- **Apideck serviceId:** `holded`
- **Unified API:** HRIS
- **Auth type:** apiKey
- **Apideck setup guide:** [Connection guide](https://developers.apideck.com/connectors/holded/docs/consumer+connection) · [image](https://developers.apideck.com/connectors/holded/docs/consumer+image)
- **Gotchas:** [page](https://developers.apideck.com/apis/hris/holded/gotchas)
- **Homepage:** https://www.holded.com/

## At a glance

- **Implementation difficulty:** moderate — API Key Authentication - Each Consumer Creates Their Own Key in Holded
- **Vendor partnership required:** no
- **Apideck-managed credentials:** not available — Each consumer supplies their own Holded API key.
- **Account type required:** A Holded account on a paid plan: the free plan carries no API access.
- **Consumer access level:** A user who can reach the Developers section in Holded, which the default developer role grants.
- **Sandbox:** available — Every Holded account includes a demo environment, switched into from the account menu. It takes sample data, can be reset, and the API reaches it too.
- **Costs:** Holded does not sell API access separately, so the cost is the subscription your consumer already pays, on whichever plan carries the quota you need.
- **Rate limits:** 60 to 600 calls a minute by plan, plus a monthly quota from 500 on the entry plan to 100,000 at the top. Lower plans 429 at the cap; the top meters overage.
- **Authentication:** Sent as a request header; not OAuth.
- **Webhooks:** Virtual webhooks - created and updated events across 11 resources, from invoices, bills and payments to employees. Deletions raise nothing.

**Important to know:**

- The monthly quota, not the per-minute rate, is what usually decides whether Holded can carry an integration: it is a single allowance for the whole account, drawn down by every key on it rather than granted per integration.
- A Holded API key belongs to the account rather than to the person who created it. Anyone holding it reaches everything the account exposes within the module permissions picked at creation, so choose those permissions deliberately.
- Holded serves both the accounting and HRIS APIs, and Vault keys a connection to one unified API, so each vertical is a separate connection using the same Holded API key. Employees are reachable only through HRIS: the accounting side excludes them.

> Facts synced from Apideck's connector metadata API — `GET /connector/connectors/holded` (`overview` field) is the live, authoritative version.

## When to use this skill

Activate this skill when the user explicitly wants to work with **Holded** — for example, "sync employees in Holded" or "list time-off requests in Holded". This skill teaches the agent:

1. Which Apideck unified API covers Holded (HRIS)
2. The correct `serviceId` to pass on every call (`holded`)
3. Holded-specific auth and coverage caveats

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

// List employees in Holded
const { data } = await apideck.hris.employees.list({
  serviceId: "holded",
});
```

## Portable across 58 HRIS connectors

The Apideck **HRIS** unified API exposes the same methods for every connector in its catalog. Switching from Holded to another HRIS connector is a one-string change — no rewrite, no new SDK.

```typescript
// Today — Holded
await apideck.hris.employees.list({ serviceId: "holded" });

// Tomorrow — same code, different connector
await apideck.hris.employees.list({ serviceId: "bamboohr" });
await apideck.hris.employees.list({ serviceId: "workday" });
```

This is the compounding advantage of using Apideck over integrating Holded directly: code against the unified HRIS API once, gain access to every connector in it. New connectors Apideck adds become available to your app without code changes.

## Authentication

- **Type:** API Key
- **Managed by:** Apideck Vault — the user pastes their Holded API key into the Vault modal; Apideck stores it encrypted and injects it on every request.
- **Rotation:** if the user rotates their key, they re-enter it in Vault. No code changes needed.

**Setup guide:** Apideck publishes a step-by-step guide for registering an OAuth app / configuring credentials for Holded — see [https://developers.apideck.com/connectors/holded/docs/consumer+connection](https://developers.apideck.com/connectors/holded/docs/consumer+connection). Use that as the authoritative source when walking users through connection setup.

See [`apideck-best-practices`](../../skills/apideck-best-practices/) for Vault setup, connection lifecycle, and handling re-auth flows.

## Verifying coverage

Not every HRIS operation is supported by every connector. Always verify before assuming a method works:

```bash
curl 'https://unify.apideck.com/connector/connectors/holded' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}"
```

See [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) for patterns around `UnsupportedOperationError` and connector-specific fallbacks.

## Escape hatch: Proxy API

When an endpoint isn't covered by the HRIS unified API, use Apideck's Proxy to call Holded directly — Apideck injects auth headers and handles token refresh. Set `x-apideck-downstream-url` to the target endpoint on Holded's own API:

```bash
curl 'https://unify.apideck.com/proxy' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}" \
  -H "x-apideck-consumer-id: ${CONSUMER_ID}" \
  -H "x-apideck-service-id: holded" \
  -H "x-apideck-downstream-url: <target endpoint on Holded>" \
  -H "x-apideck-downstream-method: GET"
```

See [Holded's API docs](#) for available endpoints.

## Sibling connectors

Other **HRIS** connectors that share this unified API surface (same method signatures, just change `serviceId`):

[`bamboohr`](../bamboohr/), [`workday`](../workday/), [`deel`](../deel/) *(beta)*, [`hibob`](../hibob/), [`personio`](../personio/), [`adp-ihcm`](../adp-ihcm/) *(beta)*, [`adp-workforce-now`](../adp-workforce-now/) *(beta)*, [`paychex`](../paychex/) *(beta)*, and 49 more.

## See also

- [Apideck connection guide for Holded](https://developers.apideck.com/connectors/holded/docs/consumer+connection)
- [Apideck image guide](https://developers.apideck.com/connectors/holded/docs/consumer+image)
- [HRIS OpenAPI spec](https://specs.apideck.com/hris.yml) · [API Explorer](https://developers.apideck.com/api-explorer?id=hris)
- [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) — programmatic coverage checks
- [`apideck-best-practices`](../../skills/apideck-best-practices/) — architecture, Vault, pagination, error handling
- [`apideck-node`](../../skills/apideck-node/) — TypeScript / Node SDK patterns
