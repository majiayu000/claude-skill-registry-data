---
name: mishandling-exceptional-conditions
description: >
  Detect, analyze, and remediate OWASP A10:2025 — Mishandling of Exceptional Conditions in Python
  web applications (FastAPI and Flask). Use this skill whenever the user asks about error handling
  security, exception management, fail-open vulnerabilities, stack trace exposure, uncaught exceptions,
  transaction rollback safety, or resource leaks in exception paths. Also trigger for any OWASP A10
  audit, security code review involving try/except blocks, global exception handlers, or HTTP error
  responses that may leak sensitive information. If the user mentions CWE-209, CWE-248, CWE-636,
  CWE-703, CWE-754, or CWE-476 in a Python context, use this skill immediately.
---

# OWASP A10:2025 — Mishandling of Exceptional Conditions

**Brand new category for 2025**, replacing SSRF (absorbed into A01). Contains **24 CWEs** with
**769,581 recorded occurrences**. Addresses programs that fail to prevent, detect, and respond
to unusual situations — leading to crashes, unexpected behaviour, information disclosure, and
exploitable states.

---

## Core Concepts

### What It Covers
| Weakness | Risk |
|---|---|
| Improper error handling | Unhandled exceptions crash the app or expose internals |
| Failing open (CWE-636) | Auth/authz checks that pass when an exception is thrown |
| Sensitive data in error messages (CWE-209) | Stack traces, DB details, file paths leaked to clients |
| Uncaught exceptions (CWE-248) | No global safety net → 500 with debug output |
| Resource exhaustion in exception paths | DB connections, file handles never closed on error |
| State corruption | Partial transactions committed on exception |
| NULL pointer / None dereference (CWE-476) | Missing guard for `None` before attribute access |
| Missing default cases (CWE-754) | `if/elif` chains with no `else`; `match` with no wildcard |
| Race conditions in error recovery | Cleanup logic itself can be interrupted |

### Prevention Principles
1. **Catch errors where they occur** — at the function that can handle them, not three layers up.
2. **Fail closed** — when auth/authz logic throws, deny access; never pass through.
3. **Roll back completely** — partial DB transactions must be rolled back, never committed.
4. **Separate user messages from technical details** — log the stack trace server-side; return a safe, generic message to the client.
5. **Global exception handler as safety net** — every app needs one, but it is not a substitute for local handling.
6. **Rate-limit and quota** — prevent exceptional conditions (e.g., resource exhaustion) from being triggered intentionally.

---

## FastAPI Testing Checklist

### 1. Global Exception Handler
```python
# REQUIRED — catches anything not handled locally
@app.exception_handler(Exception)
async def global_handler(request: Request, exc: Exception):
    logger.error("Unhandled exception", exc_info=exc)
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})
```
**Flag if absent.** The default FastAPI 500 response may include traceback in development mode.

### 2. Fail-Closed Auth Middleware (CWE-636)
```python
# BAD — exception causes pass-through (fail open)
@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    try:
        verify_token(request)
    except Exception:
        pass                       # ← VULNERABILITY
    return await call_next(request)

# GOOD — exception causes denial (fail closed)
@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    try:
        verify_token(request)
    except Exception as e:
        logger.warning("Auth check failed", exc_info=e)
        return JSONResponse(status_code=401, content={"detail": "Unauthorized"})
    return await call_next(request)
```

### 3. Custom HTTP Error Responses (CWE-756 / CWE-209)
```python
# Register handlers for all common error codes
@app.exception_handler(404)
async def not_found(request, exc):
    return JSONResponse(status_code=404, content={"detail": "Not found"})

@app.exception_handler(422)
async def validation_error(request, exc):
    return JSONResponse(status_code=422, content={"detail": "Invalid input"})
```
**Flag any handler that returns `str(exc)`, `repr(exc)`, or `traceback.format_exc()`** in the response body.

### 4. Resource Cleanup in Exception Paths
```python
# BAD — connection leaked if query raises
conn = db.connect()
result = conn.execute(query)   # raises → conn never closed
conn.close()

# GOOD — context manager guarantees cleanup
with db.connect() as conn:
    result = conn.execute(query)
```
Scan for: `db.connect()`, `open(file)`, `socket.socket()` **not** inside a `with` block or `try/finally`.

