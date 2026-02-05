---
name: Design Guide
description: Ensures every UI component looks modern and professional. Enforces clean minimal design, neutral color palettes, consistent spacing (8px grid), clear typography hierarchy, and proper interactive states. No gradients, no clutter.
---

# Design Guide Skill

## Purpose

Provides strict design standards for building modern, professional UIs. Prevents common amateur mistakes like rainbow gradients, inconsistent spacing, and cluttered layouts.

**Philosophy**: Less is more. Clean, minimal, and functional beats flashy and complex.

## When to Use

Reference this skill whenever building ANY UI component:
- Buttons, forms, cards, modals, navigation
- Landing pages, dashboards, admin panels
- Mobile layouts, responsive designs
- Component libraries, design systems

## Core Design Principles

### 1. Clean and Minimal

**Rules**:
- Lots of white space (or off-white background)
- Not cluttered - remove unnecessary elements
- Every element should have a clear purpose
- Group related items, separate unrelated ones

✅ **Good**:
```css
/* Breathing room around content */
.container {
  padding: 48px 24px;
  max-width: 1200px;
  margin: 0 auto;
}

.card {
  padding: 32px;
  margin-bottom: 24px;
}
```

❌ **Bad**:
```css
/* Cramped, no breathing room */
.container {
  padding: 5px;
}

.card {
  padding: 10px;
  margin-bottom: 5px;
}
```

### 2. Neutral Color Palette

