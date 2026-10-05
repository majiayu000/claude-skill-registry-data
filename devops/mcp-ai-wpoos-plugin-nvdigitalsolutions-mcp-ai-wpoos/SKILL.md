---
type: Skill
name: mcp-ai-wpoos-plugin
description: Complete operational guide for the NV oOS (Open Operator System) WordPress plugin in Docker/WSL2 — setup, assistant creation, credential tokens, MCP tool calling, API key auto-detection, env var bridging, common fixes, and IGCSE study configuration. Use when setting up the plugin for the first time, creating assistants programmatically, generating MCP bridge tokens, troubleshooting Docker path issues, bridging API keys, or calling tools via JSON-RPC over HTTP.
license: Proprietary. See LICENSE.txt
metadata:
  plugin: mcp-ai-wpoos
  plugin-version: "1.1.91"
  plugin-version-tested: "1.1.91"
  last-updated: "2026-10-01"
---
# NV oOS Plugin — Docker/WSL2 Setup & Operational Guide

Complete operational skill for the NV Digital Open Operator System (oOS)
WordPress plugin running in Docker on Windows/WSL2. Covers the full lifecycle:
startup, assistant creation, credential tokens, MCP tool calling, API key
auto-detection, and tool assignment.

## When to use this skill

- Setting up the plugin in a Docker Compose stack for the first time
- Plugin produces `file_put_contents` / `mkdir` PHP warnings on startup
- Docker volume mount fails with "invalid volume specification"
- Need to create an assistant programmatically (not via admin UI)
- Need to generate a `cred_xxxxx.SECRET` token for the MCP bridge
- Calling MCP tools via `curl` / HTTP JSON-RPC
- API keys not being picked up from Docker environment variables
- Troubleshooting 0 tools returned from `tools/list` (or HTTP 403 `wp_mcp_ai_assistant_scope_required` — strict-scope toggle, v1.1.90+)
- Configuring the plugin for IGCSE study (which tools to assign)
- WordPress.org submission prep — Plugin Check (PCP) runs, wp.org listing
  screenshots, packaging exclusions, and the compliance checklist are covered
  by the `.agents/skills/mcp-ai-wpoos-wporg-submission` skill instead of this
  one (see that skill for Docker PCP recipes and the CI gate anatomy)

## Architecture

```
Zed / Claude Desktop / Cursor
        │
        │ MCP JSON-RPC over HTTP
        ▼
┌─────────────────────────────────┐
│  WordPress REST API              │
│  /wp-json/mcp-ai/v1/mcp         │  ← MCP endpoint
│  Auth: Bearer cred_xxxxx.SECRET │
└──────────────┬──────────────────┘
               │
     ┌─────────┴──────────┐
     │  WP_MCP_AI_*       │
     │  Tool Registry     │  ~347 base / ~1,648 full tools
     │  Credentials       │  Token validation
     │  Assistant (CPT)   │  Post type: mcp_ai_assistant
     └────────────────────┘
```

## Quick Start (Docker)

### 1. Environment Setup

The docker-compose.yml uses **relative paths** (`.`) for volume mounts,
which Docker Desktop translates automatically for WSL2 — no manual path
fix needed.

```bash
cp .env.example .env
# Edit .env: set BASE_URL=http://localhost:8000 and add API keys
wsl docker compose up -d
# Wait for wp-plugin-seed to exit (installs WP + activates plugin)
wsl docker compose logs -f wp-plugin-seed
```

WordPress is at `http://localhost:8000`, admin at `/wp-admin`
(**admin / password**).

### Design Stack deployment (F:\GITHUB\design-stack)

The environment actually operated day-to-day uses different ports and
credentials than this repo's dev compose (verified on the live stack,
2026-09 session):

| Service | Address |
|---|---|
| WordPress | `http://localhost:8092` — admin at `/wp-admin` (**admin / design_admin_2026**) |
| Media worker | `http://localhost:3100` |
| MySQL | `localhost:3308` |

- The stack mounts the plugin from `design-stack/plugins/mcp-ai-wpoos` — an
  NTFS junction to the plugin repo — so code edits land in this repo.
- `design-stack/.agents/skills/design-*` and `mcp-ai-wpoos-plugin` are
  junctions into this repo's `.agents/skills/` (creation script:
  `bin/create-skill-junctions.ps1`), so skill edits ship in the same PR as
  plugin code.
- `wp` inside the Design Stack WP container requires `--allow-root`.

### 2. API Key Auto-Detection (v1.1.47+)

On activation, the plugin now **automatically reads** well-known environment
variables and populates settings. No manual bridging script needed.

| Environment Variable | Plugin Setting |
|----------------------|---------------|
| `OPENAI_API_KEY` | `openai_api_key` |
| `GEMINI_API_KEY` / `GOOGLE_API_KEY` | `gemini_api_key` |
| `ANTHROPIC_API_KEY` | `anthropic_api_key` |
| `DEEPSEEK_API_KEY` | `deepseek_api_key` |
| `BRAVE_API_KEY` / `BRAVE_SEARCH_API_KEY` | `brave_search_api_key` |
| `TAVILY_API_KEY` | `tavily_api_key` |
| `PERPLEXITY_API_KEY` | `perplexity_api_key` |
| `LM_STUDIO_API_KEY` | `lm_studio_api_key` |
| `NVIDIA_API_KEY` | `nvidia_api_key` |
| `HUGGINGFACE_API_KEY` / `HF_API_KEY` | `huggingface_api_key` |
| `CLOUDFLARE_API_TOKEN` | `cloudflare_api_token` |
| `KIMI_API_KEY` | `kimi_api_key` |
| `DIGITALOCEAN_API_KEY` | `digitalocean_api_key` |
| `STABILITY_API_KEY` | `stability_api_key` |
| `MUBERT_API_KEY` | `mubert_api_key` |
| `EXA_API_KEY` | `exa_api_key` |
| `CRAWL4AI_API_KEY` | `crawl4ai_api_key` |
| `REMOVEBG_API_KEY` | `removebg_api_key` |
| `GOOGLE_MAPS_API_KEY` | `google_maps_api_key` |
| `ITA_TARIFF_API_KEY` | `ita_tariff_api_key` |

Set them before starting Docker:

```bash
export OPENAI_API_KEY="sk-..."
export BRAVE_API_KEY="BSA..."
wsl docker compose up -d
```

**Guard rails:**
- Runs once per site (flag: `wp_mcp_ai_env_keys_checked`)
- Never overwrites existing manually-configured keys
- Stores in both `wp_mcp_ai_settings` array AND standalone `wp_mcp_ai_*` options
- Plaintext values are auto-migrated to AES-256-GCM encrypted on first read

