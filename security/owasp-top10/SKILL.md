---
name: owasp-top10
description: A deep prevention reference for the OWASP Top 10 web risks — broken access control, injection, crypto failures, insecure design, SSRF and more — with vulnerable-vs-fixed code, edge cases, and a runnable naive-vulnerability scanner.
type: skill
version: 2.0.0
updated: 2026-06-28
---
# OWASP Top 10 Prevention

Most real-world breaches exploit a short, well-known list of weaknesses. This package is the deep
reference: each category gets its root cause, the default defense, and a vulnerable-vs-fixed example.
Category deep-dives live in `references/`, side-by-side fixes in `examples/`, and a runnable heuristic
scanner in `scripts/`.

> Based on the OWASP Top 10 (2021). The list shifts over time, but the underlying defenses are durable.

## The list (and the one-line defense for each)

| # | Category | Default defense |
|---|---|---|
| A01 | **Broken Access Control** | Enforce authorization server-side on every action; deny by default; check ownership (stop IDOR). |
| A02 | **Cryptographic Failures** | TLS in transit; encrypt sensitive data at rest; hash passwords with argon2/bcrypt; never roll your own crypto. |
| A03 | **Injection** (SQL/cmd/XSS) | Parameterize queries; context-aware output encoding; never concatenate untrusted input. |
| A04 | **Insecure Design** | Threat-model before building; secure-by-design defaults; abuse-case thinking. |
| A05 | **Security Misconfiguration** | Harden defaults; disable debug in prod; least-privilege; remove unused features. |
| A06 | **Vulnerable Components** | Inventory dependencies; patch on a schedule; scan for CVEs (see `vuln-scanner` agent). |
| A07 | **Auth Failures** | Strong session handling, MFA, rate-limit logins, no credential stuffing surface (see `secure-auth`). |
| A08 | **Software & Data Integrity** | Verify signatures; secure CI/CD; don't deserialize untrusted data. |
| A09 | **Logging & Monitoring Failures** | Log security events, alert on them, don't log secrets (see `audit-logging`). |
| A10 | **SSRF** | Allow-list outbound destinations; validate/resolve URLs; block internal ranges. |

## The two that cause the most damage

### A01 — Broken Access Control (the #1 risk)
The bug: the server checks *authentication* (who you are) but not *authorization* (whether you may do
this specific thing). Classic IDOR — changing an ID in the URL to read someone else's data.

```js
// VULNERABLE: any logged-in user can read any invoice by guessing an id
app.get('/invoices/:id', auth, async (req, res) => {
  const invoice = await db.getInvoice(req.params.id);
  res.json(invoice);
});

// FIXED: authorize against ownership, deny by default
app.get('/invoices/:id', auth, async (req, res) => {
  const invoice = await db.getInvoice(req.params.id);
  if (!invoice || invoice.ownerId !== req.user.id) return res.status(404).end(); // 404 hides existence
  res.json(invoice);
});
```
Deep-dive: `references/access-control.md`.

### A03 — Injection
The bug: untrusted input is interpreted as code/query/markup. Defense is structural separation of code
from data.

```js
// VULNERABLE: SQL injection
db.query(`SELECT * FROM users WHERE email = '${input}'`);

// FIXED: parameterized query — driver treats input strictly as data
db.query('SELECT * FROM users WHERE email = $1', [input]);
```
SQL, command, and XSS variants with fixes: `references/injection.md` and `examples/sql-injection-fix.md`,
`examples/xss-fix.md`.

## A worked SSRF case (A10)

```js
// VULNERABLE: fetches any URL the user supplies -> attacker hits internal metadata service
const data = await fetch(req.query.url);

// FIXED: allow-list hosts and block internal ranges
const url = new URL(req.query.url);
if (!ALLOWED_HOSTS.has(url.hostname)) return res.status(400).json({ error: 'host not allowed' });
// ...plus resolve DNS and reject private IP ranges (169.254/16, 10/8, 127/8) to stop rebinding
```
Detail and the private-range checks: `references/ssrf-and-design.md`.

## Edge cases & gotchas

- **Blocklists fail; allow-lists work.** Trying to block "bad" input (e.g. stripping `<script>`) is
  whack-a-mole — encode for the output context instead, and allow-list what's permitted.
- **404 vs 403 to avoid existence leakage.** For unauthorized access to a resource whose very existence
  is sensitive, return `404`, not `403`, so attackers can't enumerate.
- **Mass assignment.** Binding request bodies straight to models lets attackers set fields like
  `isAdmin`. Allow-list bindable fields.
- **Second-order injection.** Stored input that's safe on the way in can be unsafe when later used in a
  different context (e.g. a stored value concatenated into a query). Defend at every sink.
- **Defense in depth.** No single control is enough — combine input validation, parameterization,
  output encoding, authz checks, and monitoring.

## When the "fix" isn't enough

Input sanitization alone is not a substitute for parameterization/encoding — it's a fragile add-on.
And security review (this skill + the `security-auditor` agent) catches code-level bugs, but design-level
flaws (A04) need **threat modeling up front** (see the `threat-modeler` agent) — you can't audit your
way out of an insecure design.

## Files in this package

- `references/access-control.md` — A01 in depth: authz patterns, IDOR, mass assignment
- `references/injection.md` — A03: SQL/command/XSS with defenses per context
- `references/crypto-failures.md` — A02: hashing, encryption, key handling
- `references/ssrf-and-design.md` — A10 + A04: SSRF defense and secure design
- `examples/sql-injection-fix.md` — vulnerable vs parameterized, with edge cases
- `examples/xss-fix.md` — output encoding and safe rendering
- `scripts/scan-injection.mjs` — runnable heuristic scanner for naive injection patterns (selftest passes)

Pairs with the `security-auditor` agent, the `threat-modeler` agent, and the `secure-auth` and
`secrets-management` skills.
