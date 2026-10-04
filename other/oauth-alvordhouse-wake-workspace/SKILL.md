---
name: OAuth
description: Implement OAuth 2.0 and OpenID Connect flows securely.
metadata: {"clawdbot":{"emoji":"🔑","os":["linux","darwin","win32"]}}
---

## Flow Selection

- Authorization Code + PKCE: use for all clients—web apps, mobile, SPAs
- Client Credentials: service-to-service only—no user context
- Implicit flow: deprecated—don't use; was for SPAs before PKCE existed
- Device Code: for devices without browsers (TVs, CLIs)—user authorizes on separate device

## PKCE (Proof Key for Code Exchange)

- Required for public clients (SPAs, mobile), recommended for all
- Generate `code_verifier`: 43-128 char random string, stored client-side
- Send `code_challenge`: SHA256 hash of verifier, sent with auth request
- Token exchange includes `code_verifier`—server verifies against stored challenge
- Prevents authorization code interception—attacker can't use stolen code without verifier

## State Parameter

- Always include `state` in authorization request—prevents CSRF attacks
- Generate random, unguessable value; store in session before redirect
- Verify returned `state` matches stored value before processing callback
- Can also encode return URL or other context (encrypted or signed)

## Redirect URI Security

- Register exact redirect URIs—no wildcards, no open redirects
- Validate redirect_uri on both authorize and token endpoints
- Use HTTPS always—except localhost for development
- Path matching is exact—`/callback` ≠ `/callback/`

## Tokens

- Access token: short-lived (minutes to hour), used for API access
- Refresh token: longer-lived, used only at token endpoint for new access tokens
- ID token (OIDC): JWT with user identity claims—don't use for API authorization
- Don't send refresh tokens to resource servers—only to authorization server

## Scopes

- Request minimum scopes needed—users trust granular requests more
- Scope format varies: `openid profile email` (OIDC), `repo:read` (GitHub-style)
- Server may grant fewer scopes than requested—check token response
- `openid` scope required for OIDC—triggers ID token issuance

## OpenID Connect

- OIDC = OAuth 2.0 + identity layer—adds ID token and UserInfo endpoint
- ID token is JWT with `sub`, `iss`, `aud`, `exp` + profile claims
- Verify ID token signature before trusting claims
- `nonce` parameter prevents replay attacks—include in auth request, verify in ID token

## Security Checklist

- HTTPS everywhere—tokens in URLs must be protected in transit
- Validate `iss` and `aud` in tokens—prevents token confusion across services
- Bind authorization code to client—code usable only by requesting client
- Short authorization code lifetime (10 min max)—single use
- Implement token revocation for logout/security events

## Common Mistakes

- Using access token as identity proof—use ID token for authentication
- Storing tokens in localStorage—vulnerable to XSS; prefer httpOnly cookies or memory
- Not validating redirect_uri—allows open redirect attacks
- Accepting tokens from URL fragment in backend—fragment never reaches server
- Long-lived access tokens—use short access + refresh pattern

## Token Endpoints

- `/authorize`: user-facing, returns code via redirect
- `/token`: backend-to-backend, exchanges code for tokens; requires client auth for confidential clients
- `/userinfo` (OIDC): returns user profile claims; requires access token
- `/revoke`: invalidates tokens; accepts access or refresh token

## Client Types

- Confidential: can store secrets (backend apps)—uses client_secret
- Public: cannot store secrets (SPAs, mobile)—uses PKCE only
- Never embed client_secret in mobile apps or SPAs—it will be extracted
