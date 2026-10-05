---
name: sap-developers-mcp
description: Use when connecting an MCP client (Claude Code, Claude Desktop, Joule, Cursor, or any MCP-compatible agent) to the SAP Developers hosted MCP server to search tutorials, read missions and the knowledge graph, or access personalized tutorial progress. Covers the anonymous read-only endpoints plus authenticated access via Personal Access Token (PAT) and OAuth, including the XSUAA "does not support dynamic client registration" workaround.
---

# SAP Developers hosted MCP server

The SAP Developers site ([developers.sap.com](https://developers.sap.com)) exposes a hosted
**Model Context Protocol** server so any MCP client can search tutorials, read missions, query the
knowledge graph, and (when signed in) read personal tutorial progress — no scraping, no SDK.

The server speaks **Streamable HTTP** (MCP protocol `2025-06`). It is built on `@cap-js/mcp` over
the platform's CAP backend, and each service is mounted at its own path — **there is no aggregate
`/mcp` root**.

## Base URLs

- **Production:** `https://developers.sap.com`
- **Dev:** ask your admin for the current dev route

Replace `<base>` below with the right host.

## Three access tiers

| Namespace | Auth | Use for |
| --- | --- | --- |
| `/mcp/*` | none (anonymous, read-only) | search, missions, news/videos, knowledge graph |
| `/mcp-pat/api` | Personal Access Token (bearer header) | headless/CI + personal progress — **simplest** |
| `/mcp-auth/api` | OAuth 2.1 (XSUAA, via `mcp-remote`) | interactive personal progress in a desktop client |

Pick anonymous unless you need *your* tutorial progress or personalized recommendations.

## Anonymous (read-only) — start here

Three services, each mounted separately:

| Service | Endpoint | Tools |
| --- | --- | --- |
| Search | `<base>/mcp/search` | `search_tutorials`, `list_missions`, `get_mission`, `get_tutorial`, `search_events` |
| Homepage | `<base>/mcp/homepage` | `get_recent_news`, `get_recent_videos`, `get_news_detail` |
| Knowledge graph | `<base>/mcp/graph` | `kg_prerequisites`, `kg_what_to_learn_next` |

Each service also auto-exposes `describe` (returns the service CSN) and a generic CQN `query` tool.

**Add to Claude Code:**

```bash
claude mcp add --transport http sap-developers-search https://developers.sap.com/mcp/search
```

**Claude Desktop / any MCP client** (`.mcp.json`, or the client's server config):

```json
{
  "mcpServers": {
    "sap-developers-search":   { "type": "http", "url": "https://developers.sap.com/mcp/search" },
    "sap-developers-homepage": { "type": "http", "url": "https://developers.sap.com/mcp/homepage" },
    "sap-developers-graph":    { "type": "http", "url": "https://developers.sap.com/mcp/graph" }
  }
}
```

**Reachability check** (expect an SSE `text/event-stream` reply):

```bash
curl -sS -X POST https://developers.sap.com/mcp/search \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```

## Authenticated — personal progress

Authenticated tools live on **DeveloperService + HomepageService**:

| Tool | What it does |
| --- | --- |
| `get_my_tutorials` | your in-progress and completed tutorials |
| `get_my_missions` | your mission progress |
| `get_my_events` | your registered upcoming events |
| `get_my_completed_steps` | completed step numbers for one tutorial |
| `get_tutorial_step` | full HTML of a tutorial step |
| `complete_step` | mark a step done (needs `write` scope) |
| `reset_tutorial_progress` | reset all progress on a tutorial (needs `write` scope) |
| `get_my_recommended_tutorials` | persona-ranked tutorial recommendations |
| `get_my_recommended_missions` | persona-ranked mission recommendations |

### Option A — Personal Access Token (recommended, no browser flow)

Simplest for Claude Code, CI, and headless agents.

1. Sign in to `<base>/me/tokens/` (needs the **Tutorials MCP Users** role collection).
2. **Create token** → name it, pick scopes (`read`, or `read write` to allow `complete_step` /
   `reset_tutorial_progress`), set a TTL. The token is shown **once** — copy it immediately (the
   server stores only a SHA-256 hash).
3. Point your client at `/mcp-pat/api` with a bearer header:

```json
{
  "mcpServers": {
    "sap-developers-auth": {
      "url": "https://developers.sap.com/mcp-pat/api",
      "headers": { "Authorization": "Bearer pat_..." }
    }
  }
}
```

An expired or revoked PAT returns `401`.

### Option B — OAuth via `mcp-remote`

> **Native `type: http` OAuth does NOT work against this server.** Claude Code's and Claude
> Desktop's built-in OAuth clients require **Dynamic Client Registration** (RFC 7591); XSUAA
> requires a **pre-registered** client, so they fail with
> `does not support dynamic client registration`. Bridge through `mcp-remote`, which accepts a
> pre-registered `client_id`.

```bash
npm install -g mcp-remote
```

```json
{
  "mcpServers": {
    "sap-developers-auth": {
      "command": "npx",
      "args": [
        "-y", "mcp-remote", "https://developers.sap.com/mcp-auth/api",
        "--static-oauth-client-info", "{\"client_id\":\"sb-tutorials-prod!t676072\"}",
        "--host", "localhost"
      ]
    }
  }
}
```

The flow is authorization-code + PKCE (no client secret); endpoints are discovered from
`<base>/.well-known/oauth-authorization-server`. First run opens a browser for SAP universal-ID
consent; the token is then cached in `~/.mcp-auth/` and refreshed silently.

**The `client_id` is environment-specific:**

| Environment | `<base>` | `client_id` |
| --- | --- | --- |
| Production | `https://developers.sap.com` | `sb-tutorials-prod!t676072` |
| Dev | your dev route | `sb-tutorials!t676072` |

To confirm the id for your environment, read the bound credentials:
`cf env tutorials-prod-srv` (prod) or `cf env tutorials-srv` (dev) →
`VCAP_SERVICES.xsuaa[0].credentials.clientid`.

## Resources & prompts

The server also exposes MCP **resources** (`resources/list`, `resources/read`):

- `tutorial://<slug>` — a tutorial's metadata, step titles, and rendered HTML
- `mission://<slug>` — a mission and its ordered tutorials
- `concept://<id>` — a knowledge-graph concept and the tutorials that teach it

…and reusable **prompt templates** (`prompts/list`, `prompts/get`):

| Prompt | Arguments |
| --- | --- |
| `summarize_mission_for_beginner` | `mission_slug` |
| `generate_lab_exercise` | `tutorial_slug`, `step?` |
| `explain_concept` | `concept_id` |
| `suggest_learning_path` | `from_slug`, `to_slug` |

## Older stdio-only clients

Clients that only speak stdio bridge through `mcp-remote`:

```json
{
  "mcpServers": {
    "sap-developers-search": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://developers.sap.com/mcp/search"]
    }
  }
}
```

## Troubleshooting

| Symptom | Cause / fix |
| --- | --- |
| `initialize` returns `401` | You hit `/mcp-auth/*` anonymously. Use `/mcp/*` for anonymous access. |
| `tools/list` is empty | Wrong path. Each service mounts separately — `/mcp/search`, `/mcp/homepage`, `/mcp/graph`. No aggregate `/mcp` root. |
| `does not support dynamic client registration` | Native OAuth needs DCR; XSUAA doesn't. Use `mcp-remote` + `--static-oauth-client-info`, or a PAT. |
| `redirect_uri does not match the configuration` | `mcp-remote` bound the callback to `127.0.0.1`. Pass `--host localhost`; delete `~/.mcp-auth/` and reconnect. |
| Silent OAuth failure | You used `--static-oauth-client-id` (not a real flag — ignored). Use `--static-oauth-client-info '{"client_id":"…"}'`. |
| First response slow (5–15s) | Cold start; the backend spins down when idle. Retries are fast. |
| Nothing returns, no error | Anonymous per-IP throttle. Back off and retry. |
| `The request for authorization was invalid` | Wrong `client_id` for the environment (e.g. dev id against prod). Match the table above. |

## Conventions

- **Anonymous is read-only.** `/mcp/*` never mutates state. Only `complete_step` /
  `reset_tutorial_progress` (authenticated, `write` scope) write.
- **Lowercase slugs.** Slugs are lowercased server-side, but pass them lowercase.
- **Shared resource.** Respect the per-IP throttle; a `429`/silent stall means back off.

## Full reference

- End-user quickstart (all clients, incl. Joule Work Desktop / Joule Studio): [docs/end-users/mcp-quickstart.md](../../docs/end-users/mcp-quickstart.md)
- Per-tool parameter & return shapes: [docs/developers/reference/mcp-server.md](../../docs/developers/reference/mcp-server.md)
