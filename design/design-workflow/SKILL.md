---
name: design-workflow
description: UI/UX design workflow guidelines. Activate when working with design systems, accessibility (WCAG), user interface patterns, or design tokens.
location: user
---

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in RFC 2119.

# Design Workflow

## Core Principles

1. **Clarity over decoration** - Function before form
2. **Consistency over novelty** - Reuse patterns
3. **Accessibility over convenience** - WCAG 2.1 AA minimum
4. **Performance over polish** - Fast > pretty
5. **Feedback over silence** - Always show state
6. **Progressive disclosure** - Show what's needed when needed

---

## Accessibility Requirements

Accessibility is NOT optional. All implementations MUST achieve these standards.

### Color Contrast (MUST Achieve)

- **Normal text**: MUST have 4.5:1 contrast ratio minimum
- **Large text** (18px+ or 14px+ bold): MUST have 3:1 contrast ratio minimum
- **UI components/focus indicators**: MUST have 3:1 contrast ratio

### Keyboard Navigation (MUST Achieve)

- All interactive elements MUST be focusable via Tab key
- Focus order MUST follow logical reading order
- Custom components MUST implement appropriate ARIA roles
- Escape key MUST close modals and dropdowns
- Arrow keys SHOULD navigate within composite widgets

```typescript
// Focus trap for modals - REQUIRED
const useFocusTrap = (containerRef: RefObject<HTMLElement>) => {
  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;
    const focusables = container.querySelectorAll(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );
    const first = focusables[0] as HTMLElement;
    const last = focusables[focusables.length - 1] as HTMLElement;
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key !== 'Tab') return;
      if (e.shiftKey && document.activeElement === first) {
        e.preventDefault(); last.focus();
      } else if (!e.shiftKey && document.activeElement === last) {
        e.preventDefault(); first.focus();
      }
    };
    container.addEventListener('keydown', handleKeyDown);
    first?.focus();
    return () => container.removeEventListener('keydown', handleKeyDown);
  }, [containerRef]);
};
```

### Focus Management (MUST Achieve)

- Opening modal MUST move focus to modal; closing MUST return focus to trigger
- Route changes SHOULD move focus to main content or heading
- Error states MUST announce to screen readers

### Screen Reader Testing (MUST Test With)

- **macOS/iOS**: VoiceOver | **Windows**: NVDA/JAWS | **Android**: TalkBack
- All images: meaningful alt text (alt="" for decorative)
- Form inputs: associated labels | Headings: logical hierarchy
- Dynamic content: aria-live regions | Interactive elements: accessible names

### Reduced Motion (MUST Respect)

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

### Lighthouse Score: MUST be >95

Run: `npx lighthouse <url> --only-categories=accessibility`

---

## Design Tokens

Design tokens MUST be the single source of truth for visual styling.

```css
:root {
  /* Colors - Semantic */
  --color-primary: #2563eb;
  --color-primary-hover: #1d4ed8;
  --color-secondary: #64748b;
  --color-success: #16a34a;
  --color-warning: #ca8a04;
  --color-error: #dc2626;
  /* Colors - Neutral */
  --color-neutral-50: #fafafa;
  --color-neutral-100: #f4f4f5;
  --color-neutral-200: #e4e4e7;
  --color-neutral-700: #3f3f46;
  --color-neutral-800: #27272a;
  --color-neutral-900: #18181b;
  /* Spacing - 4px base */
  --space-1: 0.25rem; --space-2: 0.5rem; --space-3: 0.75rem;
  --space-4: 1rem; --space-6: 1.5rem; --space-8: 2rem;
  --space-12: 3rem; --space-16: 4rem;
  /* Typography */
  --font-sans: system-ui, -apple-system, sans-serif;
  --font-mono: ui-monospace, 'Cascadia Code', monospace;
  --text-xs: 0.75rem; --text-sm: 0.875rem; --text-base: 1rem;
  --text-lg: 1.125rem; --text-xl: 1.25rem; --text-2xl: 1.5rem;
  --leading-tight: 1.25; --leading-normal: 1.5; --leading-relaxed: 1.75;
}
```

---

