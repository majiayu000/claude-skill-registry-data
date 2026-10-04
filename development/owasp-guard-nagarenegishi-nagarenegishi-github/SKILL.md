---
name: owasp-guard
description: >
  Automatic OWASP Top 10:2025 compliance checker for all code suggestions and implementations.
  Use this skill whenever writing, reviewing, suggesting, or modifying code that touches
  security-relevant domains: authentication, authorization, database queries, user input handling,
  cryptography, HTTP endpoints, file I/O, error handling, dependency management, session management,
  configuration, logging, or API design. Also trigger when the user mentions OWASP, security review,
  secure coding, vulnerability check, or hardening.
---

# OWASP Guard

Enforce OWASP Top 10:2025 compliance on code touching security-relevant domains.
Guidance sourced from the official OWASP Cheat Sheet Series, cached locally.

## Cache

Cache location: `.claude/skills/owasp-guard/cache/`

```
cache/
├── last_updated.json
└── <CheatSheet>.md files
```

Pre-cached cheat sheets are bundled with the skill in `.claude/skills/owasp-guard/cache/`.
To update the cache, the user runs `/owasp-update` (see the `owasp-update` skill).
This skill never fetches cheat sheets itself.

### Staleness Check

Read `.claude/skills/owasp-guard/cache/last_updated.json`.
If any required cheat sheet is missing from the JSON or has `fetched_at` older than 90 days, suggest:

> "OWASP cheat sheet cache is over 90 days old. Run `/owasp-update` to refresh."

Do not block, do not auto-fetch. Continue with existing cached content.

---

## Workflow

### Step 1: Check Security Relevance

Skip entirely if code does not touch: authentication, session management, authorization,
access control, database queries, user input handling, cryptography, secrets, HTTP endpoints,
API design, file I/O, path handling, error handling that could leak info, dependency management,
configuration, environment variables, logging with sensitive data, deserialization.

### Step 2: Identify Language and Load References

Detect language/framework. Read `.claude/skills/owasp-guard/references/<language>.md` to determine
which OWASP categories and cheat sheets are relevant.

Available: `.claude/skills/owasp-guard/references/python.md`, `.claude/skills/owasp-guard/references/javascript.md`,
`.claude/skills/owasp-guard/references/go.md`, `.claude/skills/owasp-guard/references/java.md`,
`.claude/skills/owasp-guard/references/csharp.md`

No matching reference file → use the checklist below with general OWASP guidance.

### Step 3: OWASP Top 10:2025 Checklist

Check only relevant categories. Read cached cheat sheet content from
`.claude/skills/owasp-guard/cache/` for guidance. If a required cheat sheet is not cached,
note this in findings and continue with built-in knowledge.

**A01 — Broken Access Control**: Authorization on every protected resource? Object ownership validated? Client-side-only access control? CORS restrictive? SSRF vectors?

**A02 — Security Misconfiguration**: Debug/dev settings disabled for prod? Default credentials removed? Security headers set? Unnecessary endpoints disabled? Environment-aware config?

**A03 — Software Supply Chain Failures**: Dependencies pinned to exact versions? Trusted sources? Lockfile committed? Build scripts injection-safe?

**A04 — Cryptographic Failures**: Data encrypted at rest and in transit? Strong algorithms (no MD5/SHA1/DES for security)? Keys/secrets outside code? TLS enforced? Cryptographically secure RNG?

**A05 — Injection**: Input validated/sanitized? Parameterized queries (no string concatenation)? Output encoded by context? OS command execution avoided or strictly validated?

**A06 — Insecure Design**: Rate limits on sensitive operations? Business logic abuse protection? Least-privilege design?

**A07 — Authentication Failures**: MFA for sensitive operations? Passwords hashed with Argon2id (preferred) or bcrypt (legacy)? Session tokens regenerated after login? Brute-force protection?

**A08 — Software or Data Integrity Failures**: Deserialized data validated? CI/CD tamper-protected? Updates signature-verified?

**A09 — Security Logging & Alerting Failures**: Auth events logged? Access control failures logged? Logs exclude sensitive data? Structured logging?

**A10 — Mishandling of Exceptional Conditions**: Fail-closed error handling? Generic error messages to users? Resources released in error paths? Timeouts on external calls?

### Step 4: Report Findings

On violations:
1. State OWASP category (e.g., "A05:2025 — Injection")
2. Explain what is wrong and the risk
3. Cite the OWASP Cheat Sheet recommendation from cache
4. Provide a compliant alternative after verifying it (Step 5)

No violations → proceed normally. Do not announce "OWASP check passed" unless
user explicitly asked for a security review.

### Step 5: Verify Alternatives

Before suggesting any library/API/pattern as a fix, verify it is both maintained and safe.

**5a — Deprecation & Maintenance Gate**:

Search `<package> deprecated OR unmaintained OR archived` to confirm the package
is actively maintained. Deprecated, unmaintained, or archived packages are never
recommended regardless of CVE status. Find an actively maintained alternative instead.

**5b — CVE Check via OSV.dev** (preferred, requires `api.osv.dev`):

```bash
curl -s -X POST "https://api.osv.dev/v1/query" \
  -H "Content-Type: application/json" \
  -d '{"version":"<VER>","package":{"name":"<PKG>","ecosystem":"<ECO>"}}'
```

Ecosystems: `PyPI`, `npm`, `Go`, `Maven`, `NuGet`, `crates.io`, `RubyGems`, `Packagist`
If the package ecosystem is not listed, skip OSV.dev and use web search fallback.

Vulnerabilities found → do not recommend. Find nearest patched version.

On failure, inform user:
> "OSV.dev API (`api.osv.dev`) not reachable. Using web search for CVE verification.
> Allow `api.osv.dev` for precise version-specific checks."

**5b fallback — Web Search for CVEs**:
Search `<package> <version> CVE vulnerability` if OSV.dev is unreachable.

**5c — State verification result**:
> "Use `argon2-cffi` (v23.1.0) — maintained, no known vulnerabilities (OSV.dev)."

Or on fallback:
> "Use `argon2-cffi` (v23.1.0) — maintained, no active CVEs found (web search, OSV.dev unreachable)."

Never suggest unverified alternatives. If verification fails entirely, state this
and recommend the user verify manually.

---

## Behavior

- Only surface findings on actual issues. No boilerplate.
- Be specific: category, exact pattern, risk, fix with cheat sheet citation.
- If user is prototyping, note issues briefly, do not block.
