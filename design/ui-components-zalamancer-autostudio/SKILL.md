---
name: ui-components
description: UI component registry and design system for ProAnimate. Auto-applied before creating ANY UI — buttons, inputs, panels, modals, layouts. Prevents duplicate components and enforces visual consistency.
user-invocable: false
---

# UI Component Registry & Design System

**BEFORE creating any UI element, check this registry.** If a component exists that does what you need, USE IT. Never create a duplicate.

## Rule: Search Before Creating

Before writing ANY new UI element (button, input, select, toggle, slider, modal, card, spinner, toast, dropdown, tab, progress bar, color picker, drag zone), run:

```bash
rg "ComponentNameYouMightNeed" src/components/ui/
```

If it exists, import and use it. If it doesn't, build it following the patterns below and ADD it to `src/components/ui/`.

## Shared Components (`src/components/ui/`)

### Layout & Structure
| Component | Import | Use For |
|-----------|--------|---------|
| `PanelLayout` | `@/components/ui/PanelHeader` | Wrapping entire panel (icon + title + scrollable body + sticky footer) |
| `PanelHeader` | `@/components/ui/PanelHeader` | Panel header with icon, title, trailing content, optional search |
| `PanelSection` | `@/components/ui/panel-controls/PanelSection` | Grouping controls with title + bottom border. Supports `collapsible`, `icon`, `badge`, `defaultOpen` props. |
| `GlassPanel` | `@/components/ui/GlassPanel` | Frosted glass card container |

### Buttons
| Component | Import | Use For |
|-----------|--------|---------|
| `PanelActionButton` | `@/components/ui/panel-controls/PanelActionButton` | Primary/secondary/destructive/accent action buttons in panels |
| `IconButton` | `@/components/ui/IconButton` | Icon-only buttons (solid/ghost/outline variants) |
| `PanelButtonGroup` | `@/components/ui/panel-controls/PanelButtonGroup` | Radio-style button groups |

**PanelActionButton variants:**
- `primary` -- `bg-[#4a7eff] text-white hover:bg-[#3a6aee]`
- `secondary` -- `bg-[#2a2a2a] text-white hover:bg-[#3a3a3a]`
- `destructive` -- `bg-red-600/10 text-red-400 hover:bg-red-600/20`
- `accent` -- `bg-green-500 text-white hover:bg-green-600`

**IconButton variants:**
- `solid` / `ghost` / `outline`
- States: `default` / `active` / `disabled`
- Sizes: `sm` / `md` / `lg`

### Inputs
| Component | Import | Use For |
|-----------|--------|---------|
| `PanelInput` | `@/components/ui/panel-controls/PanelInput` | Text/number input with label |
| `PanelTextarea` | `@/components/ui/panel-controls/PanelTextarea` | Multi-line input with optional char count |
| `PanelSlider` | `@/components/ui/panel-controls/PanelSlider` | Range slider with label, suffix, precision |
| `PanelSelect` | `@/components/ui/panel-controls/PanelSelect` | Dropdown select with label |
| `PanelToggle` | `@/components/ui/panel-controls/PanelToggle` | Toggle switch with label and description |
| `PanelCheckbox` | `@/components/ui/panel-controls/PanelCheckbox` | Checkbox with label and icon |
| `PanelMultiSelect` | `@/components/ui/panel-controls/PanelMultiSelect` | Multi-select dropdown with checkboxes and images |
| `PanelSearchInput` | `@/components/ui/panel-controls/PanelSearchInput` | Search input with icon prefix |
| `DraggableNumberInput` | `@/components/ui/DraggableNumberInput` | Drag-to-change number input with formula mode |
| `CustomSelect` | `@/components/ui/CustomSelect` | Standalone custom dropdown |
| `FormulaInput` | `@/components/ui/FormulaInput` | Formula text input with autocomplete |
| `FormulaAutocomplete` | `@/components/ui/FormulaAutocomplete` | Autocomplete popup for formula input |

