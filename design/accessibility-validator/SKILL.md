---
name: react-accessibility-validator
description: Automatically validate React/Next.js components meet WCAG 2.1 AA standards. Use when creating components, forms, buttons, modals, navigation, or any interactive UI elements.
---

# Accessibility Validator

Auto-enforces WCAG 2.1 AA accessibility standards for all React/Next.js components.

## Activation Triggers

This skill activates when:
- Creating React/Next.js components
- Building forms, buttons, modals, navigation
- Adding interactive elements
- Mentioning "component", "UI", "form", "button"
- Creating pages or layouts
- Working on user-facing features

## WCAG 2.1 AA Requirements (MANDATORY)

All components MUST meet:
- ✅ **Keyboard navigation** - All interactive elements focusable and usable via keyboard
- ✅ **Semantic HTML** - Proper HTML elements and ARIA attributes
- ✅ **Color contrast** - 4.5:1 for normal text, 3:1 for large text
- ✅ **Screen reader support** - All content accessible to assistive technologies
- ✅ **Focus management** - Visible focus indicators, logical tab order
- ✅ **Form accessibility** - Labels, error announcements, help text

## Auto-Validation Process

### Step 1: Detect Component Creation

When detecting component being written:

```tsx
// Component without accessibility
function LoginButton({ onClick }) {
  return <div onClick={onClick}>Login</div>  // ❌ Multiple issues!
}
```

### Step 2: Run Accessibility Checklist

Verify:
1. ❌ Using div instead of button (semantic HTML)
2. ❌ No keyboard support (only onClick, no onKeyDown)
3. ❌ Not focusable (div not in tab order)
4. ❌ No ARIA attributes
5. ❌ No focus styles

### Step 3: Auto-Fix Violations

**Before (Inaccessible):**
```tsx
function LoginButton({ onClick }) {
  return <div onClick={onClick}>Login</div>
}
```

**After (Accessible):**
```tsx
function LoginButton({ onClick }) {
  return (
    <button
      onClick={onClick}
      type="button"
      className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
    >
      Login
    </button>
  )
}
```

### Step 4: Explain Fixes

> **Accessibility Violations Fixed**
>
> **Changes:**
> 1. ✅ Changed `<div>` to `<button>` (semantic HTML)
> 2. ✅ Added `type="button"` (prevents form submission)
> 3. ✅ Button is now keyboard accessible (Enter/Space keys work)
> 4. ✅ Automatically focusable (in tab order)
> 5. ✅ Added visible focus ring (focus:ring-2)
>
> **Why:**
> - Buttons are natively accessible to keyboard and screen readers
> - Focus ring shows keyboard users where they are
> - Proper semantics help assistive technologies

## Common Accessibility Patterns

### Pattern 1: Buttons vs Links

```tsx
// ❌ WRONG - div as button
<div onClick={handleClick}>Click me</div>

// ❌ WRONG - link as button
<a href="#" onClick={handleClick}>Click me</a>

// ✅ CORRECT - button for actions
<button onClick={handleClick} type="button">
  Click me
</button>

// ✅ CORRECT - link for navigation
<Link href="/page">Go to page</Link>
```

### Pattern 2: Form Labels

```tsx
// ❌ WRONG - no label
<input type="email" placeholder="Email" />

// ❌ WRONG - placeholder as label (insufficient)
<input type="email" placeholder="Enter your email" />

// ✅ CORRECT - explicit label
<label htmlFor="email" className="block text-sm font-medium">
  Email Address
</label>
<input
  id="email"
  type="email"
  className="mt-1 block w-full rounded-md border-gray-300"
  aria-required="true"
/>

// ✅ CORRECT - with error handling
<label htmlFor="email" className="block text-sm font-medium">
  Email Address
</label>
<input
  id="email"
  type="email"
  aria-invalid={!!errors.email}
  aria-describedby={errors.email ? "email-error" : undefined}
/>
{errors.email && (
  <p id="email-error" className="mt-1 text-sm text-red-600" role="alert">
    {errors.email.message}
  </p>
)}
```

### Pattern 3: Modal Dialogs

```tsx
// ✅ CORRECT - Accessible modal
import { Dialog } from '@headlessui/react'

function Modal({ isOpen, onClose, title, children }) {
  return (
    <Dialog
      open={isOpen}
      onClose={onClose}
      className="relative z-50"
    >
      {/* Backdrop */}
      <div className="fixed inset-0 bg-black/30" aria-hidden="true" />

      {/* Modal */}
      <div className="fixed inset-0 flex items-center justify-center p-4">
        <Dialog.Panel className="bg-white rounded-lg p-6 max-w-md">
          <Dialog.Title className="text-lg font-semibold">
            {title}
          </Dialog.Title>

          <div className="mt-4">
            {children}
          </div>

          <button
            onClick={onClose}
            className="mt-4 px-4 py-2 bg-gray-200 rounded"
            aria-label="Close dialog"
          >
            Close
          </button>
        </Dialog.Panel>
      </div>
    </Dialog>
  )
}
```

### Pattern 4: Icon Buttons

```tsx
// ❌ WRONG - no accessible name
<button>
  <XIcon />
</button>

// ✅ CORRECT - with aria-label
<button aria-label="Close" type="button">
  <XIcon className="h-5 w-5" aria-hidden="true" />
</button>

// ✅ CORRECT - with visually hidden text
<button type="button" className="relative">
  <span className="sr-only">Close</span>
  <XIcon className="h-5 w-5" aria-hidden="true" />
</button>
```

### Pattern 5: Loading States

```tsx
// ❌ WRONG - no screen reader announcement
{isLoading && <Spinner />}

// ✅ CORRECT - with live region
{isLoading && (
  <div role="status" aria-live="polite">
    <Spinner />
    <span className="sr-only">Loading...</span>
  </div>
)}
```

