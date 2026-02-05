---
name: Design System Compliance
description: Ensure all UI components follow the design guidelines including purple-indigo gradient, rounded-xl borders, backdrop-blur-sm effects, dark mode support, and accessibility requirements
---

# Design System Compliance

This skill ensures all UI components follow the My Prompt Manager design guidelines for visual consistency, accessibility, and brand identity.

## When to Use This Skill

Invoke this skill when:
- Creating new UI components
- Modifying existing components
- Adding buttons, forms, cards, or modals
- Implementing hover, focus, or active states
- Working on light/dark mode styling
- User asks for "design consistency", "styling", or "UI updates"

## Critical Requirements

From `docs/DESIGN_GUIDELINES.md`:

> **CRITICAL**: When creating or modifying UI components, you MUST follow the design guidelines in `docs/DESIGN_GUIDELINES.md`.

**Non-Negotiables:**
1. **Purple-indigo gradient** for all primary actions
2. **rounded-xl (12px)** for cards, inputs, buttons
3. **Dark mode support** - EVERY style needs `dark:` variant
4. **Backdrop-blur** with semi-transparent backgrounds
5. **Predefined focus classes** - Never create custom focus styles
6. **Accessibility** - ARIA labels, keyboard navigation, color contrast

## Design System Overview

### Brand Identity

**Primary Colors:**
```css
/* Purple-Indigo Gradient (Brand) */
bg-linear-to-r from-purple-600 to-indigo-600

/* Hover state */
hover:from-purple-700 hover:to-indigo-700
```

**Status Colors:**
```css
bg-green-500   /* Success */
bg-red-500     /* Error */
bg-yellow-500  /* Warning */
bg-blue-500    /* Info */
```

**Gray Scale:**
```css
/* Light Mode */
bg-white       /* #ffffff */
bg-gray-50     /* #f9fafb - Backgrounds */
bg-gray-100    /* #f3f4f6 - Section backgrounds */
text-gray-900  /* #111827 - Primary text */
text-gray-600  /* #4b5563 - Secondary text */

/* Dark Mode */
dark:bg-gray-900  /* #111827 - Darkest background */
dark:bg-gray-800  /* #1f2937 - Container background */
dark:bg-gray-700  /* #374151 - Card background */
dark:text-gray-100 /* #f3f4f6 - Primary text */
dark:text-gray-400 /* #9ca3af - Secondary text */
```

### Typography System

**Font Sizes:**
```css
text-xs    /* 12px - Helper text, character counts */
text-sm    /* 14px - Body text, form labels, buttons */
text-base  /* 16px - Default body text */
text-xl    /* 20px - Section headers */
text-2xl   /* 24px - Page titles (rare) */
```

**Font Weights:**
```css
font-medium   /* 500 - Secondary headings */
font-semibold /* 600 - Primary headings, buttons */
font-bold     /* 700 - Major section titles */
```

**Common Patterns:**
```tsx
{/* Page Title */}
<h1 className="text-xl font-bold text-gray-900 dark:text-gray-100">
  Add New Prompt
</h1>

{/* Section Header */}
<h2 className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-3">
  Category
</h2>

{/* Body Text */}
<p className="text-sm text-gray-600 dark:text-gray-400">
  Description text
</p>

{/* Helper Text */}
<p className="text-xs text-gray-500 dark:text-gray-400 font-medium">
  100/10000 characters
</p>
```

### Spacing & Layout

**Standard Spacing:**
```css
p-3   /* 12px - Compact components */
p-4   /* 16px - Standard padding */
p-5   /* 20px - Form sections, cards */
p-6   /* 24px - Page containers, headers */
```

**Common Gaps:**
```css
space-x-2  /* 8px - Button groups */
space-x-3  /* 12px - Header elements */
gap-3      /* 12px - Form field gaps */
```

### Border Radius

