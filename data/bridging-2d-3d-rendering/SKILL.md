---
name: bridging-2d-3d-rendering
description: Bridging 2D canvas and 3D spatial rendering in StickerNest. Use when working with coordinate conversion, parallel DOM/WebGL architecture, widget rendering across modes, Html vs pure 3D decisions, or mode-aware components. Covers spatialCoordinates utilities, SpatialCanvas, SpatialWidgetContainer, and XR session detection.
---

# Bridging 2D Canvas and 3D Spatial Rendering

StickerNest uses a **parallel rendering architecture** where 2D DOM canvas and 3D WebGL scene coexist. Understanding this bridge is critical for building features that work across desktop, VR, and AR.

## Core Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  CanvasPage.tsx                                             │
│  ┌─────────────────────┐    ┌─────────────────────────────┐ │
│  │  CanvasRenderer     │    │  SpatialCanvas              │ │
│  │  (DOM/2D)           │    │  (WebGL/3D)                 │ │
│  │                     │    │                             │ │
│  │  - HTML elements    │    │  - Three.js scene           │ │
│  │  - CSS positioning  │    │  - 3D meshes & materials    │ │
│  │  - React components │    │  - WebXR sessions           │ │
│  │                     │    │                             │ │
│  │  visible: desktop   │    │  visible: vr/ar             │ │
│  └─────────────────────┘    └─────────────────────────────┘ │
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐│
│  │  Shared State (Zustand stores)                          ││
│  │  - useCanvasStore (widgets, stickers, positions)        ││
│  │  - useSpatialModeStore (desktop/vr/ar mode)             ││
│  └─────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

**Key principle**: Both renderers read from the same state. Position a widget in 2D, and it appears in the correct 3D location automatically.

## Spatial Modes

```typescript
import { useActiveSpatialMode, useIsDesktopMode } from '@/state/useSpatialModeStore';

type SpatialMode = 'desktop' | 'vr' | 'ar';

// In components:
const spatialMode = useActiveSpatialMode();
const isDesktopMode = spatialMode === 'desktop';
```

| Mode | Renderer | Use Case |
|------|----------|----------|
| `desktop` | CanvasRenderer (DOM) | Traditional 2D editing |
| `vr` | SpatialCanvas (WebGL) | Immersive VR headset |
| `ar` | SpatialCanvas (WebGL) | AR passthrough |

## Coordinate Conversion

The bridge between 2D and 3D is **coordinate conversion**. Use these utilities from `src/utils/spatialCoordinates.ts`:

### Constants

```typescript
import {
  PIXELS_PER_METER,    // 100 - conversion factor
  DEFAULT_WIDGET_Z,    // -2 meters (in front of user)
  DEFAULT_EYE_HEIGHT,  // 1.6 meters (standing user)
} from '@/utils/spatialCoordinates';
```

### 2D to 3D Conversion

```typescript
import { toSpatialPosition, toSpatialSize, toSpatialRotation } from '@/utils/spatialCoordinates';

// Position: pixels → meters
const pos3D = toSpatialPosition({ x: 500, y: 300 });
// Returns: [5, 1.1, -2] (x in meters, y adjusted for eye height, z = default depth)

// Size: pixels → meters
const size3D = toSpatialSize({ width: 200, height: 150 });
// Returns: { width: 2, height: 1.5 }

// Rotation: degrees → radians (around Z axis)
const rot3D = toSpatialRotation(45);
// Returns: [0, 0, -0.785] (Euler angles)
```

### 3D to 2D Conversion

```typescript
import { toDOMPosition, toDOMSize } from '@/utils/spatialCoordinates';

// Position: meters → pixels
const pos2D = toDOMPosition([5, 1.1, -2]);
// Returns: { x: 500, y: 300 }

// Size: meters → pixels
const size2D = toDOMSize({ width: 2, height: 1.5 });
// Returns: { width: 200, height: 150 }
```

### Full Transform

```typescript
import { toSpatialTransform } from '@/utils/spatialCoordinates';

const transform = toSpatialTransform({
  x: 500,
  y: 300,
  width: 200,
  height: 150,
  rotation: 45,
  scale: 1,
  z: -3, // optional custom depth
});
// Returns: { position: [x,y,z], rotation: [rx,ry,rz], scale: [s,s,s] }
```

### Y-Axis Inversion

**Critical**: DOM Y grows downward, 3D Y grows upward. The conversion handles this:

```
DOM:     (0,0) ──────► X        3D:      Y ▲
              │                           │
              │                           │
              ▼ Y                         └──────► X
```

## Widget Rendering Across Modes

### The Html Component Problem

The `<Html>` component from `@react-three/drei` renders DOM content in 3D space. **BUT** it creates DOM overlays that break immersive WebXR:

```tsx
// This breaks immersive VR! DOM overlays appear as flat screen
<Html transform position={[0, 0, 0]}>
  <div>Widget content</div>
</Html>
```

### XR Session Detection

Always check if in an XR session before rendering Html:

```tsx
import { useXR } from '@react-three/xr';

function SpatialWidget({ widget }) {
  // Detect active XR session
  const session = useXR((state) => state.session);
  const isPresenting = !!session;

  return (
    <group position={position3D}>
      {/* 3D panel mesh - always renders */}
      <mesh>
        <planeGeometry args={[width, height]} />
        <meshStandardMaterial color="#1e1b4b" />
      </mesh>

      {/* Html content - ONLY when NOT in XR session */}
      {!isPresenting && (
        <Html transform center>
          <WidgetContent />
        </Html>
      )}

      {/* 3D placeholder - ONLY when IN XR session */}
      {isPresenting && (
        <Text position={[0, 0, 0.01]} fontSize={0.05}>
          {widget.name}
        </Text>
      )}
    </group>
  );
}
```

