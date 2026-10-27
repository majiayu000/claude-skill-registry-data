---
name: luke-security
description: >
  Security-focused audit for the Luke codebase. Covers IDOR, auth bypass,
  session security, input validation, rate limiting gaps, sensitive data
  exposure, LDAP injection, JWT/token issues, and invokes Trail of Bits
  sharp-edges and insecure-defaults plugins.
  Use when asked to audit security or find vulnerabilities.
  Scoping: default = diff vs merge-base. /luke-security apps/api | --since <ref> | --full
argument-hint: '[--full|--since <ref>|<path> [--since <ref>]]'
context: fork
agent: Explore
background: false
disallowed-tools: Edit, Write, NotebookEdit
---

# Luke Security Audit

Read-only. Do NOT modify any file.
Every finding needs a concrete attack scenario — no theoretical issues.

**Read `.claude/skills/luke-shared/audit-protocol.md` first** and apply it in
full: diff scoping (§1), baseline suppression (§2), the mandatory "Promotion
to rule" section (§3), `lessons.md` as a check input (§4), and the
constraint/heuristic classification (§8).

**This skill owns the systematic exploit hunt** for the application
(`.claude/skills/luke-shared/governance-map.md`). Two boundaries:

- **Dependency and supply-chain advisories are not yours.** A vulnerable
  package, an override that still resolves to a patched version, a deprecated
  security-sensitive dependency: `/luke-deps security`. The mechanical
  correctness of a security gate — a scanner chain that does not fail closed —
  is `/luke-deps platform`. What belongs here is the semantics: a recurring
  injection pattern with no Semgrep rule is yours to propose (§3).
- **`/luke-bugs` escalates to you.** It reports runtime defects and no longer
  keeps its own IDOR / rate-limit / secret-exposure checklist. A bug carrying
  `Security escalation: YES` arrives with a scenario but no exploitability
  judgement — that judgement is this skill's job. Re-derive it from the code;
  an escalation is a pointer, not a finding you inherit.

**Invocation arguments:** $ARGUMENTS

Resolve the invocation arguments above per `audit-protocol.md` §1 **before**
running any git scope derivation. The whole bound value is the scope selector
here — this skill takes no mode. If it is empty, use the protocol default —
diff vs merge-base, not the whole monorepo. If it carries an explicit selector,
that selector wins and the default is never derived.

Exception to scoping: authentication, session, and token-handling checks must
always be evaluated **at the system level**, even when the diff doesn't touch
them. A bypass often arises from the interaction between new code and an
existing control elsewhere — limiting the read to the diff here would hide
exactly the class of problems this skill looks for.

---

## Phase 1 — Trail of Bits Static Analysis

Invoke these plugins if installed, passing the scoped path:

1. `Skill(sharp-edges)` — error-prone APIs, dangerous default configurations
2. `Skill(insecure-defaults)` — fail-open patterns when config is missing

If either plugin is not installed, note it in the report and continue.

---

## Phase 2 — Check Areas

Three areas, one single pass. See the fan-out note in `../luke-shared/audit-protocol.md` §6.

### 1 — Authentication, Session & Token Security

1. **LDAP injection**: `searchFilter` or `groupSearchFilter` built from user input without sanitization — `(&(uid=${username}))` allows filter injection
2. **Session fixation**: after successful login (especially LDAP), verify new session token is generated and pre-auth session is invalidated
3. **JWT secret exposure**: `getApiJwtSecret()` or `getNextAuthSecret()` in client-side code or in any logger call
4. **Token validation gaps**: JWT verification that checks signature but not expiry, issuer, or audience
5. **Password reset token entropy**: token generation using `Math.random()` or tokens shorter than 32 bytes (64 hex chars) — CRITICAL
6. **Missing auth on tRPC procedures**: public procedures (no `requirePermission`) returning or modifying non-public data. Check especially: `getById` procedures, anything under `product.*` or `admin.*` routers
7. **Privilege escalation via role assignment**: user update procedures — can non-admin change their own role or another user's role?
8. **Admin-only endpoints reachable by editor**: every operation ADR-038 lists under "Admin-only operations" (`docs/decisions/038-resource-action-permissions-grants-follow-section-visibility.md`) and ADR-029 under "Admin-only operations" and "Maintenance" (`docs/decisions/029-resource-action-permissions-one-builder-logged-refusals.md`), plus any procedure called only from a page hidden to editor by default — verify not reachable by editor through any code path

