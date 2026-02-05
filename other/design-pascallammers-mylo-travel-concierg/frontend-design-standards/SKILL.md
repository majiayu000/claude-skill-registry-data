---
name: frontend-design-standards
description: Use when generating React/TypeScript UI components, forms, layouts, or pages - prevents generic AI aesthetic, enforces accessibility, semantic HTML, theme compliance, minimum text sizes, proper states, and brand differentiation
---

# Frontend Design Standards

## Overview

AI-generated UI suffers from systematic failures: generic aesthetics, accessibility violations, div soup, small text, missing states, and brand blindness. This skill enforces production-quality standards that prevent the "AI look."

**Core principle:** Every component must pass accessibility, theming, responsiveness, and semantic HTML checks BEFORE considering the task complete.

## Mandatory Checklist

Run through EVERY category for EVERY component. No exceptions.

### 1. Theme Compliance (Zero Hardcoded Colors)

**FORBIDDEN - Tailwind color classes:**
```tsx
// WRONG - hardcoded colors
className="bg-gray-50 text-gray-900 border-gray-200"
className="bg-blue-600 text-white hover:bg-blue-700"
className="text-green-500 bg-red-100"
```

**REQUIRED - Theme variables:**
```tsx
// CORRECT - uses theme system
className="bg-background text-foreground border-border"
className="bg-primary text-primary-foreground hover:bg-primary/90"
className="text-success bg-destructive/10"
```


**FORBIDDEN - Hardcoded Hex Values:**
```tsx
// WRONG - magic numbers/colors
className="bg-[#F3F4F6] text-[#111827]"
style={{ backgroundColor: '#ff0000' }}
```

**Verification:**
```bash
# Find violations - any match is a failure
grep -rn "bg-gray\|bg-blue\|bg-green\|bg-red\|text-gray\|text-blue" --include="*.tsx"
grep -rn "#[0-9a-fA-F]\{3,6\}" --include="*.tsx"  # Catch hex codes
```

If a semantic color doesn't exist, ADD IT to the theme system - don't use raw Tailwind colors or Hex values.

### 2. Typography Standards (16px Minimum Body Text)

**FORBIDDEN:**
```tsx
// WRONG - below 16px minimum for readable content
className="text-sm"  // 14px - TOO SMALL for body
className="text-xs"  // 12px - TOO SMALL for any readable content
```

**ALLOWED uses of small text:**
- Timestamps, metadata, captions: `text-sm` acceptable
- Legal disclaimers: `text-xs` acceptable
- Labels for inputs: `text-sm` acceptable

**Body text, paragraphs, descriptions MUST be:**
```tsx
className="text-base"  // 16px - minimum
className="text-lg"    // 18px - preferred for long-form
```

**Line height requirement:**
```tsx
// REQUIRED - 1.5 minimum for paragraphs
className="leading-relaxed"  // 1.625
className="leading-normal"   // 1.5
```

### 3. Semantic HTML (No Div Soup)

**FORBIDDEN - Generic divs for semantic content:**
```tsx
// WRONG
<div className="navigation">
  <div onClick={handleClick}>Home</div>
</div>
```

**REQUIRED - Proper semantic elements:**

| Content Type | Required Element |
|-------------|------------------|
| Navigation | `<nav aria-label="Main">` |
| Main content area | `<main>` |
| Article/post | `<article>` |
| Section with heading | `<section aria-labelledby="id">` |
| Side content | `<aside>` |
| Page footer | `<footer>` |
| Clickable action | `<button type="button">` |
| Form submission | `<button type="submit">` |
| Navigation link | `<a href="">` or Next.js `<Link>` |
| List of items | `<ul>/<ol>` with `<li>` |
| Headings | `<h1>` through `<h6>` in order |

**Heading hierarchy rule:** Never skip levels. After `<h2>`, use `<h3>`, not `<h4>`.

### 4. Accessibility Requirements

**Skip link for keyboard users (on page layouts):**
```tsx
// REQUIRED at top of page layouts
<a
  href="#main-content"
  className="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 focus:z-50 focus:px-4 focus:py-2 focus:bg-background focus:text-foreground focus:ring-2 focus:ring-ring"
>
  Skip to main content
</a>
// ... later
<main id="main-content">
```

**Every interactive element MUST have:**

```tsx
// Buttons with icons only
<button
  aria-label="Close dialog"  // REQUIRED for icon-only buttons
  type="button"
>
  <X className="h-5 w-5" />
</button>

// Toggle buttons
<button
  aria-expanded={isOpen}  // REQUIRED for expandable controls
  aria-controls="menu-id"  // REQUIRED - ID of controlled element
>

// Form inputs
<label htmlFor="email">Email</label>  // REQUIRED - visible label
<input
  id="email"
  aria-describedby="email-error"  // REQUIRED when error present
  aria-invalid={hasError}  // REQUIRED when validation fails
/>
<p id="email-error" role="alert">{error}</p>  // Announced to screen readers
```

