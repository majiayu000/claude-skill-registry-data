---
name: nvoos-gateway
description: Operate NV oOS WordPress sites through the NV oOS MCP Gateway — namespaced tools, key scoping, background research, and health checks. Use when working with tools prefixed <site-slug>.<tool> or when asked about the gateway.
---

# NV oOS MCP Gateway

The gateway is a public, fleet-scoped MCP endpoint aggregating the native
MCP bridges of bound NV oOS (Open Operator System) WordPress sites. One API
key authenticates against every site bound to that key.

## Tool namespacing

Tools are always namespaced `<site-slug>.<tool>` — e.g. `demo.deep_research`,
`console.create_post`. The site part of the name decides which WordPress
site executes the tool. Call tools with the prefixed name exactly as listed;
never strip the prefix.

## Scoping

- Every key maps to a set of sites; tools outside the key's bindings are
  not listed and are rejected with `-32602`.
- Each site enforces its own Fleet Operator allowlist server-side: a key
  can only see and call what the site's operator credential permits.
- Read-only keys exist (demo keys): write-capable tools fail with 403.

## OAuth 2.1 resource server (Phase 1, PR #6945)

With `GATEWAY_OAUTH_ISSUER` set, the gateway is an RFC 9728 protected
resource **alongside** static API keys; everything stays inert (404 /
unchanged 401s) when OAuth is unconfigured.

- **Metadata** — `GET /.well-known/oauth-protected-resource` and the
  `/mcp` path-insertion variant (each asserts its matching `resource`
  identifier per RFC 9728 §3.3).
- **Challenges** — 401s carry `WWW-Authenticate: Bearer` with
  `resource_metadata` + the supported-scope list; scope-less tokens get
  403 `insufficient_scope`.
- **Tokens** — zero-dependency JWT validation (`src/oauth/jwt.js`):
  node:crypto RS256/384/512 + ES256/384, in-memory JWKS cache with TTL +
  rotation refetch, strict `iss` / `aud` (accepting the `/mcp` variant) /
  `exp` / `nbf` / scope checks — **fail-closed** on any fetch or parse
  failure.
- **Site binding** — `site:<slug>` scopes grant access to bound sites
  (mirroring static-key semantics); `site:read` is advertised for future
  fine-grained enforcement.
- **No token passthrough** — the gateway keeps exchanging for per-site
  Fleet Operator tokens; OAuth tokens never travel upstream
  (confused-deputy discipline required by the spec).
- **Config** — `GATEWAY_OAUTH_ISSUER` / `GATEWAY_OAUTH_JWKS_URI` /
  `GATEWAY_OAUTH_RESOURCE`, validated as absolute https URLs (boot fails
  closed on invalid values).

Phases 2–5 (Auth0 tenant provisioning with DCR + PKCE, scripted PKCE
end-to-end + ChatGPT "Add custom MCP server" test, `server.json` +
`mcp-publisher` registry submission, deployment guide) are deferred.

## Long-running tools

Tools such as `deep_research` (standard/comprehensive depth) can exceed
client-side tool timeouts in immediate mode. Prefer:

- `run_mode: "background"` — returns immediately; results are cached for
  one hour and served on the next call with the same topic, or
- a raised client timeout (`MCP_TIMEOUT=180000` in Claude Code).

## Health & errors

- Public health: `GET https://mcp.nvoos.pro/health` (no auth).
- A failing upstream site degrades the tool list with a
  `_meta.gateway.errors` entry instead of failing the whole list.
- `-32603` with "upstream timeout" means the site is slow or the gateway
  budget was exceeded — retry with background mode for long tools.

## Empty tools/list -- diagnosis (verified 2026-10)

An empty `tools: []` with **no** `_meta.gateway.errors` entry means the bound
upstream(s) answered -- it is a scoping problem, not an outage. Work the
chain in order:

1. `GET /health` (public) and `GET /health/full` (Bearer key): check the
   key's `bindings` (which sites this key reaches), each site's upstream
   `url`, and `lastOkAt`/`lastError`.
2. Call the site's native MCP endpoint directly
   (`https://<site>/wp-json/mcp-ai/v1/mcp`) with the site's Fleet Operator
   token (`op_xxxx.SECRET`) -- the credential family the gateway uses
   upstream. Per-assistant `cred_...` tokens are a different family and do
   not reflect the gateway's view.
3. `initialize` reveals the bound assistant (`serverInfo.name`) and plugin
   version. If that assistant has tools assigned (check
   `GET /wp-json/mcp-ai/v1/assistants` with the same token -- the roster
   includes each assistant's `tools` array) but `tools/list` is still
   empty, the scoping layer is the Fleet Operator allowlist.
4. Confirm with `tools/call` on a tool the assistant definitely has: a
   `-32603` error reading "Tool \"X\" is outside this operator credential's
   allowlist" (HTTP 403) is the signature of an empty operator allowlist.
5. Fix on the site, not the gateway: Settings -> External Operators, edit
   the operator credential, and populate the tool allowlist (slugs, fnmatch
   globs, `group:<toolkit>` entries, or `*` for a wide-open demo). Scoping
   is per-request and stateless -- no gateway restart or key rotation is
   needed; the namespaced tools appear on the next `tools/list`.

Two gateway bindings may point at the same site host with different
operator credentials; each binding is scoped independently, so one key can
see zero tools for a site while another key sees the full roster.

## Conventions

- Prefer read-only tools for checks; keep writes explicit and minimal.
- Verify credentials before reporting auth failures — a 401 means the
  key is wrong, rotated, or not bound to the requested site.
