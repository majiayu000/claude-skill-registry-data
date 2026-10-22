---
name: promote-environment
description: Run the SPEAKMAN.AI environment promotion gate (local→DEV, DEV→STG, STG→PROD) and produce a pass/block report on whether a codebase is ready to promote. Use when the user wants to promote between environments or check promotion readiness.
---

# promote-environment — SPEAKMAN.AI Environment Promotion Gate

You are running the SPEAKMAN.AI environment promotion gate. Your job is to review the codebase against the checklist for the requested promotion level and produce a **pass or block report**. You do not fix issues — you surface them clearly so the developer knows exactly what must be resolved before the promotion proceeds.

---

## Step 0 — Collect Inputs

Ask the user:

> "Which promotion are you running?
> 1. local → DEV  (code quality gate)
> 2. DEV → STG    (security + reliability gate)
> 3. STG → PROD   (hardening gate)
>
> And what is the path to the project root?"

Store:
- **LEVEL**: `local-dev`, `dev-stg`, or `stg-prod`
- **PROJECT_ROOT**: absolute path to the repository root

Each higher level inherits all checks from levels below it. STG → PROD runs all checks from all three levels.

**Level 3 only — UAT results file:**
At Level 3, also look for the UAT results file. Check in this order:
1. `{PROJECT_ROOT}/uat/uat_test_cases.md`
2. If not found, ask: "Where is the completed UAT test cases file? (leave blank if UAT has not been run)"

Store as **UAT_FILE** (absolute path or null).

---

## Step 1 — Read the Codebase

Before running any checks, read:
- Root `package.json` (or equivalent manifest) to identify services and tech stack
- All source files across every service — do not skip any layer
- All test files — presence and structure matter, not just source
- All environment config files (`.env.example`, config objects, etc.) — never read `.env` directly
- `README` or equivalent if present

Do not guess at file content — read every file before drawing conclusions.

**Level 3 only — parse UAT results:**

If UAT_FILE is set, read it and extract the following. The file is Markdown produced by
`/generate-uat-tests` — parse these patterns:

1. **UC-IDs** — from `###` headings whose text ends with ` — UC-{ID}` (e.g. `### Login — UC-01`).
   Collect every UC-ID present in the file as **UAT_UC_IDS**.

2. **Test cases** — from `####` headings matching `TC-{NNN} ·`. Each `####` block belongs to the
   most recently seen `###` UC-ID heading above it.

3. **Status per test case** — from the **Execution Record** table immediately below each `####`
   heading. The table has columns `Actual Result | Status | Tester | Date | Notes`. Read the
   data row (the row after the `|---|` separator). The `Status` cell contains `PASS`, `FAIL`,
   `BLOCKED`, or is blank (not run).

4. **Business outcomes** — if a `## Business Outcomes` section exists, read its table. Each row
   maps an outcome description to a list of UC-IDs. Store as **UAT_OUTCOMES**.

5. **Scope delta** — if a `## Scope Delta` section exists, note how many untraced features and
   unimplemented UC-IDs are listed.

Build **UAT_RESULTS**:
```
{
  "total": N,
  "pass": N,
  "fail": N,
  "blocked": N,
  "not_run": N,        // blank Status cell
  "uc_ids": {
    "UC-01": { "tests": [{"id":"TC-001","status":"PASS"}, ...] },
    "UC-02": { "tests": [{"id":"TC-003","status":"FAIL"}, ...] },
    ...
  },
  "uc_coverage": {     // UC-IDs with at least one PASS
    "passing": [...],
    "failing": [...],  // has tests but none are PASS
    "blocked": [...],  // all tests BLOCKED, none PASS
    "not_run": [...]   // all tests blank
  },
  "scope_delta": { "untraced": N, "unimplemented": N }
}
```

If UAT_FILE is null, set UAT_RESULTS = null.

---

## Step 2 — Run the Checklist

Work through every check at or below the requested level. For each check record:
- **Status**: PASS / FAIL / WARN / N/A
- **Evidence**: the specific file and line that proves the status (for FAIL and WARN, quote the offending code)
- **Action**: what must be done to resolve it (for FAIL items only)

### Level 1 — local → DEV: Code Quality

