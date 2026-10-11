---
name: jwt
description: JWT — structure, signing algorithms, refresh, security pitfalls.
---

# JWT (JSON Web Token)

## Structure

A JWT is three Base64URL-encoded segments separated by dots:

```
header.payload.signature
```

**Header**
```json
{ "alg": "HS256", "typ": "JWT" }
```

**Payload** (claims)
```json
{
  "sub": "user-uuid",
  "iss": "https://auth.example.com",
  "aud": "api.example.com",
  "exp": 1700000000,
  "iat": 1699996400,
  "jti": "unique-token-id",
  "email": "user@example.com",
  "role": "admin"
}
```

**Signature** — HMAC or RSA/ECDSA over `header.payload` using the signing key.

---

## Standard Claims (RFC 7519)

| Claim | Name | Required | Description |
|---|---|---|---|
| `iss` | Issuer | Recommended | Who issued the token |
| `sub` | Subject | Recommended | Who the token represents (user ID) |
| `aud` | Audience | Recommended | Who the token is intended for |
| `exp` | Expiration | **Required** | Unix timestamp — reject after this |
| `iat` | Issued At | Recommended | When it was issued |
| `nbf` | Not Before | Optional | Not valid before this timestamp |
| `jti` | JWT ID | Optional | Unique ID for this token (for revocation) |

Always validate `exp`. Validate `iss` and `aud` when the system has multiple token issuers or audiences.

---

## Signing Algorithms

| Algorithm | Type | When to use |
|---|---|---|
| `HS256` / `HS384` / `HS512` | Symmetric (shared secret) | Single service; secret never leaves the server |
| `RS256` / `RS384` / `RS512` | Asymmetric (RSA) | Multiple services; public key distributed for verification |
| `ES256` / `ES384` / `ES512` | Asymmetric (ECDSA) | Same as RS but smaller keys, faster |

**Default recommendation**: `HS256` for single-service systems, `RS256` or `ES256` when multiple services need to verify tokens independently.

**Never use `none` algorithm** — it disables signature verification entirely.

---

## Token Expiry & Refresh Strategy

Short-lived access tokens + long-lived refresh tokens:

| Token | Typical TTL | Where to store |
|---|---|---|
| Access token | 15 min – 1 hour | Memory (JS), `Authorization` header |
| Refresh token | 7–30 days | `httpOnly` secure cookie or secure storage |

**Refresh flow**:
1. Client sends expired access token (or proactively refreshes before expiry)
2. Server validates refresh token (check DB — is it still valid, not revoked?)
3. Server issues new access token (and optionally rotates the refresh token)
4. Client uses the new access token

**Refresh token rotation** (recommended): each use of a refresh token invalidates the old one and issues a new one. Detects stolen tokens — if a rotated token is used, revoke the entire session.

---

## Validation Checklist

Every JWT validation must check all of the following:

- [ ] Signature is valid (using the correct key and algorithm)
- [ ] `exp` is in the future
- [ ] `iat` is in the past (clock skew tolerance: ≤ 60 seconds)
- [ ] `iss` matches the expected issuer
- [ ] `aud` matches the expected audience (if used)
- [ ] Algorithm header matches what the server expects — **never accept `none`**
- [ ] Token is not on the revocation list (if implementing revocation)

---

## Implementation by Language

**Node.js / TypeScript**
```typescript
import jwt from 'jsonwebtoken'

// Sign
const token = jwt.sign(
  { sub: userId, role: 'user' },
  process.env.JWT_SECRET!,
  { expiresIn: '1h', issuer: 'api.example.com' }
)

// Verify — throws on invalid/expired
const payload = jwt.verify(token, process.env.JWT_SECRET!, {
  issuer: 'api.example.com',
  algorithms: ['HS256']
})
```

**Python**
```python
import jwt  # PyJWT

token = jwt.encode(
    {"sub": user_id, "exp": datetime.utcnow() + timedelta(hours=1)},
    settings.JWT_SECRET,
    algorithm="HS256"
)

payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
```

**Go**
```go
import "github.com/golang-jwt/jwt/v5"

token := jwt.NewWithClaims(jwt.SigningMethodHS256, jwt.MapClaims{
    "sub": userID,
    "exp": time.Now().Add(time.Hour).Unix(),
})
signed, _ := token.SignedString([]byte(os.Getenv("JWT_SECRET")))

// Verify
parsed, err := jwt.Parse(signed, func(t *jwt.Token) (interface{}, error) {
    if _, ok := t.Method.(*jwt.SigningMethodHMAC); !ok {
        return nil, fmt.Errorf("unexpected signing method")
    }
    return []byte(os.Getenv("JWT_SECRET")), nil
})
```

**PHP**
```php
use Firebase\JWT\JWT;
use Firebase\JWT\Key;

$token = JWT::encode(['sub' => $userId, 'exp' => time() + 3600], $_ENV['JWT_SECRET'], 'HS256');
$decoded = JWT::decode($token, new Key($_ENV['JWT_SECRET'], 'HS256'));
```

---

## Custom Claims

Add application-specific claims to the payload. Prefix custom claims to avoid collisions:

```json
{
  "sub": "user-uuid",
  "exp": 1700000000,
  "https://example.com/roles": ["admin", "editor"],
  "tenant_id": "acme-corp"
}
```

**Authorization decisions** must be based on claims set by the server, not user-supplied data. If claims are read from a user-controlled source, an attacker can elevate privileges.

---

## Revocation

JWTs are stateless — they're valid until `exp`. To revoke before expiry:

| Strategy | How |
|---|---|
| **Blocklist** | Store revoked `jti` values in Redis; check on each request |
| **Refresh token revocation** | Don't revoke access tokens — make them short-lived (≤15 min). Revoke refresh tokens in DB |
| **Secret rotation** | Rotate the signing secret — invalidates all tokens at once; use only for emergency |

Short-lived access tokens (15 min) make individual revocation largely unnecessary — prefer this over a blocklist for most use cases.

---

## Security Pitfalls

| Pitfall | Risk | Fix |
|---|---|---|
| Long-lived access tokens (days/weeks) | Stolen token stays valid forever | Keep to ≤ 1 hour |
| Storing JWT in `localStorage` | XSS can steal it | Use memory or `httpOnly` cookie |
| Accepting `none` algorithm | Auth bypass — no signature checked | Allowlist algorithms explicitly |
| Not validating `iss` / `aud` | Token from another service accepted | Always validate when multi-service |
| Sensitive data in payload | JWTs are not encrypted — anyone can decode | Never put passwords, PII, or secrets in payload |
| Weak secret (`secret123`) | Brute-forceable signature | Use ≥ 256-bit cryptographically random secret |
| Trusting user-supplied claims | Privilege escalation | Only trust claims from verified token, issued by known issuer |