Implementation: `includes/bootstrap/activation.php` →
`wp_mcp_ai_auto_detect_env_keys()`, called from `wp_mcp_ai_activate_single_site()`.

### 3. Fix Uploads Directory Warnings (v1.1.47+)

The plugin now uses `wp_mkdir_p()` (WordPress core, since WP 2.0) with
`is_dir()` guards before all `file_put_contents()` calls in:

- `includes/integrations/class-wp-mcp-ai-custom-tool-loader.php`
- `includes/paper-store/class-wp-mcp-ai-paper-store-manager.php`

If you still see warnings on older versions, pre-create the directories:

```bash
docker compose exec -T wordpress sh -c "
  mkdir -p /var/www/html/wp-content/uploads/wp-mcp-ai-custom-tools
  mkdir -p /var/www/html/wp-content/uploads/mcp-ai-wpoos/paper-store
  chown -R www-data:www-data /var/www/html/wp-content/uploads
"
```

### 4. WSL2 Docker Path Compatibility

The current `docker-compose.yml` uses relative paths (`.`) which Docker Desktop
translates automatically. No action needed. If you encounter path issues with
custom setups, use WSL paths (`/mnt/c/...`, `/mnt/f/...`) rather than Windows
drive letters (`C:/...`, `/F:/...`). See Docker Compose header comment for details.

### 5. Symlinks on WSL2 / Windows

**`ln -s` silently creates copies on NTFS drives.** When you run `ln -s` from
WSL targeting a path on a Windows-mounted drive (e.g. `/mnt/f/...`), it does
NOT error — but it creates a real directory copy instead of a symlink. You
need Windows Developer Mode enabled OR admin privileges for true symlinks.

**Workaround: use NTFS junctions.** Junctions are directory-only reparse points
that work without admin and are transparent to both Windows and WSL:

```powershell
# PowerShell (from WSL):
Remove-Item "F:\path\to\link" -Recurse -Force
New-Item -Path "F:\path\to\link" -ItemType Junction -Target "F:\path\to\target"
```

```bash
# Or via cmd.exe (no admin needed for junctions):
cmd.exe /c "mklink /J F:\path\to\link F:\path\to\target"
```

**Batch creation** is best done via a PowerShell `.ps1` script, not a shell
loop — each `cmd.exe /c` spawns a new process with the copyright banner.

**When to use which:**

| Type | Command | Admin | Scope |
|------|---------|-------|-------|
| Junction | `mklink /J` | No | Directories only, same volume |
| Symlink (file) | `mklink` | Usually | Files, cross-volume OK |
| Symlink (dir) | `mklink /D` | Yes | Directories, cross-volume OK |
| WSL symlink | `ln -s` | Dev Mode | Only on WSL-native filesystems |

> **Design Stack**: `.agents/skills/design-*` and `mcp-ai-wpoos-plugin` use
> junctions pointing to `plugins/mcp-ai-wpoos/.agents/skills/`. The creation
> script is at `bin/create-skill-junctions.ps1`.

---

## Creating an Assistant Programmatically

Assistants are WordPress custom post types (`mcp_ai_assistant`). Create one
via PHP in the container:

```php
<?php
define( 'WP_USE_THEMES', false );
require_once '/var/www/html/wp-load.php';

// 1. Create the assistant post
$post_id = wp_insert_post( array(
    'post_type'    => 'mcp_ai_assistant',
    'post_title'   => 'My Assistant',
    'post_content' => 'Description of what this assistant does',
    'post_status'  => 'publish',
), true );

if ( is_wp_error( $post_id ) ) {
    die( 'Failed to create assistant: ' . $post_id->get_error_message() );
}

// 2. Assign tools (required — otherwise tools/list returns [])
$tools = array(
    'search_content', 'web_search', 'create_post',
    'save_post', 'get_recent_posts', 'create_chart',
    'get_site_health', 'get_environment_status',
    // ... add more from the IGCSE list below
);
update_post_meta( $post_id, '_wp_mcp_ai_tools', $tools );

// 3. Generate a credential token
$result = WP_MCP_AI_Credentials::issue_credential( $post_id, 1 );
if ( is_wp_error( $result ) ) {
    die( 'Failed to issue credential: ' . $result->get_error_message() );
}
$token = $result['token'];  // format: cred_XXXXX.SECRET
echo "Assistant ID: $post_id\n";
echo "Token: $token\n";
```

**Key insight:** If `_wp_mcp_ai_tools` post meta is empty, the MCP `tools/list`
returns `[]` even though hundreds of tools are registered at the system level.
Always assign tools after creating an assistant.

### WP-CLI provisioning (preferred — verified end-to-end)

The PHP path above works, but the WP-CLI path is shorter and idempotent.
Verified on the Design Stack (2026-09):

```bash
# 0. In the Design Stack WP container, wp requires --allow-root.
#    (In this repo's own compose: docker compose run --rm wp-cli ...)

# 1. Discover valid tool slugs before assigning.
wp mcp-ai tool list               # base registry: slug + enabled + capability
wp mcp-ai toolkit list            # Pro toolkit settings keys

# 2. Create the assistant record.
wp mcp-ai assistant create --title="Brand Assistant" --status=publish --porcelain
# → prints the new assistant ID

# 3. Set runtime meta. NOTE: assistant create/update --model / --system-prompt
#    write legacy mcp_ai_model / mcp_ai_system_prompt keys that the runtime
#    does NOT read. The runtime reads _wp_mcp_ai_* — set those explicitly.
wp post meta update <id> _wp_mcp_ai_provider openai
wp post meta update <id> _wp_mcp_ai_model gpt-4o-mini
wp post meta update <id> _wp_mcp_ai_temperature 0.7
wp post meta update <id> _wp_mcp_ai_system_prompt "$(cat assistant-system-prompt.md)"
wp post meta update <id> _wp_mcp_ai_classification internal
wp post meta update <id> mcp_ai_required_capability manage_options
# Tools is a serialized PHP array; wp post meta update would store a string,
# so use wp eval for that one key:
wp eval 'update_post_meta(<id>, "_wp_mcp_ai_tools", array("web_search", "deep_research", "create_post"));'

# 4. Issue the credential (prints cred_xxxxx.SECRET exactly once).
wp mcp-ai credential issue <id> --porcelain

# 5. Smoke test (chat REST is the reliable verification path).
curl -s -X POST http://localhost:8092/wp-json/mcp-ai/v1/chat \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"assistant_id": <id>, "messages": [{"role":"user","content":"Reply with exactly: OK"}]}'
```

---

## MCP Token & Authentication

### Generating a Token

Tokens follow the format `cred_XXXXX.SECRET` (32-char secret, bcrypt hashed):

