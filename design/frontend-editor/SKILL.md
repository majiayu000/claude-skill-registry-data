---
name: epci:frontend-editor
description: >-
  Tailwind CSS patterns for presentation layer. Includes design tokens,
  component variants (primary, secondary, success, warning, danger, ghost, outline),
  responsive utilities, WCAG 2.1 AA accessibility. Use when: Tailwind styling development, tailwind config detected, frontend presentation styling.
  Not for: JavaScript behavior logic, Vue Svelte frameworks, Bootstrap styling, backend code.
user-invocable: false
---

# Frontend Editor — Tailwind CSS & Presentation Layer

## Overview

Modern CSS patterns with Tailwind utility-first approach. This skill focuses on the **presentation layer**: design tokens, component variants, responsive layouts, and accessibility-first styling.

**Key principle**: Separate presentation (this skill) from behavior (`javascript-react`).

| Aspect | Frontend Editor | JavaScript React |
|--------|-----------------|------------------|
| Focus | HTML/CSS/Tailwind | React components |
| Variants | Styling patterns | State management |
| Tokens | Colors, spacing, typography | Props, hooks |
| Output | Classes, styles | Interactive behavior |

## Auto-detection

Loaded when detecting:
- `tailwind.config.js`, `tailwind.config.ts`, `tailwind.config.mjs`
- Optional: `components.json` (shadcn/ui), `@radix-ui/*` in package.json
- Files: `*.css`, `*.scss` with Tailwind directives
- Structure: `src/components/`, `src/ui/`

## MCP Integration

### Auto-activation

| MCP Server | Role | Trigger |
|------------|------|---------|
| **Magic** | Component generation via 21st.dev | Primary, auto with `--persona-frontend` |
| **Context7** | Tailwind/Radix documentation | Secondary, on "tailwind", "design-system" |

### Keywords

`component`, `button`, `form`, `modal`, `card`, `table`, `layout`, `responsive`, `tailwind`, `css`, `style`, `ui`, `ux`, `variant`, `theme`, `design`

### Workflow

```
1. Detect Tailwind config → Load skill
2. Magic + Context7 activated if frontend persona
3. Generate component with variants
4. Apply accessibility patterns automatically
```

## Design Tokens

### Color System

```javascript
// tailwind.config.ts
export default {
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff', 100: '#dbeafe', 200: '#bfdbfe',
          300: '#93c5fd', 400: '#60a5fa', 500: '#3b82f6',
          600: '#2563eb', 700: '#1d4ed8', 800: '#1e40af', 900: '#1e3a8a',
        },
        // secondary, success, warning, danger follow same pattern
      },
    },
  },
};
```

### Spacing Scale

| Token | Value | Use Case |
|-------|-------|----------|
| 1 | 4px | Tight gaps |
| 2 | 8px | Component padding |
| 4 | 16px | Section spacing |
| 6 | 24px | Card padding |
| 8 | 32px | Layout gaps |

-> See `${CLAUDE_PLUGIN_ROOT}/skills/stack/frontend-editor/references/tailwind-conventions.md` for full token system

## Component Variants

### 7 Standard Variants

| Variant | Use Case | Base Classes |
|---------|----------|--------------|
| `primary` | Main actions | `bg-primary-600 text-white hover:bg-primary-700` |
| `secondary` | Secondary actions | `bg-gray-200 text-gray-900 hover:bg-gray-300` |
| `success` | Confirmations | `bg-green-600 text-white hover:bg-green-700` |
| `warning` | Cautionary | `bg-yellow-600 text-white hover:bg-yellow-700` |
| `danger` | Destructive | `bg-red-600 text-white hover:bg-red-700` |
| `ghost` | Subtle actions | `text-gray-700 hover:bg-gray-100` |
| `outline` | Border emphasis | `border border-gray-300 hover:bg-gray-50` |

### Size Variants

| Size | Padding | Text | Touch Target |
|------|---------|------|--------------|
| `sm` | `px-3 py-1.5` | `text-sm` | 32px |
| `md` | `px-4 py-2` | `text-base` | 40px |
| `lg` | `px-6 py-3` | `text-lg` | 48px |