**Focus management:**
```tsx
// REQUIRED - visible focus indicator
className="focus:ring-2 focus:ring-ring focus:ring-offset-2"
className="focus-visible:outline-none focus-visible:ring-2"
```

**Color contrast:** Verify all text meets WCAG AA (4.5:1 for normal text, 3:1 for large text).

**Images require alt text:**
```tsx
// Informative image
<img src="chart.png" alt="Sales increased 40% in Q3" />

// Decorative image (empty alt, not missing)
<img src="decorative-swoosh.svg" alt="" role="presentation" />

// WRONG - missing alt
<img src="product.jpg" />  // Screen readers say "image" with no context
```

### 5. Component States (No Happy Path Only)

Every component that loads data or accepts input MUST handle:

| State | Required Implementation |
|-------|------------------------|
| **Loading** | Skeleton or spinner with `aria-busy="true"` |
| **Error** | Error message with `role="alert"`, retry action |
| **Empty** | Helpful empty state with action suggestion |
| **Success** | Confirmation with `role="status"` |

**FORBIDDEN - Silent failures:**
```tsx
// WRONG - just logs to console
} catch (error) {
  console.error(error);
}
```

**REQUIRED - User-visible feedback:**
```tsx
} catch (error) {
  setError("Failed to load. Please try again.");
}

// In render:
{error && (
  <div role="alert" className="text-destructive">
    {error}
    <button onClick={retry}>Retry</button>
  </div>
)}
```

### 6. Responsive Design Requirements

**Touch target minimum:**
```tsx
// REQUIRED - 44px minimum for touch targets
className="min-h-[44px] min-w-[44px]"
// Or use padding to achieve:
className="p-3"  // 12px padding + content = ~44px
```

**Mobile-first breakpoints:**
```tsx
// CORRECT - mobile first, add complexity upward
className="flex flex-col md:flex-row"
className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3"

// WRONG - desktop first with mobile overrides
className="flex flex-row sm:flex-col"  // Backwards
```

**Required responsive considerations:**
- Does navigation collapse to hamburger menu?
- Do touch targets meet 44px minimum?
- Does text remain readable without horizontal scroll?
- Do images have responsive sizing?

### 7. Brand Differentiation (Anti-Generic)

Before generating UI, ASK or DETERMINE:

1. **Color personality:** What emotions should colors evoke?
2. **Typography character:** Playful, professional, technical, luxurious?
3. **Shape language:** Sharp/angular or soft/rounded?
4. **Density:** Spacious/breathing or compact/efficient?
5. **Motion:** Bouncy/playful or subtle/refined?

**If brand requirements are vague, DO NOT default to:**
- Gray backgrounds with blue accents
- Inter/system font with slate text
- Standard 3-column feature grids
- Purple gradients

**Instead, ask:** "What makes this brand/product unique? What should users FEEL?"

### 8. Motion and Micro-interactions (Anti-Dead Interface)

AI-generated UIs often feel "static" or "dead." Consider:

```tsx
// Add meaningful transitions
className="transition-colors duration-200"
className="transition-transform hover:scale-105"

// Loading feedback
className="animate-pulse"  // skeleton loading
className="animate-spin"   // spinner
```

**Motion principles:**
- Hover states on all interactive elements
- Transitions between states (not instant jumps)
- Loading indicators for async operations
- Success/error feedback animations

**Don't overdo it:** Subtle > flashy. Respect `prefers-reduced-motion`.

### 9. Code Validity (No Hallucinations)

AI sometimes generates non-existent CSS properties or imports libraries/components that aren't installed.

**FORBIDDEN - Hallucinated/obsolete CSS:**
```css
/* These don't exist */
width: fit-parent;
text-fill-color: transparent;

/* Obsolete vendor prefixes for modern properties */
-webkit-border-radius: 8px;  /* Just use border-radius */
```

**FORBIDDEN - Hallucinated Imports:**
```tsx
// WRONG - Do not import things that don't exist
import { Sparkles } from '@heroicons/react/solid'; // Check if 'solid' exists in your version
import { useMagicHook } from 'react-use'; // Check if 'react-use' is installed
```