```php
$result = WP_MCP_AI_Credentials::issue_credential( $assistant_id, $user_id );
$token  = $result['token']; // Already includes "cred_" prefix
```

The `parse_token()` method validates the format:
- Must be a non-empty string
- Must contain a `.` separator (exactly 2 parts)
- First part must start with `cred_`
- Both parts must be non-empty

Default credential lifetime is 90 days (configurable via
`credential_lifetime_days` setting; 0 = no expiry).

### Using the Token

```bash
# JSON-RPC via curl
curl -s -X POST http://localhost:8000/wp-json/mcp-ai/v1/mcp \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer cred_xxxxx.SECRET" \
  -d '{"jsonrpc":"2.0","method":"tools/list","id":1}'

# MCP Bridge (stdio ↔ HTTP relay)
node bin/mcp-bridge.js
# Requires env: MCP_AI_BASE_URL + MCP_AI_TOKEN
```

### Auth Methods (in order of preference)

1. **Bearer token** (`cred_xxxxx.SECRET`) — recommended for MCP clients
2. **Raw credential** (`Authorization: cred_xxxxx.SECRET` without `Bearer `) —
   accepted since v1.1.55 for agent configs that forward the header verbatim
   (e.g. Cloudways Agent); disable via filter
   `wp_mcp_ai_accept_raw_credential_header`
3. **OAuth 2.0** (authorization_code grant) — browser-based MCP app flow
4. **Mesh Key** (`X-WP-MCP-AI-Mesh-Key` header) — mesh federation
5. **WordPress nonce** (`X-WP-Nonce` header + auth cookie) — browser admin

Application passwords (Basic auth) are not supported on the MCP endpoint.
Use Bearer tokens instead.

---

## MCP JSON-RPC Protocol

The endpoint is at `/wp-json/mcp-ai/v1/mcp`. Standard JSON-RPC 2.0.

### Initialize

```json
{
  "jsonrpc": "2.0",
  "method": "initialize",
  "params": {
    "protocolVersion": "2024-11-05",
    "capabilities": {},
    "clientInfo": {"name": "my-client", "version": "1.0"}
  },
  "id": 1
}
```

Response includes `serverInfo.name` (the assistant title) and server
`capabilities` (tools, resources, etc.).

### List Tools

```json
{"jsonrpc": "2.0", "method": "tools/list", "id": 1}
```

Returns only tools assigned to the authenticated assistant via
`_wp_mcp_ai_tools` post meta. Each tool includes `name`, `description`,
and `inputSchema` (JSON Schema).

### Call a Tool

```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "tool_slug",
    "arguments": {"param1": "value1"}
  },
  "id": 1
}
```

Response is in `result.content[0].text` as a JSON string. Canonical envelope:
success returns an array; errors return a `WP_Error` object serialized as
`{"code":"...", "message":"...", "data":{...}}`.

### HTTP status semantics (v1.1.55+)

JSON-RPC **error envelopes are returned with HTTP 200** so client SDKs that
drop non-2xx bodies (e.g. the TypeScript SDK bundled with `mcp-remote`)
still relay errors to the agent. Pre-1.1.55, errors were returned as
400/404/500 and such SDKs **silently discarded them** — tool calls appeared
to return nothing. Auth failures (401/403) and pre-dispatch guards (429)
keep their HTTP statuses. Revert via filter `wp_mcp_ai_mcp_error_http_status`.
Since v1.1.90 the opt-in `mcp_require_assistant_scope` setting adds one more
403: `tools/list`/`tools/call` fail closed (`wp_mcp_ai_assistant_scope_required`)
when no assistant resolves — see Troubleshooting.

---

## Testing Tools Through the Chat REST Endpoint (no MCP client needed)

The chat UI executes tools through `POST /wp-json/mcp-ai/v1/tools` — the
fastest way to verify a tool end-to-end with `curl` instead of spinning up
an MCP client or a chat session.

```json
{
  "assistant_id": 9,
  "tool": "search_upwork_jobs",
  "arguments": { "query": "wordpress developer", "limit": 5 }
}
```

- **Auth:** `X-WP-Nonce` + the logged-in cookie (same origin), or a Bearer
  credential. The nonce must be **bound to a real session** — generate one
  from a probe script, not from a bare CLI `wp_create_nonce()`:

  ```php
  $expiration = time() + 3600;
  $token = WP_Session_Tokens::get_instance( $uid )->create( $expiration );
  $cookie = wp_generate_auth_cookie( $uid, $expiration, 'logged_in', $token );
  $_COOKIE[ LOGGED_IN_COOKIE ] = $cookie;          // nonce binds to this session
  wp_set_current_user( $uid );
  $nonce = wp_create_nonce( 'wp_rest' );           // use with curl -H "X-WP-Nonce: ..."
  ```

