---
name: oauth-jwt-auth
description: >
  Architect, implement, and audit OAuth 2.0, OpenID Connect (OIDC), and JSON Web Token
  (JWT) authentication and authorization systems. Use when securing API endpoints,
  implementing Authorization Code with PKCE, validating JWT signatures via JWKS,
  configuring token lifetimes, enforcing CSRF protections, or designing secure token
  storage and revocation strategies.
compatibility: >
  Agent Skills-compatible coding agents operating across web, backend, and API gateway
  environments with access to cryptographic and HTTP libraries. Tooling is required only
  for executable validation.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "oauth2, oidc, jwt, authentication, authorization, pkce, jwks, tokens, security, csrf"
  topics: "security"
---

# OAuth 2.0, OIDC & JWT Security Architecture

Modern web and microservice architectures rely on OAuth 2.0 for delegated authorization, OpenID Connect (OIDC) for identity federation, and JSON Web Tokens (JWT) for compact, stateless credential transmission. Ensuring system security requires strict adherence to cryptographic verification, algorithm pinning, token lifetime boundaries, and defensible storage practices.

## Purpose & Overview

Authentication flaws represent critical vulnerabilities, leading directly to account takeover, horizontal and vertical privilege escalation, and data exfiltration. Misconfigured token issuance, improper validation (such as allowing the `none` algorithm or accepting mismatched audiences), and vulnerable storage mechanisms (such as unencrypted `localStorage`) routinely undermine otherwise secure applications.

This skill equips agents with principles and patterns to:
- Select and implement appropriate OAuth 2.0 grant types (Authorization Code with PKCE, Client Credentials, Refresh Token).
- Differentiate the lifecycles and scopes of **Identity Tokens (ID Tokens)**, **Access Tokens**, and **Refresh Tokens**.
- Perform rigorous cryptographic JWT validation: signature verification via remote JSON Web Key Sets (JWKS), algorithm pinning, issuer (`iss`) and audience (`aud`) checks, and clock skew mitigation.
- Store client-side tokens securely against Cross-Site Scripting (XSS) and Cross-Site Request Forgery (CSRF).
- Implement token introspection (RFC 7662) and low-latency token revocation via distributed blocklists.

---

## Core Principles & Rules

1. **Always Use PKCE for Authorization Code Flow**: Proof Key for Code Exchange (RFC 7636) is mandatory for both Single Page Applications (SPAs), mobile clients, and confidential server-rendered clients to prevent authorization code interception attacks.
2. **Never Use Deprecated Flows**: The OAuth 2.0 Implicit Grant (`response_type=token`) and Resource Owner Password Credentials (ROPC) grant are deprecated by OAuth 2.1 and must never be implemented in new architectures.
3. **Explicitly Pin Permitted Signature Algorithms**: When validating JWTs, never rely on the `alg` header supplied by the untrusted incoming token. Explicitly whitelist expected algorithms (e.g., `RS256`, `ES256`, or `EdDSA`) to prevent algorithm substitution attacks (such as the `none` vulnerability or asymmetric key confusion with `HS256`).
4. **Enforce Strict Claims Validation**:
   - `iss` (Issuer): Must match the expected identity provider URL byte-for-byte with HTTPS.
   - `aud` (Audience): Must contain the specific identifier of the resource server.
   - `exp` (Expiration): Reject expired tokens, allowing a maximum clock skew of 30 to 60 seconds.
5. **Separate ID Tokens from Access Tokens**: ID Tokens are meant strictly for the client application to read user profile information. Never pass an ID Token in the `Authorization: Bearer` header to authenticate API requests; only Access Tokens are valid API credentials.
6. **Never Store Refresh or Access Tokens in `localStorage`**: Tokens stored in `localStorage` or `sessionStorage` are accessible to any script executing in the document origin (XSS vulnerability). Store tokens in `HttpOnly`, `Secure`, `SameSite=Strict` (or `Lax`) cookies or hold short-lived access tokens exclusively in memory.

---

## Standard Workflows & Procedures

### Workflow 1: Authorization Code Flow with PKCE (RFC 7636)

```
Client (SPA/Native)               Authorization Server              Resource API
       │                                   │                              │
 1. Generate code_verifier &               │                              │
    code_challenge = SHA256(verifier)      │                              │
       │                                   │                              │
 2. GET /authorize?code_challenge=...─────►│                              │
       │                                   │ (User logs in & consents)    │
 3. Redirect back with auth code ◄─────────│                              │
       │                                   │                              │
 4. POST /token + code + code_verifier ───►│                              │
       │                                   │ (Verifies challenge == hash) │
 5. Return access_token & refresh_token ───│                              │
       │                                                                  │
 6. GET /api/v1/resource with Bearer Token ──────────────────────────────►│
       │                                                                  │ (Validates JWT)
 7. Protected Data Response ◄─────────────────────────────────────────────│
```

