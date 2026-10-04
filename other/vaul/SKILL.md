---
name: Vaul
description: Drawer component for React by Emil Kowalski — bottom sheets, snap points, nested drawers, clean API
---

Vaul is a drawer (bottom sheet) component for React by Emil Kowalski. Use it for mobile-style slide-up panels, settings sheets, and contextual actions.

## Installation

```bash
npm install vaul
# or
pnpm i vaul
```

## Basic Usage

```tsx
'use client';
import { Drawer } from 'vaul';

export function MyDrawer() {
  return (
    <Drawer.Root>
      <Drawer.Trigger asChild>
        <button>Open</button>
      </Drawer.Trigger>
      <Drawer.Portal>
        <Drawer.Overlay className="fixed inset-0 bg-black/40" />
        <Drawer.Content className="bg-white flex flex-col rounded-t-[10px] h-full mt-24 fixed bottom-0 left-0 right-0">
          <div className="p-4 bg-white rounded-t-[10px] flex-1">
            <div className="mx-auto w-12 h-1.5 flex-shrink-0 rounded-full bg-gray-300 mb-8" />
            <h2 className="text-lg font-semibold">Title</h2>
            <p>Content goes here.</p>
          </div>
        </Drawer.Content>
      </Drawer.Portal>
    </Drawer.Root>
  );
}
```

## Components API

| Component | Description |
|-----------|-------------|
| `Drawer.Root` | Root state manager |
| `Drawer.Trigger` | Opens the drawer |
| `Drawer.Portal` | Renders outside DOM tree |
| `Drawer.Overlay` | Backdrop |
| `Drawer.Content` | The drawer panel |
| `Drawer.Title` | Accessible title |
| `Drawer.Description` | Accessible description |
| `Drawer.Close` | Close trigger |

## Drawer.Root Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `open` | boolean | — | Controlled open state |
| `onOpenChange` | function | — | State change callback |
| `defaultOpen` | boolean | false | Uncontrolled default |
| `snapPoints` | (string\|number)[] | — | Snap positions |
| `activeSnapPoint` | string\|number | — | Controlled snap |
| `setActiveSnapPoint` | function | — | Snap change callback |
| `direction` | string | `bottom` | `top` `right` `left` `bottom` |
| `dismissible` | boolean | true | Allow drag-to-close |
| `shouldScaleBackground` | boolean | false | Scale page behind drawer |
| `modal` | boolean | true | Block background interaction |
| `onClose` | function | — | On close callback |
| `fadeFromIndex` | number | — | Snap fade index |

## Snap Points

```tsx
<Drawer.Root snapPoints={['148px', '355px', 1]} fadeFromIndex={2}>
  {/* 1 = 100% height */}
</Drawer.Root>
```

## Controlled State

```tsx
const [open, setOpen] = React.useState(false);

<Drawer.Root open={open} onOpenChange={setOpen}>
  <Drawer.Trigger onClick={() => setOpen(true)}>Open</Drawer.Trigger>
  ...
  <Drawer.Close onClick={() => setOpen(false)}>Close</Drawer.Close>
</Drawer.Root>
```

## Direction Variants

```tsx
// Side drawer (right panel)
<Drawer.Root direction="right">
  <Drawer.Content className="fixed right-0 top-0 h-full w-[400px]">
    ...
  </Drawer.Content>
</Drawer.Root>
```

## Scale Background (iOS-style)

```tsx
// Add to body wrapper
<div vaul-drawer-wrapper="">
  <App />
</div>

// Enable on drawer
<Drawer.Root shouldScaleBackground>
```

## Nested Drawers

```tsx
<Drawer.Root>
  <Drawer.Trigger>Open</Drawer.Trigger>
  <Drawer.Portal>
    <Drawer.Content>
      <Drawer.Root nested>
        <Drawer.Trigger>Open nested</Drawer.Trigger>
        <Drawer.Portal>
          <Drawer.Content>Nested content</Drawer.Content>
        </Drawer.Portal>
      </Drawer.Root>
    </Drawer.Content>
  </Drawer.Portal>
</Drawer.Root>
```

## Clean Code Rules

- Always add `<div className="mx-auto w-12 h-1.5 rounded-full bg-gray-300 mb-8" />` drag handle at top
- Use `shouldScaleBackground` for immersive mobile-like feel (requires `vaul-drawer-wrapper` on body)
- Use `direction="right"` for settings/filter panels, `direction="bottom"` for actions
- Combine with Sonner for toast feedback on drawer actions
- Keep drawer content scrollable: use `overflow-y-auto` on the inner content div
