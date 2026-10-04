---
name: wp-guided-tour
description: "Use when adding a guided onboarding or feature-discovery tour to a WordPress admin plugin using Driver.js v1 — setting up the IIFE bundle (window.driver.js.driver), PHP backend tour config arrays (autoStart, pages, steps, element, popover), JS scope detection from URL pathname + hash (getCurrentScope, hashchange listener), localStorage-based completion tracking, CSS selector rules for WP admin elements including Tailwind bracket-notation escaping, testing selectors in browser console, and generating/updating the POT file for tour strings. Triggers: \"add a guided tour to my plugin\", \"onboarding walkthrough in WP admin\", \"Driver.js setup\", \"highlight this admin element\", \"step-by-step tutorial in WP admin\", \"tour not starting\", \"tour completion not saving\", \"scope detection for admin pages\", \"add tooltips to my settings page\", \"first-run wizard\", \"window.driver.js.driver\", \"getCurrentScope()\", \"hashchange listener for tour\", \"localStorage tour tracking\", \"Tailwind selector escaping in PHP\", \"Driver.js popover\", \"autoStart tour config\", \"tour step element not found\", \"verify selector in browser console\", \"tour i18n POT file\". Not for: front-end SPAs or non-WordPress apps; guided tours in themes."
---

# WordPress Admin Guided Tours (Driver.js)

> **Model note:** IIFE bundle setup and PHP config scaffolding are mechanical (`haiku`). JS scope detection from URL + hash, and debugging selector mismatches against live DOM, need `sonnet`.

## When to use

- "Add a guided tour to my plugin", "set up Driver.js in WordPress admin".
- "Wire up tour scopes by URL/hash", "detect which page the user is on for tour routing".
- "Track tour completion correctly", "fix tour firing on dismiss instead of Done".
- "Test tour selectors against live DOM".

**Not for:** Front-end-only SPAs or non-WordPress JS apps — requires WP admin backend context. Guided tours in themes — this skill targets plugin-owned admin pages only.

## Setup

### 1 — Vendor Driver.js

Download the Driver.js v1 IIFE build (NOT the ESM build):
- `driver.js.iife.js` → `assets/admin/js/driverjs/driver.js.iife.js`
- `driver.css` → `assets/admin/js/driverjs/driver.css`

The IIFE build exposes `window.driver.js.driver` (double namespace). Always call it as:
```js
window.driver.js.driver({ ... })
```

### 2 — Enqueue in Asset.php

```php
// Enqueue on all admin pages (is_admin() block)
$this->enqueue_script(
    'shopflow_guided_tour_driverjs',
    SHOPFLOW_ASSETS_URL . 'admin/js/driverjs/driver.js.iife.js',
    array()
);
$this->enqueue_style(
    'shopflow_guided_tour_driverjs',
    SHOPFLOW_ASSETS_URL . 'admin/js/driverjs/driver.css',
    array()
);
$this->enqueue_script(
    'shopflow_guided_tour',
    SHOPFLOW_ASSETS_URL . 'admin/js/guided-tour.js',
    array( 'shopflow_guided_tour_driverjs' )
);

// Add tour configs to the main localized object
$localized['tours'] = shopflow_get_tour_configs();
```

The `$localized` array must be passed to `localize_script()` on the **main SPA script** (not the tour script) so `window.SHOPFLOW.tours` is available before `guided-tour.js` runs.

---

## PHP Tour Config (`functions.php`)

```php
function shopflow_get_tour_configs() {
    return apply_filters( 'shopflow_tour_configs', array(

        'dashboard' => array(
            'autoStart' => true,          // only one scope should be true
            'pages'     => array( 'shopflow' ),
            'steps'     => array(
                array(
                    // Centered popover — no element key
                    'popover' => array(
                        'title'       => __( 'Welcome!', 'my-plugin' ),
                        'description' => __( 'Quick intro text.', 'my-plugin' ),
                        'side'        => 'bottom',
                    ),
                ),
                array(
                    // Element-targeted step
                    'element' => '#my-stable-id',
                    'popover' => array(
                        'title'       => __( 'Step Title', 'my-plugin' ),
                        'description' => __( 'Step description.', 'my-plugin' ),
                        'side'        => 'right',
                    ),
                ),
            ),
        ),

    ) );
}
```

**Rules:**
- Only one scope should have `autoStart: true` (the primary onboarding page)
- Always use `__()` on title and description — run `makepot` after adding new steps
- `side` values: `top`, `bottom`, `left`, `right`
- Do NOT set `align: 'start'` — it's the default; explicit is noise
- `pages` array is metadata only; actual detection is done by JS `getCurrentScope()`

---

## JS Scope Detection (`guided-tour.js`)

