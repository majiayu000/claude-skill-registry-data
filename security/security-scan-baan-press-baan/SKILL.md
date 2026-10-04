---
name: security-scan
description: Security audit skill for scanning the codebase for vulnerabilities. Use when asked for a "security scan", "security audit", "vulnerability check", or to verify that no secrets are leaking. Optionally scoped with "auth", "api", "deps", or "secrets" (git history + secret pattern scan).
---

# Security Scan

Scan the codebase for security issues and produce a report grouped by severity.

## Scope arguments

With no argument, run the full scan. Otherwise narrow to the listed area.

| Argument | Target |
|----------|--------|
| (none) | Everything |
| `auth` | Authentication / session only |
| `api` | API endpoints only |
| `deps` | Dependencies only |
| `secrets` | Sensitive files and secret leaks only (including git history) |

## Procedure

Work through the checklist below and emit a structured report. When a
scope argument is supplied, run only the matching section.

---

## 1. Authentication and session (`auth`)

Use Grep / Glob / Read to verify:

- **Missing `withAuth` / `withAdminAuth` on admin APIs**
  - Search `app/(admin)/baan-admin/api/**/*.ts` for `export async function GET/POST/PUT/PATCH/DELETE`
  - Flag any handler exported directly without `withAuth` / `withAdminAuth`
  - Exceptions: paths already registered in `skipAuthPaths` (`/api/auth/*`, `/api/setup`)

- **Unnecessary entries in `skipAuthPaths`**
  - Check `skipAuthPaths` in `proxy.ts`
  - Flag paths that should require auth but are accidentally exempted

- **Hardcoded session secrets**
  - No literal `SESSION_SECRET` / `JWT_SECRET` values in source code
  - All access must go through `process.env`

- **JWT / token expiry**
  - Confirm `expiresIn` / explicit expiry is set when tokens are issued under `lib/security/`

---

## 2. Input validation and injection (`api`)

- **SQL injection**
  - Read SQL statements under `lib/db/`
  - No user input interpolated directly into template literals (prepared statements only)
  - Grep for patterns like `SELECT ... WHERE ${userInput}`

- **Path traversal**
  - User-provided paths must pass through `getSecurePath()`
  - Flag `path.join(basePath, userInput)` without further validation

- **XSS**
  - Grep all `dangerouslySetInnerHTML` usages
  - Confirm they are sanitised via `sanitizeHtml()` / `lib/security/html-sanitizer.ts`

- **File uploads**
  - Any `multipart/form-data` endpoint must call `validateFileMagicBytes()`
  - Flag extension-only checks (`endsWith('.jpg')`, etc.)

---

## 3. Secret handling (`api`)

- **Hardcoded secrets**
  - Grep for well-known token prefixes in source: `sk-`, `AIza`, `ghp_`, `Bearer `
  - No API keys, passwords, or tokens as literal strings

- **Information leakage via `console.log`**
  - No `console.log` remaining under `app/(admin)/baan-admin/api/` (`console.error` / `console.warn` are fine)
  - Logged output must not contain session data, API keys, or passwords

- **`.gitignore` coverage**
  - `.env*` (except `.env.example`), `data/`, `*.pem`, `.session-secret`, etc. are excluded

---

## 4. API security (`api`)

- **Missing rate limits**
  - Public endpoints under `app/api/**/*.ts` must apply `checkRateLimit()`
  - A matching preset exists in `RATE_LIMITS` in `lib/security/rate-limit.ts`

- **SSRF**
  - Grep for `fetch(url, ...)` / `axios.get(url)` where `url` is user-provided
  - Must go through `validateSSRFUrl()` (`lib/security/ssrf.ts`)
  - Ensure localhost / 169.254.169.254 / private IP ranges are blocked

- **Secret comparison**
  - No timing-attack-prone `=== token` / `== secret`
  - Must use `safeCompare()` (`lib/security/safe-compare.ts`)

- **Debug endpoints exposed in production**
  - No debug API without a `NODE_ENV !== 'production'` guard
  - Glob for endpoints named `debug`, `test`, `dev`

- **CORS**
  - No unrestricted `Access-Control-Allow-Origin: *` in `next.config.ts` or API routes

---

## 5. Dependencies (`deps`)

- **Run `npm audit`**
  - `npm audit --audit-level=high`
  - Enumerate any High / Critical vulnerabilities

- **License issues**
  - Baan ships under AGPL-3.0-or-later. Flag dependencies whose license is incompatible (e.g. SSPL, BUSL, CC-BY-NC) or stricter than AGPL (e.g. AGPL-only when we ship -or-later)
  - Inspect `package.json` dependencies

---

## 6. Information leakage (`api`)

- **Stack traces in error responses**
  - `catch (error)` blocks must not include `error.stack` in responses
  - Plain `{ error: error.message }` should be avoided without sanitisation

- **Environment variable leaks**
  - Never return `process.env` values directly in responses

---

## 7. Sensitive files and secret leaks (`secrets`)

Verify that no sensitive information has been committed to the repo.
Run all four stages with the **Bash tool**.

### Stage 1 — files currently tracked

```bash
git ls-files | grep -iE '\.(env|pem|key|p12|pfx|crt|cer|jks)$|\bsecret\b|credential|\.session-secret'
```

- Any match under git tracking → 🔴 Critical
- Exclude `.env.example` / `.env.sample` / `.env.template` (intended to be public)

### Stage 2 — sensitive files in git history