## Dark Mode Implementation

```css
:root {
  --bg-primary: #ffffff;
  --bg-secondary: #f4f4f5;
  --text-primary: #18181b;
  --text-secondary: #52525b;
  --border-color: #e4e4e7;
}
:root.dark {
  --bg-primary: #18181b;
  --bg-secondary: #27272a;
  --text-primary: #fafafa;
  --text-secondary: #a1a1aa;
  --border-color: #3f3f46;
}
@media (prefers-color-scheme: dark) {
  :root:not(.light) { /* Apply dark values */ }
}
```

- MUST persist user preference (localStorage)
- MUST respect prefers-color-scheme as default
- MUST NOT flash wrong theme on load
- SHOULD use `color-scheme: dark` for native elements

---

## Component Patterns

### Buttons

```css
.btn {
  display: inline-flex; align-items: center; justify-content: center;
  gap: var(--space-2); padding: var(--space-2) var(--space-4);
  font-weight: 500; border-radius: 0.375rem;
  transition: background-color 150ms, box-shadow 150ms;
}
.btn:focus-visible { outline: 2px solid var(--color-primary); outline-offset: 2px; }
.btn:disabled { opacity: 0.5; cursor: not-allowed; }
```

- MUST have visible focus state
- MUST be minimum 44x44px touch target on mobile
- MUST show loading state during async operations
- SHOULD NOT rely on color alone to convey meaning

### Forms

```html
<div class="form-field">
  <label for="email">Email address</label>
  <input type="email" id="email" aria-describedby="email-error" aria-invalid="true" />
  <span id="email-error" role="alert">Please enter a valid email</span>
</div>
```

- Labels MUST be visible (no placeholder-only labels)
- Error messages MUST be associated via aria-describedby
- Required fields MUST be indicated visually AND via aria-required
- SHOULD validate on blur, NOT on every keystroke

### Modals

- MUST trap focus within modal
- MUST close on Escape key
- MUST return focus to trigger on close
- MUST have accessible name (aria-labelledby or aria-label)
- SHOULD use `<dialog>` element when possible
- SHOULD prevent body scroll when open

---

## Motion and Animation

Animation SHOULD be subtle and purposeful. Never use motion for decoration.

```css
:root {
  --ease-out: cubic-bezier(0, 0, 0.2, 1);
  --ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);
  --duration-fast: 150ms; --duration-normal: 200ms; --duration-slow: 300ms;
}
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
@keyframes slideUp { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: translateY(0); } }
```

- Keep durations under 300ms for UI feedback
- Use ease-out for entering, ease-in for exiting elements
- MUST respect prefers-reduced-motion

---

## Responsive Design

Mobile-first approach is REQUIRED.

```css
:root { --bp-sm: 640px; --bp-md: 768px; --bp-lg: 1024px; --bp-xl: 1280px; }
.container { padding: var(--space-4); }
@media (min-width: 768px) { .container { padding: var(--space-6); } }
@media (min-width: 1024px) { .container { padding: var(--space-8); max-width: 1200px; margin: 0 auto; } }
```

- Touch targets MUST be minimum 44x44px on mobile
- Text MUST be readable without horizontal scrolling
- Images MUST be responsive (max-width: 100%)
- SHOULD use CSS Grid/Flexbox over fixed widths

---

## Loading and Error States

Every async operation MUST show appropriate feedback.

```tsx
// Loading
<button disabled={isLoading}>
  {isLoading ? <><Spinner aria-hidden="true" /><span>Saving...</span></> : 'Save'}
</button>
<div aria-busy="true" aria-label="Loading content">
  <div class="skeleton skeleton-text" />
</div>

// Error
<div role="alert" class="error-banner">
  <ErrorIcon aria-hidden="true" />
  <div>
    <p class="error-message">Failed to save changes</p>
    <p class="error-detail">Please check your connection and try again</p>
  </div>
  <button onClick={retry}>Retry</button>
</div>
```

- Loading MUST be indicated within 100ms of action
- Errors MUST explain what went wrong and SHOULD suggest how to fix
- Empty states MUST guide users to next action
- MUST NOT show raw error messages to users
