---
name: boardkit-canvas-input-model
description: |
  Canvas input model: pan/zoom, pointer events, keyboard shortcuts, selection, gestures.
  Use when working on canvas interactions, navigation, or input handling.
allowed-tools: Read, Grep, Glob
---

# Boardkit Canvas Input Model

## Tools

| Tool | Shortcut | Behavior |
|------|----------|----------|
| Select | `V` | Click to select, drag to move/resize |
| Hand | `H` | Drag to pan canvas |
| Rectangle | `R` | Click+drag to draw |
| Ellipse | `O` | Click+drag to draw |
| Line | `L` | Click+drag to draw |
| Arrow | `A` | Click+drag to draw |
| Pencil | `P` | Freehand drawing |
| Text | `T` | Click to place text block |

## Navigation

### Pan
| Input | Behavior |
|-------|----------|
| Hand tool + drag | Pan canvas |
| Middle mouse + drag | Pan canvas |
| Space + drag | Temporary hand tool |
| Trackpad two-finger | Pan canvas |

### Zoom
| Input | Behavior |
|-------|----------|
| Scroll wheel | Zoom at cursor |
| Trackpad pinch | Zoom at center |
| `Cmd/Ctrl` + `+` | Zoom in |
| `Cmd/Ctrl` + `-` | Zoom out |
| `Cmd/Ctrl` + `0` | Reset zoom (100%) |

**Zoom range**: 10% — 500%

## Selection

| Input | Behavior |
|-------|----------|
| Click widget/element | Select single |
| `Shift` + click | Add to selection (future) |
| Click empty space | Deselect all |
| `Escape` | Deselect all |
| Drag on empty | Marquee selection (future) |

## Widget Interactions

| Input | Behavior |
|-------|----------|
| Drag widget | Move |
| Corner handles | Resize |
| `Shift` + resize | Maintain aspect ratio |
| Double-click | Enter edit mode |
| `Delete` / `Backspace` | Delete selected |
| `Cmd/Ctrl` + `D` | Duplicate |

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Cmd/Ctrl` + `K` | Command palette |
| `Cmd/Ctrl` + `Z` | Undo |
| `Cmd/Ctrl` + `Shift` + `Z` | Redo |
| `Cmd/Ctrl` + `D` | Duplicate |
| `Cmd/Ctrl` + `A` | Select all |
| `Escape` | Deselect / Cancel |
| `Delete` | Delete selected |
| `V`, `H`, `R`, `O`, `L`, `A`, `P`, `T` | Tool shortcuts |

## Focus Model

```
┌─────────────────────────────────────┐
│ Canvas Focus (shortcuts work)       │
│                                     │
│   ┌─────────────────────────────┐   │
│   │ Widget Focus                │   │
│   │ (widget captures input)     │   │
│   │                             │   │
│   │   ┌─────────────────────┐   │   │
│   │   │ Input Focus         │   │   │
│   │   │ (text input active) │   │   │
│   │   └─────────────────────┘   │   │
│   └─────────────────────────────┘   │
└─────────────────────────────────────┘
```

- **Canvas focus**: Tool shortcuts work (V, H, R, etc.)
- **Widget focus**: Widget captures input, canvas shortcuts disabled
- **Input focus**: Text input captures all keyboard

## Drawing Elements

| Action | Behavior |
|--------|----------|
| Click + drag | Create shape |
| `Shift` + drag | Constrain (square, straight) |
| `Enter` | Commit text element |
| `Escape` | Cancel drawing |

## Performance Rules

1. Use CSS transforms for drag (no re-render)
2. Throttle pointer events with `requestAnimationFrame`
3. Lazy render elements outside viewport (future)

## Key Files

| Purpose | Path |
|---------|------|
| Canvas (web) | `apps/web/src/components/BoardCanvas.vue` |
| Canvas (desktop) | `apps/desktop/src/components/BoardCanvas.vue` |
| Widget frame | `packages/ui/src/components/WidgetFrame.vue` |
| Selection handles | `packages/ui/src/components/SelectionHandles.vue` |
| Tool store | `packages/core/src/stores/toolStore.ts` |
| Keyboard shortcuts | `packages/core/src/composables/useKeyboardShortcuts.ts` |