```js
function getCurrentScope() {
    const urlParams = new URLSearchParams(window.location.search);
    const page = urlParams.get('page');

    if (!page || !page.startsWith('myprefix')) return null;

    // Non-SPA pages (full page reloads)
    if (page === 'myprefix-settings') return 'settings';
    if (page === 'myprefix-wizard')   return 'wizard';

    // Main SPA — differentiate by hash route
    // Strip pagination suffix like /page/2
    const hash = window.location.hash.replace('#', '').replace(/\/page\/\d+$/, '');

    if (!hash || hash === '/' || hash === '/dashboard') return 'dashboard';
    if (hash.startsWith('/products/add'))  return 'add-product';
    if (hash === '/orders/new')            return 'create-order';
    if (hash === '/orders')                return 'orders';
    if (hash === '/customers')             return 'customers';
    if (hash.startsWith('/reports'))       return 'reports';

    return null;
}
```

**Key points:**
- Check `page.startsWith('myprefix')` — NOT `page.startsWith('myprefix-')` (would miss the bare slug `page=myprefix`)
- Hash routes need explicit prefix matching (`.startsWith`) for pages with sub-routes
- `hashchange` listener re-runs scope detection for SPA navigation:
  ```js
  window.addEventListener('hashchange', () => setTimeout(autoStartTours, 500));
  ```

---

## JS Tour Lifecycle

```js
let currentTour = null;

function startTour(scope = null) {
    if (!window.driver?.js?.driver) {
        console.warn('Driver.js not loaded');
        return false;
    }

    const targetScope = scope || getCurrentScope();
    if (!targetScope || !window.SHOPFLOW?.tours[targetScope]) return false;

    if (currentTour) currentTour.destroy();

    const steps     = window.SHOPFLOW.tours[targetScope].steps;
    const lastIndex = steps.length - 1;

    // Inject completion tracking ONLY on the final step's Next/Done click.
    // onDestroyed fires for BOTH completion AND early dismiss — do NOT use it
    // for completion tracking.
    const stepsWithCompletion = steps.map((step, i) => {
        if (i !== lastIndex) return step;
        return {
            ...step,
            popover: {
                ...step.popover,
                onNextClick: () => {
                    markTourCompleted(targetScope);
                    currentTour.destroy();
                },
            },
        };
    });

    currentTour = window.driver.js.driver({
        showProgress: true,
        smoothScroll: true,
        showButtons:  ['next', 'previous', 'close'],
        steps:        stepsWithCompletion,
        onDestroyed:  () => { currentTour = null; },
    });

    setTimeout(() => currentTour.drive(), 100);
    return true;
}
```

**Critical:** `onDestroyed` fires on close AND completion. Never call `markTourCompleted` there. Inject it into the last step's `onNextClick` only.

---

## Selector Rules

| Pattern | Good/Bad | Reason |
|---------|----------|--------|
| `#my-stable-id` | ✅ | Most stable |
| `.unique-class-combo` | ✅ | Stable if combo is unique |
| `.my-class:first-of-type` | ❌ | `:first-of-type` matches by tag, not class |
| `:nth-child(2)` | ❌ | Breaks on DOM reorder |
| Tailwind responsive variants | ⚠️ | Need backslash escaping in PHP strings |

**Tailwind escaping in PHP:**
```php
// CSS selector: .border-[#F0EDFB]
// In PHP string:
'element' => '.border-\\[\\#F0EDFB\\]',
```

**Test every selector in browser console before committing:**
```js
!!document.querySelector('.my-selector')  // must return true on target page
```

**Important:** Test each selector on its OWN page. A selector for the orders tour will return `false` on the dashboard — that's expected.

---

## Browser Verification Checklist

After implementing tours, verify in browser:

```js
// 1. All tours loaded
Object.keys(window.SHOPFLOW.tours)  // should list all scopes

// 2. Scope detection works on current page
getCurrentScope()  // should return expected scope string

// 3. All selectors resolve (run on EACH tour's own page)
window.SHOPFLOW.tours['my-scope'].steps
  .filter(s => s.element)
  .map(s => ({ el: s.element, found: !!document.querySelector(s.element) }))

// 4. Tour renders
localStorage.clear()
startTour('my-scope')

// 5. Completion tracking — click Done on last step
localStorage.getItem('myprefix_my-scope_tour_completed')  // → "true"

// 6. Dismiss tracking — restart, click X on step 1
// localStorage key must NOT be set
```

---

## Post-Implementation Checklist

- [ ] Run `composer run makepot` — all `__()` strings in tour configs must be in `.pot`
- [ ] Every scope in `shopflow_get_tour_configs()` has a matching case in `getCurrentScope()`
- [ ] Only one scope has `autoStart: true`
- [ ] All element selectors verified on their own pages via browser console
- [ ] Completion fires on Done, not on X/close
- [ ] `smoothScroll: true` in driver config (prevents jarring jumps on long pages)
- [ ] No `align: 'start'` in steps (redundant default)
- [ ] Update docs file if one exists

## References

- `references/scope-detection.md` — `getCurrentScope()` patterns for URL-only and hash-routed SPA pages, common pitfalls.
- `references/php-tour-config.md` — Full PHP config shape with all fields, Tailwind selector escaping, and filter pattern.
- `references/driver-js-lifecycle.md` — `startTour()` implementation with correct completion tracking, `autoStartTours()` pattern, IIFE namespace.
