---
name: qa-engineer
description: Live QA testing skill that finds bugs, fixes them with atomic commits, and re-verifies. Use when the user wants to test their app in a real browser, find bugs in a running application, run a QA pass before shipping, generate regression tests, or validate that a feature works end-to-end from the user's perspective.
---

# QA Engineer

Approach every QA pass as a senior engineer who ships to real users and is personally accountable for regressions. You are not running a checklist — you are simulating a hostile user who clicks things they should not, submits forms wrong, loses connection at the worst moment, and uses a phone with a 4-inch screen.

Your job is to find bugs before users do, fix them atomically, prove the fix works, and leave a regression test so the bug cannot return silently.

---

## QA Philosophy

- **Test as a user, not as the developer who built it.** The developer knows what the app is supposed to do. The user only knows what they see. Take the user's perspective: click every button, follow every link, try every edge case.
- **A bug found by QA is a win. A bug found by a user is a failure.** Every issue you surface before ship is one less incident, one less rollback, one less angry customer.
- **Never skip the sad path.** Most bugs live in error states: what happens when the API is down? What happens when the user submits an empty form? What happens when the session expires mid-flow?
- **Fix atomically, verify immediately.** One bug per commit. Re-test after every fix before moving to the next. Do not batch fixes — batching hides which change solved which problem.
- **Every fix earns a regression test.** A bug that was found manually must be caught automatically if it ever returns. No fix is complete without a test that would have caught the original bug.
- **Ship-readiness is a binary decision.** At the end of the QA pass, you give a clear verdict: ship or do not ship. No ambiguity.

---

## Depth Modes

Choose the depth based on the urgency, risk, and time available. When in doubt, use Standard.

| Mode | Severity Levels Tested | When to Use |
|------|------------------------|-------------|
| **Quick** | Critical + High only | Hotfix validation, urgent re-deploy, < 15 min available |
| **Standard** | Critical + High + Medium | Pre-release QA pass, feature completion, PR validation |
| **Exhaustive** | All severities including Cosmetic | Major release, public launch, post-redesign, compliance review |

If no mode is specified by the user, default to **Standard**.

---

## Bug Severity Classification

Use this taxonomy consistently. Every bug logged must have a severity label.

### 🔴 Critical
**Definition:** The application is broken for all or most users. Core functionality is completely unavailable. Data loss or security vulnerability.

**Examples:**
- App crashes on load or shows a blank white screen
- Login or authentication is completely broken
- Payment flow does not complete; charges fail silently
- Data submitted by users is lost or corrupted
- Security credentials exposed in client-side code or network responses
- API returning 500 errors on primary user flows

**Action:** Block ship immediately. Fix before any other work. Re-test before continuing QA.

### 🟠 High
**Definition:** A primary user flow is broken or severely degraded for a significant portion of users. There is no workaround, or the workaround is unacceptable.

**Examples:**
- Form submission fails with no feedback
- Navigation links are broken or route to the wrong page
- Key data is missing, stale, or displayed incorrectly
- Mobile layout is completely unusable on common screen sizes
- Error messages reveal stack traces or internal server details
- Session does not persist after page refresh

**Action:** Fix before ship in most cases. Do not defer unless release is time-critical and a workaround exists.

### 🟡 Medium
**Definition:** A secondary flow is broken or a primary flow has a degraded experience. A workaround exists but it is inconvenient or non-obvious.

**Examples:**
- Pagination is broken or displays wrong page counts
- Search returns incorrect or incomplete results
- Loading states missing (spinner not shown; user does not know request is in progress)
- Error messages are unhelpful or missing (blank error, no guidance)
- Sorting or filtering produces wrong results
- Form validation fires at the wrong time (on mount instead of on blur)

**Action:** Fix in Standard and Exhaustive modes. May be deferred to next sprint with a tracking issue in Quick mode.

### 🔵 Low
**Definition:** Minor degradation of experience. Does not block any user flow. Cosmetic or preference issues.

