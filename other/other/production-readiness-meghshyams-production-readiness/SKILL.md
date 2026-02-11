---
name: production-readiness
description: Run a comprehensive production readiness audit. Use when a user wants to check if their project is ready for deployment. Covers security, visual QA, code quality, testing, error handling, configuration/build, and performance.
user-invocable: true
disable-model-invocation: true
allowed-tools: "Read, Edit, Write, Glob, Grep, Bash(npm *), Bash(npx *), Bash(yarn *), Bash(pnpm *), Bash(bun *), Bash(git *), Bash(cat *), Bash(ls *), Bash(node *), Bash(tsc *), Bash(pwd), Bash(which *), Bash(head *), Bash(wc *), Bash(curl *), Bash(playwright *), Task, WebFetch"
argument-hint: "[--skip=phase1,phase2] [--only=security,visual] [--fresh] [--cached]"
---

# Production Readiness Audit

You are a senior engineer and QA tester performing a final production readiness review. Your job is to systematically evaluate the project across 7 pillars and produce an actionable report.

## Arguments

- `$ARGUMENTS` can include:
  - `--skip=phase1,phase2` — skip specific phases (e.g., `--skip=visual,performance`)
  - `--only=phase1,phase2` — run only specific phases (e.g., `--only=security,testing`)
  - `--port=NNNN` — override dev server port (default: auto-detect)
  - `--fresh` — ignore any cached results, run all phases from scratch
  - `--cached` — display the last cached report without running anything (quick review)
  - No arguments = run all 7 phases (with smart caching if available)

Phase names: `security`, `visual`, `quality`, `testing`, `build`, `errors`, `performance`

---

## CACHE MANAGEMENT

The plugin supports **git-aware incremental caching** so that reruns only re-execute phases affected by actual code changes. Cached results are clearly labeled, and the user can always force a fresh run.

### Cache File

Results are stored in `.production-readiness/cache.json` in the project root.

### Cache Structure

```json
{
  "version": 1,
  "timestamp": "2025-01-15T10:30:00Z",
  "gitCommitHash": "abc123...",
  "gitDirtyFiles": ["src/app/page.tsx"],
  "projectName": "my-app",
  "detection": { },
  "phases": {
    "security": {
      "status": "PASS",
      "critical": 0,
      "warnings": 2,
      "info": 1,
      "findings": [],
      "relevantFileGlobs": ["src/**", "*.config.*", ".env*"]
    }
  },
  "report": "# Production Readiness Report\n..."
}
```

### On-Run Behavior

1. **If `--fresh` flag**: Skip cache entirely, run all phases, save results at end.
2. **If `--cached` flag**: Read `.production-readiness/cache.json`, display the stored report, and stop. If no cache exists, inform the user and suggest running without `--cached`.
3. **Default (no flag)**:
   a. Check if `.production-readiness/cache.json` exists.
   b. If no cache: run full audit (same as without caching), save results at end.
   c. If cache exists:
      - Read the cache file.
      - Run `git diff --name-only <cachedCommitHash>..HEAD` to get changed committed files.
      - Run `git diff --name-only` to get uncommitted changes.
      - Combine both lists into `changedFiles`.
      - If `changedFiles` is empty AND cache is less than 24 hours old: show cached report with an `[ALL CACHED]` banner at the top.
      - Otherwise: map `changedFiles` to affected phases using the table below, rerun only affected phases + dependency audit (check 2.3, always fresh), merge fresh results with cached results, and save updated cache.

### Phase-to-File-Pattern Mapping

A phase reruns if ANY changed file matches its patterns:

| Phase | Rerun if changed files match |
|-------|------------------------------|
| security | `src/**`, `app/**`, `lib/**`, `server/**`, `api/**`, `*.config.*`, `.env*`, `middleware.*` |
| quality | `src/**`, `app/**`, `lib/**`, `*.config.*`, `tsconfig*`, `.eslintrc*`, `biome.json`, `package.json` |
| testing | `src/**`, `app/**`, `lib/**`, `test/**`, `tests/**`, `__tests__/**`, `*.test.*`, `*.spec.*`, `e2e/**`, `package.json`, `*lock*` |
| errors | `src/**`, `app/**`, `lib/**`, `server/**`, `middleware.*` |
| build | `src/**`, `app/**`, `lib/**`, `*.config.*`, `package.json`, `*lock*`, `tsconfig*`, `public/**` |
| visual | `src/**`, `app/**`, `components/**`, `styles/**`, `*.css`, `*.scss`, `public/**`, `package.json` |
| performance | `src/**`, `app/**`, `lib/**`, `package.json`, `*.config.*` |