**Correctness**
- [ ] All test suites pass (report the test command and expected output — do not run it, flag it as "must verify")
- [ ] No hardcoded service URLs in source code — every inter-service URL comes from an environment variable
- [ ] Boolean request fields are validated as strict type before use — no `Boolean()` coercion on user input
- [ ] Unhandled error responses (status 500) return a static message — raw `error.message` is never forwarded to the client
- [ ] Unhandled errors are logged server-side before responding (console.error or equivalent)
- [ ] String fields that accept user input have a maximum length enforced — unbounded strings are a FAIL
- [ ] Numeric fields that accept user input have minimum and maximum bounds enforced
- [ ] Every domain event published in the code has a wired subscriber, OR is documented as a forward extension point with no consumer — a published event whose consumer exists (an event-driven use case in the use case catalog) but has no subscriber is a FAIL, because the downstream effect silently never runs

**Completeness**
- [ ] A health check endpoint exists (`GET /health` or equivalent) with no auth requirement
- [ ] Every API operation defined in the API contract has a corresponding UI control (if a frontend exists)
- [ ] Create forms include inputs for every optional field the API accepts, not just required fields
- [ ] Destructive actions (delete, irreversible status changes) require explicit user confirmation before the API call

**Environment hygiene**
- [ ] `.env` files are listed in `.gitignore` and are not committed to the repository
- [ ] An `.env.example` file exists for every service that reads environment variables
- [ ] No secrets, API keys, or tokens appear in source code or committed config files

**Test coverage**
- [ ] Domain / unit tests exist and cover every invariant and validation rule
- [ ] Integration / infrastructure tests use a real database or equivalent (no mocked persistence layer)
- [ ] Interface / API tests cover every route: happy path, auth failure, and at least one validation error per endpoint
- [ ] E2E tests exist for every primary use case
- [ ] At least one E2E test exercises each primary user journey end-to-end through the API — the full ordered sequence of use cases for an actor, not just isolated single use cases
- [ ] E2E / journey tests do not seed the database at seams between use cases — any value one use case produces and another consumes must be obtained from the producing API response; direct seeding at a seam can hide a response-contract gap and is a FAIL

---

### Level 2 — DEV → STG: Security + Reliability

*(Runs all Level 1 checks plus the following)*

**Security**
- [ ] Rate limiting is applied to all authentication endpoints (login, register, password reset, OTP)
- [ ] Rate limiting is applied to any endpoint that reveals the existence of a resource (anti-enumeration)
- [ ] Authentication error messages are identical for "not found" and "wrong credential" cases
- [ ] JWT or session tokens are verified on every protected endpoint — no endpoint is accidentally unprotected
- [ ] Request body size limits are explicitly configured — default framework limits must be confirmed or tightened
- [ ] Dependency audit is clean — no known high or critical vulnerabilities in production dependencies

**Reliability**
- [ ] Every outbound HTTP call to an external or downstream service has a timeout configured
- [ ] Network failures to downstream services return a structured error response (e.g. 502) — no unhandled promise rejections
- [ ] Database connections are closed or returned to a pool correctly — no connection leak on error paths
- [ ] The application handles SIGTERM gracefully — in-flight requests are allowed to complete before shutdown

**Input validation**
- [ ] All fields from the FIELD DEFINITIONS CATALOG (or equivalent spec) have their constraints enforced at the API boundary — minLength, maxLength, pattern, allowedValues
- [ ] Fields defined as strict types (boolean, integer, UUID) reject incorrect types with a 422 response — no silent coercion
- [ ] Pagination parameters are present on all list endpoints — unbounded list responses are a FAIL at this level

**Observability**
- [ ] All unhandled errors are logged with enough context to diagnose the failure (request path, error code, stack if available)
- [ ] Health check endpoint is present and returns a meaningful status (not just 200 OK — include version or uptime if possible)

---

### Level 3 — STG → PROD: Hardening

*(Runs all Level 1 and Level 2 checks plus the following)*

**Infrastructure**
- [ ] Database is configured for production workloads — connection pooling, appropriate journal mode (WAL for SQLite, pgBouncer for Postgres, etc.), query timeouts
- [ ] Indexes exist on every column used in a `WHERE`, `ORDER BY`, or `JOIN` clause in production queries
- [ ] Database credentials are injected via environment variables — no credentials in migration scripts or config files
- [ ] File-based storage is not used for persistent data — a proper database or object store is required

**Security hardening**
- [ ] HTTPS is enforced — HTTP requests are redirected or rejected
- [ ] Security headers are set (Content-Security-Policy, X-Frame-Options, X-Content-Type-Options, Strict-Transport-Security)
- [ ] CORS origin is restricted to the production frontend domain — wildcard `*` is a FAIL
- [ ] JWT secrets and signing keys meet minimum entropy requirements (256-bit / 32 bytes random)
- [ ] Token expiry is configured and short enough for the security profile of the application