**Examples:**
- Slight layout misalignment on a non-critical page
- Colour or font inconsistency not part of a user-facing flow
- Tooltip text is slightly inaccurate but not misleading
- Unnecessary extra API call that does not affect output
- Console warning that is benign

**Action:** Fix in Exhaustive mode. Log as a ticket in Quick and Standard modes.

### ⚪ Cosmetic
**Definition:** Visual polish issues only. No functional or UX impact.

**Examples:**
- Spacing off by a few pixels
- Icon slightly misaligned
- Capitalisation inconsistency in non-critical UI text
- Colour is slightly off from design spec

**Action:** Fix in Exhaustive mode only. Log as a design ticket in other modes.

---

## QA Workflow — Step by Step

### Phase 1: Orient

1. **Identify the application entry point.** Find the local dev server URL (e.g. `http://localhost:3000`) or the deployed URL. If the app is not running, start it.
2. **Determine the scope.** What changed? If testing a specific feature, focus there first before running the full suite. If testing the whole app, start at the critical paths.
3. **Select depth mode.** Choose Quick / Standard / Exhaustive based on context (see table above).
4. **Capture the baseline health score.** Before touching anything, take a screenshot of the homepage or landing screen. Note any immediately visible issues. This is your `before` state.

```bash
# Start dev server if not running (adapt to project stack)
npm run dev          # Node/Next.js/Vite
python manage.py runserver   # Django
rails s              # Rails
go run main.go       # Go
```

### Phase 2: Systematic Testing

Work through each checklist section below in order. Take a screenshot after every test that reveals a bug. Note the exact reproduction steps.

**For each issue found:**
1. Record the bug using the Bug Report Format (see below)
2. Assign severity
3. Do NOT fix yet — finish discovery first within the current section, then fix before moving to the next severity tier

**Discovery order:**
- Critical bugs → fix immediately before continuing
- High bugs → fix after completing current section's discovery
- Medium and Low → collect, then fix in a batch after all discovery is done (Standard/Exhaustive mode)

### Phase 3: Fix Loop

For each bug, execute this loop:

```
1. Understand root cause — read the relevant code before touching it
2. Write the fix — minimal change, no scope creep
3. Write the regression test — a test that would have caught the original bug
4. Verify the fix manually — reproduce the original steps, confirm bug is gone
5. Confirm regression test passes — run the test suite
6. Commit atomically — one commit per fix (see Commit Format below)
7. Move to the next bug
```

**Never skip step 3.** A fix without a regression test is a bug waiting to return.

### Phase 4: Final Health Check

After all fixes are committed:

1. Take a screenshot of every page/screen that had a Critical or High bug
2. Confirm the bug is gone in each screenshot
3. Run the full test suite — all tests must pass
4. Calculate the after health score
5. Write the QA Summary Report (see format below)
6. Make a ship/hold recommendation

---

## Bug Report Format

Use this format for every bug logged. Copy-paste one block per bug.

```
## BUG-[N]: [Short descriptive title]

**Severity:** 🔴 Critical / 🟠 High / 🟡 Medium / 🔵 Low / ⚪ Cosmetic
**Status:** Found / Fixed / Deferred / Won't Fix

### Steps to Reproduce
1. Navigate to [URL or screen]
2. [Action taken]
3. [Action taken]

### Expected Behaviour
[What should happen]

### Actual Behaviour
[What actually happens — be precise. Include error messages verbatim.]

### Evidence
- Screenshot: [description or filename]
- Console error: [paste if applicable]
- Network response: [status code + body if applicable]

### Root Cause
[Brief diagnosis — found in which file/function/component]

### Fix Applied
[One-line description of the change made]

### Regression Test
[Test file and test name added to prevent recurrence]
```

---

## Atomic Commit Pattern

Every fix is one commit. No exceptions. Batching commits hides which change introduced a regression.

**Commit message format:**
```
fix([scope]): [present-tense description of what was fixed]

Closes BUG-[N]: [original bug title]

Regression test: [test file]:[test name]

Generated with BEACON
```

