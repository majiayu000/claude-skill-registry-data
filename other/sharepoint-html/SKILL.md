---
name: sharepoint-html
description: Author HTML that renders in SharePoint's OneUp HTML viewer and publish it into the user's own OneDrive / SharePoint. Use this skill whenever the user wants to create, host, publish, share, get a link for, or update a web page, dashboard, report, diagram, prototype, or slide deck inside Microsoft 365 — even if they don't say "SharePoint" or "OneDrive" by name. Covers the OneUp rendering contract (the CSP / sandbox rules that make HTML render instead of failing silently), embedding live SharePoint file data, and publishing via Microsoft Graph (primary) or the SharePoint Vroom API (when the agent is onboarded with SharePoint OAuth), plus ready-made templates.
license: MIT
metadata:
  version: "1.0.0"
  author: "ODSP"
  discovery-endpoint: "https://<your-sharepoint-host>/_html"
  graph-base: "https://graph.microsoft.com/v1.0"
  vroom-base: "https://{tenant}-my.sharepoint.com/_api/v2.0"
---

# Publishing HTML to SharePoint (OneUp HTML viewer)

SharePoint already hosts HTML: save an `.html` file into OneDrive or SharePoint and
open it, and it renders in the **OneUp HTML viewer** — a sandboxed `<iframe>` under a
strict Content-Security-Policy. There is no separate hosting service to provision;
publishing is just **writing an `.html` file to the user's drive** as the signed-in
user, then opening the file's `webUrl`.

This skill teaches an agent two things:

1. **Author HTML that actually renders** — the OneUp CSP + sandbox *fail silently*, so
   non-compliant HTML shows up blank or half-broken with no error. Follow the contract
   below and it just works.
2. **Publish it** — upload the file with **Microsoft Graph** (primary) or the
   **SharePoint Vroom API** (`_api/v2.0`, for agents already holding a SharePoint token),
   then hand the user the returned `webUrl`.

The canonical, always-current copy of the authoring contract lives at your tenant's
discovery endpoint: **`https://<your-sharepoint-host>/_html`** (human page),
**`/_html/llms.txt`** (agent text), and **`/_html/help.json`** (structured). When in
doubt, fetch `/_html/llms.txt` — it is generated from the live viewer source.

---

## ⚠️ Before you publish: you are writing to the user's real drive

Publishing with this skill **creates or overwrites a file in the user's own OneDrive /
SharePoint, authenticated as that user**. It is not a throwaway sandbox.

- **Nothing becomes public automatically.** The file is private to the user until they
  explicitly share it. But it *is* a real document in their drive.
