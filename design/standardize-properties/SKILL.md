---
name: standardize-properties
description: Enforce Cinema design tokens and PanelSlider usage in all right-panel property editors. Use when creating or modifying any property panel, transform controls, or settings UI in the right panel.
user-invocable: true
---

# Standardize Properties Panel

Right-panel property editors MUST use the existing `PanelSlider` component from `@/components/ui/panel-controls`. NEVER create custom input components (InlineInput, NumberInput, custom drag handlers, etc.) — PanelSlider already handles pointer-lock drag, double-click edit, wheel scroll, shift-for-precision, and Cinema styling.

## Rules

### 1. Always use PanelSlider

```tsx
import { PanelSlider } from '@/components/ui/panel-controls'

// Label on the left, pill on the right (default)
<PanelSlider label="Opacity" value={opacity} onChange={setOpacity} min={0} max={100} step={1} suffix="%" />

// Label INSIDE the pill (for compact side-by-side layout)
<PanelSlider label="x" value={x} onChange={setX} min={-2000} max={2000} step={1} suffix="px" inline />
```

### 2. Side-by-side grouped inputs

When two values belong together (x/y, w/h), put a row label on the left and two `inline` PanelSliders side by side:

```tsx
<div className="flex items-center gap-3 mb-1">
  <span className="text-gray-400 text-sm shrink-0 w-16">Position</span>
  <div className="flex-1 flex gap-1.5">
    <PanelSlider label="x" value={x} onChange={setX} min={-2000} max={2000} step={1} suffix="px" inline className="flex-1" />
    <PanelSlider label="y" value={y} onChange={setY} min={-2000} max={2000} step={1} suffix="px" inline className="flex-1" />
  </div>
</div>
```

### 3. Cinema design tokens

| Token | Value | Usage |
|-------|-------|-------|
| Pill bg | `bg-[#2a2a2a]` | PanelSlider default (built in) |
| Pill hover | `hover:bg-[#333]` | PanelSlider hover (built in) |
| Pill active ring | `ring-1 ring-[#4a7eff]` | During drag (built in) |
| Label color | `text-gray-400` | Row labels (built in) |
| Value color | `text-white` | Values (built in) |
| Suffix color | `text-gray-500` | px, %, ° (built in) |
| Row border | `border-white/5` | Section dividers |
| Accent | `#4a7eff` | Active states, lock icon |
| Collapsible header | `bg-[#2a2a2a] hover:bg-[#3a3a3a]` | Expandable section headers |

### 4. Collapsible sections use thick Cinema rows

```tsx
<div className="rounded-lg overflow-hidden border border-white/5">
  <div
    onClick={() => setExpanded(!expanded)}
    className="w-full flex items-center gap-2 px-3 py-2.5 bg-[#2a2a2a] hover:bg-[#3a3a3a] cursor-pointer"
  >
    {expanded ? <ChevronDown size={14} /> : <ChevronRight size={14} />}
    <span className="text-xs font-medium text-gray-200">{label}</span>
  </div>
  {expanded && <div className="px-3 py-2.5">...</div>}
</div>
```

### 5. Empty states

```tsx
<div className="flex flex-col items-center justify-center py-16 text-gray-600">
  <Icon size={28} className="mb-3" />
  <span className="text-sm text-gray-400">No item selected</span>
  <span className="text-xs text-gray-600 mt-1">Select one on the canvas</span>
</div>
```

### 6. Toggle buttons must match input field dimensions

Toggles (Visible/Hidden, On/Off) must be the same width and height as PanelSlider pills. Use a full-width row with the same label width as sliders — never a small pill floating next to a label:

```tsx
<PanelSlider label="Opacity" value={opacity} onChange={setOpacity} min={0} max={100} step={1} suffix="%" />
{/* Visible toggle — same row height and pill width as PanelSlider above */}
<div className="flex items-center h-[36px]">
  <span className="text-gray-400 text-sm shrink-0 w-20">Visible</span>
  <button
    onClick={toggleVisible}
    className={cn(
      'flex-1 h-[28px] rounded-md text-xs font-medium transition-colors',
      visible ? 'bg-accent/10 text-accent' : 'bg-[#2a2a2a] text-gray-500',
    )}
  >
    {visible ? 'Visible' : 'Hidden'}
  </button>
</div>
```

### 7. No redundant section titles

If a section's content is already inside a collapsible header, do NOT add a separate `<h2>` title above it — the collapsible header IS the title. Only use `<h2>` titles for non-collapsible sections that have no other header.

### 8. Don't duplicate navigation from other panels

If items are already listed elsewhere (e.g., layers panel, timeline tracks), do NOT add a "Other X" switcher list in the properties panel. The right panel shows properties for the selected item — it does not need to replicate item navigation.

### 9. Action buttons sticky at bottom

Destructive actions (Remove, Delete) go in a sticky footer pinned to the panel bottom with `mt-auto`. Never inline them in scrollable content. Keep text short: "Remove" not "Remove from Canvas".

```tsx
{/* Sticky bottom action */}
<div className="mt-auto p-4 border-t border-white/5">
  <button className="w-full py-2 rounded-lg text-xs font-medium bg-red-500/10 text-red-400 hover:bg-red-500/20 transition-colors flex items-center justify-center gap-2">
    <Trash2 size={12} />
    Remove
  </button>
</div>
```

## What NOT to do

- **NEVER** create custom number inputs, inline inputs, or drag-to-scrub components
- **NEVER** use raw `<input type="number">` — always PanelSlider
- **NEVER** use PanelSelect for numeric values — PanelSlider handles those
- **NEVER** use custom font-mono styled spans for values
- **NEVER** skip the `suffix` prop — always show units (px, %, °, etc.)
- **NEVER** use `compact` when `inline` is what you need (compact just removes label width, inline puts label inside pill)
- **NEVER** add toggle buttons that are smaller than adjacent input fields — match dimensions
- **NEVER** add redundant section titles above collapsible headers
- **NEVER** duplicate item lists that already exist in layers/timeline panels
- **NEVER** inline destructive action buttons in scrollable content — always sticky bottom

## Reference implementations

- `PartTransformControls.tsx` — Position (x/y inline), Scale (w/h inline + lock), Rotation, Z-Index
- `MediaPropertiesPanel.tsx` — Opacity, blur, brightness sliders
- `TextPropertiesPanel.tsx` — Font size, letter spacing, line height
- `ShapePropertiesPanel.tsx` — Corner radius, stroke width
- `MotionGraphicPropertiesPanel.tsx` — Uniform slider widths, sticky Remove, no redundant lists
