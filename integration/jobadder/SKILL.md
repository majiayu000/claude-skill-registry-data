---
name: jobadder
description: |
  JobAdder integration via Apideck's ATS unified API — same methods work across every connector in ATS, switch by changing `serviceId`. Use when the user wants to read, write, or sync jobs, applicants, and applications in JobAdder. Routes through Apideck with serviceId "jobadder".
license: Apache-2.0
alwaysApply: false
metadata:
  author: apideck
  version: "1.0.0"
  serviceId: jobadder
  unifiedApis: ["ats"]
  authType: oauth2
  tier: "2"
  verified: true
  status: beta
  difficulty: moderate
  partnershipRequired: true
  sandboxAvailable: false
---

# JobAdder (via Apideck)

Access JobAdder through Apideck's **ATS** unified API — one of 11 ATS connectors that share the same method surface. Code you write here ports to Greenhouse, Workday, Lever and 7 other ATS connectors by changing a single `serviceId` string. Apideck handles auth, pagination, rate limiting, and retries so you don't write per-tenant JobAdder plumbing.

> **Beta connector.** JobAdder is currently in beta on Apideck. Expect partial resource coverage and occasional mapping gaps. Always verify coverage (see below) and fall back to the Proxy API for unsupported operations.

## Quick facts

- **Apideck serviceId:** `jobadder`
- **Unified API:** ATS
- **Auth type:** oauth2
- **Status:** beta
- **Gotchas:** [page](https://developers.apideck.com/apis/ats/jobadder/gotchas)
- **Homepage:** https://www.jobadder.com/

## At a glance

- **Implementation difficulty:** moderate — Self-Service OAuth App + JobAdder Approval Required Before Credentials Work
- **Vendor partnership required:** yes ([JobAdder developer portal](https://developers.jobadder.com/register)) — Registration is self-service, but JobAdder approves the developer account, then each application inside it. API team: api@jobadder.com.
- **Apideck-managed credentials:** not available — Each application owner registers their own JobAdder application.
- **Account type required:** JobAdder account on a plan that includes API access.
- **Consumer access level:** Any JobAdder user who can complete the authorisation. The connection then reaches only the data that user's account can access.
- **Sandbox:** not available — JobAdder provisions one only for contracted customers, and offers no free trial to develop against.
- **Costs:** JobAdder prices on quotation, with no published list price. API access is included only from the mid plans upward, so an entry-level plan cannot connect.
- **Rate limits:** None published. JobAdder's API terms reserve the right to impose limits at its own discretion, without stating a number.
- **Authentication:** Authorization Code flow.
- **Webhooks:** No webhooks (poll the API for changes).

**Important to know:**

- A refresh token expires after two weeks without use, and every use resets that two-week window. A connection in regular use therefore stays alive on its own, while one that goes quiet for a fortnight stops working and the consumer has to authorise again.
- Raise the approval with JobAdder's API team at the start of a build rather than at the end: until both approvals land, the client id and secret return errors, so there is nothing to build or test against.

> Facts synced from Apideck's connector metadata API — `GET /connector/connectors/jobadder` (`overview` field) is the live, authoritative version.

## When to use this skill

Activate this skill when the user explicitly wants to work with **JobAdder** — for example, "list open jobs in JobAdder" or "move an applicant through stages in JobAdder". This skill teaches the agent:

1. Which Apideck unified API covers JobAdder (ATS)
2. The correct `serviceId` to pass on every call (`jobadder`)
3. JobAdder-specific auth and coverage caveats

For the full method surface (parameters, pagination, filtering), use your language SDK skill:

- [`apideck-node`](../../skills/apideck-node/), [`apideck-python`](../../skills/apideck-python/), [`apideck-dotnet`](../../skills/apideck-dotnet/), [`apideck-java`](../../skills/apideck-java/), [`apideck-go`](../../skills/apideck-go/), [`apideck-php`](../../skills/apideck-php/), or [`apideck-rest`](../../skills/apideck-rest/)

For the raw OpenAPI spec:

- **ATS:** [https://specs.apideck.com/ats.yml](https://specs.apideck.com/ats.yml) · [API Explorer](https://developers.apideck.com/api-explorer?id=ats)

## Minimal example (TypeScript)

```typescript
import { Apideck } from "@apideck/unify";

const apideck = new Apideck({
  apiKey: process.env.APIDECK_API_KEY,
  appId: process.env.APIDECK_APP_ID,
  consumerId: "your-consumer-id",
});

// List applicants in JobAdder
const { data } = await apideck.ats.applicants.list({
  serviceId: "jobadder",
});
```

## Portable across 11 ATS connectors

The Apideck **ATS** unified API exposes the same methods for every connector in its catalog. Switching from JobAdder to another ATS connector is a one-string change — no rewrite, no new SDK.

```typescript
// Today — JobAdder
await apideck.ats.applicants.list({ serviceId: "jobadder" });

// Tomorrow — same code, different connector
await apideck.ats.applicants.list({ serviceId: "greenhouse" });
await apideck.ats.applicants.list({ serviceId: "workday" });
```

This is the compounding advantage of using Apideck over integrating JobAdder directly: code against the unified ATS API once, gain access to every connector in it. New connectors Apideck adds become available to your app without code changes.

## Authentication

- **Type:** OAuth 2.0
- **Managed by:** Apideck Vault — Apideck handles the full OAuth dance (authorization code flow, token exchange, refresh). Never ask the user for API keys or tokens directly.
- **User setup:** Users authorize via the Vault modal. Connection state progresses `available → added → authorized → callable`.
- **Token refresh:** automatic. Expired tokens are refreshed transparently on the next API call.

See [`apideck-best-practices`](../../skills/apideck-best-practices/) for Vault setup, connection lifecycle, and handling re-auth flows.

## Verifying coverage

Not every ATS operation is supported by every connector. Always verify before assuming a method works:

```bash
curl 'https://unify.apideck.com/connector/connectors/jobadder' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}"
```

See [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) for patterns around `UnsupportedOperationError` and connector-specific fallbacks.

## Escape hatch: Proxy API

When an endpoint isn't covered by the ATS unified API, use Apideck's Proxy to call JobAdder directly — Apideck injects auth headers and handles token refresh. Set `x-apideck-downstream-url` to the target endpoint on JobAdder's own API:

```bash
curl 'https://unify.apideck.com/proxy' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}" \
  -H "x-apideck-consumer-id: ${CONSUMER_ID}" \
  -H "x-apideck-service-id: jobadder" \
  -H "x-apideck-downstream-url: <target endpoint on JobAdder>" \
  -H "x-apideck-downstream-method: GET"
```

See [JobAdder's API docs](#) for available endpoints.

## Sibling connectors

Other **ATS** connectors that share this unified API surface (same method signatures, just change `serviceId`):

[`greenhouse`](../greenhouse/), [`workday`](../workday/), [`lever`](../lever/), [`workable`](../workable/) *(beta)*, [`bullhorn-ats`](../bullhorn-ats/) *(beta)*, [`teamtailor`](../teamtailor/) *(beta)*, [`freshteam`](../freshteam/), [`recruitee`](../recruitee/), and 2 more.

## See also

- [ATS OpenAPI spec](https://specs.apideck.com/ats.yml) · [API Explorer](https://developers.apideck.com/api-explorer?id=ats)
- [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) — programmatic coverage checks
- [`apideck-best-practices`](../../skills/apideck-best-practices/) — architecture, Vault, pagination, error handling
- [`apideck-node`](../../skills/apideck-node/) — TypeScript / Node SDK patterns
