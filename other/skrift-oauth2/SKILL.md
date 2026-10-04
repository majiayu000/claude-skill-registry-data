---
name: skrift-oauth2
description: "Skrift OAuth2 Authorization Server — hub/spoke identity federation, Authorization Code + PKCE flow, token architecture, and Skrift auth provider."
---

# Skrift OAuth2 Authorization Server

Skrift can act as an OAuth2 Authorization Server (hub) so other Skrift instances (spokes) can authenticate users against it. Supports Authorization Code grant with PKCE (S256 only). Tokens are stdlib HMAC-SHA256 signed — no JWT library required.

## Hub/Spoke Flow

```
Spoke Site                          Hub Site (OAuth2 Server)
──────────                          ────────────────────────
User clicks "Login with Skrift"
    │
    ├──→ GET /oauth/authorize ──────→ Show consent screen
    │                                  (or redirect to /auth/login first)
    │
    │    ◄── Redirect with ?code= ◄── User clicks "Allow"
    │
    ├──→ POST /oauth/token ─────────→ Validate code + PKCE
    │    ◄── { access_token, ... } ◄── Return token pair
    │
    ├──→ GET /oauth/userinfo ───────→ Validate access token
    │    ◄── { sub, email, name } ◄── Return user claims
    │
    └──→ Session created on spoke
```

## Hub Configuration (`app.yaml`)

The hub registers each spoke as an OAuth2 client:

```yaml
oauth2:
  clients:
    - client_id: "spoke-site-1"
      client_secret: "optional-secret"  # omit for public clients
      redirect_uris:
        - "https://spoke.example.com/auth/skrift/callback"
```

Config model: `OAuth2ClientConfig`

| Field | Type | Default | Notes |
|-------|------|---------|-------|
| `client_id` | `str` | required | Unique identifier for the spoke |
| `client_secret` | `str` | `""` | Empty = public client (PKCE required) |
| `redirect_uris` | `list[str]` | `[]` | Allowed callback URLs (strict match) |

The `OAuth2Controller` is auto-registered when `settings.oauth2.clients` is non-empty (`skrift/asgi.py:731`). The `/oauth/token` endpoint is auto-excluded from CSRF.

## Spoke Configuration (`app.yaml`)

The spoke uses the `skrift` auth provider to point at the hub:

```yaml
auth:
  redirect_base_url: "https://spoke.example.com"
  providers:
    skrift:
      server_url: "https://hub.example.com"
      client_id: "spoke-site-1"
      client_secret: ""  # empty for public clients
      scopes: ["openid", "profile", "email"]
```

Config model: `SkriftProviderConfig`

| Field | Type | Default | Notes |
|-------|------|---------|-------|
| `server_url` | `str` | required | Base URL of the hub Skrift instance |
| `client_id` | `str` | required | Must match a hub `oauth2.clients` entry |
| `client_secret` | `str` | `""` | Empty = public client |
| `scopes` | `list[str]` | `["openid", "profile", "email"]` | Requested scopes |

## Endpoints (Hub)

| Method | Path | Purpose |
|--------|------|---------|
| `GET` | `/oauth/authorize` | Show consent screen (or redirect to login if unauthenticated) |
| `POST` | `/oauth/authorize` | Process consent form — issue auth code via redirect |
| `POST` | `/oauth/token` | Exchange auth code or refresh token for access/refresh tokens |
| `GET` | `/oauth/userinfo` | Return user claims from a valid `Bearer` access token |

## Token Architecture

All tokens use `base64(json_payload).base64(hmac_sha256_signature)` format. Signed with `settings.secret_key`.

| Token | TTL | `type` field | Payload |
|-------|-----|-------------|---------|
| Auth code | 10 min | `"code"` | `user_id`, `email`, `name`, `picture_url`, `client_id`, `redirect_uri`, `code_challenge` |
| Access token | 15 min | `"access"` | `user_id`, `email`, `name`, `picture_url`, `client_id` |
| Refresh token | 30 days | `"refresh"` | `user_id`, `client_id` |

The `type` field prevents cross-use — a refresh token cannot be used as an access token.

Token exchange with `grant_type=refresh_token` performs **token rotation**: both access and refresh tokens are reissued.

## PKCE

- Only `S256` is supported (`code_challenge_method=S256`)
- **Required** for public clients (no `client_secret`)
- Optional but supported for confidential clients
- Verification: `base64url(sha256(code_verifier)) == code_challenge`
- The `code_challenge` is embedded in the auth code token and verified at `/oauth/token`

## SkriftProvider (Spoke Side)

`SkriftProvider` (`skrift/auth/providers.py:245`) handles the spoke's OAuth flow:

- `requires_pkce = True` — always sends PKCE parameters
- `resolve_url()` replaces `{server_url}` in provider URLs with the configured `server_url`
- `build_token_data()` omits `client_secret` from POST body when empty (public client)
- `extract_user_data()` maps hub's `sub` → `oauth_id`, plus `email`, `name`, `picture`

Provider URLs are defined in `skrift/setup/providers.py` with `{server_url}` placeholders:
- `auth_url`: `{server_url}/oauth/authorize`
- `token_url`: `{server_url}/oauth/token`
- `userinfo_url`: `{server_url}/oauth/userinfo`

## Consent Template

`skrift/templates/oauth/authorize.html` — extends `auth/base.html`, shows client ID and requested scopes. CSRF-protected form with Allow/Deny buttons. Customizable by overriding in project `templates/oauth/authorize.html`.

## Security Notes

- Tokens are **signed, not encrypted** — payload is base64-encoded and readable. Do not store secrets in token payloads.
- `redirect_uri` is validated against the client's registered list (strict match)
- Consent form uses CSRF protection (`csrf_field`)
- The `type` field in each token prevents cross-use (code vs access vs refresh)
- `hmac.compare_digest` used for constant-time signature comparison

## Key Files

| File | Purpose |
|------|---------|
| `skrift/controllers/oauth2.py` | OAuth2Controller — authorize, token, userinfo endpoints |
| `skrift/auth/tokens.py` | `create_signed_token()` / `verify_signed_token()` — HMAC-SHA256 |
| `skrift/auth/providers.py` | `SkriftProvider` class (spoke-side OAuth flow) |
| `skrift/config.py` | `OAuth2ClientConfig`, `OAuth2Config`, `SkriftProviderConfig` |
| `skrift/setup/providers.py` | `OAuthProviderInfo` for `skrift` (URL templates, fields) |
| `skrift/asgi.py` | Auto-registers `OAuth2Controller` when clients configured |
| `skrift/templates/oauth/authorize.html` | Consent screen template |
| `skrift/auth/session_keys.py` | Session key constants used in auth code payload |
| `skrift/forms/__init__.py` | `verify_csrf()` used by consent POST |
| `tests/test_oauth2_server.py` | OAuth2 server endpoint tests |