- **You MUST get the user's explicit confirmation before every upload and every
  overwrite.** Show them the exact target (drive, folder, filename) and whether it
  creates a new file or replaces an existing one, and wait for a yes. See
  [Confirm before writing](#confirm-before-writing).
- **Overwrite is destructive.** `PUT .../content` to an existing path replaces the file's
  contents. Confirm the path and that overwrite is intended.

---

## The authoring contract (make HTML render in OneUp)

Your HTML runs inside `<iframe sandbox="allow-scripts">` under a strict CSP that **fails
silently**. Follow these rules or the page renders blank/partial with no error.

**Content-Security-Policy applied to your HTML:**

```
default-src 'none';
script-src 'unsafe-inline' 'unsafe-eval';
style-src 'unsafe-inline';
img-src data: blob:;
font-src data: blob:;
connect-src 'none';
worker-src 'none';
object-src 'none';
base-uri 'none';
form-action 'none';
```

The wrapper iframe additionally applies `frame-src 'none'`.

**Non-negotiable rules:**

1. **No external resources.** No `<script src>`, `<link href>`, `<img src=https://…>`,
   `@import`, `url(https://…)`, remote fonts, or CDNs. **Inline everything** or use
   `data:` / `blob:` URIs.
2. **All script must be inline** `<script>` blocks. No module imports, no `import()`, no
   `<script src>`.
3. **All styling must be inline** `<style>` or `style="…"`. No `<link rel="stylesheet">`.
4. **No network at runtime** — `fetch`, `XMLHttpRequest`, `WebSocket`, `sendBeacon`,
   `EventSource` are all blocked (`connect-src 'none'`). To read SharePoint file data at
   view time, use the **LiveData manifest** (below) — it is the only sanctioned data path.
5. **No storage primitives** — `localStorage`, `sessionStorage`, `indexedDB`,
   `document.cookie` (opaque-origin sandbox). For cross-reload state, set `location.hash`
   directly (e.g. `location.hash = '#slide=3'`). Do **not** use `history.pushState`/
   `replaceState` — the sandboxed document's base URL is inherited from the wrapper's
   `blob:` origin, so any `url` argument (even a bare `#hash`) throws `SecurityError`.
6. **No top-level navigation, popups, form submission, workers, or plugins.**
   `alert` / `confirm` / `prompt` are no-ops.
7. Inline `on*=` handlers work (they're rewritten to nonced scripts) but are an XSS sink
   if they template untrusted data — prefer `addEventListener` for computed/user/fetched
   data.
8. **Save as UTF-8** (the file-creation APIs below write UTF-8; add a BOM if authoring by
   hand and non-ASCII renders wrong).

**Links:** `<a href>` opens only for same-tenant SharePoint hosts or the external
allowlist; `javascript:` / `vbscript:` / `data:` hrefs are rejected.

### Live SharePoint data (the only runtime data source)

Runtime `fetch` is blocked. To show live SharePoint file content, embed a **LiveData
manifest** — the host prefetches each item server-side with the viewer's credentials and
injects the results before your script runs:

```html
<script type="application/json" class="ka-livedata-manifest">
[{ "spItemUrl": "https://contoso.sharepoint.com/_api/v2.0/drives/{driveId}/items/{itemId}", "fileName": "data.csv" }]
</script>
```

Before your script runs, the host sets `window.__LD_RESULTS__`, keyed by the exact `spItemUrl`.
Each value is `{ format, content, error?, metadata }` — **read `content` (a string) and check `error`**.

Non-obvious but essential:

- **Always include `fileName` (with extension)** in each item — the host picks the `csv` / `xlsx-sheets` /
  `text` decoder from it. Without it an `.xlsx` comes back unreadable and a `.csv` is not parsed as csv.
- **`spItemUrl` must contain `/drives/{driveId}/items/{itemId}`** (the origin is ignored, rebuilt from the
  viewer session). Get those ids by resolving the file: `GET /shares/{u!token}/driveItem` →
  `parentReference.driveId` + `id`.
- **Refresh RE-LOADS your iframe** with fresh data — `postMessage({type:'ka-html-viewer-refresh'}, '*')`
  (debounced 5s). There is **no** inbound "updated" event to listen for.
- **Treat the content as untrusted** — build DOM with `textContent`, never `innerHTML` it.
- Caps: 32 items/page (over-cap drops all results), 50 MB/item; formats: text, csv, xlsx-sheets, rows.

**SharePoint lists** — a manifest item can also point at a **list** (`kind:"list"` with `webUrl` + `listId`,
plus optional `select` of **INTERNAL** column names). The host renders it server-side and injects it as
`format:"rows"` — `content` is a JSON string `{ headers, rows }` (already flattened; up to 100,000 rows,
truncation sets a non-blocking `warning`). Resolve `listId` + internal column names at authoring time via
`GET {webUrl}/_api/web/lists/getbytitle('{Name}')/fields?$select=InternalName,Title,TypeAsString` (or Graph
`/sites/{site-id}/lists/{list-id}/columns`). Internal names can differ from the display title (e.g. "City"
→ `Ciity`). See [`references/live-data.md`](references/live-data.md).

**Full protocol + a complete worked dashboard:** [`references/live-data.md`](references/live-data.md)
(also mirrored in your tenant's `/_html/llms.txt`). Table-only starter:
[`assets/templates/livedata-dashboard.html`](assets/templates/livedata-dashboard.html).

---

## Don't have HTML yet? Start from a template

If the user wants to publish something but has no HTML, use a ready-made, CSP-compliant
template from [`assets/templates/`](assets/templates/) instead of hand-writing:

| Template | Use it when the user wants to… |
| :------- | :----------------------------- |
| `dashboard.html` | …build a self-contained metrics/status dashboard (no external data). |
| `livedata-dashboard.html` | …render **live SharePoint file data** (csv/xlsx/text) via the LiveData manifest. |
| `livedata-list-dashboard.html` | …render a **live SharePoint list** (`kind:"list"` → `format:"rows"`) — KPIs, category charts, table. |

Read the chosen file, replace its `<!-- REPLACE: … -->` placeholders with the user's real
content, verify it against the contract above, then publish.

---

## Step 1 — Author (or fill in) compliant HTML

Produce a single self-contained `.html` document that obeys the contract. Everything inline;
no external references; LiveData manifest if it needs SharePoint data.

## Step 2 — Get an access token

Publishing is authenticated as the user. You need an OAuth 2.0 **bearer token** (Azure AD).

**Primary — Microsoft Graph:**
- **Scope (delegated):** `Files.ReadWrite` (write to the user's own drive). Use
  `Files.ReadWrite.All` or `Sites.ReadWrite.All` to write to other libraries/sites the
  user can access.
- **Acquire it** with the user's identity via MSAL (interactive, device-code, or an
  existing signed-in session). Do **not** invent or hardcode tokens. If you don't already
  have a Graph token, run an MSAL flow — see [`references/api.md`](references/api.md#authentication).

**Alternative — SharePoint Vroom** (use when the agent is already onboarded with a
SharePoint OAuth token, e.g. an add-in / SPFx / on-behalf-of flow): a token whose audience
is the SharePoint resource (`https://{tenant}.sharepoint.com` or `-my.sharepoint.com`),
scope `AllSites.Write` / `MyFiles.Write`. Same driveItem calls, different base URL.

Full token flows, scopes, and consent are in [`references/api.md`](references/api.md#authentication).

## Step 3 — Confirm, then publish

### Confirm before writing

First **preflight** the HTML — run `scripts/preflight.sh <file>`; it greps for forbidden APIs and checks
LiveData manifest items (file items need `spItemUrl` + `fileName`; `kind:"list"` items need `spItemUrl` +
`webUrl` + `listId`) ("renders blank with no error" is the top failure). Then **list the destination
folder** (`GET …/children`) to detect a name collision, so you can tell the user accurately whether this
is a **create** or an **overwrite**.

Before the upload call, show the user exactly what will happen and get a yes:

```
About to publish to SharePoint/OneDrive:
  Account:   user@contoso.com
  Location:  OneDrive  ›  Documents/Agent HTML/
  File:      sales-dashboard.html
  Action:    Create new file            (or: Overwrite existing file — REPLACES its contents)
  Renders at: <webUrl>?web=1   (?web=1 opens the OneUp viewer; the bare webUrl downloads)
Proceed?
```

Only continue on an explicit yes. For overwrite, make the destructive nature explicit.

### Publish via Microsoft Graph (primary)

Simple upload (files ≤ 4 MB — plenty for inlined HTML). New file by path:

```
PUT https://graph.microsoft.com/v1.0/me/drive/root:/Agent HTML/<name>.html:/content
Authorization: Bearer <token>
Content-Type: text/html

<!DOCTYPE html> … your document …
```

Response `201 Created` (new) / `200 OK` (replace) → a **driveItem**. Read **`webUrl`**, then
give the user `<webUrl>?web=1` — the `?web=1` opens it in the OneUp viewer; the bare `webUrl`
downloads the .html file:

```json
{
  "id": "01ABC…",
  "name": "sales-dashboard.html",
  "size": 84213,
  "webUrl": "https://contoso-my.sharepoint.com/personal/user_contoso_com/Documents/Agent%20HTML/sales-dashboard.html",
  "file": { "mimeType": "text/html" }
}
```

For files > 4 MB use an **upload session** (`createUploadSession`) — see
[`references/api.md`](references/api.md#large-files-upload-session).

### Publish via SharePoint Vroom (alternative)

Same shape, SharePoint base URL, SharePoint-audience token. Use this when you already hold a
SharePoint OAuth token (SPFx / add-in / on-behalf-of) or want to target a specific SharePoint host
or site directly. (`graph.microsoft.com` already routes own-drive uploads to the caller's farm —
including dogfood rings like `*.sharepoint-df.com` — so Graph alone is usually enough.)

```
PUT https://{tenant}-my.sharepoint.com/_api/v2.0/me/drive/root:/Agent HTML/<name>.html:/content
Authorization: Bearer <sharepoint-token>
Content-Type: text/html

<!DOCTYPE html> … your document …
```

Returns the same driveItem (read `webUrl`). Full details, including site-drive paths
(`/_api/v2.0/drives/{driveId}/items/{itemId}/content`), in
[`references/api.md`](references/api.md#vroom-sharepoint-_apiv20).

### Publish into a SharePoint site library (instead of your OneDrive)

Same call against a **site drive**. With Graph (scope `Sites.ReadWrite.All`):

```
PUT https://graph.microsoft.com/v1.0/sites/{site-id}/drive/root:/Agent HTML/<name>.html:/content
```

or Vroom against the site host:

```
PUT {siteUrl}/_api/v2.0/drive/root:/Agent HTML/<name>.html:/content
```

The site drive root is its default document library ("Shared Documents"), so keep the path
root-relative. Resolve `{site-id}` with `GET /sites/{host}:/sites/{path}` (or `/teams/{path}`).

### Publish by folder URL — fewest calls (Shares API)

If you only have the **destination folder's URL**, skip resolving drive/site ids — encode the URL as
a sharing token and upload into it directly:

1. Encode: `u!` + unpadded base64url of the folder URL (base64, strip `=`, `/`→`_`, `+`→`-`).
2. `GET /shares/{u!token}/driveItem` → the folder's `id` + `parentReference.driveId` (one call).
3. `PUT /drives/{driveId}/items/{folderId}:/<name>.html:/content` → upload.

That's **2 calls**, and it works for any OneDrive, site, or library. Details in
[`references/api.md`](references/api.md#publish-by-folder-url-shares-api--fewest-calls); ready-made
script: [`scripts/publish-to-folder.sh`](scripts/publish-to-folder.sh).

## Step 4 — Open it

Give the user `<webUrl>?web=1` (the `webUrl` from the response with `?web=1` appended). The
`?web=1` renders the HTML in the OneUp viewer; the bare `webUrl` downloads the .html file.
`webUrl` is **stable across updates**, so links keep working after you modify.

---

## Updating / modifying an asset you created

To change a published file, **overwrite it** — same path (or item id), same call:

```
PUT https://graph.microsoft.com/v1.0/me/drive/items/{item-id}/content
Authorization: Bearer <token>
Content-Type: text/html

<!DOCTYPE html> … updated document …
```

or by path: `PUT /me/drive/root:/Agent HTML/<name>.html:/content`.

**Overwrite replaces the file's contents — confirm with the user first** (show the target
+ that it replaces the existing file). The `webUrl` stays the same. Vroom is identical with
its base URL. To rename/move instead of replace content, use `PATCH …/items/{item-id}`
(see [`references/api.md`](references/api.md#update-metadata-rename--move)).

---

## Error codes

| Code | Meaning | Action |
| :--- | :--- | :--- |
| `401` | Unauthorized | Missing/expired token, or wrong audience (Graph vs SharePoint). Re-acquire with the right scope. |
| `403` | Forbidden | Token lacks write scope (`Files.ReadWrite`), or the user can't write that location. |
| `404` | Not found | Wrong drive/item/path, or the parent folder doesn't exist (create it first). |
| `413` | Payload too large | File > 4 MB on simple upload — use an upload session. |
| `423` | Locked | The item is checked out / locked. |
| `507` | Insufficient storage | The user's drive is full. |

Blank / half-rendered page after opening → an authoring-contract violation (usually an
external resource or a runtime `fetch`). Re-check the [contract](#the-authoring-contract-make-html-render-in-oneup).

---

## Reference

- [`references/api.md`](references/api.md) — full Graph + Vroom endpoint reference:
  authentication & scopes, token acquisition, request/response schemas, upload sessions,
  metadata update, and the driveItem shape.
- [`references/contract.md`](references/contract.md) — the OneUp authoring contract in full.
- [`assets/templates/`](assets/templates/) — ready-made CSP-compliant templates.
- **Live docs** (authoritative, tenant-specific): `https://<your-sharepoint-host>/_html`,
  `/_html/llms.txt`, `/_html/help.json`.