```bash
git log --all --oneline --diff-filter=A -- \
  '*.env' '*.env.local' '*.env.production' '*.env.development' \
  '.session-secret' 'credentials.json' '*-credentials*.json' \
  '*.pem' '*.key' '*.p12' '*.pfx' 'integrations.json'
```

- Any hit → 🔴 Critical (even if the file was later deleted, it is still in history)
- Inspect hits with `git show --stat <hash>`

### Stage 3 — secret string scan across git history

Search added diffs directly, including deleted commits. Target the **last 6 months**.
Every hit must be verified with Read or `git show <hash>` before reporting (watch for false positives).

#### 3a. Known service prefixes

```bash
git log --all -p --since="6 months ago" | grep -E '^\+.*(cms_live_|sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{36}|AIza[A-Za-z0-9_\-]{35}|xoxb-[0-9]{9,}-[A-Za-z0-9]+|AKIA[A-Z0-9]{16})'
```

| Pattern | Meaning |
|---------|---------|
| `cms_live_...` | Baan CMS API key |
| `sk-[A-Za-z0-9]{20,}` | OpenAI API key |
| `ghp_[A-Za-z0-9]{36}` | GitHub Personal Access Token |
| `AIza[A-Za-z0-9_\-]{35}` | Google API key |
| `xoxb-...` | Slack bot token |
| `AKIA[A-Z0-9]{16}` | AWS Access Key ID |

#### 3b. Variable assignment plus long string (prefix-agnostic)

Catches keys whose prefix you don't know. Secrets are typically 20+ alphanumeric characters assigned to a variable.

```bash
git log --all -p --since="6 months ago" | grep -E '^\+.*(key|token|secret|password|credential|api_key|apiKey|access_key)\s*[=:]\s*["'"'"']?[A-Za-z0-9+/\-_]{20,}'
```

#### 3c. JWT tokens

```bash
git log --all -p --since="6 months ago" | grep -E '^\+.*eyJ[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+'
```

#### 3d. High-entropy long strings (wide net)

Detects added lines containing 40+ character Base64/Hex strings. False positive rate is high (hashes, encoded content) but it catches secrets in unknown formats.

```bash
git log --all -p --since="6 months ago" | grep -E '^\+.*[A-Za-z0-9+/]{40,}={0,2}' | grep -v -E '(node_modules|dist/|\.lock|package-lock|yarn\.lock|[0-9a-f]{40} )'
```

For each hit, check whether the long string follows `=` / `:` or whether the variable name suggests a credential.

#### Scan checklist

- [ ] No commit diff contains a real API key
- [ ] No `.env` file contents live in history
- [ ] No JWT / Bearer tokens in history
- [ ] No long random strings assigned to credential-named variables
- [ ] **If a secret ever appeared: record the commit hash and strongly advise the user to rotate (revoke) the key** — removing from history does NOT invalidate the credential

> **Note:** Proper scanning should use `gitleaks` or `truffleHog` with entropy analysis. The commands above are a manual baseline.

### Stage 4 — hardcoded secrets in current source (HEAD)

Target: whole project (exclude `node_modules`, `.next`, `.next-test`, `dist`).

```bash
grep -r --include="*.ts" --include="*.tsx" --include="*.js" --include="*.json" \
  -E 'sk-[A-Za-z0-9]{20,}|AIza[A-Za-z0-9_\-]{35}|ghp_[A-Za-z0-9]{36}|AKIA[A-Z0-9]{16}|-----BEGIN [A-Z ]*PRIVATE KEY-----' \
  . --exclude-dir=node_modules --exclude-dir=.next --exclude-dir=.next-test --exclude-dir=dist \
  -l
```

### Stage 5 — `.gitignore` coverage

Run `cat .gitignore` and confirm the following are excluded:

| Pattern | Reason |
|---------|--------|
| `.env` / `.env.*` (except `.env.example`) | Environment variables |
| `data/` | SQLite DB files |
| `.session-secret` | Session secret |
| `*.pem`, `*.key`, `*.p12` | Private keys |
| `credentials.json`, `*-credentials*.json` | Service account keys |
| `integrations.json` | May contain API keys |

### Severity table

| Finding | Severity |
|---------|----------|
| Sensitive file currently tracked by git | 🔴 Critical |
| Sensitive file present in past commits (even if deleted) | 🔴 Critical |
| Secret pattern embedded in source | 🔴 Critical |
| `.gitignore` coverage gap | 🟠 High |
| Non-placeholder value in `.env.example` | 🟡 Medium |

---

## Output format

Produce the report in this format:

```
## Security diagnostic report

Date: YYYY-MM-DD
Scope: full / auth / api / deps / secrets

### Summary
| Severity | Count |
|----------|-------|
| 🔴 Critical | N |
| 🟠 High     | N |
| 🟡 Medium   | N |
| 🟢 Low      | N |
| ✅ Clean    | N items |

### Details

#### 🔴 Critical

**[title]**
- File: `path/to/file.ts:line`
- Issue: concrete description
- Fix: code snippet or step-by-step

#### 🟠 High
...

#### 🟡 Medium
...

### ✅ Verified clean
- Auth: `withAuth` applied to every Admin API
- ...

### Overall verdict
🟢 CLEAN / 🟡 CAUTION / 🔴 ACTION REQUIRED
```

---

## Ground rules

- This scan is **read-only**. Never modify code.
- Report findings; never silently fix. The user decides.
- Run `npm audit` via the Bash tool (`npm audit --audit-level=high --json`).
- For every suspicious hit, Read the actual code before reporting (avoid false positives).
