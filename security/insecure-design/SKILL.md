---
name: insecure-design
description: >
  Detect, analyze, and remediate OWASP A06:2025 Insecure Design vulnerabilities in Python web
  applications (FastAPI and Flask). Use this skill whenever the user asks about architecture-level
  security flaws, threat modeling, rate limiting gaps, business logic vulnerabilities, insecure file
  uploads, race conditions, tenant isolation failures, or client-side enforcement of server-side
  security. Trigger even if the user doesn't say "Insecure Design" explicitly — common signals
  include: "missing rate limiting", "file upload security", "business logic flaw", "race condition",
  "multi-tenant isolation", "threat modeling", "STRIDE", "design review", or "can users abuse this
  flow". Also trigger for code reviews or audits where architecture-level security controls are
  being evaluated, not just implementation bugs.
---

# OWASP A06:2025 — Insecure Design

## What This Skill Does

Guides detection, analysis, and remediation of **Insecure Design** vulnerabilities — architecture-level
failures where security controls are absent or structurally inadequate. Unlike implementation bugs,
insecure design **cannot be fixed by patching code alone**; it requires redesigning the flow or
adding missing control layers.

**OWASP 2025 position:** #6 (down from #4 in 2021, as threat modeling adoption has improved)  
**CWEs covered:** 39 | **Avg incidence:** 1.86%  
**Key CWEs:** CWE-434, CWE-269, CWE-362, CWE-799, CWE-602

---

## Core Concepts

### Design vs. Implementation
| Insecure Design (A06) | Implementation Bug (other categories) |
|---|---|
| Rate limiting never architected into login flow | Rate limiter present but misconfigured |
| File upload stored in web root by design | Upload handler missing extension check |
| No tenant isolation in multi-tenant DB schema | Query missing WHERE clause |
| Business logic allows negative quantities | Missing server-side input validation |

A design flaw requires **adding a new control** or **refactoring the architecture**, not just
patching existing code.

---

## Testing Checklist for FastAPI / Flask

### 1. Rate Limiting (CWE-799)
Verify that login, registration, password reset, and high-value transaction endpoints enforce rate limits.

**FastAPI — SlowAPI:**
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/login")
@limiter.limit("5/minute")
async def login(request: Request, ...): ...
```

**Flask — Flask-Limiter:**
```python
from flask_limiter import Limiter
limiter = Limiter(app, key_func=get_remote_address)

@app.route("/login", methods=["POST"])
@limiter.limit("5 per minute")
def login(): ...
```

**Red flags to flag in review:**
- Login, `/register`, `/reset-password`, `/checkout` routes with no rate-limiting decorator
- `RATELIMIT_ENABLED = False` or limiter initialized without being applied to sensitive routes
- Rate limits too permissive (e.g., `1000/minute` on auth endpoints)

---

### 2. File Upload Security (CWE-434)
File uploads must be validated by **content**, not just extension, and stored **outside the web root**.

```python
import magic  # python-magic

ALLOWED_MIME = {"image/jpeg", "image/png", "application/pdf"}
MAX_SIZE = 5 * 1024 * 1024  # 5 MB

@app.post("/upload")
async def upload(file: UploadFile):
    content = await file.read(MAX_SIZE + 1)
    if len(content) > MAX_SIZE:
        raise HTTPException(400, "File too large")
    mime = magic.from_buffer(content[:2048], mime=True)
    if mime not in ALLOWED_MIME:
        raise HTTPException(400, "Unsupported file type")
    # Store in /var/app/uploads/ — NOT inside static/ or public/
    safe_path = UPLOAD_DIR / secrets.token_hex(16)
    safe_path.write_bytes(content)
```

**Red flags:**
- Relying on `file.content_type` or extension alone (`filename.endswith(".jpg")`)
- Storing uploads in `static/`, `public/`, or any web-accessible path
- No file size cap
- Serving uploaded files via direct URL without authentication

---

### 3. Business Logic Flaws
Business logic flaws are application-specific — they exploit valid flows in unintended ways.

**Common patterns to test:**

| Scenario | Test |
|---|---|
| Negative quantity in cart | POST with `quantity: -1`, verify order total doesn't go negative |
| Price manipulation | POST with a `price` field — verify server ignores client-supplied price |
| Concurrent purchase race | Parallel requests to buy last item — verify only one succeeds |
| Booking system abuse | Book same slot twice in parallel |
| Coupon reuse | Apply same coupon twice before first transaction commits |

**FastAPI example — safe quantity handling:**
```python
class OrderItem(BaseModel):
    product_id: int
    quantity: int = Field(..., ge=1, le=100)  # enforced server-side
