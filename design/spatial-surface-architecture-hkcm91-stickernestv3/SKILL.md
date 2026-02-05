---
name: spatial-surface-architecture
description: Surface-first hybrid architecture for StickerNest widget and sticker placement in VR/AR. Use when designing spatial placement systems, deciding between XR planes vs custom environments, implementing widget snapping, or understanding how surfaces should be prioritized. Covers Meta Horizon OS and visionOS design patterns, diegetic vs non-diegetic UI, and the room-as-canvas paradigm.
---

# Spatial Surface Architecture for StickerNest

This skill documents the recommended architecture for widget and sticker placement in 3D/VR/AR environments, based on research of state-of-the-art platform guidelines and StickerNest's specific use cases.

## Core Principle: The Room as Canvas

> "Use spatial anchors in combination with semantic surfaces (walls, table, floor) to create rich experiences. **The user's room becomes a spatial rendering canvas**."
> — Meta Horizon OS Design Guidelines

StickerNest treats surfaces (real or virtual) as the primary canvas for content placement:
- **Real surfaces** from WebXR plane/mesh detection when available
- **Virtual surfaces** from custom 3D environments as fallback
- **Free space** only when no surfaces are detected

---

## StickerNest Content Types & Placement Behavior

### Widgets (Non-Diegetic Panels)

Widgets are **floating 2D panels** displaying interactive content:

| Behavior | Description |
|----------|-------------|
| **Default Position** | 2m in front of user, eye level |
| **Movement** | Grabbable, draggable in 3D space |
| **Surface Interaction** | CAN snap to surfaces but not required |
| **Persistence** | Store world position or surface-relative position |
| **Orientation** | Billboard toward user OR fixed to surface normal |

**Design Pattern**: Like Horizon OS panels or visionOS windows

```
Widget in Space:
┌─────────────────────┐
│                     │
│   Widget Content    │  ← Floating in front of user
│                     │
└─────────────────────┘
        │
        ↓ (optional snap)
════════════════════════ ← Wall surface
```

### Stickers (Diegetic Elements)

Stickers are **surface-attached visuals** that feel like real objects:

| Behavior | Description |
|----------|-------------|
| **Default Position** | Must attach to a surface |
| **Movement** | Drag along surfaces, snap between surfaces |
| **Surface Interaction** | ALWAYS attached to a surface |
| **Persistence** | Store surface-relative position (offset from anchor) |
| **Orientation** | Face outward from surface normal |

**Design Pattern**: Like physical stickers, posters, or wall decorations

```
Sticker on Wall:
                    ╔═══╗
════════════════════╣ 🎯 ╠════════════════
                    ╚═══╝
                      ↑
              Attached to wall surface
```

### Widget Launchers (Hybrid)

Stickers that open widgets when activated:

| Behavior | Description |
|----------|-------------|
| **Placement** | Surface-attached (like stickers) |
| **Activation** | Click/tap spawns associated widget |
| **Widget Spawn** | Widget appears floating near the sticker |

---

## Surface Priority System

When multiple surface sources are available, use this priority order:

```
Priority 1: WebXR Planes (Real World)
├── Highest confidence - actual physical surfaces
├── Semantic labels: wall, floor, ceiling, table
└── Updated in real-time as room understanding improves

Priority 2: WebXR Meshes (Quest 3+, Vision Pro)
├── Full room geometry for precise collision
├── Includes furniture, irregular surfaces
└── Use for raycasting, not individual surface tracking

Priority 3: Custom 3D Environment
├── Fallback when XR detection unavailable
├── User-loaded GLTF/GLB with collision meshes
├── Provides "virtual room" in outdoor/unscanned spaces
└── Named collision meshes: *_wall, *_floor, *_collision

Priority 4: Free Placement
├── Last resort - no surfaces available
├── Place at comfortable viewing distance
└── Allow user to manually position
```

### Implementation Pattern

```typescript
function getPlacementSurface(position: Vector3): CollisionSurface | null {
  // 1. Try XR planes first
  const xrSurface = findNearestXRPlane(position);
  if (xrSurface && xrSurface.confidence > 0.8) {
    return xrSurface;
  }

  // 2. Try XR mesh intersection
  const meshHit = raycastXRMesh(position);
  if (meshHit) {
    return meshHit;
  }

  // 3. Try custom environment surfaces
  const envSurface = findNearestEnvironmentSurface(position);
  if (envSurface) {
    return envSurface;
  }

  // 4. No surface - free placement
  return null;
}
```