**Color System**:
- **Base**: Grays and off-whites (#F9FAFB, #F3F4F6, #E5E7EB, #9CA3AF, #374151, #1F2937)
- **ONE Accent Color**: Used sparingly for CTAs and important actions
  - Primary: Choose ONE (#3B82F6 blue, #10B981 green, #EF4444 red, #F59E0B amber)
- **Text**: Dark gray on light backgrounds (#1F2937, #374151, #6B7280)
- **NO generic purple/blue gradients**
- **NO rainbow colors**

✅ **Good Palette**:
```css
/* Neutral base with single accent */
--bg-primary: #FFFFFF;
--bg-secondary: #F9FAFB;
--text-primary: #1F2937;
--text-secondary: #6B7280;
--border: #E5E7EB;
--accent: #3B82F6;  /* ONE accent color */
```

❌ **Bad Palette**:
```css
/* Rainbow mess */
--primary: linear-gradient(purple, blue, pink);
--secondary: #FF6B9D;
--tertiary: #FFC371;
--accent: #00F260;
```

### 3. Consistent Spacing (8px Grid System)

**Spacing Scale**:
- `4px` - Tight spacing (icon + text)
- `8px` - Minimum spacing
- `16px` - Default spacing
- `24px` - Comfortable spacing
- `32px` - Section padding
- `48px` - Large gaps
- `64px` - Major section separation

**No random numbers**: Use 8, 16, 24, 32, 48, 64 - never 13px, 27px, 45px

✅ **Good Spacing**:
```css
.button {
  padding: 12px 24px;  /* Vertical: 12, Horizontal: 24 */
  margin-bottom: 16px;
}

.form-group {
  margin-bottom: 24px;
}

.section {
  padding: 64px 0;
}
```

❌ **Bad Spacing**:
```css
.button {
  padding: 7px 19px;  /* Random numbers */
  margin-bottom: 13px;
}

.form-group {
  margin-bottom: 22px;
}
```

### 4. Typography Hierarchy

**Font Rules**:
- **Maximum 2 fonts**: One for headings, one for body (or same for both)
- **Body text minimum**: 16px (never smaller)
- **Line height**: 1.5-1.6 for body, 1.2-1.3 for headings
- **Font weights**: Regular (400), Medium (500), Semibold (600), Bold (700)
- **System fonts are fine**: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto

**Type Scale**:
```css
/* Clear hierarchy */
--text-xs: 12px;    /* Labels, captions */
--text-sm: 14px;    /* Secondary text */
--text-base: 16px;  /* Body text (minimum) */
--text-lg: 18px;    /* Emphasized text */
--text-xl: 20px;    /* Small headings */
--text-2xl: 24px;   /* Section headings */
--text-3xl: 30px;   /* Page headings */
--text-4xl: 36px;   /* Hero headings */
```

✅ **Good Typography**:
```css
body {
  font-size: 16px;
  line-height: 1.6;
  color: #1F2937;
}

h1 {
  font-size: 36px;
  line-height: 1.2;
  font-weight: 700;
  margin-bottom: 24px;
}

.label {
  font-size: 14px;
  font-weight: 500;
  color: #6B7280;
}
```

❌ **Bad Typography**:
```css
body {
  font-size: 12px;  /* Too small! */
  line-height: 1.1;
}

h1 {
  font-size: 100px;  /* Way too big */
  font-family: 'Comic Sans';
}
```

### 5. Subtle Shadows

**Shadow Scale**:
```css
/* Use sparingly, not on everything */
--shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
--shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
--shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1);
--shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.1);
```

**Rules**:
- Cards: Use subtle shadow OR border, not both
- Buttons: Very subtle shadow on hover
- Modals: Medium shadow to lift from page
- No heavy drop shadows (0 20px 50px rgba(0,0,0,0.5))

✅ **Good Shadows**:
```css
.card {
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  border: none;
}

.button:hover {
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
```

❌ **Bad Shadows**:
```css
.card {
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);  /* Too heavy */
  border: 2px solid black;  /* AND a border */
}
```

### 6. Rounded Corners

**Border Radius Scale**:
```css
--rounded-sm: 4px;    /* Subtle */
--rounded: 8px;       /* Default */
--rounded-lg: 12px;   /* Cards */
--rounded-full: 9999px;  /* Pills, avatars */
```

**Rules**:
- Don't round EVERYTHING - mix sharp and rounded
- Buttons: 6-8px
- Cards: 8-12px
- Input fields: 6-8px
- Avatars/pills: fully rounded (9999px)

✅ **Good Rounding**:
```css
.button {
  border-radius: 8px;
}

.card {
  border-radius: 12px;
}

.input {
  border-radius: 6px;
}
```

❌ **Bad Rounding**:
```css
/* Everything is a circle */
.button, .card, .input, .container {
  border-radius: 50px;
}
```

### 7. Clear Interactive States

**Required States**:
- **Default**: Base appearance
- **Hover**: Subtle feedback (lighter/darker, shadow)
- **Active**: Pressed state
- **Disabled**: Reduced opacity, cursor not-allowed
- **Focus**: Clear outline for keyboard navigation

✅ **Good Interactive States**:
```css
.button {
  background: #3B82F6;
  transition: all 150ms ease;
}

.button:hover {
  background: #2563EB;  /* Slightly darker */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.button:active {
  background: #1D4ED8;  /* Even darker */
  transform: translateY(1px);
}

.button:disabled {
  background: #9CA3AF;
  cursor: not-allowed;
  opacity: 0.6;
}

.button:focus-visible {
  outline: 2px solid #3B82F6;
  outline-offset: 2px;
}
```

❌ **Bad Interactive States**:
```css
.button {
  background: blue;
}

/* No hover, active, or disabled states! */
```

### 8. Mobile-First Thinking

**Approach**:
1. Design for mobile first (320px+)
2. Progressively enhance for tablet (768px+)
3. Add desktop features (1024px+)

**Rules**:
- Touch targets: Minimum 44x44px
- Readable text without zooming
- Vertical layouts on mobile, horizontal on desktop
- Single column → multi-column
- Hidden navigation → visible navigation

✅ **Good Mobile-First**:
```css
/* Mobile first (default) */
.container {
  padding: 16px;
}

.grid {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

/* Tablet and up */
@media (min-width: 768px) {
  .container {
    padding: 32px;
  }

  .grid {
    flex-direction: row;
    gap: 24px;
  }
}
```

❌ **Bad Desktop-First**:
```css
/* Desktop only, breaks on mobile */
.container {
  width: 1200px;
  display: flex;
}
```

## Component Patterns

### Buttons

✅ **Good Button**:
```css
.button {
  /* Spacing */
  padding: 12px 24px;

  /* Typography */
  font-size: 16px;
  font-weight: 500;

  /* Colors */
  background: #3B82F6;
  color: white;
  border: none;

  /* Visual */
  border-radius: 8px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);

  /* Interaction */
  cursor: pointer;
  transition: all 150ms ease;
}

.button:hover {
  background: #2563EB;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
```

❌ **Bad Button**:
```css
.button {
  padding: 5px 10px;  /* Too small */
  font-size: 12px;  /* Unreadable */
  background: linear-gradient(45deg, purple, pink);  /* NO gradients */
  border-radius: 50px;  /* Too rounded */
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);  /* Too heavy */
}
```

### Cards

✅ **Good Card**:
```css
.card {
  /* Layout */
  padding: 32px;

  /* Visual - choose ONE: border OR shadow */
  background: white;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);

  /* Spacing */
  margin-bottom: 24px;
}
```

❌ **Bad Card**:
```css
.card {
  padding: 10px;  /* Too tight */
  background: linear-gradient(white, gray);  /* NO gradients */
  border: 3px solid black;  /* Heavy border */
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5);  /* AND heavy shadow */
  border-radius: 50px;  /* Too rounded */
}
```

### Forms

✅ **Good Form**:
```css
.form-group {
  margin-bottom: 24px;  /* Consistent spacing */
}

.label {
  display: block;
  font-size: 14px;
  font-weight: 500;
  color: #374151;
  margin-bottom: 8px;
}

.input {
  width: 100%;
  padding: 12px 16px;
  font-size: 16px;  /* Readable */
  color: #1F2937;
  background: white;
  border: 1px solid #E5E7EB;
  border-radius: 6px;
  transition: border-color 150ms ease;
}

.input:focus {
  outline: none;
  border-color: #3B82F6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.input.error {
  border-color: #EF4444;
}

.error-message {
  margin-top: 8px;
  font-size: 14px;
  color: #EF4444;
}
```

❌ **Bad Form**:
```css
.input {
  padding: 5px;  /* Too tight */
  font-size: 12px;  /* Too small */
  border: 3px solid rainbow;  /* What? */
  border-radius: 0;  /* Too sharp */
}

/* No error states, no focus states */
```

## Design Checklist

Before shipping any UI component, verify:

- [ ] **Spacing**: Using 8px grid system? (8, 16, 24, 32, 48, 64)
- [ ] **Colors**: Neutral base + ONE accent color? No gradients?
- [ ] **Typography**: 16px minimum body text? Clear hierarchy?
- [ ] **Shadows**: Subtle and purposeful? Not heavy?
- [ ] **Borders**: Rounded appropriately? Not everything rounded?
- [ ] **Interactive States**: Hover, active, disabled, focus defined?
- [ ] **Mobile**: Works on 320px+ screens? Touch targets 44px+?
- [ ] **White Space**: Breathing room? Not cluttered?
- [ ] **Consistency**: Matches existing components?

## Quick Reference

### Spacing Scale
```
4px, 8px, 16px, 24px, 32px, 48px, 64px
```

### Color Variables
```css
--bg-primary: #FFFFFF;
--bg-secondary: #F9FAFB;
--bg-tertiary: #F3F4F6;
--text-primary: #1F2937;
--text-secondary: #6B7280;
--border: #E5E7EB;
--accent: #3B82F6;  /* Choose one */
```

### Typography Scale
```css
--text-sm: 14px;
--text-base: 16px;
--text-lg: 18px;
--text-xl: 20px;
--text-2xl: 24px;
--text-3xl: 30px;
```

### Shadow Scale
```css
--shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
--shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
--shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1);
```

### Border Radius
```css
--rounded-sm: 4px;
--rounded: 8px;
--rounded-lg: 12px;
--rounded-full: 9999px;
```

## Common Mistakes to Avoid

❌ **Gradients everywhere** - Use solid colors
❌ **Tiny text** - 16px minimum for body
❌ **Inconsistent spacing** - Stick to 8px grid
❌ **Rainbow colors** - Neutral + ONE accent
❌ **Heavy shadows** - Keep them subtle
❌ **No hover states** - Always define interactions
❌ **Cluttered layouts** - Add white space
❌ **Desktop-only** - Design mobile-first

## Integration with Other Skills

- **Before building**: Check Idea Validator for market validation
- **Before implementing**: Use Confidence Check for technical validation
- **While building**: Reference Design Guide for UI standards
- **After building**: Test on mobile (320px) and desktop (1920px)

## Examples

### Modern Button Group
```html
<div class="button-group">
  <button class="button button-primary">Primary Action</button>
  <button class="button button-secondary">Secondary</button>
  <button class="button button-ghost">Cancel</button>
</div>
```

```css
.button-group {
  display: flex;
  gap: 12px;  /* 8px grid system */
}

.button {
  padding: 12px 24px;
  font-size: 16px;
  font-weight: 500;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  transition: all 150ms ease;
}

.button-primary {
  background: #3B82F6;  /* Accent color */
  color: white;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.button-primary:hover {
  background: #2563EB;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.button-secondary {
  background: #F3F4F6;  /* Neutral */
  color: #374151;
}

.button-secondary:hover {
  background: #E5E7EB;
}

.button-ghost {
  background: transparent;
  color: #6B7280;
}

.button-ghost:hover {
  background: #F9FAFB;
}
```

### Clean Card Layout
```html
<div class="card">
  <h3 class="card-title">Card Title</h3>
  <p class="card-description">
    Clean description with good typography and spacing.
  </p>
  <button class="button-primary">Action</button>
</div>
```

```css
.card {
  background: white;
  border-radius: 12px;
  padding: 32px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.card-title {
  font-size: 24px;
  font-weight: 600;
  color: #1F2937;
  margin-bottom: 12px;
}

.card-description {
  font-size: 16px;
  line-height: 1.6;
  color: #6B7280;
  margin-bottom: 24px;
}
```

## Tailwind CSS Equivalent

If using Tailwind, these principles map to:

```html
<!-- Button -->
<button class="px-6 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition">
  Button
</button>

<!-- Card -->
<div class="bg-white rounded-xl p-8 shadow-sm">
  <h3 class="text-2xl font-semibold text-gray-900 mb-3">Title</h3>
  <p class="text-base text-gray-600 mb-6">Description</p>
  <button class="px-6 py-3 bg-blue-500 text-white rounded-lg">Action</button>
</div>

<!-- Form -->
<div class="mb-6">
  <label class="block text-sm font-medium text-gray-700 mb-2">Label</label>
  <input
    class="w-full px-4 py-3 text-base border border-gray-300 rounded-lg focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
    type="text"
  />
</div>
```

Tailwind spacing: `p-2` = 8px, `p-4` = 16px, `p-6` = 24px, `p-8` = 32px
