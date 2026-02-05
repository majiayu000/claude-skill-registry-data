---
name: opentui
description: Build terminal user interfaces with OpenTUI (@opentui/core). Use when creating TUI apps, terminal dashboards, CLI interfaces, or working with OpenTUI renderables, constructs, keyboard handling, or Yoga flexbox layouts in the terminal.
---

# OpenTUI Development

TypeScript library for building terminal UIs. Uses Yoga (flexbox) for layout. Requires Bun runtime.

## Installation

```bash
bun add @opentui/core
```

Requires [Zig](https://ziglang.org/learn/getting-started/) installed for native modules.

## Basic Setup

```typescript
import { createCliRenderer, TextRenderable, BoxRenderable } from "@opentui/core"

const renderer = await createCliRenderer({
  exitOnCtrlC: true,
  targetFps: 30,
})

const text = new TextRenderable(renderer, {
  id: "greeting",
  content: "Hello, OpenTUI!",
  fg: "#00FF00",
})
renderer.root.add(text)

renderer.start()
```

## Two API Styles

### Imperative (Renderables)

Direct instances with `RenderContext`. Mutate state via setters.

```typescript
const box = new BoxRenderable(renderer, { id: "panel", width: 30, height: 10 })
renderer.root.add(box)
box.backgroundColor = "#444477"  // Mutate directly
```

### Declarative (Constructs/VNodes)

Functional composition returning VNodes. Instantiated when added to root.

```typescript
import { Text, Box, Input, delegate } from "@opentui/core"

function LabeledInput(props: { id: string; label: string }) {
  return delegate(
    { focus: `${props.id}-input` },
    Box(
      { flexDirection: "row" },
      Text({ content: props.label }),
      Input({ id: `${props.id}-input`, width: 20 })
    )
  )
}

renderer.root.add(Box({ padding: 1 }, LabeledInput({ id: "name", label: "Name: " })))
```

## Core Renderables

| Renderable | Purpose |
|------------|---------|
| `TextRenderable` | Styled text with attributes (bold, underline, colors) |
| `BoxRenderable` | Container with border, background, title |
| `InputRenderable` | Text input with cursor, placeholder, events |
| `SelectRenderable` | Scrollable list selection (up/down/j/k) |
| `TabSelectRenderable` | Horizontal tab selection (left/right) |
| `GroupRenderable` | Invisible layout container |

See [references/renderables.md](references/renderables.md) for full API and examples.

## Layout (Quick Reference)

```typescript
{
  flexDirection: "row" | "column",
  justifyContent: "flex-start" | "center" | "flex-end" | "space-between",
  alignItems: "flex-start" | "center" | "flex-end" | "stretch",
  width: 30 | "100%" | "auto",
  height: 10,
  padding: 1,
  margin: 1,
  position: "relative" | "absolute",
  zIndex: 100,
}
```

See [references/layout.md](references/layout.md) for complete flexbox reference.

## Input & Focus (Quick Reference)

```typescript
// Keyboard
renderer.keyInput.on("keypress", (key) => {
  if (key.name === "escape") modal.visible = false
  if (key.ctrl && key.name === "q") renderer.exit()
})

// Focus
input.focus()
input.blur()
input.on(RenderableEvents.FOCUSED, () => {})
```

See [references/input-focus.md](references/input-focus.md) for keyboard events, colors, lifecycle.

## Common Patterns

See [references/patterns.md](references/patterns.md) for:
- Modal dialogs
- Form tab navigation
- Responsive layouts
- Loading states
- Confirmation dialogs
- Status bars

## Framework Integrations

```bash
bun add @opentui/react   # React reconciler
bun add @opentui/solid   # SolidJS reconciler
```

## Resources

- [GitHub](https://github.com/sst/opentui)
- [Examples](https://github.com/sst/opentui/tree/main/packages/core/src/examples)
- [Awesome OpenTUI](https://github.com/msmps/awesome-opentui)