### Color
| Component | Import | Use For |
|-----------|--------|---------|
| `ColorPicker` | `@/components/ui/ColorPicker` | Full HSV color picker with hex input + eye dropper |
| `ColorPickerPanel` | `@/components/ui/ColorPicker` | Portal-based color picker popover (same file) |
| `PanelColorSwatches` | `@/components/ui/panel-controls/PanelColorSwatches` | Color grid with custom color option |
| `ColorSwatches` | `@/components/ui/ColorSwatches` | Extracted color swatches with modify state |
| `GradientEditor` | `@/components/ui/GradientEditor` | Linear/radial/conic gradient editor |

### Feedback
| Component | Import | Use For |
|-----------|--------|---------|
| `LoadingSpinner` | `@/components/ui/LoadingSpinner` | Inline spinner (size + className + label) |
| `LoadingOverlay` | `@/components/ui/LoadingSpinner` | Full overlay spinner (same file) |
| `ToastContainer` | `@/components/ui/ToastContainer` | Toast notifications (success/error/warning/info) |

### Navigation
| Component | Import | Use For |
|-----------|--------|---------|
| `TabNavigation` | `@/components/ui/TabNavigation` | Tab bar with icons (animated or standard mode) |
| `PanelCategoryTabs` | `@/components/ui/panel-controls/PanelCategoryTabs` | Pill-style sub-tabs within panels |
| `AspectRatioSelector` | `@/components/ui/AspectRatioSelector` | Aspect ratio pill buttons |

### Interaction
| Component | Import | Use For |
|-----------|--------|---------|
| `PanelDropZone` | `@/components/ui/panel-controls/PanelDropZone` | Drag-and-drop upload zone with icon + label |
| `BlendModeSelector` | `@/components/ui/BlendModeSelector` | Blend mode dropdown |

### Utility
| Component | Import | Use For |
|-----------|--------|---------|
| `NotificationBell` | `@/components/ui/NotificationBell` | Bell icon with unread badge |
| `NotificationDropdown` | `@/components/ui/NotificationDropdown` | Notifications dropdown panel |
| `AudioSampleCard` | `@/components/ui/AudioSampleCard` | Audio file card with metadata |
| `TimingTemplatePreview` | `@/components/ui/TimingTemplatePreview` | Timing template visual preview |

## Design Tokens (`src/components/ui/panel-controls/tokens.ts`)

**ALWAYS import tokens instead of hardcoding colors:**

```typescript
import { PANEL } from '@/components/ui/panel-controls/tokens'
```

| Token | Value | Use For |
|-------|-------|---------|
| `PANEL.surface` | `bg-[#2a2a2a]` | Input backgrounds, secondary surfaces |
| `PANEL.surfaceHover` | `hover:bg-[#3a3a3a]` | Hover state on surfaces |
| `PANEL.surfaceActive` | `bg-[#3a3a3a]` | Active/pressed surfaces |
| `PANEL.accent` | `bg-[#4a7eff]` | Primary accent (buttons, active states) |
| `PANEL.accentHover` | `hover:bg-[#3a6aee]` | Hover on accent |
| `PANEL.accentText` | `text-[#4a7eff]` | Accent-colored text |
| `PANEL.accentBg` | `bg-[#4a7eff]/10` | Subtle accent background |
| `PANEL.accentBorder` | `border-[#4a7eff]` | Accent border |
| `PANEL.accentBorderSubtle` | `border-[#4a7eff]/30` | Subtle accent border |
| `PANEL.label` | `text-gray-400 text-sm` | Control labels |
| `PANEL.labelFixed` | `text-gray-400 text-sm w-20 shrink-0` | Fixed-width labels |
| `PANEL.sublabel` | `text-gray-500 text-xs` | Sub-labels, descriptions |
| `PANEL.heading` | `text-white text-base font-semibold` | Section headings |
| `PANEL.headingSm` | `text-white text-sm font-semibold` | Small section headings |
| `PANEL.value` | `text-white text-sm` | Display values |
| `PANEL.border` | `border-white/5` | Section dividers |
| `PANEL.borderSurface` | `border-[#3a3a3a]` | Surface borders |
| `PANEL.focusRing` | `focus:outline-none focus:ring-1 focus:ring-[#4a7eff]` | Focus rings |
| `PANEL.input` | `bg-[#2a2a2a] text-white text-sm px-3 py-2 rounded-lg ...` | Text inputs |
| `PANEL.toggleOn` | `bg-[#4a7eff]` | Toggle on state |
| `PANEL.toggleOff` | `bg-[#3a3a3a]` | Toggle off state |
| `PANEL.btnPrimary` | `bg-[#4a7eff] text-white hover:bg-[#3a6aee]` | Primary buttons |
| `PANEL.btnSecondary` | `bg-[#2a2a2a] text-white hover:bg-[#3a3a3a]` | Secondary buttons |
| `PANEL.btnDestructive` | `bg-red-600/10 text-red-400 hover:bg-red-600/20` | Destructive buttons |
| `PANEL.btnAccent` | `bg-[#4a7eff]/10 text-[#4a7eff] border ...` | Accent outline buttons |
| `PANEL.section` | `border-b border-white/5` | Section dividers |

