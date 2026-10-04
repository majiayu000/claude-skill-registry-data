---
name: accessibility-audit
description: Audit and fix accessibility in ProAnimate's editor UI. Covers ARIA, keyboard navigation, focus management, color contrast, and reduced motion. Use when creating or modifying any interactive component.
user-invocable: true
argument-hint: [component or area to audit]
---

# Accessibility Audit

## Current State

ProAnimate has near-zero accessibility implementation. This skill exists to change that incrementally.

## Requirements (WCAG 2.1 AA)

### 1. Keyboard Navigation

**Every interactive element must be reachable via Tab and operable via Enter/Space.**

Priority areas:
- Timeline track selection and scrubbing (arrow keys)
- Layer list reordering (arrow keys + modifier for move)
- Panel tab switching (arrow keys within tab group)
- Canvas zoom/pan (keyboard shortcuts documented in settings)
- Modal focus trapping (Tab cycles within modal, Escape closes)

Pattern for list navigation:
```tsx
const handleKeyDown = (e: React.KeyboardEvent, index: number) => {
  if (e.key === 'ArrowDown') {
    e.preventDefault()
    focusItem(index + 1)
  } else if (e.key === 'ArrowUp') {
    e.preventDefault()
    focusItem(index - 1)
  }
}
```

### 2. ARIA Labels

**Every icon-only button needs `aria-label`. Every region needs `role` and `aria-label`.**

```tsx
// Icon buttons
<IconButton aria-label="Delete layer" icon={Trash2} onClick={onDelete} />

// Panel regions
<div role="region" aria-label="Layer properties">

// Live updates (toasts, status changes)
<div role="status" aria-live="polite">{statusMessage}</div>

// Dialogs
<div role="dialog" aria-modal="true" aria-labelledby="dialog-title">
```

### 3. Color Contrast

Minimum contrast ratios (WCAG AA):
- Normal text: 4.5:1
- Large text (18px+ or 14px bold): 3:1
- UI components and graphical objects: 3:1

Current palette check:
| Combo | Ratio | Pass? |
|-------|-------|-------|
| white on #2a2a2a | 12.6:1 | Yes |
| gray-400 on #2a2a2a | 5.1:1 | Yes |
| gray-500 on #2a2a2a | 3.4:1 | Fails for normal text |
| #4a7eff on #2a2a2a | 4.2:1 | Fails for normal text |

**Fix needed:** `text-gray-500` sublabels and accent-colored text need contrast adjustment on dark backgrounds.

### 4. Reduced Motion

```tsx
// Tailwind prefix for all animations
className="motion-safe:animate-pulse"
className="motion-safe:transition-all motion-safe:duration-200"

// JS check for complex animations
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches
```

Apply to: panel transitions, modal animations, canvas preview playback speed indicator, skeleton loaders.

### 5. Focus Management

```tsx
// Focus ring (consistent across all interactive elements)
className="focus-visible:ring-1 focus-visible:ring-[#4a7eff] focus-visible:ring-offset-1 focus-visible:ring-offset-[#1e1e1e] outline-none"

// Auto-focus on modal open
useEffect(() => {
  if (isOpen) firstFocusRef.current?.focus()
}, [isOpen])

// Return focus on close
useEffect(() => {
  const trigger = document.activeElement
  return () => (trigger as HTMLElement)?.focus()
}, [])
```

## Audit Checklist

When creating or modifying any component, check:

- [ ] Can I Tab to every interactive element?
- [ ] Do all icon-only buttons have `aria-label`?
- [ ] Do lists support arrow key navigation?
- [ ] Does Escape close any overlay/modal/dropdown?
- [ ] Is focus trapped inside open modals?
- [ ] Does focus return to trigger element on close?
- [ ] Are loading states announced to screen readers?
- [ ] Are error messages associated with their inputs via `aria-describedby`?
- [ ] Do animations respect `prefers-reduced-motion`?
- [ ] Does the component work without color as the only indicator?
