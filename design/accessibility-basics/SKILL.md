---
name: accessibility-basics
category: frontend
description: Use on every UI change - semantic HTML, labels for controls, keyboard-navigable dialogs/menus, visible focus, and never color as the only signal
source: vercel-labs/web-interface-guidelines (MIT), adapted
---
# Accessibility Basics

## Overview

Accessibility is not a pass at the end — it's built into each component. The recurring defects are `div` with `onClick` instead of a button, icon buttons with no label, and custom menus/dialogs that trap keyboard users.

**Core principle:** Semantic HTML and the accessible primitives do most of the work — reach for them first.

## Rules

- **Semantic HTML first:** `button` for actions, `a` for navigation, headings in order with exactly one `<h1>` per page. A `div` with `onClick` is a defect (no keyboard, no role).
- **Every control is labeled:** every form control has an associated `<label>`; every icon-only button has an `aria-label`; decorative icons are `aria-hidden`.
- **Dialogs and menus are keyboard-navigable:** focus moves in on open, is trapped while open, and returns to the trigger on close — the Radix primitives do this, so use them instead of hand-rolling.
- **Visible focus everywhere:** never remove an outline without a replacement `:focus-visible` style; sticky/fixed elements never cover the focus ring.
- **Color is never the only signal:** pair status with an icon or text; keep contrast ≥4.5:1 for body text and ≥3:1 for large text, in both themes.
- **Touch and zoom:** hit targets ≥44px on phone / ≥24px on desktop (pad a smaller visual out to that size); a checkbox or radio shares one hit target with its label (`<label>` wrapping both, or `htmlFor`) so the combined row reaches 44px with no dead zone between box and text; `<input>` font size ≥16px on phones to stop iOS auto-zoom; never disable browser zoom (`user-scalable=no`, `maximum-scale=1`).
- **Motion:** respect `prefers-reduced-motion` via `motion-reduce:` on any animation you add; smooth anchor scrolling only as `motion-safe:scroll-smooth` on `<html>`, never unconditional `scroll-behavior: smooth`.
- **Structure for screen readers:** page landmarks (`header`, `nav`, `main`, `footer`), a skip-to-content link before the nav, `scroll-margin-top` on anchor targets sitting under a sticky header, and `lang` on `<html>` matching the active locale.
- **Live regions:** toasts and inline validation messages use `aria-live="polite"` so assistive tech announces them without stealing focus.
- **Forms:** on submit, move focus to the first invalid field; its error is linked with `aria-describedby` and the field carries `aria-invalid`.

## Worked Example

```tsx
// ❌ not keyboard-accessible, no role, no label
<div className="icon-btn" onClick={onDelete}><TrashIcon /></div>

// ✅ real button, labeled, gets focus + Enter/Space for free
<button type="button" aria-label="Delete task" onClick={onDelete}>
  <TrashIcon aria-hidden />
</button>
```

The `button` is focusable and keyboard-activatable with no extra code; the `aria-label` gives screen readers the action; `aria-hidden` on the icon stops it being announced twice.

## Proving keyboard behaviour

There is no keyboard-press browser tool at runtime (`browser_click`/`browser_fill` only) — prove tab order, `Escape`, and focus-return in a co-located RTL component test instead of a manual browser pass:

```tsx
test("closes on Escape and returns focus to the trigger", async () => {
  const user = userEvent.setup();
  render(<MenuExample />);
  await user.click(screen.getByRole("button", { name: "Actions" }));
  await user.keyboard("{Escape}");
  expect(screen.getByRole("button", { name: "Actions" })).toHaveFocus();
});
```

`user.tab()` walks focus order, `user.keyboard('{Escape}')` fires the key, `toHaveFocus()` asserts the result — this is how keyboard behaviour is verified since the browser tools have no key-press action.

## Common Mistakes

- `div`/`span` with `onClick` for an action.
- Icon-only button with no `aria-label`.
- A hand-rolled dropdown/dialog that traps keyboard users → use the Radix primitive.
- Removing focus outlines with no replacement.
- Status shown by color alone.
- A touch target under 44px on phone, or `<input>` text under 16px causing iOS zoom.
- Shipping a keyboard interaction with no test proving it.

## Red Flags

- A clickable element that isn't a `button`/`a`.
- An interactive widget you built from raw `div`s instead of a primitive.
- `outline: none` with nothing in its place.
- `user-scalable=no` or `maximum-scale=1` in a viewport meta tag.
- A component test suite with no `user.tab()`/`user.keyboard()` coverage for a new interactive widget.