### Decision Tree: Html vs Pure 3D

```
Is this for XR (VR/AR)?
├─ YES: Use pure Three.js
│       - <mesh> with materials
│       - <Text> from drei for labels
│       - Textures for images
│       - NO <Html> components
│
└─ NO (desktop/preview): Can use Html
        - <Html> for complex React UI
        - iframes for widget sandboxing
        - Full CSS styling
```

## Mode-Aware Component Pattern

```tsx
import { useActiveSpatialMode } from '@/state/useSpatialModeStore';
import { useXR } from '@react-three/xr';

function ModeAwareWidget({ widget }) {
  const spatialMode = useActiveSpatialMode();
  const session = useXR((state) => state.session);
  const isXRActive = !!session;

  // Desktop mode: use CanvasRenderer (not this component)
  // This component only runs in SpatialCanvas (vr/ar modes)

  if (isXRActive) {
    // TRUE XR: Pure WebGL only
    return <PureWebGLWidget widget={widget} />;
  }

  // Preview mode (vr/ar without XR session): Can use Html
  return <HtmlBasedWidget widget={widget} />;
}
```

## Parallel Rendering in CanvasPage

```tsx
// src/pages/CanvasPage.tsx structure
function CanvasPage() {
  const spatialMode = useActiveSpatialMode();
  const isDesktopMode = spatialMode === 'desktop';

  return (
    <>
      {/* DOM Renderer - visible only in desktop mode */}
      {isDesktopMode && (
        <CanvasRenderer
          widgets={widgets}
          // ... DOM-based rendering
        />
      )}

      {/* WebGL/XR Renderer - visible in VR/AR modes */}
      <SpatialCanvas active={!isDesktopMode} />
    </>
  );
}
```

## Common Patterns

### Pattern: Conditional Widget Content

```tsx
function WidgetPanel({ widget, isPresenting }) {
  const size3D = toSpatialSize({ width: widget.width, height: widget.height });

  return (
    <group>
      {/* Base panel - always visible */}
      <mesh>
        <planeGeometry args={[size3D.width, size3D.height]} />
        <meshStandardMaterial color="#1e1b4b" transparent opacity={0.95} />
      </mesh>

      {/* Content layer */}
      {isPresenting ? (
        // XR mode: 3D placeholder
        <group position={[0, 0, 0.01]}>
          <Text fontSize={0.05} color="white" anchorX="center">
            {widget.name || 'Widget'}
          </Text>
          <Text position={[0, -0.08, 0]} fontSize={0.03} color="#888">
            {widget.widgetDefId}
          </Text>
        </group>
      ) : (
        // Preview mode: Full HTML content
        <Html transform center distanceFactor={1.5}>
          <WidgetIframe widget={widget} />
        </Html>
      )}
    </group>
  );
}
```

### Pattern: Syncing 3D Changes Back to 2D

When users move widgets in VR, update the 2D canvas state:

```tsx
function handleWidgetMove(widgetId: string, newPos3D: [number, number, number]) {
  // Convert 3D position back to 2D
  const pos2D = toDOMPosition(newPos3D);

  // Update the shared canvas store
  useCanvasStore.getState().updateWidget(widgetId, {
    x: pos2D.x,
    y: pos2D.y,
  });
}
```

### Pattern: Resolution Scaling for VR

HTML content can look pixelated in VR. Use resolution scaling:

```tsx
const VR_RESOLUTION_SCALE = 2.5;

function getWidgetResolutionScale(width: number, height: number): number {
  const maxDimension = Math.max(width, height);
  if (maxDimension <= 600) return VR_RESOLUTION_SCALE;
  // Scale down for large widgets to save memory
  return Math.max(1.5, VR_RESOLUTION_SCALE * (600 / maxDimension));
}

// Render at higher resolution, scale down visually
const scaledWidth = widget.width * resolutionScale;
const scaledHeight = widget.height * resolutionScale;
const inverseScale = 1 / resolutionScale;

<Html scale={inverseScale} style={{ width: scaledWidth, height: scaledHeight }}>
  {/* Content renders at higher resolution */}
</Html>
```

## Reference Files

| File | Purpose |
|------|---------|
| `src/utils/spatialCoordinates.ts` | All coordinate conversion utilities |
| `src/state/useSpatialModeStore.ts` | Spatial mode state (desktop/vr/ar) |
| `src/pages/CanvasPage.tsx` | Parallel renderer orchestration |
| `src/components/spatial/SpatialCanvas.tsx` | WebGL/Three.js canvas |
| `src/components/spatial/SpatialScene.tsx` | 3D scene composition |
| `src/components/spatial/SpatialWidgetContainer.tsx` | Widget rendering in 3D |
| `src/components/canvas/CanvasRenderer.tsx` | DOM-based 2D rendering |

## Troubleshooting

### Issue: VR shows flat screen instead of immersive 3D
**Cause**: `<Html>` components rendering in XR session
**Fix**: Check `isPresenting` and skip Html when true

### Issue: Widget positions don't match between 2D and 3D
**Cause**: Missing Y-axis inversion or eye height offset
**Fix**: Use `toSpatialPosition()` / `toDOMPosition()` consistently

### Issue: Widgets look pixelated in VR
**Cause**: Default resolution too low for VR displays
**Fix**: Apply `VR_RESOLUTION_SCALE` multiplier to Html content

### Issue: Widget interactions don't work in VR
**Cause**: Pointer events not reaching 3D meshes
**Fix**: Ensure `pointerEvents: 'auto'` on Html or use `onClick` on meshes
