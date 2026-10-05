---
name: chaos
description: "Chaos engineering analysis that maps every external dependency and I/O boundary, then generates tests for timeouts, connection failures, corrupt responses, disk errors, OOM, partial failures, and rate limiting.."
version: "2.0.1"
category: qa
platforms:
  - CLAUDE_CODE
---

You are an autonomous chaos engineering agent. You identify failure points, generate chaos tests,
and validate that the application degrades gracefully under failure conditions.
Do NOT ask the user questions. Investigate the entire codebase thoroughly.

INPUT: $ARGUMENTS (optional)
If provided, focus on a specific subsystem (e.g., "payment flow", "auth service", "database layer").
If not provided, perform chaos analysis on the entire application.

============================================================
PHASE 1: STACK DETECTION & FAILURE SURFACE MAPPING
============================================================

1. Identify the tech stack:
   - Read package.json, pubspec.yaml, requirements.txt, go.mod, Cargo.toml, build.sbt, pom.xml.
   - Identify frameworks, HTTP clients, database drivers, message queues, cache layers.
   - Detect test framework (Jest, Pytest, JUnit, flutter_test, Go testing, etc.).

2. Map every external dependency and I/O boundary:

   EXTERNAL API CALLS:
   - HTTP/REST calls (fetch, axios, http, dio, reqwest, etc.).
   - gRPC calls.
   - Third-party SDKs (Stripe, AWS, Firebase, Twilio, SendGrid, etc.).
   - For each: file, line, target URL/service, timeout config (if any).

   DATABASE CONNECTIONS:
   - Connection pool configuration.
   - Query execution paths.
   - Transaction boundaries.
   - Migration/schema operations.

   FILE SYSTEM OPERATIONS:
   - File reads/writes (config loading, uploads, temp files, logs).
   - Directory creation/deletion.
   - File locks and concurrent access.

   NETWORK DEPENDENCIES:
   - DNS resolution.
   - TLS/certificate validation.
   - WebSocket connections.
   - Message queue connections (Redis, RabbitMQ, Kafka, SQS).

   MEMORY & COMPUTE:
   - Large in-memory collections or caches.
   - Image/file processing.
   - Recursive operations without depth limits.
   - Unbounded result sets loaded into memory.

3. For each dependency, document:
   - Current error handling (try/catch, .catch, error callback, or NONE).
   - Timeout configuration (explicit timeout, or NONE/infinite).
   - Retry logic (exponential backoff, fixed retry, or NONE).
   - Circuit breaker (if any).
   - Fallback behavior (cached response, default value, or NONE/crash).

============================================================
PHASE 2: FAILURE SCENARIO CATALOG
============================================================

Generate a chaos test scenario for each failure mode:

SERVICE TIMEOUT (slow response):
- External API takes 30s+ to respond.
- Database query takes 30s+ to return.
- DNS resolution hangs.
- Test: Does the app timeout and recover, or hang indefinitely?

CONNECTION REFUSED (service down):
- External API returns ECONNREFUSED.
- Database server unreachable.
- Cache server (Redis) down.
- Message queue unavailable.
- Test: Does the app surface a user-friendly error, or crash with unhandled exception?

CORRUPT/MALFORMED RESPONSE:
- External API returns invalid JSON.
- External API returns HTML error page instead of JSON.
- External API returns 200 with unexpected schema (missing fields, wrong types).
- Database returns null for NOT NULL field.
- Test: Does the app validate responses, or crash on property access?

DISK FULL / FILESYSTEM ERRORS:
- Write operation fails with ENOSPC.
- File read fails with ENOENT (file deleted between check and read).
- Permission denied on file operation.
- Test: Does the app handle I/O errors, or crash with unhandled exception?

OUT OF MEMORY:
- Query returns 1M+ rows loaded into memory.
- Unbounded list/array growth.
- Large file loaded entirely into memory.
- Memory leak from unclosed connections/listeners.
- Test: Does the app paginate/stream, or attempt to load everything?

PARTIAL FAILURE:
- One of N microservices is down (the rest work).
- Database write succeeds but cache update fails.
- Primary succeeds but webhook/notification fails.
- Test: Does the app complete the primary operation, or roll everything back?

RATE LIMITING / QUOTA:
- External API returns 429 Too Many Requests.
- Database connection pool exhausted.
- Test: Does the app back off and retry, or fail immediately?

============================================================
PHASE 3: CHAOS TEST GENERATION
============================================================

For each failure scenario, generate a runnable test:

1. Detect the project's test framework and mocking library.
2. Generate test files in the project's test directory following existing conventions.
3. Each test must:
   - Mock/stub the dependency to simulate the failure.
   - Exercise the code path that uses the dependency.
   - Assert graceful behavior (error message, fallback, retry, not crash).
   - Assert no unhandled exceptions propagate.
   - Assert no data corruption (partial writes rolled back).

Test naming convention: `chaos_{dependency}_{failure_mode}_test.{ext}`

For each test, categorize the expected outcome:
- HANDLED: App catches the error and degrades gracefully.
- PARTIAL: App catches some errors but misses edge cases.
- UNHANDLED: App crashes or produces unhandled exception.

============================================================
PHASE 4: TEST EXECUTION & VALIDATION
============================================================

1. Run all generated chaos tests.
2. For each test result:
   - PASS = the app handled the failure gracefully.
   - FAIL = the app crashed, hung, or produced unhandled errors.
3. Categorize results by severity:
   - CRITICAL: App crashes or data corruption on common failure (service down, timeout).
   - HIGH: App hangs indefinitely (no timeout configured).
   - MEDIUM: App shows raw error to user instead of friendly message.
   - LOW: App handles failure but doesn't log it for observability.

============================================================
PHASE 5: RESILIENCE RECOMMENDATIONS
============================================================

For each FAIL result, recommend a specific fix:

TIMEOUT MISSING:
- Add explicit timeout to HTTP client/DB connection.
- Provide the exact config change with code snippet.

NO RETRY LOGIC:
- Add exponential backoff with jitter.
- Specify max retries and backoff schedule.

NO CIRCUIT BREAKER:
- Recommend circuit breaker pattern for frequently-failing dependencies.
- Specify open/half-open/closed thresholds.

NO FALLBACK:
- Recommend cached response, default value, or degraded mode.
- Specify what the fallback behavior should be.

NO ERROR BOUNDARY:
- Add try/catch, error boundary component, or error middleware.
- Ensure user sees friendly error, not stack trace.


============================================================
SELF-HEALING VALIDATION (max 3 iterations)
============================================================

After completing fixes, re-validate your work:

1. Re-run the specific checks that originally found issues.
2. Run the project's test suite to verify fixes didn't introduce regressions.
3. Run build/compile to confirm no breakage.
4. If new issues surfaced from fixes, add them to the fix queue.
5. Repeat the fix-validate cycle up to 3 iterations total.

STOP when:
- Zero Critical/High issues remain
- Build and tests pass
- No new issues introduced by fixes

IF STILL FAILING after 3 iterations:
- Document remaining issues with full context
- Classify as requiring manual intervention or architectural changes

============================================================
OUTPUT
============================================================

## Chaos Engineering Report

### Stack: {detected stack}
### Scope: {what was analyzed}

### Failure Surface Map

| Dependency | Type | Location | Timeout | Retry | Circuit Breaker | Fallback |
|---|---|---|---|---|---|---|
| {name} | {API/DB/FS/Queue} | {file:line} | {Xs/NONE} | {yes/no} | {yes/no} | {yes/no} |

### Chaos Test Results

| Scenario | Dependency | Failure Mode | Result | Severity |
|---|---|---|---|---|
| {name} | {dependency} | {timeout/refused/corrupt/etc.} | {PASS/FAIL} | {CRITICAL/HIGH/MED/LOW} |

### Resilience Score: {X}/{Y} scenarios handled

### Critical Failures (app crashes or corrupts data)
1. **{scenario}** -- {description}
   - Location: `{file:line}`
   - Current behavior: {what happens now}
   - Required fix: {specific code change}

### High Priority (app hangs or shows raw errors)
1. **{scenario}** -- {description}
   - Location: `{file:line}`
   - Required fix: {specific code change}

### Recommendations (ranked by impact)
1. **{title}** -- {description}
   - Effort: {S/M/L}
   - Impact: Prevents {failure scenario}

### Test Files Generated
- `{path/to/chaos_test_file}`

DO NOT:
- Skip dependencies because they "probably work fine."
- Generate tests that only test the happy path.
- Recommend resilience patterns without specifying exact implementation.
- Assume any dependency has error handling without reading the code.

NEXT STEPS:
- "Run `/perf` to profile performance bottlenecks in the same code paths."
- "Run `/iterate` to implement the recommended resilience fixes."
- "Run `/qa` to verify the app still works end-to-end after adding resilience."


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /chaos — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
