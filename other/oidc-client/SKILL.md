---
name: oidc-client
description: Build and review OAuth 2.x and OpenID Connect clients and resource servers in Node.js/TypeScript with openid-client 6.x, jose 6.x and oauth4webapi 3.x (checked against 6.8.8, 6.2.14, 3.8.8), per the OAuth Security BCP (RFC 9700) and OAuth 2.1. Covers code flow + PKCE S256 login with state and nonce stored server-side and used once, the redirect_uri openid-client sends behind a proxy, RFC 9207 iss checks, what openid-client verifies in ID tokens, JWT access token validation in APIs (RFC 9068 typ at+jwt, issuer, audience, pinned algorithms, required exp, JWKS from discovery with rotation, RFC 6750 errors), refresh token rotation with reuse detection (single-flight refresh, storing the rotated token, invalid_grant vs outages) and logout. Use when code imports openid-client, jose or oauth4webapi, when adding login, SSO or OIDC to an app or BFF, protecting an API with bearer JWTs, refreshing tokens, or on openid-client v5 idioms (Issuer.discover, generators, client.callback) or hand-decoded JWTs.
license: MIT
---

# OAuth 2.x and OpenID Connect in Node.js

Three jobs share one set of mistakes: **signing users in** (a web app or BFF is the OAuth client),
**protecting an API** (a resource server validating bearer tokens) and **calling APIs on a user's
behalf** (refreshing tokens). Much of the example code on the web uses openid-client v5 or
`jsonwebtoken`, validates JWTs by decoding them, and ignores concurrency in refresh. Everything
below was checked on 2026-11-01 against openid-client 6.8.8, jose 6.2.14, oauth4webapi 3.8.8 and
Node 24, and run against a local identity provider.

## 1. Know which libraries you have

```sh
npm ls openid-client jose oauth4webapi
```

