---
name: mcp-authorization
description: This skill should be used when the user mentions "MCP auth", "MCP OAuth", "MCP authorization", "OAuth 2.1", "OIDC", "access token validation", "audience", "resource server", "protected resource metadata", "token passthrough", "confused deputy", "Entra", "Okta", or securing a remote MCP server's identity and access. It provides the 2026-07-28 OAuth 2.1 / OIDC model for MCP servers as OAuth resource servers.
---

# MCP Authorization

## Purpose
The MCP 2026-07-28 spec aligns authorization with production **OAuth 2.1 and OIDC**, so a remote MCP server plugs into enterprise identity (Microsoft Entra, Okta, Auth0, Keycloak) without custom workarounds. The model is simple to state and easy to get dangerously wrong: the **MCP server is an OAuth 2.1 resource server**. It does not mint tokens and it does not log users in; it **validates** an access token on every request and serves only what that token authorizes. This skill covers correct validation and the two highest-severity anti-patterns, token passthrough and the confused deputy. (stdio/local servers do not use OAuth, skip this for them.)

## The roles
| Role | Who | Responsibility |
|---|---|---|
| Authorization server (AS) | Entra / Okta / Auth0 / your IdP | authenticates the user, issues access tokens |
| Resource server (RS) | **your MCP server** | validates the token, enforces scope, serves tools |
| Client | Claude Code / the host app | obtains a token from the AS, sends it to the RS |

Your job is the RS. You never see the user's password; you receive a bearer access token and must prove it is valid **and minted for you**.

## Validate every token, every request
On each request, verify (see `references/token-validation.md` for code):
- **Signature** against the AS's published JWKS (cache keys, honor rotation).
- **Issuer** (`iss`) equals your trusted AS.
- **Audience** (`aud`) equals **this MCP server's** identifier. This is the line that stops the confused deputy, "a valid JWT" is not enough; it must be a token intended for you.
- **Expiry / not-before** (`exp`, `nbf`) within skew.
- **Scope** covers the specific tool/action being invoked; enforce least privilege per tool.
Reject with `401` (invalid/absent/expired token) or `403` (valid token, insufficient scope). A stateless RS validates the token on the request itself, no server session needed.

## Protected Resource Metadata
Publish `/.well-known/oauth-protected-resource` describing this RS and pointing clients at the authorization server(s) that can issue tokens for it. This is how a 2026-07-28 client discovers where to authenticate. Returning a `WWW-Authenticate` header on a `401` that references this metadata lets the client start the OAuth flow automatically.

## The two anti-patterns that fail an audit
1. **Token passthrough.** The RS takes the client's incoming token and reuses it to call a downstream API (GitHub, a database proxy, another service). This leaks the token beyond its intended audience and lets a compromised server impersonate the user everywhere. Correct: the RS uses **its own** credential or performs a proper token exchange to obtain a **new** token scoped to the downstream audience.
2. **Confused deputy.** The RS accepts any well-formed token without checking `aud`, so a token minted for service A is replayed against your server and honored. Correct: bind `aud` to this server and reject anything else.

## Golden rules
- **Validate audience, not just validity.** Bind `aud` to this server; reject tokens minted for anyone else.
- **Never pass the incoming token downstream.** Mint/exchange a token for the downstream audience instead.
- **Least privilege per tool.** Map scopes to actions; a read token cannot invoke a destructive tool.
- **Publish Protected Resource Metadata** and answer `401` with a `WWW-Authenticate` pointer.
- **Secrets from the environment / a secret store**, never hard-coded, never logged.
- **stdio servers are exempt**, no OAuth; do not add token checks to a local single-user process.

## Additional Resources
### Reference Files
- **`references/oauth-oidc-patterns.md`**: the RS discovery/handshake flow, Protected Resource Metadata shape, `WWW-Authenticate` challenge, downstream token exchange vs passthrough, and per-IdP notes (Entra, Okta, Auth0, Keycloak).
- **`references/token-validation.md`**: copy-adaptable JWT/JWKS validation (Node `jose`, Python `PyJWT`/`authlib`) with audience/issuer/expiry/scope checks and the confused-deputy test.
