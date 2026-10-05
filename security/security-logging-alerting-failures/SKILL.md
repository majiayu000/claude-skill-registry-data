---
name: security-logging-alerting-failures
description: >
  Use this skill whenever auditing, reviewing, or testing Python web applications (FastAPI or Flask)
  for OWASP A09:2025 — Security Logging & Alerting Failures. Trigger this skill when the user mentions:
  logging security, audit trails, log injection, sensitive data in logs, alerting gaps, insufficient
  logging, SIEM integration, log monitoring, incident detection readiness, or any request to audit or
  fix logging/alerting in a Python backend. Also trigger when a user asks "are we logging the right
  things?", "how do I detect attacks?", or "what should we be alerting on?". Do NOT skip this skill
  just because the request sounds simple — log-related security issues are consistently underestimated
  and require systematic coverage across all five CWEs.
---

# A09:2025 — Security Logging & Alerting Failures

**OWASP rank:** #9 (community-voted for third consecutive cycle)  
**Renamed in 2025:** Added "Alerting" — logging without alerting provides minimal security value.  
**Stats:** 5 CWEs, 723 CVEs, 3.91% average incidence rate  
**Coverage CWEs:** CWE-778, CWE-117, CWE-532, CWE-223, CWE-390

---

## What This Category Covers

| Failure Type | Description |
|---|---|
| **Insufficient Logging** | Auditable events (logins, access control failures, validation errors) not logged |
| **Log Injection** | User input flows unescaped into log messages — enables log forgery |
| **Sensitive Data in Logs** | Passwords, tokens, PII, card numbers written to log output |
| **Omission of Security-Relevant Info** | Errors/warnings logged without context (IP, user, timestamp, action) |
| **No Alerting** | Logs exist but no thresholds, rules, or platform routes them to incident response |

---

## Audit Checklist — FastAPI & Flask

Work through each section systematically. For each item, note: **PASS**, **FAIL**, or **NOT APPLICABLE**.

### 1. Log Injection (CWE-117)
User-controlled input must never flow raw into log statements.

**What to look for:**
```python
# VULNERABLE — newline injection, ANSI escape injection
logger.info(f"User logged in: {request.form['username']}")
logger.warning("Failed login for: " + username)

# SAFE — sanitize before logging
import re
safe_username = re.sub(r'[\r\n\x1b]', '_', username)
logger.info("Failed login for: %s", safe_username)
```

**Checklist:**
- [ ] No f-strings or `+` concatenation with raw request data in log calls
- [ ] Newlines (`\r`, `\n`) stripped from all user-supplied log values
- [ ] ANSI escape codes (`\x1b[`) stripped (prevent terminal injection)
- [ ] Structured logging used (JSON format) — field separation prevents injection by design

---

### 2. Sensitive Data in Logs (CWE-532)
Secrets must never appear in log output — even at DEBUG level.

**Patterns to flag:**
```python
# VULNERABLE
logger.debug(f"Auth token: {token}")
logger.info(f"Processing payment for card: {card_number}")
app.logger.debug(request.json)         # May contain password field
print(f"Password reset for {email}, token={reset_token}")

# SAFE
logger.info("Auth token validated for user_id=%s", user_id)
logger.info("Payment processed for user_id=%s, last4=%s", user_id, card_number[-4:])
```

**What to scan for:**
- [ ] No logging of: `password`, `passwd`, `secret`, `token`, `api_key`, `authorization` header values
- [ ] No logging of: credit card numbers, SSNs, full email+password combos
- [ ] `request.json` / `request.form` not logged wholesale without field filtering
- [ ] No `print()` statements containing sensitive variables in production code
- [ ] Bandit rule `B506` (and similar) passes in CI/CD

---

### 3. Insufficient Logging (CWE-778)
The following events **must** produce log entries with full context.

**Required log events:**
| Event | Minimum Fields |
|---|---|
| Failed authentication | timestamp, IP, username attempted, user-agent |
| Successful authentication | timestamp, IP, user_id, method (password/OAuth/MFA) |
| Authorization failure (403) | timestamp, IP, user_id, resource attempted, HTTP method |
| Input validation failure | timestamp, IP, user_id, field name (not value if sensitive), error |
| High-value transaction | timestamp, user_id, action, resource ID, before/after state |
| Account changes (password reset, role change) | timestamp, actor_user_id, target_user_id, change type |
| Admin actions | timestamp, admin_user_id, action, affected resource |

**FastAPI implementation pattern:**
```python
import logging
import structlog  # recommended for structured logs

log = structlog.get_logger()

# In auth endpoint
@router.post("/login")
async def login(credentials: LoginSchema, request: Request):
    user = await authenticate(credentials)
    if not user:
        log.warning(
            "auth.failed",
            ip=request.client.host,
            username=credentials.username,    # OK — username is not a secret
            user_agent=request.headers.get("user-agent"),
        )
        raise HTTPException(status_code=401, detail="Invalid credentials")
    log.info("auth.success", user_id=user.id, ip=request.client.host)
```

