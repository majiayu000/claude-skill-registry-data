---
name: orbit-qa-flaky-detector
description: Detect flaky Playwright tests — runs each spec N times, flags any that pass-then-fail-then-pass, ranks by flakiness rate, suggests root causes (timing, network, parallelism, state leak). Use when the user says "flaky tests", "intermittent failure", "CI flaky", "test passes locally fails in CI".
---

# 🪐 orbit-qa-flaky-detector — Flaky Playwright test detector

A flaky test is worse than no test — it trains the team to ignore failures. This skill catches them by running tests many times and ranking pass-rate.

---

## Quick start

```bash
bash ~/Claude/orbit/scripts/detect-flaky.sh --runs 10
```

Output: `reports/flaky-<timestamp>.md`.

---

## How it works

1. Run the full Playwright suite N times (default 10)
2. Record pass/fail per spec per run
3. Compute pass rate
4. Rank: 100% pass = stable, < 100% = flaky
5. For each flaky, propose root-cause hypothesis based on failure pattern

---

## Pass-rate interpretation

| Rate | Verdict |
|---|---|
| 100% | Stable. Trust it. |
| 90-99% | Mildly flaky — investigate but not urgent |
| 60-89% | Flaky — deprioritise CI block, fix soon |
| < 60% | Broken — disable + fix |

---

## Common flaky causes + diagnostics

### Timing (race condition)
**Whitepaper intent:** A test that passes at 60ms and fails at 200ms is racing the page. Use Playwright's auto-wait, never `waitForTimeout`.

```js
// ❌ Hard-coded wait
await page.waitForTimeout(500);

// ✅ Wait for actual condition
await page.locator('.my-component').waitFor({ state: 'visible' });
```

### Parallelism / shared state
Tests using the same DB record concurrently corrupt each other. Mark state-mutating tests `serial`:
```js
test.describe.configure({ mode: 'serial' });
```

### Network jitter
Real network calls in tests are flaky. Mock:
```js
await page.route('**/api/**', route => route.fulfill({ status: 200, body: '{}' }));
```

### Browser inconsistencies
Same test passes on Chromium, fails on WebKit. Often a subtle CSS / event-bubbling difference. Pin to one browser if you don't actually need cross-browser.

### Auth state expiry
Cookies expire mid-suite. Re-auth before each test or use Playwright's `storageState`.

### Animation
Element measured mid-fade-in, value flips. Disable animations:
```js
await expect(page).toHaveScreenshot('x.png', { animations: 'disabled' });
```

---

## Output

```markdown
# Flaky Test Detector — my-plugin (10 runs)

## Stable: 38/42 specs (90%)

## Flaky (4 specs)
- ❌ flows/checkout.spec.js > "Complete purchase" — 5/10 pass (50%)
   → Failure pattern: retry succeeds → likely race condition
   → Suggested fix: add explicit wait for stripe.elements ready

- ⚠ blocks/dynamic-list.spec.js > "Load 100 items" — 8/10 (80%)
   → Failure pattern: timeout
   → Suggested fix: increase timeout for this test, or batch items

- ⚠ admin/settings.spec.js > "Save settings" — 9/10 (90%)
   → Failure pattern: passed except run 7 — auth cookie expired mid-suite
   → Suggested fix: add beforeEach re-login or refresh storageState

- ⚠ visual/cards.spec.js > "Card spacing" — 7/10 (70%)
   → Failure pattern: pixel diff > 2%
   → Suggested fix: animations disabled missing
```

---

## Pair with

- `/orbit-playwright` — debug flaky tests with trace viewer
- `/orbit-qa-snapshot-cleanup` — stale snapshots cause visual flakiness

---

## Sources & Evergreen References

### Canonical docs
- [Playwright — Flaky tests](https://playwright.dev/docs/test-retries) — auto-retry strategies
- [Playwright Best Practices](https://playwright.dev/docs/best-practices) — root-cause patterns
- [Stripe Engineering — Reducing Flaky Tests](https://stripe.com/blog/the-secret-to-reducing-flaky-tests) — case study

### Last reviewed
- 2026-04-29