| Installed | What it is | Write |
| --- | --- | --- |
| `openid-client@6.x` | Functional API on top of oauth4webapi; ESM; Web Crypto + fetch | `import * as oidc from 'openid-client'`, `oidc.discovery(...)`, then free functions that take the `Configuration` |
| `openid-client@5.x` | Legacy class API (`Issuer`, `Client`, `generators`, `TokenSet`) | Match the repo, or migrate with [the v5 to v6 map](references/openid-client-v6.md). v6.x is the only line listed as supported in the README. |
| `jose@6.x` | JWT/JWS/JWE/JWKS primitives; returns `CryptoKey`s; ESM | `jwtVerify` + `createRemoteJWKSet` for APIs |
| `oauth4webapi@3.x` | Low-level, spec-shaped OAuth functions (openid-client's engine) | Only when you need full control; includes `validateJwtAccessToken` for RFC 9068 |

openid-client 6 has **no** `Issuer`, `Client`, `generators`, `custom` or `TokenSet` exports. Code
that imports them fails at module load (`does not provide an export named 'Issuer'`). The Passport
strategy moved to `openid-client/passport`. CommonJS `require()` works only where Node has
`require(esm)` (20.19+, 22.12+, 23+).

## 2. Signing users in (authorization code + PKCE)

### Procedure

1. Discover once and cache the `Configuration`: `await oidc.discovery(new URL(issuer), clientId, clientSecret)`.
   openid-client refuses plain HTTP (`ClientError` `OAUTH_HTTP_REQUEST_FORBIDDEN`, "only requests to
   HTTPS are allowed"); pass `{ execute: [oidc.allowInsecureRequests] }` as the fifth argument only
   behind an explicit dev/test setting. With a secret string the client authenticates with
   `client_secret_post`; for `client_secret_basic` call
   `discovery(issuerUrl, clientId, undefined, oidc.ClientSecretBasic(secret))`.
2. On `/login`, generate **per attempt**: `randomPKCECodeVerifier()`, `randomState()`,
   `randomNonce()`. Store them server-side (session, or an encrypted/signed short-lived cookie) with a
   timestamp. Never in a module-level variable: the next visitor overwrites it.
3. Redirect to `buildAuthorizationUrl(config, { redirect_uri, scope: 'openid ...', code_challenge:
   await calculatePKCECodeChallenge(verifier), code_challenge_method: 'S256', state, nonce })`.
   `calculatePKCECodeChallenge` is **async**; without `await` the URL carries
   `code_challenge=[object Promise]` and the token exchange fails.
4. On the callback, **take the pending attempt out of storage before validating** (single use), reject
   if none or expired, then call `authorizationCodeGrant(config, currentUrl, checks)`.
5. Regenerate the session id, then store the user (`tokens.claims()`), and keep `tokens.id_token`
   for logout. Redirect to a fixed path or a validated same-site path, never to a raw `returnTo`.

```ts
import * as oidc from 'openid-client'

// Callback. `started` (verifier, state, nonce) was already removed from the session.
const returnedTo = new URL(rp.redirectUri)                       // the registered, public URL
returnedTo.search = new URL(req.originalUrl, returnedTo).search  // plus the IdP's query string
const tokens = await oidc.authorizationCodeGrant(idpConfig, returnedTo, {
  pkceCodeVerifier: started.verifier,
  expectedState: started.state,
  expectedNonce: started.nonce,
  idTokenExpected: true,
})
const claims = tokens.claims()! // validated ID token claims: sub, email, name...
```

### What `authorizationCodeGrant` does, and the traps around it

- **`redirect_uri` comes from `currentUrl`.** It sends `currentUrl` minus query and fragment as the
  token request's `redirect_uri`. Behind a TLS-terminating proxy, `req.protocol`, `req.host` and the
  Host header describe the internal hop (`http://10.0.3.7:3000/...`), so building the URL from the
  request gives `invalid_grant` ("redirect_uri does not match"). Build it from the configured redirect
  URI as above. If the registered redirect URI has its own query string, see the `customFetch`
  workaround in [openid-client v6](references/openid-client-v6.md).
- `currentUrl` must be a `URL` or a Fetch `Request`; a string (`req.url`) is a `TypeError`.
- **Checks are exact expectations.** `expectedState: undefined` means "the response must have no
  state"; `expectedNonce: undefined` means "the ID token must have no nonce". Sending a nonce and
  forgetting `expectedNonce` fails every login with "unexpected JWT claim value". Never use
  `oidc.skipStateCheck` to make an error go away.
- **iss (RFC 9207) is checked for you**: a callback whose `iss` differs from the discovered issuer
  is rejected, and so is a callback without `iss` when the IdP advertises
  `authorization_response_iss_parameter_supported`. Pass the full query string; don't rebuild it.
- An `error=access_denied` callback throws `AuthorizationResponseError` (`err.error`). Handle it as
  a normal "sign-in cancelled" page, not a 500.
- **ID token checks it performs**: `alg` against the client's `id_token_signed_response_alg`, else
  the IdP's `id_token_signing_alg_values_supported`, else RS256 (so `none` and unexpected HS256 are
  rejected); `iss`, `sub`, `aud`, `exp`, `iat` present; `iss` equals the issuer; `aud` contains the
  client id; several audiences require `azp` equal to the client id; `exp` with 30 s tolerance;
  `nonce`; `auth_time` when `maxAge` is used.
- **It does not verify the ID token signature by default.** OIDC Core 3.1.3.7 lets a client rely on
  TLS to the token endpoint instead. A token signed by a foreign key with the right claims is
  accepted. If you keep or forward the ID token as proof of anything, or the token endpoint is not
  behind TLS, add `oidc.enableNonRepudiationChecks` (to `execute`, or call it on the config), which
  verifies against the IdP's JWKS.

### Rules that libraries cannot enforce for you

- One pending attempt per transaction, bound to the browser that started it, consumed once. A
  callback for an attempt this browser did not start must fail (login CSRF, code injection), and
  replaying a used callback must not reach the token endpoint again.
- Session fixation: call `req.session.regenerate()` (express-session) after the code exchange and
  before writing the user; with your own store, issue a new session id.
- Store tokens server-side (BFF pattern). Don't put access or refresh tokens in `localStorage` or
  in a cookie the browser can read.
- Ask for `offline_access` (or the IdP's equivalent) only if you will refresh.
- Request scopes, not roles: authorization decisions use claims you validated, not what the
  frontend sent.

## 3. Protecting an API (resource server)

A resource server validates every access token itself. "It came over TLS from our gateway" is not
validation, and decoding the payload (`jose.decodeJwt`, `jwt.decode`, `JSON.parse(atob(...))`)
verifies nothing.

```ts
import { createRemoteJWKSet, jwtVerify } from 'jose'

// Once per process: discovery keeps the issuer path (append, don't resolve against "/").
const meta = await (await fetch(`${issuer.replace(/\/$/, '')}/.well-known/openid-configuration`)).json()
if (meta.issuer !== issuer) throw new Error('discovery issuer mismatch')
const jwks = createRemoteJWKSet(new URL(meta.jwks_uri)) // reuse across requests

export async function verifyBearer(token: string) {
  const { payload } = await jwtVerify(token, jwks, {
    issuer,
    audience: apiIdentifier,
    algorithms: ['RS256', 'ES256'],     // what your IdP actually uses
    typ: 'at+jwt',                       // RFC 9068 access tokens
    requiredClaims: ['exp', 'sub', 'client_id'],
  })
  return payload
}
```

Non-obvious facts about jose 6:

- **`exp` and `nbf` are checked only if present.** A token without `exp` passes unless
  `requiredClaims` includes `'exp'`. RFC 9068 makes `exp` mandatory; require it.
- `issuer`, `audience` and `subject` options also require the claim. `aud` may be an array; it
  passes when any entry matches.
- `typ` comparison ignores case and an `application/` prefix, so `at+jwt` also accepts
  `application/at+jwt` (both are valid per RFC 9068).
- `alg: none` is never accepted by `jwtVerify`. Without `algorithms`, any algorithm that fits the
  key is allowed; pin the list anyway, and remember a pinned list blocks a rotation to a new key
  type (RS256 to ES256) unless both are listed.
- `createRemoteJWKSet` caches keys (`cacheMaxAge` 10 min), refetches when a token names an unknown
  `kid` but at most once per `cooldownDuration` (30 s), times out after 5 s, does not follow
  redirects and rejects non-200 responses. Create it once; one per request refetches every time.
  A cache that never refetches (keys loaded at startup) breaks on the IdP's next rotation.
- **Never accept an ID token as an access token.** An ID token's `aud` is a client id and its `typ`
  is `JWT`. Require your API's audience and `typ: 'at+jwt'` when your IdP issues RFC 9068 tokens;
  if it does not set `typ`, check what it sends before enforcing it and rely on audience separation.
- Map failures to RFC 6750 (details in [resource servers](references/resource-server.md)):
  no credentials: `401` + `WWW-Authenticate: Bearer realm="..."`; rejected token (any
  `errors.JOSEError`): `401` + `error="invalid_token"`; missing scope: `403` +
  `error="insufficient_scope"`. Never answer 500 for a bad token, and never echo the token or the
  precise failure to the client.
- Scopes are a space-separated string in `scope`. Split and compare exactly: `'reports:readonly'`
  must not satisfy `reports:read`. Some IdPs use `scp` (string or array) instead.

oauth4webapi offers the same as one call, `validateJwtAccessToken(as, request, audience)`: it needs
a Fetch `Request`, requires `iss exp aud sub iat jti client_id`, checks `typ`, and caches the JWKS
for 5 min (refetch on unknown `kid` after 60 s).

## 4. Refreshing tokens (rotation, reuse detection, concurrency)

RFC 9700 makes rotation or sender-constraining mandatory for public clients' refresh tokens, and
many IdPs offer rotation for confidential clients too. With rotation, each refresh returns a
**new** refresh token, the old one dies, and presenting a used one again is treated as theft, so
the IdP revokes the whole grant. The classic bug is not the refresh call; it is everything around it.

1. **Store the new refresh token from every response**, atomically with the new access token and
   expiry. Keep the old one only when the response has no `refresh_token` (RFC 6749 section 6).
   Keep `id_token` too (refresh responses often omit it, and logout needs it).
2. **Refresh ahead of expiry**: compute `expiresAt = Date.now() + expires_in * 1000` when the
   response arrives (`tokens.expiresIn()`), refresh when less than 30-60 s remain.
3. **One refresh in flight per session.** A dashboard that fires `Promise.all` of three API calls,
   two tabs, or a retry loop will otherwise send the same refresh token twice; the second use trips
   reuse detection and logs the user out of everything. Share the in-flight promise per session
   key, remove it when it settles (success or failure), and **re-read the stored tokens inside the
   flight** so a caller that loaded the session before an earlier refresh finished does not send a
   rotated token.
4. **Classify failures.** `ResponseBodyError` with `err.error === 'invalid_grant'` means the grant
   is over (revoked, expired, reused): delete the session and send the user to sign in; never retry.
   Outages must keep the session (answer 503, let a later request retry): 5xx arrives as
   `ClientError` with `code: 'OAUTH_RESPONSE_IS_NOT_CONFORM'`, network failures as
   `TypeError: fetch failed`. A 401 with `WWW-Authenticate` (bad client credentials) arrives as
   `WWWAuthenticateChallengeError`: a configuration problem to alert on, not a reason to drop
   sessions.
5. With several app instances, the in-process map is not enough: use a short distributed lock
   keyed by session, or an IdP grace period for the previous refresh token, and re-read after
   acquiring the lock.

```ts
const inFlight = new Map<string, Promise<StoredTokens>>()

function freshTokens(key: string): Promise<StoredTokens> {
  let flight = inFlight.get(key)
  if (!flight) {
    flight = rotate(key).finally(() => inFlight.delete(key)) // failed flights are not cached
    inFlight.set(key, flight)
  }
  return flight
}

async function rotate(key: string): Promise<StoredTokens> {
  const current = await vault.read(key)                     // re-read inside the flight
  if (!current) throw new ReauthRequired('no session')
  if (current.expiresAt - SKEW_MS > Date.now()) return current // someone already refreshed
  try {
    const t = await oidc.refreshTokenGrant(await getIdp(), current.refreshToken)
    const next = {
      accessToken: t.access_token,
      refreshToken: t.refresh_token ?? current.refreshToken,
      idToken: t.id_token ?? current.idToken,
      expiresAt: Date.now() + (t.expiresIn() ?? 60) * 1000,
    }
    await vault.write(key, next)
    return next
  } catch (err) {
    if (err instanceof oidc.ResponseBodyError && err.error === 'invalid_grant') {
      await vault.remove(key)
      throw new ReauthRequired('sign in again', { cause: err })
    }
    throw new TransientIdpError('refresh failed', { cause: err }) // 503, keep the session
  }
}
```

express-session saves each request's own copy of the session; with `resave: true`, or when two
parallel requests both modify it, a stale copy can overwrite the rotated token (see its README on
`resave`). Keep rotating tokens in a store you update directly, and re-read before writing.

More patterns (per-session mutex, multi-instance locks, reactive refresh on 401, client
credentials caching, back-channel logout) are in [token lifecycle](references/token-lifecycle.md).

## 5. Logging out

- Destroy the server-side session (not only the cookie), then redirect to
  `oidc.buildEndSessionUrl(config, { id_token_hint, post_logout_redirect_uri })`; it adds
  `client_id`. The `post_logout_redirect_uri` must be registered at the IdP.
- Use `POST` for `/logout` from your own pages; optionally revoke the refresh token with
  `oidc.tokenRevocation(config, refreshToken)` if the IdP supports it.

## 6. Review checklist

Login (client):
- [ ] openid-client v6 API (no `Issuer`/`Client`/`generators`), `Configuration` discovered once.
- [ ] PKCE S256 on every request; `await calculatePKCECodeChallenge`; state and nonce per attempt.
- [ ] Pending attempt stored server-side or in a signed cookie, bound to the browser, deleted on
      first use, with a TTL.
- [ ] `currentUrl` built from the registered redirect URI plus the callback's query string.
- [ ] `expectedState`, `expectedNonce`, `pkceCodeVerifier` passed; `iss` left in the query.
- [ ] Session id regenerated after login; user taken from `tokens.claims()`.
- [ ] `allowInsecureRequests` only behind an explicit dev/test flag.
- [ ] `enableNonRepudiationChecks` if the ID token is kept as evidence or forwarded.

API (resource server):
- [ ] `jwtVerify` with `issuer`, `audience`, `algorithms`, `typ: 'at+jwt'`, `requiredClaims` with `exp`.
- [ ] JWKS URL from discovery, `createRemoteJWKSet` created once; no keys hard-coded or loaded only at startup.
- [ ] ID tokens and tokens for other audiences rejected; scopes split and matched exactly.
- [ ] 401/403 with RFC 6750 `WWW-Authenticate`; `JOSEError` never becomes a 500.
- [ ] No `decodeJwt`/`jwt.decode` result used before verification.

Refresh:
- [ ] Rotated refresh token stored on every refresh; `id_token` kept.
- [ ] One refresh in flight per session; tokens re-read inside it; rejected flights not cached.
- [ ] `invalid_grant` deletes the session (sign in again); outages keep it (503, retry later).
- [ ] Multi-instance deployments have a distributed lock or an IdP grace period.

## References

- [openid-client v6](references/openid-client-v6.md): v5 to v6 map, every function used above,
  error classes, custom fetch, timeouts, Passport.
- [Resource servers](references/resource-server.md): jose and oauth4webapi validation, JWKS
  caching and rotation, RFC 6750 responses, discovery pitfalls.
- [Token lifecycle](references/token-lifecycle.md): refresh patterns, client credentials, logout,
  what to store where.
- [Sources](references/sources.md): versions, specs and the behaviours verified by running them.