```

**Red flags:**
- Price, discount, or role fields accepted from client payload
- No idempotency key or duplicate-check on financial transactions
- Quantity or amount not bounded with `ge=1` in Pydantic or equivalent

---

### 4. Tenant Isolation (CWE-269)
In multi-tenant apps, every DB query must scope to the authenticated tenant.

**Pattern to enforce:**
```python
# UNSAFE — returns data across all tenants
def get_reports(db: Session):
    return db.query(Report).all()

# SAFE — scoped to current tenant
def get_reports(db: Session, current_user: User):
    return db.query(Report).filter(Report.tenant_id == current_user.tenant_id).all()
```

**Red flags:**
- Any `db.query(Model).all()` without tenant/user filter
- Admin-like queries reachable from user-facing endpoints
- Tenant ID passed in request body (must come from JWT/session, not user input)

---

### 5. Client-Side Enforcement of Server-Side Security (CWE-602)
Security enforced only in the browser is trivially bypassed via direct API calls.

**Red flags:**
- Authorization check only in JavaScript / frontend, not in the API route
- Hidden form fields controlling price, role, or access level
- Feature flags based on client-provided values (use JWT claims or server session)

```python
# WRONG — trusting client-supplied role
@app.post("/admin/action")
async def admin_action(role: str = Body(...)):  # never do this
    if role == "admin":
        ...

# CORRECT — derive from authenticated token
@app.post("/admin/action")
async def admin_action(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(403)
    ...
```

---

### 6. Credential / Account Recovery Design
Insecure recovery flows are a design flaw, not an implementation bug.

**Red flags:**
- Knowledge-based security questions (mother's maiden name, pet name) — guessable from social media
- Password reset link not expiring within 15–60 minutes
- Reset token sent over HTTP or stored without hashing
- Account enumeration possible via reset flow ("no account found" vs. silent success)

**Safe pattern:**
```python
# Generate short-lived, single-use, high-entropy token
token = secrets.token_urlsafe(32)
expiry = datetime.utcnow() + timedelta(minutes=30)
# Store hash of token, not the token itself
db_token = PasswordResetToken(
    user_id=user.id,
    token_hash=hashlib.sha256(token.encode()).hexdigest(),
    expires_at=expiry,
    used=False
)
```

---

## Threat Modeling Guidance (STRIDE)

Use STRIDE to find design flaws before they reach code:

| Threat | Applies to | Example in FastAPI/Flask |
|---|---|---|
| **S**poofing | Auth flows | Predictable session tokens, missing MFA |
| **T**ampering | Data in transit/storage | Missing HMAC on signed data, writable uploads |
| **R**epudiation | Audit logs | Missing request logging on financial actions |
| **I**nformation Disclosure | Error messages, API docs | `/docs` open in prod, stack traces in 500 |
| **D**enial of Service | Rate limiting, resource use | No request size cap, missing rate limiter |
| **E**levation of Privilege | Authorization design | Client-supplied role, missing tenant scope |

---

## Remediation Priority Matrix

| Finding | Severity | Fix complexity |
|---|---|---|
| No rate limiting on auth/payment endpoints | High | Low — add SlowAPI/Flask-Limiter |
| File uploads stored in web root | High | Medium — move storage path, add serving layer |
| Client-supplied price/role fields | Critical | Low — remove field from request model |
| Missing tenant scope on DB queries | Critical | Medium — audit all queries |
| Knowledge-based security questions | Medium | High — redesign recovery flow |
| Race condition on inventory/booking | Medium | High — add DB-level locking or idempotency |

---

## Reference Material

For deeper dives, see:
- `references/cwe-details.md` — full CWE descriptions and examples for all 39 CWEs in A06
- `references/threat-modeling.md` — STRIDE worksheet template for FastAPI/Flask apps

For related OWASP categories that overlap with design issues:
- **A01 Broken Access Control** — when the design grants too much access by default
- **A07 Authentication Failures** — when auth flow design is the root cause
- **A10 Mishandling of Exceptional Conditions** — when error recovery design fails closed