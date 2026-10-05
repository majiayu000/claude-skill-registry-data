---
name: figma
description: >
  Bidirectional Figma skill — read designs and write back to Figma.
  READ: extract tokens, map Vue/Reka UI components, translate Auto Layout to Tailwind.
  WRITE: push components, screens, and design tokens from code to Figma.
  Requires /figma:figma-use skill before every use_figma call.
---

# Skill: Figma ↔ Vue 3 + shadcn-vue

## Reading flow via MCP (Figma → Code)

```
1. mcp:figma → get_design_context(nodeId or URL)  ← always first
2. mcp:figma → get_variable_defs(nodeId)           ← formal tokens
3. mcp:figma → search_design_system(query)         ← DS components
4. mcp:figma → get_screenshot(nodeId)              ← visual reference
```

---

## Figma → Tailwind Translation

### Auto Layout → Flexbox/Grid Vue

| Figma Auto Layout | Tailwind | Vue template |
|---|---|---|
| Horizontal, gap 16 | `flex gap-4` | `<div class="flex gap-4">` |
| Vertical, gap 24 | `flex flex-col gap-6` | `<div class="flex flex-col gap-6">` |
| Space between | `flex justify-between` | |
| Fill container (width) | `flex-1` or `w-full` | |
| Fixed width 320px | `w-80` or `w-[320px]` | |
| Wrap | `flex flex-wrap` | |
| Align center | `items-center` | |
| Grid 3 cols, gap 16 | `grid grid-cols-3 gap-4` | |

### Colors → shadcn-vue CSS Variables

| Figma Semantic | shadcn CSS Variable | Tailwind |
|---|---|---|
| Primary | `--primary` | `bg-primary text-primary-foreground` |
| Background | `--background` | `bg-background` |
| Foreground | `--foreground` | `text-foreground` |
| Muted | `--muted-foreground` | `text-muted-foreground` |
| Destructive | `--destructive` | `text-destructive border-destructive` |
| Border | `--border` | `border-border` |
| Card | `--card` | `bg-card` |

### Figma Typography → Tailwind

| Figma | Tailwind |
|---|---|
| 12px Regular | `text-xs` |
| 14px Regular | `text-sm` |
| 14px Medium 500 | `text-sm font-medium` |
| 14px Semibold 600 | `text-sm font-semibold` |
| 16px Regular | `text-base` |
| 18px Semibold | `text-lg font-semibold` |
| 20px Bold | `text-xl font-bold` |
| 24px Bold | `text-2xl font-bold` |
| 30px Bold | `text-3xl font-bold` |

Figma line-height (absolute) → Tailwind (relative):
- 16px line-height with 14px font → `leading-none` (1)
- 20px / 14px → `leading-tight` (1.25)
- 20px / 16px → `leading-5` (1.25)
- 24px / 16px → `leading-6` (1.5) ← default body

### Spacing → Tailwind Scale (base 4px)

| Figma px | Tailwind | rem |
|---|---|---|
| 2 | `gap-0.5 p-0.5` | 0.125 |
| 4 | `gap-1 p-1` | 0.25 |
| 8 | `gap-2 p-2` | 0.5 |
| 12 | `gap-3 p-3` | 0.75 |
| 16 | `gap-4 p-4` | 1 |
| 20 | `gap-5 p-5` | 1.25 |
| 24 | `gap-6 p-6` | 1.5 |
| 32 | `gap-8 p-8` | 2 |
| 40 | `gap-10 p-10` | 2.5 |
| 48 | `gap-12 p-12` | 3 |

### Border radius → Tailwind

| Figma | Tailwind |
|---|---|
| 4px | `rounded` |
| 6px | `rounded-md` |
| 8px | `rounded-lg` |
| 12px | `rounded-xl` |
| 16px | `rounded-2xl` |
| 50% / circle | `rounded-full` |

### Shadows → Tailwind

| Figma | Tailwind |
|---|---|
| `0 1px 2px rgba(0,0,0,0.05)` | `shadow-sm` |
| `0 1px 3px rgba(0,0,0,0.1)` | `shadow` |
| `0 4px 6px rgba(0,0,0,0.07)` | `shadow-md` |
| `0 10px 15px rgba(0,0,0,0.1)` | `shadow-lg` |
| `0 25px 50px rgba(0,0,0,0.25)` | `shadow-2xl` |

---

## Figma → shadcn-vue Vue Component Mapping

| Visual pattern in Figma | shadcn-vue component |
|---|---|
| Surface / Card with padding | `<Card>` + sub-parts |
| Primary button | `<Button>` |
| Destructive button | `<Button variant="destructive">` |
| Ghost button | `<Button variant="ghost">` |
| Text input | `<Input>` |
| Text area | `<Textarea>` |
| Dropdown / Select | `<Select>` + sub-parts |
| Select with search | Combobox (Command + Popover) |
| Modal / Overlay | `<Dialog>` |
| Bottom sheet | `<Sheet>` |
| Temporary notification | `toast()` from vue-sonner |
| Badge / Chip | `<Badge>` |
| Context menu | `<DropdownMenu>` |
| Tooltip | `<Tooltip>` |
| Tabs | `<Tabs>` + sub-parts |
| Accordion | `<Accordion>` + sub-parts |
| Checkbox | `<Checkbox>` |
| Toggle on/off | `<Switch>` |
| Loading placeholder | `<Skeleton>` |
| Empty state | `<Empty>` + sub-parts |
| Data table | `<DataTable>` |
| Breadcrumb | `<Breadcrumb>` + sub-parts |
| Form field | `<Field>` or `<FormField>` |
| Button group | `<ButtonGroup>` |
| Input with icon | `<InputGroup>` |
| Spinner | `<Spinner>` |
| Stepper | `<Stepper>` + sub-parts |