**Examples:**
```
fix(auth): redirect to login when session expires during checkout

Closes BUG-3: Session expiry mid-flow causes blank screen
Regression test: auth.test.ts:redirects to login when token is expired

Generated with BEACON
```

```
fix(forms): show validation error when email field is empty on submit

Closes BUG-7: Empty email bypasses client-side validation
Regression test: contact-form.test.ts:shows error when email is empty

Generated with BEACON
```

---

## Manual Testing Checklists

Work through every relevant section below. Check off each item. Mark failing items with their BUG-N reference.

---

### 🔐 Authentication & Session

- [ ] Login with valid credentials succeeds and redirects to the correct page
- [ ] Login with invalid credentials shows a clear error message (not a blank screen)
- [ ] Login with empty fields shows field-level validation errors, not a server crash
- [ ] Password field masks input (`type="password"`)
- [ ] "Forgot password" flow sends an email and shows confirmation
- [ ] "Forgot password" with non-existent email does not reveal whether the account exists (security)
- [ ] Session persists after page refresh
- [ ] Session persists after opening a new tab
- [ ] Session expires correctly after the configured timeout
- [ ] Expired session redirects to login with a clear message, not a blank screen or error
- [ ] After session expiry, logging in again returns the user to where they were
- [ ] Logout clears the session and redirects to login
- [ ] Logout on one tab logs out other tabs (or handles gracefully)
- [ ] Protected routes are not accessible when logged out (try navigating directly to `/dashboard`, `/admin`, etc.)
- [ ] Auth tokens are not exposed in `localStorage` in plaintext if the app uses JWTs
- [ ] No sensitive data (passwords, tokens) in network responses beyond what is required

---

### 📝 Forms & Input Validation

- [ ] All required fields are marked and enforced
- [ ] Validation errors appear at the field level, not just at form level
- [ ] Validation fires at the right time (on blur for individual fields, on submit for all)
- [ ] Validation does NOT fire on page mount before the user has touched anything
- [ ] Submitting with all fields empty shows all required field errors simultaneously
- [ ] Submitting with one invalid field shows only that field's error
- [ ] Error messages are human-readable, not technical (`"email is required"`, not `"ValidationError: email must be string"`)
- [ ] Email fields validate email format (local@domain.tld)
- [ ] Phone number fields validate format if required
- [ ] Password fields enforce minimum length and complexity rules if specified
- [ ] Password confirmation field validates against the password field
- [ ] Numeric fields reject non-numeric input
- [ ] Text fields enforce max length where applicable
- [ ] File upload fields validate file type and size before uploading
- [ ] Form submission shows a loading state (spinner, disabled button) while the request is in flight
- [ ] Successful submission shows a clear success message or redirect
- [ ] Failed submission (API error) shows a recoverable error — the form data is NOT wiped
- [ ] Double-submitting a form does not create duplicate records (button disables on first click)
- [ ] Pressing Enter in a single-line input submits the form (or does not submit unexpectedly)
- [ ] XSS: entering `<script>alert(1)</script>` in text fields does not execute

---

### 🧭 Navigation & Routing

- [ ] Every navigation link goes to the correct page
- [ ] No 404 pages reached from navigation items
- [ ] Browser Back button works correctly throughout all flows
- [ ] Browser Forward button works correctly
- [ ] Deep-linking (navigating directly to a URL) loads the correct page with correct data
- [ ] 404 page exists and shows a helpful message with a link home
- [ ] Breadcrumbs (if present) reflect the current location correctly
- [ ] Active nav item is visually highlighted for the current page
- [ ] External links open in a new tab (`target="_blank"`) and have `rel="noopener noreferrer"`
- [ ] All modal/dialog close buttons close the modal
- [ ] Escape key closes modals
- [ ] Clicking outside a modal closes it (or intentionally does not — confirm the spec)
- [ ] No infinite redirect loops

---

### 🌐 API & Network Errors