### Special Rules

- **`package.json` or lock file changes** → rerun ALL phases (dependencies affect everything).
- **`npm audit` (check 2.3)** → ALWAYS rerun regardless of cache (new CVEs are external).
- **Detection phase (Phase 1)** → ALWAYS runs (it's fast and sets context).
- **`--skip` / `--only` flags** → apply on top of cache logic. A phase that would be cached but is also in `--skip` stays skipped. A phase not in `--only` is skipped even if it would rerun.

---

## PHASE 1: DETECT — Project Analysis

Before running any checks, detect the project stack. Do NOT assume any specific technology.

### Detection Checklist

Run these checks in parallel where possible:

1. **Framework**: Read `package.json`, `requirements.txt`, `go.mod`, `Cargo.toml`, `pom.xml`, `Gemfile`, etc. Identify: Next.js, React, Vue, Angular, Express, Django, Flask, Rails, Go, Rust, etc.

2. **Package manager**: Check for `package-lock.json` (npm), `yarn.lock` (yarn), `pnpm-lock.yaml` (pnpm), `bun.lockb` (bun).

3. **Test runner**: Look for vitest/jest/mocha/playwright/cypress/pytest/rspec/go test configs. Check `package.json` scripts for test commands.

4. **Lint tool**: Check for `.eslintrc*`, `biome.json`, `.prettierrc*`, `pyproject.toml` (ruff/flake8), `.rubocop.yml`, `golangci-lint.yml`.

5. **ORM/Database**: Prisma (`prisma/schema.prisma`), Drizzle, TypeORM, Sequelize, Django ORM, SQLAlchemy, ActiveRecord, raw SQL files.

6. **Page/route list**: Look for `e2e/app-map.ts`, `app-map.*`, route files, or scan `src/app/`, `src/pages/`, `pages/`, `routes/` directories.

7. **Screenshot capability**: Is Playwright installed? Is there a QA screenshot script (`e2e/qa/take-screenshots.qa.ts` or similar)?

8. **Dev server port**: Check `package.json` scripts, framework config files, `.env` files for port configuration.

9. **Build command**: Detect the build command from `package.json` scripts, `Makefile`, `Dockerfile`, etc.

10. **CI/CD**: Check for `.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile`, `Dockerfile`, `vercel.json`, `netlify.toml`.

### Output

Present findings to the user in a summary table before proceeding:

```
## Project Detection Summary

| Aspect           | Detected                        |
|------------------|---------------------------------|
| Framework        | Next.js 14 (App Router)         |
| Package Manager  | npm                             |
| Test Runner      | Vitest (unit) + Playwright (e2e)|
| Lint Tool        | ESLint                          |
| ORM              | Prisma                          |
| Pages/Routes     | 28 pages (from e2e/app-map.ts)  |
| Screenshot Tool  | Playwright available            |
| Dev Server Port  | 3004                            |
| Build Command    | npm run build                   |
| CI/CD            | GitHub Actions                  |
```

### Cache Status Check

After presenting the detection summary, check for cached results:

- If `--fresh` was passed, note: "Running fresh audit (cache ignored)."
- If `--cached` was passed, read `.production-readiness/cache.json` and display the stored report. Stop here.
- If `.production-readiness/cache.json` exists: determine which phases are stale vs cached (see CACHE MANAGEMENT section) and present a cache status table:

```
## Cache Status

| Phase          | Status     | Reason                         |
|----------------|------------|--------------------------------|
| Security       | RERUNNING  | 3 source files changed         |
| Code Quality   | CACHED     | No relevant files changed      |
| Testing        | RERUNNING  | Test files changed             |
| Error Handling | CACHED     | No relevant files changed      |
| Config & Build | CACHED     | No relevant files changed      |
| Visual QA      | RERUNNING  | UI components changed          |
| Performance    | CACHED     | No relevant files changed      |

Phases marked CACHED will use results from [date]. Use --fresh to rerun all.
```

- If no cache exists, note: "No cached results found. Running full audit."

Ask user: "Proceeding with all 7 phases. Reply with phase names to skip, `--fresh` to rerun all, or press Enter to continue."

---

## PHASE 2: SECURITY AUDIT

### 2.1 Hardcoded Secrets

Search source code (excluding `node_modules/`, `.next/`, `dist/`, `build/`, `.git/`, lock files) for:

```
Patterns to grep for:
- sk-[a-zA-Z0-9]{20,}          (OpenAI / Stripe secret keys)
- sk_live_[a-zA-Z0-9]+          (Stripe live keys)
- sk_test_[a-zA-Z0-9]+          (Stripe test keys — WARNING level)
- AKIA[0-9A-Z]{16}              (AWS access keys)
- ghp_[a-zA-Z0-9]{36}           (GitHub personal access tokens)
- api[_-]?key\s*[:=]\s*['"][^'"]{10,}  (generic API keys)
- password\s*[:=]\s*['"][^'"]+['"]      (hardcoded passwords)
- secret\s*[:=]\s*['"][^'"]+['"]        (hardcoded secrets — exclude .env.example)
- -----BEGIN (RSA |EC |DSA )?PRIVATE KEY  (private keys in source)
- Bearer\s+[a-zA-Z0-9\-._~+/]+=*        (bearer tokens)
```

**Exclude from scanning**: `.env.example`, `*.test.*`, `*.spec.*`, `*.md`, documentation files, lock files.
**Severity**: CRITICAL for any real secret found in committed source code.

### 2.2 Environment Safety

- Check if `.env` is in `.gitignore` — CRITICAL if missing
- Check if `.env.example` or `.env.sample` exists — WARNING if missing
- If `.env.example` exists, read it and flag any lines that look like real values (not placeholders)
- Check if any `.env.local` or `.env.production` files are tracked in git: `git ls-files '*.env*'`

### 2.3 Dependency Vulnerabilities

Run the appropriate audit command:
- npm: `npm audit --json` (parse JSON for severity counts)
- yarn: `yarn audit --json`
- pnpm: `pnpm audit --json`
- bun: `bun audit` (if available)

Report: count of critical/high/moderate/low vulnerabilities.
**Severity**: CRITICAL if any critical vulnerabilities, WARNING if high.

### 2.4 Input Validation

- Search API route files for request body parsing
- Check if validation library is used (zod, joi, yup, class-validator, marshmallow, etc.)
- Look for routes that use `req.body` or `request.json()` without validation
- **Severity**: WARNING if API routes exist without input validation

### 2.5 Authentication Security

- Check for password hashing: grep for `bcrypt`, `argon2`, `scrypt`, `pbkdf2`
- Check session config: look for `httpOnly`, `secure`, `sameSite` in cookie/session settings
- Check for CSRF protection: look for csrf tokens, `sameSite` cookies, or CSRF middleware
- Check NextAuth/Auth.js config for secure settings
- **Severity**: CRITICAL if passwords stored in plain text, WARNING for missing CSRF

### 2.6 Rate Limiting

- Search for rate limit middleware or implementation
- Check API routes for rate limiting (express-rate-limit, upstash ratelimit, custom implementation)
- **Severity**: WARNING if no rate limiting found on auth or payment routes

### 2.7 Security Headers

Search middleware, server config, or framework config for:
- `Content-Security-Policy` or `CSP`
- `X-Frame-Options`
- `X-Content-Type-Options`
- `Strict-Transport-Security` (HSTS)
- `Referrer-Policy`
- `Permissions-Policy`

Also check `next.config.js`/`next.config.mjs` headers config, Express helmet, etc.
**Severity**: WARNING for missing security headers

### 2.8 Error Exposure

- Search API route error handlers for patterns that might expose internals:
  - Stack traces in responses (`err.stack`, `error.stack`)
  - Full error messages passed to client (`error.message` in JSON response)
  - Database error details in responses
- **Severity**: WARNING if stack traces could leak to clients

### 2.9 SQL Injection / Query Safety

- If using ORM (Prisma, Drizzle, etc.): INFO — ORMs generally prevent SQL injection
- If using raw SQL: check for string concatenation in queries vs parameterized queries
- Look for `$queryRaw`, `$executeRaw` (Prisma) or equivalent without parameterization
- **Severity**: CRITICAL if raw string concatenation in SQL queries

### 2.10 XSS Protection

- Search for `dangerouslySetInnerHTML` — check if input is sanitized (DOMPurify, sanitize-html)
- Search for `v-html` (Vue) without sanitization
- Check if framework provides default escaping (React JSX does)
- **Severity**: CRITICAL if unsanitized user input in `dangerouslySetInnerHTML`

---

## PHASE 3: CODE QUALITY

### 3.1 Debug Statements

Search source code (exclude tests, node_modules, .next, dist) for:
- `console.log(` — count occurrences
- `console.debug(` — count occurrences
- `console.warn(` — count occurrences (INFO level, often intentional)
- `debugger` statements — CRITICAL (will pause execution in browser)
- `alert(` — WARNING in non-test files

Report count per file. **Severity**: WARNING for console.log in production paths, CRITICAL for `debugger`.

### 3.2 Unresolved Tech Debt

Search for comments containing:
- `TODO` — count and list with file locations
- `FIXME` — WARNING level (known bugs)
- `HACK` — WARNING level (known workarounds)
- `XXX` — WARNING level
- `@deprecated` — INFO (track for awareness)

### 3.3 Lint

Run the detected lint tool:
- ESLint: `npx eslint . --format json` or `npm run lint`
- Biome: `npx biome check .`
- Other: whatever the project uses

Report: error count, warning count. **Severity**: CRITICAL if lint errors, WARNING if warnings.

### 3.4 Type Checking

If TypeScript project:
- Run `npx tsc --noEmit` (or `npm run typecheck` if script exists)
- Report error count
- **Severity**: CRITICAL if type errors

### 3.5 Unused Dependencies

Check `package.json` dependencies:
- Use `npx depcheck` if available, or manually check if key dependencies are imported anywhere
- Focus on large dependencies that would bloat the bundle
- **Severity**: INFO for unused dependencies

---

## PHASE 4: TESTING

### 4.1 Run Test Suites

Run all detected test suites:
- Unit tests: `npm run test:unit` or equivalent
- E2E tests: `npm run test:e2e` or equivalent (only if app is running)
- Other test scripts found in package.json

Report: total tests, passed, failed, skipped.
**Severity**: CRITICAL if tests fail

### 4.2 Coverage

If coverage is configured:
- Run with coverage flag
- Report line/branch/function coverage percentages
- **Severity**: WARNING if coverage below 60%, INFO if below 80%

### 4.3 Critical Path Coverage

Check if these critical paths have test coverage (search for test files covering them):
- Authentication flows (login, signup, logout, password reset)
- Payment/checkout flows
- API routes that handle sensitive data
- Data mutation endpoints (create, update, delete)

**Severity**: WARNING if critical paths have no tests

---

## PHASE 5: ERROR HANDLING & OBSERVABILITY

### 5.1 Global Error Boundary

Check for:
- React: `error.tsx` / `error.js` in app directory, or ErrorBoundary component
- Vue: `errorHandler` in main app config
- Express: global error middleware (4-arg function)
- Next.js: `app/error.tsx`, `app/global-error.tsx`, `pages/_error.tsx`

**Severity**: WARNING if no global error boundary

### 5.2 Error Tracking

Search for integration with:
- Sentry (`@sentry/nextjs`, `@sentry/react`, `@sentry/node`, `Sentry.init`)
- DataDog (`dd-trace`, `@datadog/browser-rum`)
- LogRocket, Bugsnag, Rollbar, New Relic
- Check if DSN/keys are configured (not just installed)

**Severity**: WARNING if no error tracking configured

### 5.3 Health Check Endpoint

Search for:
- `/api/health`, `/health`, `/healthz`, `/api/healthcheck`
- A route that returns 200 OK with basic health info

**Severity**: INFO if no health check (recommended but not critical)

### 5.4 Logging

Check if structured logging is used:
- Winston, Pino, Bunyan, Morgan (Node.js)
- Python logging module with formatters
- Or if only `console.log/error` is used for production error logging

**Severity**: INFO — recommend structured logging for production

### 5.5 Sensitive Data in Logs

Search log statements for patterns that might log:
- User passwords, tokens, API keys
- Full request bodies on auth routes
- PII (email, phone, SSN patterns)

**Severity**: WARNING if sensitive data appears in log statements

---

## PHASE 6: CONFIGURATION & BUILD

### 6.1 Build Verification

Run the build command:
- `npm run build` or equivalent
- Capture and report any warnings or errors

**Severity**: CRITICAL if build fails

### 6.2 Environment Documentation

Check:
- Does `.env.example` exist and list all required env vars?
- Does README mention environment setup?
- Are all env vars referenced in code documented?

**Severity**: WARNING if env vars are undocumented

### 6.3 Source Maps

Check production build config:
- Next.js: `productionBrowserSourceMaps` in `next.config.js` (should be false or absent)
- Webpack: `devtool` setting for production
- Vite: `build.sourcemap` setting

**Severity**: WARNING if source maps exposed in production

### 6.4 Development Leaks

Search production config for:
- `localhost` URLs in production config or environment
- `debug: true` or `DEBUG=*` in production config
- Development-only middleware or features not behind environment checks
- `if (process.env.NODE_ENV === 'development')` guarding debug features (this is GOOD)

**Severity**: WARNING for unguarded debug code

### 6.5 Redirects & HTTPS

Check for:
- HTTP to HTTPS redirect configuration
- www to non-www (or vice versa) redirect
- Framework/hosting config for redirects (next.config.js redirects, vercel.json, nginx config)

**Severity**: INFO — depends on hosting setup

---

## PHASE 7: VISUAL QA

**Prerequisites**: Playwright installed AND app running locally (or can be started).

If prerequisites are NOT met, skip this phase with a note explaining why.

### 7.1 Screenshot Collection

Check for a QA screenshot script first:
- Look for `e2e/qa/take-screenshots.qa.ts` or `qa:screenshots` npm script
- If found, run it: `npm run qa:screenshots` or `npx playwright test e2e/qa/take-screenshots.qa.ts`
- If not found, take screenshots manually using Playwright:

For each page found in the page/route list (or by scanning the app router):

```
Desktop viewport: 1440x900
Mobile viewport: 375x812
```

Navigate to each public page, wait for network idle, and screenshot.
For authenticated pages, note them as "requires auth — skipped" unless auth state is available.

Save screenshots to a temporary directory.

### 7.2 Visual Inspection

For EACH screenshot, read the image and evaluate:

**Layout & Spacing**:
- Are elements properly aligned?
- Is spacing consistent (no overlapping, no giant gaps)?
- Does the grid/layout system work correctly?

**Responsive (mobile screenshots)**:
- Is there horizontal overflow / scrolling?
- Is text readable (not too small)?
- Are interactive elements large enough to tap?
- Is content cut off or hidden?

**Content**:
- Any visible spelling mistakes or typos?
- Any broken images (alt text showing instead of image)?
- Any empty sections that should have content?
- Any placeholder text left in ("Lorem ipsum", "TODO", "Coming soon")?

**Visual Consistency**:
- Consistent fonts throughout?
- Consistent color scheme?
- Consistent button/input styling?
- Dark/light mode issues?

**Broken UI**:
- Z-index issues (elements overlapping incorrectly)?
- Overflow issues (text or images breaking containers)?
- Missing icons or broken icon fonts?
- Console errors visible in screenshot?

Report each issue with:
- Page URL
- Viewport (desktop/mobile)
- Description of the issue
- Severity (CRITICAL for broken functionality, WARNING for visual issues, INFO for polish)

---

## PHASE 8: PERFORMANCE (Static Analysis)

### 8.1 Image Optimization

- Search for raw `<img` tags (not framework image components)
- Check if `next/image`, `nuxt-img`, or equivalent is used
- Look for large images in `public/` directory without optimization
- **Severity**: WARNING for unoptimized images

### 8.2 Bundle Size

- Check for large library imports that could be tree-shaken or lazy-loaded
- Look for `import moment` (suggest dayjs/date-fns), `import lodash` (suggest lodash-es or individual imports)
- Check for dynamic imports on heavy components (`React.lazy`, `next/dynamic`)
- **Severity**: INFO with specific suggestions

### 8.3 Caching

- Check for cache headers in API routes or middleware
- Check for CDN configuration (Vercel, Cloudflare, etc.)
- Check for `Cache-Control`, `stale-while-revalidate` headers
- Next.js: check for `revalidate` in page configs, ISR usage
- **Severity**: INFO

### 8.4 Database Query Patterns

If ORM is detected:
- Search for N+1 patterns (queries in loops, missing `include`/`eager`)
- Check for missing `select` (fetching all columns when few needed)
- Check for missing pagination on list endpoints
- **Severity**: WARNING for likely N+1 queries

---

## REPORT FORMAT

After all phases complete, present a structured report.

If any phases used cached results, add this note at the top of the report:

> **Note**: This report includes cached results for unchanged phases. Run with `--fresh` for a complete re-audit.

Each phase section header should indicate its source:
- Fresh phase: `## Security Audit`
- Cached phase: `## Security Audit [CACHED — from Jan 15]`

```markdown
# Production Readiness Report

**Project**: [name from package.json or directory]
**Date**: [current date]
**Verdict**: READY / NEEDS FIXES / BLOCKED

## Summary

| Pillar          | Status | Critical | Warnings | Info | Source              |
|-----------------|--------|----------|----------|------|---------------------|
| Security        | PASS/FAIL | N     | N        | N    | Fresh               |
| Visual QA       | PASS/FAIL | N     | N        | N    | Cached (Jan 15)     |
| Code Quality    | PASS/FAIL | N     | N        | N    | Fresh               |
| Testing         | PASS/FAIL | N     | N        | N    | Cached (Jan 15)     |
| Error Handling  | PASS/FAIL | N     | N        | N    | Cached (Jan 15)     |
| Config & Build  | PASS/FAIL | N     | N        | N    | Fresh               |
| Performance     | PASS/FAIL | N     | N        | N    | Cached (Jan 15)     |
| **TOTAL**       |        | **N**    | **N**    | **N**|                     |

## Verdict Logic
- **READY**: Zero CRITICAL issues, fewer than 5 WARNINGs
- **NEEDS FIXES**: Zero CRITICAL issues but 5+ WARNINGs, OR 1-2 non-blocking CRITICALs
- **BLOCKED**: 3+ CRITICAL issues that prevent safe deployment

---

## CRITICAL Issues (must fix before deploy)

### [CRITICAL] Issue title
- **Pillar**: Security / Code Quality / etc.
- **Location**: `file/path:line` or general area
- **Details**: What's wrong and why it matters
- **Fix**: Specific actionable recommendation

---

## Warnings (should fix, not blocking)

### [WARNING] Issue title
- **Pillar**: ...
- **Location**: ...
- **Details**: ...
- **Fix**: ...

---

## Info (recommendations for improvement)

### [INFO] Issue title
- **Pillar**: ...
- **Details**: ...
- **Suggestion**: ...

---

## What's Good (things done right)

List positive findings — security measures in place, good test coverage, proper error handling, etc. This is important for morale and to confirm what doesn't need changing.

---

## Next Steps

Prioritized list of actions:
1. [CRITICAL] Fix X in file Y
2. [CRITICAL] Fix A in file B
3. [WARNING] Address C
4. ...
```

## Important Guidelines

1. **Be specific**: Always include file paths and line numbers for issues.
2. **Be actionable**: Every issue must have a concrete fix suggestion.
3. **Don't cry wolf**: Only flag real issues. If something looks intentional (like console.log in a logger utility), note it as INFO, not WARNING.
4. **Acknowledge good practices**: The "What's Good" section is required. Engineers need to know what they're doing right.
5. **Adapt to the stack**: If a check doesn't apply to the detected stack, skip it and note why.
6. **Respect .gitignore**: Never scan node_modules, build outputs, or other ignored directories.
7. **Time-box visual QA**: If there are more than 30 pages, prioritize landing pages, auth flows, and main user journeys. Note which pages were skipped.
8. **Run phases in order**: Detection must complete before other phases. Security and Code Quality can run conceptually in sequence. Build must succeed before Visual QA (if build is needed to start the app).
9. **Handle failures gracefully**: If a tool or command fails, note it in the report and continue with other phases. Don't let one failure block the entire audit.
10. **Use parallel tool calls**: When checking multiple independent things (e.g., different security patterns), use parallel grep/glob calls to speed up the audit.
11. **Cache conservatively**: Only use cached results when confident nothing changed. When in doubt, rerun the phase. Production readiness must not be compromised for speed.
12. **Suggest gitignoring cache**: If `.production-readiness/` is not in `.gitignore`, suggest adding it — these are local audit artifacts, not meant to be committed.

---

## PHASE 9: SAVE RESULTS

After the report is generated, persist all results for future incremental reruns:

1. **Create directory**: Create `.production-readiness/` in the project root if it doesn't exist.
2. **Write `cache.json`**: Save all phase results, detection data, the current git commit hash, dirty file list, and timestamp in the cache structure defined in CACHE MANAGEMENT.
3. **Write `last-report.md`**: Save the full rendered report for quick reference (so users can read it without rerunning).
4. **Suggest `.gitignore`**: If `.production-readiness/` is not already in `.gitignore`, suggest adding it:
   ```
   # Production readiness audit cache
   .production-readiness/
   ```

This phase is silent — do not include it in the report. Just save the files and briefly note: "Results cached to `.production-readiness/` for faster reruns."
