---
name: ui-design
description: ProAnimate UI/UX design principles, visual hierarchy, spacing, animation, and accessibility. Auto-applied when creating or modifying UI components, panels, modals, or landing pages.
user-invocable: false
---

# ProAnimate UI/UX Design System

## Design Tokens

All editor UI uses the `PANEL` token object from `src/components/ui/panel-controls/tokens.ts`.

### Color Palette (Dark Theme)

| Role | Hex | Tailwind | When to use |
|------|-----|----------|-------------|
| Surface | #2a2a2a | `bg-[#2a2a2a]` | Input backgrounds, secondary areas |
| Surface Hover | #3a3a3a | `bg-[#3a3a3a]` | Hover states, active surfaces |
| Canvas BG | #1e1e1e | `bg-[#1e1e1e]` | Canvas area, dark preview |
| Accent | #4a7eff | `bg-[#4a7eff]` | Primary buttons, active states, focus rings |
| Accent Hover | #3a6aee | `hover:bg-[#3a6aee]` | Button hover |
| Text Primary | white | `text-white` | Headings, values, primary content |
| Text Secondary | gray-400 | `text-gray-400` | Labels, descriptions |
| Text Tertiary | gray-500 | `text-gray-500` | Sublabels, hints, timestamps |
| Destructive | red-600/10 | `bg-red-600/10 text-red-400` | Delete, remove, dangerous actions |
| Success | green-500 | `text-green-500` | Active indicators, success states |
| Border Subtle | white/5 | `border-white/5` | Dividers between sections |
| Border Medium | #3a3a3a | `border-[#3a3a3a]` | Surface borders, panels |

**Never use raw Tailwind colors (bg-blue-500, text-gray-300). Always use the palette above.**

**Domain-specific accent colors are NOT allowed.** All panels use `#4a7eff` as the accent. Do not use amber, sky, emerald, purple, or any other Tailwind color as a panel-specific accent. The only accent is `#4a7eff`.

### Typography

| Level | Classes | Use |
|-------|---------|-----|
| Heading | `text-white text-base font-semibold` | Panel titles, section headers |
| Label | `text-gray-400 text-sm` | Input labels, property names |
| Sublabel | `text-gray-500 text-xs` | Hints, secondary info |
| Value | `text-white text-sm` | Input values, numbers |
| Body | `text-gray-300 text-sm` | Descriptions, help text |

Font: Inter (sans-serif). No other fonts in the editor.

### Spacing

| Context | Value | Example |
|---------|-------|---------|
| Panel header padding | `p-3` | `<div className="p-3 min-h-[49px]">` |
| Panel body padding | `px-4 py-3` | Section content |
| Panel footer | `px-4 py-3 border-t border-white/5` | Sticky at bottom |
| Between controls | `gap-2` | Vertical stack of inputs |
| Between sections | `gap-4` | Between PanelSection groups |
| Tight inline | `gap-1.5` | Icon + label pairs |

### Elevation / Shadows

| Level | Use | Classes |
|-------|-----|---------|
| Flat | Default surfaces | No shadow |
| Glass | Overlays, landing cards | `backdrop-blur-lg bg-white/5` |
| Glow | CTAs, accent highlights | `shadow-glow` (defined in tailwind config) |

## Component Rules

### Panel Pattern (Mandatory for all right-panel views)
```tsx
<PanelLayout icon={IconName} title="Title" footer={<PanelActionButton>Save</PanelActionButton>}>
  <PanelSection title="Section Name">
    <PanelInput label="Name" />
    <PanelToggle label="Enabled" />
    <DraggableNumberInput label="Size" />
  </PanelSection>
</PanelLayout>
```

### Button Hierarchy
1. **PanelActionButton variant="primary"** — One per panel footer. The main action.
2. **PanelActionButton variant="secondary"** — Supporting actions in footer.
3. **IconButton variant="ghost"** — Toolbar actions, inline toggles.
4. **PanelActionButton variant="destructive"** — Delete/remove, always requires confirmation.

Never create a raw `<button>`. Always use PanelActionButton or IconButton.

### Input Mapping
| Data type | Component | Why |
|-----------|-----------|-----|
| Number | `DraggableNumberInput` | Drag-to-change + direct input + formula mode |
| Boolean | `PanelToggle` | Switch with label + optional description |
| Selection | `PanelSelect` | Dropdown with label |
| Color | `ColorPicker` | HSV wheel + hex input + eyedropper |
| Text | `PanelInput` | Single line with label |
| Long text | `PanelTextarea` | Multi-line with label |
| Range | `PanelSlider` | Slider with label + value display |

### Modals and Overlays
- Use `backdrop-blur-lg bg-black/50` for overlay backdrop
- Modal card: `bg-[#2a2a2a] rounded-lg border border-white/10 shadow-xl`
- Max width: `max-w-md` for confirmations, `max-w-2xl` for complex modals
- Always include close button (X icon, top-right) and Escape key handler
- Focus trap: first focusable element on open, return focus on close

