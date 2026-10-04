---
name: "Stack: OpenTUI"
description: "OpenTUI terminal UI library reference: @opentui/core, terminal UIs, renderables, Yoga layouts, Zig-native rendering."
when_to_use: "When building or debugging a terminal UI with @opentui/core: renderable composition, Yoga layout issues or anything touching the Zig-native rendering layer."
user-invocable: false
metadata:
  family: clod-stack
allowed-tools: ["Read", "Glob", "Grep"]
---

# OpenTUI Operative

> Comprehensive reference for building terminal UIs with OpenTUI (@opentui/core).
> Source: https://opentui.com/docs/, all 29 documentation pages.

## Trigger

Use when: user mentions "OpenTUI", "TUI", "terminal UI", "@opentui/core", renderables, or works on files importing from `@opentui/core`. No `paths:` glob is set: OpenTUI code has no distinctive file extension (it's ordinary `.ts`/`.tsx` importing from the package), so keyword/import-based triggering is more reliable than a path pattern here.

## Role

You are an expert in OpenTUI, a TypeScript library for building rich terminal interfaces with Yoga-powered flexbox layouts and Zig-native rendering. You know every API surface, every gotcha and every pattern. You write correct OpenTUI code on the first attempt.

## 1. Quick Start

**Requires Bun.**

```bash
bun add @opentui/core
```

```typescript
import { createCliRenderer, Text } from "@opentui/core"

const renderer = await createCliRenderer({ exitOnCtrlC: true })
renderer.root.add(Text({ content: "Hello, OpenTUI!", fg: "#00FF00" }))
```

Run with `bun index.ts`. Press Ctrl+C to exit.

## 2. Renderer

The `CliRenderer` drives everything: terminal output, input events, render loop and context for renderables.

### Creation

```typescript
import { createCliRenderer } from "@opentui/core"

const renderer = await createCliRenderer({
  exitOnCtrlC: true,   // default: true
  targetFps: 30,       // default: 30
})
```

The factory:
1. Loads the native Zig rendering library
2. Configures terminal (mouse, keyboard protocol, alternate screen)
3. Returns an initialised `CliRenderer`

### Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `exitOnCtrlC` | `boolean` | `true` | Destroy renderer on Ctrl+C |
| `exitSignals` | `NodeJS.Signals[]` | (none) | Signals that trigger cleanup |
| `targetFps` | `number` | `30` | Target FPS for render loop |
| `maxFps` | `number` | `60` | Max FPS for immediate re-renders |
| `useMouse` | `boolean` | `true` | Enable mouse input/tracking |
| `autoFocus` | `boolean` | `true` | Focus nearest focusable on left click |
| `enableMouseMovement` | `boolean` | `true` | Track mouse movement (not just clicks) |
| `useAlternateScreen` | `boolean` | `true` | Use terminal alternate screen buffer |
| `consoleOptions` | `ConsoleOptions` | (none) | Built-in console overlay options |
| `openConsoleOnError` | `boolean` | `true` | Auto-open console on errors (dev only) |
| `onDestroy` | `() => void` | (none) | Callback on renderer destruction |

### Key Properties

| Property | Type | Description |
|----------|------|-------------|
| `root` | `RootRenderable` | Root of the component tree (fills terminal) |
| `width` | `number` | Current width in columns |
| `height` | `number` | Current height in rows |
| `console` | `TerminalConsole` | Built-in console overlay |
| `keyInput` | `KeyHandler` | Keyboard input handler |
| `isRunning` | `boolean` | Whether render loop is active |
| `isDestroyed` | `boolean` | Whether renderer is destroyed |
| `currentFocusedRenderable` | `Renderable \| null` | Currently focused component |

### Render Loop Control

**Automatic mode (default)** re-renders only when the component tree changes:
```typescript
const renderer = await createCliRenderer()
renderer.root.add(Text({ content: "Static content" }))
// No start() needed; renders automatically on tree changes
```

**Continuous mode** runs at targetFps:
```typescript
renderer.start()   // Begin continuous rendering
renderer.stop()    // Stop continuous rendering
```

**Live rendering**, for animations:
```typescript
renderer.requestLive()   // Request continuous rendering
renderer.dropLive()      // Drop live rendering request
```

**Pause/Suspend:**
```typescript
renderer.pause()
renderer.suspend()
renderer.resume()
```

### Events

```typescript
renderer.on("resize", (width, height) => { /* terminal resized */ })
renderer.on("destroy", () => { /* renderer destroyed */ })
renderer.on("selection", (selection) => { /* text selected */ })
```

### Cursor Control

```typescript
renderer.setCursorPosition(10, 5, true)
renderer.setCursorStyle("block", true)    // block | underline | line
renderer.setCursorColor(RGBA.fromHex("#FF0000"))
```

### Cleanup

```typescript
renderer.destroy()
```

**CRITICAL:** Always call `destroy()` when finished. This restores terminal state (mouse tracking, raw mode, alternate screen). OpenTUI does NOT automatically clean up on `process.exit` or unhandled errors.

### Debug Overlay

```typescript
renderer.toggleDebugOverlay()

import { DebugOverlayCorner } from "@opentui/core"
renderer.configureDebugOverlay({ enabled: true, corner: DebugOverlayCorner.topRight })
```

## 3. Renderables (Imperative API)

Renderables are the building blocks of the UI. Each represents a visual element using Yoga layout engine for positioning.

### Creating Renderables

```typescript
import { TextRenderable, BoxRenderable } from "@opentui/core"

// Constructor: new XxxRenderable(ctx: RenderContext, options)
// ctx IS the renderer itself (or any object implementing RenderContext)
const greeting = new TextRenderable(renderer, {
  id: "greeting",
  content: "Hello!",
  fg: "#00FF00",
})
renderer.root.add(greeting)
```

### Available Renderables

| Class | Description |
|-------|-------------|
| `BoxRenderable` | Container with border, background and layout |
| `TextRenderable` | Read-only styled text display |
| `InputRenderable` | Single-line text input |
| `TextareaRenderable` | Multi-line editable text |
| `SelectRenderable` | Dropdown/list selection |
| `TabSelectRenderable` | Horizontal tab selection |
| `ScrollBoxRenderable` | Scrollable container |
| `ScrollBarRenderable` | Standalone scroll bar control |
| `CodeRenderable` | Syntax-highlighted code display |
| `LineNumberRenderable` | Line number gutter |
| `DiffRenderable` | Unified or split diff viewer |
| `ASCIIFontRenderable` | ASCII art font display |
| `FrameBufferRenderable` | Raw framebuffer for custom graphics |
| `MarkdownRenderable` | Markdown renderer |
| `SliderRenderable` | Numeric slider control |

Full per-component API (options, events, gotchas) is in [component-reference.md](component-reference.md); load it when working with a specific component beyond basic construction.

### The Renderable Tree

```typescript
const container = new BoxRenderable(renderer, {
  id: "container",
  flexDirection: "column",
  padding: 1,
})

const title = new TextRenderable(renderer, { id: "title", content: "My App" })
const body = new TextRenderable(renderer, { id: "body", content: "Content" })

container.add(title)
container.add(body)
renderer.root.add(container)

// Remove a child: MUST use string ID, not the renderable instance
container.remove("body")
```

### CRITICAL: remove() API

**`remove(id: string): void`** is the ONLY signature. Always pass a string ID.

```typescript
// CORRECT
container.remove("body")
container.remove(child.id)     // .id returns the auto-generated or explicit ID

// WRONG: will fail at runtime
container.remove(child)        // passes object, not string
```

Every renderable gets an auto-generated `.id` from a static counter. If you set `id` in options, that becomes the ID. Otherwise it's auto-generated. Access via `renderable.id`.

### Finding Renderables

```typescript
const title = container.getRenderable("title")              // Direct child by ID
const deep = container.findDescendantById("nested-input")   // Recursive search
const children = container.getChildren()                     // All children
```

### Visibility

```typescript
panel.visible = false   // Hides AND removes from layout (like CSS display: none)
panel.visible = true
```

### Opacity

```typescript
panel.opacity = 0.5   // Affects renderable and all children
```

### Z-Index

```typescript
const overlay = new BoxRenderable(renderer, {
  position: "absolute",
  zIndex: 100,   // Higher values render on top
})
```

### Translation (Visual Offset)

```typescript
renderable.translateX = 10
renderable.translateY = -5
// Moves visually without affecting layout
```

### Destroying Renderables

```typescript
renderable.destroy()              // Remove from parent, free resources
container.destroyRecursively()    // Destroy self and all children
```

### Lifecycle Methods (Custom Renderables)

```typescript
class CustomRenderable extends Renderable {
  onUpdate(deltaTime: number) { /* called each frame before render */ }
  onResize(width: number, height: number) { /* dimensions changed */ }
  onRemove() { /* removed from parent; cleanup here */ }
  renderSelf(buffer: OptimizedBuffer, deltaTime: number) { /* custom drawing */ }
}
```

### Live Rendering

```typescript
const box = new AnimatedBox(renderer, {
  live: true,   // Enable continuous rendering for this renderable
})
```

### Buffered Rendering

```typescript
const complex = new BoxRenderable(renderer, {
  buffered: true,   // Render to offscreen buffer first
  renderAfter: (buffer) => {
    buffer.fillRect(0, 0, 10, 5, RGBA.fromHex("#FF0000"))
  },
})
```

## 4. Constructs (Declarative API)

Factory functions that create VNodes: lightweight descriptions of components. VNodes become actual Renderables when added to the tree.

```typescript
import { Box, Text, Input } from "@opentui/core"

Box(
  { width: 40, height: 10, borderStyle: "rounded", padding: 1 },
  Text({ content: "Welcome!" }),
  Input({ placeholder: "Enter your name..." }),
)
```

### Available Constructs

`ASCIIFont`, `Box`, `Code`, `FrameBuffer`, `Input`, `ScrollBox`, `Select`, `TabSelect`, `Text`, `SyntaxStyle`

**NOT yet available as constructs** (use Renderable API): `Textarea`, `ScrollBar`, `Slider`, `Markdown`, `LineNumber`, `Diff`

### Method Chaining on VNodes

VNodes queue method calls, applied after the component is created:
```typescript
const input = Input({ placeholder: "Name..." })
input.focus()   // Queued, applied when added to tree
```

### Delegation

Routes method/property calls to descendant IDs:
```typescript
import { delegate } from "@opentui/core"

function LabeledInput(props) {
  return delegate(
    { focus: `${props.id}-input` },   // focus() routes to child input
    Box(
      { flexDirection: "row" },
      Text({ content: props.label }),
      Input({ id: `${props.id}-input`, placeholder: props.placeholder }),
    ),
  )
}

const field = LabeledInput({ id: "name", label: "Name:", placeholder: "..." })
field.focus()   // Delegates to the inner input
```

### Mixing Renderables and Constructs

```typescript
const container = new BoxRenderable(renderer, { id: "root", flexDirection: "column" })
container.add(Text({ content: "Title" }), Input({ placeholder: "Type here..." }))
renderer.root.add(container)
```

## 5. Layout (Yoga Flexbox)

### Flex Direction

```typescript
{ flexDirection: "column" }       // vertical (default)
{ flexDirection: "row" }          // horizontal
{ flexDirection: "row-reverse" }
{ flexDirection: "column-reverse" }
```

### Justify Content (Main Axis)

`flex-start` | `flex-end` | `center` | `space-between` | `space-around` | `space-evenly`

### Align Items (Cross Axis)

`flex-start` | `flex-end` | `center` | `stretch` (default) | `baseline`

### Sizing

```typescript
{ width: 30, height: 10 }        // Fixed (characters/rows)
{ width: "100%", height: "50%" }  // Percentage
{ flexGrow: 1, flexShrink: 0 }   // Flex behaviour
{ minWidth: 20, maxHeight: 30 }   // Constraints
```

### Positioning

```typescript
{ position: "relative" }   // default; flows in layout
{ position: "absolute", left: 10, top: 5 }   // removed from flow
```

### Spacing

```typescript
{ padding: 2 }                          // All sides
{ paddingTop: 1, paddingX: 4 }          // Specific sides/axes
{ margin: 1 }                           // Same pattern
```

### Gap

```typescript
{ gap: 1 }   // Space between children
```

## Additional resources

Deep-dive detail lives in supporting files, loaded only when needed:

- [component-reference.md](component-reference.md): full API for every renderable (BoxRenderable through FrameBufferRenderable): options, events, gotchas
- [input-and-styling.md](input-and-styling.md): keyboard input, focus management, colours/RGBA, console overlay, environment variables
- [advanced-and-testing.md](advanced-and-testing.md): tree-sitter integration, Solid.js/React framework bindings, common patterns (screen pattern, lifecycle, dynamic updates), mock-renderer testing, the full gotchas list
