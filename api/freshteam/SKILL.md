---
name: freshteam
description: |
  Freshteam integration via Apideck's HRIS, ATS unified API — same methods work across every connector in HRIS, ATS, switch by changing `serviceId`. Use when the user wants to read or sync employees, departments, payrolls, and time-off records in Freshteam. Routes through Apideck with serviceId "freshteam".
license: Apache-2.0
alwaysApply: false
metadata:
  author: apideck
  version: "1.0.0"
  serviceId: freshteam
  unifiedApis: ["hris", "ats"]
  authType: apiKey
  tier: "2"
  verified: true
---

# Freshteam (via Apideck)

Access Freshteam through Apideck's **HRIS, ATS** unified API — one of 58 HRIS connectors that share the same method surface. Code you write here ports to BambooHR, Workday, Deel and 54 other HRIS connectors by changing a single `serviceId` string. Apideck handles auth, pagination, rate limiting, and retries so you don't write per-tenant Freshteam plumbing.

## Quick facts

- **Apideck serviceId:** `freshteam`
- **Unified APIs:** HRIS, ATS
- **Auth type:** apiKey
- **Freshteam docs:** https://developers.freshworks.com/freshteam/
- **Homepage:** https://www.freshworks.com/hrms/

## When to use this skill

Activate this skill when the user explicitly wants to work with **Freshteam** — for example, "sync employees in Freshteam" or "list time-off requests in Freshteam". This skill teaches the agent:

1. Which Apideck unified API covers Freshteam (HRIS, ATS)
2. The correct `serviceId` to pass on every call (`freshteam`)
3. Freshteam-specific auth and coverage caveats

For the full method surface (parameters, pagination, filtering), use your language SDK skill:

- [`apideck-node`](../../skills/apideck-node/), [`apideck-python`](../../skills/apideck-python/), [`apideck-dotnet`](../../skills/apideck-dotnet/), [`apideck-java`](../../skills/apideck-java/), [`apideck-go`](../../skills/apideck-go/), [`apideck-php`](../../skills/apideck-php/), or [`apideck-rest`](../../skills/apideck-rest/)

For the raw OpenAPI spec:

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

// List employees in Freshteam
const { data } = await apideck.hris.employees.list({
  serviceId: "freshteam",
});
```

## Portable across 58 HRIS connectors

The Apideck **HRIS** unified API exposes the same methods for every connector in its catalog. Switching from Freshteam to another HRIS connector is a one-string change — no rewrite, no new SDK.

```typescript
// Today — Freshteam
await apideck.hris.employees.list({ serviceId: "freshteam" });

// Tomorrow — same code, different connector
await apideck.hris.employees.list({ serviceId: "bamboohr" });
await apideck.hris.employees.list({ serviceId: "workday" });
```

This is the compounding advantage of using Apideck over integrating Freshteam directly: code against the unified HRIS API once, gain access to every connector in it. New connectors Apideck adds become available to your app without code changes.

## Authentication

- **Type:** API Key
- **Managed by:** Apideck Vault — the user pastes their Freshteam API key into the Vault modal; Apideck stores it encrypted and injects it on every request.
- **Rotation:** if the user rotates their key, they re-enter it in Vault. No code changes needed.

See [`apideck-best-practices`](../../skills/apideck-best-practices/) for Vault setup, connection lifecycle, and handling re-auth flows.

## Verifying coverage

Not every HRIS operation is supported by every connector. Always verify before assuming a method works:

```bash
curl 'https://unify.apideck.com/connector/connectors/freshteam' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}"
```

See [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) for patterns around `UnsupportedOperationError` and connector-specific fallbacks.

## Escape hatch: Proxy API

When an endpoint isn't covered by the HRIS unified API, use Apideck's Proxy to call Freshteam directly — Apideck injects auth headers and handles token refresh. Set `x-apideck-downstream-url` to the target endpoint on Freshteam's own API:

```bash
curl 'https://unify.apideck.com/proxy' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}" \
  -H "x-apideck-consumer-id: ${CONSUMER_ID}" \
  -H "x-apideck-service-id: freshteam" \
  -H "x-apideck-downstream-url: <target endpoint on Freshteam>" \
  -H "x-apideck-downstream-method: GET"
```

See [Freshteam's API docs](https://developers.freshworks.com/freshteam/) for available endpoints.

## Sibling connectors

Other **HRIS** connectors that share this unified API surface (same method signatures, just change `serviceId`):

[`bamboohr`](../bamboohr/), [`workday`](../workday/), [`deel`](../deel/) *(beta)*, [`hibob`](../hibob/), [`personio`](../personio/), [`adp-ihcm`](../adp-ihcm/) *(beta)*, [`adp-workforce-now`](../adp-workforce-now/) *(beta)*, [`paychex`](../paychex/) *(beta)*, and 49 more.

Other **ATS** connectors that share this unified API surface (same method signatures, just change `serviceId`):

[`greenhouse`](../greenhouse/), [`workday`](../workday/), [`lever`](../lever/), [`workable`](../workable/) *(beta)*, [`bullhorn-ats`](../bullhorn-ats/) *(beta)*, [`teamtailor`](../teamtailor/) *(beta)*, [`jobadder`](../jobadder/) *(beta)*, [`recruitee`](../recruitee/), and 2 more.

## See also

- [HRIS OpenAPI spec](https://specs.apideck.com/hris.yml) · [API Explorer](https://developers.apideck.com/api-explorer?id=hris)
- [ATS OpenAPI spec](https://specs.apideck.com/ats.yml) · [API Explorer](https://developers.apideck.com/api-explorer?id=ats)
- [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) — programmatic coverage checks
- [`apideck-best-practices`](../../skills/apideck-best-practices/) — architecture, Vault, pagination, error handling
- [`apideck-node`](../../skills/apideck-node/) — TypeScript / Node SDK patterns
- [Freshteam official docs](https://developers.freshworks.com/freshteam/)
