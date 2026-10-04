---
description: Check E2E test (Playwright) status and identify/fix failures when detected
---

# E2E Fix

Check the status of E2E tests (Playwright) on GitHub Actions, identify failure causes, and apply fixes.

## Steps

### 1. Check E2E workflow run status

```bash
gh run list --workflow=e2e.yml --limit=5
```

### 2. If failing, check logs

```bash
# Get detailed logs for the failed run
gh run view <run-id> --log-failed

# Download test report (artifact)
gh run download <run-id> -n playwright-report -D /tmp/playwright-report
```

### 3. Analyze failure cause

#### Common failure patterns

| Pattern | Cause | Remedy |
|---------|-------|--------|
| Timeout | Page load delay, element not visible | Adjust waitFor timeout, verify selector |
| Element not found | Selector changed, DOM structure changed | Check `data-testid`, fix selector |
| Navigation error | URL changed, redirect changed | Verify routing |
| Auth failure | Credentials expired | Check SSM parameters (requires AWS access) |
| Flaky test | Async race condition | Add `waitForSelector`, `waitForResponse` |
| Environment issue | Deployment not complete, service down | Check target environment status |

### 4. Check and fix test code

```bash
# Check E2E test files
ls frontend/tests/

# Local execution (using Mockoon mock, via dev script)
dev/test-frontend

# Debug execution for a specific test
cd frontend && npx playwright test --debug <test-file>

# Visual verification in headed mode
cd frontend && npx playwright test --headed <test-file>
```

### 5. Check Playwright report

```bash
# Open the downloaded report
cd frontend && npx playwright show-report /tmp/playwright-report
```

### 6. Verify after fix

```bash
# Run all tests locally (Mockoon startup + Playwright)
dev/test-frontend
```

### 7. Commit and push fix to re-run

After user confirmation, commit and push the fix.

## E2E Test Environments

| Environment | Frontend URL | Backend URL | Credentials |
|-------------|-------------|-------------|-------------|
| dev | SSM: `/ai-reception-dev/frontend-url` | SSM: `/ai-reception-dev/backend-url` | SSM (encrypted) |
| stg | SSM: `/ai-reception-stg/frontend-url` | SSM: `/ai-reception-stg/backend-url` | SSM (encrypted) |
| prod | SSM: `/ai-reception-prod/frontend-url` | SSM: `/ai-reception-prod/backend-url` | SSM (encrypted) |

## Notes

- Playwright reports (artifacts) are retained for 7 days
- CI runs Chromium and WebKit only (Firefox excluded)
- Local tests use Mockoon mock server; CI E2E connects to real environments
- Fix root causes of flaky tests rather than relying on retries

## Language

- **All user-facing output, reports, and summaries must be written in Japanese(すべてのユーザーへの出力は日本語にしてください)**