- **Gate 1 — assistant allowlist:** every assistant scopes tool access via
  the `_wp_mcp_ai_tools` post meta. A tool not in that list returns
  `403 wp_mcp_ai_tool_forbidden` ("This assistant is not allowed to execute
  the requested tool"). Grant access with
  `update_post_meta( $assistant_id, '_wp_mcp_ai_tools', $tools_with_slug )`.
- **Gate 2 — availability:** `search_upwork_jobs` (and the other Upwork CRM
  tools) also need `enable_crm_toolkit` in `wp_mcp_ai_settings`.
- **DuckDuckGo returns no real SERPs.** The default `web_search_provider`
  (`duckduckgo`) hits the free Instant Answer API, which returns empty
  `RelatedTopics` for ordinary queries — so fallback-mode tools that
  depend on `web_search` (`search_upwork_jobs` without an Upwork
  connection, `research_company`, etc.) come back with **0 results** even
  though outbound internet works. Configure a Brave (`BRAVE_API_KEY` env)
  or Tavily key and set `web_search_provider` to it — Brave also supplies
  `published_date`, which the Upwork fallback maps onto `published`.
- **MSYS path gotcha:** `docker exec <ctr> php /tmp/probe.php` mangles
  `/tmp/...` into a Windows path unless prefixed with `MSYS_NO_PATHCONV=1`.
  CLI `php` inside the WP container also defaults to 128M — use
  `php -d memory_limit=512M` when bootstrapping WordPress with Elementor.

---

## MCP Transports & Client Compatibility

The `/wp-json/mcp-ai/v1/mcp` endpoint supports **two transports**, chosen by
the request shape:

| Transport | How it connects | Response channel |
|-----------|-----------------|------------------|
| **Streamable HTTP** (default) | `POST /mcp` JSON-RPC, `Accept` includes `application/json` | JSON body on the POST response, HTTP 200/202 |
| **Legacy HTTP+SSE** (v1.1.55+, flag `WP_MCP_AI_LEGACY_SSE_ENABLED`) | `GET /mcp` with SSE-only `Accept: text/event-stream` (or `?stream=true`) → `event: endpoint` with `session_id`; then `POST /mcp?session_id=...` | POST returns 202; responses arrive on the GET stream as `event: message` frames |

**Discriminator rule:** `Accept` containing `text/event-stream` **and not**
`application/json` → legacy SSE handshake. Mixed `Accept` headers
(`application/json, text/event-stream`) always get JSON — that is deliberate,
because Zed, Cursor, LM Studio and mcp-remote all send the mixed header but
expect JSON responses.

**Session model (legacy SSE):** sessions are owned by the credential that
opened them (SHA-256 hash of the `Authorization` header); message POSTs with
a different credential get 404. Caps: 5 sessions/credential, 20 global,
30-min TTL (`wp_mcp_ai_sse_session_ttl` / `wp_mcp_ai_sse_max_per_credential` /
`wp_mcp_ai_sse_max_total`). Store: `WP_MCP_AI_SSE_Session_Store`
(`includes/rest/class-wp-mcp-ai-sse-session-store.php`).

**`GET /sse` is NOT a message channel** — it streams the assistant directory
(`event: directory`). Legacy SSE clients cannot complete a session there.
`GET /no-sse` returns the directory as JSON.

### Client compatibility quick reference

| Client | What works |
|--------|-----------|
| Zed / Cursor / LM Studio / new SDKs | Native Streamable HTTP (`url` = `/mcp`) |
| Python MCP SDK | `streamable_http_client(url, headers=...)` works; `sse_client(url)` **requires v1.1.55+** for the handshake |
| mcp-remote bridge (Claude Desktop, older agents) | `npx -y mcp-remote@latest <url> --header "Authorization: Bearer <token>"` — connects via Streamable HTTP, needs Node 24+ |
| Cloudways Agent 0.19.0 / Codex-style agents | A bare `url:` is treated as **SSE transport** — use the mcp-remote stdio bridge, or point at the `/mcp` endpoint on v1.1.55+ |

### mcp-remote stdio bridge pattern (verified)

For agents whose MCP client only speaks legacy SSE over a configured URL
(Cloudways Agent, Claude Desktop):

```yaml
mcp_servers:
  nv-oos-sophie-agent:
    command: npx
    args:
      - "-y"
      - "mcp-remote@latest"
      - "https://<site>/wp-json/mcp-ai/v1/mcp"
      - "--header"
      - "Authorization: Bearer cred_xxxxx.SECRET"
    enabled: true
```

mcp-remote auto-detects the transport (`http-first` strategy) and exposes the
remote tools over local stdio. **Note:** mcp-remote opens a GET SSE stream
for server-initiated messages and retries it on failure — on pre-1.1.55
servers that GET hits the request rate limiter, and the retry loop can burn
the whole hourly quota (see Rate Limiting below).

### SSH-only sites — `bin/mcp-bridge-ssh.js` (Zed stdio over SSH)

For sites with **no public web route** (SSH is the only way in), use the
repo's own bridge, which owns the SSH port-forward and delegates to
`bin/mcp-bridge.js` (newline-delimited stdio ↔ Streamable HTTP relay). No
manual tunnel, no mcp-remote, no npm dependencies — Zed spawns it as a stdio
context server.

**Prerequisite:** SSH key auth (`ssh <user>@<host> -p <port>` must succeed
non-interactively). Password prompts are impossible for a spawned process
with no TTY.

Zed `context_servers` entry (Settings → AI → MCP Servers → Add Local Server):

```json
{
  "command": "node",
  "args": ["bin/mcp-bridge-ssh.js"],
  "env": {
    "MCP_AI_SSH_USER": "user",
    "MCP_AI_SSH_HOST": "203.0.113.10",
    "MCP_AI_SSH_PORT": "2222",
    "MCP_AI_SSH_REMOTE_PORT": "80",
    "MCP_AI_TOKEN": "op_xxxx.SECRET"
  }
}
```

Key env vars: `MCP_AI_SSH_REMOTE_HOST`/`MCP_AI_SSH_REMOTE_PORT` (web server
from the server's perspective; probe with curl over SSH — Cloudways Apache
may sit on 8080), `MCP_AI_HOST_HEADER` (canonical host override when the
web server 301-redirects on Host), `MCP_AI_SSH_EXTRA_ARGS` (e.g.
`"-i C:/keys/id_ed25519 -o ProxyJump=bastion"`), `MCP_AI_ENV_FILE` (default
`~/.nvoos-bridge.env` — keep the token out of settings.json).

Operator-credential audience binding is checked against `home_url()` from
the database, not the request Host header, so `http://127.0.0.1:<port>`
requests through the tunnel validate normally.

Orphan-proofing: the bridge holds ssh's stdin open so a hard-killed bridge
closes the pipe and ssh exits — no stray tunnels. Tests:
`node bin/test-mcp-bridge-ssh.js`.

For driving a **Hermes Agent** (Nous Research) itself rather than the NV oOS
console — its WebUI API over public HTTPS — see `bin/hermes-mcp-server.js`
(tools: `hermes_chat`, `hermes_list_sessions`, `hermes_session_detail`,
`hermes_sync_skills`; runbook: `docs/operations/fleet/hermes-operator-setup.md`
§7). The server also auto-syncs `.agents/skills/` to the agent on startup
(`HERMES_SYNC_SKILLS_ON_START=1`, default); the standalone CLI
`bin/sync-skills-to-hermes.js` does the same from cron or a git post-merge hook.

---

## Rate Limiting & Agent Traffic

Two independent limiters apply to MCP traffic:

1. **General request limiter** — `rate_limit_requests` per
   `rate_limit_window` seconds per user/IP (oOS → Security → Network & Headers).
   GET/HEAD requests are exempt since v1.1.55 (discovery/SSE probes must not
   consume the budget aimed at state-changing traffic).
   **For AI-agent workloads set `rate_limit_requests` to 1000** — the default
   300 is for chat usage, and client retry loops burn requests fast.
2. **Tool execution limiter** — v1.1.55+ settings under oOS → Security →
   **Tool Rate Limiting**: `tool_rate_limit_max` (default 300, 0 = unlimited),
   `tool_rate_limit_window` (default 60s), `tool_rate_limit_exempt_tokens`
   (default **on** — credential-token/agent traffic is exempt because an
   assistant credential is already an explicit grant of its tool set).
   Pre-1.1.55 this was a hardcoded 60 calls/60s with no UI — agents burst
   through it routinely.
3. **Nefarious usage monitor** — a third counter, deliberately namespaced
   (`wp_mcp_ai_nefarious_rate_limit_` transient) away from the chat REST
   limiter (`wp_mcp_ai_rate_limit_`): a shared counter would halve the
   configured chat budget and entangle the two enforcement paths.
   Rate-limit classification uses the dispatching request's real HTTP verb
   (internal dispatches like `rest_do_request`/WP-CLI are classified
   correctly instead of by the ambient request); GET/HEAD stay exempt.
   Custom emitters of `wp_mcp_ai_before_chat_request` may fire the legacy
   2-arg `( $messages, $request_data )` shape — core subscribers tolerate
   both it and the canonical
   `( $assistant_id, $messages, $options, $request )`.

**Symptom of a tripped tool limiter on pre-1.1.55 servers:** tools/call
returns HTTP 500 with a `-32603 "Tool rate limit exceeded"` error body —
which mcp-remote-style SDKs silently drop, so the agent sees no response
at all. With v1.1.55+ the same condition returns a visible JSON-RPC error
(and is unlikely to trip for agent tokens).

---

## Restricted Users & Chat Rate Limits (v1.1.60+)

The plugin converts ephemeral rate-limit and token-budget blocks into
**persistent restriction records** (`WP_MCP_AI_Restriction_Registry`) so
admins can review, lift, or add them.

- **Chat rate limit** — the hardcoded 60 req/min chat cap is now filterable:
  `wp_mcp_ai_chat_rate_limit` and `wp_mcp_ai_chat_rate_limit_window`
  (WordPress bridge → `ChatOrchestrator::setChatRateLimit()`).
- **Enforcement hooks** — `wp_mcp_ai_tool_token_limit_exceeded`,
  `wp_mcp_ai_per_session_limit_exceeded`, and the new
  `wp_mcp_ai_rate_limit_exceeded` (fired by the OOS `RateLimiter` adapter)
  feed the registry; records auto-expire on a daily cleanup cron and are
  audit-logged.
- **Admin surfaces** — Token Manager "Restricted Users" panel (Base) with
  one-click lift; Pro Command Center **Restrictions** tab (KPI cards, live
  table, lift actions); dismissible notices toggled from Settings →
  Orchestration → Restriction Notifications (`enable_restriction_admin_notices`).
- **WP-CLI** — `wp mcp-ai restrictions list|lift|add`.
- **REST** — `GET /mcp-ai/v1/restrictions`,
  `GET|POST /mcp-ai/v1/users/{id}/restrictions`,
  `DELETE /mcp-ai/v1/users/{id}/restrictions/{type}`; rate-limited responses
  carry IETF headers (`RateLimit-Policy`, `RateLimit`, `Retry-After`).
- Full reference: `docs/features/security/user-restrictions.md`.

## Conversation Import (v1.1.60+, JetEngine)

Import external AI conversation exports into the JetEngine
`ai_chat_transcripts` CCT (one row per conversation):

- **Formats** — ChatGPT `conversations.json` (incl. ZIP), Google Takeout
  Gemini activity, Claude `conversations.jsonl`, ShareGPT, OpenAI
  fine-tuning JSONL.
- **Tools** — `conversation_import_detect|run|status|delete` (require
  `manage_options`; JetEngine must be active).
- **WP-CLI** — `wp mcp-ai conversation-import detect|import|status|delete`
  (`--dry-run`, `--policy=skip|refresh`, `--resume-token=`).
- **Admin** — upload/preview page with progress reporting; GDPR
  export/erase + retention coverage; optional memory mining via
  `mine_agent_memory`. Guide: `docs/user-guides/conversation-import.md`.

## Agent Identity Bridging & OKF Bundle (v1.1.61+)

- **Agent identity bridging** — `store_agent_context` resolves virtual agent
  keys (e.g. `nvoos-pro-spa-memory-drawer`) to the canonical assistant post
  ID (`WP_MCP_AI_Agent_Identity_Resolver`, alias map in the
  `wp_mcp_ai_agent_id_aliases` option); the envelope echoes
  `original_agent_id` / `agent_id_resolved`. Chat-memory recall merges alias
  buckets (`stored_under` per record) and the memory drawers show
  scope/stored-under chips, the agent ID, and a show-all-scopes toggle.
**OKF bundle.** The `skill-knowledge` bundle is auto-generated from
  bundled skills on bootstrap (and after bundled-skill reinstall), so
  `okf_search` works out of the box (no more "OKF bundle not found").

## OKF Bundle Management & Pro Knowledge Routing (v1.1.62+)

- **Bundle Manager (Base)** — `WP_MCP_AI_OKF_Bundle_Manager` owns the OKF
  bundle lifecycle: create/list/rename/archive/delete, ZipSlip-safe ZIP
  import/export, health stats, log maintenance; `skill-knowledge` is
  protected from tool writes (`okf_protected_bundle` — curated knowledge
  belongs in `site-knowledge`). Admin screen under Assistants:
  `edit.php?post_type=mcp_ai_assistant&page=wp-mcp-ai-okf-bundle-manager`
  (Bundles/Browser/Editor/Import-Export/Validate; `manage_options`).
- **Tools** — three new base tools (`okf_list_bundles`, `okf_validate_bundle`,
  `okf_import_bundle`) plus the `okf_write_concept` provenance schema
  (`resource`/`sources`/`usage_window`/`verified`) — OKF tool surface: 10.
  Two new Pro tools: `okf_enrich_site_content` (`manage_options`) and
  `route_knowledge_query` (`read`).
- **Pro knowledge routing** — `load_skill` resolves `bundle:concept_id`
  names (OKF-to-Skill Bridge, per-assistant grants + trust gating); the
  enrichment agent crawls site content into OKF concepts; the hybrid
  knowledge router classifies queries across OKF / vector / Paper stores.
- **Pro SPA v2 drawer** — in-chat OKF Skills Drawer backed by the read-only
  `mcp-ai-pro/v1/okf` REST surface (bundles, concept browse/search,
  assistant skill grants); `%2F`-encoded concept IDs decode correctly.
- **Vector stores** — all vector-store tools now run on the Responses API
  (no `OpenAI-Beta: assistants=v2` header; `file_batches` ingestion with
  bounded polling + fallback) ahead of the 2026-08-26 Assistants API
  removal.
- Guide: `docs/features/okf-integration.md`; roadmap:
  `docs/project/plans/OKF-BUNDLE-MANAGEMENT-IMPLEMENTATION-PLAN.md`.

---

## Artifact Evolution, Addons Page & Storage Worker (v1.1.63+)

- **Artifact evolution Phases A–G (Base + Pro)** — the Continual Harness
  Evolver + Meta-Harness are now a gated Darwinian self-improvement loop for
  skills, prompts, and roles (`includes/harness/class-wp-mcp-ai-artifact-*.php`):
  populations + parent sampling, failure replay + post-mutation verification,
  pre-commit admission gate, holdout-gated deployment with shadow A/B + drift
  rollback, governor + human approval queue + lineage. **Every layer defaults
  off**; the opt-in switches live in Settings → Orchestration Layer
  (`WP_MCP_AI_Evolution_Settings_Bridge`). The `evolve_harness` tool now calls
  the repaired Evolver contract (`analyze_failures()`, component-scoped
  `evolve()`, enforced `dry_run`). Proposal:
  `docs/project/proposals/007-artifact-evolution.md`.
- **Pro Addons page (v1.1.63+)** — NV oOS Pro Dashboard → Addons
  (`/wp-admin/admin.php?page=wp-mcp-ai-addons`) installs/activates standalone
  addons whose ZIPs ship in `build/`; nonce + `install_plugins` + allowlist;
  non-WordPress components listed read-only.
- **Chat storage worker offload** — saves ≥ `wp_mcp_ai_storage_worker_threshold`
  (default 10,000 chars) offload `JSON.stringify` to the browser
  `storage-worker.js`; sync fallback for small saves/unload/worker failure;
  kill switch: `add_filter( 'wp_mcp_ai_storage_worker_threshold',
  '__return_zero' );`. Plan:
  `docs/project/proposals/032-chat-web-workers-wiring-implementation-plan.md`.
- **DeepSeek empty-schema fix** — tool schema `properties` must encode as `{}`
  never `[]`; legacy tools are wrapped before the first register attempt.

## Reasoning Models, Full-Crawl Proxy & Security-Posture Closure (v1.1.65+)

- **OpenAI reasoning-model parameters** — o-series and gpt-5 models reject
  `max_tokens` (o-series also `temperature`); `lib/core`
  `OpenAiCompatibleClient` strips unsupported parameters per model
  (`applyModelConstraints()`) and retries 400 rejections with corrected
  payloads (`sendWithParameterCorrection()`) on sync and streaming paths.
  Do not blanket-add `max_tokens` for reasoning models.
- **Media Worker full-Crawl4AI proxy (031 Phase 3)** — env-gated
  `POST /api/crawl/full` + `GET /api/crawl/full/task/:id` forward to
  `CRAWL4AI_FULL_URL` with SSRF-validated targets, token gating, and
  503/502/400 envelopes; `TEMP_ROOT` is the strict-path sandbox root
  (028 Q5). Worker version stays **v3.2.0** — `package.json` is
  authoritative.
- **Security-posture closure (issue #5972)** — Algorave Tone.js raw eval
  requires per-session confirmation + warning banner; TMA source map
  removed; webhook `__return_true` callbacks carry justification comments.
- **Chat/REST hardening** — legacy top-level `attachments` parameters
  tolerated; custom message roles work via
  `wp_mcp_ai_allowed_message_roles`; orphaned tool messages silently
  discarded; sign-preserving transcript pagination; legacy `input_text`
  segments normalized to `text`.
- **TPM fallback** — token-budget service falls back to the bundled model
  catalog when the rate-limits CCT has no entry (TPM limits work without
  JetEngine).
- **Slash commands & blocks** — toolkit manager re-resolves the handler on
  registration; CSV list args accept `"1,2"` and `"1, 2"`;
  assistant-builder and Pro toolkit blocks register idempotently
  (WP 7.1 notices).

## Release Notes (per version)

Historical per-version release notes (v1.1.66 through v1.1.91) moved to
[RELEASE-NOTES.md](RELEASE-NOTES.md) to keep SKILL.md under the Zed 100KB
skill-size limit. Append new version sections there, not here.

---

## Plugin Internals Reference

### Key Classes

| Class | File | Purpose |
|-------|------|---------|
| `WP_MCP_AI_Tool_Registry` | `includes/class-wp-mcp-ai-tool-registry.php` | Singleton, `get_instance()->get_tools()` |
| `WP_MCP_AI_Credentials` | `includes/class-wp-mcp-ai-credentials.php` | Token issue/validate/revoke (`issue_credential()`, `validate_token()`, `parse_token()`) |
| `WP_MCP_AI_Admin_Settings_Base` | `includes/admin/class-wp-mcp-ai-admin-settings-base.php` | Settings defaults, sensitive field list, `OPTION_NAME = 'wp_mcp_ai_settings'` |
| `WP_MCP_AI_Api_Key_Store` | `includes/security/class-wp-mcp-ai-api-key-store.php` | Encrypted API key storage (AES-256-GCM), transparent plaintext migration |
| `WP_MCP_AI_REST` | `includes/class-wp-mcp-ai-rest.php` | MCP endpoint permission checks, auth methods |

### Key Options

| Option | Content |
|--------|---------|
| `wp_mcp_ai_settings` | All settings including provider API keys, model choices, feature toggles |
| `wp_mcp_ai_credentials` | Credential index (maps `cred_XXXXX` → assistant ID) |
| `wp_mcp_ai_env_keys_checked` | Flag: env var auto-detection has run (prevents re-scan) |
| `wp_mcp_ai_activated_version` | Last activated plugin version (skip heavy re-activation work) |

### Key Post Types

| Post Type | Purpose |
|-----------|---------|
| `mcp_ai_assistant` | AI assistants (meta: `_wp_mcp_ai_tools`, `_wp_mcp_ai_credentials`) |
| `mcp_ai_profession` | Profession templates for creating assistants via admin UI |

### Key Post Meta

| Meta Key | Type | Purpose |
|----------|------|---------|
| `_wp_mcp_ai_tools` | `array` of strings | Tool slugs assigned to the assistant |
| `_wp_mcp_ai_credentials` | `array` of credential records | Issued tokens (hashed) with creation/expiry metadata |
| `_wp_mcp_ai_provider` | `string` | Provider slug (`openai`, `gemini`, `anthropic`, `deepseek`, `ollama`, …) |
| `_wp_mcp_ai_model` | `string` | Model identifier (`gpt-4o-mini`, `gemini-2.5-flash`, …) |
| `_wp_mcp_ai_system_prompt` | `string` | Assistant persona / system prompt |
| `_wp_mcp_ai_temperature` | `float` | Sampling temperature |
| `_wp_mcp_ai_classification` | `string` | Information label; defaults to `internal` |
| `mcp_ai_required_capability` | `string` | Capability gate for tool calls — **no `_wp_` prefix** (`manage_options`, `edit_posts`) |
| `_wp_mcp_ai_vector_store_id` | `string` | OpenAI vector store for RAG |
| `_wp_mcp_ai_memory_files` | `array` | Memory file attachment IDs |
| `_wp_mcp_ai_harness_profile` | `array` (JSON) | Agent-harness profile (memory summary etc.) |

### Toolkit Categories (12 Built-In)

`content_publishing`, `media_processing`, `data_analytics`,
`ecommerce_business`, `developer_technical`, `security_compliance`,
`research_discovery`, `geospatial_location`, `workflow_automation`,
`communication_outreach`, `integration_external`, `ai_model_management`

Additional Pro toolkits are addons under `addons/pro/`.

### Files Changed by Plugin Fix Plan (Aug 2026)

| File | Fix |
|------|-----|
| `docker-compose.yml` | WSL2 comment (relative paths already correct) |
| `includes/integrations/class-wp-mcp-ai-custom-tool-loader.php` | `wp_mkdir_p()` + `is_dir()` guards before writes |
| `includes/paper-store/class-wp-mcp-ai-paper-store-manager.php` | `mkdir()` → `wp_mkdir_p()`, guards before writes |
| `includes/bootstrap/activation.php` | `wp_mcp_ai_auto_detect_env_keys()` + activation hook |

### Integration contracts (updated Aug 2026)

Notable filter/API contract changes from the recent test-suite repair
clusters — relevant when writing integrations against these seams:

| Seam | Contract |
|------|----------|
| `wp_mcp_ai_vendor_package_paths` | Filter on the NPM vendor package-path map in `wp_mcp_ai_check_vendor_packages()`; lets integrations remap/inject package locations (PR #6097) |
| `wp_mcp_ai_chat_transcript_handler` | Now invoked with **7 args** (`$handler, $assistant_id, $messages, $options, $response, $request, $context`) by `WP_MCP_AI_Chat_Transcript_Recorder::resolve_handler()` |
| Chat message `content` shape | The REST validator stores message content as **segments**: `array( array( 'type' => 'text', 'text' => '…' ) )` — affects `/chat-transcripts` payloads and `extract_request_messages()` consumers |
| `WP_MCP_AI_Profession_CPT::sanitize_memory_files()` | Negative IDs now **clamp to 0 and are dropped** (previously `absint()` coerced e.g. `-999` → `999`) — PR #6105 |
| Graphify `on_plugins_loaded` | Admin classes (`NV_oOS_Graphify_Settings`, `NV_oOS_Graphify_Remote_Admin`) are now required defensively before `init()` when `is_admin()` — PR #6106 |

## Development & Test Suite

For the PHPUnit repair workflow — Docker test commands (WP 6.9 + 7.1),
CI log triage, the recurring root-cause patterns, and the cluster-by-cluster
PR conventions — see the dedicated skill
[`mcp-ai-wpoos-test-suite`](../mcp-ai-wpoos-test-suite/SKILL.md) and
`.context/testing.md` for test-writing patterns and the coverage policy.

---

## Troubleshooting

### "invalid volume specification" on Docker start

**Cause:** Windows drive-letter path in a custom compose override
(`F:/GITHUB/...`).
**Fix:** Use WSL path (`/mnt/f/GITHUB/...`). The default `docker-compose.yml`
already uses relative paths (`.`), so this only affects custom setups.

### PHP warnings about file_put_contents / mkdir on startup

**Cause (v1.1.46 and earlier):** Plugin tried to write to `uploads/` subdirs
before they existed.
**Fix:** Upgrade to v1.1.47+ (Fix 2 applied). Quick workaround for older versions:
```bash
docker compose exec -T wordpress mkdir -p /var/www/html/wp-content/uploads/wp-mcp-ai-custom-tools
```

### tools/list returns []

**Cause:** Assistant has no tools assigned in `_wp_mcp_ai_tools` post meta.
**Fix:** Assign tools:
```php
update_post_meta( $assistant_id, '_wp_mcp_ai_tools', array( 'web_search', 'create_post', /* ... */ ) );
```

### tools/list or tools/call returns HTTP 403 (`wp_mcp_ai_assistant_scope_required`)

**Cause (v1.1.90+):** opt-in `mcp_require_assistant_scope` (Security → Access & Identity, default OFF) is on and the request resolves to no assistant (no explicit `assistant_id`, no token-bound assistant, no `default_assistant`).
**Fix:** pass `assistant_id`, bind the credential to an assistant, set `default_assistant`, or turn the toggle off.

### MCP App OAuth connect fails with "OAuth 2.0 discovery failed" (v1.1.91+)

**Cause:** the older client only probed the bare `/.well-known/oauth-authorization-server` URL, so path-scoped or RFC 9728-style OAuth servers looked unsupported even when they fully implement OAuth.
**Fix (v1.1.91+):** `discover_metadata()` walks the full chain — RFC 8414 metadata (+ §3.2 path insertion), RFC 9728 protected-resource metadata (every advertised `authorization_servers` entry), the 401 `WWW-Authenticate` probe, OIDC `.well-known/openid-configuration`, then the WordPress REST fallback. The metabox failure alert now shows every attempt (URL → HTTP status / transport error) and the real cURL/DNS/TLS error instead of the generic message — read the `attempts` + `hint` in the alert before assuming the server has no OAuth.

### Provider Connect buttons bounce to the wp-admin dashboard (OAuth redirects)

**Cause:** `wp_safe_redirect()` rejects off-site consent-page hosts missing from the `allowed_redirect_hosts` allowlist and silently falls back to `admin_url()` — the connect click lands on the dashboard instead of the provider's consent page.
**Fix (v1.1.91+):** LinkedIn (`www.linkedin.com`), QuickBooks (`appcenter.intuit.com`), Mailjet (`app.mailjet.com`), and Yahoo Sports (`api.login.yahoo.com`) are now allowlisted via per-provider filters deriving the host from the authorize-endpoint filter. When wiring a **new** OAuth flow, register its consent host the same way — the GitHub/Meta pattern in `includes/integrations/` is the template.

### "No AI providers configured" / tools return errors

**Cause:** No API key for the provider, or the provider's enable flag is off.
**Fix:** Set environment variables before starting Docker (Fix 3 auto-detects
them), or set keys via WordPress admin → oOS → Providers tab.

Since the provider-defaults fix (PR #6255), fresh installs keep **all** cloud
providers disabled by default: after adding an API key, also check the
"Enable … Provider" checkbox on Settings → NV oOS → AI Providers (each
provider's subtab), or enter the key via the onboarding wizard, which
auto-enables the provider whose key you provide. Provider dropdowns elsewhere
in admin only list providers that are both **enabled** and **credentialed**
(`WP_MCP_AI_Model_Config::get_available_providers()`), so an enabled-but-keyless
or keyed-but-disabled provider is invisible in dropdowns.

### semantic_content_search returns "No OpenAI API key has been configured"

**Cause (pre-1.2.0):** the tool picked the embedding backend from the
assistant's chat provider and hard-failed on OpenAI. Since v1.2.0 embeddings
are resolved independently of the chat provider — configure **any** embedding
backend:

| Backend | Setting |
|---|---|
| OpenAI | `openai_api_key` |
| Gemini | `gemini_api_key` |
| Ollama (local) | `ollama_endpoint_url` |
| DigitalOcean | `digitalocean_api_key` |

Pin a specific backend with `embedding_provider` (`openai`, `gemini`,
`ollama`, or `digitalocean`). With no backend configured, the tool falls back
to keyword search (`fallback_mode: "keyword"`) instead of failing.

### Credential token invalid (401)

**Cause:** Token malformed, expired, or revoked.
**Check:** Token format must be `cred_XXXXX.SECRET`. Verify with:
```php
$parsed = WP_MCP_AI_Credentials::parse_token( $token );    // null = invalid format
$result = WP_MCP_AI_Credentials::validate_token( $token ); // WP_Error = invalid/expired
```

### web_search uses DuckDuckGo instead of Brave

**Cause:** `web_search_provider` not set to `brave` AND Brave API key not configured.
**Fix:** Ensure `brave_search_api_key` is set (via env var `BRAVE_API_KEY` or admin UI),
then set provider:
```php
$settings = get_option( 'wp_mcp_ai_settings', array() );
$settings['web_search_provider'] = 'brave';
update_option( 'wp_mcp_ai_settings', $settings );
```

### Env var API keys not detected after activation

**Cause:** Plugin was activated before Fix 3 was applied, or the flag
`wp_mcp_ai_env_keys_checked` is already set.
**Fix:** Reset the flag and re-trigger detection:
```php
delete_option( 'wp_mcp_ai_env_keys_checked' );
wp_mcp_ai_auto_detect_env_keys();
```
Or set keys manually via admin UI → oOS → Providers.

### Agent logs "unhandled errors in a TaskGroup (1 sub-exception)" / tools never load

**Cause:** the client is using the legacy SSE transport against `/mcp`, but
the server answers JSON (`SSEError: Expected response with content type
'text/event-stream', got 'application/json'`).
**Fix:** switch the client to Streamable HTTP, use the mcp-remote stdio
bridge (see Transports section), or upgrade the server to v1.1.55+ where
GET `/mcp` with an SSE-only Accept serves a real SSE handshake.

### Tool call responses never come back (agent hangs on tools)

**Cause (pre-v1.1.55):** tool errors are returned as HTTP 400/404/500 with a
JSON-RPC error body; SDKs like the one in mcp-remote **silently drop
non-2xx responses**, so the pending request never resolves. This includes
rate-limit hits and every tool `WP_Error`.
**Fix:** upgrade to v1.1.55+ (errors return HTTP 200 with the JSON-RPC
envelope), or reduce tool-call frequency to avoid the 60/min tool limit.

### Constant "429 ... Failed to open SSE stream: Too Many Requests" from mcp-remote

**Cause:** mcp-remote's GET SSE-stream retry loop consumes the general
`rate_limit_requests` bucket (per user/IP). Each retry counts.
**Fix:** raise `rate_limit_requests` (1000 for agent sites) and upgrade to
v1.1.55+ (GETs exempt from the quota, real SSE stream stops the retry loop).

### `remote_wp_connection` / `ezuite_erp` calls hang, then return 0 bytes

**Cause:** these network-dependent tools route through the async job queue;
`mcp_wait_for_async_tool()` could poll up to 6 minutes (120 polls × 3s),
longer than Cloudflare's ~100s cutoff (524) — the request dies mid-wait.
**Fix:** v1.1.55+ bounds the wait to ~45s (filter `wp_mcp_ai_async_max_polls`,
default 15) and kicks stuck jobs inline (`kick_inline_if_stale`) so hosts
with a dead WP-Cron loopback self-heal; timeouts now surface as visible
errors instead of resets.

### Cloudflare blocks non-browser clients (error 1010) or 524 timeouts

**Cause:** Cloudflare WAF blocks default non-browser user agents (e.g.
Python `urllib`); long synchronous tool calls exceed the ~100s proxy cutoff.
**Fix:** use curl/browser-like user agents for probes, and prefer v1.1.55+
where long tools are bounded or delivered out-of-band (SSE message queue).

### `wp mcp-ai provider list` / `wp mcp-ai chat` fatal (PHP 8, fixed in #6625)

Both commands fataled with a PHP 8 error on builds before the CLI fix:
`provider list` goes through `WP_MCP_AI_CLI_Base_Command::format_output()`,
which passed an inline array literal to `WP_CLI\Formatter`'s by-reference
constructor (a fatal on every command using the base class), and `chat`
constructed the language model router with zero arguments. **Fixed in #6625**
(merged to alpha-working; ships after v1.1.79). On older builds:

- Provider config status → NV oOS settings page; connectivity →
  `wp mcp-ai provider test <slug>`.
- Chat → the REST smoke test instead:
  `POST /wp-json/mcp-ai/v1/chat` with `assistant_id` + `messages`
  (see the provisioning recipe above).

### `wp mcp-ai assistant create --model=…` has no runtime effect

`assistant create|update --model` / `--system-prompt` write legacy
`mcp_ai_model` / `mcp_ai_system_prompt` meta keys, while the chat runtime
reads `_wp_mcp_ai_model` / `_wp_mcp_ai_system_prompt` — the flags are
currently cosmetic. Set the `_wp_mcp_ai_*` keys via `wp post meta update`
(or `wp eval` for the tools array) after creation. `assistant list|get`
read the legacy keys too, so treat their model column as unreliable.

---

## References

- Plugin repo: `https://github.com/nvdigitalsolutions/mcp-ai-wpoos`
- WordPress admin (Docker): `http://localhost:8000/wp-admin` (admin / password)
- MCP endpoint: `http://localhost:8000/wp-json/mcp-ai/v1/mcp`
- Status endpoint (public): `http://localhost:8000/wp-json/mcp-ai/v1/status`
- Settings option: `wp_mcp_ai_settings`
- Activation logic: `includes/bootstrap/activation.php`
- Credentials: `includes/class-wp-mcp-ai-credentials.php`
- API key store: `includes/security/class-wp-mcp-ai-api-key-store.php`
- MCP controller (transports, SSE handshake): `includes/rest/class-wp-mcp-ai-rest-mcp-controller.php`
- Legacy SSE session store: `includes/rest/class-wp-mcp-ai-sse-session-store.php`
- JSON-RPC dispatch & error mapping: `includes/class-wp-mcp-ai-rest-mcp-methods.php`
- Rate limiters: `check_rate_limit()` / `check_tool_rate_limit()` in `includes/class-wp-mcp-ai-rest.php`
- Implementation plans: `docs/developer/implementation-plan-mcp-agent-compat.md`, `docs/developer/legacy-sse-transport-plan.md`
