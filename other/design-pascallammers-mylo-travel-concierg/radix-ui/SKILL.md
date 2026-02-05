---
name: radix-ui
description: Use for accessible React primitives when shadcn doesn't have the component you need
---

# Radix UI Primitives

## When to Use

Use Radix directly when:
- shadcn doesn't have the component you need
- You need lower-level control over accessibility behavior
- Building custom compound components with full a11y support

**Check shadcn first** - most Radix primitives have styled shadcn wrappers.

## Installation

```bash
npm install @radix-ui/<primitive>

# Examples:
npm install @radix-ui/react-toggle
npm install @radix-ui/react-toggle-group
npm install @radix-ui/react-toolbar
```

## Primitives NOT in shadcn

These Radix primitives don't have direct shadcn equivalents:

| Primitive | Use Case |
|-----------|----------|
| `toggle` | Single on/off toggle button |
| `toggle-group` | Mutually exclusive toggle buttons |
| `toolbar` | Accessible toolbar containers |
| `visually-hidden` | Screen-reader-only content |
| `portal` | Render children in document.body |
| `slot` | Merge props onto child element |
| `direction-provider` | RTL/LTR direction context |
| `accessible-icon` | Icon with accessible label |

## Usage Patterns

### Toggle

```tsx
import * as Toggle from "@radix-ui/react-toggle"

<Toggle.Root
  pressed={pressed}
  onPressedChange={setPressed}
  className="rounded p-2 data-[state=on]:bg-primary"
>
  {pressed ? <BoldIcon /> : <BoldOffIcon />}
</Toggle.Root>
```

### Toggle Group

```tsx
import * as ToggleGroup from "@radix-ui/react-toggle-group"

<ToggleGroup.Root type="single" value={value} onValueChange={setValue}>
  <ToggleGroup.Item value="left" className="...">
    <AlignLeftIcon />
  </ToggleGroup.Item>
  <ToggleGroup.Item value="center" className="...">
    <AlignCenterIcon />
  </ToggleGroup.Item>
  <ToggleGroup.Item value="right" className="...">
    <AlignRightIcon />
  </ToggleGroup.Item>
</ToggleGroup.Root>
```

### Toolbar

```tsx
import * as Toolbar from "@radix-ui/react-toolbar"

<Toolbar.Root className="flex gap-2 p-2 border rounded">
  <Toolbar.Button className="...">Bold</Toolbar.Button>
  <Toolbar.Separator className="w-px bg-border" />
  <Toolbar.Link href="/help">Help</Toolbar.Link>
  <Toolbar.ToggleGroup type="single">
    <Toolbar.ToggleItem value="left">Left</Toolbar.ToggleItem>
    <Toolbar.ToggleItem value="center">Center</Toolbar.ToggleItem>
  </Toolbar.ToggleGroup>
</Toolbar.Root>
```

### Visually Hidden

```tsx
import * as VisuallyHidden from "@radix-ui/react-visually-hidden"

<button>
  <GearIcon />
  <VisuallyHidden.Root>Settings</VisuallyHidden.Root>
</button>
```

## Styling Radix Components

Radix uses `data-*` attributes for state styling:

```tsx
// State attributes
data-[state=open]:bg-accent
data-[state=closed]:opacity-0
data-[state=on]:bg-primary
data-[state=off]:bg-muted
data-[disabled]:opacity-50
data-[highlighted]:bg-accent

// Orientation
data-[orientation=horizontal]:flex-row
data-[orientation=vertical]:flex-col

// Side (for positioned elements)
data-[side=top]:animate-slideDown
data-[side=bottom]:animate-slideUp
```

## Composition Pattern

Radix primitives are composable. Build complex components from simple parts:

```tsx
import * as Toolbar from "@radix-ui/react-toolbar"
import * as ToggleGroup from "@radix-ui/react-toggle-group"
import * as Tooltip from "@radix-ui/react-tooltip"

// Combine toolbar with tooltips on each button
<Toolbar.Root>
  <Tooltip.Provider>
    <Tooltip.Root>
      <Tooltip.Trigger asChild>
        <Toolbar.Button>Bold</Toolbar.Button>
      </Tooltip.Trigger>
      <Tooltip.Content>Make text bold</Tooltip.Content>
    </Tooltip.Root>
  </Tooltip.Provider>
</Toolbar.Root>
```

## Key Props

| Prop | Description |
|------|-------------|
| `asChild` | Merge props onto child element instead of rendering wrapper |
| `forceMount` | Keep in DOM even when closed (for animations) |
| `defaultOpen` / `open` | Uncontrolled / controlled open state |
| `onOpenChange` | Callback when open state changes |
| `modal` | Whether to trap focus (dialogs) |
