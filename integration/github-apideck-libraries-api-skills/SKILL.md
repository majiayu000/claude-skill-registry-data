---
name: github
description: |
  GitHub integration via Apideck's Issue Tracking unified API — same methods work across every connector in Issue Tracking, switch by changing `serviceId`. Use when the user wants to read, write, or comment on tickets and issues in GitHub. Routes through Apideck with serviceId "github".
license: Apache-2.0
alwaysApply: false
metadata:
  author: apideck
  version: "1.0.0"
  serviceId: github
  unifiedApis: ["issue-tracking"]
  authType: oauth2
  tier: "1b"
  verified: true
  status: beta
  difficulty: straightforward
  partnershipRequired: false
  sandboxAvailable: true
---

# GitHub (via Apideck)

Access GitHub through Apideck's **Issue Tracking** unified API — one of 6 Issue Tracking connectors that share the same method surface. Code you write here ports to Jira, GitLab, Linear and 2 other Issue Tracking connectors by changing a single `serviceId` string. Apideck handles auth, pagination, rate limiting, and retries so you don't write per-tenant GitHub plumbing.

> **Beta connector.** GitHub is currently in beta on Apideck. Expect partial resource coverage and occasional mapping gaps. Always verify coverage (see below) and fall back to the Proxy API for unsupported operations.

## Quick facts

- **Apideck serviceId:** `github`
- **Unified API:** Issue Tracking
- **Auth type:** oauth2
- **Status:** beta
- **Gotchas:** [page](https://developers.apideck.com/apis/issue-tracking/github/gotchas)
- **GitHub docs:** https://docs.github.com/en/rest
- **Homepage:** https://github.com/

## At a glance

- **Implementation difficulty:** straightforward — Self-Service GitHub App + Free Account, No Partnership
- **Vendor partnership required:** no — A GitHub App can be registered under any personal account or organisation you own.
- **Apideck-managed credentials:** not available — Each customer registers their own GitHub App and supplies its Client ID and Secret.
- **Account type required:** A GitHub organisation; one organisation per connection.
- **Consumer access level:** Organisation owner, since only owners can install the GitHub App on the organisation.
- **Sandbox:** available ([signup](https://github.com/signup)) — Test with a free GitHub account.
- **Rate limits:** 5,000 requests per hour per user for a GitHub App acting on a user's behalf; 15,000 per hour when the app is owned by a GitHub Enterprise Cloud organisation.
- **Authentication:** Authorization Code flow; access follows the GitHub App's permissions, not OAuth scopes.
- **Webhooks:** Native - issue events (opened, edited, closed, deleted and other issue changes).

> Facts synced from Apideck's connector metadata API — `GET /connector/connectors/github` (`overview` field) is the live, authoritative version.

## When to use this skill

Activate this skill when the user explicitly wants to work with **GitHub** — for example, "create a ticket in GitHub" or "comment on an issue in GitHub". This skill teaches the agent:

1. Which Apideck unified API covers GitHub (Issue Tracking)
2. The correct `serviceId` to pass on every call (`github`)
3. GitHub-specific auth and coverage caveats

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

// List tickets in GitHub
const { data } = await apideck.issueTracking.tickets.list({
  serviceId: "github",
});
```

## Portable across 6 Issue Tracking connectors

The Apideck **Issue Tracking** unified API exposes the same methods for every connector in its catalog. Switching from GitHub to another Issue Tracking connector is a one-string change — no rewrite, no new SDK.

```typescript
// Today — GitHub
await apideck.issueTracking.tickets.list({ serviceId: "github" });

// Tomorrow — same code, different connector
await apideck.issueTracking.tickets.list({ serviceId: "jira" });
await apideck.issueTracking.tickets.list({ serviceId: "gitlab" });
```

This is the compounding advantage of using Apideck over integrating GitHub directly: code against the unified Issue Tracking API once, gain access to every connector in it. New connectors Apideck adds become available to your app without code changes.

## GitHub via Apideck Issue Tracking

GitHub Issues is mapped to Apideck's Issue Tracking unified API. Covers repositories, issues, comments, users, and labels.

### Entity mapping

| GitHub concept | Apideck Issue Tracking resource |
|---|---|
| Repository | `collections` |
| Issue | `tickets` |
| Comment | `comments` |
| User | `users` |
| Label | `tags` |
| Milestone | use Proxy (not in unified) |
| Pull Request | use Proxy (distinct GitHub surface) |
| Project (Projects v2) | use Proxy |

### Coverage highlights

- ✅ List repositories (collections) the authenticated user can access
- ✅ CRUD on issues (tickets)
- ✅ Comments
- ✅ Labels (tags)
- ❌ Pull requests — separate surface; use Proxy with `/repos/{owner}/{repo}/pulls`
- ❌ GitHub Actions, Packages, Codespaces — use Proxy

### Auth

- **Type:** OAuth 2.0 or GitHub App installation, managed by Apideck Vault
- **Scopes:** repo scope for read/write on private repos; public_repo for public-only.
- **Org-level vs. user-level:** each connection targets one owner (user or org). To access multiple orgs, create multiple connections.
- **Rate limits:** GitHub's rate limits apply (5,000/hour for authenticated users; higher for Apps). Apideck backs off on 403/429.

### Example: list open issues in a repo

```typescript
const { data } = await apideck.issueTracking.collectionTickets.list({
  serviceId: "github",
  collectionId: "owner/repo", // or GitHub's numeric repo ID depending on SDK
  filter: { status: "open" },
});
```

## Escape hatch: Proxy API

When an endpoint isn't covered by the Issue Tracking unified API, use Apideck's Proxy to call GitHub directly — Apideck injects auth headers and handles token refresh. Set `x-apideck-downstream-url` to the target endpoint on GitHub's own API:

```bash
curl 'https://unify.apideck.com/proxy' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}" \
  -H "x-apideck-consumer-id: ${CONSUMER_ID}" \
  -H "x-apideck-service-id: github" \
  -H "x-apideck-downstream-url: <target endpoint on GitHub>" \
  -H "x-apideck-downstream-method: GET"
```

See [GitHub's API docs](https://docs.github.com/en/rest) for available endpoints.

## Sibling connectors

Other **Issue Tracking** connectors that share this unified API surface (same method signatures, just change `serviceId`):

[`jira`](../jira/) *(beta)*, [`gitlab`](../gitlab/) *(beta)*, [`linear`](../linear/) *(beta)*, [`gitlab-server`](../gitlab-server/) *(beta)*, [`linear-multiworkspace`](../linear-multiworkspace/) *(beta)*.

## See also

- [Issue Tracking OpenAPI spec](https://specs.apideck.com/issue-tracking.yml) · [API Explorer](https://developers.apideck.com/api-explorer?id=issue-tracking)
- [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) — programmatic coverage checks
- [`apideck-best-practices`](../../skills/apideck-best-practices/) — architecture, Vault, pagination, error handling
- [`apideck-node`](../../skills/apideck-node/) — TypeScript / Node SDK patterns
- [GitHub official docs](https://docs.github.com/en/rest)
