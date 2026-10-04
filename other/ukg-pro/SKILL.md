---
name: ukg-pro
description: |
  UKG Pro integration via Apideck's HRIS unified API — same methods work across every connector in HRIS, switch by changing `serviceId`. Use when the user wants to read or sync employees, departments, payrolls, and time-off records in UKG Pro. Routes through Apideck with serviceId "ukg-pro".
license: Apache-2.0
alwaysApply: false
metadata:
  author: apideck
  version: "1.0.0"
  serviceId: ukg-pro
  unifiedApis: ["hris"]
  authType: basic
  tier: "2"
  verified: true
  status: beta
  difficulty: moderate
  partnershipRequired: false
  sandboxAvailable: false
---

# UKG Pro (via Apideck)

Access UKG Pro through Apideck's **HRIS** unified API — one of 58 HRIS connectors that share the same method surface. Code you write here ports to BambooHR, Workday, Deel and 54 other HRIS connectors by changing a single `serviceId` string. Apideck handles auth, pagination, rate limiting, and retries so you don't write per-tenant UKG Pro plumbing.

> **Beta connector.** UKG Pro is currently in beta on Apideck. Expect partial resource coverage and occasional mapping gaps. Always verify coverage (see below) and fall back to the Proxy API for unsupported operations.

## Quick facts

- **Apideck serviceId:** `ukg-pro`
- **Unified API:** HRIS
- **Auth type:** basic
- **Status:** beta
- **Gotchas:** [page](https://developers.apideck.com/apis/hris/ukg-pro/gotchas)
- **Homepage:** https://www.ukg.com/solutions/ukg-pro

## At a glance

- **Implementation difficulty:** moderate — Web Services Account Created by a UKG Administrator for Each Consumer
- **Vendor partnership required:** no — UKG reserves only a few API areas, such as Background Check and Benefits Integration, for official partners; this connector uses none of them.
- **Apideck-managed credentials:** not available — Each consumer supplies the credentials of their own UKG Pro Web Services account.
- **Account type required:** UKG Pro HCM tenant
- **Consumer access level:** System administrator, to create the Web Services account and read the Customer API Key
- **Sandbox:** not available — Test against a consumer's own UKG Pro test environment.
- **Rate limits:** No numeric limit published; UKG applies gateway quotas over roughly one minute.
- **Authentication:** Uses a Web Services account's username and password, plus a Customer API Key sent in a header.
- **Webhooks:** Virtual webhooks - employee created and updated events

> Facts synced from Apideck's connector metadata API — `GET /connector/connectors/ukg-pro` (`overview` field) is the live, authoritative version.

## When to use this skill

Activate this skill when the user explicitly wants to work with **UKG Pro** — for example, "sync employees in UKG Pro" or "list time-off requests in UKG Pro". This skill teaches the agent:

1. Which Apideck unified API covers UKG Pro (HRIS)
2. The correct `serviceId` to pass on every call (`ukg-pro`)
3. UKG Pro-specific auth and coverage caveats

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

// List employees in UKG Pro
const { data } = await apideck.hris.employees.list({
  serviceId: "ukg-pro",
});
```

## Portable across 58 HRIS connectors

The Apideck **HRIS** unified API exposes the same methods for every connector in its catalog. Switching from UKG Pro to another HRIS connector is a one-string change — no rewrite, no new SDK.

```typescript
// Today — UKG Pro
await apideck.hris.employees.list({ serviceId: "ukg-pro" });

// Tomorrow — same code, different connector
await apideck.hris.employees.list({ serviceId: "bamboohr" });
await apideck.hris.employees.list({ serviceId: "workday" });
```

This is the compounding advantage of using Apideck over integrating UKG Pro directly: code against the unified HRIS API once, gain access to every connector in it. New connectors Apideck adds become available to your app without code changes.

## Authentication

- **Type:** Basic auth (username/password)
- **Managed by:** Apideck Vault — credentials are collected through the Vault modal and stored encrypted server-side.
- **Note:** basic auth connectors often require manual rotation by the end user. If auth fails persistently, prompt them to re-enter credentials in Vault.

See [`apideck-best-practices`](../../skills/apideck-best-practices/) for Vault setup, connection lifecycle, and handling re-auth flows.

## Verifying coverage

Not every HRIS operation is supported by every connector. Always verify before assuming a method works:

```bash
curl 'https://unify.apideck.com/connector/connectors/ukg-pro' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}"
```

See [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) for patterns around `UnsupportedOperationError` and connector-specific fallbacks.

## Escape hatch: Proxy API

When an endpoint isn't covered by the HRIS unified API, use Apideck's Proxy to call UKG Pro directly — Apideck injects auth headers and handles token refresh. Set `x-apideck-downstream-url` to the target endpoint on UKG Pro's own API:

```bash
curl 'https://unify.apideck.com/proxy' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}" \
  -H "x-apideck-consumer-id: ${CONSUMER_ID}" \
  -H "x-apideck-service-id: ukg-pro" \
  -H "x-apideck-downstream-url: <target endpoint on UKG Pro>" \
  -H "x-apideck-downstream-method: GET"
```

See [UKG Pro's API docs](#) for available endpoints.

## Sibling connectors

Other **HRIS** connectors that share this unified API surface (same method signatures, just change `serviceId`):

[`bamboohr`](../bamboohr/), [`workday`](../workday/), [`deel`](../deel/) *(beta)*, [`hibob`](../hibob/), [`personio`](../personio/), [`adp-ihcm`](../adp-ihcm/) *(beta)*, [`adp-workforce-now`](../adp-workforce-now/) *(beta)*, [`paychex`](../paychex/) *(beta)*, and 49 more.

## See also

- [HRIS OpenAPI spec](https://specs.apideck.com/hris.yml) · [API Explorer](https://developers.apideck.com/api-explorer?id=hris)
- [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) — programmatic coverage checks
- [`apideck-best-practices`](../../skills/apideck-best-practices/) — architecture, Vault, pagination, error handling
- [`apideck-node`](../../skills/apideck-node/) — TypeScript / Node SDK patterns