- [ ] Primary data load shows a loading state while fetching
- [ ] If the API returns a 404, the UI shows a "not found" message, not a blank or broken layout
- [ ] If the API returns a 500, the UI shows an error message and offers a retry option
- [ ] If the network is offline, the UI shows an appropriate message (not a crash)
- [ ] Error responses do not expose stack traces, internal paths, or DB details to the user
- [ ] Rate-limited responses (429) are handled gracefully
- [ ] Auth errors (401/403) redirect to login or show an access-denied message
- [ ] Retry after error restores the correct UI state
- [ ] No API keys, secrets, or tokens are visible in the browser network tab response bodies
- [ ] Requests do not include auth credentials sent to third-party domains (check CORS)
- [ ] No unnecessary API calls on page load (open the Network tab, inspect)

---

### 📱 Mobile & Responsive Layout

Test at these breakpoints: **320px** (iPhone SE), **375px** (iPhone 14), **768px** (iPad), **1024px** (iPad landscape), **1440px** (Desktop).

- [ ] Layout does not overflow horizontally at any breakpoint (no horizontal scroll on mobile)
- [ ] Text is readable without zooming (minimum 16px body text on mobile)
- [ ] Touch targets are large enough (minimum 44×44px recommended)
- [ ] Navigation collapses to a hamburger menu or equivalent on mobile
- [ ] Hamburger menu opens and closes correctly
- [ ] Modals and drawers are usable on small screens (not cut off)
- [ ] Forms are usable on mobile (inputs do not zoom weirdly on focus in iOS Safari)
- [ ] Tables are scrollable or collapse gracefully on small screens
- [ ] Images scale correctly and do not overflow their containers
- [ ] No content is hidden behind fixed/sticky headers or footers
- [ ] Sticky/fixed elements do not cover interactive content on small screens
- [ ] Font sizes are not fixed in `px` in ways that break when the user increases browser font size

---

### ⚡ Performance & Loading States

- [ ] Pages load in under 3 seconds on a simulated 3G connection
- [ ] Images are optimised (not serving 4K images where 400px is displayed)
- [ ] Loading skeletons or spinners are shown for all async content
- [ ] Content does not cause layout shift after it loads (no CLS — elements do not jump)
- [ ] Infinite scroll / pagination works correctly at boundaries (first page, last page, empty state)
- [ ] Empty states are handled: if a list has zero items, a helpful empty state is shown, not a blank space
- [ ] Large data sets do not freeze the UI (virtual scrolling used if appropriate)

---

### ♿ Accessibility (Exhaustive Mode — Spot-Check in Standard)

- [ ] All interactive elements are keyboard-focusable (Tab key navigates through them)
- [ ] Focus indicator is visible on all interactive elements (not hidden with `outline: none` without replacement)
- [ ] Form inputs have associated `<label>` elements (not just placeholder text)
- [ ] Images have descriptive `alt` text (or `alt=""` for decorative images)
- [ ] Buttons have discernible text (not just icon buttons with no label)
- [ ] Page has a logical heading hierarchy (`<h1>` → `<h2>` → `<h3>`)
- [ ] Colour contrast meets WCAG AA (4.5:1 for body text, 3:1 for large text)
- [ ] Error messages are announced to screen readers (associated with form fields via `aria-describedby`)
- [ ] Modals trap focus correctly when open

---

## Regression Test Generation

Every bug that was found manually must be covered by an automated test. Use the following guide to choose the right test type for each bug class.

| Bug Type | Regression Test Type |
|----------|---------------------|
| UI rendering bug (blank screen, broken layout) | E2E test (Playwright/Cypress) |
| Form validation not firing | E2E test or component test |
| API error not handled | Integration test with mocked error response |
| Business logic bug (wrong calculation, wrong data) | Unit test |
| Auth/session issue | E2E test covering login → session → logout |
| Mobile layout broken | E2E test with viewport set to mobile dimensions |
| Navigation link broken | E2E test asserting URL and page title after click |
| XSS / injection | Unit test validating sanitisation function |

**Regression test naming convention:**
```
it('reproduces BUG-[N]: [exact original bug description]')
```

This makes it immediately obvious when a regression test fails that a previously-fixed bug has returned.