**Flask implementation pattern:**
```python
from flask import request
import logging

@app.route("/login", methods=["POST"])
def login():
    user = authenticate(request.form["username"], request.form["password"])
    if not user:
        app.logger.warning(
            "auth.failed ip=%s username=%s ua=%s",
            request.remote_addr,
            request.form.get("username"),
            request.user_agent.string,
        )
        return {"error": "Invalid credentials"}, 401
```

**Checklist:**
- [ ] All 401/403 responses have a corresponding `logger.warning()` or `logger.error()` call
- [ ] Log entries include: timestamp (automatic with `logging`), source IP, user identifier
- [ ] Password reset and account modification flows are logged
- [ ] Admin panel actions are logged with actor identity
- [ ] High-value business transactions produce audit log entries

---

### 4. Structured Logging & SIEM Compatibility
Log format must be parseable by observability platforms (ELK, Splunk, Datadog, Sentry).

**FastAPI — structlog + JSON:**
```python
# main.py
import structlog
import logging

structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.stdlib.add_log_level,
        structlog.processors.JSONRenderer(),  # machine-parseable
    ],
    wrapper_class=structlog.BoundLogger,
    logger_factory=structlog.PrintLoggerFactory(),
)
```

**Flask — python-json-logger:**
```python
from pythonjsonlogger import jsonlogger

handler = logging.StreamHandler()
handler.setFormatter(jsonlogger.JsonFormatter(
    fmt="%(asctime)s %(levelname)s %(name)s %(message)s"
))
app.logger.addHandler(handler)
```

**Checklist:**
- [ ] Log output is JSON-formatted (not plain text) in production
- [ ] Log level is not `DEBUG` in production (leaks verbose info)
- [ ] Logs ship to a centralized platform: Sentry, ELK, Splunk, Datadog, CloudWatch
- [ ] Log retention policy exists and meets compliance requirements (e.g., 90 days minimum)

---

### 5. Alerting Integration
Logging without alerting = silent failures. Verify active monitoring exists.

**Sentry (exception alerting):**
```python
# FastAPI
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
sentry_sdk.init(dsn=settings.SENTRY_DSN, integrations=[FastApiIntegration()])

# Flask
from sentry_sdk.integrations.flask import FlaskIntegration
sentry_sdk.init(dsn=settings.SENTRY_DSN, integrations=[FlaskIntegration()])
```

**Recommended alerting thresholds:**
| Signal | Alert Trigger |
|---|---|
| Failed logins | >10 failures for same username in 5 min |
| Failed logins | >100 failures from same IP in 5 min |
| 403 responses | >50 from same user_id in 1 min |
| 500 errors | >5% of requests in any 1-min window |
| New admin account | Immediate alert, every occurrence |
| Privilege escalation | Immediate alert, every occurrence |

**Checklist:**
- [ ] Sentry or equivalent is initialized and receiving events in production
- [ ] Rate-limit violations produce alert events (not just HTTP 429 responses)
- [ ] Repeated auth failures trigger alerts (brute force detection)
- [ ] Alerting runbooks/playbooks exist for each alert type
- [ ] Honeytokens deployed in high-value areas (near-zero false-positive intrusion detection)

---

## Automated Scanning

Run these tools as part of CI/CD:

```bash
# Static analysis — catches log injection patterns, sensitive data in logs
bandit -r . -t B106,B107,B110 --severity-level medium

# Search for raw request data in log calls
grep -rn "logger\.\(info\|warning\|error\|debug\)" . \
  | grep -E "request\.(form|json|args|data|headers)\[" \
  | grep -v "\.get(" 

# Search for potential sensitive field logging
grep -rn "logger\|logging\|print" . \
  | grep -iE "password|passwd|secret|token|api_key|card|ssn|cvv"
```

---

## Key CWEs Reference

| CWE | Name | Python Risk |
|---|---|---|
| CWE-778 | Insufficient Logging | No logging on auth/authz failures |
| CWE-117 | Log Injection | f-string user input in logger calls |
| CWE-532 | Sensitive Info in Logs | Passwords/tokens in debug output |
| CWE-223 | Omission of Security-Relevant Info | Logs lack IP/user context |
| CWE-390 | Detection of Error Condition Without Action | Exception caught, swallowed, not logged |

---

## Reference Files

- `references/remediation-patterns.md` — Full before/after code fixes for each CWE
- `references/alerting-platforms.md` — Integration guides for Sentry, ELK, Splunk, Datadog

Read these when the user needs detailed implementation help beyond the checklist.