---
name: onedrive
description: |
  OneDrive integration via Apideck's File Storage unified API — same methods work across every connector in File Storage, switch by changing `serviceId`. Use when the user wants to read, write, upload, or search files, folders, and drives in OneDrive. Routes through Apideck with serviceId "onedrive".
license: Apache-2.0
alwaysApply: false
metadata:
  author: apideck
  version: "1.0.0"
  serviceId: onedrive
  unifiedApis: ["file-storage"]
  authType: oauth2
  tier: "1b"
  verified: true
  difficulty: moderate
  partnershipRequired: false
  sandboxAvailable: true
---

# OneDrive (via Apideck)

Access OneDrive through Apideck's **File Storage** unified API — one of 5 File Storage connectors that share the same method surface. Code you write here ports to SharePoint, Box, Dropbox and 1 other File Storage connectors by changing a single `serviceId` string. Apideck handles auth, pagination, rate limiting, and retries so you don't write per-tenant OneDrive plumbing.

## Quick facts

- **Apideck serviceId:** `onedrive`
- **Unified API:** File Storage
- **Auth type:** oauth2
- **Gotchas:** [page](https://developers.apideck.com/apis/file-storage/onedrive/gotchas)
- **OneDrive docs:** https://learn.microsoft.com/onedrive/developer/
- **Homepage:** https://onedrive.live.com/

## At a glance

- **Implementation difficulty:** moderate — Self-Service OAuth + Publisher Verification Needed for Cross-Tenant Consent
- **Vendor partnership required:** no ([Microsoft Entra publisher verification](https://learn.microsoft.com/en-us/entra/identity-platform/publisher-verification-overview)) — No partner programme or contract. Publisher verification, via a Microsoft AI Cloud Partner Program account, is the only review step.
- **Apideck-managed credentials:** available — The Microsoft consent screen shows "Apideck". Use your own Microsoft Entra app in production.
- **Account type required:** A personal Microsoft account with OneDrive, or a work or school account whose Microsoft 365 licence includes OneDrive
- **Consumer access level:** Any user with access to the drive they connect
- **Sandbox:** available ([signup](https://developer.microsoft.com/microsoft-365/dev-program)) — A free personal Microsoft account gives you a OneDrive to test against; the Microsoft 365 E5 developer tenant (25 users) is eligibility-gated.
- **Costs:** None. App registration, publisher verification and standard Microsoft Graph calls are free.
- **Rate limits:** Per app per tenant: 1,250 to 6,250 resource units/min (1 to 2 units per call), scaling with tenant size; HTTP 429/503 with Retry-After on excess
- **Authentication:** Authorization Code flow through Microsoft Entra ID.
- **Webhooks:** Native — drive.updated only (a library-level change notification; per-file events are not emitted)

**Important to know:**

- Publisher verification is the hidden gate: since November 2020 Microsoft blocks users in other tenants from consenting to a new multitenant app that is not publisher verified. Plan for it before onboarding, including a publisher domain you own.
- Many work and school tenants switch off user consent, so a tenant admin has to approve the app before anyone in that organisation can connect; plan for an admin-consent step in your onboarding.
- A connection is pinned to one drive: after authorizing, the consumer can point it at a specific drive from a live list of their own drives; left unset, the account's default drive is used. A consumer with several drives, or shared libraries, needs one connection per drive.
- Refresh tokens expire after 90 days without use, so a consumer whose integration is idle for three months has to re-authorise the connection.

> Facts synced from Apideck's connector metadata API — `GET /connector/connectors/onedrive` (`overview` field) is the live, authoritative version.

## When to use this skill

Activate this skill when the user explicitly wants to work with **OneDrive** — for example, "upload a file in OneDrive" or "list a folder in OneDrive". This skill teaches the agent:

1. Which Apideck unified API covers OneDrive (File Storage)
2. The correct `serviceId` to pass on every call (`onedrive`)
3. OneDrive-specific auth and coverage caveats

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

// List files in OneDrive
const { data } = await apideck.fileStorage.files.list({
  serviceId: "onedrive",
});
```

## Portable across 5 File Storage connectors

The Apideck **File Storage** unified API exposes the same methods for every connector in its catalog. Switching from OneDrive to another File Storage connector is a one-string change — no rewrite, no new SDK.

```typescript
// Today — OneDrive
await apideck.fileStorage.files.list({ serviceId: "onedrive" });

// Tomorrow — same code, different connector
await apideck.fileStorage.files.list({ serviceId: "sharepoint" });
await apideck.fileStorage.files.list({ serviceId: "box" });
```

This is the compounding advantage of using Apideck over integrating OneDrive directly: code against the unified File Storage API once, gain access to every connector in it. New connectors Apideck adds become available to your app without code changes.

## OneDrive via Apideck File Storage

OneDrive (Microsoft personal + business) is accessed via Microsoft Graph, same as SharePoint. Apideck normalizes the Drive/File/Folder surface.

### Entity mapping

| OneDrive concept | Apideck File Storage resource |
|---|---|
| Drive (user's OneDrive) | `drives` |
| DriveItem (file) | `files` |
| DriveItem (folder) | `folders` |
| Shared link | `shared-links` |
| Upload session | `upload-sessions` |

### Coverage highlights

- ✅ CRUD on files and folders
- ✅ Upload via resumable sessions (required for large files)
- ✅ Download file content
- ✅ Shared links
- ❌ Delta queries (change tracking) — use Proxy with Graph `/delta`

### Auth

- **Type:** OAuth 2.0 (Microsoft identity platform), managed by Apideck Vault
- **Personal vs. Work:** both account types work. Personal accounts don't need admin consent; corporate tenants often do for Graph scopes.
- **User binding:** each connection is bound to one user's OneDrive (unlike SharePoint which exposes site-wide drives).

### Example: list files in root

```typescript
const { data } = await apideck.fileStorage.files.list({
  serviceId: "onedrive",
});
```

## Escape hatch: Proxy API

When an endpoint isn't covered by the File Storage unified API, use Apideck's Proxy to call OneDrive directly — Apideck injects auth headers and handles token refresh. Set `x-apideck-downstream-url` to the target endpoint on OneDrive's own API:

```bash
curl 'https://unify.apideck.com/proxy' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}" \
  -H "x-apideck-consumer-id: ${CONSUMER_ID}" \
  -H "x-apideck-service-id: onedrive" \
  -H "x-apideck-downstream-url: <target endpoint on OneDrive>" \
  -H "x-apideck-downstream-method: GET"
```

See [OneDrive's API docs](https://learn.microsoft.com/onedrive/developer/) for available endpoints.

## Sibling connectors

Other **File Storage** connectors that share this unified API surface (same method signatures, just change `serviceId`):

[`sharepoint`](../sharepoint/), [`box`](../box/), [`dropbox`](../dropbox/), [`google-drive`](../google-drive/).

## See also

- [File Storage OpenAPI spec](https://specs.apideck.com/file-storage.yml) · [API Explorer](https://developers.apideck.com/api-explorer?id=file-storage)
- [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) — programmatic coverage checks
- [`apideck-best-practices`](../../skills/apideck-best-practices/) — architecture, Vault, pagination, error handling
- [`apideck-node`](../../skills/apideck-node/) — TypeScript / Node SDK patterns
- [OneDrive official docs](https://learn.microsoft.com/onedrive/developer/)
