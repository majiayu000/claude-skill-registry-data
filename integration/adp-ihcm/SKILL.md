---
name: adp-ihcm
description: |
  ADP iHCM integration via Apideck's HRIS unified API — same methods work across every connector in HRIS, switch by changing `serviceId`. Use when the user wants to read or sync employees, departments, payrolls, and time-off records in ADP iHCM. Routes through Apideck with serviceId "adp-ihcm".
license: Apache-2.0
alwaysApply: false
metadata:
  author: apideck
  version: "1.0.0"
  serviceId: adp-ihcm
  unifiedApis: ["hris"]
  authType: oauth2
  tier: "1c"
  verified: true
  status: beta
  difficulty: highly_complex
  partnershipRequired: false
  sandboxAvailable: false
---

# ADP iHCM (via Apideck)

Access ADP iHCM through Apideck's **HRIS** unified API — one of 58 HRIS connectors that share the same method surface. Code you write here ports to BambooHR, Workday, Deel and 54 other HRIS connectors by changing a single `serviceId` string. Apideck handles auth, pagination, rate limiting, and retries so you don't write per-tenant ADP iHCM plumbing.

> **Beta connector.** ADP iHCM is currently in beta on Apideck. Expect partial resource coverage and occasional mapping gaps. Always verify coverage (see below) and fall back to the Proxy API for unsupported operations.

## Quick facts

- **Apideck serviceId:** `adp-ihcm`
- **Unified API:** HRIS
- **Auth type:** oauth2
- **Status:** beta
- **Gotchas:** [page](https://developers.apideck.com/apis/hris/adp-ihcm/gotchas)
- **ADP iHCM docs:** https://developers.adp.com
- **Homepage:** https://www.adp.com/

## At a glance

- **Implementation difficulty:** highly complex — Custom Auth + Multi-Step Per-Consumer Setup
- **Vendor partnership required:** no — The ADP Marketplace Partner Program is a separate route that adds a sandbox and partner API access under a partner agreement; API Central needs no partnership.
- **Apideck-managed credentials:** not available — Each consumer provisions their own ADP credentials and certificate.
- **Account type required:** An ADP iHCM account, ADP's HR and payroll platform outside the US and Canada, with ADP API Central enabled.
- **Consumer access level:** An ADP administrator who can enable API Central for the account and obtain the certificate and credentials.
- **Sandbox:** not available — A test instance exists only inside ADP's Marketplace Partner enrollment, which this connection model does not use.
- **Costs:** Paid by the consumer: ADP bills API Central International as a recurring subscription; prices are shown after signing in. No free trial.
- **Rate limits:** 120 requests/minute per API Central project and a maximum of 10 concurrent requests; ADP returns HTTP 429 beyond either limit.
- **Authentication:** Client credentials over mutual TLS on ADP's EU infrastructure, not a user-consent flow. Needs an X.509 client certificate, Client ID and Secret.
- **Webhooks:** Virtual webhooks - Apideck polls for employee created and updated events

**Important to know:**

- An iHCM subscription alone never yields credentials: the consumer must have ADP API Central enabled first. Plan for that decision landing inside your onboarding flow rather than before it.
- Consumers in the US or Canada are not on iHCM: ADP sells Workforce Now there, which Apideck supports through a separate connector. Confirm which ADP platform a consumer runs before pointing them at this one.
- The connection depends on a client certificate and stops working the moment it lapses: a dated, per-connection failure that lands long after the build is finished.
- You cannot de-risk this build before a consumer commits: your first end-to-end test necessarily runs against that consumer's live iHCM tenant.

> Facts synced from Apideck's connector metadata API — `GET /connector/connectors/adp-ihcm` (`overview` field) is the live, authoritative version.

## When to use this skill

Activate this skill when the user explicitly wants to work with **ADP iHCM** — for example, "sync employees in ADP iHCM" or "list time-off requests in ADP iHCM". This skill teaches the agent:

1. Which Apideck unified API covers ADP iHCM (HRIS)
2. The correct `serviceId` to pass on every call (`adp-ihcm`)
3. ADP iHCM-specific auth and coverage caveats

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

// List employees in ADP iHCM
const { data } = await apideck.hris.employees.list({
  serviceId: "adp-ihcm",
});
```

## Portable across 58 HRIS connectors

The Apideck **HRIS** unified API exposes the same methods for every connector in its catalog. Switching from ADP iHCM to another HRIS connector is a one-string change — no rewrite, no new SDK.

```typescript
// Today — ADP iHCM
await apideck.hris.employees.list({ serviceId: "adp-ihcm" });

// Tomorrow — same code, different connector
await apideck.hris.employees.list({ serviceId: "bamboohr" });
await apideck.hris.employees.list({ serviceId: "workday" });
```

This is the compounding advantage of using Apideck over integrating ADP iHCM directly: code against the unified HRIS API once, gain access to every connector in it. New connectors Apideck adds become available to your app without code changes.

## Authentication

- **Type:** OAuth 2.0
- **Managed by:** Apideck Vault — Apideck handles the full OAuth dance (authorization code flow, token exchange, refresh). Never ask the user for API keys or tokens directly.
- **User setup:** Users authorize via the Vault modal. Connection state progresses `available → added → authorized → callable`.
- **Token refresh:** automatic. Expired tokens are refreshed transparently on the next API call.

See [`apideck-best-practices`](../../skills/apideck-best-practices/) for Vault setup, connection lifecycle, and handling re-auth flows.

## Verifying coverage

Not every HRIS operation is supported by every connector. Always verify before assuming a method works:

```bash
curl 'https://unify.apideck.com/connector/connectors/adp-ihcm' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}"
```

See [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) for patterns around `UnsupportedOperationError` and connector-specific fallbacks.

## Escape hatch: Proxy API

When an endpoint isn't covered by the HRIS unified API, use Apideck's Proxy to call ADP iHCM directly — Apideck injects auth headers and handles token refresh. Set `x-apideck-downstream-url` to the target endpoint on ADP iHCM's own API:

```bash
curl 'https://unify.apideck.com/proxy' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}" \
  -H "x-apideck-consumer-id: ${CONSUMER_ID}" \
  -H "x-apideck-service-id: adp-ihcm" \
  -H "x-apideck-downstream-url: <target endpoint on ADP iHCM>" \
  -H "x-apideck-downstream-method: GET"
```

See [ADP iHCM's API docs](https://developers.adp.com) for available endpoints.

## Sibling connectors

Other **HRIS** connectors that share this unified API surface (same method signatures, just change `serviceId`):

[`bamboohr`](../bamboohr/), [`workday`](../workday/), [`deel`](../deel/) *(beta)*, [`hibob`](../hibob/), [`personio`](../personio/), [`adp-workforce-now`](../adp-workforce-now/) *(beta)*, [`paychex`](../paychex/) *(beta)*, [`paylocity`](../paylocity/), and 49 more.

## See also

- [HRIS OpenAPI spec](https://specs.apideck.com/hris.yml) · [API Explorer](https://developers.apideck.com/api-explorer?id=hris)
- [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) — programmatic coverage checks
- [`apideck-best-practices`](../../skills/apideck-best-practices/) — architecture, Vault, pagination, error handling
- [`apideck-node`](../../skills/apideck-node/) — TypeScript / Node SDK patterns
- [ADP iHCM official docs](https://developers.adp.com)
