---
name: ui-clone
description: Pixel-perfect UI cloning from screenshots or reference pages. Use when users ask to replicate, clone, or recreate a UI from an image, screenshot, or reference website. Triggers on keywords like "复刻", "clone", "replicate", "recreate UI", "像素级还原", "照着这个做", or when a screenshot is provided with implementation intent.
---

# UI Clone Skill

Two-phase workflow for pixel-perfect UI replication in Next.js App Router projects.

## Project Context

Working in `ai-frontend-scaffold` with:

- Tailwind CSS (semantic tokens: `bg-background`, `bg-card`, `text-foreground`, `border-border`)
- shadcn/ui (`components/ui`)
- next-themes (dark mode support)

## Constraints

1. **No hardcoded colors** - Use tokens: `bg-background`, `bg-card`, `bg-secondary`, `text-muted-foreground`, `ring-border/60`
2. **Container-first** - Nail the skeleton first (max-width, padding, card radius/shadow/border), then details
3. **Mobile-first** - base → md → lg, specify which elements show only at lg (e.g., sidebar)
4. **Minimal changes** - Output file list before coding
5. **Page = assembly only** - UI components go to `app/(main)/<route>/components/`

## Phase 1: Design Breakdown

Before any code, analyze the reference and output:

### A. Structure Tree (precise container hierarchy)

```
- Page background: color, padding (top/right/bottom/left)
- Main container: max-width, centering method, horizontal padding
- Header card: height, padding, radius, shadow, border, content alignment
- Content card: gap from header, radius, shadow, padding
- Form sections: label/textarea/button layout (vertical spacing, alignment)
- Sidebar (if any): position (top/right), size, radius, shadow, border, header style
- Floating buttons (if any): position (left + top%), button size, gap, radius, shadow
```

### B. JSONC Visual Spec

```jsonc
{
  "breakpoints": {
    "base": {
      /* mobile layout */
    },
    "md": {
      /* tablet adjustments */
    },
    "lg": {
      /* desktop: sidebar visible, etc. */
    },
  },
  "spacing": {
    "headerToContent": "24px or 32px?",
    "cardPadding": "p-6",
    "sectionGap": "space-y-6",
  },
  "radius": {
    "card": "rounded-xl",
    "input": "rounded-lg",
    "button": "rounded-md",
  },
  "shadow": {
    "card": "shadow-sm",
    "floating": "shadow-lg",
  },
  "border": {
    "card": "ring-1 ring-border/60",
  },
  "typography": {
    "logo": "text-xl font-black",
    "nav": "text-sm font-medium",
    "label": "text-sm font-bold",
    "body": "text-sm",
  },
  "colors": "ONLY tokens: bg-background, bg-card, bg-secondary, text-foreground, text-muted-foreground, border-border",
}
```

**Output breakdown only, no code yet.**

## Phase 2: Implementation

With the breakdown from Phase 1, implement:

### File Structure

```
app/(main)/<route>/
├── page.tsx              # Assembly only
├── components/
│   ├── header.tsx
│   ├── main-card.tsx
│   ├── sidebar.tsx       # (if needed)
│   └── floating-actions.tsx  # (if needed)
└── data.ts               # Sample data (if >20 lines)
```

### Implementation Rules

1. Output file list first, then code
2. `page.tsx` only assembles components
3. All colors via tokens
4. Card border + shadow: `ring-1 ring-border/60 shadow-sm`
5. Responsive explicit:
   - base: single column
   - lg: sidebar visible (`hidden lg:block`)

### Self-Check

After implementation, verify:

- [ ] Spacing (px/py/mt) matches spec
- [ ] Header card height and padding correct
- [ ] Content card max-width and centering correct
- [ ] No hardcoded hex colors

## Phase 3: Refinement (1-2 rounds)

When "close but not quite", provide a diff list for minimal fixes:

```
差异清单示例：
1) Header card height too short: need +4px padding
2) Content card gap too small: mt-6 → mt-8
3) Textarea background too dark: bg-secondary → bg-muted
4) Sidebar top position off: top-24 → top-28
5) Floating buttons need to be closer to edge: left-4 → left-3
```

### Refinement Rules

- Only modify className related to the diff
- No directory/component restructuring
- Still no hardcoded hex colors