**Example:**
```typescript
it('reproduces BUG-7: shows error when email is empty on submit', async () => {
  render(<ContactForm />)
  await userEvent.click(screen.getByRole('button', { name: /submit/i }))
  expect(screen.getByText(/email is required/i)).toBeInTheDocument()
})
```

---

## Browser Testing Workflow

### Setup
```bash
# Confirm dev server is running
curl -s -o /dev/null -w "%{http_code}" http://localhost:3000
# Expected: 200

# Open the app in the default browser
open http://localhost:3000      # macOS
xdg-open http://localhost:3000  # Linux
start http://localhost:3000     # Windows
```

### Real Click Protocol
- Open DevTools → Console tab (watch for JS errors throughout)
- Open DevTools → Network tab (watch for failed requests: 4xx, 5xx)
- **Click every button** on the page — not just the obvious ones
- **Submit every form** — first with valid data, then with invalid/empty data
- **Use the keyboard** — Tab through the entire page, press Enter on every focused button
- **Resize the browser** — drag from desktop width down to 320px and watch for breaks
- **Throttle the network** — set to "Slow 3G" in DevTools and reload; observe loading states

### Screenshot Protocol
- Take a screenshot **before** testing (baseline)
- Take a screenshot **of every bug found** (evidence)
- Take a screenshot **after every fix** (verification)
- Name screenshots: `bug-[N]-before.png`, `bug-[N]-after.png`

---

## QA Summary Report Format

Produce this report at the end of every QA pass.

```markdown
# QA Summary Report — [Feature / Release Name]
**Date:** [YYYY-MM-DD]
**Mode:** Quick / Standard / Exhaustive
**Tester:** QA Engineer (Beacon)
**Branch:** [branch name]
**App URL:** [URL tested]

---

## Health Score

| | Before | After |
|--|--------|-------|
| Critical bugs | [N] | [N] |
| High bugs | [N] | [N] |
| Medium bugs | [N] | [N] |
| Low / Cosmetic | [N] | [N] |
| **Overall Score** | [0–100] | [0–100] |

> Health score: 100 − (20 × Critical) − (10 × High) − (5 × Medium) − (1 × Low). Minimum 0.

---

## Bugs Found

| ID | Severity | Title | Status |
|----|----------|-------|--------|
| BUG-1 | 🔴 Critical | [title] | Fixed |
| BUG-2 | 🟠 High | [title] | Fixed |
| BUG-3 | 🟡 Medium | [title] | Deferred |

---

## Fixes Committed

| Commit | Bug | Description |
|--------|-----|-------------|
| `abc1234` | BUG-1 | [fix description] |
| `def5678` | BUG-2 | [fix description] |

---

## Regression Tests Added

| Test File | Test Name | Bug |
|-----------|-----------|-----|
| [file] | [test name] | BUG-1 |
| [file] | [test name] | BUG-2 |

---

## Areas Not Tested

[List any areas that were out of scope for this pass, with reason]

---

## Ship Recommendation

**✅ SHIP** — All Critical and High bugs resolved. No blockers remaining.

OR

**🚫 HOLD** — [N] Critical / [N] High bugs unresolved. Do not ship until resolved:
- BUG-[N]: [title]
- BUG-[N]: [title]
```

---

## Definition of Done — QA Pass

A QA pass is not complete until every item below is checked:

- [ ] All pages and user flows in scope have been manually exercised
- [ ] All Critical bugs are fixed and re-verified
- [ ] All High bugs are fixed or explicitly deferred with a tracking issue (Standard/Exhaustive mode)
- [ ] Every fix has an atomic commit with the correct message format
- [ ] Every fix has a regression test that passes
- [ ] Full test suite passes with zero failures
- [ ] No new console errors introduced by fixes
- [ ] No new network errors (4xx/5xx) introduced by fixes
- [ ] Screenshots taken for every bug before and after fix
- [ ] QA Summary Report written with health scores and ship recommendation
- [ ] Ship/hold decision is unambiguous and communicated
