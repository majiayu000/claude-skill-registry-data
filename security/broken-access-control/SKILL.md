---
name: broken-access-control
description: >
  Security testing skill for A01:2025 Broken Access Control — the #1 OWASP risk for two consecutive cycles.
  Use this skill whenever the user asks about: access control vulnerabilities, IDOR (insecure direct object
  references), authorization bugs, SSRF testing, CORS misconfiguration, privilege escalation, JWT/session
  manipulation, CSRF protection, or auditing FastAPI/Flask endpoints for missing auth guards.
  Also trigger when the user says "test my API for access control", "check authorization", "find IDOR bugs",
  "review permissions", "audit my routes", or mentions CWE-284, CWE-285, CWE-352, CWE-639, CWE-862, or CWE-918.
---

# Broken Access Control (A01:2025)

**The #1 OWASP risk for two consecutive cycles.** Found in **3.74% of applications** with over **1.8 million occurrences** and **32,654 CVEs**. Access control enforces that users cannot act outside their intended permissions. Failures lead to unauthorized data disclosure, modification, or destruction.

> For deep reference on all CWEs and remediation patterns, see `references/bac-detail.md`.

---

## What This Skill Covers

| Sub-category | Description | Key CWEs |
|---|---|---|
| Missing Authorization | Routes/endpoints with no auth guard | CWE-862, CWE-284 |
| IDOR | Resource ownership not verified | CWE-639, CWE-285 |
| CORS Misconfiguration | Wildcard or overly-permissive origins | CWE-284 |
| SSRF | Outbound requests to internal/private IPs | CWE-918 |
| CSRF | State-changing forms missing token validation | CWE-352 |
| Privilege Escalation | Users accessing higher-privilege roles | CWE-269 |
| JWT/Session Manipulation | Metadata tampering, session fixation | CWE-287 |

---

## Workflow: Auditing a FastAPI or Flask App

### Step 1 — Identify All Routes

**FastAPI:**
```python
# List all routes and their dependencies
for route in app.routes:
    print(route.path, route.methods, route.dependencies)
```

**Flask:**
```python
# Print all registered endpoints
for rule in app.url_map.iter_rules():
    print(rule.endpoint, rule.methods, rule.rule)
```

Flag any route that:
- Handles POST, PUT, PATCH, DELETE without an auth dependency
- Returns user-specific data (profile, orders, files) without ownership check
- Has no rate limiting on sensitive operations

---

### Step 2 — Check Authorization Guards

**FastAPI — look for missing `Depends()`:**
```python
# VULNERABLE — no auth check
@app.get("/users/{user_id}/data")
async def get_user_data(user_id: int):
    return db.query(UserData).filter_by(owner_id=user_id).all()

# SECURE — requires authenticated user
@app.get("/users/{user_id}/data")
async def get_user_data(user_id: int, current_user: User = Depends(get_current_user)):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")
    return db.query(UserData).filter_by(owner_id=user_id).all()
```

**Flask — look for missing `@login_required`:**
```python
# VULNERABLE
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

# SECURE
@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")
```

---

### Step 3 — IDOR Check (Resource Ownership)

IDOR is the most common BAC failure. Every query that fetches a user-owned resource must compare `resource.owner_id` against `current_user.id`.

```python
# VULNERABLE IDOR — attacker can request any document_id
@app.get("/documents/{doc_id}")
async def get_doc(doc_id: int, user=Depends(get_current_user)):
    return db.get(Document, doc_id)  # No ownership check!

# SECURE
@app.get("/documents/{doc_id}")
async def get_doc(doc_id: int, user=Depends(get_current_user)):
    doc = db.get(Document, doc_id)
    if not doc or doc.owner_id != user.id:
        raise HTTPException(status_code=404)  # 404 preferred over 403 (avoids enumeration)
    return doc
```

**Test vector:** Authenticate as User A, record a resource ID, then authenticate as User B and request that same ID. If you get data — it's an IDOR.

---

### Step 4 — CORS Misconfiguration

**FastAPI:**
```python
# VULNERABLE — wildcard origin
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True)

# SECURE — explicit allowlist
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://app.yourdomain.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type"],
)
```

**Flask:**
```python
# VULNERABLE
CORS(app, origins="*")

# SECURE
CORS(app, origins=["https://app.yourdomain.com"], supports_credentials=True)
```

