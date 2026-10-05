---
name: authentication-failures
description: >
  Use this skill whenever you need to audit, test, or fix Authentication Failures
  (OWASP A07:2025) in Python web applications — especially FastAPI and Flask. Triggers
  include: any mention of JWT security, session management, brute force protection,
  credential stuffing, password policy, MFA enforcement, login rate limiting, session
  fixation, token validation, or auth-related error messages. Also trigger for requests
  to "check authentication", "audit login flows", "test auth security", "find auth bugs",
  or any task involving CWEs: CWE-287, CWE-307, CWE-384, CWE-521, CWE-798, CWE-613.
  Use proactively whenever the user shares auth-related code (routes, middleware,
  decorators, token handlers) even if they haven't explicitly mentioned security testing.
---

# Authentication Failures — OWASP A07:2025

**Rank:** #7 (stable) | **CWEs covered:** 36 | **Occurrences:** 1.1 million+
**New 2025 threat:** Hybrid password attacks / password spray — attackers increment
leaked credentials (e.g., `Password1!` → `Password2!`).

---

## What This Skill Covers

Authentication Failures occur when an application's identity verification mechanisms
are absent, weak, or bypassable. Key attack patterns:

- **Credential stuffing / brute force** — automated login attempts using leaked creds
- **Weak/default passwords** — accounts created with guessable or known-breached passwords
- **Insecure credential recovery** — password reset flows that leak information or are bypassable
- **Missing or bypassed MFA** — no second factor, or MFA that can be skipped
- **Exposed session identifiers** — tokens in URLs, logs, or referrer headers
- **Session fixation** — attacker sets a known session ID before authentication
- **Improper session invalidation** — sessions that survive logout or token revocation

---

## Testing Checklist for FastAPI & Flask

Work through each section systematically. Mark ✓ pass, ✗ fail, N/A where not applicable.

### 1. JWT Implementation

```python
# ✓ GOOD — short-lived tokens, claim validation
token = jwt.encode(
    {"sub": user_id, "exp": datetime.utcnow() + timedelta(minutes=15),
     "iss": "myapp", "aud": "myapp-client"},
    settings.SECRET_KEY, algorithm="HS256"
)
jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"],
           audience="myapp-client", issuer="myapp")

# ✗ BAD — no expiry, no claim validation, accepts any algorithm
jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256", "RS256", "none"])
```

**Checks:**
- [ ] Access tokens expire in 15–30 minutes
- [ ] Refresh tokens rotate on use and are invalidated on logout
- [ ] `aud` (audience) and `iss` (issuer) claims are set AND verified on decode
- [ ] Algorithm is pinned to an explicit list — never include `"none"`
- [ ] JWT secret loaded from `os.environ`, minimum 32 characters
- [ ] Algorithm confusion attack prevented: RS256 keys never accepted as HS256 secrets

### 2. Rate Limiting on Auth Endpoints

```python
# FastAPI — slowapi
from slowapi import Limiter
from slowapi.util import get_remote_address
limiter = Limiter(key_func=get_remote_address)

@app.post("/login")
@limiter.limit("5/minute")          # ✓ per-IP rate limit
async def login(request: Request, credentials: LoginSchema):
    ...

# Flask — Flask-Limiter
from flask_limiter import Limiter
limiter = Limiter(app, key_func=get_remote_address, default_limits=["200/day"])

@app.route("/login", methods=["POST"])
@limiter.limit("5 per minute")      # ✓
def login():
    ...
```

**Checks:**
- [ ] Login endpoint rate-limited (≤5–10 attempts/minute per IP)
- [ ] Per-account lockout after repeated failures (not just per-IP)
- [ ] Registration and password-reset endpoints also rate-limited
- [ ] Rate limit responses return `429 Too Many Requests`, not `401`

### 3. Password Policy & Breached-Password Checking

```python
# ✓ GOOD — check against breached databases
import hashlib, httpx

def is_pwned(password: str) -> bool:
    sha1 = hashlib.sha1(password.encode()).hexdigest().upper()
    prefix, suffix = sha1[:5], sha1[5:]
    resp = httpx.get(f"https://api.pwnedpasswords.com/range/{prefix}")
    return suffix in resp.text

# ✓ GOOD — enforce minimum complexity
def validate_password(password: str):
    if len(password) < 12:
        raise ValueError("Password must be at least 12 characters")
    if is_pwned(password):
        raise ValueError("Password found in known data breach")
```

**Checks:**
- [ ] Minimum length enforced (NIST 800-63b recommends ≥8; prefer ≥12)
- [ ] Check against known-breached passwords (HaveIBeenPwned API or local list)
- [ ] **Do NOT force periodic rotation** (NIST 800-63b deprecates this)
- [ ] Password screened against top-10,000 worst passwords list
- [ ] No maximum password length below 64 characters

