---
name: auth
description: 'Use when the user wants to authenticate to a NocoBase v2 instance, asks "how do I get a token for NocoBase", "how do I log in via API or CLI", "how do I connect an agent or MCP client", "why is my request returning 401 from NocoBase", or needs working curl/Node samples that send the bearer token. Covers the CLI path (`nb env add` / `nb env auth`), the upstream login flow (NB_USER + NB_PASSWORD → auth:signIn → token), the long-lived API Key path, OAuth through the IdP: OAuth plugin, and the separate Auth: OIDC SSO plugin.'
---

# Authentication — NocoBase v2

NocoBase v2 accepts `Authorization: Bearer <token>` on every `/api/` request. The OpenAPI spec declares this as the `api-key` security scheme (HTTP bearer). There are four ways to get a token; pick by who or what is calling:

| Caller | Pick |
|---|---|
| An agent or person at a terminal using the `nb` CLI | **Path 0** — `nb env add` / `nb env auth` (native; credential stored by the CLI) |
| Script that can store the admin password | **Path A** — sign-in |
| CI job, cron, bot, MCP client — wants a static token | **Path B** — API Key |
| A tool that must sign in as a person without a password (CLI on a headless host, MCP client) | **Path C** — OAuth via the IdP: OAuth plugin |
| End users clicking "Sign in with Google / Keycloak / Entra" in the browser | **Path D** — Auth: OIDC (SSO; a different plugin from Path C) |

## Path 0 — the CLI way (`nb env add` / `nb env auth`)

The CLI keeps a named *env* (API base URL plus credential) and every `nb api …` command uses it. No environment variables are needed.

```bash
# Save the endpoint (URL includes /api) and choose how to authenticate
nb env add prod --api-base-url https://app.example.com/api --auth-type token --access-token <api-key>
nb env add prod --api-base-url https://app.example.com/api --auth-type basic --username <user>   # password prompted in a TTY
nb env add prod --api-base-url https://app.example.com/api --auth-type oauth                     # browser / device sign-in
nb env add prod --api-base-url https://app.example.com/api --skip-auth                           # authenticate later

# Authenticate (or re-authenticate) a saved env
nb env auth prod --auth-type basic|token|oauth
nb env info prod        # shows the saved auth type; secrets masked unless --show-secrets
```

`--auth-type oauth` signs in through the IdP: OAuth plugin using the **Device Authorization Grant** when the server supports it: the command prints a verification URL and a code, and you approve in any browser — it works on a remote or headless server. Otherwise it falls back to a browser loopback (PKCE) flow. `--auth-type oauth` cannot be combined with `--access-token`, `--username` or `--password`. Prefer `oauth` or `token` over putting a password on the command line.

This is the *native* way. The `NB_URL` / `NB_USER` / `NB_PASSWORD` / `NB_TOKEN` variables below remain for curl and Node scripts and for the `nocobase-dsl-reconciler` scripts.

## Env vars contract (REST scripts and `nocobase-dsl-reconciler`)

```bash
NB_URL=https://app.example.com           # required
NB_USER=admin@example.com                # required for Path A (sign-in)
NB_PASSWORD=<password>                   # required for Path A
NB_TOKEN=eyJhbGciOi...                   # optional, skips sign-in (Path B)
# NOCOBASE_API_TOKEN is a synonym for NB_TOKEN — upstream auth.ts reads either.
```

These names match what the upstream `nocobase/skills` library uses — keep them identical in your `.env` so hand-maintained and upstream skills agree on one truth.

## Path A — Sign-in with admin credentials (upstream default for scripts)

This is what the upstream `nocobase-dsl-reconciler` skill uses. Username + password → `auth:signIn` → short-lived bearer token. Best for scripts that are OK re-logging in periodically.

```bash
export NB_URL="https://app.example.com"
export NB_USER="admin@example.com"
export NB_PASSWORD="<password>"

# 1. Sign in and capture the token
TOKEN=$(curl -sS -X POST "${NB_URL}/api/auth:signIn" \
  -H "Content-Type: application/json" \
  -d '{"account":"'"$NB_USER"'","password":"'"$NB_PASSWORD"'"}' \
  | jq -r '.data.token')

# 2. Use it as a Bearer
curl -H "Authorization: Bearer $TOKEN" \
     "${NB_URL}/api/collections:list"
```

The `NB_USER` value is whatever admin account you set during `nb init --ui` — the root-admin account.

## Path B — Long-lived API Key (when you want a static token)

Useful when you don't want to re-login every call: cron jobs, agents, deploy hooks, third-party integrations, MCP clients.

### 1. Make sure the API Keys plugin is on

`API keys` (`@nocobase/plugin-api-keys`) is built in and enabled by default. If `nb plugin list` shows it disabled:

```bash
nb plugin enable @nocobase/plugin-api-keys
```

The `nocobase-plugin-manage` skill covers `nb plugin` semantics and error handling.

### 2. Create a token in the admin UI

Open NocoBase → `Settings → API keys → Create`:

