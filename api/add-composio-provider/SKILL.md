---
description: Add a new Composio OAuth provider (toolkit) for connected accounts. Wires up the slug across providers list, proxy allowlist, scope map, scope descriptions, agent service discovery, system prompt, and downloads the icon.
---

# Add a Composio OAuth Provider

Adds support for a new connected-account service backed by Composio's managed OAuth (e.g. Google Slides, Notion, Linear). The provider's toolkit slug must be threaded through several files; missing any one will silently degrade behavior (no icon, blocked proxy requests, missing scope-consent text, agent can't discover it, etc.).

## Pre-flight: confirm Composio supports the provider

1. Check the Composio toolkit page exists, e.g. `https://docs.composio.dev/toolkits/<slug>`.
2. Confirm **"Composio Managed App Available? Yes"** — without managed auth we can't auto-create the auth config. If it's only available via custom OAuth, stop and ask the user how to proceed.
3. Note the canonical **toolkit slug** (lowercase, no spaces; usually no hyphen for Google services — `googleslides`, not `google-slides`). This slug is what gets passed to Composio's API and what we key everything off of.
4. Note the **API host(s)** the toolkit calls (e.g. `slides.googleapis.com`) — the proxy allowlist needs them or requests will 403.
5. Note the **OAuth scopes** the toolkit requests and brief end-user-facing descriptions. Source of truth: the provider's official scope reference docs.

## Files to update (all required)

The list below is exhaustive — every place where an existing peer toolkit (e.g. `googlecalendar`) appears, the new slug must appear too. Use it as a checklist.

### 1. `src/shared/lib/composio/providers.ts`
Add an entry to `SUPPORTED_PROVIDERS` (the master list shown in the Connections settings UI):
```ts
{
  slug: 'googleslides',
  displayName: 'Google Slides',
  icon: 'presentation',     // Lucide icon name; only a hint — actual rendering uses the SVG below
  description: 'Google presentations',
},
```

### 2. `src/shared/lib/composio/client.ts`
If the provider is Google or Microsoft, add the slug to `googleToolkits` / `microsoftToolkits` inside `getAccountDisplayName()` so the connected-account label resolves to the user's email instead of the generic provider name.

### 3. `src/shared/lib/proxy/allowed-hosts.ts`
Add the API host(s) to `TOOLKIT_ALLOWED_HOSTS`. The proxy rejects any host not in this list, so missing entries = all calls 403.
```ts
googleslides: ['slides.googleapis.com', 'www.googleapis.com'],
```

### 4. `src/shared/lib/proxy/allowed-hosts.test.ts`
Add the slug to the `expectedToolkits` array in the "has entries for all expected toolkits" test, so we don't silently drop providers from the allowlist.

### 5. `src/shared/lib/proxy/scope-maps.ts`
Add an entry mapping HTTP method + path patterns → sufficient OAuth scopes. The proxy uses this to compute which scope a request needs, and the scope-policy editor uses `allScopes` for the consent UI.
```ts
"googleslides": {
  provider: "googleslides",
  apiHost: "slides.googleapis.com",
  basePath: "",
  allScopes: ["drive", "drive.file", "drive.readonly", "presentations", "presentations.readonly"],
  scopeMap: [
    { method: "POST", pathPattern: "/v1/presentations", sufficientScopes: ["drive", "drive.file", "presentations"], description: "Creates a blank presentation..." },
    // … one entry per endpoint we expect agents to hit
  ],
},
```
Pull endpoint paths + scope requirements from the provider's REST reference (e.g. `developers.google.com/workspace/slides/api/reference/rest/v1/...`).

### 6. `src/shared/lib/proxy/scope-descriptions.ts`
Add an entry to `SCOPE_DESCRIPTIONS` with end-user-friendly text for **every** scope listed in `allScopes` from step 5. The structural test (`scope-descriptions.test.ts`) enforces a 1:1 match — both directions:
- every scope in `allScopes` has a description here
- no description keys reference scopes outside `allScopes`

```ts
"googleslides": {
  "drive": "See, edit, create, and delete all of your Google Drive files",
  "drive.file": "...",
  "drive.readonly": "...",
  "presentations": "See, edit, create, and delete all your Google Slides presentations",
  "presentations.readonly": "View your Google Slides presentations",
},
```

### 7. `agent-container/src/tools/search-connected-account-services.ts`
Add the slug to the `SERVICES` array so the agent's `search_connected_account_services` tool can discover it.

### 8. `agent-container/src/system-prompt.md`
Add the slug to the appropriate category in the "Supported services include" line in the Requesting Connected Accounts section. This is what the agent reads to know what's available without calling the search tool first.

### 9. `scripts/download-service-icons.ts`
Add the slug to `ALL_SLUGS`. If the Composio logos API serves the icon under a different name (test with `curl -sI https://logos.composio.dev/api/<name>`), also add a `SLUG_TO_API_NAME` mapping. Many Google services need hyphenation (`googlesheets` → `google-sheets`), but **not** all of them — `googleslides` works as-is.

### 10. Download the icon (manual, single-file)
Do **not** run the full `download-service-icons.ts` script — it re-fetches every icon and Composio routinely ships updated SVGs, producing dozens of unintended diffs. Instead fetch only the new one and apply the script's normalization manually:

```bash
# Try the bare slug first; if 404, try with hyphens (google-sheets style).
curl -s 'https://logos.composio.dev/api/<slug>' -o src/renderer/public/service-icons/<slug>.svg
```

Then strip `width="…"` and `height="…"` from the root `<svg>` tag (the script's `normalizeSvg` does this — needed so the icon scales with CSS). Quick verify:
```bash
head -1 src/renderer/public/service-icons/<slug>.svg
# should start with <svg viewBox="…"  (no width/height)
```

## Verify

```bash
npx tsc --noEmit
cd agent-container && npx tsc --noEmit && cd ..
npx eslint 'src/shared/lib/composio/**/*.ts' 'src/shared/lib/proxy/**/*.ts' 'scripts/download-service-icons.ts'
npx vitest run src/shared/lib/proxy/
```

The proxy test suite includes the structural contract tests on `SCOPE_DESCRIPTIONS` ↔ `SCOPE_MAPS` and the toolkit-allowlist coverage check — both will fail loudly if any of steps 4 / 5 / 6 are out of sync.

## Sanity checklist

Before reporting done, confirm `git status` shows:
- 9 modified `.ts` / `.tsx` / `.md` files (steps 1–9)
- 1 new `.svg` file under `src/renderer/public/service-icons/`
- **no other SVGs touched** — if you see them, you accidentally ran the full icon-download script; `git restore src/renderer/public/service-icons/` and redo step 10 manually.