**Standard Values:**
```css
rounded-md   /* 6px - Small elements */
rounded-lg   /* 8px - Icon buttons */
rounded-xl   /* 12px - Cards, inputs, buttons, modals */
rounded-full /* Pills, badges, toggle knobs */
```

**CRITICAL:** Use `rounded-xl` (12px) for:
- All primary buttons
- All input fields
- All cards and containers
- All modals and dialogs

### Effects & Shadows

**Glassmorphism (Signature Effect):**
```css
bg-white/70 dark:bg-gray-800/70 backdrop-blur-sm
```

**Shadow Scale:**
```css
shadow-xs  /* Subtle elevation */
shadow-lg  /* Primary buttons, elevated cards */
shadow-xl  /* Modals, dialogs */
```

**Transitions:**
```css
transition-all duration-200  /* Default for all interactive elements */
```

## Component Patterns

### 1. Primary Button

**Pattern:**
```tsx
<button className="
  px-6 py-3
  text-sm font-semibold text-white
  bg-linear-to-r from-purple-600 to-indigo-600
  rounded-xl
  hover:from-purple-700 hover:to-indigo-700
  transition-all duration-200
  shadow-lg hover:shadow-xl
  disabled:opacity-50
  focus-primary
">
  Save Prompt
</button>
```

**Key Elements:**
- Purple-indigo gradient background
- White text
- rounded-xl (12px radius)
- Gradient hover state
- Shadow elevation
- Predefined focus class

**Focus Class (Predefined in Tailwind config):**
```css
.focus-primary {
  @apply focus:outline-hidden focus:ring-2 focus:ring-purple-500
         focus:ring-offset-2 focus:ring-offset-white
         dark:focus:ring-offset-gray-900;
}
```

### 2. Secondary Button

**Pattern:**
```tsx
<button className="
  px-6 py-3
  text-sm font-semibold
  text-gray-700 dark:text-gray-300
  bg-white/60 dark:bg-gray-700/60 backdrop-blur-sm
  border border-purple-200 dark:border-gray-600
  rounded-xl
  hover:bg-white/80 dark:hover:bg-gray-700/80
  transition-all duration-200
  focus-secondary
">
  Cancel
</button>
```

**Key Elements:**
- Glassmorphism effect (semi-transparent + backdrop-blur)
- Border with purple tint
- Dark mode support
- No shadow (subtle appearance)

### 3. Input Fields

**Text Input:**
```tsx
<input
  type="text"
  className="
    w-full px-4 py-3
    border border-purple-200 dark:border-gray-600
    rounded-xl
    focus-input
    bg-white/60 dark:bg-gray-700/60 backdrop-blur-sm
    transition-all duration-200
    text-gray-900 dark:text-gray-100
    placeholder-gray-500 dark:placeholder-gray-400
  "
  placeholder="Enter text..."
/>
```

**Textarea:**
```tsx
<textarea
  rows={8}
  className="
    w-full px-4 py-3
    border border-purple-200 dark:border-gray-600
    rounded-xl
    focus-input
    resize-none
    bg-white/60 dark:bg-gray-700/60 backdrop-blur-sm
    transition-all duration-200
    text-gray-900 dark:text-gray-100
  "
  placeholder="Enter your prompt content..."
/>
```

**Input with Error:**
```tsx
<input
  className="
    w-full px-4 py-3
    border rounded-xl focus-input
    bg-white/60 dark:bg-gray-700/60 backdrop-blur-sm
    transition-all duration-200
    text-gray-900 dark:text-gray-100
    border-red-300 dark:border-red-500
  "
/>
{errors.field && (
  <p className="mt-2 text-sm text-red-600 dark:text-red-400 font-medium">
    {errors.field}
  </p>
)}
```

**Focus Class:**
```css
.focus-input {
  @apply focus:outline-hidden focus:ring-2 focus:ring-purple-500
         focus:border-purple-500 dark:focus:ring-purple-400
         dark:focus:border-purple-400;
}
```

### 4. Cards