## Color Palette (DO NOT deviate)

### Surfaces
| Use | Class | Hex |
|-----|-------|-----|
| Input/secondary bg | `bg-[#2a2a2a]` | #2a2a2a |
| Hover bg | `bg-[#3a3a3a]` | #3a3a3a |
| Dark preview areas | `bg-[#1e1e1e]` | #1e1e1e |
| Alt dark bg | `bg-zinc-900` | -- |

### Accent
| Use | Class |
|-----|-------|
| Active/primary | `bg-[#4a7eff]` |
| Hover | `hover:bg-[#3a6aee]` |
| Subtle bg | `bg-[#4a7eff]/10` |
| Active text | `text-[#4a7eff]` |

### Text
| Use | Class |
|-----|-------|
| Headings/values | `text-white` |
| Labels | `text-gray-400` |
| Sublabels | `text-gray-500` or `text-gray-600` |
| Muted | `text-zinc-500` |

### Status
| State | Background | Text | Border |
|-------|-----------|------|--------|
| Success/Active | `bg-green-500` | `text-green-500` | `border-green-500/30` |
| Warning | `bg-yellow-500/10` | `text-yellow-400` | -- |
| Error | `bg-red-600/10` | `text-red-400` | `border-red-500/40` |
| Info | `bg-blue-500/10` | `text-blue-300` | -- |

### Borders
| Use | Class |
|-----|-------|
| Subtle divider | `border-white/5` |
| Medium divider | `border-white/10` |
| Input border | `border-zinc-700` |
| Surface border | `border-[#3a3a3a]` |

## Icon System

**Library:** Lucide React (`lucide-react`)

```typescript
import { IconName } from 'lucide-react'
```

- Common sizes: `size={14}` (small), `size={16}` (default), `size={18}` (medium), `size={20}` (large)
- Icon props typed as `LucideIcon`
- NEVER use any other icon library

## Panel Component Pattern

**Every panel MUST follow this structure:**

```tsx
import { PanelLayout } from '@/components/ui/PanelHeader'
import { PanelSection } from '@/components/ui/panel-controls/PanelSection'
import { PanelInput } from '@/components/ui/panel-controls/PanelInput'
import { PanelActionButton } from '@/components/ui/panel-controls/PanelActionButton'
import { PANEL } from '@/components/ui/panel-controls/tokens'

export function MyPanel() {
  return (
    <PanelLayout icon={IconName} title="Panel Title" footer={<PanelActionButton variant="primary">Action</PanelActionButton>}>
      <PanelSection title="Section">
        <PanelInput label="Name" value={name} onChange={setName} />
        <PanelSlider label="Amount" value={amount} onChange={setAmount} min={0} max={100} />
        <PanelToggle label="Enabled" checked={enabled} onChange={setEnabled} />
      </PanelSection>

      <PanelSection title="Advanced" collapsible defaultOpen={false} icon={Settings}>
        <PanelSlider label="Fine tune" value={val} onChange={setVal} min={0} max={100} />
      </PanelSection>
    </PanelLayout>
  )
}
```

## Utility: `cn()` for className merging

