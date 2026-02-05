---
name: parallel-rendering-architecture
description: Understanding StickerNest's parallel DOM/WebGL rendering architecture. Use when working with the dual renderer system, switching between 2D DOM and 3D WebGL modes, or understanding how desktop and VR/AR rendering coexist. Covers SpatialCanvas, mode switching, and renderer coordination.
---

# Parallel Rendering Architecture

StickerNest uses a **parallel rendering architecture** where two rendering systems coexist:
- **DOM Renderer**: Traditional React/CSS for desktop mode (fast, accessible, proven)
- **WebGL Renderer**: Three.js/R3F for VR/AR modes (immersive, 3D-capable)

## Why Parallel, Not Unified?

| Approach | Pros | Cons |
|----------|------|------|
| **Unified 3D** | Single codebase | Breaks existing DOM, performance overhead for 2D |
| **Parallel** | Desktop stays fast, VR gets proper 3D | Two renderers to maintain |

We chose **parallel** because:
1. Desktop rendering already works and is performant
2. VR/AR requires fundamentally different rendering (WebGL, cameras, depth)
3. Incremental migration is safer than full rewrite
4. Fallback to DOM if WebGL fails

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                    useSpatialModeStore                  │
│              activeMode: 'desktop' | 'vr' | 'ar'        │
└─────────────────────────┬───────────────────────────────┘
                          │
              ┌───────────┴───────────┐
              ▼                       ▼
┌─────────────────────┐   ┌─────────────────────────────┐
│   DOM Renderer      │   │      WebGL Renderer         │
│   (CanvasRenderer)  │   │   (SpatialCanvas + R3F)     │
│                     │   │                             │
│  - React components │   │  - Three.js scene           │
│  - CSS transforms   │   │  - XR session               │
│  - 2D hit testing   │   │  - 3D raycasting            │
└─────────────────────┘   └─────────────────────────────┘
              │                       │
              └───────────┬───────────┘
                          ▼
              ┌───────────────────────┐
              │    Shared State       │
              │  (Zustand stores)     │
              │                       │
              │  - Widget positions   │
              │  - Entity data        │
              │  - Selection state    │
              └───────────────────────┘
```

---

## Key Components

### 1. Mode Store (`useSpatialModeStore`)

Controls which renderer is active:

```typescript
import { useSpatialModeStore, useActiveSpatialMode } from '../state/useSpatialModeStore';

const spatialMode = useActiveSpatialMode(); // 'desktop' | 'vr' | 'ar'

// Mode determines which renderer shows
if (spatialMode === 'desktop') {
  // Show DOM renderer
} else {
  // Show WebGL renderer
}
```

### 2. DOM Renderer (`CanvasRenderer`)

The existing 2D renderer at `src/components/CanvasRenderer.tsx`:

```tsx
// Existing component - no changes needed for parallel architecture
<CanvasRenderer
  widgets={widgets}
  entities={entities}
  // ... props
/>
```

### 3. WebGL Renderer (`SpatialCanvas`)

New Three.js/R3F renderer at `src/components/spatial/SpatialCanvas.tsx`:

```tsx
import { Canvas } from '@react-three/fiber';
import { XR, createXRStore } from '@react-three/xr';

const xrStore = createXRStore({ /* config */ });

function SpatialCanvas({ widgets, entities }) {
  return (
    <Canvas>
      <XR store={xrStore}>
        {/* 3D scene that mirrors widget/entity state */}
        <WidgetLayer3D widgets={widgets} />
        <EntityLayer3D entities={entities} />
      </XR>
    </Canvas>
  );
}
```

### 4. Renderer Switcher

Coordinates which renderer is visible:

```tsx
function EditorCanvas() {
  const spatialMode = useActiveSpatialMode();
  const widgets = useWidgets();
  const entities = useEntities();

  return (
    <div className="editor-canvas">
      {/* DOM renderer - visible only in desktop mode */}
      <div style={{ display: spatialMode === 'desktop' ? 'block' : 'none' }}>
        <CanvasRenderer widgets={widgets} entities={entities} />
      </div>

      {/* WebGL renderer - visible only in VR/AR modes */}
      {spatialMode !== 'desktop' && (
        <SpatialCanvas widgets={widgets} entities={entities} />
      )}
    </div>
  );
}
```

---

## Data Flow

Both renderers consume the **same state**:

```
┌──────────────────┐
│  User Interaction │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐     ┌──────────────────┐
│  DOM Events      │ OR  │  XR Input        │
│  (mouse, touch)  │     │  (controller)    │
└────────┬─────────┘     └────────┬─────────┘
         │                        │
         └──────────┬─────────────┘
                    ▼
         ┌──────────────────┐
         │  Intent System   │
         │  (select, grab)  │
         └────────┬─────────┘
                  │
                  ▼
         ┌──────────────────┐
         │  Zustand Store   │
         │  (single source) │
         └────────┬─────────┘
                  │
         ┌────────┴────────┐
         ▼                 ▼
