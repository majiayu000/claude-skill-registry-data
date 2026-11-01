---
name: security-audit
description: Security Audit Engineer — Institutional capability and runbook for security-audit.
---

# SKILL: Security Audit Engineer
## Domain: Authentication, Authorization, API Security, Data Protection

**Activation triggers:** new auth flow, permission check, credential storage,
OAuth implementation, CORS config, rate limiting, security review.

---

## Auth Security Checklist

```
Authentication:
  [ ] JWT access tokens expire in 30 minutes max
  [ ] Refresh tokens rotate on every use (single-use)
  [ ] Refresh tokens stored as SHA-256 hashes (never plaintext)
  [ ] bcrypt password hashing (cost ≥ 12)
  [ ] Account lockout after N failed attempts (configurable)
  [ ] Locked_until timestamp cleared only on successful auth
  [ ] OAuth codes exchanged immediately (single-use, short TTL)
  [ ] email_verified enforced for sensitive operations

Authorization:
  [ ] Every protected endpoint has Depends(get_current_active_user)
  [ ] Admin endpoints additionally require role check
  [ ] Resource ownership verified before returning data
  [ ] RBAC permissions cached but refreshed on role change
```

---

## CORS Configuration Rules

```python
# CORRECT: origins from environment, never hardcoded
app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(o) for o in settings.BACKEND_CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# .env (dev)
BACKEND_CORS_ORIGINS=["http://localhost:5173","http://localhost:3000"]

# .env (prod)
BACKEND_CORS_ORIGINS=["https://integralmarket.com","https://app.integralmarket.com"]

# WRONG: hardcoded in source
allow_origins=["http://localhost:5173"]  # never commit this
allow_origins=["*"]  # never use wildcard in production
```

---

## Credential Encryption

```python
# Broker credentials stored encrypted with Fernet (AES-256-CBC + HMAC-SHA256)
from cryptography.fernet import Fernet

def encrypt_credentials(creds: dict, key: str) -> dict:
    fernet = Fernet(key.encode())
    token = fernet.encrypt(json.dumps(creds).encode()).decode()
    return {"encrypted": token}

def decrypt_credentials(stored: dict, key: str) -> dict:
    fernet = Fernet(key.encode())
    return json.loads(fernet.decrypt(stored["encrypted"].encode()))

# ENCRYPTION_KEY in .env — generate with:
# python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

---

## Rate Limiting Tiers

```python
# Market backend security_and_metrics_middleware
RATE_LIMITS = {
    "/auth/login":     (20, 300),    # 20 requests per 5 minutes (brute force protection)
    "/auth/register":  (20, 300),
    "/auth/oauth":     (20, 300),
    "/auth/refresh":   (120, 60),
    "/auth/me":        (120, 60),
    "/upload":         (10, 60),
    "default":         (100, 60),
}
```

---

## SQL Injection Prevention

```python
# ALWAYS use parameterized queries
# CORRECT:
result = await db.execute(
    text("SELECT * FROM iam.users WHERE email = :email AND deleted_at IS NULL"),
    {"email": email.lower()},
)

# WRONG:
result = await db.execute(f"SELECT * FROM iam.users WHERE email = '{email}'")

# ALSO WRONG (ORM without params):
result = await db.execute(
    text(f"SELECT * FROM iam.users WHERE email = '{user_input}'")
)
```

---

## Security Headers

```python
# All responses should include these headers
SECURITY_HEADERS = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "X-XSS-Protection": "1; mode=block",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "Permissions-Policy": "camera=(), microphone=(), geolocation=()",
    # Content-Security-Policy: configure per environment
}
```

---

## OAuth Security Rules

```python
# 1. State parameter prevents CSRF
params = {"state": "google", "nonce": secrets.token_urlsafe(16), ...}

# 2. Redirect URI must match exactly registered URI
redirect_uri = settings.GOOGLE_REDIRECT_URI  # from env, never from request

# 3. Code exchange catches ALL exceptions, not just ValueError
try:
    oauth_info = await OAuthService.get_google_user_info(code=data.code)
except httpx.TimeoutException:
    raise HTTPException(503, "OAuth provider timeout")
except httpx.ConnectError:
    raise HTTPException(503, "Cannot reach OAuth provider")
except ValueError as e:
    raise HTTPException(400, f"OAuth failed: {e}")
# Any other exception propagates to global_exception_handler → 500 JSON
```

---

## Anti-Patterns

```
✗ Wildcard CORS (*) in production
✗ Storing refresh tokens plaintext (hash with SHA-256)
✗ Missing account lockout (enables brute force)
✗ OAuth redirect_uri from request body (open redirect vulnerability)
✗ JWT without expiry
✗ Missing ownership check (user A reading user B's data)
✗ Logging credentials or tokens (PII/secret exposure)
✗ Single-point exception handler hiding errors silently
✗ Admin endpoints without role verification
```
