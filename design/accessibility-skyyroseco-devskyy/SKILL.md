---
name: accessibility
description: Design, implement, and audit inclusive digital products using WCAG 2.2 Level AA
  standards. Use when auditing a page, template, or component for accessibility barriers or WCAG
  compliance, generating semantic ARIA for Web or accessibility traits for Native (iOS/Android),
  or fixing a11y gate findings (missing alt text, lang attr, skip-link, focus traps, contrast).
  Do NOT use for performance/CWV audits, SEO, or visual design taste — those have their own
  skills; this one covers accessibility barriers only.
origin: ECC
---

# Accessibility (WCAG 2.2)

This skill ensures that digital interfaces are Perceivable, Operable, Understandable, and Robust (POUR) for all users, including those using screen readers, switch controls, or keyboard navigation. It focuses on the technical implementation of WCAG 2.2 success criteria.

## When to Use

- Defining UI component specifications for Web, iOS, or Android.
- Auditing existing code for accessibility barriers or compliance gaps.
- Implementing new WCAG 2.2 standards like Target Size (Minimum) and Focus Appearance.
- Mapping high-level design requirements to technical attributes (ARIA roles, traits, hints).

**When NOT to use:** performance/Core Web Vitals work (`optimize` skill), SEO/structured data,
or visual design judgment — accessibility barriers only.

## Inputs

Required before starting — if any is absent, **stop and ask; never proceed on a guess**:

- **The surface under audit** — concrete file paths (e.g. `wordpress-theme/skyyrose-flagship/header.php`,
  a component under `frontend/`) or a reachable URL. No named target = nothing to audit; never
  audit from memory of the code.
- **Target platform(s)** — Web (HTML/ARIA), iOS (SwiftUI traits), or Android (Compose semantics).
  The remediation vocabulary differs per platform (see Cross-Platform Mapping below).
- **Conformance target** — default is WCAG 2.2 Level AA. Note any stricter house rules: in this
  repo, contrast is also a brand constraint — crimson `#DC143C` on `#0A0A0A` is 3.63:1, below AA
  for body text, so it is fills/borders/glows only (`CLAUDE.md` §6).
- **For theme work** — a checkout containing `wordpress-theme/skyyrose-flagship/` so the
  `a11y-static` gate in Verification below can run.

## Core Concepts

- **POUR Principles**: The foundation of WCAG (Perceivable, Operable, Understandable, Robust).
- **Semantic Mapping**: Using native elements over generic containers to provide built-in accessibility.
- **Accessibility Tree**: The representation of the UI that assistive technologies actually "read."
- **Focus Management**: Controlling the order and visibility of the keyboard/screen reader cursor.
- **Labeling & Hints**: Providing context through `aria-label`, `accessibilityLabel`, and `contentDescription`.

## Procedure

### Step 1: Identify the Component Role

Determine the functional purpose (e.g., Is this a button, a link, or a tab?). Use the most semantic native element available before resorting to custom roles.

### Step 2: Define Perceivable Attributes

- Ensure text contrast meets **4.5:1** (normal) or **3:1** (large/UI).
- Add text alternatives for non-text content (images, icons).
- Implement responsive reflow (up to 400% zoom without loss of function).

### Step 3: Implement Operable Controls

- Ensure a minimum **24x24 CSS pixel** target size (WCAG 2.2 SC 2.5.8).
- Verify all interactive elements are reachable via keyboard and have a visible focus indicator (SC 2.4.11).
- Provide single-pointer alternatives for dragging movements.

### Step 4: Ensure Understandable Logic

- Use consistent navigation patterns.
- Provide descriptive error messages and suggestions for correction (SC 3.3.3).
- Implement "Redundant Entry" (SC 3.3.7) to prevent asking for the same data twice.

### Step 5: Robust Compatibility

- Use correct `Name, Role, Value` patterns.
- Implement `aria-live` or live regions for dynamic status updates.

### Step 6: Run the gate

Every audit or fix ends by re-running the gate below and reporting the row status with an
evidence tag — an edit whose gate output was never observed is an unverified claim.

## Verification

Run the repo's static accessibility gate. It parses every delivered theme `.php` template for
`<img>` tags without `alt`, a missing `lang` attribute in `header.php`, and a missing skip-link:

