---
name: okta
description: |
  Okta integration via Apideck's HRIS unified API — same methods work across every connector in HRIS, switch by changing `serviceId`. Use when the user wants to read or sync employees, departments, payrolls, and time-off records in Okta. Routes through Apideck with serviceId "okta".
license: Apache-2.0
alwaysApply: false
metadata:
  author: apideck
  version: "1.0.0"
  serviceId: okta
  unifiedApis: ["hris"]
  authType: apiKey
  tier: "2"
  verified: true
  status: beta
  difficulty: moderate
  partnershipRequired: false
  sandboxAvailable: true
---

# Okta (via Apideck)

Access Okta through Apideck's **HRIS** unified API — one of 58 HRIS connectors that share the same method surface. Code you write here ports to BambooHR, Workday, Deel and 54 other HRIS connectors by changing a single `serviceId` string. Apideck handles auth, pagination, rate limiting, and retries so you don't write per-tenant Okta plumbing.

> **Beta connector.** Okta is currently in beta on Apideck. Expect partial resource coverage and occasional mapping gaps. Always verify coverage (see below) and fall back to the Proxy API for unsupported operations.

## Quick facts

- **Apideck serviceId:** `okta`
- **Unified API:** HRIS
- **Auth type:** apiKey
- **Status:** beta
- **Gotchas:** [page](https://developers.apideck.com/apis/hris/okta/gotchas)
- **Homepage:** https://www.okta.com/

## At a glance

- **Implementation difficulty:** moderate — API Token Authentication - Each Consumer Creates Their Own Token in Okta
- **Vendor partnership required:** no — No partner programme gates API access.
- **Apideck-managed credentials:** not available — Each consumer creates their own API token in their own Okta org.
- **Account type required:** An Okta organisation (Workforce Identity).
- **Consumer access level:** An Okta administrator; the token inherits that admin's privileges.
- **Sandbox:** available ([signup](https://developer.okta.com/signup/)) — Integrator Free Plan org, signed up with a business email, for building and testing; it deactivates after 90 days without a sign-in.
- **Costs:** API access is included with an Okta org.
- **Rate limits:** Set per Okta org by plan; a new API token gets 50 percent of each API's maximum by default.
- **Authentication:** An Okta API token plus the consumer's Okta domain.
- **Webhooks:** Native - employee created, updated, deleted and terminated events

**Important to know:**

- Okta is an identity provider, not an HR system of record. Employees are Okta users, so what comes back depends on the profile attributes the consumer's org has configured.
- Each connection with webhooks registers an event hook in the consumer's Okta org, which allows at most 25 active and verified event hooks, so consumers with many existing hooks may hit that cap.

> Facts synced from Apideck's connector metadata API — `GET /connector/connectors/okta` (`overview` field) is the live, authoritative version.

## When to use this skill

Activate this skill when the user explicitly wants to work with **Okta** — for example, "sync employees in Okta" or "list time-off requests in Okta". This skill teaches the agent:

1. Which Apideck unified API covers Okta (HRIS)
2. The correct `serviceId` to pass on every call (`okta`)
3. Okta-specific auth and coverage caveats

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

// List employees in Okta
const { data } = await apideck.hris.employees.list({
  serviceId: "okta",
});
```

## Portable across 58 HRIS connectors

The Apideck **HRIS** unified API exposes the same methods for every connector in its catalog. Switching from Okta to another HRIS connector is a one-string change — no rewrite, no new SDK.

```typescript
// Today — Okta
await apideck.hris.employees.list({ serviceId: "okta" });

// Tomorrow — same code, different connector
await apideck.hris.employees.list({ serviceId: "bamboohr" });
await apideck.hris.employees.list({ serviceId: "workday" });
```

This is the compounding advantage of using Apideck over integrating Okta directly: code against the unified HRIS API once, gain access to every connector in it. New connectors Apideck adds become available to your app without code changes.

## Authentication

- **Type:** API Key
- **Managed by:** Apideck Vault — the user pastes their Okta API key into the Vault modal; Apideck stores it encrypted and injects it on every request.
- **Rotation:** if the user rotates their key, they re-enter it in Vault. No code changes needed.

See [`apideck-best-practices`](../../skills/apideck-best-practices/) for Vault setup, connection lifecycle, and handling re-auth flows.

## Verifying coverage

Not every HRIS operation is supported by every connector. Always verify before assuming a method works:

```bash
curl 'https://unify.apideck.com/connector/connectors/okta' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}"
```

See [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) for patterns around `UnsupportedOperationError` and connector-specific fallbacks.

## Escape hatch: Proxy API

When an endpoint isn't covered by the HRIS unified API, use Apideck's Proxy to call Okta directly — Apideck injects auth headers and handles token refresh. Set `x-apideck-downstream-url` to the target endpoint on Okta's own API:

```bash
curl 'https://unify.apideck.com/proxy' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}" \
  -H "x-apideck-consumer-id: ${CONSUMER_ID}" \
  -H "x-apideck-service-id: okta" \
  -H "x-apideck-downstream-url: <target endpoint on Okta>" \
  -H "x-apideck-downstream-method: GET"
```

See [Okta's API docs](#) for available endpoints.

## Sibling connectors

Other **HRIS** connectors that share this unified API surface (same method signatures, just change `serviceId`):

[`bamboohr`](../bamboohr/), [`workday`](../workday/), [`deel`](../deel/) *(beta)*, [`hibob`](../hibob/), [`personio`](../personio/), [`adp-ihcm`](../adp-ihcm/) *(beta)*, [`adp-workforce-now`](../adp-workforce-now/) *(beta)*, [`paychex`](../paychex/) *(beta)*, and 49 more.

## See also

- [HRIS OpenAPI spec](https://specs.apideck.com/hris.yml) · [API Explorer](https://developers.apideck.com/api-explorer?id=hris)
- [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) — programmatic coverage checks
- [`apideck-best-practices`](../../skills/apideck-best-practices/) — architecture, Vault, pagination, error handling
- [`apideck-node`](../../skills/apideck-node/) — TypeScript / Node SDK patterns