### Utility Function

```typescript
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
```

-> See `${CLAUDE_PLUGIN_ROOT}/skills/stack/frontend-editor/references/components-catalog.md` for implementation examples

## Accessibility (WCAG 2.1 AA)

Built into every pattern:

### Requirements

| Criterion | Requirement | Implementation |
|-----------|-------------|----------------|
| Color contrast | 4.5:1 text, 3:1 UI | Verified color tokens |
| Focus visible | Always visible | `focus:ring-2 focus:ring-offset-2` |
| Touch targets | >= 44px | Size variants enforce this |
| Keyboard nav | Full support | Semantic HTML + ARIA |

### Focus Pattern

```css
/* Applied to all interactive elements */
focus:outline-none
focus:ring-2
focus:ring-offset-2
focus:ring-primary-500
```

### Screen Reader

```html
<!-- Visually hidden, screen reader visible -->
<span class="sr-only">Description</span>

<!-- Skip link -->
<a href="#main" class="sr-only focus:not-sr-only">Skip to main</a>
```

-> See `${CLAUDE_PLUGIN_ROOT}/skills/stack/frontend-editor/references/accessibility.md` for complete WCAG checklist

## Responsive Design

### Breakpoints

| Prefix | Min Width | Target |
|--------|-----------|--------|
| (none) | 0px | Mobile first |
| `sm:` | 640px | Large phones |
| `md:` | 768px | Tablets |
| `lg:` | 1024px | Laptops |
| `xl:` | 1280px | Desktops |
| `2xl:` | 1536px | Large screens |

### Pattern

```html
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  <!-- Responsive grid -->
</div>

<button class="px-3 py-1.5 md:px-4 md:py-2 lg:px-6 lg:py-3">
  <!-- Responsive sizing -->
</button>
```

## Dark Mode

### Configuration

```javascript
// tailwind.config.ts
darkMode: 'class', // or 'media' for system preference
```

### Pattern

```html
<div class="bg-white dark:bg-gray-900 text-gray-900 dark:text-white">
  <!-- Automatically switches -->
</div>
```

## Commands

```bash
# Development
npm run dev           # Vite dev with HMR
npm run build         # Production build

# Tailwind
npx tailwindcss -i ./src/input.css -o ./dist/output.css --watch

# Design tokens
npm run tokens:build  # Generate from design tokens
```

## Quick Reference

| Task | Pattern |
|------|---------|
| Merge classes | `cn(base, variant, className)` |
| Variants | 7 types: primary, secondary, success, warning, danger, ghost, outline |
| Sizes | sm (32px), md (40px), lg (48px) touch targets |
| Colors | Design tokens in tailwind.config |
| Spacing | Tailwind scale (4px base unit) |
| Focus | Always `focus:ring-2 focus:ring-offset-2` |
| Responsive | Mobile-first: `md:`, `lg:`, `xl:` |
| Dark mode | `dark:` prefix |
| Accessibility | WCAG 2.1 AA minimum |

## Common Patterns

| Pattern | Implementation | Benefit |
|---------|----------------|---------|
| Utility cn() | clsx + tailwind-merge | Safe class merging |
| Variant objects | Map of class strings | Type-safe variants |
| Size scale | sm/md/lg consistent | Predictable sizing |
| Focus rings | ring-2 + offset-2 | Visible focus |
| Token system | CSS variables | Runtime theming |
| Responsive grid | grid + breakpoints | Fluid layouts |

## Anti-patterns

| Anti-pattern | Problem | Alternative |
|--------------|---------|-------------|
| Inline styles | Hard to maintain | Tailwind classes |
| `!important` | Specificity wars | Layer system |
| Random colors | Inconsistent | Design tokens |
| Skip focus states | Accessibility fail | Always include |
| Fixed px values | Not responsive | Tailwind scale |
| Hardcoded breakpoints | Inconsistent | Tailwind prefixes |
| Mix frameworks | Conflicts | Tailwind only |

---

*Frontend Editor v1.0 — EPCI Stack Integration*