```bash
bash wordpress-theme/skyyrose-flagship/scripts/verify-theme.sh --only a11y-static
```

**PASS:** the row reads `[PASS] a11y-static  img alt / lang attr / skip-link present`. `[test]`
**Not a pass:** a `[WARN]` row — it carries concrete findings (e.g. `2 <img> without alt`,
observed on this tree 2026-07-29) that must be fixed and the gate re-run. The script exits 0 on
WARN by design, so the pass condition is the row status, never the exit code alone. `[repro]`

The interactive half (keyboard reachability, focus order, contrast measurement, axe-core run) is
deliberately a SKIP in the same gate:

```bash
bash wordpress-theme/skyyrose-flagship/scripts/verify-theme.sh --only a11y-interactive
```

**Expected:** `[SKIP] a11y-interactive  needs-browser — caller: axe-core + keyboard/focus/contrast pass`.
A SKIP is not a PASS — the browser pass must be executed against the rendered page with a real
browser (Playwright MCP / Chrome DevTools), on mobile AND desktop, and reported with its own
evidence tag: `[repro]` against a local render, `[live]` against skyyrose.co. For component-level
work outside the theme, the jest-axe / `@axe-core/playwright` patterns under Automated
Accessibility Testing below apply — but neither package is installed in this repo today
(`frontend/package.json` carries vitest + Playwright only), so install them first; a check that
cannot run must be reported as not-run, never as passed.

## Accessibility Architecture Diagram

```mermaid
flowchart TD
  UI["UI Component"] --> Platform{Platform?}
  Platform -->|Web| ARIA["WAI-ARIA + HTML5"]
  Platform -->|iOS| SwiftUI["Accessibility Traits + Labels"]
  Platform -->|Android| Compose["Semantics + ContentDesc"]

  ARIA --> AT["Assistive Technology (Screen Readers, Switches)"]
  SwiftUI --> AT
  Compose --> AT
```

## Cross-Platform Mapping

| Feature            | Web (HTML/ARIA)          | iOS (SwiftUI)                        | Android (Compose)                                           |
| :----------------- | :----------------------- | :----------------------------------- | :---------------------------------------------------------- |
| **Primary Label**  | `aria-label` / `<label>` | `.accessibilityLabel()`              | `contentDescription`                                        |
| **Secondary Hint** | `aria-describedby`       | `.accessibilityHint()`               | `Modifier.semantics { stateDescription = ... }`             |
| **Action Role**    | `role="button"`          | `.accessibilityAddTraits(.isButton)` | `Modifier.semantics { role = Role.Button }`                 |
| **Live Updates**   | `aria-live="polite"`     | `.accessibilityLiveRegion(.polite)`  | `Modifier.semantics { liveRegion = LiveRegionMode.Polite }` |

## Examples

### Web: Accessible Search

```html
<form role="search">
  <label for="search-input" class="sr-only">Search products</label>
  <input type="search" id="search-input" placeholder="Search..." />
  <button type="submit" aria-label="Submit Search">
    <svg aria-hidden="true">...</svg>
  </button>
</form>
```

### iOS: Accessible Action Button

```swift
Button(action: deleteItem) {
    Image(systemName: "trash")
}
.accessibilityLabel("Delete item")
.accessibilityHint("Permanently removes this item from your list")
.accessibilityAddTraits(.isButton)
```

### Android: Accessible Toggle

```kotlin
Switch(
    checked = isEnabled,
    onCheckedChange = { onToggle() },
    modifier = Modifier.semantics {
        contentDescription = "Enable notifications"
    }
)
```

## Anti-Patterns to Avoid

- **Div-Buttons**: Using a `<div>` or `<span>` for a click event without adding a role and keyboard support.
- **Color-Only Meaning**: Indicating an error or status _only_ with a color change (e.g., turning a border red).
- **Uncontained Modal Focus**: Modals that don't trap focus, allowing keyboard users to navigate background content while the modal is open. Focus must be contained _and_ escapable via the `Escape` key or an explicit close button (WCAG SC 2.1.2).
- **Redundant Alt Text**: Using "Image of..." or "Picture of..." in alt text (screen readers already announce the role "Image").

## Best Practices Checklist