---

### 2 — Authorization (IDOR) & Input Validation

**IDOR:**

1. tRPC procedures accepting an ID and returning the resource without verifying the requesting user has access to THAT SPECIFIC record — check: collection layout rows, pricing parameter sets, vendor/brand/season operations
2. Horizontal privilege escalation: procedures scoped to `brandId`/`seasonId` from user input — verify brand/season belongs to current context, not just that it exists
3. Permission check bypass via HTTP: any routes outside tRPC (REST endpoints, Next.js API routes) without equivalent permission checks

**Input validation:** 4. **Zod schema bypass**: procedures where `.parse()` result is ignored and original input is used in subsequent operations 5. **AppConfig key injection**: endpoint accepting config key as user input and writing to AppConfig without validating against `AppConfigRegistry` — attacker could overwrite `auth.strategy` 6. **Path traversal in storage**: storage operations where `key` or `bucket` comes from user input without sanitization 7. **SQL injection via sanitizeCompany**: any direct string interpolation of `config.company` into SQL without `sanitizeCompany()` — CRITICAL 8. **JSON.parse on user input**: user-supplied strings parsed as JSON without try/catch AND without schema validation on parsed result

---

### 3 — Sensitive Data & Rate Limiting

**Sensitive data exposure:**

1. tRPC responses including encrypted config values or password fields:
   - `config.list` must return `valuePreview: null` for every encrypted entry
     (the NAV password included), never the stored value
   - `getLdapConfig` must return `hasBindPassword: boolean`, not the credential
   - User queries must not return password hash
2. TRPCError messages including SQL error details, file paths, stack traces, or internal IDs sent to frontend
3. `logAudit()` storing sensitive field values (password fields, encrypted config) in plaintext
4. `appConfig.upsert` for keys matching `*password*`, `*secret*`, `*token*`, `*key*` where `isEncrypted: false`
5. `logger.info/debug` or `debugLog` logging request bodies, config objects, or user data containing sensitive fields

**Rate limiting & DoS:** 6. Missing rate limiting on: `/trpc/auth.login`, password reset, email verification, LDAP test connection — brute force / enumeration attack vector 7. Storage `put` operation: verify `maxFileSizeMB` limit is enforced BEFORE reading stream into memory — check after buffering = DoS via large upload 8. `findMany` without `take` limit on user-controlled filters — attacker can request all records 9. Manual sync trigger endpoint not rate-limited — each call opens mssql connection pool 10. Complex regex patterns applied to user input without length limits (LDAP searchFilter, AppConfig key validation) — ReDoS risk

---

## Report Format

```
## Luke Security Audit Report
Scanned: <path or 'full monorepo'>
Date: <today>
Trail of Bits: sharp-edges ✅/❌  |  insecure-defaults ✅/❌

### Trail of Bits Findings
[Output from sharp-edges and insecure-defaults if installed]

### Summary
| Area                          | CRITICAL | HIGH | MEDIUM |
|-------------------------------|----------|------|--------|
| Auth & Session & Tokens       |    N     |  N   |   N    |
| IDOR & Input Validation       |    N     |  N   |   N    |
| Sensitive Data & Rate Limiting|    N     |  N   |   N    |

### Findings

**[CRITICAL/HIGH/MEDIUM]** — <title>
File: `path/to/file.ts:line`
Attack scenario: <exact how an attacker exploits this>
Impact: <what they can do>
Fix:
\`\`\`typescript
// proposed fix
\`\`\`
Regression test: <target file + key assertion>

### Promotion to rule
<mandatory section — see §3 of the shared protocol>
```

### Rules

- CRITICAL: auth bypass, data exfiltration, privilege escalation, injection
- HIGH: information disclosure, missing rate limit, weak tokens
- MEDIUM: defense-in-depth gap with moderate exploitability
- No LOW — security either matters or it doesn't
- Every finding needs a concrete attack scenario
- If area is clean: `✅ No findings`
