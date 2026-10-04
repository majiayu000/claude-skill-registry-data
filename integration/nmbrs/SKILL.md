---
name: nmbrs
description: |
  Visma Nmbrs integration via Apideck's HRIS unified API — same methods work across every connector in HRIS, switch by changing `serviceId`. Use when the user wants to read or sync employees, departments, payrolls, and time-off records in Visma Nmbrs. Routes through Apideck with serviceId "nmbrs".
license: Apache-2.0
alwaysApply: false
metadata:
  author: apideck
  version: "1.0.0"
  serviceId: nmbrs
  unifiedApis: ["hris"]
  authType: oauth2
  tier: "2"
  verified: true
  difficulty: moderate
  partnershipRequired: true
  sandboxAvailable: true
---

# Visma Nmbrs (via Apideck)

Access Visma Nmbrs through Apideck's **HRIS** unified API — one of 58 HRIS connectors that share the same method surface. Code you write here ports to BambooHR, Workday, Deel and 54 other HRIS connectors by changing a single `serviceId` string. Apideck handles auth, pagination, rate limiting, and retries so you don't write per-tenant Visma Nmbrs plumbing.

## Quick facts

- **Apideck serviceId:** `nmbrs`
- **Unified API:** HRIS
- **Auth type:** oauth2
- **Gotchas:** [page](https://developers.apideck.com/apis/hris/nmbrs/gotchas)
- **Visma Nmbrs docs:** https://support.nmbrs.com
- **Homepage:** https://www.nmbrs.com

## At a glance

- **Implementation difficulty:** moderate — Demo Validation Required for Production Subscription
- **Vendor partnership required:** yes ([Nmbrs App Store](https://www.nmbrs.com/nl/payroll/building-a-nmbrs-integration)) — Joining gives the production subscription, approved after a demo video and the Ready-to-demo form.
- **Apideck-managed credentials:** available — For testing only, through a shared Apideck partner app.
- **Account type required:** A Nmbrs Payroll (formerly Nmbrs) environment.
- **Consumer access level:** A client login or company login created at debtor level; a master login in an Accountant environment does not work.
- **Sandbox:** available ([signup](https://developer.payroll.nmbrs.com/docs/create-nmbrs-account)) — Free demo environment: sign up with a domain named extdev-{AppName} and affiliate code DEMO, or it is deleted after 30 days.
- **Costs:** Nmbrs publishes no fee for API access.
- **Rate limits:** Set by the developer-portal subscription product; the development subscription has lower limits than the production one.
- **Authentication:** Authorization Code flow with pushed authorization requests; a Nmbrs subscription key is also sent with each call.
- **Webhooks:** Virtual webhooks - employee created and updated events, detected by polling.

> Facts synced from Apideck's connector metadata API — `GET /connector/connectors/nmbrs` (`overview` field) is the live, authoritative version.

## When to use this skill

Activate this skill when the user explicitly wants to work with **Visma Nmbrs** — for example, "sync employees in Visma Nmbrs" or "list time-off requests in Visma Nmbrs". This skill teaches the agent:

1. Which Apideck unified API covers Visma Nmbrs (HRIS)
2. The correct `serviceId` to pass on every call (`nmbrs`)
3. Visma Nmbrs-specific auth and coverage caveats

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

// List employees in Visma Nmbrs
const { data } = await apideck.hris.employees.list({
  serviceId: "nmbrs",
});
```

## Portable across 58 HRIS connectors

The Apideck **HRIS** unified API exposes the same methods for every connector in its catalog. Switching from Visma Nmbrs to another HRIS connector is a one-string change — no rewrite, no new SDK.

```typescript
// Today — Visma Nmbrs
await apideck.hris.employees.list({ serviceId: "nmbrs" });

// Tomorrow — same code, different connector
await apideck.hris.employees.list({ serviceId: "bamboohr" });
await apideck.hris.employees.list({ serviceId: "workday" });
```

This is the compounding advantage of using Apideck over integrating Visma Nmbrs directly: code against the unified HRIS API once, gain access to every connector in it. New connectors Apideck adds become available to your app without code changes.

## Authentication

- **Type:** OAuth 2.0
- **Managed by:** Apideck Vault — Apideck handles the full OAuth dance (authorization code flow, token exchange, refresh). Never ask the user for API keys or tokens directly.
- **User setup:** Users authorize via the Vault modal. Connection state progresses `available → added → authorized → callable`.
- **Token refresh:** automatic. Expired tokens are refreshed transparently on the next API call.

See [`apideck-best-practices`](../../skills/apideck-best-practices/) for Vault setup, connection lifecycle, and handling re-auth flows.

## Verifying coverage

Not every HRIS operation is supported by every connector. Always verify before assuming a method works:

```bash
curl 'https://unify.apideck.com/connector/connectors/nmbrs' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}"
```

See [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) for patterns around `UnsupportedOperationError` and connector-specific fallbacks.

## Escape hatch: Proxy API

When an endpoint isn't covered by the HRIS unified API, use Apideck's Proxy to call Visma Nmbrs directly — Apideck injects auth headers and handles token refresh. Set `x-apideck-downstream-url` to the target endpoint on Visma Nmbrs's own API:

```bash
curl 'https://unify.apideck.com/proxy' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}" \
  -H "x-apideck-consumer-id: ${CONSUMER_ID}" \
  -H "x-apideck-service-id: nmbrs" \
  -H "x-apideck-downstream-url: <target endpoint on Visma Nmbrs>" \
  -H "x-apideck-downstream-method: GET"
```

See [Visma Nmbrs's API docs](https://support.nmbrs.com) for available endpoints.

## Sibling connectors

Other **HRIS** connectors that share this unified API surface (same method signatures, just change `serviceId`):

[`bamboohr`](../bamboohr/), [`workday`](../workday/), [`deel`](../deel/) *(beta)*, [`hibob`](../hibob/), [`personio`](../personio/), [`adp-ihcm`](../adp-ihcm/) *(beta)*, [`adp-workforce-now`](../adp-workforce-now/) *(beta)*, [`paychex`](../paychex/) *(beta)*, and 49 more.

## See also

- [HRIS OpenAPI spec](https://specs.apideck.com/hris.yml) · [API Explorer](https://developers.apideck.com/api-explorer?id=hris)
- [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) — programmatic coverage checks
- [`apideck-best-practices`](../../skills/apideck-best-practices/) — architecture, Vault, pagination, error handling
- [`apideck-node`](../../skills/apideck-node/) — TypeScript / Node SDK patterns
- [Visma Nmbrs official docs](https://support.nmbrs.com)