- [ ] Interactive elements meet the **24x24px** (Web) or **44x44pt** (Native) target size.
- [ ] Focus indicators are clearly visible and high-contrast.
- [ ] Modals **contain focus** while open, and release it cleanly on close (`Escape` key or close button).
- [ ] Dropdowns and menus restore focus to the trigger element on close.
- [ ] Forms provide text-based error suggestions.
- [ ] All icon-only buttons have a descriptive text label.
- [ ] Content reflows properly when text is scaled.

## References

- [WCAG 2.2 Guidelines](https://www.w3.org/TR/WCAG22/)
- [WAI-ARIA Authoring Practices](https://www.w3.org/TR/wai-aria-practices/)
- [iOS Accessibility Programming Guide](https://developer.apple.com/documentation/accessibility)
- [iOS Human Interface Guidelines - Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility)
- [Android Accessibility Developer Guide](https://developer.android.com/guide/topics/ui/accessibility)

## Composite WAI-ARIA Widget Patterns

### Dialog with Focus Trap (`role="dialog"` + `aria-modal`)

A modal must trap keyboard focus inside while open and restore it to the trigger on close.

```html
<button id="open-dialog">Open Settings</button>

<div
  id="settings-dialog"
  role="dialog"
  aria-modal="true"
  aria-labelledby="dialog-title"
  aria-describedby="dialog-desc"
  hidden
>
  <h2 id="dialog-title">Settings</h2>
  <p id="dialog-desc">Adjust your account preferences below.</p>

  <label for="theme-select">Theme</label>
  <select id="theme-select">
    <option>Light</option>
    <option>Dark</option>
  </select>

  <button id="dialog-close">Close</button>
</div>
```

```js
// Minimal focus-trap implementation
const FOCUSABLE = 'a[href],button:not([disabled]),input,select,textarea,[tabindex]:not([tabindex="-1"])';

function openDialog(dialog, trigger) {
  dialog.hidden = false;
  const focusable = [...dialog.querySelectorAll(FOCUSABLE)];
  focusable[0]?.focus();

  dialog.addEventListener('keydown', function trap(e) {
    if (e.key === 'Escape') { closeDialog(dialog, trigger); dialog.removeEventListener('keydown', trap); return; }
    if (e.key !== 'Tab') return;
    const first = focusable[0], last = focusable[focusable.length - 1];
    if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
    else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
  });
}

function closeDialog(dialog, trigger) {
  dialog.hidden = true;
  trigger.focus(); // restore focus to trigger
}
```

### Combobox (`role="combobox"` + `aria-expanded` / `aria-controls` / `aria-activedescendant`)

```html
<label for="country-input">Country</label>
<div class="combobox-wrapper">
  <input
    id="country-input"
    type="text"
    role="combobox"
    aria-expanded="false"
    aria-autocomplete="list"
    aria-controls="country-listbox"
    aria-activedescendant=""
    autocomplete="off"
  />
  <ul id="country-listbox" role="listbox" aria-label="Countries" hidden>
    <li id="opt-au" role="option" aria-selected="false">Australia</li>
    <li id="opt-ca" role="option" aria-selected="false">Canada</li>
    <li id="opt-us" role="option" aria-selected="false">United States</li>
  </ul>
</div>
```

Key attributes to keep in sync as the user navigates:
- `aria-expanded="true"` when the listbox is visible.
- `aria-activedescendant` set to the `id` of the currently highlighted option.
- `aria-selected="true"` on the confirmed selection; `"false"` on all others.

### Tabs (`role="tablist"` / `role="tab"` / `role="tabpanel"`)

```html
<div class="tabs">
  <ul role="tablist" aria-label="Order details">
    <li>
      <button
        id="tab-summary"
        role="tab"
        aria-selected="true"
        aria-controls="panel-summary"
        tabindex="0"
      >Summary</button>
    </li>
    <li>
      <button
        id="tab-items"
        role="tab"
        aria-selected="false"
        aria-controls="panel-items"
        tabindex="-1"
      >Items</button>
    </li>
  </ul>

  <div id="panel-summary" role="tabpanel" aria-labelledby="tab-summary" tabindex="0">
    <!-- summary content -->
  </div>
  <div id="panel-items" role="tabpanel" aria-labelledby="tab-items" tabindex="0" hidden>
    <!-- items content -->
  </div>
</div>
```

Keyboard contract: `ArrowLeft`/`ArrowRight` move focus between tabs; `Home`/`End` jump to first/last. Set `tabindex="0"` on the active tab, `tabindex="-1"` on all others. Activate on focus (recommended for desktop) or on `Enter`/`Space` (manual activation).

## Automated Accessibility Testing

### jest-axe (unit / component level)

```ts
// Button.test.tsx
import { render } from '@testing-library/react';
import { axe, toHaveNoViolations } from 'jest-axe';
import { IconButton } from './IconButton';

expect.extend(toHaveNoViolations);

it('has no axe violations', async () => {
  const { container } = render(
    <IconButton icon="trash" label="Delete item" onClick={() => {}} />
  );
  const results = await axe(container);
  expect(results).toHaveNoViolations();
});
```

### @axe-core/playwright (integration / E2E level)

```ts
// dialog.spec.ts
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test('settings dialog is accessible', async ({ page }) => {
  await page.goto('/settings');
  await page.getByRole('button', { name: 'Open Settings' }).click();
  await page.getByRole('dialog').waitFor();

  const results = await new AxeBuilder({ page })
    .include('[role="dialog"]')
    .analyze();

  expect(results.violations).toEqual([]);
});
```

Install: `npm install --save-dev jest-axe @axe-core/playwright`

## Motion & Auto-Playing Surfaces

### SC 2.2.2 Pause, Stop, Hide

Any content that starts automatically, moves, scrolls, or auto-updates, lasts longer than 5 seconds, and is presented in parallel with other content must give the user a way to pause, stop, or hide it — a marquee, an auto-advancing carousel, a ticker. The requirement does not apply if the moving content is **pure decoration**: it conveys no information and is not part of an activity (e.g. a looping ambient background video with no controls, no text, no call to action).

```html
<!-- BAD: auto-advancing carousel with no pause control -->
<div class="carousel" data-autoplay="4000">...</div>

<!-- GOOD: visible pause control, autoplay stops on interaction -->
<div class="carousel" data-autoplay="4000">
  <button type="button" class="carousel-pause" aria-pressed="false" aria-label="Pause carousel">
    <span class="icon-pause" aria-hidden="true"></span>
  </button>
  <!-- slides -->
</div>
```

```js
const pauseBtn = document.querySelector('.carousel-pause');
pauseBtn.addEventListener('click', () => {
  const paused = pauseBtn.getAttribute('aria-pressed') === 'true';
  pauseBtn.setAttribute('aria-pressed', String(!paused));
  paused ? resumeAutoplay() : stopAutoplay();
});
```

### SC 2.3.3 Animation from Interactions

Motion animation triggered by an interaction (parallax scroll effects, hover-triggered pans, cursor-follow elements) should be disable-able unless the animation is essential to the function or information being conveyed. Respect `prefers-reduced-motion` (see the vanilla CSS/JS pattern in `frontend-a11y`) rather than shipping a separate settings toggle when the OS-level signal already covers it.

### Canvas / WebGL Basics

`<canvas>` and WebGL scenes (Three.js heroes, 3D product viewers) are invisible to the accessibility tree by default — the canvas is a single opaque bitmap.

```html
<!-- BAD: canvas has no accessible name, no fallback -->
<canvas id="hero-scene"></canvas>

<!-- GOOD: role + label describe what the scene shows; fallback content for no-JS/no-WebGL -->
<canvas id="hero-scene" role="img" aria-label="Rotating 3D preview of the Black Rose jacket">
  <p>Interactive 3D preview unavailable. <a href="/product/black-rose-jacket">View product photos</a>.</p>
</canvas>
```

- Any interaction possible with the mouse (drag-to-rotate, pinch-to-zoom, click-to-select-color) needs a keyboard equivalent (arrow keys to rotate, +/- to zoom, a visible button/select for variant choice) — a 3D viewer that only responds to drag/scroll locks out keyboard-only users entirely.
- If the canvas conveys information beyond decoration (a chart, a configurator, a product state), that information must also exist in a non-canvas form (a data table, a text summary, an HTML control) so screen reader users aren't excluded.

## Related Skills

- `frontend-patterns`
- `design-system`
- `liquid-glass-design`
