---
name: linear
description: |
  Linear integration via Apideck's Issue Tracking unified API — same methods work across every connector in Issue Tracking, switch by changing `serviceId`. Use when the user wants to read, write, or comment on tickets and issues in Linear. Routes through Apideck with serviceId "linear".
license: Apache-2.0
alwaysApply: false
metadata:
  author: apideck
  version: "1.0.0"
  serviceId: linear
  unifiedApis: ["issue-tracking"]
  authType: oauth2
  tier: "1b"
  verified: true
  status: beta
  difficulty: straightforward
  partnershipRequired: false
  sandboxAvailable: false
---

# Linear (via Apideck)

Access Linear through Apideck's **Issue Tracking** unified API — one of 6 Issue Tracking connectors that share the same method surface. Code you write here ports to Jira, GitHub, GitLab and 2 other Issue Tracking connectors by changing a single `serviceId` string. Apideck handles auth, pagination, rate limiting, and retries so you don't write per-tenant Linear plumbing.

> **Beta connector.** Linear is currently in beta on Apideck. Expect partial resource coverage and occasional mapping gaps. Always verify coverage (see below) and fall back to the Proxy API for unsupported operations.

## Quick facts

- **Apideck serviceId:** `linear`
- **Unified API:** Issue Tracking
- **Auth type:** oauth2
- **Status:** beta
- **Gotchas:** [page](https://developers.apideck.com/apis/issue-tracking/linear/gotchas)
- **Linear docs:** https://developers.linear.app
- **Homepage:** https://linear.app/

## At a glance

- **Implementation difficulty:** straightforward — Self-Service OAuth App - No Linear Review, No Partnership, Free Workspace Sufficient
- **Vendor partnership required:** no ([Linear workspace settings](https://linear.app/settings/api/applications/new)) — Linear reviews an application only if you choose to submit it to the Linear integration directory, which is optional.
- **Apideck-managed credentials:** available — Consumers can connect before you register a Linear application of your own.
- **Account type required:** Any Linear plan. Creating the OAuth application needs a workspace admin; the person who connects does not.
- **Consumer access level:** The connection reaches what the authorising Linear user can already see, across the workspace's public teams.
- **Sandbox:** not available — Develop against a second free Linear workspace of your own; there is no separate test environment.
- **Costs:** No separate charge for API access. Linear includes it on every plan, the free one included.
- **Rate limits:** 5,000 requests an hour for each connected workspace, within a budget of 2,000,000 GraphQL complexity points over the same hour.
- **Authentication:** Authorization Code flow.
- **Webhooks:** Native - ticket created, updated and deleted.

**Important to know:**

- Linear attaches the webhook destination to the OAuth application itself, so events reach only an application owner running their own Linear OAuth application. Apideck's shared credentials cannot carry them.
- A new Linear OAuth application is private until it is switched to public distribution. Until then every consumer outside the workspace that created it is turned away, with nothing in the authorisation flow to explain why.
- Tickets and comments the integration writes land in Linear under the application's own name rather than under the person who authorised the connection. That is the opposite of Linear's default, so anyone who knows Linear will expect the other behaviour.

> Facts synced from Apideck's connector metadata API — `GET /connector/connectors/linear` (`overview` field) is the live, authoritative version.

## When to use this skill

Activate this skill when the user explicitly wants to work with **Linear** — for example, "create a ticket in Linear" or "comment on an issue in Linear". This skill teaches the agent:

1. Which Apideck unified API covers Linear (Issue Tracking)
2. The correct `serviceId` to pass on every call (`linear`)
3. Linear-specific auth and coverage caveats

For the full method surface (parameters, pagination, filtering), use your language SDK skill:

- [`apideck-node`](../../skills/apideck-node/), [`apideck-python`](../../skills/apideck-python/), [`apideck-dotnet`](../../skills/apideck-dotnet/), [`apideck-java`](../../skills/apideck-java/), [`apideck-go`](../../skills/apideck-go/), [`apideck-php`](../../skills/apideck-php/), or [`apideck-rest`](../../skills/apideck-rest/)

For the raw OpenAPI spec:

- **Issue Tracking:** [https://specs.apideck.com/issue-tracking.yml](https://specs.apideck.com/issue-tracking.yml) · [API Explorer](https://developers.apideck.com/api-explorer?id=issue-tracking)

## Minimal example (TypeScript)

```typescript
import { Apideck } from "@apideck/unify";

const apideck = new Apideck({
  apiKey: process.env.APIDECK_API_KEY,
  appId: process.env.APIDECK_APP_ID,
  consumerId: "your-consumer-id",
});

// List tickets in Linear
const { data } = await apideck.issueTracking.tickets.list({
  serviceId: "linear",
});
```

## Portable across 6 Issue Tracking connectors

The Apideck **Issue Tracking** unified API exposes the same methods for every connector in its catalog. Switching from Linear to another Issue Tracking connector is a one-string change — no rewrite, no new SDK.

```typescript
// Today — Linear
await apideck.issueTracking.tickets.list({ serviceId: "linear" });

// Tomorrow — same code, different connector
await apideck.issueTracking.tickets.list({ serviceId: "jira" });
await apideck.issueTracking.tickets.list({ serviceId: "github" });
```

This is the compounding advantage of using Apideck over integrating Linear directly: code against the unified Issue Tracking API once, gain access to every connector in it. New connectors Apideck adds become available to your app without code changes.

## Linear via Apideck Issue Tracking

Linear is a modern issue tracker for product teams. Apideck maps its Team/Issue model.

### Entity mapping

| Linear concept | Apideck Issue Tracking resource |
|---|---|
| Team | `collections` |
| Issue | `tickets` |
| Comment | ⚠️ coverage is evolving — check `/connector/connectors/linear` |
| User | ⚠️ coverage is evolving |
| Label | ⚠️ coverage is evolving |
| Project, Cycle | use Proxy (GraphQL) |

### Coverage highlights

- ✅ Team list (collections)
- ✅ Issues (tickets) — create, list, update, delete
- ⚠️ Users, comments, tags — may be partial; verify with coverage endpoint
- ❌ Projects, Cycles, Roadmaps — use Proxy with Linear's GraphQL API

### Auth

- **Type:** OAuth 2.0, managed by Apideck Vault
- **Workspace binding:** each connection targets one Linear workspace. For multi-workspace scenarios, use the separate `linear-multiworkspace` connector.
- **API:** Linear is GraphQL-only upstream; Apideck abstracts this. For raw GraphQL queries use Proxy.

### Example: list issues in a team

```typescript
const { data } = await apideck.issueTracking.collectionTickets.list({
  serviceId: "linear",
  collectionId: "team_abc123",
});
```

## Escape hatch: Proxy API

When an endpoint isn't covered by the Issue Tracking unified API, use Apideck's Proxy to call Linear directly — Apideck injects auth headers and handles token refresh. Set `x-apideck-downstream-url` to the target endpoint on Linear's own API:

```bash
curl 'https://unify.apideck.com/proxy' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}" \
  -H "x-apideck-consumer-id: ${CONSUMER_ID}" \
  -H "x-apideck-service-id: linear" \
  -H "x-apideck-downstream-url: <target endpoint on Linear>" \
  -H "x-apideck-downstream-method: GET"
```

See [Linear's API docs](https://developers.linear.app) for available endpoints.

## Sibling connectors

Other **Issue Tracking** connectors that share this unified API surface (same method signatures, just change `serviceId`):

[`jira`](../jira/) *(beta)*, [`github`](../github/) *(beta)*, [`gitlab`](../gitlab/) *(beta)*, [`gitlab-server`](../gitlab-server/) *(beta)*, [`linear-multiworkspace`](../linear-multiworkspace/) *(beta)*.

## See also

- [Issue Tracking OpenAPI spec](https://specs.apideck.com/issue-tracking.yml) · [API Explorer](https://developers.apideck.com/api-explorer?id=issue-tracking)
- [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) — programmatic coverage checks
- [`apideck-best-practices`](../../skills/apideck-best-practices/) — architecture, Vault, pagination, error handling
- [`apideck-node`](../../skills/apideck-node/) — TypeScript / Node SDK patterns
- [Linear official docs](https://developers.linear.app)
