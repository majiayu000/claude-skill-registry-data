---
name: icon-system
description: Establish or validate the canonical Icon wrapper component, size token scale, stroke weight conventions, and illustration usage standards. Creates src/components/ui/icon.tsx and documents the full icon system. Run once to bootstrap, then as a validator.
user-invocable: true
allowed-tools: Read, Write, Edit, Grep, Glob
---

Establish or validate the canonical icon and illustration system for this project.

Mode: $ARGUMENTS

- If no argument or `setup`: create the Icon wrapper and validate/document the system
- If `validate`: audit the wrapper and conventions without creating files
- If `docs`: only output the icon system reference (for pasting into design docs)

## Step 1 — Assess Current State

1. Check if `src/components/ui/icon.tsx` exists. Read it if so.
2. Read `src/app/globals.css` — note existing CSS custom properties.
3. Read `tailwind.config.ts` — note the spacing/sizing token scale.
4. Search for current icon import patterns: `grep -r "from 'lucide-react'" src/ --include="*.tsx" | head -20`
5. Note any existing raw Lucide usage to understand migration scope.

## Step 2 — Create the Icon Wrapper (if missing or incomplete)

The canonical `<Icon>` component is the **single point of contact** for all icon rendering in the UI. It enforces:
- The size token scale
- `currentColor` inheritance (no inline color)
- `shrink-0` to prevent flex compression
- Correct accessibility defaults (`aria-hidden` for decorative, `aria-label` passthrough for labeled)
- Consistent `strokeWidth` per size tier

Write `src/components/ui/icon.tsx`:

```tsx
import * as React from "react"
import { type LucideIcon } from "lucide-react"
import { cn } from "@/lib/utils"

// Canonical size scale — use these tokens, never arbitrary pixel values
export const ICON_SIZES = {
  xs: 12,   // captions, badges, inline metadata
  sm: 16,   // inline text, form labels, table cells
  md: 20,   // default UI, buttons, nav items
  lg: 24,   // section headers, card actions, prominent UI
  xl: 32,   // empty states, feature highlights
  "2xl": 48, // hero sections, marketing, onboarding
} as const

export type IconSize = keyof typeof ICON_SIZES

// Stroke weight per size tier — thinner at large sizes for refinement
const STROKE_WIDTHS: Record<IconSize, number> = {
  xs: 2,
  sm: 2,
  md: 2,
  lg: 2,
  xl: 1.5,
  "2xl": 1.5,
}

interface IconProps {
  /** The Lucide icon component to render */
  icon: LucideIcon
  /** Size token — never use raw pixel values */
  size?: IconSize
  /** Override stroke width — only use if the size-tier default isn't right */
  strokeWidth?: number
  /** Accessible label. If provided, icon is announced to screen readers.
   *  If omitted, icon is treated as decorative (aria-hidden). */
  label?: string
  className?: string
}

/**
 * Canonical Icon component. Always use this instead of raw Lucide icons.
 *
 * @example Decorative (adjacent text provides meaning)
 * <Icon icon={Check} size="md" />
 *
 * @example Labeled (icon is the only affordance — e.g. icon-only button)
 * <Button variant="ghost" size="icon" aria-label="Close">
 *   <Icon icon={X} size="md" />
 * </Button>
 *
 * @example With explicit label (standalone icon with semantic meaning)
 * <Icon icon={AlertTriangle} size="lg" label="Warning" />
 */
export function Icon({
  icon: IconComponent,
  size = "md",
  strokeWidth,
  label,
  className,
}: IconProps) {
  const px = ICON_SIZES[size]
  const sw = strokeWidth ?? STROKE_WIDTHS[size]

  return (
    <IconComponent
      size={px}
      strokeWidth={sw}
      aria-hidden={!label}
      aria-label={label}
      className={cn("shrink-0", className)}
    />
  )
}
```

## Step 3 — Validate the Wrapper

After creating or reading the wrapper, confirm it satisfies:

- [ ] All 6 size tokens present (`xs`, `sm`, `md`, `lg`, `xl`, `2xl`)
- [ ] Stroke weight differentiates small (2) from large (1.5) tiers
- [ ] `shrink-0` applied unconditionally
- [ ] `aria-hidden={!label}` — decorative by default, labeled when needed
- [ ] `aria-label={label}` passed through
- [ ] No hardcoded colors — uses `currentColor` via Tailwind text classes
- [ ] TypeScript types: `LucideIcon`, `IconSize`, `IconProps`
- [ ] Exported: `Icon`, `ICON_SIZES`, `IconSize`

## Step 4 — Document the Usage Conventions

Output the following as the Icon System Reference. Save to `_docs/design/ICON_SYSTEM.md` if it doesn't exist:

---

# Icon System Reference

## Core Principle

One library, one wrapper. All icons go through `<Icon>` from `@/components/ui/icon`. Never import and render Lucide icons directly in application components.

## Library