---

## Platform Design Guidelines Summary

### Meta Horizon OS

**Panel Placement**:
- Place objects at ~1 meter distance, slightly below eye level
- Align surface-attached objects with the surface normal
- Use spatial anchors for persistence across sessions

**Interaction**:
- Grab any edge or control bar to move panels
- Drag corners to resize
- Hinged panels for related content groups

**Key Quote**:
> "Spatial anchors enable anchoring of virtual objects to a specific location or object in the physical environment."

### Apple visionOS

**Window Placement**:
- Launch apps in front of the user, within field of view
- **Never anchor to the user's head** - causes discomfort
- Use dynamic scaling (windows grow when far, shrink when near)

**Ergonomics**:
- Horizontal head movement is easier than vertical
- Avoid placing objects too high or too low
- Use wider aspect ratios when more space is needed

**Key Quote**:
> "Anchor content in people's space, giving them the freedom to look around naturally."

### Shared Best Practices

| Practice | Why |
|----------|-----|
| Surface attachment over free float | Feels grounded, predictable |
| World-anchored over head-anchored | Prevents motion sickness |
| Semantic surfaces (wall/floor/table) | Enables intelligent placement |
| Visual feedback during placement | Builds user confidence |
| Snap points for precision | Reduces placement frustration |

---

## Diegetic vs Non-Diegetic UI

### Diegetic (In-World)

Elements that could exist within the virtual/mixed reality world:
- Stickers on walls
- Buttons on virtual devices
- Information displays on surfaces
- QR code markers with attached content

**Use for**: Surface-attached content, world-integrated experiences

### Non-Diegetic (Overlay)

Elements that exist as system UI, not part of the world:
- Floating widget panels
- System menus and toolbars
- HUD elements
- Notifications

**Use for**: Information access, system controls, temporary displays

### StickerNest Mapping

| Content Type | Category | Attachment |
|--------------|----------|------------|
| Stickers | Diegetic | Surface-required |
| Widget Panels | Non-diegetic | Surface-optional |
| XR Toolbar | Non-diegetic | Follow user |
| Widget Library | Non-diegetic | Floating panel |
| Snap Indicators | Non-diegetic | Surface preview |

---

## AR Without Room Mapping: The Environment Fallback

When Meta Quest room mapping isn't available (outdoors, new space, user hasn't set up):

### Problem
- No XR planes detected
- No surfaces for sticker attachment
- Poor user experience for surface-attached content

### Solution: Custom 3D Environment as Virtual Room

```
Real World (Camera)
        ↓
┌─────────────────────────────┐
│   Custom 3D Environment     │
│   ┌─────────────────────┐   │
│   │                     │   │
│   │   Virtual Room      │   │ ← Provides collision surfaces
│   │   with Walls        │   │
│   │                     │   │
│   └─────────────────────┘   │
└─────────────────────────────┘
        ↓
Widgets/Stickers attach to virtual surfaces
```

### Environment Alignment Options

1. **QR Code Alignment**
   - Place physical QR code in real space
   - Scan QR to position environment origin
   - Environment aligns to real-world reference

2. **Manual Placement**
   - User places environment via AR hit test
   - Drag to position, pinch to scale
   - Confirm when aligned

3. **Marker Image Alignment** (Future)
   - Print reference image
   - Environment snaps to detected image

### Persistence Strategy

Store positions **relative to environment**, not absolute world:

```typescript
interface EnvironmentRelativePosition {
  environmentId: string;
  surfaceId: string;
  // Offset from surface centroid in surface-local coordinates
  localOffset: { x: number; y: number };
  // Distance from surface along normal
  normalOffset: number;
}
```

When environment reloads, widget positions are restored correctly even if environment moves.

---

## Unified Surface Registry Pattern

All surfaces (XR, environment, manual) register to a single store:

```typescript
interface CollisionSurface {
  id: string;
  type: 'wall' | 'floor' | 'ceiling' | 'table' | 'custom';
  source: 'xr-plane' | 'xr-mesh' | 'environment' | 'manual';

  // Priority for surface selection (higher = prefer)
  priority: number;

  // Geometry reference for raycasting
  mesh: THREE.Mesh | null;

  // Computed properties
  boundingBox: THREE.Box3;
  centroid: THREE.Vector3;
  normal: THREE.Vector3;

  // Snap points for this surface
  snapPoints: SnapPoint[];

  // Source tracking
  environmentId?: string;  // If from custom environment
  xrPlaneId?: string;      // If from XR detection
}
```

