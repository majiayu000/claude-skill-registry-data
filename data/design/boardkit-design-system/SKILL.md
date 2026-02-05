---
name: boardkit-design-system
description: |
  Boardkit UI design system: compact density, spacing, typography, tokens, components.
  Use when creating/modifying UI components, adjusting spacing, icons, or themes.
allowed-tools: Read, Grep, Glob
---

# Boardkit Design System

## Principles

1. **Compact density** - Tool-like interface, not consumer app
2. **UnoCSS tokens** - No hardcoded pixels
3. **Lucide icons** - No other icon libraries
4. **Playground validation** - All components showcased

## Spacing Scale

| Token | Value | Usage |
|-------|-------|-------|
| `gap-1` | 4px | Tight spacing |
| `gap-1.5` | 6px | Default gap |
| `gap-2` | 8px | Section gap |
| `p-1.5` | 6px | Tight padding |
| `p-2` | 8px | Default padding |
| `p-2.5` | 10px | Comfortable padding |
| `p-3` | 12px | Large padding |

## Heights

| Token | Value | Usage |
|-------|-------|-------|
| `h-7` | 28px | Small buttons/inputs |
| `h-8` | 32px | **Default** buttons/inputs |
| `h-9` | 36px | Large buttons/inputs |

## Typography

```css
--font-family: system-ui, -apple-system, sans-serif;
```

| Token | Size | Usage |
|-------|------|-------|
| `text-xs` | 11px | Labels, hints |
| `text-sm` | 13px | Secondary text |
| `text-base` | 14px | **Default** |
| `font-normal` | 400 | Body text |
| `font-medium` | 500 | Labels |
| `font-semibold` | 600 | Headings |

## Colors

| Token | Usage |
|-------|-------|
| `primary` | Actions, focus rings |
| `background` | Surface backgrounds |
| `foreground` | Text color |
| `muted` | Disabled, secondary |
| `destructive` | Delete, danger |
| `accent` | Hover states |
| `border` | Borders, dividers |

## Components Library (28)

### Form
`BkButton`, `BkIconButton`, `BkInput`, `BkTextarea`, `BkCheckbox`, `BkToggle`, `BkSelect`, `BkButtonGroup`, `BkFormRow`, `BkFormSection`, `BkDropdown`

### Canvas
`BkToolbar`, `BkToolButton`, `BkColorPicker`, `BkSlider`, `SelectionHandles`

### Layout
`WidgetFrame`, `BkModal`, `BkDivider`, `BkEditableText`, `BkTooltip`

### Data
`BkDataConnectionDialog`, `BkDataSourcePicker`, `BkHistoryList`

### Context
`BkContextMenu`, `BkIcon`, `BkMenu`

### Command Palette
`BkCommandDialog`, `BkCommandInput`, `BkCommandList`, `BkCommandGroup`, `BkCommandItem`, `BkCommandEmpty`

### Settings
`BkSettingsPanel`, `BkSettingsSection`, `BkSettingsRow`, `BkPreferenceToggle`, `BkConfigForm`

## Icons (Lucide)

```vue
<BkIcon icon="plus" :size="16" />
```

Sizes: 12, 14, 16, 18, 20

**VERIFY existence before using:**
```bash
# Check if icon exists
curl -I https://lucide.dev/icons/{icon-name}
```

Common mistakes:
- `code-2` → use `braces`
- `list-check` → use `list-todo`

## Button Variants

```vue
<BkButton variant="default">Default</BkButton>
<BkButton variant="primary">Primary</BkButton>
<BkButton variant="ghost">Ghost</BkButton>
<BkButton variant="destructive">Delete</BkButton>
<BkButton size="sm">Small</BkButton>
<BkButton size="lg">Large</BkButton>
```

## Key Files

| Purpose | Path |
|---------|------|
| Complete spec | `packages/ui/DESIGN_SYSTEM.md` |
| Components | `packages/ui/src/components/` |
| Tokens | `packages/ui/uno.config.ts` |
| CSS vars | `apps/web/src/styles/globals.css` |
| Playground | `apps/web/src/pages/Playground.vue` |