**Lucide React** — the only icon library used in this project.
- Consistent 24px grid, 2px stroke, rounded line caps
- Tree-shakeable (only the icons you import are bundled)
- TypeScript-first, actively maintained
- Searchable at: lucide.dev

## The Icon Wrapper

```tsx
import { Icon } from "@/components/ui/icon"
import { ArrowRight, Check, AlertTriangle } from "lucide-react"

// Decorative — aria-hidden by default
<Icon icon={ArrowRight} size="md" />

// With custom color via semantic token
<Icon icon={Check} size="sm" className="text-primary" />

// Labeled (standalone icon button)
<Button variant="ghost" size="icon" aria-label="Dismiss">
  <Icon icon={X} size="md" />
</Button>
```

## Size Scale

| Token | px  | Use case |
|-------|-----|----------|
| `xs`  | 12  | Captions, badges, timestamps, breadcrumbs |
| `sm`  | 16  | Inline with body text, form labels, table cells |
| `md`  | 20  | **Default.** Buttons, nav, cards, lists |
| `lg`  | 24  | Section headers, prominent actions, tabs |
| `xl`  | 32  | Empty states, feature icons, tooltips |
| `2xl` | 48  | Hero sections, onboarding, marketing |

## Color Rules

Icons inherit `currentColor` — they get their color from the surrounding `text-*` class. Never set a color directly on an icon.

```tsx
// ✅ Color the parent or the icon via semantic token
<div className="text-muted-foreground">
  <Icon icon={Calendar} size="sm" />
  <span>March 13, 2026</span>
</div>

// ✅ Or directly on the Icon
<Icon icon={AlertTriangle} size="md" className="text-destructive" />

// ❌ Never hardcode
<Icon icon={AlertTriangle} size="md" className="text-yellow-500" />
```

## Accessibility Patterns

### Decorative icons (icon + adjacent text)
The text provides the meaning. Icon is hidden from screen readers.
```tsx
<button>
  <Icon icon={Download} size="md" />  {/* aria-hidden automatically */}
  <span>Download</span>
</button>
```

### Icon-only interactive elements
The button needs an `aria-label`. Icon is still decorative.
```tsx
<Button variant="ghost" size="icon" aria-label="Close dialog">
  <Icon icon={X} size="md" />
</Button>
```

### Standalone meaningful icons
Use the `label` prop — the icon announces itself.
```tsx
<Icon icon={Lock} size="md" label="Secure connection" />
```

## Stroke Width Convention

The wrapper sets stroke weight automatically per size tier:
- `xs`–`lg`: `strokeWidth={2}` — standard weight for UI
- `xl`–`2xl`: `strokeWidth={1.5}` — lighter for large/marketing contexts

Override only when the context genuinely demands it:
```tsx
<Icon icon={Star} size="xl" strokeWidth={1} />  {/* ultra-light for decorative hero use */}
```

## Illustration Standards

For SVG illustrations (empty states, onboarding, marketing):

1. **Format:** Always SVG, never PNG/JPG for illustrations
2. **Storage:** `public/images/illustrations/` for static SVGs; `src/components/illustrations/` for React SVG components needing dynamic coloring
3. **Accessibility:**
   - Decorative: `<img src="..." alt="" />` or `aria-hidden="true"` on inline SVG
   - Meaningful: `role="img"` + `<title>` inside the SVG
4. **Dark mode:** Use CSS custom properties (`var(--color-primary)`) inside SVG files so they respect the design token system. Avoid hardcoded hex colors.
5. **Style:** Maintain one consistent illustration style across the platform. Do not mix flat, outline, and isometric in the same UI region.

## Anti-Patterns

| Anti-pattern | Fix |
|---|---|
| `import { Check } from 'lucide-react'; <Check className="w-4 h-4" />` | `<Icon icon={Check} size="sm" />` |
| `<Check className="w-5 h-5 text-blue-500" />` | `<Icon icon={Check} size="md" className="text-primary" />` |
| `<button onClick={fn}><X /></button>` (no label) | `<Button aria-label="Close"><Icon icon={X} size="md" /></Button>` |
| `<img src="empty-state.png" />` | `<img src="empty-state.svg" alt="" />` |
| Mixing Heroicons and Lucide | Use Lucide only |
| `size={18}` raw pixel on icon | Use `size="sm"` (16) or `size="md"` (20) |

---

## Step 5 — Check for `_docs/design/` directory

If it doesn't exist, create it and save `ICON_SYSTEM.md` there. If `_docs/design/ICON_SYSTEM.md` already exists, update it with any gaps.

## Output Format

```
## Icon System Setup Report

### Icon Wrapper
- Status: [Created / Already exists / Updated]
- Path: src/components/ui/icon.tsx
- Issues: [any gaps found]

### Conventions Document
- Status: [Created / Already exists / Updated]
- Path: _docs/design/ICON_SYSTEM.md

### Migration Scope
- Raw Lucide usages found: X (run /icon-audit to fix)
- Files affected: [list]

### Next Steps
1. Run /icon-audit to fix all existing raw icon usage
2. [Any other issues]
```
