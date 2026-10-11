---
name: security-audit
description: Identify vulnerabilities, exposed secrets, authorization flaws, unsafe dependencies, and cryptographic weaknesses.
---

# Security Audit

## Audit Checklist
- [ ] **Secret Hygiene:** Scan repository for hardcoded tokens, passwords, private keys, or `.env` files.
- [ ] **Authorization Boundaries:** Verify all mutations and sensitive queries require valid authentication and authorization tokens.
- [ ] **Injection Prevention:** Parameterized SQL, sanitized command execution (no raw shell string interpolation), and XSS prevention.
- [ ] **Dependency Scrutiny:** Run dependency vulnerability checks (`npm audit`, `pip-audit`, or safety).
- [ ] **Audit Trail:** Verify sensitive operational decisions are recorded in a tamper-evident, append-only ledger.
