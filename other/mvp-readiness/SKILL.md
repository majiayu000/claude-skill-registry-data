---
name: mvp-readiness
description: Runs a structured MVP quality-gate audit covering stability, security, logging, docs, and implementation integrity. Reports pass/fail with evidence.
argument-hint: "[--quick]"
allowed-tools: Bash, Read, Glob, Grep
---

# MVP Readiness Audit

Run a structured quality-gate audit before declaring any project an MVP. Check every item. Report pass/fail with evidence. Flag blockers.

## Instructions

**Two modes:**
- **Full audit** (default `/mvp-readiness`): complete checklist across all 8 sections. Use before launch.
- **Quick scan** (`/mvp-readiness --quick`): checks only the 5 hard blockers. Completes in under 30 seconds. Use during daily development.

If `--quick` is passed, skip to the [Quick Scan](#quick-scan) section and stop after producing the quick scan output. Do not run the full checklist.

---

## Quick Scan

Run each of the following 5 checks using Bash or Grep — do not read files individually. Report results in the compact output format below.

### Check 1 — Secret Scan

```bash
grep -rn "password\s*=\s*['\"]" --include="*.js" --include="*.ts" --include="*.py" --exclude-dir=node_modules .
```

Adapt the file extensions for the detected language. **FAIL** if any match is found outside of test files (`*.test.*`, `*.spec.*`, `tests/`, `__tests__/`).

### Check 2 — README Exists

Check that `README.md` or `readme.md` exists and is greater than 100 bytes. **FAIL** if the file is missing or empty.

### Check 3 — External Call Error Handling

```bash
grep -rn "fetch(\|axios\.\|\.query(\|\.connect(" --include="*.js" --include="*.ts" . | grep -v "try\|catch\|then\|rescue"
```

This is a rough heuristic. **FAIL** if more than 5 uncovered calls are found.

### Check 4 — No Secrets in Git History

```bash
git log --all --oneline -- "*.env" 2>/dev/null | head -5
```

**FAIL** if any `.env` files appear in the git history.

### Check 5 — Placeholder Code

```bash
grep -rn "TODO\|FIXME\|stub\|placeholder\|impl later" --include="*.js" --include="*.ts" --include="*.py" --exclude-dir=node_modules . | grep -v "test\|spec"
```

**FAIL** if any results are found in non-test files.

### Quick Scan Output Format

Produce a compact result in this exact format:

```
## MVP Quick Scan — <project> — <date>

✓ Secret scan: PASSED
✗ README: FAILED — README.md not found
✓ Error handling: PASSED (heuristic)
✓ Git history: PASSED
⚠ Placeholder code: WARNING — 3 TODOs in src/ (non-blocking)

Status: NOT READY — 1 blocker. Run /mvp-readiness for full audit.
```

Use `✓` for PASSED, `✗` for FAILED (blocker), and `⚠` for WARNING (non-blocking). The status line must say `READY` only if all 5 checks pass.

---

## Full Audit

Run all steps below, then evaluate every item in the MVP Checklist.

1. Use Read to load `README.md` and any files found in `docs/`.

2. Use Glob to discover the project structure:
   - Source files: `src/**/*`, `lib/**/*`, `app/**/*` (adapt to the project layout)
   - Config files: `package.json`, `pyproject.toml`, `go.mod`, `.env.example`, `.gitignore`
   - Entry points: `index.*`, `main.*`, `server.*`, `app.*`

3. Use Grep to check for common problems across the codebase:
   - Hardcoded secret patterns: `password\s*=`, `api_key\s*=`, `SECRET\s*=`, `token\s*=` (case-insensitive, exclude `.env.example`)
   - Placeholder strings: `TODO`, `FIXME`, `impl later`, `stub`, `placeholder` (in source files only)
   - Missing error handling: look for calls to external systems (fetch, axios, db., fs., open(), connect()) without adjacent try/catch or .catch()

4. Use Read to check `.gitignore` for `.env` entries.

5. Use Grep to search `README.md` for setup instructions (clone, install, run).

6. Detect package manifests (`package.json`, `requirements.txt`, `go.mod`, `Gemfile`, `composer.json`) and inspect dependency versions:
   - Flag any version set to `*`, `latest`, or an unbounded range such as `>=X` with no upper bound.
   - Flag packages with no updates in 2+ years — look for deprecation notices in the package README or `description` field.
   - Flag known abandoned or replaced packages (e.g. `request` → use `axios`/`fetch`; `moment` → use `date-fns`/`dayjs`).
   - Confirm a lockfile is present and committed (`package-lock.json`, `yarn.lock`, `poetry.lock`, `go.sum`, `Gemfile.lock`, etc.).

7. Check for performance red flags:
   - If a `webpack.config.*` or `vite.config.*` exists, note whether bundle size budgets are configured; flag if estimated bundle likely exceeds 500 KB.
   - Grep list/find/getAll endpoint handlers for array returns that lack `limit`, `offset`, or `page` parameters (missing pagination).
   - Grep for `readFileSync` and `execSync` outside of config-loading or startup modules — flag any found in async request handlers.
   - Scan schema files (`.sql`, `prisma/schema.prisma`, `**/models.*`) for foreign key columns that lack a corresponding index definition.

8. For each checklist item below, determine: **PASS**, **FAIL**, or **N/A** (with written justification).

9. Produce the MVP Readiness Report (see Output Format).

## MVP Checklist

### 1. Stability & Error Handling
- [ ] All external calls (DB, API, file system) have try/catch/except blocks or equivalent error checks.
- [ ] The application does not crash on invalid input — provides a clean error message and exits/returns gracefully.
- [ ] Repeated runs do not cause duplicate data or corrupted state (idempotency, where applicable).

### 2. Configuration & Environment
- [ ] The app validates required environment variables or config files on startup and fails fast if missing.
- [ ] No hardcoded "magic strings," URLs, or ports — all moved to config or env.
- [ ] No secrets committed to the repo (`.gitignore` covers `.env` and credential files; Grep finds no secrets in code).

### 3. Logging & Observability
- [ ] Logs include timestamps and severity levels (INFO, WARN, ERROR).
- [ ] No silent failures — every error condition is logged with enough context to debug.

### 4. Security (Golden Rules)
- [ ] All user input (CLI args, HTTP params, file contents) is validated or sanitized before use.
- [ ] The app only requests minimum permissions it needs (least privilege).
- [ ] Sensitive features are off by default unless explicitly configured (secure defaults).

### 5. Documentation & UX
- [ ] README explains how to go from "clone" to "run" in fewer than 3 steps.
- [ ] Help commands (`--help`) or README usage examples are provided.
- [ ] (For web projects) Meets WCAG AA contrast and works on mobile.

### 6. Implementation Integrity
- [ ] No placeholder or "impl later" comments in production code paths.
- [ ] Naming follows camelCase (or the language convention documented in `docs/assumptions.md`).
- [ ] README includes stack, license, and troubleshooting sections.

### 7. Dependency Health
- [ ] All dependency versions are pinned or range-constrained (no `*` or `latest`).
- [ ] No obviously abandoned or deprecated packages in use.
- [ ] A lockfile exists and is committed (`package-lock.json`, `yarn.lock`, `poetry.lock`, etc.).

### 8. Performance Baseline
- [ ] No obvious N+1 query patterns or unindexed foreign keys in schema.
- [ ] List endpoints implement pagination.
- [ ] No synchronous blocking calls in async request handlers.

## Output Format

Produce a markdown report in this exact format:

---

## MVP Readiness Report — <Project Name> — <Date>

### Summary

**Status:** READY / NOT READY
**Blockers:** <count>

### Checklist Results

| # | Section | Item | Status | Evidence |
|---|---------|------|--------|----------|
| 1 | Stability & Error Handling | Error boundaries on all external calls | PASS | All DB calls in src/db.ts wrapped in try/catch |
| 2 | Stability & Error Handling | No crash on invalid input | FAIL | CLI crashes with TypeError on non-numeric --port (src/cli.ts:42) |
| 3 | Configuration & Environment | No hardcoded secrets | PASS | .gitignore covers .env; no secrets found by Grep |
| 4 | Logging & Observability | Logs include timestamps and severity | PASS | Winston logger configured with level and timestamp |
| 5 | Security | All user input validated | FAIL | HTTP query params in src/api/users.ts:18 passed to DB without validation |
| 6 | Documentation & UX | README explains setup in <3 steps | PASS | README has clone/install/run in three numbered steps |
| 7 | Implementation Integrity | No placeholder comments in prod paths | PASS | No TODOs found in src/ |
| 8 | Dependency Health | All versions pinned, no abandoned packages, lockfile committed | FAIL | `moment` detected in package.json; package-lock.json not in repo |
| 9 | Performance Baseline | Pagination on list endpoints, no sync blocking, no unindexed FKs | FAIL | GET /users returns full array without limit/offset (src/api/users.ts:34) |
| ... | | | | |

### Blockers (must fix before MVP)

- [#2] `src/cli.ts:42` — CLI crashes on non-numeric --port. Add input validation before parseInt.
- [#8] Dependency Health — `moment` is abandoned; replace with `date-fns` or `dayjs`. Commit the lockfile.
- [#9] Performance Baseline — GET /users (`src/api/users.ts:34`) returns unbounded array; add `limit`/`offset` query params.

### N/A Items

- [#X] reason (e.g. "No web UI — accessibility check not applicable")

---

The project is **NOT MVP-ready** if any item is FAIL unless explicitly marked N/A with written justification.