**Rule:**
1. **Check `package.json`** before importing a 3rd party library.
2. **Check file structure** before importing local components (don't assume `@/components/ui/card` exists).
3. **Check MDN** if unsure about a CSS property.

### 10. Project Structure (Anti-Monolith)

AI tends to dump everything into a single file. This is unmaintainable.

**FORBIDDEN - The "God Component":**
- Single file > 250 lines (unless it's a complex data table).
- Defining multiple complex sub-components in the same file.
- Mixing heavy business logic (`useEffect`, data fetching) with UI rendering.

**REQUIRED - Separation of Concerns:**
1. **Extract Types:** Move interfaces to `types.ts` if shared, or top of file.
2. **Extract Hooks:** Move complex logic to `useFeatureName.ts`.
3. **Extract Components:** If a sub-component renders > 20 lines of JSX, move it to its own file.
4. **Colocation:** Keep related files together (e.g., `components/Feature/Feature.tsx`, `components/Feature/useFeature.ts`).

## Verification Checklist

Before marking any UI work complete, verify:

- [ ] Zero hardcoded Tailwind colors OR Hex codes (grep check passes)
- [ ] Body text uses `text-base` (16px) or larger
- [ ] Semantic HTML elements for all landmarks
- [ ] All interactive elements have accessible names
- [ ] Focus indicators visible on all interactive elements
- [ ] Loading, error, and empty states implemented
- [ ] Touch targets meet 44px minimum
- [ ] Mobile layout tested (or responsive classes verified)
- [ ] Brand differentiation considered (not generic gray/blue)
- [ ] Skip link present on page layouts
- [ ] `aria-expanded` on all toggle buttons
- [ ] All images have alt text (empty for decorative)
- [ ] Hover/transition states on interactive elements
- [ ] No hallucinated CSS properties or Imports (verify existence)
- [ ] No "God Components" (>250 lines) - extracted sub-components

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "text-sm is fine for labels" | Labels yes, but body text/descriptions must be 16px+ |
| "Gray is neutral and professional" | Gray is also generic and forgettable. Ask about brand. |
| "I'll add accessibility later" | Later never comes. 80% of sites fail WCAG. Do it now. |
| "Loading states weren't requested" | Real apps have latency. Always include loading states. |
| "The design looks clean" | "Clean" often means "generic." Ask what makes it unique. |
| "Tailwind gray matches the theme" | Use theme variables. `bg-muted` exists for this. |
| "Mobile can be handled later" | 60%+ traffic is mobile. Design mobile-first. |
| "Div works fine here" | Divs have no semantic meaning. Use proper elements. |
| "Client is waiting, no time to ask" | 5 min asking saves hours of rework. Ask about brand. |
| "Just console.error is fine" | Users see nothing. Always show visible error feedback. |
| "Skip link is overkill" | Keyboard users can't use your site without it. Required. |
| "I'll make it unique with colors" | Unique = structure + typography + spacing, not just hue. |
| "aria-label on every button is tedious" | Accessibility is not optional. Screen readers need it. |
| "Alt text can be added later" | Missing alt = broken for screen readers. Add it now. |
| "This CSS property should work" | If MDN doesn't have it, it doesn't exist. Check first. |
| "Animations are nice-to-have" | Static UIs feel dead. Basic transitions are required. |

## Red Flags - Stop and Reconsider

If you catch yourself doing ANY of these, STOP:

- Using `bg-gray-*`, `text-gray-*`, or Hex codes (`#F3F4F6`)
- Importing libraries without checking `package.json`
- Creating "God Components" (>250 lines) without splitting
- Body text smaller than 16px (`text-sm` for paragraphs)
- Interactive elements without accessible names
- No loading or error state handling
- All buttons/cards look identical
- Can't explain what makes this design unique
- No semantic landmarks (`<nav>`, `<main>`, `<article>`)
- Skip link not implemented for keyboard users
- Assuming brand requirements instead of asking
- Using `console.error()` without user-visible feedback
- Missing `aria-expanded` on toggle buttons
- Using `onClick` on divs instead of buttons
- Images without alt attributes
- Using CSS properties you haven't verified exist
- No hover states or transitions on buttons/links

## Quick Reference

### Semantic Color Mapping

| Concept | Theme Variable | NOT This |
|---------|---------------|----------|
| Page background | `bg-background` | `bg-white`, `bg-gray-50` |
| Card background | `bg-card` | `bg-white`, `bg-gray-100` |
| Primary action | `bg-primary` | `bg-blue-600`, `bg-indigo-500` |
| Destructive | `bg-destructive` | `bg-red-500`, `bg-red-600` |
| Muted/secondary | `bg-muted` | `bg-gray-100`, `bg-slate-100` |
| Borders | `border-border` | `border-gray-200` |
| Main text | `text-foreground` | `text-gray-900`, `text-black` |
| Secondary text | `text-muted-foreground` | `text-gray-500`, `text-gray-600` |

### Text Size Guide

| Usage | Class | Size | Line Height |
|-------|-------|------|-------------|
| Hero headline | `text-4xl` to `text-6xl` | 36-60px | `leading-tight` |
| Section heading | `text-2xl` to `text-3xl` | 24-30px | `leading-snug` |
| Card title | `text-lg` to `text-xl` | 18-20px | `leading-normal` |
| Body text | `text-base` | 16px | `leading-relaxed` |
| Metadata only | `text-sm` | 14px | `leading-normal` |

### Essential ARIA Patterns

```tsx
// Expandable content
<button aria-expanded={open} aria-controls="content-id">
<div id="content-id" hidden={!open}>

// Form error
<input aria-invalid={!!error} aria-describedby="error-id" />
<p id="error-id" role="alert">{error}</p>

// Loading content
<div aria-busy={loading} aria-live="polite">

// Dynamic announcements
<div role="status" aria-live="polite">{message}</div>
```