```typescript
import { cn } from '@/lib/utils'

// Always use cn() for conditional classes
<div className={cn('base-classes', isActive && 'active-classes', className)} />
```

## Property-to-Control Mapping (MANDATORY)

When implementing a property control, use the CANONICAL control for that property type.

### Numeric Properties
| Property | Canonical Control | Notes |
|----------|------------------|-------|
| Font size, position, scale, rotation, opacity, volume, speed, duration, border radius/width, blur, letter spacing, line height, padding/margin | `DraggableNumberInput` | With appropriate suffix (px, %, x, s) |

**Rule: ANY numeric property** that a user fine-tunes uses `DraggableNumberInput`. Never use `PanelSlider` for numeric properties with units.

**Exception:** `PanelSlider` is acceptable ONLY for coarse "feel" controls in generation/AI panels (e.g., "creativity level") where the property has no unit.

### Boolean Properties
| Property | Canonical Control |
|----------|------------------|
| Any on/off setting (visible, loop, muted, enabled) | `PanelToggle` |
| Multi-select options | `PanelCheckbox` |

### Choice Properties
| Property | Canonical Control |
|----------|------------------|
| Font family, easing type, 5+ options | `PanelSelect` |
| Blend mode | `BlendModeSelector` |
| 2-4 exclusive options | `PanelButtonGroup` |
| Multiple selections | `PanelMultiSelect` |

### Color, Text, File Properties
| Property | Canonical Control |
|----------|------------------|
| Any color | `ColorPicker` |
| Color palette | `PanelColorSwatches` |
| Short text | `PanelInput` |
| Long text / prompt | `PanelTextarea` |
| Search / filter | `PanelSearchInput` |
| File upload | `PanelDropZone` |

### Section Structure
| Element | Canonical Control |
|---------|------------------|
| Section with title | `PanelSection` (use `collapsible` for progressive disclosure) |
| Panel wrapper | `PanelLayout` (from `@/components/ui/PanelHeader`) |
| Sub-tabs within panel | `PanelCategoryTabs` |

### Error / Feedback
| Situation | Canonical Control |
|-----------|------------------|
| Operation success/failure | `useToastStore` toast |
| Inline validation error | `<span className="text-red-400 text-xs mt-1">` |
| Loading | `LoadingSpinner` or `Loader2` with `animate-spin` |
| Progress | `<div className="h-1 bg-[#4a7eff] rounded-full">` |

## Common Anti-Patterns (NEVER DO)

1. Creating a new button when `PanelActionButton` or `IconButton` exists
2. Hardcoding `bg-[#4a7eff]` instead of using `PANEL.accent` or `PANEL.btnPrimary`
3. Creating a new spinner/loader instead of using `LoadingSpinner`
4. Creating a new toggle instead of using `PanelToggle`
5. Creating a new select/dropdown instead of using `PanelSelect` or `PanelMultiSelect`
6. Using a slider for numeric properties that belong in `DraggableNumberInput`
7. Using `bg-gray-800` instead of `bg-[#2a2a2a]` (wrong color)
8. Using `bg-blue-500` instead of `bg-[#4a7eff]` (wrong accent)
9. Using inline hex colors that don't match the palette
10. Creating a new toast/notification instead of using `useToastStore`
11. Writing a new search input instead of using `PanelSearchInput`
12. Building a new drag-drop zone instead of using `PanelDropZone`
13. Importing icons from any library other than `lucide-react`
14. Using `RPSlider` in property panels (legacy RightPanel component)
15. Importing `PanelLayout` from wrong path (correct: `@/components/ui/PanelHeader`)
16. Rolling your own collapsible section with useState + ChevronDown/ChevronUp instead of using `PanelSection collapsible`
17. Using domain-specific accent colors (amber, sky, emerald, purple) instead of `#4a7eff`

## When to Create a NEW Component

Only create a new component in `src/components/ui/` when:
1. No existing component handles the use case
2. The element will be reused across 2+ panels
3. It follows the design tokens and color palette above
4. It's added to this registry (update this SKILL.md)

For one-off UI that's specific to a single panel, build it inline using the design tokens -- but still use existing sub-components (PanelActionButton, etc.) within it.
