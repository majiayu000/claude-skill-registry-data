---
name: breathehr
description: |
  Breathe HR integration via Apideck's HRIS unified API — same methods work across every connector in HRIS, switch by changing `serviceId`. Use when the user wants to read or sync employees, departments, payrolls, and time-off records in Breathe HR. Routes through Apideck with serviceId "breathehr".
license: Apache-2.0
alwaysApply: false
metadata:
  author: apideck
  version: "1.0.0"
  serviceId: breathehr
  unifiedApis: ["hris"]
  authType: apiKey
  tier: "2"
  verified: true
  difficulty: moderate
  partnershipRequired: false
  sandboxAvailable: true
---

# Breathe HR (via Apideck)

Access Breathe HR through Apideck's **HRIS** unified API — one of 58 HRIS connectors that share the same method surface. Code you write here ports to BambooHR, Workday, Deel and 54 other HRIS connectors by changing a single `serviceId` string. Apideck handles auth, pagination, rate limiting, and retries so you don't write per-tenant Breathe HR plumbing.

## Quick facts

- **Apideck serviceId:** `breathehr`
- **Unified API:** HRIS
- **Auth type:** apiKey
- **Gotchas:** [page](https://developers.apideck.com/apis/hris/breathehr/gotchas)
- **Breathe HR docs:** https://developer.breathehr.com
- **Homepage:** https://www.breathehr.com/

## At a glance

- **Implementation difficulty:** moderate — API key authentication, where the consumer creates the credential manually
- **Vendor partnership required:** no ([developer portal](https://www.breathehr.com/en-gb/partners)) — Breathe's partner programme is a commercial referral arrangement for HR consultants and resellers, not a gate on API access.
- **Apideck-managed credentials:** not available — Each Breathe API key is tied to one Breathe account, so every consumer supplies their own.
- **Account type required:** Any active Breathe account.
- **Consumer access level:** Account Admin. Only an Admin can switch the API on and read the key.
- **Sandbox:** available ([signup](https://developer.breathehr.com/)) — Free developer sandbox, available self-service from developer.breathehr.com.
- **Costs:** Included in a Breathe subscription at no extra charge. Consumers need an active plan: Breathe offers a 14-day free trial but no permanent free tier.
- **Rate limits:** 60 requests per 60 seconds per Breathe account; beyond that Breathe returns HTTP 429.
- **Authentication:** Sent in the x-api-key header, not OAuth. The key carries the permissions of the whole Breathe account and does not expire on a schedule.
- **Webhooks:** Virtual webhooks (Apideck polls Breathe for employee created, updated and terminated events)

**Important to know:**

- One API key grants full access to the consumer's Breathe account: Breathe has no scoped permissions, and the only way to withdraw access is to regenerate the key. Make clear what the consumer is granting before they hand it over.
- Breathe is a UK-focused SME platform, so its HR data follows UK conventions such as holiday allowances and UK leave types. Expect that shape in the unified model, and check the fit if your integration targets other regions.

> Facts synced from Apideck's connector metadata API — `GET /connector/connectors/breathehr` (`overview` field) is the live, authoritative version.

## When to use this skill

Activate this skill when the user explicitly wants to work with **Breathe HR** — for example, "sync employees in Breathe HR" or "list time-off requests in Breathe HR". This skill teaches the agent:

1. Which Apideck unified API covers Breathe HR (HRIS)
2. The correct `serviceId` to pass on every call (`breathehr`)
3. Breathe HR-specific auth and coverage caveats

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

// List employees in Breathe HR
const { data } = await apideck.hris.employees.list({
  serviceId: "breathehr",
});
```

## Portable across 58 HRIS connectors

The Apideck **HRIS** unified API exposes the same methods for every connector in its catalog. Switching from Breathe HR to another HRIS connector is a one-string change — no rewrite, no new SDK.

```typescript
// Today — Breathe HR
await apideck.hris.employees.list({ serviceId: "breathehr" });

// Tomorrow — same code, different connector
await apideck.hris.employees.list({ serviceId: "bamboohr" });
await apideck.hris.employees.list({ serviceId: "workday" });
```

This is the compounding advantage of using Apideck over integrating Breathe HR directly: code against the unified HRIS API once, gain access to every connector in it. New connectors Apideck adds become available to your app without code changes.

## Authentication

- **Type:** API Key
- **Managed by:** Apideck Vault — the user pastes their Breathe HR API key into the Vault modal; Apideck stores it encrypted and injects it on every request.
- **Rotation:** if the user rotates their key, they re-enter it in Vault. No code changes needed.

See [`apideck-best-practices`](../../skills/apideck-best-practices/) for Vault setup, connection lifecycle, and handling re-auth flows.

## Verifying coverage

Not every HRIS operation is supported by every connector. Always verify before assuming a method works:

```bash
curl 'https://unify.apideck.com/connector/connectors/breathehr' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}"
```

See [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) for patterns around `UnsupportedOperationError` and connector-specific fallbacks.

## Escape hatch: Proxy API

When an endpoint isn't covered by the HRIS unified API, use Apideck's Proxy to call Breathe HR directly — Apideck injects auth headers and handles token refresh. Set `x-apideck-downstream-url` to the target endpoint on Breathe HR's own API:

```bash
curl 'https://unify.apideck.com/proxy' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}" \
  -H "x-apideck-consumer-id: ${CONSUMER_ID}" \
  -H "x-apideck-service-id: breathehr" \
  -H "x-apideck-downstream-url: <target endpoint on Breathe HR>" \
  -H "x-apideck-downstream-method: GET"
```

See [Breathe HR's API docs](https://developer.breathehr.com) for available endpoints.

## Sibling connectors

Other **HRIS** connectors that share this unified API surface (same method signatures, just change `serviceId`):

[`bamboohr`](../bamboohr/), [`workday`](../workday/), [`deel`](../deel/) *(beta)*, [`hibob`](../hibob/), [`personio`](../personio/), [`adp-ihcm`](../adp-ihcm/) *(beta)*, [`adp-workforce-now`](../adp-workforce-now/) *(beta)*, [`paychex`](../paychex/) *(beta)*, and 49 more.

## See also

- [HRIS OpenAPI spec](https://specs.apideck.com/hris.yml) · [API Explorer](https://developers.apideck.com/api-explorer?id=hris)
- [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) — programmatic coverage checks
- [`apideck-best-practices`](../../skills/apideck-best-practices/) — architecture, Vault, pagination, error handling
- [`apideck-node`](../../skills/apideck-node/) — TypeScript / Node SDK patterns
- [Breathe HR official docs](https://developer.breathehr.com)
