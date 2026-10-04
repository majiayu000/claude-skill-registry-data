---
name: jira
description: |
  Jira integration via Apideck's Issue Tracking unified API — same methods work across every connector in Issue Tracking, switch by changing `serviceId`. Use when the user wants to read, write, or comment on tickets and issues in Jira. Routes through Apideck with serviceId "jira".
license: Apache-2.0
alwaysApply: false
metadata:
  author: apideck
  version: "1.0.0"
  serviceId: jira
  unifiedApis: ["issue-tracking"]
  authType: oauth2
  tier: "1a"
  verified: true
  status: beta
  difficulty: moderate
  partnershipRequired: false
  sandboxAvailable: false
---

# Jira (via Apideck)

Access Jira through Apideck's **Issue Tracking** unified API — one of 6 Issue Tracking connectors that share the same method surface. Code you write here ports to GitHub, GitLab, Linear and 2 other Issue Tracking connectors by changing a single `serviceId` string. Apideck handles auth, pagination, rate limiting, and retries so you don't write per-tenant Jira plumbing.

> **Beta connector.** Jira is currently in beta on Apideck. Expect partial resource coverage and occasional mapping gaps. Always verify coverage (see below) and fall back to the Proxy API for unsupported operations.

## Quick facts

- **Apideck serviceId:** `jira`
- **Unified API:** Issue Tracking
- **Auth type:** oauth2
- **Status:** beta
- **Gotchas:** [page](https://developers.apideck.com/apis/issue-tracking/jira/gotchas)
- **Jira docs:** https://developer.atlassian.com/cloud/jira/platform/rest/v3/
- **Homepage:** https://www.atlassian.com/software/jira

## At a glance

- **Implementation difficulty:** moderate — Self-Service OAuth App + Atlassian Review Needed to Scale Past One Shared Hourly Quota
- **Vendor partnership required:** no ([Atlassian developer console](https://developer.atlassian.com/console/myapps/)) — No partner programme or Marketplace listing needed. Atlassian reviews an app only if you submit it.
- **Apideck-managed credentials:** available — You can connect and test before registering an app of your own.
- **Account type required:** Any Jira Cloud plan, including the free one. Registering the app needs a free Atlassian developer account.
- **Consumer access level:** Any Jira user on the site can authorise, with no admin rights needed. The connection then reaches what that user can already see there.
- **Sandbox:** not available — Atlassian's Sandbox feature belongs to the Premium and Enterprise plans. A separate free Jira Cloud site serves as a test environment at no cost.
- **Costs:** Atlassian publishes no separate charge for API access. What a connection can reach follows the Jira Cloud plan the site is already on.
- **Rate limits:** 65,000 points an hour, enforced since 2 March 2026, plus per-second burst and per-issue write caps. Most reads cost one point.
- **Authentication:** Authorization Code flow.
- **Webhooks:** Native - ticket created, updated and deleted.

**Important to know:**

- The hourly request quota belongs to the app, not to each connected Jira site: every site draws from the same pool, so the tenth consumer competes with the first. A larger per-site pool exists, but Atlassian assigns it only after reviewing an app with sustained heavy use.
- Until Atlassian has reviewed the app, everyone who authorises it is warned that it has not been reviewed by Atlassian. Nothing but that review removes the warning.
- This connector speaks Atlassian's Cloud authorisation, so a self-hosted Jira Data Center or Server site cannot connect through it. Those run a different mechanism that their own administrator has to set up.

> Facts synced from Apideck's connector metadata API — `GET /connector/connectors/jira` (`overview` field) is the live, authoritative version.

## When to use this skill

Activate this skill when the user explicitly wants to work with **Jira** — for example, "create a ticket in Jira" or "comment on an issue in Jira". This skill teaches the agent:

1. Which Apideck unified API covers Jira (Issue Tracking)
2. The correct `serviceId` to pass on every call (`jira`)
3. Jira-specific auth and coverage caveats

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

// List tickets in Jira
const { data } = await apideck.issueTracking.tickets.list({
  serviceId: "jira",
});
```

## Portable across 6 Issue Tracking connectors

The Apideck **Issue Tracking** unified API exposes the same methods for every connector in its catalog. Switching from Jira to another Issue Tracking connector is a one-string change — no rewrite, no new SDK.

```typescript
// Today — Jira
await apideck.issueTracking.tickets.list({ serviceId: "jira" });

// Tomorrow — same code, different connector
await apideck.issueTracking.tickets.list({ serviceId: "github" });
await apideck.issueTracking.tickets.list({ serviceId: "gitlab" });
```

This is the compounding advantage of using Apideck over integrating Jira directly: code against the unified Issue Tracking API once, gain access to every connector in it. New connectors Apideck adds become available to your app without code changes.

## Jira via Apideck Issue Tracking

Jira Cloud is the reference Issue Tracking connector. Covers issues (tickets), projects (collections), comments, and users.

### Entity mapping

| Jira concept | Apideck Issue Tracking resource |
|---|---|
| Project | `collections` |
| Issue | `tickets` |
| Comment | `comments` |
| User | `users` |
| Label | `tags` |
| Issue type (Story, Bug, Task) | `ticket.type` |
| Status (To Do, In Progress, Done) | `ticket.status` |
| Priority | `ticket.priority` |
| Assignee | `ticket.assignees[]` |
| Custom fields | `ticket.custom_fields[]` |
| Epic link, Sprint | use Proxy or custom fields |
| Worklog (time tracking) | use Proxy |
| Jira Service Desk tickets | ❌ separate auth-only connector |

### Coverage highlights

- ✅ CRUD on issues across all accessible projects
- ✅ Comments (create, list, update, delete)
- ✅ Filtering by project, status, assignee, labels
- ✅ Transitioning issue status (Apideck maps to Jira's workflow transition API under the hood)
- ✅ Issue search via JQL (pass as `filter[jql]`)
- ⚠️ Custom fields — exposed as `custom_fields[]`; write values must match Jira's expected type
- ❌ Jira Service Management / Service Desk — separate product surface; use the JSM connector (auth-only in Apideck today)
- ❌ Boards, Sprints (Agile) — use Proxy with Agile REST endpoints
- ❌ Workflow configuration — use Proxy

### Jira-specific auth notes

- **Type:** OAuth 2.0 (3LO) via Atlassian, managed by Apideck Vault
- **Cloud only:** this connector targets Jira Cloud. Self-hosted Jira (Data Center / Server) is a separate surface — use the Proxy API with basic auth or a PAT.
- **Site selection:** Atlassian accounts can have access to multiple Jira sites (cloudIds). OAuth picks one — if the user has several, confirm the right site was selected. Multi-site access = multiple connections.

### Common Jira quirks handled by Apideck

- **ADF (Atlassian Document Format)** — Jira v3 uses ADF for rich text in `description` and comment bodies. Apideck accepts plain text or Markdown and transforms to ADF on write; on read, ADF is flattened to plain text in `ticket.description`. For rich content, use `raw=true` to see ADF directly.
- **Issue keys vs. IDs** — Jira surfaces both (`PROJ-123` and numeric ID). Apideck accepts either on read; writes return both.
- **Transitions are not status updates** — in Jira, you don't PUT a status; you POST a transition. Apideck handles this: `ticket.status = "Done"` triggers the right transition if one exists.
- **Pagination** — Jira uses `startAt`/`maxResults`. Apideck normalizes to cursor-based pagination.
- **Rate limits** — Atlassian Cloud enforces strict per-tenant rate limits; Apideck backs off automatically on 429.

### Example: create a bug with labels

Tickets in the Issue Tracking API are nested under a collection (project). See [`apideck-node`](../../skills/apideck-node/) for the canonical method signature — typically requires `collectionId`.

```typescript
const { data } = await apideck.issueTracking.collectionTickets.create({
  serviceId: "jira",
  collectionId: "10001", // Jira project ID
  ticket: {
    title: "Login button fails on Safari",
    description: "Repro: open Safari 17, click login. Nothing happens.",
    type: "Bug",
    priority: "High",
    assignees: [{ id: "5b10a2844c20165700ede21g" }],
    tags: [{ name: "safari" }, { name: "regression" }],
  },
});
```

### Example: search with JQL via Proxy

The unified Issue Tracking API supports basic filters, but complex JQL isn't exposed. Use the Proxy for full JQL:

```bash
curl 'https://unify.apideck.com/proxy' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}" \
  -H "x-apideck-consumer-id: ${CONSUMER_ID}" \
  -H "x-apideck-service-id: jira" \
  -H "x-apideck-downstream-url: /rest/api/3/search?jql=project%20%3D%20PROJ" \
  -H "x-apideck-downstream-method: GET"
```

### Example: transition an issue status

In Jira you don't PUT a status — you POST a transition. Apideck's `update` with `ticket.status = "Done"` triggers the matching workflow transition if one exists. If the transition isn't auto-resolvable, use Proxy with `/rest/api/3/issue/{id}/transitions`.

```typescript
await apideck.issueTracking.collectionTickets.update({
  serviceId: "jira",
  collectionId: "10001",
  ticketId: "10042",
  ticket: { status: "Done" },
});
```

## Sibling connectors

Other **Issue Tracking** connectors that share this unified API surface (same method signatures, just change `serviceId`):

[`github`](../github/) *(beta)*, [`gitlab`](../gitlab/) *(beta)*, [`linear`](../linear/) *(beta)*, [`gitlab-server`](../gitlab-server/) *(beta)*, [`linear-multiworkspace`](../linear-multiworkspace/) *(beta)*.

## See also

- [Issue Tracking OpenAPI spec](https://specs.apideck.com/issue-tracking.yml) · [API Explorer](https://developers.apideck.com/api-explorer?id=issue-tracking)
- [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) — programmatic coverage checks
- [`apideck-best-practices`](../../skills/apideck-best-practices/) — architecture, Vault, pagination, error handling
- [`apideck-node`](../../skills/apideck-node/) — TypeScript / Node SDK patterns
- [Jira official docs](https://developer.atlassian.com/cloud/jira/platform/rest/v3/)
