---
name: test
description: "Run dotnet integration tests AND Playwright E2E tests for Skoleoverblikket. USE THIS SKILL when the user explicitly asks to run tests, Playwright/E2E tests, or API integration tests. For compile checks and dotnet format only, use /verify instead. The Aspire stack is assumed to already be running for Playwright."
---

# Test Skill

Runs API integration tests and the full Playwright E2E suite.

## Step 1 — API integration tests

```bash
dotnet test --project api/tests/Skoleoverblikket.Api.IntegrationTests/Skoleoverblikket.Api.IntegrationTests.csproj --configuration Release
```

Runs all tUnit integration tests via Testcontainers. Needs Docker running. If Docker is not running, say so explicitly rather than claiming failure is a code bug.

## Step 2 — Playwright E2E

```bash
cd web && npx playwright test --reporter=line
```

Playwright config starts the full Aspire stack automatically via `aspire run --non-interactive` if not already up. Pass `SKIP_ASPIRE=1` only if the stack is already running.

Do NOT pre-start Aspire manually. Do NOT poll for port readiness. Just run the command — Playwright handles it.

## What to report

After both steps, report clearly:

- **API tests**: pass/fail count and any failure details (test name, assertion error, file:line)
- **E2E tests**: pass/fail count, which tests failed (name and file, verbatim), failure details
- **Whether failure is code or environment** — if a test fails because Aspire isn't running or Docker is down, say so explicitly

## Fixing failures

If tests fail:

1. Read the failure output carefully before touching any code
2. Check whether the failure is environmental (stack not running, wrong port, Docker down, leftover state) vs a real regression
3. If it's a real regression, investigate the root cause in the relevant test file and the frontend/API code it exercises
4. Fix the underlying issue, then re-run to confirm green

Do not comment out failing tests or lower assertion thresholds to make tests pass.

## Test locations

- API integration tests: `api/tests/`
- E2E spec files: `web/tests/e2e/`
- Playwright config: `web/playwright.config.ts`
