---
name: picsee-short-link
description: PicSee URL shortener via MCP — shorten URLs, generate QR codes, view rich click analytics (daily / platform / referrer / region / audience), and manage links. Use when the user asks to shorten a URL, see link analytics, list/search short links, edit/delete links, or mentions PicSee. Anonymous mode supports `create_short_link` only; OAuth 2.1 unlocks the full 14-tool authenticated surface.
license: MIT
compatibility: Requires an MCP-compatible client with Streamable HTTP transport (or a stdio bridge such as `mcp-remote`). Internet access to `api.picsee.io` and `public-api-oauth.picsee.io`.
metadata:
  author: picsee
  version: "3.0.2"
  emoji: "🔗"
  repository: https://github.com/PicSeeInc/picsee-short-link
  mcp_url: https://api.picsee.io/mcp
  mcp_command: npx mcp-remote https://api.picsee.io/mcp
  oauth_authorization_server: https://public-api-oauth.picsee.io
  scopes: "user:read user:write"
---

# PicSee Short Link

URL shortener with **rich click analytics** and full **link management** — exposed to AI agents through the **PicSee MCP server** at `https://api.picsee.io/mcp`.

The skill ships no code: it just teaches your agent how to call the MCP server. Authentication is handled by **OAuth 2.1 with PKCE** (Dynamic Client Registration), so no API tokens are ever stored on disk by the skill.

---

## Installation

Add the PicSee MCP server to your AI client's MCP config. Pick the transport your client supports — most modern clients speak Streamable HTTP directly.

### Streamable HTTP (recommended)

```json
{
  "mcpServers": {
    "picsee-short-link": { "url": "https://api.picsee.io/mcp" }
  }
}
```

### Stdio bridge (for clients without remote-MCP support)

```json
{
  "mcpServers": {
    "picsee-short-link": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://api.picsee.io/mcp"]
    }
  }
}
```

See [README.md](README.md) for the exact config file path on each platform.

---

## Authentication

### Anonymous mode (no setup)

`create_short_link` is callable with no credentials. Anonymous calls are pinned to `pse.is` and have no access to `externalId` filtering / attribution dashboards.

### Authenticated mode (OAuth 2.1)

On the first authenticated tool call, the MCP client triggers an OAuth flow:

1. Dynamic Client Registration → `https://public-api-oauth.picsee.io/oauth/register`
2. Browser → `https://public-api-oauth.picsee.io/oauth/authorize`
3. User signs in to PicSee and grants `user:read` + `user:write`
4. Client receives access + refresh tokens via PKCE/S256
5. Token is stored by the MCP client — **never** by this skill

All 14 authenticated tools become available after this flow.

---

## Tools

15 tools total. `create_short_link` is callable anonymously; the rest require OAuth.

### `create_short_link` *(anonymous OK)*

Create a new short link.