**Observability**
- [ ] Structured logging is in place — logs are machine-parseable (JSON) and routed to an aggregator
- [ ] Error tracking is configured (Sentry, Datadog, CloudWatch, or equivalent)
- [ ] Key business events are logged (user registration, authentication, mutations) for audit purposes

**Deployment readiness**
- [ ] All environment variables are documented in `.env.example` with descriptions
- [ ] The application starts cleanly with no warnings or deprecation notices
- [ ] Build output (if applicable) produces no errors or warnings
- [ ] `README` contains accurate run-locally and deploy instructions

**Functionality** *(Level 3 only — requires completed UAT file)*
- [ ] UAT test cases file exists and has been located
- [ ] All test cases have been executed — no blank Status cells remain
- [ ] UC coverage is 100% — every UC-ID in the file has at least one PASS result
- [ ] Test pass rate is 100% — no FAIL status in any test case
- [ ] Scope delta is documented — untraced features and unimplemented UCs are noted

Scoring rules:
- UAT_FILE null → F (UAT not run — FAIL; cannot promote to PROD without human UAT sign-off)
- any `not_run` > 0 → FAIL (incomplete UAT; all cases must be executed)
- any UC-ID in `uc_coverage.failing` → FAIL (a requirement is demonstrably broken)
- any UC-ID in `uc_coverage.not_run` → FAIL (a requirement was never tested)
- any UC-ID in `uc_coverage.blocked` → WARN (environment constraint; document and accept)
- all UC-IDs in `uc_coverage.passing` → PASS

---

## Step 3 — Produce the Report

Output the report in this exact format:

```
PROMOTION GATE: {FROM} → {TO}
PROJECT: {PROJECT_ROOT}
DATE: {today}

RESULT: PASS | BLOCKED

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FAILURES ({count}) — must resolve before promotion
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[F-01] {check name}
       File: {file}:{line}
       Found: {quoted evidence}
       Fix: {specific action required}

[F-02] ...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
WARNINGS ({count}) — should resolve, will not block
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[W-01] {check name}
       File: {file}:{line}
       Note: {what was found and why it's a concern}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PASSED ({count})
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ {check name}
✓ ...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
N/A ({count}) — not applicable to this stack
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- {check name}: {reason not applicable}
```

**Level 3 only — append the Functionality Report section after PASSED / N/A:**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FUNCTIONALITY REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
UAT file         : {UAT_FILE path, or "NOT FOUND — run /generate-uat-tests first"}
Tests total      : {total}  (Pass: {pass}  Fail: {fail}  Blocked: {blocked}  Not run: {not_run})

UC coverage      : {passing count} / {total uc count} ({pct}%)
Test pass rate   : {pass} / {pass+fail} executed ({pct}%)   [excludes Blocked]
Scope delta      : {untraced} untraced features · {unimplemented} unimplemented UC-IDs

{If any UC-IDs are failing or not run, list them:}
UC-IDs with no passing test:
  ✗ UC-{ID} — {feature name}  [{FAIL / Not run / Blocked}]
  ...

{If UAT_OUTCOMES is present:}
Business Outcome Coverage:
  {For each outcome row:}
  ✓ {outcome}  (UC-{IDs} — all PASS)
  ✗ {outcome}  (UC-{IDs} — {one or more not passing})
  ~ {outcome}  (UC-{IDs} — BLOCKED)

FUNCTIONALITY SCORE: {pass}/{total} tests · {uc_passing}/{uc_total} UC-IDs · {PASS | FAIL | PARTIAL}
```

The FUNCTIONALITY SCORE line contributes to the overall RESULT:
- Any Functionality FAIL → overall RESULT is BLOCKED (add F-entries in the FAILURES section above)
- Any Functionality WARN (blocked UCs) → add W-entries in the WARNINGS section above
- All Functionality PASS → does not change overall RESULT (other checks still apply)

If RESULT is BLOCKED, end with:
> "Resolve all FAILURES above and re-run `/promote-environment {level}` before proceeding."

If RESULT is PASS, end with:
> "All checks passed. This codebase is cleared for promotion to {TARGET}."

---

## Rules

- **Never fix issues** — only report them. The developer decides how to resolve.
- **Quote evidence for every FAIL** — "this file looks fine" is not evidence; a file path and line number is.
- **N/A requires a reason** — if a check doesn't apply, say why (e.g. "no frontend in this project", "not using a relational database").
- **Do not skip checks** — every check in the level must appear in the report as PASS, FAIL, WARN, or N/A. Omitting a check is not allowed.
- **Warnings do not block** — they are concerns the developer should be aware of but can choose to defer.
- **Higher levels inherit lower levels** — a STG → PROD run must include all Level 1 and Level 2 checks.