**Prompt Card:**
```tsx
<article className="
  bg-white/70 dark:bg-gray-800/70 backdrop-blur-sm
  border-b border-purple-100 dark:border-gray-700
  p-5
  hover:bg-white/90 dark:hover:bg-gray-800/90
  transition-all duration-200
  relative group
">
  <h3 className="font-semibold text-gray-900 dark:text-gray-100 text-sm">
    Prompt Title
  </h3>
  <p className="text-sm text-gray-600 dark:text-gray-400 mt-2">
    Prompt content preview...
  </p>
</article>
```

**Settings Card:**
```tsx
<div className="
  bg-white/70 dark:bg-gray-800/70 backdrop-blur-sm
  border border-purple-100 dark:border-gray-700
  rounded-xl
  p-5
  hover:shadow-md
  transition-all duration-200
">
  {/* Card content */}
</div>
```

**Key Elements:**
- Glassmorphism background
- rounded-xl for standalone cards
- border-b for list items
- Hover state for interaction feedback

### 5. Modals & Dialogs

**Modal Container:**
```tsx
<div className="
  fixed inset-0 z-50
  flex items-center justify-center p-3
">
  {/* Backdrop */}
  <div
    className="
      absolute inset-0
      bg-black bg-opacity-50
      transition-opacity
    "
    onClick={onClose}
  />

  {/* Modal Panel */}
  <div className="
    relative
    bg-white dark:bg-gray-800
    rounded-xl p-3
    shadow-xl
    transform transition-all
    max-w-xs w-full mx-2
    backdrop-blur-sm
    border border-purple-100 dark:border-gray-700
  ">
    {/* Modal content */}
  </div>
</div>
```

**Confirm Dialog:**
```tsx
<div className="p-5">
  <div className="flex items-start">
    {/* Icon */}
    <div className="
      shrink-0 flex items-center justify-center
      h-8 w-8
      rounded-full
      bg-red-100 dark:bg-red-900/20
    ">
      <svg className="w-6 h-6 text-red-600">{/* Icon */}</svg>
    </div>

    {/* Content */}
    <div className="ml-3 flex-1">
      <h3 className="text-sm leading-5 font-bold text-gray-900 dark:text-gray-100">
        Delete Prompt
      </h3>
      <p className="mt-1 text-xs text-gray-600 dark:text-gray-400 leading-tight">
        Are you sure? This action cannot be undone.
      </p>
    </div>
  </div>

  {/* Actions */}
  <div className="mt-3 flex flex-row-reverse gap-2">
    <button className="
      px-3 py-1.5
      text-xs font-semibold text-white
      bg-red-600 hover:bg-red-700
      rounded-lg shadow-xs
      transition-colors
      focus-danger
    ">
      Delete
    </button>
    <button className="
      px-3 py-1.5
      text-xs font-semibold
      text-gray-700 dark:text-gray-300
      bg-white dark:bg-gray-700
      border border-gray-300 dark:border-gray-600
      rounded-lg
      hover:bg-gray-50 dark:hover:bg-gray-600
      transition-colors
      focus-secondary
    ">
      Cancel
    </button>
  </div>
</div>
```

### 6. Search Input

**Pattern:**
```tsx
<div className="relative">
  <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none z-10">
    <svg className="h-5 w-5 text-purple-400 dark:text-purple-300">
      {/* Search icon */}
    </svg>
  </div>
  <input
    type="text"
    className="
      w-full pl-12 pr-12 py-3
      bg-white/60 dark:bg-gray-700/60 backdrop-blur-sm
      border border-purple-200 dark:border-gray-600
      rounded-xl
      focus-input
      text-sm
      text-gray-900 dark:text-gray-100
      placeholder-gray-500 dark:placeholder-gray-400
      shadow-xs
      hover:bg-white/80 dark:hover:bg-gray-700/80
      transition-all duration-200
    "
    placeholder="Search prompts"
  />
</div>
```

### 7. Toggle Switch

