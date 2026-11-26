---
license: MIT
name: ui-design
description: Opinionated constraints for building better interfaces with agents. Use when building UI components, implementing animations, designing layouts, reviewing frontend accessibility, or working with Tailwind CSS, motion/react, or accessible primitives like Radix/Base UI.
---

# UI Design

Opinionated constraints for building better interfaces with agents.

## When to Use

- Building UI components with Tailwind CSS
- Implementing animations or transitions
- Adding interactive elements with keyboard/focus behavior
- Reviewing frontend code for accessibility
- Designing layouts with proper z-index and spacing
- Working with loading states, error handling, or empty states

## Stack

| Requirement | Rule |
|-------------|------|
| Tailwind CSS | MUST use defaults (spacing, radius, shadows) before custom values |
| Animation library | MUST use `motion/react` (formerly `framer-motion`) for JS animation |
| CSS animation | SHOULD use `tw-animate-css` for entrance and micro-animations |
| Class logic | MUST use `cn` utility (`clsx` + `tailwind-merge`) |

## Components

| Requirement | Rule |
|-------------|------|
| Interactive primitives | MUST use accessible primitives (`Base UI`, `React Aria`, `Radix`) for keyboard/focus behavior |
| Existing components | MUST use project's existing primitives first |
| Consistency | NEVER mix primitive systems within the same interaction surface |
| New primitives | SHOULD prefer [`Base UI`](https://base-ui.com/react/components) if compatible with stack |
| Icon buttons | MUST add `aria-label` to icon-only buttons |
| Custom behavior | NEVER rebuild keyboard or focus behavior by hand unless explicitly requested |

## Interaction

| Requirement | Rule |
|-------------|------|
| Destructive actions | MUST use `AlertDialog` for destructive or irreversible actions |
| Loading states | SHOULD use structural skeletons |
| Viewport height | NEVER use `h-screen`, use `h-dvh` |
| Fixed elements | MUST respect `safe-area-inset` |
| Error display | MUST show errors next to where the action happens |
| Input behavior | NEVER block paste in `input` or `textarea` elements |

## Animation

| Requirement | Rule |
|-------------|------|
| Default | NEVER add animation unless explicitly requested |
| Compositor props | MUST animate only `transform`, `opacity` |
| Layout props | NEVER animate `width`, `height`, `top`, `left`, `margin`, `padding` |
| Paint props | SHOULD avoid `background`, `color` except for small, local UI (text, icons) |
| Entrance easing | SHOULD use `ease-out` on entrance |
| Feedback timing | NEVER exceed `200ms` for interaction feedback |
| Looping | MUST pause looping animations when off-screen |
| Accessibility | MUST respect `prefers-reduced-motion` |
| Custom easing | NEVER introduce custom easing curves unless explicitly requested |
| Large surfaces | SHOULD avoid animating large images or full-screen surfaces |

## Typography

| Requirement | Rule |
|-------------|------|
| Headings | MUST use `text-balance` |
| Body text | MUST use `text-pretty` for paragraphs |
| Data | MUST use `tabular-nums` |
| Dense UI | SHOULD use `truncate` or `line-clamp` |
| Letter spacing | NEVER modify `letter-spacing` (`tracking-`) unless explicitly requested |

## Layout

| Requirement | Rule |
|-------------|------|
| Z-index | MUST use a fixed scale (no arbitrary `z-x`) |
| Square elements | SHOULD use `size-x` instead of `w-x` + `h-x` |

## Performance

| Requirement | Rule |
|-------------|------|
| Blur effects | NEVER animate large `blur()` or `backdrop-filter` surfaces |
| Will-change | NEVER apply `will-change` outside an active animation |
| useEffect | NEVER use for anything expressible as render logic |

## Design

| Requirement | Rule |
|-------------|------|
| Gradients | NEVER use unless explicitly requested |
| Purple/multicolor gradients | NEVER use |
| Glow effects | NEVER use as primary affordances |
| Shadows | SHOULD use Tailwind CSS default scale unless explicitly requested |
| Empty states | MUST give one clear next action |
| Accent colors | SHOULD limit to one per view |
| Color tokens | SHOULD use existing theme or Tailwind CSS tokens before introducing new ones |

## Common Pitfalls

The most common UI design failures occur in spacing, color contrast, mobile responsiveness, state management, and visual hierarchy. These gotchas are discovered through repeated agent mistakes when building interfaces.

### 1. Inconsistent Spacing (Arbitrary Margins, No System)

**Problem:** Using an inconsistent mix of Tailwind spacing values without a deliberate system makes layouts feel incoherent.

```tsx
// ❌ WRONG - arbitrary pixel values, no spacing system
<div className="ml-[13px] mr-[22px] pt-[7px]">Content</div>

// ✅ CORRECT - use system scales
<div className="ml-4 mr-4 pt-4">Content</div>
```

**Why it fails:** 
- Designs look accidental (some spacing is `2px`, some is `16px`, no pattern)
- Mobile layouts break (spacing doesn't scale proportionally)
- Alignment is impossible (gaps don't align to grid)

**Fix:**
- **ALWAYS use Tailwind spacing scale** (`0`, `1`, `2`, `3`, `4`, `6`, `8`, `12`, `16`, `24`, `32`, etc.)
- **Define spacing systems for common patterns:**
  - Button padding: `px-4 py-2`
  - Card padding: `p-6`
  - Gap between sections: `gap-8`
  - Nested spacing: `ml-6` (not `ml-3`)
- **Group related elements** with consistent gaps (use same `gap-x` for all horizontal lists)

### 2. Poor Color Contrast (Accessibility Violations)

**Problem:** Color combinations that fail WCAG AA contrast ratios (4.5:1 for text, 3:1 for UI components) making content illegible for low-vision users.

```tsx
// ❌ WRONG - gray-400 text on gray-100 background fails contrast
<p className="text-gray-400 bg-gray-100">Important content</p>

// ✅ CORRECT - gray-700 on gray-100 passes WCAG AA
<p className="text-gray-700 bg-gray-100">Important content</p>
```

**Why it fails:**
- Approximately 4-5% of users have color blindness, and a broader 15%+ have some form of visual impairment
- Users on bright displays (phones) can't read low-contrast text
- Legal liability (WCAG compliance required in many jurisdictions)

**Fix:**
- **Use color pairs with sufficient contrast:**
  - `text-gray-900`/`text-white` on any background (always safe)
  - `text-gray-700` on light backgrounds
  - `text-gray-300` on dark backgrounds
- **Test colors:** Use online contrast checkers (https://webaim.org/resources/contrastchecker/)
- **Avoid problematic pairs:**
  - `gray-400` on `gray-100` ❌
  - `red-500` on `pink-100` ❌
  - Disabled states: use `text-gray-400` on white, `text-gray-600` on color
- **For colored text (not gray):** Use darker tints (`red-700` not `red-300`)

### 3. Mobile-Unfriendly Layouts (Small Touch Targets, Horizontal Scroll)

**Problem:** Touch targets smaller than 44×44px, horizontal scrolling, or layouts that don't adapt to narrow viewports.

```tsx
// ❌ WRONG - button too small, no responsive layout
<button className="px-2 py-1 text-xs">Click me</button>
<div className="flex gap-2">
  <div className="w-80">Sidebar</div>
  <div className="w-80">Content</div>
</div>

// ✅ CORRECT - hit target size, responsive stack
<button className="px-4 py-3 md:px-6 md:py-3">Click me</button>
<div className="flex flex-col md:flex-row gap-4">
  <div className="w-full md:w-80">Sidebar</div>
  <div className="flex-1">Content</div>
</div>
```

**Why it fails:**
- 40% of traffic is mobile; small buttons are impossible to tap
- Horizontal scrolling is a UX nightmare on phones
- Layouts that work on desktop can be unusable on mobile

**Fix:**
- **Minimum touch target: 44×44px**
  - Buttons: at least `px-4 py-3` (standard: `px-6 py-3`)
  - Links: wrap in larger clickable area
- **Stack on mobile:** Use `flex-col` by default, `md:flex-row` for desktop
- **Use responsive widths:**
  - `w-full` on mobile, `md:w-80` or `md:w-1/3` on desktop
  - Use `flex-1` instead of fixed widths for flexible layouts
- **Test responsiveness:** Check at 375px (iPhone SE) and 768px (tablet) breakpoints
- **Avoid horizontal scroll:** Never force users to scroll sideways

### 4. Missing States (Loading, Error, Empty, Disabled)

**Problem:** Interfaces that only show the happy path, failing silently when loading, erroring, or empty.

```tsx
// ❌ WRONG - no feedback states
<button onClick={save}>Save</button>
<div>{data.map(item => <ItemCard item={item} />)}</div>

// ✅ CORRECT - all states accounted for
<button onClick={save} disabled={loading}>
  {loading ? 'Saving...' : 'Save'}
</button>

{loading && <LoadingSkeleton />}
{error && <ErrorAlert message={error} />}
{!loading && data.length === 0 && <EmptyState action="Create your first item" />}
{!loading && !error && data.map(item => <ItemCard item={item} />)}
```

**Why it fails:**
- Users don't know if action worked (no feedback = perceived failure)
- Empty lists look broken (not intentionally empty)
- No recovery path from errors

**Fix:**
- **Loading states:** Use structural skeletons (not spinners)
  - Layout remains stable while content loads
  - Users see what's coming, not just spinning
- **Error states:** Show next to the failed action
  - Explain what happened and how to fix it
  - Include retry button
- **Empty states:** Make intentional and actionable
  - "No items yet" → "Create your first item" (button)
  - Show what empty state means, how to populate
- **Disabled states:** Always provide visual feedback
  - `disabled={true}` + `opacity-50` or `cursor-not-allowed`
  - Never silently disable without explaining why

### 5. Unclear Hierarchy (Everything Looks Equally Important)

**Problem:** All text the same size, all colors the same weight, all spacing the same distance — nothing stands out.

```tsx
// ❌ WRONG - flat hierarchy
<div className="text-lg text-gray-700">
  <div className="text-lg text-gray-700">Subheading</div>
  <div className="text-lg text-gray-700">Subtitle</div>
  <button className="text-lg px-4 py-2">Action</button>
</div>

// ✅ CORRECT - clear hierarchy
<div>
  <h1 className="text-3xl font-bold text-gray-900">Title</h1>
  <h2 className="text-xl font-semibold text-gray-700 mt-6">Subheading</h2>
  <p className="text-base text-gray-600 mt-2">Subtitle</p>
  <button className="mt-6 px-6 py-3 bg-blue-600 text-white font-semibold rounded">
    Primary Action
  </button>
</div>
```

**Why it fails:**
- Users don't know where to look first
- Scanning pages is slower (no skimmable structure)
- Important actions get missed

**Fix:**
- **Size hierarchy:** 
  - Headings: `text-3xl` (h1) → `text-2xl` (h2) → `text-xl` (h3)
  - Body text: `text-base` (paragraphs) → `text-sm` (secondary)
- **Weight hierarchy:**
  - Primary actions: `font-bold` or `font-semibold`
  - Important text: `font-semibold`
  - Body: `font-normal`
  - Secondary: `font-normal` with lighter color
- **Color hierarchy:**
  - Primary text: `text-gray-900`
  - Secondary text: `text-gray-600`
  - Tertiary: `text-gray-500`
- **Spacing hierarchy:**
  - Section gaps: `gap-8` (largest)
  - Component gaps: `gap-4`
  - Dense content: `gap-2`
- **One accent color per view:** Use a single color for CTAs, not multiple colors fighting for attention

---

## Quick Reference

### Allowed Animation Properties
```
transform, opacity
```

### Forbidden Animation Properties
```
width, height, top, left, margin, padding, blur(), backdrop-filter
```

### Required Accessibility Patterns
```tsx
// Icon button - always add aria-label
<button aria-label="Close dialog">
  <XIcon />
</button>

// Respect reduced motion
@media (prefers-reduced-motion: reduce) {
  * { animation: none !important; }
}
```

### Class Utility Pattern
```tsx
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
```