| Field | Required | Notes |
|-------|----------|-------|
| `url` | ✅ | Destination URL, ≤2048 chars |
| `encodeId` | | Custom slug, 3–90 chars (letters / digits / `_` / `-` / Chinese). Must be globally unique — conflicts return `PUB00503` |
| `domain` | | `pse.is` or a BSD from `get_my_domains`. **Ignored when called anonymously** |
| `externalId` | | 1–100 chars. Agents SHOULD default this to their own product name — see [Attribution](#attribution) |
| `utm` | | `{ source, medium, campaign, term, content }` |
| `title` | | OG preview title, 3–300 chars |
| `description` | | OG preview description, 3–300 chars |
| `imageUrl` | | OG preview image URL |
| `tags` | | Array of up to 3 tag names — use `get_my_tags` to offer a picker |
| `targets` | | Device-specific redirects, see below |
| `fbPixel` | | Meta Pixel ID — must already be saved in PicSee (`get_my_tracking_tools`) |
| `gTag` | | GTM container ID — must already be saved in PicSee (`get_my_tracking_tools`) |
| `pathFormat` | | `{ key: "<param-name>" }` — Path Parameterization add-on (paid Advanced) |

`targets[].target` enum: `ios_android`, `ios`, `ios_store`, `android`, `android_store`, `ios_line`, `ios_safari`, `android_fb`, `pc_mac`, `pc`, `mac`, `facebook`, `twitter`. `ios_android` = all mobile; `pc_mac` = all desktop. App-store buckets only fire for users with the app installed.

Returns `picseeUrl` (the shortened link).

### Account / discovery tools

#### `get_api_status`

No params. Returns the account's API plan, lifetime quota, current period usage, and plan expiration. **Call this before bulk operations** to confirm remaining quota.

#### `get_api_usage_by_external_id`

| Field | Required | Notes |
|-------|----------|-------|
| `startTime` | | Taipei time `YYYY-MM-DDTHH:mm:ss`. Defaults to 30 days before `endTime` |
| `endTime` | | Taipei time `YYYY-MM-DDTHH:mm:ss`. Defaults to current hour. Max 31-day range |

Returns API-link counts grouped by `externalId` — useful for attributing usage to agents / campaigns.

#### `get_my_domains`

No params. Lists every short-link domain on the account: brand short domains (BSDs), PicSee subdomains, shared root. Each entry flags HTTPS support and default status. **Call before `create_short_link`** if the user wants a non-default domain.

#### `get_my_tags`

No params. Returns `{ id, value }` pairs, where `value` is the tag name accepted by `tags` on `create_short_link` / `edit_short_link`.

#### `get_my_tracking_tools`

No params. Returns previously-used UTM sources / mediums, saved Meta Pixels, and saved GTM containers. Use to populate pickers instead of asking the user to retype IDs.

### `list_short_links`

| Field | Notes |
|-------|-------|
| `limit` | 1–50, default 20 |
| `startTime` | Taipei time `YYYY-MM-DDTHH:mm:ss`. **Returns links created _at or before_ this timestamp** — i.e. queries backward. Default = now |
| `prevMapId` | Cursor: return links with `mapId` older than this. Combine with `startTime` for AND filtering |
| `isAPI` | `true` (default) = only API-created links; `false` = only website-created |
| `isStar` | `true` = starred only. Default `false` |
| `externalId` | Exact-match filter |
| `search.encodeId` | Exact slug — priority 1, overrides all other search fields |
| `search.authorId` | Filter by author's PicSee user ID — priority 2 |
| `search.tag` | Tag name, 3–30 chars — priority 3 |
| `search.keyword` | Substring, 3–30 chars — priority 4 |

**Tip**: when the user says "links from March 2026", pass `startTime: "2026-03-31T23:59:59"` (the end of the period) — the server queries backward from there.

### `edit_short_link`

| Field | Required | Notes |
|-------|----------|-------|
| `encodeId` | ✅ | Slug of the link to edit |
| `url` | | New destination. May be rejected with `PUB00510` if the new origin is on a different brand |
| `domain` | | |
| `title` / `description` / `imageUrl` | | 3–300 chars for text fields |
| `tags` | | Up to 3 |
| `targets` | | Same enum as `create_short_link` |
| `fbPixel` / `gTag` | | Pass `null` to clear |
| `utm` | | Pass `null` to clear all UTM params |
| `expireTime` | | Future Taipei time `YYYY-MM-DDTHH:mm:ss`, or `null` to remove. Requires the expiration add-on |

### `delete_short_link`

| Field | Required | Notes |
|-------|----------|-------|
| `encodeId` | ✅ | |
| `value` | | `delete` (default) = move to trash; `recover` = restore from trash |

- Starred links can't be deleted (`PUB00706`) — unstar via web first.
- Links trashed for >30 days can't be recovered (`PUB00704`).

### Per-link analytics

All five tools share the same shape: required `encodeId`, optional `startTime` / `endTime` (Taipei `YYYY-MM-DDTHH:mm:ss`). Default window is the last 30 days; Advanced plan can look back up to 365 days.

| Tool | Returns |
|------|---------|
| `get_link_overview` | Total clicks, unique clicks, destination URL, domain, HTTPS flag, creation time. **Use for at-a-glance summaries** |
| `get_link_daily_clicks` | Time-series of total + unique clicks aggregated by day. Use as raw data for chart rendering |
| `get_link_platforms` | Unique-click breakdown by device (`iphone`, `android`, `windows`, `macintosh`, …). Aggregate to mobile/desktop client-side if needed |
| `get_link_referrers` | Unique-click breakdown by referrer (search engines, social, AI agents, long-tail). Clicks without referrer info → `direct` |
| `get_link_regions` | Unique-click breakdown by country (no city-level data). Unknown countries → `Others` (`code: "others"`) |
| `get_link_audience_labels` | Interest + brand labels. **Privacy guard**: only returns data when the link has >100 lifetime unique clicks; otherwise both arrays come back empty. No `startTime` / `endTime` — covers link lifetime |

---

## Attribution

The `create_short_link` schema asks the calling agent to set `externalId` to its own product name when the user hasn't specified one. PicSee account owners use this to attribute API usage in their dashboard.

| Agent | Recommended `externalId` |
|-------|--------------------------|
| Claude Code | `Claude Code` |
| Cursor | `Cursor` |
| Codex / Codex CLI | `Codex` |
| Antigravity | `Antigravity` |
| OpenClaw / ClawHub | `OpenClaw` |
| Gemini CLI | `Gemini CLI` |
| GitHub Copilot | `Copilot` |
| ChatGPT | `ChatGPT` |

Rules:
- Canonical product name only — no version numbers, session IDs, or user names.
- If the user explicitly provides an `externalId`, **always honor their value** instead.

---

## Agent Recipes

The MCP server intentionally doesn't ship QR or chart-rendering tools — those are easier to compose client-side from public services.

### Generate a QR code from a short link

Construct a URL against [api.qrserver.com](https://goqr.me/api/):

```
https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=<URL-encoded-short-link>
```

Surface the URL inline if your client renders images; otherwise return it as a link. For a larger code, change `size=500x500`.

### Render a daily-clicks chart

1. Call `get_link_daily_clicks` to get the time series.
2. Build a [QuickChart](https://quickchart.io) URL from the data:

```
https://quickchart.io/chart?c={type:'line',data:{labels:['2026-03-01',...],datasets:[{label:'Clicks',data:[12,38,...]}]}}
```

URL-encode the `c` parameter. Display inline if possible; otherwise return the link.

---

## Common Workflows

### Shorten a URL with full attribution

1. Call `create_short_link` with `url` and `externalId` = your agent name.
2. Return `picseeUrl` to the user.
3. If the user wanted a custom slug and got `PUB00503`, suggest an alternative.

### Pick a branded short domain

1. `get_my_domains` to enumerate BSDs + PicSee subdomains.
2. Offer the user a picker (note which is `isDefault`).
3. Pass the chosen `domain` to `create_short_link`.

### Show analytics for a link

1. `get_link_overview` for the headline numbers.
2. If the user wants breakdowns, call one or more of `get_link_daily_clicks` / `get_link_platforms` / `get_link_referrers` / `get_link_regions` / `get_link_audience_labels`.
3. For audience labels: warn the user if the link has ≤100 unique clicks (data will be empty due to the privacy guard).

### List the user's recent links

1. Call `list_short_links` with the user's filters.
2. If they say "March 2026", pass `startTime: "2026-03-31T23:59:59"`.
3. Paginate with `prevMapId` from the last result if they ask for more.

### Migrate a link to a new destination

1. `edit_short_link` with `encodeId` + new `url`.
2. If you get `PUB00510`, the brand of the new URL doesn't match. Tell the user.

### Track API usage by agent

`get_api_usage_by_external_id` with no params returns the last 30 days, grouped by attribution tag. Useful for "which AI created most of my links?"

---

## Migration from v2.x

v2.x was a Node.js CLI that stored an encrypted API token under `~/.openclaw/`. v3.0.0 removes that entirely — no CLI, no token files, no Node.js requirement on the agent side.

```bash
# Clean up v2 artifacts
rm -f ~/.openclaw/.picsee_token ~/.openclaw/.picsee_salt
rm -rf ~/.claude/skills/picsee-short-link/cli
rm -rf ~/.openclaw/workspace/skills/picsee-short-link/cli
```

Behavioral changes:
- **Auth**: long-lived API token → OAuth 2.1 + PKCE (browser sign-in on first authenticated call)
- **QR / chart**: were CLI subcommands → now agent recipes against `api.qrserver.com` / `quickchart.io`
- **`delete` vs `recover`**: were two CLI commands → one tool `delete_short_link` with `value: "delete" | "recover"`
- **Analytics**: was a single `analytics` command → split into 6 granular tools (`get_link_overview` + 5 dimensional breakdowns)
- **Per-account discovery**: new tools `get_my_domains`, `get_my_tags`, `get_my_tracking_tools`, `get_api_status`, `get_api_usage_by_external_id` have no v2 equivalent

---

## Error codes

| Code | Meaning |
|------|---------|
| `PUB00503` | `encodeId` (custom slug) already taken |
| `PUB00510` | New `url` rejected on edit — different brand than the original |
| `PUB00704` | Cannot recover a link that has been in trash >30 days |
| `PUB00706` | Cannot delete a starred link — unstar it via the PicSee web app first |

---

## References

- PicSee website: https://picsee.io
- Developer docs: https://picsee.io/developers
- MCP spec: https://modelcontextprotocol.io
- OAuth 2.1 (MCP profile): https://modelcontextprotocol.io/specification/draft/basic/authorization
