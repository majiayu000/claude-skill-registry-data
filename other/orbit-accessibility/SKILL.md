---
name: orbit-accessibility
description: WCAG 2.2 AA accessibility audit for a WordPress plugin's admin UI, block editor output, and frontend markup. Combines axe-core (automated 30% coverage) with code-review for the 70% axe can't catch — focus traps, keyboard nav, ARIA misuse, screen-reader announcements, colour contrast on dynamic content. Use when the user says "a11y", "accessibility", "WCAG", "axe-core", "screen reader", or after any UI change to the plugin's admin pages or block output.
---

# 🪐 orbit-accessibility — WCAG 2.2 AA audit

Two layers: **automated** (axe-core via Playwright) + **code review** (the 70% axe can't catch).

---

## Quick start

```bash
# Automated scan on every visual URL
WP_TEST_URL=http://localhost:8881 \
  npx playwright test --project=a11y

# Plus code-review pass via Claude
claude "/orbit-accessibility Audit ~/plugins/my-plugin admin UI + frontend output for WCAG 2.2 AA. Output markdown."
```

Runs automatically as part of `/orbit-gauntlet --mode full` (Step 11 — accessibility-compliance audit).

---

## What axe-core catches (the 30%)

- Missing `alt` on `<img>`
- Form inputs without `<label>`
- Insufficient colour contrast (text vs background)
- Missing `lang` on `<html>`
- Empty buttons / links
- Duplicate IDs
- Heading order skipped (h1 → h3)

---

## What this skill catches (the 70%)

### Keyboard navigation
- ❌ Tab order doesn't follow visual order
- ❌ Focus disappears (`outline: none` without alternative)
- ❌ Modal opens but focus stays on the trigger button
- ❌ Modal closes but focus doesn't return to the trigger
- ❌ Custom dropdown not reachable by keyboard (uses `mousedown` only)
- ❌ Date picker / colour picker / range slider with no keyboard support

### Screen reader (ARIA)
- ❌ `<div role="button">` without `tabindex="0"` and key handlers
- ❌ Toast / notice appears but no `aria-live` region
- ❌ Form error appears but no `aria-describedby` link
- ❌ Loading spinner with no `aria-busy="true"`
- ❌ Toggle button switches state but no `aria-pressed`
- ❌ Tabs without `role="tablist"` / `role="tab"` / `aria-selected`
- ❌ Modal without `role="dialog"` + `aria-labelledby`
- ❌ Icon-only button without `aria-label`
- ❌ `aria-hidden="true"` on focusable element

### Dynamic content
- ❌ AJAX result inserted into DOM with no announcement
- ❌ Page change via `history.pushState` without focus management
- ❌ Auto-refresh of content without `aria-live="polite"`
- ❌ Form submission shows toast but doesn't move focus

### Colour & visual
- ❌ Information conveyed by colour alone (red = error, no icon)
- ❌ Hover-only affordance (no keyboard equivalent)
- ❌ Required field marked with `*` only (no text "Required")
- ❌ Touch target < 44×44px (WCAG 2.5.5)

### Forms (WCAG 3.3)
- ❌ Validation errors without `aria-invalid="true"`
- ❌ Error message only on submit (no inline validation hint)
- ❌ Generic error "Invalid input" instead of "Email must contain @"
- ❌ Labels disappearing on focus (placeholder-as-label anti-pattern)

### Block editor (Gutenberg)
- ❌ Custom block missing `supports.html` declaration
- ❌ InspectorControls without proper `__()` text
- ❌ Block toolbar buttons without `aria-label`
- ❌ Inline transforms with no preview / undo

---

## Report format

```markdown
# Accessibility Audit — [Plugin]

## Summary
- Pages scanned: 12
- WCAG 2.2 AA violations: 23
  - Critical: 4 (block release)
  - Serious: 8 (block release)
  - Moderate: 7
  - Minor: 4

## Critical findings

### 1. Modal focus trap missing
**File:** assets/js/admin/modal.js:42
**WCAG:** 2.4.3 Focus Order, 2.1.2 No Keyboard Trap
**Issue:** Modal opens via `dialog.show()` but focus stays on trigger button. Users on keyboard or screen reader can't navigate into the modal.
**Fix:**
```js
function openModal(modal) {
  const focusable = modal.querySelectorAll('a, button, input, [tabindex]');
  focusable[0]?.focus();
  document.addEventListener('keydown', trapFocus);
}
```

### 2. Toast notice not announced
**File:** includes/admin/notice.php:18
**WCAG:** 4.1.3 Status Messages
**Issue:** `<div class="notice">` rendered but no `role="status"` or `aria-live`. Screen readers ignore the success/error message.
**Fix:**
```php
echo '<div class="notice notice-success" role="status" aria-live="polite">';
```

[Continue for all findings]
```

---

## Run on a URL list (CI-friendly)

```bash
A11Y_URLS=$(jq -r '.visualUrls | join(",")' qa.config.json) \
  npx playwright test --project=a11y
```

Reads `visualUrls` from `qa.config.json`. Each URL gets its own axe-core scan.

---

## Pair with `/orbit-visual-regression`

Visual regression catches "did the UI change visually". This skill catches "is the UI usable for keyboard / screen reader / low-vision users". They overlap on **0%** — run both.

---

## Common false positives (don't fix these)

| Axe says | Why it's OK |
|---|---|
| `color-contrast` on disabled buttons | WCAG exempts disabled controls (1.4.3) |
| `region` rule on a single-purpose admin page | Admin pages are exempt — `<main>` is enough |
| `landmark-unique` in WP admin | WP core admin already has landmarks |

Document any "expected fail" in `tests/playwright/a11y-known-issues.md` so the next reviewer doesn't refile the same finding.

---

## Tools used

- `@axe-core/playwright` — automated WCAG scan
- `axe-core` 4.x rules → mapped to WCAG 2.2 AA
- Claude Code review for the 70% axe can't see

---

## Severity → release gate

| WCAG impact | Block release? |
|---|---|
| Critical (focus trap, keyboard not reachable) | ✅ Yes |
| Serious (no aria-label on icon button, no error association) | ✅ Yes |
| Moderate (colour alone, touch target < 44px) | ⚠ Document, fix in next release |
| Minor (lang attr, duplicate ID) | Log + defer |

---

## Standards reference

- [WCAG 2.2 AA Quick Reference](https://www.w3.org/WAI/WCAG22/quickref/)
- [WordPress Accessibility Coding Standards](https://make.wordpress.org/core/handbook/best-practices/coding-standards/accessibility-coding-standards/)
- [10up Accessibility Guide](https://10up.github.io/Engineering-Best-Practices/markup/#accessibility)