### Pattern 6: Images

```tsx
// ❌ WRONG - no alt text
<img src="/logo.png" />

// ✅ CORRECT - with alt text
<img src="/logo.png" alt="Company Logo" />

// ✅ CORRECT - decorative image
<img src="/decoration.png" alt="" aria-hidden="true" />
```

## Keyboard Navigation Checklist

For every component, verify:

- ✅ All interactive elements are focusable (button, a, input, etc.)
- ✅ Tab order is logical (follows visual flow)
- ✅ Focus is visible (outline, ring, or custom indicator)
- ✅ No keyboard traps (can escape from all UI)
- ✅ Enter/Space work on buttons
- ✅ Escape closes modals/dropdowns
- ✅ Arrow keys work in lists/menus

## Color Contrast Requirements

Check all text meets minimum contrast:

```tsx
// ❌ WRONG - insufficient contrast (2.5:1)
<p className="text-gray-400 bg-white">Low contrast text</p>

// ✅ CORRECT - good contrast (7:1)
<p className="text-gray-900 bg-white">High contrast text</p>

// ✅ CORRECT - large text can be 3:1
<h1 className="text-2xl text-gray-600 bg-white">Large heading</h1>
```

**Minimum Ratios:**
- Normal text (< 18pt): 4.5:1
- Large text (≥ 18pt or bold ≥ 14pt): 3:1
- UI components: 3:1

## Screen Reader Support

### Landmark Regions

```tsx
// ✅ CORRECT - proper landmarks
<header role="banner">
  <nav role="navigation" aria-label="Main navigation">
    {/* nav items */}
  </nav>
</header>

<main role="main">
  {/* main content */}
</main>

<aside role="complementary" aria-label="Related content">
  {/* sidebar */}
</aside>

<footer role="contentinfo">
  {/* footer */}
</footer>
```

### ARIA Labels

```tsx
// ✅ CORRECT - descriptive labels
<button aria-label="Add item to cart">
  <PlusIcon aria-hidden="true" />
</button>

<nav aria-label="Breadcrumb">
  <ol>
    <li><a href="/">Home</a></li>
    <li aria-current="page">Products</li>
  </ol>
</nav>
```

### Live Regions

```tsx
// ✅ CORRECT - announce changes
<div role="alert" aria-live="assertive">
  Error: Please fill in all required fields
</div>

<div role="status" aria-live="polite">
  5 items in cart
</div>
```

## Focus Management

```tsx
'use client'
import { useEffect, useRef } from 'react'

function Modal({ isOpen, title }) {
  const titleRef = useRef<HTMLHeadingElement>(null)

  // Focus title when modal opens
  useEffect(() => {
    if (isOpen && titleRef.current) {
      titleRef.current.focus()
    }
  }, [isOpen])

  return (
    <div role="dialog" aria-modal="true">
      <h2 ref={titleRef} tabIndex={-1} className="outline-none">
        {title}
      </h2>
      {/* content */}
    </div>
  )
}
```

## Testing Recommendations

Suggest automated tests:

```tsx
import { render } from '@testing-library/react'
import { axe, toHaveNoViolations } from 'jest-axe'

expect.extend(toHaveNoViolations)

test('LoginButton has no accessibility violations', async () => {
  const { container } = render(<LoginButton onClick={() => {}} />)
  const results = await axe(container)
  expect(results).toHaveNoViolations()
})
```

## Common Violations Checked

### Missing Labels
- Form inputs without labels
- Icon buttons without aria-label
- Images without alt text

### Poor Semantics
- Divs instead of buttons
- Links instead of buttons
- Missing heading hierarchy

### Keyboard Issues
- Elements not in tab order
- Missing focus indicators
- Keyboard traps

### Screen Reader Issues
- Missing ARIA labels
- Incorrect ARIA roles
- No live region announcements

### Color Issues
- Insufficient contrast
- Color-only information
- Missing text alternatives

## Integration with Tailwind CSS (Tailwind v4 CSS-First)

Tailwind CSS v4 uses a CSS-first architecture with `@import "tailwindcss";` and `@theme` in CSS. No `tailwind.config.js` is required. Accessible design tokens (contrast colors, focus rings) should be defined directly in CSS `@theme`:

```css
/* app/globals.css */
@import "tailwindcss";

@theme {
  --color-focus-ring: #2563eb;
  --color-text-high-contrast: #111827;
  --color-text-muted: #4b5563;
}
```

Accessible utility usage in components:

```tsx
// Utility class for screen reader only text
<span className="sr-only">Accessible description</span>

// Focus ring utilities (visible focus indicator)
<button className="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-600 focus-visible:ring-offset-2">
  Click me
</button>

// High contrast text & forced colors for accessibility
<p className="text-gray-900 dark:text-gray-100 forced-colors:text-[CanvasText]">
  Good contrast in both modes and high contrast mode
</p>
```

## Success Criteria

✅ All interactive elements keyboard accessible
✅ All images have alt text
✅ All forms have labels
✅ Color contrast ≥ 4.5:1 (normal text)
✅ Proper semantic HTML used
✅ ARIA attributes where needed
✅ Focus indicators visible
✅ Screen reader tested
✅ Automated axe tests pass

## Behavior

**Proactive enforcement:**
- Check accessibility without being asked
- Fix violations immediately
- Add ARIA attributes automatically
- Explain WCAG criteria for each fix
- Suggest automated tests

**Never:**
- Require explicit "check accessibility" request
- Wait for accessibility audit
- Just warn without fixing

**Block completion if:**
- Buttons are divs
- Forms lack labels
- Color contrast fails
- Icon buttons lack accessible names
- Images missing alt text

This ensures every component is accessible from day one.