**Pattern:**
```tsx
<button
  type="button"
  role="switch"
  aria-checked={checked}
  onClick={() => onChange(!checked)}
  className={`
    w-11 h-6
    relative inline-flex items-center
    rounded-full
    transition-all duration-200
    focus:outline-hidden focus:ring-4 focus:ring-purple-300 dark:focus:ring-purple-800
    ${checked
      ? 'bg-linear-to-r from-purple-600 to-indigo-600 shadow-xs'
      : 'bg-gray-200 dark:bg-gray-700'
    }
    ${disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}
  `}
>
  <span className={`
    h-5 w-5
    inline-block transform
    rounded-full bg-white shadow-xs
    transition-transform duration-200
    border border-gray-300 dark:border-gray-600
    ${checked ? 'translate-x-6' : 'translate-x-[2px]'}
  `} />
</button>
```

### 8. Icon Button

**Pattern:**
```tsx
<button className="
  p-2
  text-gray-400 dark:text-gray-500
  hover:text-purple-600 dark:hover:text-purple-400
  rounded-lg
  hover:bg-purple-50 dark:hover:bg-purple-900/20
  transition-colors
  focus-interactive
">
  <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="..." />
  </svg>
</button>
```

**Focus Class:**
```css
.focus-interactive {
  @apply focus:outline-hidden focus:ring-2 focus:ring-purple-500
         focus:ring-offset-1 focus:ring-offset-white
         dark:focus:ring-offset-gray-800 dark:focus:ring-purple-400;
}
```

## Dark Mode Implementation

### Strategy

**Class-based dark mode with Tailwind CSS:**
```javascript
// tailwind.config.js
darkMode: 'class'
```

The `.dark` class is applied to the root element when dark mode is active.

### Dark Mode Patterns

**Every style MUST have a dark mode variant:**

```tsx
{/* ✅ CORRECT - Dark mode variant included */}
<div className="
  bg-white dark:bg-gray-900
  text-gray-900 dark:text-gray-100
  border-purple-200 dark:border-gray-600
">

{/* ❌ WRONG - Missing dark mode variants */}
<div className="
  bg-white
  text-gray-900
  border-purple-200
">
```

**Common Dark Mode Combinations:**

```css
/* Backgrounds */
bg-white dark:bg-gray-900              /* Page background */
bg-gray-50 dark:bg-gray-800            /* Section background */
bg-white/70 dark:bg-gray-800/70        /* Card with opacity */

/* Text */
text-gray-900 dark:text-gray-100       /* Primary text */
text-gray-700 dark:text-gray-300       /* Secondary text */
text-gray-500 dark:text-gray-400       /* Tertiary text */

/* Borders */
border-purple-200 dark:border-gray-600 /* Input borders */
border-purple-100 dark:border-gray-700 /* Dividers */

/* Hover States */
hover:bg-purple-50 dark:hover:bg-purple-900/20
hover:text-purple-600 dark:hover:text-purple-400

/* Focus States */
focus:ring-purple-500 dark:focus:ring-purple-400
focus:ring-offset-white dark:focus:ring-offset-gray-900
```

### Testing Dark Mode

**Manual checklist:**
- [ ] Component renders correctly in light mode
- [ ] Component renders correctly in dark mode
- [ ] All text is readable (sufficient contrast)
- [ ] Borders are visible
- [ ] Hover states work in both modes
- [ ] Focus states work in both modes
- [ ] Icons are visible in both modes
- [ ] Backdrop-blur renders properly

**Color Contrast Requirements (WCAG AA):**
- Normal text: 4.5:1 contrast ratio
- Large text (18px+): 3:1 contrast ratio
- Interactive elements: 3:1 contrast ratio

## Predefined Focus Classes

**NEVER create custom focus styles.** Always use these predefined classes:

### .focus-primary
For primary action buttons:
```css
.focus-primary {
  @apply focus:outline-hidden focus:ring-2 focus:ring-purple-500
         focus:ring-offset-2 focus:ring-offset-white
         dark:focus:ring-offset-gray-900;
}
```