### 4. Session Management (Flask)

```python
# ✓ GOOD — Flask-Login with secure session config
app.config.update(
    SESSION_COOKIE_SECURE=True,       # HTTPS only
    SESSION_COOKIE_HTTPONLY=True,     # no JS access
    SESSION_COOKIE_SAMESITE='Lax',    # CSRF mitigation
    PERMANENT_SESSION_LIFETIME=timedelta(hours=1),
)

@app.route("/logout")
@login_required
def logout():
    logout_user()           # ✓ invalidates session
    session.clear()         # ✓ belt-and-suspenders
    return redirect("/login")
```

**Checks:**
- [ ] `Flask-Login` or `Flask-Security-Too` in use (no hand-rolled session management)
- [ ] Session invalidated on logout (both server-side and cookie cleared)
- [ ] Session ID regenerated after successful login (prevents fixation)
- [ ] `SESSION_COOKIE_SECURE`, `SESSION_COOKIE_HTTPONLY`, `SESSION_COOKIE_SAMESITE` all set
- [ ] Session lifetime is bounded; idle sessions expire

### 5. Error Message Enumeration

```python
# ✗ BAD — reveals which field was wrong
if not user:
    return {"error": "Username not found"}
if not verify_password(password, user.hashed_password):
    return {"error": "Incorrect password"}

# ✓ GOOD — generic message regardless of failure reason
if not user or not verify_password(password, user.hashed_password):
    return JSONResponse({"error": "Invalid credentials"}, status_code=401)
```

**Checks:**
- [ ] Auth failures always return identical message: `"Invalid credentials"` (or equivalent)
- [ ] HTTP status codes consistent: don't return `404` for missing users vs `401` for bad password
- [ ] Password reset flow doesn't confirm whether email is registered
- [ ] Response timing is constant (use `hmac.compare_digest` and always hash even for unknown users)

### 6. Default Credentials & Hard-coded Secrets

```python
# ✗ BAD — Bandit will flag these
ADMIN_PASSWORD = "admin"
TEST_USER = {"username": "test", "password": "test123"}
JWT_SECRET = "supersecretkey"

# ✓ GOOD
JWT_SECRET = os.environ["JWT_SECRET"]  # loaded from environment / secrets manager
```

**Checks:**
- [ ] Run Bandit: `bandit -r . -t B105,B106,B107` (hardcoded password checks)
- [ ] No `admin/admin`, `test/test`, `root/root` patterns in config, seeds, or fixtures
- [ ] All secrets loaded from environment variables or a secrets manager (Vault, AWS SSM)
- [ ] `.env` files excluded from version control via `.gitignore`

### 7. MFA Enforcement

**Checks:**
- [ ] MFA offered for all user accounts; enforced for admin/privileged roles
- [ ] MFA cannot be bypassed by manipulating URL parameters or session state
- [ ] TOTP codes are single-use and expire after 30 seconds (standard TOTP)
- [ ] Recovery codes are single-use and stored as hashed values

---

## Key CWEs Reference

| CWE | Name | Typical Finding |
|-----|------|-----------------|
| CWE-287 | Improper Authentication | Missing auth check, bypassable auth |
| CWE-307 | Unrestricted Auth Attempts | No rate limit on login endpoint |
| CWE-384 | Session Fixation | Session ID not regenerated post-login |
| CWE-521 | Weak Password Requirements | No minimum length/complexity enforced |
| CWE-798 | Hard-coded Credentials | Secrets in source code |
| CWE-613 | Insufficient Session Expiration | Sessions survive logout; no timeout |

---

## Automated Scanning Commands

```bash
# Static analysis — catches CWE-798, weak crypto, debug mode
bandit -r . -ll -ii

# Specifically target hardcoded credentials
bandit -r . -t B105,B106,B107,B108

# Dependency vulnerabilities (may expose auth libraries with known CVEs)
pip-audit
safety check

# Check JWT library versions for known vulns
pip show python-jose PyJWT authlib
```

---

## Remediation Priority Order

1. **Critical:** JWT algorithm confusion / `"none"` accepted → immediate fix
2. **Critical:** No rate limiting on login → add `slowapi`/`Flask-Limiter` immediately
3. **High:** Hard-coded secrets in source → move to environment variables
4. **High:** Sessions not invalidated on logout → fix session management
5. **Medium:** Username enumeration via error messages → unify error responses
6. **Medium:** No breached-password check → integrate HaveIBeenPwned API
7. **Low:** Missing MFA option → plan rollout for privileged accounts first

---

## References

- OWASP A07:2025 full spec: https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/
- NIST SP 800-63b (Digital Identity Guidelines): https://pages.nist.gov/800-63-3/sp800-63b.html
- HaveIBeenPwned API: https://haveibeenpwned.com/API/v3