---
name: smoke-suite-gate
description: "Build-an-X workflow for a critical-path smoke suite that runs in <5 minutes - picks the 5-15 highest-business-value journeys (login, hero flow, checkout, payment, primary read), implements as fast E2E or API tests, gates per-deploy, retries on transient failures with quarantine. Use as the canary-precursor or per-deploy verification gate; the team's \"if this fails, the build can't proceed\" floor."
---

# smoke-suite-gate

## Overview

A smoke suite is the **minimum** end-to-end test set every deploy
must pass, gating pre-merge, post-merge to main, post-deploy to
staging, and post-deploy to canary. A smoke failure halts the
release.

## When to use

- The CI/CD pipeline lacks a fast deploy gate; full regression
  takes too long for per-deploy.
- A canary stage needs a precursor smoke test that's faster than
  the full canary observation.
- A new release process needs the "first-line defense" check.

For broader coverage, see the team's full E2E suite (per
`qa-web-e2e` plugin) - smoke is the
narrow, fast subset.

## Step 1 - Identify the critical paths

The smoke suite covers 5-15 journeys. Picking criteria:

1. **High business value** - broken = revenue / brand impact within
   minutes.
2. **High traffic** - most users hit this; broken = many users
   affected.
3. **Cross-system** - exercises multiple components; broken =
   integration regression.

Examples by product:

| Product type        | Smoke journeys                                              |
|---------------------|-------------------------------------------------------------|
| E-commerce           | Sign-in, search, add to cart, checkout, confirmation        |
| SaaS B2B              | Sign-in, dashboard load, primary feature, save, sign-out    |
| Banking app           | Sign-in, account balance, recent transactions, payment      |
| Content site          | Home page, article load, search, sign-up                     |

## Step 2 - Implement fast

Smoke tests must run in **<5 minutes total**. Constraints:

| Aspect              | Smoke                                            |
|---------------------|--------------------------------------------------|
| Per-test budget     | 30-60s                                            |
| Total tests          | 5-15 (one per critical journey)                  |
| Setup               | Synthetic test account + test-mode payment        |
| Assertions          | Existence + status code + key text (not exhaustive) |
| Retries             | 1 retry on transient failure                       |

```typescript
// e2e/smoke/checkout.smoke.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Smoke - checkout', () => {
  test('sign in → add to cart → checkout', async ({ page }) => {
    // 1. Sign in
    await page.goto('/login');
    await page.getByLabel('Email').fill(process.env.SMOKE_USER_EMAIL!);
    await page.getByLabel('Password').fill(process.env.SMOKE_USER_PASSWORD!);
    await page.getByRole('button', { name: /sign in/i }).click();
    await expect(page.getByRole('heading', { name: /welcome/i })).toBeVisible({ timeout: 10000 });

    // 2. Add to cart
    await page.goto('/products/SMOKE-001');
    await page.getByRole('button', { name: /add to cart/i }).click();
    await expect(page.getByTestId('cart-count')).toHaveText('1');

    // 3. Checkout
    await page.goto('/checkout');
    await page.getByLabel(/card/i).fill('4242 4242 4242 4242');
    await page.getByRole('button', { name: /place order/i }).click();
    await expect(page.getByRole('heading', { name: /order confirmed/i })).toBeVisible({ timeout: 15000 });
  });
});
```

Note: smoke tests use a pre-seeded test account, test-mode
payment, and a known SKU (`SMOKE-001`). They don't create or
delete data - pure read flows are best.

## Step 3 - Pre-deploy vs post-deploy

