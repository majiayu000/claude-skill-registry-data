---
name: collision-points-3d
description: Implementing collision detection, surface snapping, and 3D environment support for StickerNest widgets. Use when the user asks about collision detection, physics, snap points, raycasting, 3D environments, BVH acceleration, Rapier physics, or widget snapping to surfaces. Covers state-of-the-art WebXR APIs, three-mesh-bvh, react-three-rapier, custom environment loading, and hybrid surface detection.
---

# Collision Points and 3D Environment Snapping for StickerNest

This skill guides you through implementing collision detection and surface snapping for widgets in 3D/VR/AR environments. It builds upon the existing spatial XR infrastructure and leverages state-of-the-art APIs.

## State-of-the-Art Technology Stack (2025)

### WebXR Specifications
| API | Purpose | Support |
|-----|---------|---------|
| [WebXR Plane Detection](https://immersive-web.github.io/real-world-geometry/plane-detection.html) | Detect walls, floors, tables | Quest 2/3, Vision Pro |
| [WebXR Mesh Detection](https://immersive-web.github.io/real-world-meshing/) | Full room geometry | Quest 3/3S, Vision Pro |
| [WebXR Hit Test](https://www.w3.org/TR/webxr-hit-test-1/) | Ray-surface intersection | All AR devices |
| [WebXR Anchors](https://immersive-web.github.io/anchors/) | Persistent world positions | Quest 2/3, Vision Pro |

### React/Three.js Libraries
| Library | Purpose | Install |
|---------|---------|---------|
| [@react-three/xr](https://github.com/pmndrs/xr) v6+ | WebXR React bindings | Already installed |
| [three-mesh-bvh](https://github.com/gkjohnson/three-mesh-bvh) | Accelerated raycasting | `npm install three-mesh-bvh` |
| [react-three-rapier](https://github.com/pmndrs/react-three-rapier) | Physics engine | `npm install @react-three/rapier` |

### Meta-Specific
| SDK | Purpose | Docs |
|-----|---------|------|
| [IWSDK](https://iwsdk.dev/) | Immersive Web SDK | Scene understanding, locomotion |
| [@iwsdk/locomotor](https://developers.meta.com/horizon/documentation/web/iwsdk-overview) | Physics-based movement | Already installed |

---

## Existing StickerNest Foundation

### Already Implemented
```
src/components/spatial/anchors/useSpatialAnchors.ts
├── useXRPlanes() - Plane detection by type
├── snapToSurface() - Basic surface snapping
├── getNearestSurface() - Find closest surface
└── createAnchor() - Persistent anchors

src/components/spatial/xr/RoomVisualizer.tsx
├── useXRPlanes() - All plane types
├── useXRMeshes() - Room mesh (Quest 3+)
└── Visual rendering of detected geometry
```

### What Needs to Be Added
1. **Custom 3D environment loading** with collision mesh extraction
2. **BVH-accelerated raycasting** against custom geometry
3. **Snap point system** for precise widget placement
4. **Visual feedback** during drag operations
5. **Hybrid surface detection** (XR planes + custom environments)
6. **Collision store** for managing surfaces

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    COLLISION SYSTEM                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │ XR Planes    │    │ XR Meshes    │    │ Custom 3D    │      │
│  │ (WebXR API)  │    │ (Quest 3+)   │    │ Environments │      │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘      │
│         │                   │                   │               │
│         └───────────────────┼───────────────────┘               │
│                             ▼                                    │
│              ┌──────────────────────────────┐                   │
│              │    Unified Collision Store    │                   │
│              │    (useCollisionStore.ts)     │                   │
│              └──────────────┬───────────────┘                   │
│                             │                                    │
│         ┌───────────────────┼───────────────────┐               │
│         ▼                   ▼                   ▼               │
│  ┌──────────────┐  ┌──────────────────┐  ┌──────────────┐      │
│  │ BVH Raycast  │  │  Snap Points     │  │ Visual       │      │
│  │ System       │  │  Calculator      │  │ Indicators   │      │
│  └──────────────┘  └──────────────────┘  └──────────────┘      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Phase 1: BVH-Accelerated Raycasting

### Installing three-mesh-bvh

```bash
npm install three-mesh-bvh
```

### Basic BVH Setup

```typescript
// src/utils/bvhRaycasting.ts
import {
  MeshBVH,
  acceleratedRaycast,
  computeBoundsTree,
  disposeBoundsTree,
} from 'three-mesh-bvh';
import * as THREE from 'three';

// Extend THREE.Mesh prototype with BVH methods
THREE.Mesh.prototype.raycast = acceleratedRaycast;
THREE.BufferGeometry.prototype.computeBoundsTree = computeBoundsTree;
THREE.BufferGeometry.prototype.disposeBoundsTree = disposeBoundsTree;

/**
 * Create BVH for a mesh to accelerate raycasting
 * Can handle 500+ rays against 80k polygon model at 60fps
 */
export function createMeshBVH(mesh: THREE.Mesh): MeshBVH | null {
  if (!mesh.geometry) return null;

  // Compute BVH - this may take a moment for large meshes
  mesh.geometry.computeBoundsTree({
    maxLeafTris: 5,           // Triangles per leaf node
    strategy: 0,               // SAH (Surface Area Heuristic)
  });

  return mesh.geometry.boundsTree as MeshBVH;
}

/**
 * Dispose BVH when no longer needed
 */
export function disposeMeshBVH(mesh: THREE.Mesh): void {
  if (mesh.geometry?.boundsTree) {
    mesh.geometry.disposeBoundsTree();
  }
}
```

### BVH Raycasting Hook

```typescript
// src/components/spatial/collision/useBVHRaycast.ts
import { useCallback, useRef } from 'react';
import { useFrame, useThree } from '@react-three/fiber';
import { Raycaster, Vector3, Object3D, Intersection } from 'three';
import { createMeshBVH } from '../../../utils/bvhRaycasting';

interface BVHRaycastResult {
  hit: boolean;
  point: Vector3;
  normal: Vector3;
  distance: number;
  object: Object3D | null;
  faceIndex: number;
}

interface UseBVHRaycastOptions {
  /** Objects to raycast against (must have BVH computed) */
  targets: Object3D[];
  /** Only return first hit (faster) */
  firstHitOnly?: boolean;
  /** Max distance to check */
  maxDistance?: number;
}

export function useBVHRaycast(options: UseBVHRaycastOptions) {
  const { targets, firstHitOnly = true, maxDistance = 100 } = options;
  const raycasterRef = useRef(new Raycaster());

  // Configure raycaster for BVH optimization
  raycasterRef.current.firstHitOnly = firstHitOnly;
  raycasterRef.current.far = maxDistance;

  const raycast = useCallback(
    (origin: Vector3, direction: Vector3): BVHRaycastResult => {
      const raycaster = raycasterRef.current;
      raycaster.set(origin, direction.normalize());

      const intersects = raycaster.intersectObjects(targets, true);

      if (intersects.length === 0) {
        return {
          hit: false,
          point: new Vector3(),
          normal: new Vector3(),
          distance: Infinity,
          object: null,
          faceIndex: -1,
        };
      }

      const hit = intersects[0];
      return {
        hit: true,
        point: hit.point.clone(),
        normal: hit.face?.normal.clone() ?? new Vector3(0, 1, 0),
        distance: hit.distance,
        object: hit.object,
        faceIndex: hit.faceIndex ?? -1,
      };
    },
    [targets]
  );

  return { raycast };
}
```

### React Three Fiber BVH Component

```tsx
// Using @react-three/drei Bvh component (easier setup)
import { Bvh } from '@react-three/drei';

function CollisionScene({ children }) {
  return (
    <Bvh firstHitOnly>
      {/* All children get accelerated raycasting */}
      {children}
    </Bvh>
  );
}
```

---

## Phase 2: Custom 3D Environment Loading

### Environment Loader Component

```tsx
// src/components/spatial/environment/Environment3DLoader.tsx
import { useGLTF, useAnimations } from '@react-three/drei';
import { useEffect, useMemo, useRef } from 'react';
import { Group, Mesh, BufferGeometry, Object3D } from 'three';
import { createMeshBVH, disposeMeshBVH } from '../../../utils/bvhRaycasting';

interface Environment3DProps {
  /** URL to GLTF/GLB file */
  modelUrl: string;
  /** Called when environment loads with collision meshes */
  onLoad?: (scene: Group, collisionMeshes: Mesh[]) => void;
  /** Scale factor */
  scale?: number;
  /** Position offset */
  position?: [number, number, number];
}

/**
 * Naming conventions for collision meshes in GLTF:
 * - *_collision - Any collision mesh
 * - *_wall - Wall collision
 * - *_floor - Floor collision
 * - *_ceiling - Ceiling collision
 * - Objects with userData.collision = true
 */
function isCollisionMesh(object: Object3D): object is Mesh {
  if (!(object instanceof Mesh)) return false;

  const name = object.name.toLowerCase();

  // Check naming conventions
  if (name.includes('_collision')) return true;
  if (name.includes('_wall')) return true;
  if (name.includes('_floor')) return true;
  if (name.includes('_ceiling')) return true;
  if (name.includes('_table')) return true;

  // Check userData
  if (object.userData.collision === true) return true;
  if (object.userData.collider) return true;

  return false;
}

function getSurfaceType(name: string): 'wall' | 'floor' | 'ceiling' | 'table' | 'custom' {
  const lower = name.toLowerCase();
  if (lower.includes('wall')) return 'wall';
  if (lower.includes('floor')) return 'floor';
  if (lower.includes('ceiling')) return 'ceiling';
  if (lower.includes('table')) return 'table';
  return 'custom';
}

export function Environment3DLoader({
  modelUrl,
  onLoad,
  scale = 1,
  position = [0, 0, 0],
}: Environment3DProps) {
  const { scene, animations } = useGLTF(modelUrl);
  const groupRef = useRef<Group>(null);
  const { actions } = useAnimations(animations, groupRef);

  // Extract and setup collision meshes
  const collisionMeshes = useMemo(() => {
    const meshes: Mesh[] = [];

    scene.traverse((child) => {
      if (isCollisionMesh(child)) {
        // Clone to avoid modifying original
        const collisionMesh = child.clone();

        // Apply BVH for fast raycasting
        createMeshBVH(collisionMesh);

        // Add metadata
        collisionMesh.userData.surfaceType = getSurfaceType(child.name);
        collisionMesh.userData.isCollisionMesh = true;

        // Make invisible (collision only)
        collisionMesh.visible = false;

        meshes.push(collisionMesh);
      }
    });

    return meshes;
  }, [scene]);

  // Notify parent when loaded
  useEffect(() => {
    if (groupRef.current && collisionMeshes.length > 0) {
      onLoad?.(groupRef.current, collisionMeshes);
    }
  }, [collisionMeshes, onLoad]);

  // Cleanup BVH on unmount
  useEffect(() => {
    return () => {
      collisionMeshes.forEach(disposeMeshBVH);
    };
  }, [collisionMeshes]);

  return (
    <group ref={groupRef} position={position} scale={scale}>
      {/* Visible scene */}
      <primitive object={scene.clone()} />

      {/* Collision meshes (invisible) */}
      {collisionMeshes.map((mesh, i) => (
        <primitive key={i} object={mesh} />
      ))}
    </group>
  );
}

// Preload model
Environment3DLoader.preload = (url: string) => {
  useGLTF.preload(url);
};
```

### Collision Store

```typescript
// src/state/useCollisionStore.ts
import { create } from 'zustand';
import { Vector3, Quaternion, Mesh, Box3 } from 'three';

export interface CollisionSurface {
  id: string;
  type: 'wall' | 'floor' | 'ceiling' | 'table' | 'custom';
  source: 'xr-plane' | 'environment' | 'manual';

  // Reference to Three.js mesh (for raycasting)
  mesh: Mesh | null;

  // Computed bounds
  boundingBox: Box3;
  centroid: Vector3;
  normal: Vector3;

  // Snap points on this surface
  snapPoints: SnapPoint[];

  // Metadata
  environmentId?: string;
  label?: string;
}

export interface SnapPoint {
  id: string;
  surfaceId: string;
  position: Vector3;
  normal: Vector3;
  rotation: Quaternion;
  type: 'center' | 'edge' | 'corner' | 'grid';
}

interface CollisionState {
  // All registered collision surfaces
  surfaces: Map<string, CollisionSurface>;

  // Currently active surfaces (filtered by mode/environment)
  activeSurfaces: string[];

  // Settings
  snapEnabled: boolean;
  snapThreshold: number; // meters
  showDebugVisualization: boolean;

  // Actions
  registerSurface: (surface: CollisionSurface) => void;
  unregisterSurface: (id: string) => void;
  registerEnvironmentSurfaces: (environmentId: string, surfaces: CollisionSurface[]) => void;
  clearEnvironmentSurfaces: (environmentId: string) => void;

  setSnapEnabled: (enabled: boolean) => void;
  setSnapThreshold: (threshold: number) => void;
  setShowDebug: (show: boolean) => void;

  // Queries
  getSurfacesByType: (type: CollisionSurface['type']) => CollisionSurface[];
  getNearestSurface: (position: Vector3, maxDistance?: number) => CollisionSurface | null;
  getNearestSnapPoint: (position: Vector3, surfaceTypes?: CollisionSurface['type'][]) => SnapPoint | null;
}

export const useCollisionStore = create<CollisionState>((set, get) => ({
  surfaces: new Map(),
  activeSurfaces: [],
  snapEnabled: true,
  snapThreshold: 0.15, // 15cm
  showDebugVisualization: false,

  registerSurface: (surface) => {
    set((state) => {
      const newSurfaces = new Map(state.surfaces);
      newSurfaces.set(surface.id, surface);
      return { surfaces: newSurfaces };
    });
  },

  unregisterSurface: (id) => {
    set((state) => {
      const newSurfaces = new Map(state.surfaces);
      newSurfaces.delete(id);
      return { surfaces: newSurfaces };
    });
  },

  registerEnvironmentSurfaces: (environmentId, surfaces) => {
    set((state) => {
      const newSurfaces = new Map(state.surfaces);
      surfaces.forEach((s) => {
        s.environmentId = environmentId;
        newSurfaces.set(s.id, s);
      });
      return { surfaces: newSurfaces };
    });
  },

  clearEnvironmentSurfaces: (environmentId) => {
    set((state) => {
      const newSurfaces = new Map(state.surfaces);
      for (const [id, surface] of newSurfaces) {
        if (surface.environmentId === environmentId) {
          newSurfaces.delete(id);
        }
      }
      return { surfaces: newSurfaces };
    });
  },

  setSnapEnabled: (enabled) => set({ snapEnabled: enabled }),
  setSnapThreshold: (threshold) => set({ snapThreshold: threshold }),
  setShowDebug: (show) => set({ showDebugVisualization: show }),

  getSurfacesByType: (type) => {
    const { surfaces } = get();
    return Array.from(surfaces.values()).filter((s) => s.type === type);
  },

  getNearestSurface: (position, maxDistance = 10) => {
    const { surfaces } = get();
    let nearest: CollisionSurface | null = null;
    let minDist = maxDistance;

    for (const surface of surfaces.values()) {
      const dist = position.distanceTo(surface.centroid);
      if (dist < minDist) {
        minDist = dist;
        nearest = surface;
      }
    }

    return nearest;
  },

  getNearestSnapPoint: (position, surfaceTypes) => {
    const { surfaces, snapThreshold } = get();
    let nearest: SnapPoint | null = null;
    let minDist = snapThreshold;

    for (const surface of surfaces.values()) {
      if (surfaceTypes && !surfaceTypes.includes(surface.type)) continue;

      for (const snapPoint of surface.snapPoints) {
        const dist = position.distanceTo(snapPoint.position);
        if (dist < minDist) {
          minDist = dist;
          nearest = snapPoint;
        }
      }
    }

    return nearest;
  },
}));
```

---

## Phase 3: Snap Point Generation

### Snap Point Calculator

```typescript
// src/utils/snapPointCalculation.ts
import { Vector3, Quaternion, BufferGeometry, Box3, Mesh } from 'three';
import { SnapPoint } from '../state/useCollisionStore';

/**
 * Generate snap points for a collision surface
 */
export function generateSnapPoints(
  surfaceId: string,
  mesh: Mesh,
  options: {
    includeCenter?: boolean;
    includeEdges?: boolean;
    includeGrid?: boolean;
    gridSpacing?: number; // meters
  } = {}
): SnapPoint[] {
  const {
    includeCenter = true,
    includeEdges = true,
    includeGrid = false,
    gridSpacing = 0.25,
  } = options;

  const snapPoints: SnapPoint[] = [];
  const geometry = mesh.geometry;

  if (!geometry) return snapPoints;

  // Compute bounding box
  geometry.computeBoundingBox();
  const bbox = geometry.boundingBox!;

  // Calculate surface normal (simplified - assumes flat surface)
  const normal = new Vector3();
  if (mesh.userData.surfaceType === 'floor') {
    normal.set(0, 1, 0);
  } else if (mesh.userData.surfaceType === 'ceiling') {
    normal.set(0, -1, 0);
  } else {
    // Wall - use forward direction
    normal.set(0, 0, 1);
    normal.applyQuaternion(mesh.quaternion);
  }

  // Center snap point
  if (includeCenter) {
    const center = new Vector3();
    bbox.getCenter(center);
    center.applyMatrix4(mesh.matrixWorld);

    snapPoints.push({
      id: `${surfaceId}-center`,
      surfaceId,
      position: center,
      normal: normal.clone(),
      rotation: quaternionFromNormal(normal),
      type: 'center',
    });
  }

  // Corner snap points
  if (includeEdges) {
    const corners = [
      new Vector3(bbox.min.x, bbox.min.y, bbox.min.z),
      new Vector3(bbox.max.x, bbox.min.y, bbox.min.z),
      new Vector3(bbox.min.x, bbox.max.y, bbox.min.z),
      new Vector3(bbox.max.x, bbox.max.y, bbox.min.z),
      new Vector3(bbox.min.x, bbox.min.y, bbox.max.z),
      new Vector3(bbox.max.x, bbox.min.y, bbox.max.z),
      new Vector3(bbox.min.x, bbox.max.y, bbox.max.z),
      new Vector3(bbox.max.x, bbox.max.y, bbox.max.z),
    ];

    corners.forEach((corner, i) => {
      corner.applyMatrix4(mesh.matrixWorld);
      snapPoints.push({
        id: `${surfaceId}-corner-${i}`,
        surfaceId,
        position: corner,
        normal: normal.clone(),
        rotation: quaternionFromNormal(normal),
        type: 'corner',
      });
    });
  }

  // Grid snap points
  if (includeGrid) {
    const size = new Vector3();
    bbox.getSize(size);

    const countX = Math.floor(size.x / gridSpacing);
    const countY = Math.floor(size.y / gridSpacing);
    const countZ = Math.floor(size.z / gridSpacing);

    for (let x = 0; x <= countX; x++) {
      for (let y = 0; y <= countY; y++) {
        for (let z = 0; z <= countZ; z++) {
          const pos = new Vector3(
            bbox.min.x + x * gridSpacing,
            bbox.min.y + y * gridSpacing,
            bbox.min.z + z * gridSpacing
          );
          pos.applyMatrix4(mesh.matrixWorld);

          snapPoints.push({
            id: `${surfaceId}-grid-${x}-${y}-${z}`,
            surfaceId,
            position: pos,
            normal: normal.clone(),
            rotation: quaternionFromNormal(normal),
            type: 'grid',
          });
        }
      }
    }
  }

  return snapPoints;
}

/**
 * Calculate rotation quaternion to face away from surface
 */
function quaternionFromNormal(normal: Vector3): Quaternion {
  const quaternion = new Quaternion();
  const up = new Vector3(0, 1, 0);

  // Handle degenerate case (normal pointing up/down)
  if (Math.abs(normal.dot(up)) > 0.99) {
    up.set(0, 0, 1);
  }

  const right = new Vector3().crossVectors(up, normal).normalize();
  const adjustedUp = new Vector3().crossVectors(normal, right).normalize();

  const matrix = new THREE.Matrix4();
  matrix.makeBasis(right, adjustedUp, normal);
  quaternion.setFromRotationMatrix(matrix);

  return quaternion;
}

/**
 * Project a point onto a surface
 */
export function projectPointToSurface(
  point: Vector3,
  surfacePoint: Vector3,
  surfaceNormal: Vector3
): Vector3 {
  const diff = new Vector3().subVectors(point, surfacePoint);
  const distance = diff.dot(surfaceNormal);
  return new Vector3().subVectors(point, surfaceNormal.clone().multiplyScalar(distance));
}
```

---

## Phase 4: Visual Snap Feedback

### Snap Indicator Components

```tsx
// src/components/spatial/collision/SnapIndicators.tsx
import { useRef } from 'react';
import { useFrame } from '@react-three/fiber';
import { Ring, Sphere, Line } from '@react-three/drei';
import { Vector3, Quaternion } from 'three';

interface SnapPreviewProps {
  position: Vector3;
  normal: Vector3;
  rotation: Quaternion;
  active: boolean;
  surfaceType: 'wall' | 'floor' | 'ceiling' | 'table' | 'custom';
}

const SURFACE_COLORS = {
  wall: '#6366f1',
  floor: '#22c55e',
  ceiling: '#f59e0b',
  table: '#8b5cf6',
  custom: '#ffffff',
};

export function SnapPreview({
  position,
  normal,
  rotation,
  active,
  surfaceType,
}: SnapPreviewProps) {
  const ringRef = useRef<THREE.Mesh>(null);
  const color = SURFACE_COLORS[surfaceType];

  // Animate ring
  useFrame((state) => {
    if (!ringRef.current) return;
    const scale = active
      ? 1 + Math.sin(state.clock.elapsedTime * 4) * 0.1
      : 1;
    ringRef.current.scale.setScalar(scale);
  });

  return (
    <group position={position} quaternion={rotation}>
      {/* Snap ring */}
      <Ring
        ref={ringRef}
        args={[0.08, 0.12, 32]}
        rotation={[-Math.PI / 2, 0, 0]}
      >
        <meshBasicMaterial
          color={active ? '#22c55e' : color}
          transparent
          opacity={active ? 0.9 : 0.5}
        />
      </Ring>

      {/* Normal direction indicator */}
      {active && (
        <Line
          points={[[0, 0, 0], [0, 0.15, 0]]}
          color="#22c55e"
          lineWidth={2}
        />
      )}

      {/* Center dot */}
      <Sphere args={[0.015, 16, 16]} position={[0, 0.001, 0]}>
        <meshBasicMaterial color={active ? '#ffffff' : color} />
      </Sphere>
    </group>
  );
}

interface SurfaceHighlightProps {
  surfaceId: string;
  mesh: THREE.Mesh;
  intensity: number; // 0-1
  color?: string;
}

export function SurfaceHighlight({
  mesh,
  intensity,
  color = '#8b5cf6',
}: SurfaceHighlightProps) {
  return (
    <primitive object={mesh.clone()}>
      <meshBasicMaterial
        color={color}
        transparent
        opacity={intensity * 0.3}
        depthWrite={false}
      />
    </primitive>
  );
}

interface SnapGuideLinesProps {
  from: Vector3;
  to: Vector3;
  color?: string;
}

export function SnapGuideLines({ from, to, color = '#22c55e' }: SnapGuideLinesProps) {
  return (
    <Line
      points={[from.toArray(), to.toArray()]}
      color={color}
      lineWidth={1}
      dashed
      dashSize={0.05}
      gapSize={0.03}
    />
  );
}
```

### Collision Debug View

```tsx
// src/components/spatial/collision/CollisionDebugView.tsx
import { useCollisionStore } from '../../../state/useCollisionStore';
import { Text } from '@react-three/drei';

export function CollisionDebugView() {
  const surfaces = useCollisionStore((s) => s.surfaces);
  const showDebug = useCollisionStore((s) => s.showDebugVisualization);

  if (!showDebug) return null;

  return (
    <group name="collision-debug">
      {Array.from(surfaces.values()).map((surface) => (
        <group key={surface.id}>
          {/* Surface wireframe */}
          {surface.mesh && (
            <primitive object={surface.mesh.clone()}>
              <meshBasicMaterial
                color={getSurfaceColor(surface.type)}
                wireframe
                transparent
                opacity={0.3}
              />
            </primitive>
          )}

          {/* Surface label */}
          <Text
            position={surface.centroid.toArray()}
            fontSize={0.05}
            color="white"
            anchorX="center"
            outlineWidth={0.003}
            outlineColor="black"
          >
            {surface.type} ({surface.source})
          </Text>

          {/* Snap points */}
          {surface.snapPoints.map((sp) => (
            <mesh key={sp.id} position={sp.position}>
              <sphereGeometry args={[0.02, 8, 8]} />
              <meshBasicMaterial color="#22c55e" />
            </mesh>
          ))}
        </group>
      ))}
    </group>
  );
}

function getSurfaceColor(type: string): string {
  const colors: Record<string, string> = {
    wall: '#6366f1',
    floor: '#22c55e',
    ceiling: '#f59e0b',
    table: '#8b5cf6',
    custom: '#ffffff',
  };
  return colors[type] || '#ffffff';
}
```

---

## Phase 5: Surface Snapping Hook

### Complete Snapping Integration

```typescript
// src/components/spatial/collision/useSurfaceSnapping.ts
import { useCallback, useState, useRef } from 'react';
import { useFrame, useThree } from '@react-three/fiber';
import { Vector3, Quaternion, Raycaster } from 'three';
import { useCollisionStore, SnapPoint, CollisionSurface } from '../../../state/useCollisionStore';

interface SnappingState {
  isSnapping: boolean;
  snapTarget: SnapPoint | null;
  previewPosition: Vector3 | null;
  previewRotation: Quaternion | null;
  targetSurface: CollisionSurface | null;
}

interface UseSurfaceSnappingOptions {
  /** Enable snapping behavior */
  enabled?: boolean;
  /** Surface types to snap to */
  surfaceTypes?: CollisionSurface['type'][];
  /** Custom snap threshold (overrides store) */
  snapThreshold?: number;
  /** Callback when snap target changes */
  onSnapChange?: (snapPoint: SnapPoint | null) => void;
}

export function useSurfaceSnapping(options: UseSurfaceSnappingOptions = {}) {
  const {
    enabled = true,
    surfaceTypes,
    snapThreshold: customThreshold,
    onSnapChange,
  } = options;

  const { camera, raycaster } = useThree();

  const surfaces = useCollisionStore((s) => s.surfaces);
  const storeSnapThreshold = useCollisionStore((s) => s.snapThreshold);
  const snapEnabled = useCollisionStore((s) => s.snapEnabled);

  const snapThreshold = customThreshold ?? storeSnapThreshold;

  const [state, setState] = useState<SnappingState>({
    isSnapping: false,
    snapTarget: null,
    previewPosition: null,
    previewRotation: null,
    targetSurface: null,
  });

  const lastSnapPointRef = useRef<string | null>(null);

  /**
   * Update snapping based on current position
   */
  const updateSnapping = useCallback(
    (worldPosition: Vector3) => {
      if (!enabled || !snapEnabled) {
        setState((s) => ({
          ...s,
          isSnapping: false,
          snapTarget: null,
          previewPosition: null,
          previewRotation: null,
          targetSurface: null,
        }));
        return;
      }

      // Find nearest snap point
      let nearestPoint: SnapPoint | null = null;
      let nearestSurface: CollisionSurface | null = null;
      let minDist = snapThreshold;

      for (const surface of surfaces.values()) {
        // Filter by surface type
        if (surfaceTypes && !surfaceTypes.includes(surface.type)) continue;

        for (const snapPoint of surface.snapPoints) {
          const dist = worldPosition.distanceTo(snapPoint.position);
          if (dist < minDist) {
            minDist = dist;
            nearestPoint = snapPoint;
            nearestSurface = surface;
          }
        }
      }

      // Notify if snap target changed
      if (nearestPoint?.id !== lastSnapPointRef.current) {
        lastSnapPointRef.current = nearestPoint?.id ?? null;
        onSnapChange?.(nearestPoint);
      }

      setState({
        isSnapping: nearestPoint !== null,
        snapTarget: nearestPoint,
        previewPosition: nearestPoint?.position ?? null,
        previewRotation: nearestPoint?.rotation ?? null,
        targetSurface: nearestSurface,
      });
    },
    [enabled, snapEnabled, surfaces, surfaceTypes, snapThreshold, onSnapChange]
  );

  /**
   * Raycast from camera to find surface intersection
   */
  const raycastToSurface = useCallback(
    (screenPosition: { x: number; y: number }) => {
      if (!enabled) return null;

      raycaster.setFromCamera(screenPosition, camera);

      const meshes = Array.from(surfaces.values())
        .filter((s) => s.mesh && (!surfaceTypes || surfaceTypes.includes(s.type)))
        .map((s) => s.mesh!);

      const intersects = raycaster.intersectObjects(meshes, true);

      if (intersects.length > 0) {
        const hit = intersects[0];
        return {
          point: hit.point.clone(),
          normal: hit.face?.normal.clone().applyQuaternion(hit.object.quaternion) ?? new Vector3(0, 1, 0),
          surface: surfaces.get(hit.object.userData.surfaceId) ?? null,
        };
      }

      return null;
    },
    [enabled, camera, raycaster, surfaces, surfaceTypes]
  );

  /**
   * Confirm snap and return final position
   */
  const confirmSnap = useCallback((): { position: Vector3; rotation: Quaternion } | null => {
    if (!state.snapTarget) return null;

    return {
      position: state.snapTarget.position.clone(),
      rotation: state.snapTarget.rotation.clone(),
    };
  }, [state.snapTarget]);

  /**
   * Cancel snapping
   */
  const cancelSnapping = useCallback(() => {
    lastSnapPointRef.current = null;
    setState({
      isSnapping: false,
      snapTarget: null,
      previewPosition: null,
      previewRotation: null,
      targetSurface: null,
    });
  }, []);

  return {
    ...state,
    updateSnapping,
    raycastToSurface,
    confirmSnap,
    cancelSnapping,
  };
}
```

---

## Phase 6: Hybrid XR + Environment Surfaces

### Merging XR Planes with Custom Environments

```typescript
// src/components/spatial/collision/useHybridSurfaces.ts
import { useEffect } from 'react';
import { useXRPlanes, useXRMeshes } from '@react-three/xr';
import { Vector3, Box3, Mesh, BufferGeometry } from 'three';
import { useCollisionStore, CollisionSurface } from '../../../state/useCollisionStore';
import { generateSnapPoints } from '../../../utils/snapPointCalculation';

/**
 * Merges WebXR detected planes/meshes with custom environment collision surfaces.
 *
 * Priority:
 * 1. XR planes take precedence (more accurate to real world)
 * 2. Environment surfaces fill gaps where XR detection is unavailable
 */
export function useHybridSurfaces(options: {
  /** Use XR planes when available */
  useXRPlanes?: boolean;
  /** Use XR meshes when available (Quest 3+) */
  useXRMeshes?: boolean;
  /** Fallback environment ID when XR surfaces unavailable */
  fallbackEnvironmentId?: string;
}) {
  const {
    useXRPlanes: enableXRPlanes = true,
    useXRMeshes: enableXRMeshes = true,
    fallbackEnvironmentId,
  } = options;

  // Get XR detected geometry
  const xrWalls = useXRPlanes('wall');
  const xrFloors = useXRPlanes('floor');
  const xrCeilings = useXRPlanes('ceiling');
  const xrTables = useXRPlanes('table');
  const xrMeshes = useXRMeshes();

  const registerSurface = useCollisionStore((s) => s.registerSurface);
  const unregisterSurface = useCollisionStore((s) => s.unregisterSurface);
  const surfaces = useCollisionStore((s) => s.surfaces);

  // Register XR planes as collision surfaces
  useEffect(() => {
    if (!enableXRPlanes) return;

    const allPlanes = [
      ...xrWalls.map((p) => ({ plane: p, type: 'wall' as const })),
      ...xrFloors.map((p) => ({ plane: p, type: 'floor' as const })),
      ...xrCeilings.map((p) => ({ plane: p, type: 'ceiling' as const })),
      ...xrTables.map((p) => ({ plane: p, type: 'table' as const })),
    ];

    const registeredIds: string[] = [];

    for (const { plane, type } of allPlanes) {
      const id = `xr-plane-${plane.planeSpace.toString()}`;

      // Calculate centroid from polygon
      let cx = 0, cy = 0, cz = 0;
      for (const point of plane.polygon) {
        cx += point.x;
        cy += point.y;
        cz += point.z;
      }
      const centroid = new Vector3(
        cx / plane.polygon.length,
        cy / plane.polygon.length,
        cz / plane.polygon.length
      );

      // Determine normal based on type
      const normal = new Vector3();
      if (type === 'floor') normal.set(0, 1, 0);
      else if (type === 'ceiling') normal.set(0, -1, 0);
      else normal.set(0, 0, 1); // Simplified for walls

      const surface: CollisionSurface = {
        id,
        type,
        source: 'xr-plane',
        mesh: null, // XR planes don't have Three.js mesh
        boundingBox: new Box3(), // Would need to compute from polygon
        centroid,
        normal,
        snapPoints: [], // Generate after registration
      };

      registerSurface(surface);
      registeredIds.push(id);
    }

    // Cleanup on change
    return () => {
      registeredIds.forEach(unregisterSurface);
    };
  }, [xrWalls, xrFloors, xrCeilings, xrTables, enableXRPlanes, registerSurface, unregisterSurface]);

  // Check if XR surfaces are available
  const hasXRSurfaces = xrWalls.length > 0 || xrFloors.length > 0 || xrMeshes.length > 0;

  // Determine which environment surfaces to use
  useEffect(() => {
    if (hasXRSurfaces) {
      // XR surfaces available - environment surfaces are secondary
      // Could implement overlap detection here to avoid duplicates
    } else if (fallbackEnvironmentId) {
      // No XR surfaces - rely entirely on environment collision
      console.log('[Hybrid Surfaces] Using environment fallback:', fallbackEnvironmentId);
    }
  }, [hasXRSurfaces, fallbackEnvironmentId]);

  return {
    hasXRSurfaces,
    xrPlaneCount: xrWalls.length + xrFloors.length + xrCeilings.length + xrTables.length,
    xrMeshCount: xrMeshes.length,
    totalSurfaces: surfaces.size,
  };
}
```

---

## Phase 7: Rapier Physics (Optional)

For advanced physics simulation (gravity, rigid bodies):

### Setup

```bash
npm install @react-three/rapier
```

### Physics World with Collision

```tsx
// src/components/spatial/collision/PhysicsWorld.tsx
import { Physics, RigidBody, CuboidCollider, MeshCollider } from '@react-three/rapier';

function PhysicsEnabledScene({ children, environmentMesh }) {
  return (
    <Physics gravity={[0, -9.81, 0]} debug>
      {/* Environment as static collider */}
      {environmentMesh && (
        <RigidBody type="fixed" colliders={false}>
          <MeshCollider type="trimesh">
            <primitive object={environmentMesh} />
          </MeshCollider>
        </RigidBody>
      )}

      {/* Dynamic objects */}
      {children}
    </Physics>
  );
}

function PhysicsWidget({ position, children }) {
  return (
    <RigidBody position={position} colliders="cuboid">
      {children}
    </RigidBody>
  );
}
```

---

## Integration with Existing StickerNest Code

### Extending SpatialWidgetContainer

```typescript
// In src/components/spatial/SpatialWidgetContainer.tsx
// Add to existing drag handling (around line 490-536)

import { useSurfaceSnapping } from './collision/useSurfaceSnapping';
import { SnapPreview } from './collision/SnapIndicators';

function SpatialWidgetContainer({ widget }) {
  // Add snapping hook
  const {
    isSnapping,
    snapTarget,
    previewPosition,
    previewRotation,
    updateSnapping,
    confirmSnap,
  } = useSurfaceSnapping({
    enabled: isGrabbing,
    surfaceTypes: ['wall', 'floor', 'table'],
  });

  // In useFrame or drag handler
  useFrame(() => {
    if (isGrabbing && currentPosition) {
      updateSnapping(currentPosition);
    }
  });

  // On release
  const handleRelease = () => {
    if (isSnapping) {
      const snapped = confirmSnap();
      if (snapped) {
        setWidgetPosition(snapped.position);
        setWidgetRotation(snapped.rotation);
      }
    }
    setIsGrabbing(false);
  };

  return (
    <>
      {/* Existing widget render */}

      {/* Snap preview */}
      {isSnapping && snapTarget && (
        <SnapPreview
          position={previewPosition!}
          normal={snapTarget.normal}
          rotation={previewRotation!}
          active={true}
          surfaceType={targetSurface?.type ?? 'custom'}
        />
      )}
    </>
  );
}
```

---

## Device Compatibility Matrix

| Feature | Quest 2 | Quest 3/3S | Vision Pro | Android AR |
|---------|---------|------------|------------|------------|
| Plane Detection | ✅ | ✅ | ✅ | ✅ |
| Mesh Detection | ❌ | ✅ | ✅ | ❌ |
| Custom 3D Env | ✅ | ✅ | ✅ | ✅ |
| BVH Raycasting | ✅ | ✅ | ✅ | ✅ |
| Persistent Anchors | ✅ | ✅ | ✅ | ❌ |
| Rapier Physics | ✅ | ✅ | ✅ | ✅ |

---

## Reference Files

- **Existing Spatial Anchors**: `src/components/spatial/anchors/useSpatialAnchors.ts`
- **Room Visualizer**: `src/components/spatial/xr/RoomVisualizer.tsx`
- **Spatial Sticker Store**: `src/state/useSpatialStickerStore.ts`
- **Spatial Mode Store**: `src/state/useSpatialModeStore.ts`
- **Widget Container**: `src/components/spatial/SpatialWidgetContainer.tsx`

---

## External Resources

- [three-mesh-bvh](https://github.com/gkjohnson/three-mesh-bvh) - BVH acceleration
- [react-three-rapier](https://github.com/pmndrs/react-three-rapier) - Physics engine
- [@react-three/xr](https://pmndrs.github.io/xr/docs/tutorials/object-detection) - Object detection docs
- [WebXR Plane Detection Spec](https://immersive-web.github.io/real-world-geometry/plane-detection.html)
- [Meta IWSDK Scene Understanding](https://developers.meta.com/horizon/documentation/web/iwsdk-guide-scene-understanding/)
- [GLTF Physics Extensions](https://github.com/KhronosGroup/glTF/pull/2424)