┌──────────────┐   ┌──────────────┐
│ DOM Renderer │   │ WebGL Render │
│   updates    │   │   updates    │
└──────────────┘   └──────────────┘
```

---

## Position Mapping

DOM uses pixels, WebGL uses meters. Convert between them:

```typescript
// Constants
const PIXELS_PER_METER = 100; // 1 meter = 100 pixels

// 2D → 3D position
function toSpatialPosition(pos2D: { x: number; y: number }): [number, number, number] {
  return [
    pos2D.x / PIXELS_PER_METER,
    -pos2D.y / PIXELS_PER_METER, // Y is inverted in 3D
    0 // Z = 0 for flat widgets
  ];
}

// 3D → 2D position
function toDOMPosition(pos3D: [number, number, number]): { x: number; y: number } {
  return {
    x: pos3D[0] * PIXELS_PER_METER,
    y: -pos3D[1] * PIXELS_PER_METER
  };
}
```

---

## Widget Rendering in 3D

Widgets are HTML - they need special handling in WebGL:

### Option A: HTML to Texture (Simple, Limited)

```tsx
import { Html } from '@react-three/drei';

function Widget3D({ widget }) {
  const position = toSpatialPosition(widget.position);

  return (
    <Html
      position={position}
      transform
      occlude
      style={{ width: widget.width, height: widget.height }}
    >
      <WidgetContent widget={widget} />
    </Html>
  );
}
```

### Option B: CSS3DRenderer (Better Interactivity)

```tsx
// Use CSS3DRenderer alongside WebGLRenderer
// Widgets stay as DOM but are positioned in 3D space
```

### Option C: Render to Texture (Best Performance)

```tsx
// Render widget HTML to canvas, use as texture
// Best for many widgets, worst for interactivity
```

**Recommendation**: Start with Option A (`<Html>`), upgrade as needed.

---

## Switching Modes

When user clicks VR toggle:

```typescript
// 1. Store updates
useSpatialModeStore.getState().toggleVR();

// 2. This triggers re-render
const spatialMode = useActiveSpatialMode(); // now 'vr'

// 3. Renderer switcher responds
if (spatialMode === 'desktop') {
  // Hide WebGL, show DOM
} else {
  // Hide DOM, show WebGL
  // Start XR session if VR/AR
}
```

---

## XR Session Lifecycle

```tsx
function SpatialCanvas() {
  const setActiveMode = useSpatialModeStore((s) => s.setActiveMode);
  const setSessionState = useSpatialModeStore((s) => s.setSessionState);

  return (
    <Canvas>
      <XR
        store={xrStore}
        onSessionStart={() => {
          setSessionState('active');
          // Detect VR vs AR from session
          const mode = xrStore.getState().session?.mode;
          setActiveMode(mode?.includes('ar') ? 'ar' : 'vr');
        }}
        onSessionEnd={() => {
          setSessionState('none');
          setActiveMode('desktop'); // Return to DOM renderer
        }}
      >
        <Scene />
      </XR>
    </Canvas>
  );
}
```

---

## File Structure

```
src/
├── components/
│   ├── CanvasRenderer.tsx      # Existing DOM renderer (unchanged)
│   └── spatial/
│       ├── SpatialCanvas.tsx   # Main WebGL canvas wrapper
│       ├── SpatialScene.tsx    # 3D scene content
│       ├── WidgetLayer3D.tsx   # Widgets in 3D
│       ├── EntityLayer3D.tsx   # Entities in 3D
│       └── XRControls.tsx      # VR/AR specific controls
├── state/
│   └── useSpatialModeStore.ts  # Mode switching state
└── utils/
    └── spatialCoordinates.ts   # 2D ↔ 3D conversion
```

---

## Testing Strategy

### Desktop Mode
- All existing tests pass
- DOM renderer unaffected

### VR Mode
- Use WebXR Emulator extension
- Test widget visibility in 3D
- Test interaction raycasting

### Mode Switching
- Toggle VR → scene appears
- Toggle back → DOM restored
- State preserved across switches

---

## Performance Considerations

1. **Don't render both simultaneously** - one visible at a time
2. **Lazy load WebGL** - only when VR/AR mode requested
3. **Dispose Three.js objects** - prevent memory leaks on mode switch
4. **Throttle state sync** - don't update 3D scene on every frame

---

## Common Issues

### Issue: Widgets not visible in VR
**Cause**: Z-position too far or wrong scale
**Fix**: Check `toSpatialPosition` conversion, verify meters not pixels

### Issue: Performance drops when switching modes
**Cause**: Both renderers running
**Fix**: Ensure only active renderer is mounted/visible

### Issue: XR session fails
**Cause**: HTTPS required, or device unsupported
**Fix**: Check `useSpatialModeStore.capabilities`, show fallback message

---

## Reference Files

- **Mode Store**: `src/state/useSpatialModeStore.ts`
- **DOM Renderer**: `src/components/CanvasRenderer.tsx`
- **Spatial Canvas**: `src/components/spatial/SpatialCanvas.tsx` (to be created)
- **XR Skill**: `.claude/skills/implementing-spatial-xr/`