1. **Client generates PKCE cryptographic parameters**:
   - Create a cryptographically random string (43 to 128 characters) for `code_verifier`.
   - Compute `code_challenge = BASE64URL(SHA256(code_verifier))`.
   - Generate a random `state` parameter and bind it to client session storage to defend against CSRF.
2. **Redirect to authorization server**:
   ```
   GET /authorize?
     response_type=code
     &client_id=my-client-app
     &redirect_uri=https%3A%2F%2Fapp.example.com%2Fcallback
     &scope=openid%20profile%20email%20read%3Aorders
     &state=c5b70a83e742
     &code_challenge=E9Melhoa2OwvFrEMTJguCHaoeK1t8URWbuGJSstw-cM
     &code_challenge_method=S256
   ```
3. **Exchange authorization code at token endpoint**:
   ```http
   POST /oauth/token HTTP/1.1
   Host: auth.example.com
   Content-Type: application/x-www-form-urlencoded

   grant_type=authorization_code
   &client_id=my-client-app
   &code=SplxlOBeZQQYbYS6WxSbIA
   &redirect_uri=https%3A%2F%2Fapp.example.com%2Fcallback
   &code_verifier=dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk
   ```

### Workflow 2: Cryptographic JWT Signature & Claims Validation

When a Resource Server receives an incoming request containing an `Authorization: Bearer <token>` header:

```
Extract Bearer Token
       │
       ▼
Decode Header & Extract Key ID (`kid`)
       │
       ▼
Fetch Matching Public Key from JWKS Cache (refresh on unknown kid)
       │
       ▼
Verify Cryptographic Signature (Enforce pinned algorithm, e.g., RS256)
       │
       ▼
Validate Claims (`iss`, `aud`, `exp` with clock skew <= 60s, `nbf`)
       │
       ▼
Check Token Revocation / Revocation Blocklist
       │
       ▼
Grant Access & Bind Claims to Request Context
```

1. **Public Key Retrieval & Caching**: Cache the JWKS (`/.well-known/jwks.json`) in memory with an expiration (e.g. 1 hour). If a token presents an unknown `kid`, fetch the updated keyset once to support seamless key rotation.
2. **Algorithm Pinning**: Strictly restrict parsing to the asymmetric algorithm configured for the realm (e.g., `RS256`, `ES256`).
3. **Claims Verification**:
   - Confirm `token.payload.iss == expected_issuer`.
   - Confirm `token.payload.aud == expected_audience` (or contains it if `aud` is an array).
   - Confirm `token.payload.exp > current_timestamp - max_clock_skew`.

---

## Real-World Examples & Patterns

### Pattern 1: Node.js/TypeScript Secure JWT Middleware (`jose`)

Using the standard, dependency-free `jose` library with remote JWKS caching and strict claim constraints:

```typescript
import { Request, Response, NextFunction } from 'express';
import { createRemoteJWKSet, jwtVerify, JWTVerifyOptions } from 'jose';

// Configuration parameters
const ISSUER_URL = 'https://auth.example.com/';
const AUDIENCE = 'https://api.example.com';
const JWKS_URI = new URL('.well-known/jwks.json', ISSUER_URL);

// In-memory caching JWKS client with automatic key rotation support
const JWKS = createRemoteJWKSet(JWKS_URI, {
  cooldownDuration: 30000, // 30s rate limit on fetching new unknown keys
  cacheMaxAge: 600000,     // 10 minutes cache
});

const VERIFY_OPTIONS: JWTVerifyOptions = {
  issuer: ISSUER_URL,
  audience: AUDIENCE,
  algorithms: ['RS256'], // Algorithm Pinning: reject HS256, none, etc.
  clockTolerance: 30,    // 30 seconds clock skew tolerance
};

export interface AuthenticatedUser {
  sub: string;
  scope: string;
  roles: string[];
}

export async function authenticateJwt(req: Request, res: Response, next: NextFunction) {
  const authHeader = req.headers.authorization;
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return res.status(401).json({ error: 'Missing or malformed Authorization header' });
  }

  const token = authHeader.substring(7);

  try {
    const { payload } = await jwtVerify(token, JWKS, VERIFY_OPTIONS);

    // Attach validated identity to request context
    (req as any).user = {
      sub: payload.sub as string,
      scope: (payload.scope as string) || '',
      roles: (payload['https://example.com/roles'] as string[]) || [],
    };

    return next();
  } catch (err: any) {
    // Return generic error to client, avoiding leaking cryptographic internals
    return res.status(401).json({ error: 'Invalid or expired token', code: err.code });
  }
}
```

### Pattern 2: Token Storage via Secure, SameSite Cookies

