---
name: apply-hover-content
description: Use when adding tooltips, popovers, or any content that appears on hover or focus — to ensure users can dismiss it, move their pointer over it, and that it doesn't disappear before they've read it.
source: W3C WCAG 2.1 SC 1.4.13 Content on Hover or Focus (Level AA); WAI-ARIA Tooltip Pattern; Inclusive Components "Tooltips and Toggletips" (Heydon Pickering)
tags: [accessibility, wcag, a11y, tooltips, hover-content, popovers, low-vision-accessibility, developer]
related: [apply-keyboard-accessibility, apply-focus-management, design-accessibility-standards]
---

# Apply Hover Content

Make tooltips and hover content dismissible, hoverable, and persistent — so low-vision users who zoom in and users who navigate by keyboard can access tooltip content.

## Why This Is Best Practice

**Adopted by:** WCAG 2.1 SC 1.4.13 (Level AA) is required by Section 508 (US), EU EN
301 549, and UK PSBAR 2018. The WAI-ARIA Tooltip Pattern is the W3C reference
implementation. Heydon Pickering's "Inclusive Components" (the definitive accessible
component guide, used as a reference at BBC, Gov.UK, and NHS Digital) documents the
specific accessible tooltip pattern.
**Impact:** Low-vision users who zoom to 200–400% frequently trigger tooltips
accidentally when moving their pointer toward content — without the ability to dismiss
or hover over the tooltip, the content overlaps and obscures what they're trying to
read. WCAG 2.1 SC 1.4.13 was added specifically because tooltip implementations at
zoom caused content to be unreadable for low-vision users.
**Why best:** Browser `title` attribute tooltips — the alternative — are inaccessible:
they're not keyboard focusable, not readable by touch users, and disappear immediately.
Custom HTML tooltips with the three WCAG requirements (dismissible, hoverable, persistent)
are the only compliant implementation.

Sources: W3C WCAG 2.1 SC 1.4.13 (2018); WAI-ARIA Tooltip Pattern; Heydon Pickering,
"Inclusive Components" (2017); BBC GEL Tooltip component

## Steps

### Step 1: Use HTML tooltip — not the `title` attribute

```html
<!-- Wrong — title attribute is inaccessible (not keyboard focusable, disappears on touch) -->
<button title="Delete this item">🗑</button>

<!-- Right — HTML tooltip with proper ARIA -->
<button aria-describedby="delete-tooltip" aria-label="Delete item">🗑</button>
<div role="tooltip" id="delete-tooltip">Delete this item permanently</div>
```

The `title` attribute fails WCAG 1.4.13 on all three counts: not keyboard accessible,
not hoverable, not persistent.

### Step 2: Show tooltip on both hover AND focus

```javascript
const trigger = document.querySelector('[aria-describedby]');
const tooltip = document.getElementById(trigger.getAttribute('aria-describedby'));

function showTooltip() {
  tooltip.removeAttribute('hidden');
}

function hideTooltip() {
  tooltip.setAttribute('hidden', '');
}

// Show on hover AND keyboard focus
trigger.addEventListener('mouseenter', showTooltip);
trigger.addEventListener('focus', showTooltip);

// Hide on mouse leave AND blur — but see Step 3 for the dismissible requirement
trigger.addEventListener('mouseleave', hideTooltip);
trigger.addEventListener('blur', hideTooltip);
```

Tooltip must appear for keyboard users (`focus`) not just mouse users (`mouseenter`).

### Step 3: Make the tooltip dismissible with Escape (without moving focus)

```javascript
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    // Hide all visible tooltips without moving focus
    document.querySelectorAll('[role="tooltip"]:not([hidden])').forEach(tip => {
      tip.setAttribute('hidden', '');
    });
    // Do NOT call trigger.blur() — focus stays where it is
  }
});
```

Escape must dismiss the tooltip and leave focus on the trigger. If the user is a
low-vision user who zoomed in and a tooltip is covering content, Escape is their
only escape without moving the mouse.

### Step 4: Make the tooltip content hoverable — pointer can move over it

```css
/* Tooltip must remain visible when pointer moves from trigger to tooltip */

.tooltip-wrapper {
  position: relative;
  display: inline-block;
}

[role="tooltip"] {
  position: absolute;
  top: calc(100% + 4px);
  left: 0;
  /* No gap between trigger and tooltip — pointer can slide directly onto it */
}
```

```javascript
// Keep tooltip visible when pointer enters the tooltip itself
tooltip.addEventListener('mouseenter', showTooltip);
tooltip.addEventListener('mouseleave', hideTooltip);
```

If a 4px gap exists between trigger and tooltip, moving the pointer across that gap
hides the tooltip before the pointer reaches it. Either remove the gap or keep the
tooltip visible with a small delay.

### Step 5: Don't add an auto-dismiss timeout

```javascript
// Wrong — tooltip disappears before user can read it
setTimeout(() => tooltip.setAttribute('hidden', ''), 2000);

// Right — tooltip persists until user moves away or presses Escape
// No timeout needed
```

A tooltip that auto-dismisses fails WCAG 1.4.13 "persistent" requirement. Users must
be able to read the tooltip for as long as they need — particularly for users with
cognitive disabilities or low vision who read slowly.

### Complete accessible tooltip CSS pattern

```css
[role="tooltip"] {
  position: absolute;
  z-index: 100;
  background: #1a1a1a;
  color: #fff;
  padding: 6px 10px;
  border-radius: 4px;
  font-size: 0.875rem;
  max-width: 280px;
  white-space: normal;
  pointer-events: auto;   /* allows hovering over tooltip */
}

[role="tooltip"][hidden] {
  display: none;
}
```

## When NOT to Use

- **Complex, interactive content in a tooltip** — if the popup contains links, buttons, or form elements, it's a popover or dialog, not a tooltip. Use `role="dialog"` and full focus management (`apply-focus-management`).
- **Information critical to completing a task** — if users need the tooltip content to use the UI correctly, it shouldn't be hidden in a tooltip. Display it as visible text, hint text, or a label.

## Common Mistakes

**Tooltip that closes when pointer moves between trigger and tooltip.** A gap between the button and tooltip hides it mid-transit. Remove the gap, use `pointer-events: auto` on the tooltip, or add a brief hide delay.

**Tooltip triggered only on hover — not keyboard focus.** Keyboard users never see tooltip content. Always bind `focus`/`blur` in addition to `mouseenter`/`mouseleave`.

**Using `title` attribute as a tooltip.** The `title` attribute is invisible on touch devices, not keyboard accessible, and not persistent. It does not satisfy WCAG 1.4.13.