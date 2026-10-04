---
name: adp-run
description: |
  RUN Powered by ADP integration via Apideck's HRIS unified API — same methods work across every connector in HRIS, switch by changing `serviceId`. Use when the user wants to read or sync employees, departments, payrolls, and time-off records in RUN Powered by ADP. Routes through Apideck with serviceId "adp-run".
license: Apache-2.0
alwaysApply: false
metadata:
  author: apideck
  version: "1.0.0"
  serviceId: adp-run
  unifiedApis: ["hris"]
  authType: oauth2
  tier: "2"
  verified: true
  status: beta
  difficulty: highly_complex
  partnershipRequired: true
  sandboxAvailable: true
---

# RUN Powered by ADP (via Apideck)

Access RUN Powered by ADP through Apideck's **HRIS** unified API — one of 58 HRIS connectors that share the same method surface. Code you write here ports to BambooHR, Workday, Deel and 54 other HRIS connectors by changing a single `serviceId` string. Apideck handles auth, pagination, rate limiting, and retries so you don't write per-tenant RUN Powered by ADP plumbing.

> **Beta connector.** RUN Powered by ADP is currently in beta on Apideck. Expect partial resource coverage and occasional mapping gaps. Always verify coverage (see below) and fall back to the Proxy API for unsupported operations.

## Quick facts

- **Apideck serviceId:** `adp-run`
- **Unified API:** HRIS
- **Auth type:** oauth2
- **Status:** beta
- **Gotchas:** [page](https://developers.apideck.com/apis/hris/adp-run/gotchas)
- **RUN Powered by ADP docs:** https://developers.adp.com
- **Homepage:** https://www.adp.com/what-we-offer/products/run-powered-by-adp.aspx

## At a glance

- **Implementation difficulty:** highly complex — ADP Marketplace Partnership + Security Review + Custom Auth
- **Vendor partnership required:** yes ([ADP Marketplace Partner Program](https://partners.adp.com/gettingstarted/)) — ADP offers no API Central for RUN, so the ADP Marketplace Partner Program is the only route to RUN data; joining provides sandbox access.
- **Apideck-managed credentials:** not available — You supply your own ADP credentials.
- **Account type required:** A RUN Powered by ADP account in the United States; RUN is ADP's small-business product, aimed at roughly 1 to 49 employees.
- **Consumer access level:** A RUN administrator with authority to add an app to the account and grant it consent.
- **Sandbox:** available — Provided once you are enrolled as an ADP Marketplace partner.
- **Costs:** ADP publishes no fee: partner terms are a negotiated revenue share, on your side rather than your consumer's. No add-on for them to buy.
- **Rate limits:** 300 requests/minute per integration project and a maximum of 50 concurrent requests; ADP returns HTTP 429 beyond either limit.
- **Authentication:** Client credentials over mutual TLS, not a user-consent flow. Credentials are held once for your integration, not per connection.
- **Webhooks:** Virtual webhooks - Apideck polls for employee created and updated events

**Important to know:**

- This connector is in beta and has never been verified against a live RUN account: it was mapped from ADP's documentation alone. Treat connectivity and field-level behaviour alike as unproven, and prove both on your own tenant before committing to a build.
- Enrolling is a real gate, not a form: ADP requires a signed Developer's Participation Agreement and puts your integration through a security review that includes a penetration test.
- Consumer onboarding happens in ADP Marketplace, not in your product: each consumer must add your listed app there before any of their data can be read, and you cannot do that step on their behalf.
- Check which ADP product a prospective consumer actually runs before scoping this connector. Those on ADP Workforce Now or ADP iHCM need a different route entirely, and Apideck supports both as separate connectors.

> Facts synced from Apideck's connector metadata API — `GET /connector/connectors/adp-run` (`overview` field) is the live, authoritative version.

## When to use this skill

Activate this skill when the user explicitly wants to work with **RUN Powered by ADP** — for example, "sync employees in RUN Powered by ADP" or "list time-off requests in RUN Powered by ADP". This skill teaches the agent:

1. Which Apideck unified API covers RUN Powered by ADP (HRIS)
2. The correct `serviceId` to pass on every call (`adp-run`)
3. RUN Powered by ADP-specific auth and coverage caveats

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

// List employees in RUN Powered by ADP
const { data } = await apideck.hris.employees.list({
  serviceId: "adp-run",
});
```

## Portable across 58 HRIS connectors

The Apideck **HRIS** unified API exposes the same methods for every connector in its catalog. Switching from RUN Powered by ADP to another HRIS connector is a one-string change — no rewrite, no new SDK.

```typescript
// Today — RUN Powered by ADP
await apideck.hris.employees.list({ serviceId: "adp-run" });

// Tomorrow — same code, different connector
await apideck.hris.employees.list({ serviceId: "bamboohr" });
await apideck.hris.employees.list({ serviceId: "workday" });
```

This is the compounding advantage of using Apideck over integrating RUN Powered by ADP directly: code against the unified HRIS API once, gain access to every connector in it. New connectors Apideck adds become available to your app without code changes.

## Authentication

- **Type:** OAuth 2.0
- **Managed by:** Apideck Vault — Apideck handles the full OAuth dance (authorization code flow, token exchange, refresh). Never ask the user for API keys or tokens directly.
- **User setup:** Users authorize via the Vault modal. Connection state progresses `available → added → authorized → callable`.
- **Token refresh:** automatic. Expired tokens are refreshed transparently on the next API call.

See [`apideck-best-practices`](../../skills/apideck-best-practices/) for Vault setup, connection lifecycle, and handling re-auth flows.

## Verifying coverage

Not every HRIS operation is supported by every connector. Always verify before assuming a method works:

```bash
curl 'https://unify.apideck.com/connector/connectors/adp-run' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}"
```

See [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) for patterns around `UnsupportedOperationError` and connector-specific fallbacks.

## Escape hatch: Proxy API

When an endpoint isn't covered by the HRIS unified API, use Apideck's Proxy to call RUN Powered by ADP directly — Apideck injects auth headers and handles token refresh. Set `x-apideck-downstream-url` to the target endpoint on RUN Powered by ADP's own API:

```bash
curl 'https://unify.apideck.com/proxy' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}" \
  -H "x-apideck-consumer-id: ${CONSUMER_ID}" \
  -H "x-apideck-service-id: adp-run" \
  -H "x-apideck-downstream-url: <target endpoint on RUN Powered by ADP>" \
  -H "x-apideck-downstream-method: GET"
```

See [RUN Powered by ADP's API docs](https://developers.adp.com) for available endpoints.

## Sibling connectors

Other **HRIS** connectors that share this unified API surface (same method signatures, just change `serviceId`):

[`bamboohr`](../bamboohr/), [`workday`](../workday/), [`deel`](../deel/) *(beta)*, [`hibob`](../hibob/), [`personio`](../personio/), [`adp-ihcm`](../adp-ihcm/) *(beta)*, [`adp-workforce-now`](../adp-workforce-now/) *(beta)*, [`paychex`](../paychex/) *(beta)*, and 49 more.

## See also

- [HRIS OpenAPI spec](https://specs.apideck.com/hris.yml) · [API Explorer](https://developers.apideck.com/api-explorer?id=hris)
- [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) — programmatic coverage checks
- [`apideck-best-practices`](../../skills/apideck-best-practices/) — architecture, Vault, pagination, error handling
- [`apideck-node`](../../skills/apideck-node/) — TypeScript / Node SDK patterns
- [RUN Powered by ADP official docs](https://developers.adp.com)