### 5. SQLAlchemy Transaction Rollback
```python
# BAD — partial write committed on error
session.add(obj)
risky_operation()        # raises → session still commits elsewhere
session.commit()

# GOOD — rollback on exception
try:
    session.add(obj)
    risky_operation()
    session.commit()
except Exception:
    session.rollback()
    raise
```
Flag: any `session.commit()` not paired with `session.rollback()` in an `except` branch.

---

## Flask Testing Checklist

### 1. Global Exception Handler
```python
@app.errorhandler(Exception)
def global_error(e):
    app.logger.error("Unhandled exception", exc_info=e)
    return {"error": "Internal server error"}, 500
```
**Also register specific handlers:**
```python
@app.errorhandler(404)
def not_found(e):
    return {"error": "Not found"}, 404

@app.errorhandler(500)
def server_error(e):
    return {"error": "Server error"}, 500
```

### 2. Flask Debug Mode — Doubles as A02 + A10 Issue
Debug mode (`debug=True` or `FLASK_DEBUG=1`) enables the **Werkzeug interactive debugger**, which:
- Exposes full tracebacks to the browser.
- Allows **arbitrary code execution** via the debugger console.

**Flag immediately** if found in production config or environment variables.

### 3. `request.args.get()` Silent `None` Returns
```python
# BAD — returns None silently; downstream code may crash
user_id = request.args.get("user_id")
user = db.query(User).filter_by(id=user_id).first()  # id=None → wrong query

# GOOD — explicit validation
user_id = request.args.get("user_id")
if user_id is None:
    abort(400, description="user_id is required")
```
FastAPI's Pydantic models prevent this automatically; Flask requires manual guards.

### 4. Fail-Closed `before_request` Hooks
```python
# BAD — exception in auth check bypasses protection
@app.before_request
def check_auth():
    try:
        verify_session()
    except:
        pass   # ← VULNERABILITY

# GOOD
@app.before_request
def check_auth():
    try:
        verify_session()
    except Exception as e:
        app.logger.warning("Session verify failed", exc_info=e)
        abort(401)
```

---

## Automated Scanning Approach

### Static Analysis (Bandit)
```bash
bandit -r . -t B110,B112   # try-except-pass and try-except-continue
bandit -r . --severity-level medium
```
Key Bandit test IDs for this category:
- `B110` — `try: ... except: pass` (swallowed exception)
- `B112` — `try: ... except: continue` (swallowed in loop)

### Pattern Search (grep / ripgrep)
```bash
# Fail-open patterns
rg "except.*:\s*(pass|continue|return True)" --type py

# Stack traces leaking to response
rg "traceback\.format_exc\(\)|str\(exc\)|repr\(exc\)" --type py

# Missing context managers
rg "open\(|\.connect\(\)" --type py   # review each hit for 'with'

# Missing rollback
rg "session\.commit\(\)" --type py    # check each for paired rollback
```

### Runtime / DAST
- Trigger deliberate 404, 500, and validation errors (422 on FastAPI).
- Inspect HTTP responses for presence of: file paths, stack frames, SQL query strings, exception class names.
- Probe middleware by sending a malformed Authorization header — verify the response is `401`, not `200`.

---

## Key CWEs (A10:2025)

| CWE | Name | Python Manifestation |
|---|---|---|
| CWE-209 | Sensitive Info in Error Messages | `str(exc)` in JSON response, debug traceback |
| CWE-248 | Uncaught Exception | No global handler; unhandled `raise` crashes app |
| CWE-636 | Failing Open | `except: pass` in auth check |
| CWE-703 | Improper Handling of Exceptional Conditions | Broad `except` that hides errors |
| CWE-754 | Improper Check for Unusual Conditions | Missing None/empty checks on external input |
| CWE-476 | NULL Pointer Dereference | Attribute access on potentially-None object |
| CWE-756 | Missing Custom Error Page | Default framework error pages with debug info |

---

## Remediation Priority

1. **Critical:** Fail-open auth middleware / `before_request` hooks (CWE-636) — direct authentication bypass.
2. **Critical:** Debug mode enabled in production (Werkzeug debugger = RCE).
3. **High:** Stack traces / DB details in HTTP responses (CWE-209) — aids attacker reconnaissance.
4. **High:** Missing global exception handler — unhandled paths crash app and may reveal details.
5. **Medium:** Missing transaction rollback — data integrity corruption.
6. **Medium:** Resource leaks in exception paths — connection pool exhaustion under attack.
7. **Low:** Silent `None` returns from `request.args.get()` — logic bugs, not directly exploitable.

---