### Benefits of Unified Registry

1. **Single query interface** - `getNearestSurface()` works regardless of source
2. **Priority handling** - Automatically prefers XR over environment
3. **Consistent snapping** - Same snap logic for all surface types
4. **Easy debugging** - One place to visualize all surfaces
5. **Clean persistence** - Store surface reference, not raw geometry

---

## Snap Point Strategy

### Types of Snap Points

| Type | Use Case | Generation |
|------|----------|------------|
| Center | Default placement | Surface centroid |
| Corners | Alignment with edges | Bounding box corners |
| Edges | Side-by-side layout | Midpoints of edges |
| Grid | Precise arrangement | Regular spacing across surface |

### When to Show Snap Points

- **During drag**: Show available snap points on target surface
- **Within threshold**: Highlight active snap point (15cm default)
- **On release**: Snap to highlighted point if within threshold

### Snap Point Generation

```typescript
function generateSnapPoints(surface: CollisionSurface): SnapPoint[] {
  const points: SnapPoint[] = [];

  // Always include center
  points.push({
    id: `${surface.id}-center`,
    position: surface.centroid,
    normal: surface.normal,
    type: 'center',
  });

  // Add corners for walls (useful for posters, stickers)
  if (surface.type === 'wall') {
    const corners = computeBoundingBoxCorners(surface.mesh);
    corners.forEach((corner, i) => {
      points.push({
        id: `${surface.id}-corner-${i}`,
        position: corner,
        normal: surface.normal,
        type: 'corner',
      });
    });
  }

  // Add grid for tables (useful for organized layouts)
  if (surface.type === 'table') {
    const gridPoints = generateGridPoints(surface, 0.1); // 10cm grid
    points.push(...gridPoints);
  }

  return points;
}
```

---

## Visual Feedback Requirements

### During Placement/Drag

1. **Target Surface Highlight**
   - Semi-transparent overlay on candidate surface
   - Color indicates surface type (wall=indigo, floor=green)

2. **Snap Point Indicator**
   - Ring/circle at snap position
   - Animates when within snap threshold
   - Shows normal direction arrow

3. **Guide Lines**
   - Dashed line from object to snap point
   - Helps user understand snap relationship

### Placement Confirmation

1. **Snap Animation**
   - Brief ease-out motion to final position
   - Subtle haptic feedback (if available)

2. **Surface Attachment Indicator**
   - Brief glow on surface where attached
   - Confirms successful placement

---

## Reference Architecture

```
src/
├── state/
│   └── useCollisionStore.ts      # Unified surface registry
│
├── components/spatial/
│   ├── collision/
│   │   ├── useCollisionRaycast.ts    # BVH-accelerated raycasting
│   │   ├── useSurfaceSnapping.ts     # Snap logic during drag
│   │   ├── useHybridSurfaces.ts      # Merge XR + environment
│   │   ├── SnapIndicators.tsx        # Visual feedback components
│   │   └── CollisionDebugView.tsx    # Debug visualization
│   │
│   └── environment/
│       ├── Environment3DLoader.tsx   # GLTF loader with collision
│       ├── EnvironmentAlignment.tsx  # QR/manual alignment
│       └── EnvironmentLibrary.tsx    # Browse/load environments
│
├── utils/
│   ├── bvhRaycasting.ts             # three-mesh-bvh setup
│   └── snapPointCalculation.ts      # Snap point generation
│
└── types/
    └── collisionTypes.ts            # Surface, SnapPoint types
```

---

## Key Decisions Made

| Decision | Rationale |
|----------|-----------|
| Surface-first, not free-first | Matches platform guidelines, feels natural |
| XR priority over environment | Real surfaces more accurate |
| Environment as fallback | Enables AR anywhere |
| Unified surface registry | Single source of truth |
| BVH for custom environments | Performance at 90fps |
| Snap points, not continuous | Intentional placement |
| Relative persistence | Survives environment repositioning |

---

## References

- [Meta Horizon OS Panels](https://developers.meta.com/horizon/design/panels/)
- [Meta MR Design Guidelines](https://developers.meta.com/horizon/design/mr-design-guideline/)
- [visionOS Design Q&A](https://developer.apple.com/news/?id=fi8ne6ji)
- [IWSDK Spatial UI Guide](https://iwsdk.dev/guides/overview.html)
- [VR/MR UX Research](https://design4real.de/en/vr-user-experience/)
- [WebXR Hit Test Spec](https://www.w3.org/TR/webxr-hit-test-1/)