---

## Components without shadcn-vue equivalent → Reka UI primitive

```vue
<!-- Custom component with Reka UI -->
<script setup lang="ts">
import { ComboboxRoot, ComboboxInput, ComboboxContent, ComboboxItem } from 'reka-ui'
</script>
<template>
  <ComboboxRoot>
    <ComboboxInput class="..." />
    <ComboboxContent class="...">
      <ComboboxItem v-for="item in items" :key="item.id" :value="item">
        {{ item.label }}
      </ComboboxItem>
    </ComboboxContent>
  </ComboboxRoot>
</template>
```

---

## Expected output: figma-spec.md

```markdown
# Figma Spec — [Frame Name]

## Extracted tokens

### Colors
| Token | Hex | Tailwind equiv. | CSS var |
|---|---|---|---|
| Brand blue | #2563EB | `bg-blue-600` | `--primary` |

### Typography
| Usage | Size | Weight | Tailwind |
|---|---|---|---|
| Heading | 24px | 700 | `text-2xl font-bold` |

### Dominant spacing
| Usage | Value | Tailwind |
|---|---|---|
| Gap between cards | 24px | `gap-6` |

## Mapped components

### [ComponentName]
- **shadcn-vue**: `<Card>` with `<CardHeader>`, `<CardContent>`, `<CardFooter>`
- **Reka UI base**: `N/A` (shadcn-vue abstracts it)
- **Required props**: title, description, actions[]
- **Variants**: default, highlighted
- **States**: default, loading (Skeleton), empty
- **Notes**: Status Badge in CardHeader

## Documented behaviors
- Hover: card elevates with shadow-md
- Loading: 3 Skeleton cards of same dimensions

## Deviations from standard shadcn-vue
- Badge uses custom color #7C3AED — add as CSS variable
```

---

## Writing flow via MCP (Code → Figma)

### Prerequisites

**MANDATORY**: Before every `use_figma` call, load the `/figma:figma-use` skill.
This skill teaches the Figma Plugin API syntax needed for write operations.

```
1. Load /figma:figma-use skill                    ← ALWAYS first
2. mcp:figma → whoami                              ← verify connection
3. mcp:figma → search_design_system(query)         ← discover existing DS
4. mcp:figma → use_figma(javascript)               ← create/edit nodes
```

### Available write tools

| Tool | What it does |
|------|-------------|
| `use_figma` | Execute JavaScript in Figma context — create frames, text, components, set properties |
| `create_new_file` | Create a new Figma or FigJam file |
| `generate_diagram` | Create diagrams in FigJam |

### Available design skills

| Skill | When to use |
|-------|------------|
| `/figma:figma-use` | **Required** before every `use_figma` call |
| `/figma:figma-generate-design` | Push full screens/pages to Figma |
| `/figma:figma-generate-library` | Build design system with tokens and components |

### Tailwind → Figma reverse mapping

| Tailwind | Figma Auto Layout property |
|----------|---------------------------|
| `flex gap-4` | `layoutMode: "HORIZONTAL"`, `itemSpacing: 16` |
| `flex flex-col gap-6` | `layoutMode: "VERTICAL"`, `itemSpacing: 24` |
| `justify-between` | `primaryAxisAlignItems: "SPACE_BETWEEN"` |
| `items-center` | `counterAxisAlignItems: "CENTER"` |
| `p-4` | `paddingTop/Right/Bottom/Left: 16` |
| `px-4 py-2` | `paddingLeft/Right: 16`, `paddingTop/Bottom: 8` |
| `w-full` | `layoutSizingHorizontal: "FILL"` |
| `flex-1` | `layoutGrow: 1` |

| Tailwind | Figma node property |
|----------|---------------------|
| `rounded-lg` | `cornerRadius: 8` |
| `shadow-md` | Drop shadow effect: `y: 4, blur: 6, spread: -1` |
| `text-sm font-medium` | `fontSize: 14, fontWeight: 500` |
| `bg-primary` | Fill bound to variable `--primary` |
| `border-border` | Stroke bound to variable `--border` |

### Writing components — pattern

```javascript
// Example: Create a Card component in Figma
const card = figma.createFrame()
card.name = "Card"
card.layoutMode = "VERTICAL"
card.itemSpacing = 0
card.cornerRadius = 8
card.paddingTop = card.paddingBottom = 24
card.paddingLeft = card.paddingRight = 24

// Bind to variable instead of hardcoding
const bgVar = figma.variables.getLocalVariables().find(v => v.name === "card")
if (bgVar) {
  card.setBoundVariable("fills", bgVar.id)
}
```

### Writing tokens — pattern

```javascript
// Create a variable collection for design tokens
const collection = figma.variables.createVariableCollection("Design Tokens")

// Add color variable with light/dark modes
const primaryVar = figma.variables.createVariable("primary", collection.id, "COLOR")
primaryVar.setValueForMode(lightModeId, { r: 0.09, g: 0.09, b: 0.09 })
primaryVar.setValueForMode(darkModeId, { r: 0.98, g: 0.98, b: 0.98 })
```

### Gotchas — Write mode

- Always use `figma.variables` for colors — never hardcode hex
- Auto Layout must be set via `layoutMode` before setting `itemSpacing`
- Text nodes require `figma.loadFontAsync()` before setting `characters`
- Component variants: use `figma.combineAsVariants()` after creating all variants
- Figma plugin API is synchronous except font loading — handle `await` properly
