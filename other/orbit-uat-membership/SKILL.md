---
name: orbit-uat-membership
description: UAT template + Playwright spec scaffolds for membership / LMS plugins (LearnDash, MemberPress, Restrict Content Pro, Paid Memberships Pro, LifterLMS, BuddyBoss) — registration, login, paywalled content access, drip schedules, course progress, certificate generation, subscription lifecycle. Use when the user says "LMS UAT", "membership plugin UAT", "test paywall", "course completion test".
---

# 🪐 orbit-uat-membership — Membership / LMS UAT

Membership flows are stateful, time-based, and easy to break with feature additions. This UAT exercises the full lifecycle.

---

## Quick start

```bash
PLUGIN_SLUG=my-lms npx playwright test --project=uat-membership
```

---

## What the UAT covers

### 1. Registration → email verification → login
```js
test('Self-registration → confirm → login', async ({ page }) => {
  await page.goto('/register/');
  await page.fill('[name=email]', 'newuser@example.com');
  await page.fill('[name=password]', 'StrongPass123!');
  await page.click('Sign up');

  // Verify confirmation email sent
  // Click confirmation link (use MailHog fake server)
  // Now log in
  await page.fill('[name=username]', 'newuser');
  await page.fill('[name=password]', 'StrongPass123!');
  await page.click('Log in');
  await expect(page).toHaveURL(/\/account\//);
});
```

### 2. Paywall — restricted content
**Whitepaper intent:** A paywall that's only enforced client-side is no paywall. Always test that the SERVER refuses to serve restricted content to non-members:

```js
// Fetch the URL as anonymous
const anonResponse = await page.request.get('/premium-content/');
const anonBody = await anonResponse.text();
expect(anonBody).not.toContain('PREMIUM CONTENT'); // not in HTML
expect(anonBody).toContain('Members only');         // gate message in HTML

// Now log in
await page.goto('/wp-login.php');
// ... login as member ...

const memberResponse = await page.request.get('/premium-content/');
const memberBody = await memberResponse.text();
expect(memberBody).toContain('PREMIUM CONTENT');
```

### 3. Course progress tracking
```js
test('Lesson completion advances progress', async ({ page }) => {
  await loginAsStudent(page);
  await page.goto('/courses/sample/lessons/1/');
  await page.click('Mark Complete');
  await expect(page.locator('.progress-bar')).toHaveAttribute('aria-valuenow', '20'); // 1/5 lessons = 20%
});
```

### 4. Drip schedule
```js
// Set lesson to drip 7 days after enrollment
// Time-travel: WP_CLI to set enrollment date 8 days ago
await page.goto('/courses/sample/lessons/3/');
await expect(page.locator('.lesson-content')).toBeVisible();  // unlocked
```

### 5. Certificate generation
After course completion, certificate PDF / image generated, downloadable, contains user's name + course title.

### 6. Subscription lifecycle (renewal, cancel, pause)
- Subscription created → first charge succeeds
- Renewal date → second charge attempted (Stripe test mode)
- User cancels → access revoked at period end (not immediately)

### 7. Multi-tier roles
- Bronze → access tier 1 content only
- Gold → access tier 1 + 2
- Platinum → access all

Test cross-tier access leaks.

### 8. Refund flow
Refund triggers immediate access revocation.

### 9. Course/lesson admin CRUD
Admin creates a course → lesson → student sees it on next page load (no caching staleness).

---

## Output

```markdown
# Membership UAT — my-lms

## 35 tests, 32 passed, 3 failed

❌ "Anonymous can fetch /premium-content/ HTML" — content present in body
   → Restriction is JS-only. Add `the_content` filter to gate server-side.

❌ "Cancel subscription — access remains until period end" — access revoked immediately
   → Refund hook runs deletion instead of scheduling for end-of-period

❌ "Bronze tier accessing Gold content" — passes through
   → Tier check uses LIKE 'tier_%' instead of exact match
```

---

## Pair with

- `/orbit-pay-stripe` / `/orbit-pay-paypal` — billing flow
- `/orbit-wp-security` — paywall bypass
- `/orbit-gdpr` — user data export + erasure
- `/orbit-cache-compat` — content gating + page cache

---

## Sources & Evergreen References

### Canonical docs
- [LearnDash Developer Resources](https://developers.learndash.com/) — LMS reference
- [MemberPress Documentation](https://memberpress.com/documentation/) — membership patterns
- [WC Subscriptions](https://woocommerce.com/document/subscriptions/) — subscription lifecycle
- [Stripe Subscriptions](https://docs.stripe.com/billing/subscriptions/overview) — billing primitives

### Rule lineage
- Drip schedules — long-standing across all major LMS plugins
- Block-editor / FSE LMS support — rolling out across the ecosystem 2024-2026

### Last reviewed
- 2026-04-29 — re-review on major LMS plugin releases