For Single Page Applications communicating with a backend API on the same parent domain, store the refresh token (or session token) in a secure cookie:

```typescript
// Setting secure session cookie on token refresh/login
res.cookie('refresh_token', refreshToken, {
  httpOnly: true,        // Prevents JavaScript access via document.cookie (Anti-XSS)
  secure: true,          // Enforces transmission only over HTTPS
  sameSite: 'strict',    // Prevents cross-site cookie transmission (Anti-CSRF)
  path: '/api/v1/auth',  // Restricts cookie scope only to the auth renewal endpoint
  maxAge: 7 * 24 * 60 * 60 * 1000, // 7 days in milliseconds
});
```

### Pattern 3: Client Credentials Grant for Machine-to-Machine (M2M)

Used strictly for service-to-service communication without an end-user context:

```python
import time
import requests

class ServiceTokenClient:
    def __init__(self, token_url: str, client_id: str, client_secret: str, audience: str):
        self.token_url = token_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.audience = audience
        self._cached_token = None
        self._expires_at = 0

    def get_token(self) -> str:
        # Return cached token if valid for at least another 60 seconds
        if self._cached_token and time.time() < (self._expires_at - 60):
            return self._cached_token

        response = requests.post(
            self.token_url,
            data={
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "audience": self.audience,
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()

        self._cached_token = data["access_token"]
        self._expires_at = time.time() + data.get("expires_in", 3600)
        return self._cached_token
```

---

## Common Anti-Patterns & Pitfalls

| Anti-Pattern | Operational Hazard | Correct Engineering Approach |
|:---|:---|:---|
| **Accepting `alg: none`** | Attackers forge unsigned tokens containing administrative claims (`"role": "admin"`). | Explicitly pin expected algorithms in the verification options (`algorithms: ['RS256']`). |
| **Storing tokens in `localStorage`** | Any XSS vulnerability (e.g., third-party script injection) allows complete token exfiltration. | Store sensitive tokens in `HttpOnly`, `Secure`, `SameSite` cookies or memory. |
| **Using symmetric HMAC (`HS256`) with public keys** | If an API server validates an RSA-signed token with `HS256`, an attacker can sign the token using the public RSA key as the HMAC secret. | Never use symmetric verification when the identity provider publishes public keys. |
| **Allowing unbounded token lifetimes** | Long-lived access tokens (e.g. 30 days) cannot be revoked if compromised without expensive state checks. | Issue short-lived access tokens (5-15 mins) and refresh via rolling refresh tokens. |
| **Omission of Audience (`aud`) validation** | A token issued for a third-party service (e.g., Analytics) can be replayed against your Core API. | Reject any token whose `aud` claim does not explicitly match your API identifier. |
| **Using ID Tokens for API Authorization** | ID Tokens lack audience and scope boundaries suited for resource servers, causing privilege confusion. | Use Access Tokens for APIs; reserve ID Tokens for user profiling within the client. |

---

## Verification Checklist

- [ ] Deprecated grant types (Implicit Grant, Resource Owner Password Credentials) are eliminated.
- [ ] Authorization Code flow strictly enforces PKCE (`code_challenge_method: 'S256'`).
- [ ] JWT signature verification explicitly pins allowed algorithms (e.g., `RS256`, `ES256`).
- [ ] Issuer (`iss`) and Audience (`aud`) claims are checked against exact string matches.
- [ ] Expiration (`exp`) claim is checked with a maximum clock tolerance of 60 seconds.
- [ ] JWKS keys are fetched over HTTPS, cached in-memory, and refreshed on unknown `kid`.
- [ ] Access token lifetime is configured to 5-15 minutes; Refresh tokens are rotated on every use.
- [ ] Refresh tokens are stored in `HttpOnly`, `Secure`, `SameSite` cookies with restricted path scopes.
- [ ] CSRF protections (SameSite cookies or anti-CSRF synchronizer tokens) are active on mutation endpoints.
- [ ] Revoked tokens or logout events invalidate the refresh token family and update session stores.

---

## Tooling & Reference Guides

- **RFC 6749 & RFC 6750**: The OAuth 2.0 Authorization Framework and Bearer Token Usage specifications.
- **RFC 7519**: JSON Web Token (JWT) specification.
- **RFC 7636**: Proof Key for Code Exchange by OAuth Public Clients (PKCE).
- **RFC 8414 & OpenID Connect Discovery**: OAuth 2.0 Authorization Server Metadata and JWKS resolution.
- **jose (Universal JavaScript)**: Modern, standards-compliant, zero-dependency JWT/JWS/JWE library.
- **PyJWT**: Python implementation of RFC 7519 with JWKS integration.
- **OWASP JWT Cheat Sheet**: Authoritative security recommendations for token issuance and storage.