> ⚠️ `allow_origins=["*"]` combined with `allow_credentials=True` is doubly dangerous — most browsers block this, but it signals deep misconfiguration.

---

### Step 5 — SSRF (Now part of A01:2025)

Check any code that makes outbound HTTP requests with user-controlled URLs.

```python
import ipaddress, re

PRIVATE_RANGES = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("169.254.0.0/16"),  # AWS metadata
]

def is_safe_url(url: str) -> bool:
    from urllib.parse import urlparse
    import socket
    try:
        host = urlparse(url).hostname
        ip = ipaddress.ip_address(socket.gethostbyname(host))
        return not any(ip in net for net in PRIVATE_RANGES)
    except Exception:
        return False

# In your endpoint:
@app.post("/fetch")
async def fetch_url(url: str, user=Depends(get_current_user)):
    if not is_safe_url(url):
        raise HTTPException(status_code=400, detail="URL not allowed")
    return await httpx.get(url)
```

**Test vectors:** `http://169.254.169.254/latest/meta-data/` (AWS metadata), `http://localhost:6379` (Redis), `http://10.0.0.1/admin`

---

### Step 6 — CSRF (Flask-specific risk)

FastAPI APIs using JWT/Bearer tokens are generally CSRF-safe. Flask apps using session cookies need explicit protection.

```python
# Flask — verify Flask-WTF is installed and CSRF is enabled
from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect(app)

# All state-changing forms must include {{ form.hidden_tag() }} or {{ csrf_token() }}
```

Check that `WTF_CSRF_ENABLED = True` in config (it is by default, but verify it hasn't been disabled).

---

### Step 7 — JWT & Session Security

```python
# Verify JWT expiry is set (short-lived: 15 min–1 hr)
jwt.encode({"sub": user_id, "exp": datetime.utcnow() + timedelta(minutes=30)}, SECRET_KEY)

# Flask — verify session security flags
app.config["SESSION_COOKIE_SECURE"] = True    # HTTPS only
app.config["SESSION_COOKIE_HTTPONLY"] = True  # No JS access
app.config["SESSION_COOKIE_SAMESITE"] = "Lax" # CSRF mitigation
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=2)
```

---

## Quick Audit Checklist

Run through this for any Python web app:

- [ ] Every non-public route has an auth dependency / decorator
- [ ] All user-owned resource queries verify `resource.owner_id == current_user.id`
- [ ] CORS origins are an explicit allowlist, not `*`
- [ ] Outbound HTTP calls validate URL is not in private IP ranges
- [ ] Flask apps have Flask-WTF CSRF protection on all state-changing forms
- [ ] JWTs have short `exp` claims; sessions have `SECURE`, `HTTPONLY`, `SAMESITE` flags
- [ ] Session IDs are invalidated on logout
- [ ] Access control failures are logged and alerted on

---

## Automated Scanning

| Tool | What it catches | Command |
|---|---|---|
| **Bandit** | SSRF patterns, hardcoded secrets, dangerous functions | `bandit -r . -t B105,B106,B107,B501,B601` |
| **OWASP ZAP** | IDOR, missing auth at runtime, CORS | `zap-baseline.py -t http://localhost:8000` |
| **truffleHog** | Leaked tokens/keys in git history | `trufflehog git file://. --only-verified` |

---

## Key CWEs Reference

| CWE | Name | Typical Pattern |
|---|---|---|
| CWE-284 | Improper Access Control | Route accessible without any auth |
| CWE-285 | Improper Authorization | Auth present but role/ownership not checked |
| CWE-352 | CSRF | State-changing endpoint accepts cookie auth, no CSRF token |
| CWE-639 | Auth Bypass via User-Controlled Key | IDOR — `GET /orders/{id}` with no ownership check |
| CWE-862 | Missing Authorization | No `@login_required` or `Depends(get_current_user)` |
| CWE-918 | SSRF | `requests.get(user_input_url)` without validation |
| CWE-200 | Sensitive Info Exposure | Unauthorized user receives another's PII/data |

---

## See Also

- `references/bac-detail.md` — Expanded CWE descriptions, more attack examples, compliance mapping
- OWASP A01:2025 official page: https://owasp.org/Top10/A01_2025-Broken_Access_Control/