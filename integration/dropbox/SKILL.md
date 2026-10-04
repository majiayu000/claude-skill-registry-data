---
name: dropbox
description: |
  Dropbox integration via Apideck's File Storage unified API — same methods work across every connector in File Storage, switch by changing `serviceId`. Use when the user wants to read, write, upload, or search files, folders, and drives in Dropbox. Routes through Apideck with serviceId "dropbox".
license: Apache-2.0
alwaysApply: false
metadata:
  author: apideck
  version: "1.0.0"
  serviceId: dropbox
  unifiedApis: ["file-storage"]
  authType: oauth2
  tier: "1b"
  verified: true
  difficulty: moderate
  partnershipRequired: false
  sandboxAvailable: false
---

# Dropbox (via Apideck)

Access Dropbox through Apideck's **File Storage** unified API — one of 5 File Storage connectors that share the same method surface. Code you write here ports to SharePoint, Box, Google Drive and 1 other File Storage connectors by changing a single `serviceId` string. Apideck handles auth, pagination, rate limiting, and retries so you don't write per-tenant Dropbox plumbing.

## Quick facts

- **Apideck serviceId:** `dropbox`
- **Unified API:** File Storage
- **Auth type:** oauth2
- **Gotchas:** [page](https://developers.apideck.com/apis/file-storage/dropbox/gotchas)
- **Dropbox docs:** https://www.dropbox.com/developers
- **Homepage:** https://www.dropbox.com/

## At a glance

- **Implementation difficulty:** moderate — Self-Service App Registration + Dropbox Production Approval Required to Connect Users at Scale
- **Vendor partnership required:** no ([Dropbox App console](https://www.dropbox.com/developers/apps)) — No contract and no partner programme. Registering an app is free and self-service.
- **Apideck-managed credentials:** available — Temporary shared credentials for trying the connector; going live needs the app owner's own Dropbox app.
- **Account type required:** Any Dropbox account, including a free individual one.
- **Consumer access level:** Any Dropbox user can authorize access to their own account; no administrator role is involved.
- **Sandbox:** not available — Dropbox has no separate test environment.
- **Costs:** No published fee for API access. What an account can do follows its own Dropbox plan.
- **Rate limits:** No published figures. Limits apply per authorized user, or per team for team apps, and Dropbox returns 429 with a Retry-After header.
- **Authentication:** Authorization Code flow.
- **Webhooks:** No webhooks — Dropbox changes are picked up by polling instead.

**Important to know:**

- A Dropbox app starts in Development status. Its 50th connected user starts a two-week clock to obtain Production approval, and Dropbox will not usually review before that point, so applying early does not avoid it. Missing it stops new connections; existing ones keep working.
- An app is created with either App folder or Full Dropbox access, and Dropbox does not allow that choice to be changed afterwards. Correcting it means registering a new app, which every already-connected consumer then has to authorize again.
- Adding a scope later does not reach consumers who already connected: Dropbox keeps an existing authorization exactly as it was granted and never re-prompts, so each of them has to authorize again before the new permission works.

> Facts synced from Apideck's connector metadata API — `GET /connector/connectors/dropbox` (`overview` field) is the live, authoritative version.

## When to use this skill

Activate this skill when the user explicitly wants to work with **Dropbox** — for example, "upload a file in Dropbox" or "list a folder in Dropbox". This skill teaches the agent:

1. Which Apideck unified API covers Dropbox (File Storage)
2. The correct `serviceId` to pass on every call (`dropbox`)
3. Dropbox-specific auth and coverage caveats

For the full method surface (parameters, pagination, filtering), use your language SDK skill:

- [`apideck-node`](../../skills/apideck-node/), [`apideck-python`](../../skills/apideck-python/), [`apideck-dotnet`](../../skills/apideck-dotnet/), [`apideck-java`](../../skills/apideck-java/), [`apideck-go`](../../skills/apideck-go/), [`apideck-php`](../../skills/apideck-php/), or [`apideck-rest`](../../skills/apideck-rest/)

For the raw OpenAPI spec:

- **File Storage:** [https://specs.apideck.com/file-storage.yml](https://specs.apideck.com/file-storage.yml) · [API Explorer](https://developers.apideck.com/api-explorer?id=file-storage)

## Minimal example (TypeScript)

```typescript
import { Apideck } from "@apideck/unify";

const apideck = new Apideck({
  apiKey: process.env.APIDECK_API_KEY,
  appId: process.env.APIDECK_APP_ID,
  consumerId: "your-consumer-id",
});

// List files in Dropbox
const { data } = await apideck.fileStorage.files.list({
  serviceId: "dropbox",
});
```

## Portable across 5 File Storage connectors

The Apideck **File Storage** unified API exposes the same methods for every connector in its catalog. Switching from Dropbox to another File Storage connector is a one-string change — no rewrite, no new SDK.

```typescript
// Today — Dropbox
await apideck.fileStorage.files.list({ serviceId: "dropbox" });

// Tomorrow — same code, different connector
await apideck.fileStorage.files.list({ serviceId: "sharepoint" });
await apideck.fileStorage.files.list({ serviceId: "box" });
```

This is the compounding advantage of using Apideck over integrating Dropbox directly: code against the unified File Storage API once, gain access to every connector in it. New connectors Apideck adds become available to your app without code changes.

## Dropbox via Apideck File Storage

Dropbox is a popular consumer + team file sync product. Apideck covers file, folder, and upload-session operations.

### Entity mapping

| Dropbox concept | Apideck File Storage resource |
|---|---|
| File | `files` |
| Folder | `folders` |
| Upload session | `upload-sessions` |
| Shared link | not yet exposed — use Proxy |

### Coverage highlights

- ✅ List, get, create, update, delete files and folders
- ✅ Upload via sessions for large files
- ✅ Download file content
- ⚠️ Shared links — still being added; use Proxy with `/sharing/create_shared_link_with_settings` for now
- ❌ Dropbox Paper, team admin features — use Proxy

### Auth

- **Type:** OAuth 2.0, managed by Apideck Vault
- **Scopes:** Apideck Vault requests file read/write scopes as needed.
- **Team vs. personal:** both supported. Team connections include `team_member_id` context.

### Example: upload a small file

```typescript
const { data } = await apideck.fileStorage.files.create({
  serviceId: "dropbox",
  file: { name: "notes.txt", parent_folder_id: "/" },
});
```

## Escape hatch: Proxy API

When an endpoint isn't covered by the File Storage unified API, use Apideck's Proxy to call Dropbox directly — Apideck injects auth headers and handles token refresh. Set `x-apideck-downstream-url` to the target endpoint on Dropbox's own API:

```bash
curl 'https://unify.apideck.com/proxy' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}" \
  -H "x-apideck-consumer-id: ${CONSUMER_ID}" \
  -H "x-apideck-service-id: dropbox" \
  -H "x-apideck-downstream-url: <target endpoint on Dropbox>" \
  -H "x-apideck-downstream-method: GET"
```

See [Dropbox's API docs](https://www.dropbox.com/developers) for available endpoints.

## Sibling connectors

Other **File Storage** connectors that share this unified API surface (same method signatures, just change `serviceId`):

[`sharepoint`](../sharepoint/), [`box`](../box/), [`google-drive`](../google-drive/), [`onedrive`](../onedrive/).

## See also

- [File Storage OpenAPI spec](https://specs.apideck.com/file-storage.yml) · [API Explorer](https://developers.apideck.com/api-explorer?id=file-storage)
- [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) — programmatic coverage checks
- [`apideck-best-practices`](../../skills/apideck-best-practices/) — architecture, Vault, pagination, error handling
- [`apideck-node`](../../skills/apideck-node/) — TypeScript / Node SDK patterns
- [Dropbox official docs](https://www.dropbox.com/developers)