- **Name** — short identifier (e.g. `agent-bot`).
- **Role** — pick the role whose permissions the key inherits. The token can do exactly what the role can; no more.
- **Expiration** — date or `Never`.

Copy the token; it is shown only once. Put it in `NB_TOKEN` (or hand it to `nb env add --auth-type token`).

The server must have `APP_KEY` configured and kept stable — **if `APP_KEY` changes, every issued API key becomes invalid**.

### 3. Send authorised requests

```bash
export NB_URL="https://app.example.com"
export NB_TOKEN="<token-from-admin-ui>"

# List collections
curl -H "Authorization: Bearer ${NB_TOKEN}" \
     "${NB_URL}/api/collections:list"

# Create a record in the `posts` collection
curl -X POST \
     -H "Authorization: Bearer ${NB_TOKEN}" \
     -H "Content-Type: application/json" \
     -d '{"title":"hello","body":"first post"}' \
     "${NB_URL}/api/posts:create"
```

### 4. Node.js

```js
// fetch (built into Node)
const res = await fetch(`${process.env.NB_URL}/api/collections:list`, {
  headers: { Authorization: `Bearer ${process.env.NB_TOKEN}` },
});
const data = await res.json();
```

```js
// axios
import axios from "axios";

const nb = axios.create({
  baseURL: `${process.env.NB_URL}/api`,
  headers: { Authorization: `Bearer ${process.env.NB_TOKEN}` },
});

const { data } = await nb.get("/collections:list");
```

### Rotation and revocation

- Tokens are revoked from the same screen (`Settings → API keys → Delete`).
- Rotation: create the new token first, deploy it, then delete the old one — there is no in-place rotation.
- Tokens inherit the role at issuance. If the role is later restricted, the token is restricted on the next request.

## Path C — OAuth through IdP: OAuth (NocoBase as the identity provider)

The `IdP: OAuth` plugin (`@nocobase/plugin-idp-oauth`, built in, enabled by default; OAuth 2.1 and OpenID Connect) turns NocoBase **into** an identity provider for other tools. It is what lets `nb env auth --auth-type oauth` and MCP clients sign in as a NocoBase user without an API key or a stored password. It is **not** the way users sign in to NocoBase with an external IdP — that is Path D.

```bash
nb plugin list                                  # confirm @nocobase/plugin-idp-oauth is enabled
nb env auth prod --auth-type oauth              # CLI: device flow on headless hosts, browser otherwise
```

MCP clients (Claude Code shown; the endpoint is `https://<host>:<port>/api/mcp`, see `overview`):

```bash
claude mcp add --transport http nocobase https://<host>:<port>/api/mcp
# then, inside Claude Code: /mcp  → pick the server → sign in
```

Permissions follow the signed-in user; if the user has several roles, choose one with the `x-role` request header (`nb api … --role <name>` sets it).

## Path D — Auth: OIDC (SSO sign-in for end users)

`Auth: OIDC` is a **separate, commercial (Professional Edition) plugin** that lets people sign in to NocoBase with accounts from an external IdP (Google, Keycloak, Microsoft Entra ID, …) using the Authorization Code flow. It is not for backend scripts — use Path A, B or C for those. It is a licensed plugin and is not on public npm — licensed plugins are managed with `nb license` (`nb license --help`), then enabled like any other.

1. Enable the `Auth: OIDC` plugin in the plugin manager (licensed plugin).
2. `Settings → Authentication → Add → OIDC` and fill in: **Issuer** (the IdP's issuer / discovery URL), **Client ID**, **Client Secret**, **scope** (default `openid email profile`), and the field mapping used to bind users (email or username).
3. Copy the **Redirect URL** shown in the plugin's *Usage* section into the IdP's client settings.
4. Users sign in from the login page by clicking the provider button below the login form.

When testing locally use `127.0.0.1` rather than `localhost` — the state value is validated through a client cookie.

A browser SSO login gives a browser session. For agents and scripts, create an API key (Path B), or use Path C.

## Common 401 / 403 causes

- Missing or wrong `Authorization` header — value is exactly `Bearer <token>`, single space, case-sensitive `Bearer`.
- Token expired (API Key with explicit expiration, sign-in token after TTL, OAuth access token).
- API key issued before `APP_KEY` was changed — recreate it.
- Role attached to the token has no permission — check `nocobase-acl-manage`.
- Plugin providing the token type is disabled — `nb plugin list` to confirm `@nocobase/plugin-api-keys` (API keys) or `@nocobase/plugin-idp-oauth` (OAuth) is enabled.
- Multi-app instance — make sure the `X-App` header / hostname matches the app the token was issued for.
- Wrong `--api-base-url` for the CLI — it must include the `/api` prefix (`nb env info <name>` shows what is saved; `nb env update <name> --api-base-url …` fixes it).

## OpenAPI declaration

The full spec at `${CLAUDE_PLUGIN_ROOT}/references/openapi/nocobase.json` declares:

```jsonc
"securitySchemes": {
  "api-key": { "type": "http", "scheme": "bearer" }
}
```

All the paths above (CLI env, sign-in, API Key, OAuth) produce a bearer token that satisfies this scheme — the server validates the token, not its origin.