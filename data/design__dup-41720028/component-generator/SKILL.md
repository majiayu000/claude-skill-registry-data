---
name: component-generator
description: Generate production-ready SolidJS components with Kobalte accessibility primitives, CVA variants, and Storybook stories. Use when creating UI components for the frontend application.
---

# SolidJS Component Generator

Generate fully-functional SolidJS components following established architecture patterns.

## Critical Constraints

**Components MUST be purely presentational:**
- ✅ Accept props, render UI, emit events via callbacks
- ✅ Use Kobalte primitives for accessibility where appropriate
- ✅ Support both light and dark themes
- ✅ Pass biome + TypeScript checks
- ✅ Have Storybook stories for testing

**Components must NOT:**
- ❌ Make API calls or import backend packages
- ❌ Contain business logic (belongs in pages/features)
- ❌ Manage application state (use props/callbacks)

## Required Reading (BEFORE ANY GENERATION)

**Read these files in order before writing code:**

1. **`/skills/services/frontend/src/components/ui/button/button.tsx`** - PRIMARY REFERENCE pattern
2. **`/skills/.claude/skills/component-generator/kobalte-primitives.md`** - Primitive catalog with import paths
3. **`/skills/.claude/skills/component-generator/accessibility-guidelines.md`** - Props to expose per component type
4. **`/skills/.claude/skills/component-generator/color-reference.md`** - Theme tokens (NEVER use default Tailwind colors)
5. **`/skills/.claude/skills/component-generator/themed-story-pattern.md`** - Story pattern with Light/Dark variants

**Additional references:**
- `/skills/services/frontend/src/components/ui/badge/badge.tsx` - Plain HTML + CVA pattern
- `/skills/services/frontend/src/components/composite/search-input/search-input.tsx` - Complex Kobalte Combobox

## Workflow

### Stage 1: Discovery

Gather these requirements:

1. **Component Name** - PascalCase (e.g., "IconButton", "UserCard")
2. **Tier** - Where it belongs:
   - `primitives` - Layout elements (Flex, Stack, Text)
   - `ui` - Interactive components (Button, Badge, Card)
   - `composite` - Combined ui components (SearchInput, IconButton)
   - `feature` - Domain-specific layouts (Navbar, Footer)
3. **Purpose** - Brief description for Kobalte matching

### Stage 2: Design

1. **Kobalte Primitive Selection:**
   - Read `kobalte-primitives.md`
   - Match keywords from user's purpose description
   - Suggest top matches or "none" for plain HTML
   - User confirms choice

2. **Variants:**
   - Color variants: primary, secondary, info, success, warning, danger, outline (based on component type)
   - Size variants: sm, md, lg, xl (based on Button pattern)
   - User can accept suggestions or customize

3. **Props:**
   - Read `accessibility-guidelines.md` for component type
   - Determine which accessibility props to expose
   - Ask about additional props (icon, loading, etc.)

### Stage 3: Confirm

Present summary:
```
I'll create {{NAME}} with:
- Tier: {{TIER}}
- Base: {{PRIMITIVE or "Plain HTML"}}
- Variants: {{COLORS}}, {{SIZES}}
- Files: index.ts, {{name}}.tsx, {{name}}.stories.tsx

Generate?
```

### Stage 4: Generate & Validate

**Pre-generation:**
- Check if component already exists
- Create tier directory if needed

**Generate 3 files:**

1. **{name}.tsx** - Component implementation:
   - Determine pattern: USE_KOBALTE (true/false), HAS_VARIANTS (true/false)
   - Follow Button.tsx structure exactly
   - Use color-reference.md for variant classes
   - Use accessibility-guidelines.md for props
   - Always spread `{...others}` for HTML attribute passthrough

2. **index.ts** - Barrel export:
   ```typescript
   export { ComponentName, type ComponentNameProps } from "./component-name";
   ```

3. **{name}.stories.tsx** - Themed stories:
   - Follow themed-story-pattern.md exactly
   - Create Light/Dark variant pairs for each variant
   - Include AllVariants showcase story

**Validate (must all pass before proceeding):**
```bash
cd /skills/services/frontend && pnpm check      # Biome
cd /skills/services/frontend && pnpm typecheck  # TypeScript
cd /skills/services/frontend && pnpm test       # Storybook tests
```

**If validation fails:** Fix errors properly (no workarounds), re-run validation.

**Post-generation response:**
```
✅ Generated {{NAME}} successfully!

Files: index.ts, {{name}}.tsx, {{name}}.stories.tsx
Location: /skills/services/frontend/src/components/{{tier}}/{{name}}/

Validation: ✅ Biome ✅ TypeScript ✅ Tests

Import: import { {{NAME}} } from "@/components/{{tier}}/{{name}}"
Usage: <{{NAME}} variant="primary" size="md">Content</{{NAME}}>
```

## Component Patterns

**Determine based on requirements:**

| Pattern | USE_KOBALTE | HAS_VARIANTS | Example |
|---------|-------------|--------------|---------|
| Kobalte + CVA | true | true | Button |
| Plain HTML + CVA | false | true | Badge |
| Plain HTML only | false | false | Label |
| Kobalte only | true | false | (rare) |

## Story Pattern

**All stories use themed Light/Dark variants:**

```tsx
import { createThemedStories } from "@/components/story-helpers";

const primaryBase: Story = {
  args: { variant: "primary", children: "Primary" },
};

const primaryThemed = createThemedStories({
  story: primaryBase,
  testMode: "both",
});

export const PrimaryLight = primaryThemed.Light;
export const PrimaryDark = primaryThemed.Dark;
```

**testMode options:** `"both"` | `"light"` | `"dark"` | `"none"`

## Key Principles

1. **Read reference files BEFORE generation** - Button.tsx is PRIMARY REFERENCE
2. **Follow existing patterns exactly** - Don't invent new patterns
3. **Accessibility first** - Use Kobalte, expose accessibility props
4. **Dark mode mandatory** - Theme colors need `-dark` variants, shared colors don't
5. **Always spread `{...others}`** - Enables HTML attribute passthrough
6. **No workarounds** - Fix errors properly, never use type assertions
7. **One component at a time** - Complete and validate before proceeding
8. **Use `rounded-radius`** - Not `rounded-md` or `rounded-lg` (badges use `rounded-full`)

## Error Handling

**Component exists:** Ask to overwrite or choose new name

**Validation fails:**
1. Read error message
2. Fix the actual issue (no workarounds)
3. Re-run validation
4. Repeat until clean

**Invalid tier:** Show valid options (primitives, ui, composite, feature)

## Example

```
User: Create a Badge component

Agent: Which tier? (primitives/ui/composite/feature)

User: ui

Agent: Purpose?

User: Small label for status or categories

Agent: No direct Kobalte match. Use plain HTML?

User: Yes

Agent: Color variants? Suggested: primary, secondary, info, success, warning, danger

User: Use suggestions

Agent: Size variants? Suggested: sm, md

User: sm and md

Agent:
Creating Badge:
- Tier: ui | Base: span | Variants: 6 colors, 2 sizes
- Files: index.ts, badge.tsx, badge.stories.tsx

Generate?

User: Yes

Agent: [Reads reference files, generates, validates]

✅ Generated Badge successfully!
Location: /skills/services/frontend/src/components/ui/badge/
Validation: ✅ Biome ✅ TypeScript ✅ Tests
Import: import { Badge } from "@/components/ui/badge"
```

## Start

Greet the user and ask what component they'd like to create.
