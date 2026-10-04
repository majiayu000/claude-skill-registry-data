---
name: orbit-user-flow
description: User-flow / journey mapping for a WordPress plugin — measures click-depth to core features, detects setup wizards / onboarding, scores confusion (tabs × inputs × toggles), verifies analytics events fire on user actions, validates consent-mode (GDPR) compliance. Use when the user says "user flow", "click depth", "onboarding test", "first-time UX", "verify analytics events", "GDPR consent", or "test the new-user journey".
---

# 🪐 orbit-user-flow — Real-user journey mapping

Measures how a real first-time user experiences your plugin. PM-driven, not dev-driven.

---

## Quick start

```bash
PLUGIN_SLUG=my-plugin \
PLUGIN_ADMIN_SLUG=my-plugin-settings \
PLUGIN_ONBOARDING_URL=/wp-admin/admin.php?page=my-plugin-onboarding \
PLUGIN_CORE_FEATURE_URL=/wp-admin/admin.php?page=my-plugin-main \
  npx playwright test --project=pm
```

Output:
```
[PM] Onboarding present: ✅
[PM] Core feature reachable in: 3 clicks
[PM] Confusion score: 6.2/10 (tabs:3, inputs:14, toggles:5)
[PM] First-time setup completable end-to-end: ✅
```

---

## What it measures

### 1. Click depth to core feature

Starting from a fresh WP install with the plugin just activated:

```js
// flows/click-depth.spec.js
test('Reach core feature from dashboard', async ({ page }) => {
  let clicks = 0;
  await page.goto('/wp-admin/');

  while (!page.url().includes('my-plugin-main') && clicks < 10) {
    // Click any plugin-relevant link
    const link = page.getByRole('link', { name: /my-plugin/i }).first();
    if (await link.isVisible()) { await link.click(); clicks++; }
  }

  expect(clicks).toBeLessThanOrEqual(3);
  console.log(`Core feature reachable in ${clicks} clicks`);
});
```

**Decision rule:**
- ≤ 3 clicks → good
- 4-5 → onboarding can improve
- > 5 → redesign navigation

### 2. Setup wizard / onboarding detection

Looks for: dedicated onboarding URL, `<step>` markup, "Step N of M" text, progress bar, "Skip Setup" button.

```js
test('First-activate triggers wizard', async ({ page }) => {
  // Activate plugin via wp-cli
  // Visit /wp-admin/
  await page.goto('/wp-admin/');
  await expect(page).toHaveURL(/onboarding|welcome|setup/);
});
```

### 3. Confusion score

```
score = (tabCount × 1.0) + (inputCount × 0.3) + (toggleCount × 0.5) + (modalCount × 1.5)
```

Lower = simpler.
Below 4 = "feels easy"
4-7 = "okay"
> 7 = "feature creep, simplify"

### 4. Analytics events fire correctly

```bash
PLUGIN_ANALYTICS_EVENTS='[
  {"action":"click","selector":"#save-btn","expect_event":"plugin_save_clicked","endpoint_match":"google-analytics.com"},
  {"action":"click","selector":".upgrade-link","expect_event":"upgrade_cta_clicked","endpoint_match":"mixpanel"}
]' \
  npx playwright test --project=analytics
```

Test passes only if the declared event hit the declared endpoint when the user took the action. Failures = tracking script not firing, selector changed, or consent mode blocking.

### 5. Consent-mode compliance (GDPR)

```js
// flows/consent.spec.js
test('Tracking blocked without consent', async ({ page }) => {
  await page.goto('/');
  // Verify no analytics call before consent
  page.on('request', req => {
    if (req.url().includes('google-analytics')) {
      throw new Error('GA called before consent!');
    }
  });
  await page.waitForTimeout(2000);
});

test('Tracking fires after consent', async ({ page }) => {
  await page.goto('/');
  await page.getByRole('button', { name: /accept/i }).click();

  let gaCalled = false;
  page.on('request', req => { if (req.url().includes('google-analytics')) gaCalled = true; });
  await page.waitForTimeout(2000);
  expect(gaCalled).toBe(true);
});
```

Both must pass. Either failure = GDPR risk.

---

## Standalone flows you can author

`tests/playwright/flows/` is where custom user-flow specs live. Each follows the pattern:

```js
test.describe.configure({ mode: 'serial' });   // Flow tests are state-mutating
test.describe('User journey: Create first widget', () => {
  test('Step 1: dashboard → settings', ...);
  test('Step 2: settings → save API key', ...);
  test('Step 3: navigate back, verify saved', ...);
});
```

Templates available in `tests/playwright/templates/<plugin-type>/`.

---

## What "good" looks like

For an Elementor addon plugin:

```
PM Audit Score: 7.8 / 10

✅ Click depth: 2 clicks (target ≤ 3)
✅ Setup wizard: present, completable
✅ Confusion score: 4.1 (target < 5)
✅ Analytics: 7/7 events fire on consent
✅ Consent mode: tracking blocked pre-consent
⚠ Empty state: dashboard is blank with no CTA when no widgets exist (-1 pt)
⚠ Error state: 404 page lacks "back to settings" link (-0.5 pt)
```

---

## What "bad" looks like

```
PM Audit Score: 3.2 / 10

❌ Click depth: 6 clicks to reach core feature
❌ Setup wizard: missing — first-time users land on a blank settings page
❌ Confusion score: 9.1 (4 tabs × 22 inputs × 8 toggles)
⚠ Analytics: 5/7 events firing (2 selectors changed)
❌ Consent: GA loads before consent banner shown — GDPR violation
```

Any score < 5 → block release until UX is fixed.

---

## Pair with `/orbit-pm-ux-audit`

`/orbit-pm-ux-audit` checks textual quality (spelling, labels, terminology). This skill checks structural quality (depth, flow, completion). They overlap 0%.

---

## Output

`reports/user-flow-<timestamp>.md` + `reports/screenshots/flows/` (one per step).

For PM-friendly view, the `/orbit-uat-compare` HTML report includes flow videos + step-by-step screenshots.
