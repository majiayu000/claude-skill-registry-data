---
name: nick-deep-uat
description: Deep UAT testing for all Perlantir projects. Crawls every page, clicks every button, tests every form, verifies every interaction, takes screenshots for vision analysis, and checks for missing features against project scope. Runs automatically after every deploy.
---

# Changelog
- 2026-03-19: Major upgrade — added vision analysis (screenshot every page, analyze with image tool), scope gap detection (compare built features vs project spec), raised button test cap to 50, added screenshot evidence requirement for all failures.

# Deep UAT — Full Interaction + Vision + Scope Testing

## When To Use
- After EVERY deploy (automatic — never skip)
- After every phase build completion
- When Nick reports a broken button or interaction
- Before reporting "done" on any build

---

## Phase 0 — Scope Gap Detection (NEW — run FIRST)

**Before running any browser tests**, load the project spec or MEMORY.md to identify what was supposed to be built.

Extract:
- Every feature mentioned in the build spec or Nick's request
- Every page/route that should exist
- Every user-facing interaction that should work

Then after testing, produce a **Scope Gap Report**:
```
=== SCOPE GAP REPORT ===
Features in spec: [list]
Features found in build: [list]
❌ MISSING: [features that were in scope but not found in the build]
⚠️ PARTIAL: [features that exist but are incomplete]
```

This catches "it works but it's missing half the features" — which visual QA and interaction testing alone won't catch.

---

## Phase 1 — Screenshot Every Page (Vision Analysis)

For EVERY page tested, take a full-page screenshot and an above-the-fold screenshot at both desktop (1280px) and mobile (375px).

Save to: `/tmp/uat-screenshots/<project>/<page>-desktop.png`, `/tmp/uat-screenshots/<project>/<page>-mobile.png`

After collecting screenshots, use the `image` tool to analyze EACH screenshot and check:
- Does it look like a real product or a starter template?
- Are there empty/blank sections that should have content?
- Does the mobile layout break or overflow?
- Are there visible console errors, 404 images, or placeholder text?
- Does the UI look consistent with the design brief?

**Every failure must have a screenshot attached as evidence.** No failures without proof.

---

## Phase 2 — Page Health
- All routes return 200
- No "Something went wrong" error boundaries
- No console errors
- No JavaScript errors in console
- Mobile responsive (no horizontal overflow at 375px)

---

## Phase 3 — Element Discovery + Interaction Testing

### Buttons (cap: 50 per page)
Click every visible button and verify something happens:
- Navigation → URL changes
- Modal trigger → dialog opens
- Action button → toast appears OR state changes OR API call fires
- Toggle → state toggles visibly
- Submit → form validates or submits

**Failure**: button clicked, nothing happens, no state change, no network request fired.

### Forms
- Submit empty → must show validation errors per field
- Submit invalid data → must show errors
- Submit valid data → must succeed OR show meaningful feedback
- Labels visible above every input (not floating labels)

### Links
- Internal links → navigate correctly
- External links → have `target="_blank"`
- No dead links (href="#")

### Modals / Sheets / Drawers
- Opens on trigger
- Closes on Escape key
- Closes on backdrop click
- Form inside modal works end-to-end

---

## Phase 4 — Auth Flow Testing
- Signup → verify account created + redirect works
- Login with valid credentials → redirect to dashboard
- Login with invalid credentials → shows error
- Password reset → email sent message appears
- Logout → session cleared, redirects to login/home
- Protected routes → unauthenticated user redirected to login

---

## Phase 5 — Empty + Loading + Error States
For EACH of these, take a screenshot as evidence:
- **Loading state**: trigger an async operation, confirm spinner/skeleton shows
- **Empty state**: view a list/table with no data, confirm it shows a message + CTA (not blank)
- **Error state**: submit a form with an intentional error, confirm per-field error messages appear

If any of these states are missing or show blank white space → FAILURE.

---

## How To Run

```bash
node skills/nick-deep-uat/scripts/deep-uat.js <URL> [--auth email:password] [--viewport mobile|desktop|both]
```

---

## Output Format

```
=== DEEP UAT REPORT ===
URL: https://example.com
Project: [name]

=== SCOPE GAP REPORT ===
❌ MISSING FEATURES: [list any features in spec not found]
⚠️ PARTIAL FEATURES: [list incomplete features]

=== VISION ANALYSIS ===
[Page by page screenshot analysis — what looks wrong, template-like, or broken]

=== INTERACTION RESULTS ===
Pages tested: X | Buttons tested: X | Forms tested: X

✅ PASSED: X
❌ FAILED: X
⚠️ WARNINGS: X

=== FAILURES (with screenshot evidence) ===
❌ /page → Button "Save" → No response
❌ /page → Form "Contact" → No validation on empty submit
❌ /dashboard → Empty state → Blank white space (no message, no CTA)

=== SCREENSHOTS ===
[Attached: key screenshots for every failure]
```

---

## Integration With Build Pipeline

After every Claude Code build + Vercel deploy:
1. Load project spec → identify scope
2. Screenshot all pages → vision analysis
3. Run interaction tests (buttons, forms, links, modals)
4. Run auth flow
5. Check empty/loading/error states
6. Produce Scope Gap Report
7. If any FAILURES or SCOPE GAPS: auto-fix and redeploy
8. Report final results to Nick with screenshots attached

---

## Critical Rules
- NEVER report "done" without running all phases
- EVERY failure must have a screenshot as evidence
- Scope gaps are as important as broken buttons — missing features = failure
- Test BOTH desktop (1280px) AND mobile (375px)
- Blank white areas where content should be = FAILURE
- If a button does nothing when clicked = FAILURE
- If a form submits without validation = FAILURE
- Missing loading/empty/error states = FAILURE
- Dead links (href="#") = FAILURE