| Stage             | Smoke check                                              |
|-------------------|----------------------------------------------------------|
| Pre-merge (PR)     | Build artifact; deploy to ephemeral env; run smoke; tear down. |
| Post-merge to main | Deploy to staging; run smoke against staging.            |
| Post-deploy to staging | Re-run smoke (verifies the deploy didn't break anything). |
| Post-deploy to canary | Smoke runs first; if green, canary observation begins.  |
| Post-deploy to prod | Smoke runs against prod (read-only) as the final verification. |

Per stage, smoke acts as the "is this deploy worth proceeding
with" gate.

## Step 4 - Failure handling

A failing smoke isn't always a real regression - sometimes flake.
Pattern:

```yaml
- name: Run smoke
  id: smoke
  run: npx playwright test e2e/smoke/ --retries=2 --workers=2

- name: Quarantine repeat failure
  if: steps.smoke.outcome == 'failure'
  run: |
    if [ "${{ steps.smoke.conclusion }}" == "failure" ]; then
      # Real failure (failed twice with retries) - block deploy
      exit 1
    fi
```

The 2-retry rule kills most transients. A 3-retry-failure smoke
test is either:

1. A real regression - block the deploy.
2. A genuinely flaky test - quarantine + investigate via
   `flaky-test-quarantine` (in the qa-flake-triage plugin).

Don't suppress failures by raising the retry count.

## Step 5 - Smoke suite curation

The smoke suite must stay fast. Add tests deliberately:

| Add a test when                                        | Don't add when                                      |
|--------------------------------------------------------|-----------------------------------------------------|
| A critical journey doesn't have smoke coverage          | Coverage exists; just want more tests              |
| A SEV-1+ incident's would-have-caught test fits        | The test is broader than smoke (move to regression) |
| A new feature's primary flow lacks smoke                | The test is slow (>60s; move to regression)         |

Quarterly review: drop smoke tests that haven't caught a real
regression in N quarters and aren't covering a new business value.

## Step 6 - CI integration

```yaml
# .github/workflows/smoke-gate.yml
name: smoke-gate
on:
  push:
    branches: [main]
  pull_request:

jobs:
  smoke:
    runs-on: ubuntu-latest
    timeout-minutes: 10   # hard cap - smoke must finish in 10 min
    steps:
      - uses: actions/checkout@v5
      - uses: actions/setup-node@v4
        with: { node-version: '20' }
      - run: npm ci
      - run: npx playwright install --with-deps chromium
      - name: Deploy ephemeral env (PR only)
        if: github.event_name == 'pull_request'
        run: ./scripts/deploy-ephemeral.sh ${{ github.head_ref }}
      - name: Run smoke
        env:
          SMOKE_USER_EMAIL: ${{ secrets.SMOKE_USER_EMAIL }}
          SMOKE_USER_PASSWORD: ${{ secrets.SMOKE_USER_PASSWORD }}
          BASE_URL: ${{ steps.deploy.outputs.url || 'https://staging.example.com' }}
        run: npx playwright test e2e/smoke/ --retries=2
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: smoke-results
          path: playwright-report/
```

`timeout-minutes: 10` is the hard fail-fast - if smoke takes
longer, something's wrong (the suite has bloated; deploy is slow).

## Anti-patterns

| Anti-pattern                                                          | Why it fails                                                              | Fix |
|-----------------------------------------------------------------------|---------------------------------------------------------------------------|-----|
| 50-test smoke suite                                                    | Not smoke; full regression. Per-deploy gate becomes 30-min runtime.      | Cap at 15 tests (Step 1). |
| Smoke tests that create / delete data                                  | Pollute prod / test env; flake on parallel runs.                         | Read-only flows; pre-seeded data (Step 2). |
| Smoke tests that hit production with real money                        | Real charges; PII; compliance risk.                                       | Test-mode payment; synthetic accounts (Step 2 example). |
| Suppressing failures via 5+ retries                                    | Real regressions hide; "smoke green" loses meaning.                      | 2 retries max; quarantine repeat failures (Step 4). |
| Adding tests to smoke "for safety" without removing slow ones          | Suite bloats; per-deploy time grows.                                     | Curation rule (Step 5). |
| Smoke that asserts every detail                                        | Fragile to copy / layout changes; flaky.                                 | Existence + status + key text only (Step 2). |

## Limitations

- **Smoke ≠ regression.** A green smoke doesn't prove the system
  works; it proves the critical paths work. Pair with full
  regression at lower frequency.
- **Pre-seeded data dependencies.** If `SMOKE-001` SKU is deleted
  or the synthetic account is locked, smoke fails for the wrong
  reason. Monitor the test-data state.
- **Test-mode payment vs real.** Stripe / PayPal test mode behaves
  ~95% like prod; some prod-only edge cases need separate
  verification.
- **Mobile smoke is different.** Mobile uses
  `mobile-device-matrix-toolkit` (in the qa-mobile plugin)
  smoke tier; same principle, different platform.

## References

- `flaky-test-quarantine` - handles repeat-failing smoke tests.
- `prod-canary-validator` - downstream gate after smoke passes.
- `synthetic-monitor-author` - same critical journeys, but continuous-in-prod (not per-deploy).