## Visual Hierarchy Principles

1. **One primary action per view.** If a panel has multiple buttons, only one should be accent-colored.
2. **Labels above, not beside.** All form controls stack vertically with labels on top.
3. **Progressive disclosure.** Use `PanelSection collapsible defaultOpen={false}` for advanced/secondary options. Primary controls should be visible by default (`defaultOpen={true}`). The motto: simple at first glance — features appear when users need them.
4. **Empty states matter.** When a list is empty, show icon + message + action button, not blank space.
5. **Loading states.** Use skeleton placeholders for async content, spinner for actions, progress bar for exports.

## Animation / Motion

| Interaction | Duration | Easing | Implementation |
|-------------|----------|--------|----------------|
| Hover state | 150ms | ease-out | `transition-colors duration-150` |
| Panel open/close | 200ms | ease-in-out | `transition-all duration-200` |
| Modal appear | 200ms | ease-out | Scale from 95% + fade |
| Toast notification | 300ms in, 200ms out | ease-out | Slide from bottom-right |
| Skeleton pulse | 1.5s | ease-in-out | `animate-pulse` |

**No animation should exceed 300ms.** Users of professional tools want speed, not flourish.
**Respect `prefers-reduced-motion`.** Wrap all motion in `motion-safe:` Tailwind prefix.

## Accessibility Requirements

1. **All interactive elements need focus rings.** Use `focus:ring-1 focus:ring-[#4a7eff] focus:ring-offset-1 focus:ring-offset-[#1e1e1e]`.
2. **All icon-only buttons need `aria-label`.** Example: `<IconButton aria-label="Delete layer" icon={Trash2} />`.
3. **Color alone cannot convey state.** Error states need text + icon, not just red color.
4. **Keyboard navigation.** Arrow keys for lists, Tab for form controls, Escape to close overlays.
5. **Screen reader announcements.** Use `aria-live="polite"` for toast notifications and status changes.

## Landing Page vs Editor

The landing page uses a different visual language:

| Aspect | Editor | Landing Page |
|--------|--------|-------------|
| Background | `#1e1e1e` solid | Gradient + grid pattern |
| Cards | `bg-[#2a2a2a]` flat | `GlassCard` (backdrop-blur) |
| Buttons | `PanelActionButton` | `GlowButton` (glow shadow) |
| Typography | Inter, functional | Inter, larger, more whitespace |
| Animation | Minimal, fast | Allowed: float, glow-pulse, fade-in |

When creating landing page components, use the glass/glow design language. When creating editor components, use the flat/token design language. Never mix them.

## Panel Architecture (Mandatory)

### Left Panels
- **DO NOT use PanelLayout.** Left panels use raw `div` structure. The group header (`< Panel Name >`) is provided by LeftPanel.tsx automatically.
- **Animated icon tab bar** for sub-navigation — same pattern as MediaPanel. White pill for active tab, gray icons for inactive. Use the exact animation code from MediaPanel (flex transition, cubic-bezier).
- **Search bar** below tab bar with filter icon button. Filter icon toggles category pills. If ANY tab has filters, ALL tabs must have filters.
- **Full-width thick rows** for item lists — never grids. `px-3 py-2.5 rounded-lg border`. All rows same height.
- **Reference panel:** MediaPanel is the gold standard for left panel structure.

### Right Panels
- **Arrow header** matching CharacterSectionHeader — `< Name >` with ChevronLeft/ChevronRight buttons.
- **Animated TabNavigation pills** below header for section filtering (Transform, Camera, Optical, etc.).
- **Input alignment** — all PanelSlider labels use fixed `w-20`. Never use `compact`. Every input must start at the same horizontal position.
- **Dropdowns (PanelSelect)** — expand leftward to fit longest text. No truncation in dropdown options. Thick rows matching trigger height.
- **Feature toggles** — use PanelToggle on/off to show/hide control groups. Never "Add X" buttons with empty states.
- **Multi-option controls** — use PanelMultiSelect dropdown, never exposed checkboxes.
- **Metadata** — show specs inside dropdown option text in parentheses, not as subtitles below.
- **Reference panel:** Character right panel is the gold standard for right panel structure.

### Consistency Rules
1. **Same pattern everywhere** — if one tab has filters, all tabs have filters. If one section uses thick rows, all sections use thick rows.
2. **Symmetric layouts** — same card sizes, same row heights, same input widths, same spacing. Asymmetry is a bug.
3. **One purpose per panel** — left = browse/pick, right = fine-tune. Never mix concerns.
4. **No domain-specific colors** — everything uses `#4a7eff`. No amber, sky, emerald, purple.
5. **Category pills** — horizontal scroll with `shrink-0`, never `flex-1` squish.
