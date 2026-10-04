---
name: release-check
description: Comprehensive release readiness audit covering security, dependencies, community files, and code quality. Use when asked for a "release check", "release readiness" review, or "pre-release verification".
---

# Release Readiness Audit

Pre-release cross-cutting check: security, dependencies, required community files, and code quality.
Documentation and metadata checks live in `/release-docs-check` — run that separately.

---

## 1. Dependency vulnerabilities

```bash
npm audit --audit-level=high
```

- Confirm zero High / Critical
- If any remain, distinguish direct vs. transitive in the report
- Note whether `npm audit fix` can resolve them

---

## 2. Required community files

Use Glob to confirm each file exists:

| File | Purpose |
|------|---------|
| `LICENSE` | License (required) |
| `README.md` | Project overview (required) |
| `CONTRIBUTING.md` | Contribution guide (required) |
| `SECURITY.md` | Vulnerability reporting policy (required) |
| `CODE_OF_CONDUCT.md` | Code of conduct (recommended) |
| `.env.example` | Environment variable template (required) |

---

## 3. Personal / project-specific info leaks

Grep (excluding `node_modules`, `.next`, `.git`):

- **Personal domains / URLs**: scan source for `\.info`, `\.dev`, `\.me` patterns
- **Personal names / handles**: repository owner names must not be hardcoded in source
- **Project-specific names**: your own project or brand names (e.g., `my-blog-name`) must not remain in source

Allowed locations: `package.json`, `README.md`, `CONTRIBUTING.md`, `SECURITY.md`, `LICENSE`, `_release/`.

---

## 4. Secrets / credential leaks

Grep for these patterns:

- API key prefixes: `sk-`, `AIza`, `ghp_`, `xoxb-`, `AKIA`
- Hardcoded passwords: `password\s*=\s*["'][^"']{8,}`
- Bearer tokens: `Bearer [A-Za-z0-9+/]{20,}`

Read `.env.example` and verify it contains placeholders only.

---

## 5. Code quality

- **Stray `console.log`**: Grep under `app/(admin)/baan-admin/api/`
- **TODO/FIXME/HACK**: Grep under `app/`, `lib/` (minor ones are warnings)
- **Japanese error messages**: confirm API responses under `app/(admin)/baan-admin/api/` do not contain Japanese (exclude translation files like `_lib/i18n.ts`)

---

## 6. Baseline security configuration

- **`.gitignore`**: `.env*`, `data/`, `*.pem`, `.session-secret`, etc. are excluded
- **`package.json`**: `"private": true` is set correctly (appropriate for an application)
- **TypeScript strict**: `tsconfig.json` has `strict: true`

---

## 7. GitHub repository settings (manual)

Cannot be verified from code — confirm manually before release:

- [ ] GitHub Private Vulnerability Reporting enabled (Security tab)
- [ ] Default branch is `main`
- [ ] Branch protection rules set up (if required)

---

## Output format

Clean: `✅ OK`
Issue: `❌ description (file:line)`
Warning: `⚠️ description`
Manual check: `👤 description`

### Summary format

```
## Release Readiness

| Category | Status |
|----------|--------|
| Dependency vulnerabilities | ✅ / ❌ |
| Required community files | ✅ / ❌ |
| Personal info leaks | ✅ / ❌ |
| Secret leaks | ✅ / ❌ |
| Code quality | ✅ / ⚠️ / ❌ |
| Baseline security | ✅ / ❌ |

### Verdict
🟢 READY / 🟡 CAUTION / 🔴 NOT READY
```
