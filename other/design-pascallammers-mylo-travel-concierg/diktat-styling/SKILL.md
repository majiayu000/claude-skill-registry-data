---
name: diktat-styling
description: Apply Diktat.ai design system guidelines when creating or reviewing Vue/Nuxt components. Use this skill when implementing new UI components, reviewing existing components for design consistency, or answering questions about styling patterns. Includes glass-morphism aesthetics, brand colors (indigo-purple gradient), Tailwind CSS patterns, and component templates.
---

# Diktat.ai Design System Skill

## Overview

This skill ensures consistent application of Diktat.ai's design system across all Vue/Nuxt components. Use it when creating new components, reviewing existing code for design consistency, or implementing styling changes. The design system emphasizes glass-morphism aesthetics with semi-transparent backgrounds, the signature indigo-to-purple brand gradient, and modern interactive patterns.

## When to Use This Skill

Activate this skill when:

- Creating new Vue/Nuxt UI components (buttons, cards, modals, forms, etc.)
- Reviewing existing components for design system compliance
- Refactoring components to match brand guidelines
- Implementing interactive elements (hover states, transitions, animations)
- Adding status indicators, badges, or premium features
- Questions about styling patterns or Tailwind CSS classes to use
- Ensuring accessibility and responsive design adherence

## Core Design Principles

### Glass-morphism Foundation

All components should follow the glass-morphism pattern:

1. **Semi-transparent backgrounds**: `bg-white/70`, `bg-white/80`, `bg-white/90`
2. **Backdrop blur effects**: `backdrop-blur-sm`, `backdrop-blur-md`, `backdrop-blur-xl`
3. **Semi-transparent borders**: `border border-indigo-200/50`
4. **Layered shadows**: `shadow-lg`, `shadow-xl`, `shadow-2xl`

### Brand Identity

**Primary Brand Colors:**
- Indigo: `indigo-500`, `indigo-600`, `indigo-700`
- Purple: `purple-600`, `purple-700`
- Signature gradient: `bg-gradient-to-r from-indigo-500 to-purple-600`

**Usage Rules:**
- Primary actions: Always use indigo-purple gradient
- Semantic colors: Green (success), Red (error), Amber (warning), Blue (info)
- Opacity variations: `/50`, `/60`, `/70` for layering

## Component Implementation Workflow

### Step 1: Identify Component Type

Determine which component pattern applies:

- **Card/Container**: Use glass-morphism card pattern
- **Button**: Choose primary, secondary, or action button style
- **Badge/Status**: Apply semantic color system
- **Interactive Element**: Include hover states and transitions
- **Icon Container**: Use gradient background with proper sizing

### Step 2: Apply Base Styling

Start with the appropriate base classes from the design system:

**Cards:**
```vue
<div class="bg-white/70 backdrop-blur-sm border border-indigo-200/50 rounded-2xl p-6 shadow-lg">
  <!-- content -->
</div>
```

**Primary Buttons:**
```vue
<button class="px-6 py-3 bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700 text-white font-medium rounded-xl shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200">
  Button Text
</button>
```

**Status Badges:**
```vue
<span class="inline-flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-medium bg-green-100 text-green-800 border border-green-300">
  <CheckIcon class="h-4 w-4" />
  Completed
</span>
```

### Step 3: Add Interactive States

Ensure all interactive elements include:

1. **Hover effects**: Color changes, shadow progression, scale effects
2. **Transitions**: `transition-all duration-200` for smooth animations
3. **Focus states**: For accessibility (keyboard navigation)
4. **Active states**: Visual feedback on click/press

Example:
```vue
<div class="hover:bg-white/80 hover:shadow-xl transition-all duration-200 cursor-pointer">
```

### Step 4: Ensure Responsive Design

Apply mobile-first responsive patterns:

- Use `md:` prefix for desktop-specific styles
- Test on mobile viewports first
- Apply appropriate spacing for different screen sizes

Example:
```vue
<div class="flex flex-col md:flex-row gap-4 md:gap-6">
```

### Step 5: Validate Accessibility

Check for:

- Sufficient color contrast (especially with semi-transparent backgrounds)
- Keyboard navigation support
- Screen reader compatibility
- Focus indicators

## Quick Reference Patterns

### Typography Hierarchy

```css
text-gray-800  /* Primary text */
text-gray-700  /* Secondary text */
text-gray-600  /* Tertiary text */
text-gray-500  /* Subtle text */

font-bold      /* Headings */
font-semibold  /* Sub-headings */
font-medium    /* Body text, buttons */
```

### Spacing System

```css
space-y-4      /* Normal vertical spacing */
space-y-6      /* Section spacing */
gap-4, gap-6   /* Flexbox/grid gaps */

p-6            /* Standard card padding */
p-4            /* Smaller card padding */
px-6 py-3      /* Large button padding */
px-4 py-2      /* Normal button padding */
```

### Border & Shadow Progression

```css
rounded-xl     /* Standard rounded corners */
rounded-2xl    /* Main cards */

shadow-lg → hover:shadow-xl → hover:shadow-2xl
```

## Component Review Checklist

When reviewing or creating components, verify:

- [ ] Uses glass-morphism pattern (semi-transparent bg + backdrop blur + border)
- [ ] Primary actions use indigo-purple gradient
- [ ] Includes hover states with proper transitions
- [ ] Has responsive design patterns (mobile-first)
- [ ] Follows spacing system (consistent padding/margins)
- [ ] Typography hierarchy is correct
- [ ] Semantic colors used appropriately
- [ ] Has proper accessibility attributes
- [ ] Shadows and borders follow design system
- [ ] Interactive elements have scale/transition effects

## Common Patterns

### Premium/Pro Features

```vue
<!-- PRO Badge with glow effect -->
<div class="relative inline-block">
  <div class="absolute -inset-1 bg-gradient-to-r from-amber-400 via-orange-500 to-red-500 rounded-full blur opacity-30 animate-pulse"></div>
  <span class="relative bg-gradient-to-r from-amber-400 via-orange-500 to-red-500 text-white text-xs font-bold px-3 py-1 rounded-full transform rotate-12 hover:rotate-6 transition-transform">
    PRO
  </span>
</div>
```

### Icon Containers

```vue
<div class="w-10 h-10 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-lg flex items-center justify-center group-hover:scale-110 transition-transform duration-200">
  <svg class="h-5 w-5 text-white" />
</div>
```

### Loading States

Use shimmer or pulse animations for loading indicators. Reference custom animations in `references/styling-rules.md` for implementation details.

## Detailed Reference

For comprehensive styling rules, component patterns, and implementation examples, reference:

**`references/styling-rules.md`** - Complete design system documentation including:
- All color values and usage rules
- Complete component patterns
- Animation keyframes
- Detailed implementation examples
- Accessibility guidelines

Use Grep to search within this file for specific patterns:
- Search "Button" for button variations
- Search "Badge" for status indicators
- Search "Animation" for loading states
- Search "Card" for container patterns

## Best Practices

1. **Consistency First**: Always prefer existing patterns over creating new variations
2. **Progressive Enhancement**: Start with base styles, then add interactive states
3. **Mobile-First**: Design for mobile, enhance for desktop
4. **Accessibility**: Never sacrifice accessibility for aesthetics
5. **Performance**: Minimize custom CSS, leverage Tailwind utilities
6. **Documentation**: Comment complex styling logic in components

## Examples from Codebase

Look for these files for reference implementations:
- Vue components in `components/` directory
- MDC components in `components/content/`
- Layout files in `layouts/`

Search for class patterns like `bg-gradient-to-r from-indigo` to find examples of brand gradient usage across the codebase.
