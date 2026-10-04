---
name: gitlab
description: |
  GitLab integration via Apideck's Issue Tracking unified API — same methods work across every connector in Issue Tracking, switch by changing `serviceId`. Use when the user wants to read, write, or comment on tickets and issues in GitLab. Routes through Apideck with serviceId "gitlab".
license: Apache-2.0
alwaysApply: false
metadata:
  author: apideck
  version: "1.0.0"
  serviceId: gitlab
  unifiedApis: ["issue-tracking"]
  authType: oauth2
  tier: "1b"
  verified: true
  status: beta
  difficulty: straightforward
  partnershipRequired: false
  sandboxAvailable: false
---

# GitLab (via Apideck)

Access GitLab through Apideck's **Issue Tracking** unified API — one of 6 Issue Tracking connectors that share the same method surface. Code you write here ports to Jira, GitHub, Linear and 2 other Issue Tracking connectors by changing a single `serviceId` string. Apideck handles auth, pagination, rate limiting, and retries so you don't write per-tenant GitLab plumbing.

> **Beta connector.** GitLab is currently in beta on Apideck. Expect partial resource coverage and occasional mapping gaps. Always verify coverage (see below) and fall back to the Proxy API for unsupported operations.

## Quick facts

- **Apideck serviceId:** `gitlab`
- **Unified API:** Issue Tracking
- **Auth type:** oauth2
- **Status:** beta
- **Gotchas:** [page](https://developers.apideck.com/apis/issue-tracking/gitlab/gotchas)
- **GitLab docs:** https://docs.gitlab.com/ee/api/
- **Homepage:** https://www.gitlab.com/

## At a glance

- **Implementation difficulty:** straightforward — Self-Service OAuth App + Free GitLab.com Account Sufficient, No Partnership or Review
- **Vendor partnership required:** no ([GitLab OAuth application settings](https://docs.gitlab.com/integration/oauth_provider/)) — Anyone with a GitLab account, or a group they manage, registers the application in GitLab settings and gets the client ID and secret straight away.
- **Apideck-managed credentials:** available — OAuth shows "Apideck" as the requesting application.
- **Account type required:** Any GitLab.com plan, the free one included.
- **Consumer access level:** Any GitLab user with access to the group being connected. The connection reaches what that user can already see in it.
- **Sandbox:** not available ([signup](https://gitlab.com/users/sign_up)) — Test in a separate free GitLab.com account with its own group. The free plan allows 5 users per top-level group.
- **Costs:** No separate charge for API access.
- **Rate limits:** 2,000 requests a minute for each authenticated user on GitLab.com.
- **Authentication:** Authorization Code flow.
- **Webhooks:** Virtual webhooks - ticket created and updated, detected by polling the group's issues.

**Important to know:**

- Each connection reaches one GitLab group, chosen by the Group ID entered when connecting, and all data comes from that group. A consumer with several groups needs a connection for each.

> Facts synced from Apideck's connector metadata API — `GET /connector/connectors/gitlab` (`overview` field) is the live, authoritative version.

## When to use this skill

Activate this skill when the user explicitly wants to work with **GitLab** — for example, "create a ticket in GitLab" or "comment on an issue in GitLab". This skill teaches the agent:

1. Which Apideck unified API covers GitLab (Issue Tracking)
2. The correct `serviceId` to pass on every call (`gitlab`)
3. GitLab-specific auth and coverage caveats

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

// List tickets in GitLab
const { data } = await apideck.issueTracking.tickets.list({
  serviceId: "gitlab",
});
```

## Portable across 6 Issue Tracking connectors

The Apideck **Issue Tracking** unified API exposes the same methods for every connector in its catalog. Switching from GitLab to another Issue Tracking connector is a one-string change — no rewrite, no new SDK.

```typescript
// Today — GitLab
await apideck.issueTracking.tickets.list({ serviceId: "gitlab" });

// Tomorrow — same code, different connector
await apideck.issueTracking.tickets.list({ serviceId: "jira" });
await apideck.issueTracking.tickets.list({ serviceId: "github" });
```

This is the compounding advantage of using Apideck over integrating GitLab directly: code against the unified Issue Tracking API once, gain access to every connector in it. New connectors Apideck adds become available to your app without code changes.

## GitLab via Apideck Issue Tracking

GitLab Issues is mapped to Apideck's Issue Tracking unified API. Covers projects, issues, comments (notes), users, and labels.

### Entity mapping

| GitLab concept | Apideck Issue Tracking resource |
|---|---|
| Project | `collections` |
| Issue | `tickets` |
| Note (comment on issue) | `comments` |
| User (project member) | `users` |
| Label | `tags` |
| Epic, Milestone | use Proxy |
| Merge Request | use Proxy |

### Coverage highlights

- ✅ CRUD on issues within projects
- ✅ Comments (notes)
- ✅ Labels as tags
- ❌ Merge requests — separate surface; use Proxy
- ❌ CI/CD pipelines, runners — use Proxy

### Auth

- **Type:** OAuth 2.0, managed by Apideck Vault
- **Self-hosted GitLab:** the cloud `gitlab` connector targets gitlab.com. For self-hosted Data Center / CE, use the separate `gitlab-server` connector.
- **Scopes:** `api` scope for read/write access.

### Example: list issues in a project

```typescript
const { data } = await apideck.issueTracking.collectionTickets.list({
  serviceId: "gitlab",
  collectionId: "1234", // GitLab project ID
  filter: { status: "opened" },
});
```

## Escape hatch: Proxy API

When an endpoint isn't covered by the Issue Tracking unified API, use Apideck's Proxy to call GitLab directly — Apideck injects auth headers and handles token refresh. Set `x-apideck-downstream-url` to the target endpoint on GitLab's own API:

```bash
curl 'https://unify.apideck.com/proxy' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}" \
  -H "x-apideck-consumer-id: ${CONSUMER_ID}" \
  -H "x-apideck-service-id: gitlab" \
  -H "x-apideck-downstream-url: <target endpoint on GitLab>" \
  -H "x-apideck-downstream-method: GET"
```

See [GitLab's API docs](https://docs.gitlab.com/ee/api/) for available endpoints.

## Sibling connectors

Other **Issue Tracking** connectors that share this unified API surface (same method signatures, just change `serviceId`):

[`jira`](../jira/) *(beta)*, [`github`](../github/) *(beta)*, [`linear`](../linear/) *(beta)*, [`gitlab-server`](../gitlab-server/) *(beta)*, [`linear-multiworkspace`](../linear-multiworkspace/) *(beta)*.

## See also

- [Issue Tracking OpenAPI spec](https://specs.apideck.com/issue-tracking.yml) · [API Explorer](https://developers.apideck.com/api-explorer?id=issue-tracking)
- [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) — programmatic coverage checks
- [`apideck-best-practices`](../../skills/apideck-best-practices/) — architecture, Vault, pagination, error handling
- [`apideck-node`](../../skills/apideck-node/) — TypeScript / Node SDK patterns
- [GitLab official docs](https://docs.gitlab.com/ee/api/)
