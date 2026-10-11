---
name: owasp-top-10
description: OWASP Top 10 — injection, broken auth, XSS, misconfig checklist.
---

## OWASP Top 10 (2021)

| ID | Name | One-line Description | Primary Mitigation |
|----|------|----------------------|--------------------|
| A01 | Broken Access Control | Users act outside their intended permissions | Deny by default; enforce ownership checks server-side |
| A02 | Cryptographic Failures | Sensitive data exposed due to weak/missing encryption | TLS everywhere; use AES-256/bcrypt; never roll your own crypto |
| A03 | Injection | Untrusted data sent to an interpreter as a command | Parameterized queries; input validation; ORM usage |
| A04 | Insecure Design | Missing security controls at architecture level | Threat modeling; secure design patterns; defense in depth |
| A05 | Security Misconfiguration | Default configs, open cloud storage, verbose errors | Harden defaults; disable unused features; automated config checks |
| A06 | Vulnerable & Outdated Components | Libraries/frameworks with known CVEs | Dependency scanning (Snyk, Dependabot); pin versions; audit regularly |
| A07 | Identification & Auth Failures | Broken auth, weak passwords, credential stuffing | MFA; rate limiting; secure session management; breach detection |
| A08 | Software & Data Integrity Failures | Untrusted updates, insecure deserialization | Verify checksums; signed artifacts; CI/CD pipeline integrity |
| A09 | Security Logging & Monitoring Failures | Breaches undetected due to missing logs | Structured logging; alerting on anomalies; retain logs ≥ 1 year |
| A10 | Server-Side Request Forgery (SSRF) | Server fetches attacker-controlled URLs | Allowlist outbound targets; block internal IP ranges |

---

## Critical Code Examples

### A03 — SQL Injection

**Vulnerable:**
```python
# NEVER DO THIS
query = f"SELECT * FROM users WHERE email = '{user_input}'"
db.execute(query)
```

**Safe — parameterized query:**
```python
query = "SELECT * FROM users WHERE email = %s"
db.execute(query, (user_input,))
```

```javascript
// Node.js / pg
const result = await pool.query(
  'SELECT * FROM users WHERE email = $1',
  [userInput]
);
```

---

### A03 — XSS (Cross-Site Scripting)

**Vulnerable:**
```html
<!-- NEVER render raw user input -->
<div>{{{ userComment }}}</div>
```

**Safe — output encoding:**
```javascript
// React escapes by default — avoid dangerouslySetInnerHTML
<div>{userComment}</div>

// Vanilla JS — use textContent, not innerHTML
element.textContent = userComment;

// When HTML is required, sanitize first
import DOMPurify from 'dompurify';
element.innerHTML = DOMPurify.sanitize(userComment);
```

**HTTP headers (add to every response):**
```
Content-Security-Policy: default-src 'self'
X-Content-Type-Options: nosniff
```

---

### A01 — IDOR (Insecure Direct Object Reference)

**Vulnerable:**
```python
# NEVER DO THIS — trusts the caller's claimed ownership
@app.get("/invoices/{invoice_id}")
def get_invoice(invoice_id: int):
    return db.query(Invoice).get(invoice_id)
```

**Safe — ownership check before access:**
```python
@app.get("/invoices/{invoice_id}")
def get_invoice(invoice_id: int, current_user: User = Depends(get_current_user)):
    invoice = db.query(Invoice).get(invoice_id)
    if not invoice or invoice.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    return invoice
```

**Rule:** always filter by the authenticated user's identity — never trust a client-supplied owner ID.

---

## Quick Checklist per PR

- [ ] All DB queries use parameterized statements or ORM
- [ ] All user-controlled output is encoded before rendering
- [ ] Every resource endpoint checks authenticated ownership
- [ ] No sensitive data in logs, error messages, or URL params
- [ ] Dependencies scanned for known CVEs
- [ ] Auth endpoints have rate limiting
