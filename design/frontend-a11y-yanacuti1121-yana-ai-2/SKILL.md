---
name: frontend-a11y
description: Accessibility patterns for React/Next.js — semantic HTML, ARIA, form labeling, keyboard navigation, focus management, screen reader support. WCAG 2.2 AA compliance.
license: MIT
source: https://github.com/affaan-m/ECC
---

# Frontend Accessibility (a11y)

**Trigger phrases:** "accessibility", "a11y", "WCAG", "screen reader", "keyboard navigation", "ARIA", "focus trap", "semantic HTML"

## Semantic HTML First

```tsx
// ✅ Native elements
<button onClick={handleSubmit}>Submit</button>
<nav aria-label="Main navigation">...</nav>

// ❌ Div soup
<div onClick={handleSubmit} className="btn">Submit</div>
```

## ARIA Attributes

```tsx
<button aria-label="Close dialog">✕</button>
<div aria-live="polite">{statusMessage}</div>
<div role="alert">{errorMessage}</div>
<button aria-expanded={isOpen} aria-controls="menu-id">Menu</button>
```

## Form Labeling

```tsx
<label htmlFor="email">Email address</label>
<input id="email" type="email" aria-required="true"
  aria-invalid={hasError} aria-describedby={hasError ? 'email-err' : undefined} />
{hasError && <p id="email-err" role="alert">{error}</p>}
```

## Keyboard Navigation

```tsx
// ✅ Focus visible — never remove outline globally
// Tailwind: focus-visible:ring-2 focus-visible:ring-blue-500

// ✅ Skip link
<a href="#main" className="sr-only focus:not-sr-only">Skip to main content</a>
```

## Focus Management (Modals)

```tsx
import FocusTrap from 'focus-trap-react'

function Modal({ isOpen, onClose, children }) {
  if (!isOpen) return null
  return (
    <FocusTrap>
      <div role="dialog" aria-modal="true" aria-labelledby="title">
        <h2 id="title">Title</h2>
        {children}
        <button onClick={onClose}>Close</button>
      </div>
    </FocusTrap>
  )
}
```

## Screen Reader

```tsx
<button><SearchIcon aria-hidden="true" /><span className="sr-only">Search</span></button>
<img src="/hero.jpg" alt="Team collaborating in office" />
<img src="/divider.png" alt="" />  {/* decorative */}
```

## Contrast (WCAG 2.2 AA)

```
Normal text: ≥ 4.5:1
Large text (≥18px): ≥ 3:1
UI components: ≥ 3:1
```

## Anti-Fake-Pass

```
❌ outline: none on :focus without :focus-visible alternative
❌ Color alone to convey status (need icon + text)
❌ Modal without ESC to close
❌ aria-label on a div instead of semantic element
❌ Skipping heading levels (h1 → h3)
```