### .focus-secondary
For secondary buttons and menu items:
```css
.focus-secondary {
  @apply focus:outline-hidden focus:ring-2 focus:ring-purple-500
         focus:ring-offset-1 focus:ring-offset-white
         dark:focus:ring-offset-gray-800;
}
```

### .focus-danger
For delete/danger buttons:
```css
.focus-danger {
  @apply focus:outline-hidden focus:ring-2 focus:ring-red-500
         focus:ring-offset-2 focus:ring-offset-white
         dark:focus:ring-offset-gray-900;
}
```

### .focus-input
For input fields:
```css
.focus-input {
  @apply focus:outline-hidden focus:ring-2 focus:ring-purple-500
         focus:border-purple-500 dark:focus:ring-purple-400
         dark:focus:border-purple-400;
}
```

### .focus-interactive
For icon buttons and interactive elements:
```css
.focus-interactive {
  @apply focus:outline-hidden focus:ring-2 focus:ring-purple-500
         focus:ring-offset-1 focus:ring-offset-white
         dark:focus:ring-offset-gray-800 dark:focus:ring-purple-400;
}
```

## Accessibility Requirements

### ARIA Labels

**All interactive elements MUST have appropriate ARIA labels:**

```tsx
{/* Icon button with aria-label */}
<button aria-label="Copy prompt to clipboard">
  <svg aria-hidden="true">{/* Icon */}</svg>
</button>

{/* Search input with role */}
<input
  type="text"
  aria-label="Search prompts"
  role="searchbox"
/>

{/* Card with aria-labelledby */}
<article aria-labelledby="prompt-title-123">
  <h3 id="prompt-title-123">Prompt Title</h3>
</article>

{/* Toggle with role and aria-checked */}
<button
  role="switch"
  aria-checked={isEnabled}
  aria-label="Enable dark mode"
>
```

### Keyboard Navigation

**All interactive elements must be keyboard accessible:**

- **Tab:** Navigate between elements
- **Enter/Space:** Activate buttons
- **Escape:** Close modals/dropdowns
- **Arrow keys:** Navigate lists/menus

**Example:**
```tsx
<button
  onClick={handleClick}
  onKeyDown={(e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      handleClick();
    }
  }}
>
```

### Focus Management

**Visible focus indicators are mandatory:**
```tsx
{/* ✅ CORRECT - Uses predefined focus class */}
<button className="focus-primary">Save</button>

{/* ❌ WRONG - No focus state */}
<button className="outline-hidden">Save</button>
```

## Common Mistakes & Fixes

### Mistake 1: Missing Dark Mode

**Problem:**
```tsx
<div className="bg-white text-gray-900 border-gray-200">
```

**Fix:**
```tsx
<div className="bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100 border-gray-200 dark:border-gray-700">
```

### Mistake 2: Wrong Border Radius

**Problem:**
```tsx
<button className="rounded-lg">  {/* Should be rounded-xl */}
```

**Fix:**
```tsx
<button className="rounded-xl">  {/* 12px for buttons */}
```

### Mistake 3: Missing Gradient on Primary Button

**Problem:**
```tsx
<button className="bg-purple-600">Save</button>
```

**Fix:**
```tsx
<button className="bg-linear-to-r from-purple-600 to-indigo-600">Save</button>
```

### Mistake 4: Custom Focus Styles

**Problem:**
```tsx
<button className="focus:outline-hidden focus:ring-2 focus:ring-blue-500">
```

**Fix:**
```tsx
<button className="focus-primary">
```

### Mistake 5: No Backdrop Blur

**Problem:**
```tsx
<div className="bg-white/70">  {/* Missing backdrop-blur-sm */}
```

**Fix:**
```tsx
<div className="bg-white/70 backdrop-blur-sm">
```

### Mistake 6: Wrong Transition Duration

**Problem:**
```tsx
<button className="transition-all duration-300">  {/* Should be 200 */}
```

**Fix:**
```tsx
<button className="transition-all duration-200">
```

### Mistake 7: Missing ARIA Label

**Problem:**
```tsx
<button>
  <svg>{/* Icon */}</svg>
</button>
```

**Fix:**
```tsx
<button aria-label="Copy to clipboard">
  <svg aria-hidden="true">{/* Icon */}</svg>
</button>
```

## Component Creation Checklist

When creating a new component, verify:

- [ ] Uses purple-indigo gradient for primary actions
- [ ] All borders use rounded-xl (12px)
- [ ] Includes dark mode variants for ALL styles
- [ ] Uses backdrop-blur-sm with semi-transparent backgrounds
- [ ] Uses predefined focus classes (.focus-primary, .focus-input, etc.)
- [ ] All interactive elements have ARIA labels
- [ ] Keyboard navigation works (Tab, Enter, Escape)
- [ ] Hover states defined for interactive elements
- [ ] Uses transition-all duration-200 for animations
- [ ] Text follows typography scale (text-sm, text-xs, etc.)
- [ ] Spacing follows scale (p-5 for cards, p-6 for containers)
- [ ] Color contrast meets WCAG AA standards
- [ ] Component tested in both light and dark mode
- [ ] No console.* statements (use Logger instead)
- [ ] No arbitrary values (e.g., w-[237px])

## Quick Reference

### Color Palette

```css
/* Brand */
from-purple-600 to-indigo-600   /* Primary gradient */
bg-purple-500                   /* Accent */

/* Status */
bg-green-500   /* Success */
bg-red-500     /* Error */
bg-yellow-500  /* Warning */
bg-blue-500    /* Info */

/* Neutrals (Light) */
bg-white, bg-gray-50, bg-gray-100
text-gray-900, text-gray-700, text-gray-500

/* Neutrals (Dark) */
dark:bg-gray-900, dark:bg-gray-800, dark:bg-gray-700
dark:text-gray-100, dark:text-gray-300, dark:text-gray-400
```

### Common Class Combinations

**Primary Button:**
```
px-6 py-3 text-sm font-semibold text-white
bg-linear-to-r from-purple-600 to-indigo-600
rounded-xl hover:from-purple-700 hover:to-indigo-700
transition-all duration-200 shadow-lg hover:shadow-xl
disabled:opacity-50 focus-primary
```

**Text Input:**
```
w-full px-4 py-3
border border-purple-200 dark:border-gray-600
rounded-xl focus-input
bg-white/60 dark:bg-gray-700/60 backdrop-blur-sm
transition-all duration-200
text-gray-900 dark:text-gray-100
```

**Card:**
```
bg-white/70 dark:bg-gray-800/70 backdrop-blur-sm
border-b border-purple-100 dark:border-gray-700
p-5 hover:bg-white/90 dark:hover:bg-gray-800/90
transition-all duration-200
```

## Related Documentation

- **Complete Design Guidelines:** `docs/DESIGN_GUIDELINES.md` (comprehensive reference)
- **Component Catalog:** `docs/COMPONENTS.md` (40+ component examples)
- **React 19 Patterns:** `docs/REACT_19_MIGRATION.md` (form handling, optimistic updates)

## Validation Workflow

**Before marking component complete:**

1. **Visual Inspection:**
   - Check in browser (light mode)
   - Check in browser (dark mode)
   - Verify gradient on primary buttons
   - Confirm rounded-xl borders

2. **Accessibility Check:**
   - Tab through all interactive elements
   - Verify focus indicators are visible
   - Check ARIA labels in DevTools
   - Test keyboard shortcuts (Enter, Escape)

3. **Code Review:**
   - All styles have dark mode variants
   - Uses predefined focus classes
   - No console.* statements
   - Follows spacing/typography scale

4. **Testing:**
   - Run `npm test`
   - Run `npm run lint`
   - Both must pass

---

**Last Updated:** 2025-10-18
**Skill Version:** 1.0.0
