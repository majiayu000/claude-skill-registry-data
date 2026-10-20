---
name: three-js-scene
description: "World Pulse: When adding or modifying 3D elements on the globe in `src/renderer/components/Globe/`."
---

# Three.js Scene

**When to use:** When adding or modifying 3D elements on the globe in `src/renderer/components/Globe/`.

---

## Stack

- `@react-three/fiber` (`Canvas`, `useFrame`, `useThree`) for React integration.
- `@react-three/drei` (`OrbitControls`) for camera controls.
- `three` (imported as `* as THREE`) for geometry, materials, and math.

---

## Globe Constants (from `Globe.tsx`)

```ts
const GLOBE_RADIUS = 1;          // canonical unit radius

// Oblivion palette for 3D
const OB_COLORS = {
  cyan: '#00D4FF',
  cyanDim: '#00D4FF',
  amber: '#FF8C42',
  danger: '#FF3D3D',
  atmosphere: '#00D4FF',
  stars: '#C8E6F0',
};
```

All 3D color values must reference `OB_COLORS`. Do not introduce new color literals.

---

## Geometry Conventions

| Object | Geometry | Segments | Notes |
|---|---|---|---|
| Globe surface | `sphereGeometry` | 96×48 | High fidelity for always-on display |
| Atmosphere glow | `sphereGeometry` | 64×32 | Scaled 1.06×, `THREE.BackSide` |
| Atmosphere ring | `ringGeometry` | 64 | Scaled 1.02×–1.12× |
| Wireframe overlay | `sphereGeometry` | 48×24 | Scaled 1.002×, `opacity: 0.06` |
| Event marker | `sphereGeometry` | 12×12 | `size: 0.015` normal, `0.025` featured |
| Event ring | `ringGeometry` | 24 | Radii `[0.02, 0.035]` |
| Stars | `bufferGeometry` (points) | 800 points | Distributed 8–23 units out |

---

## Animation Loop

Use `useFrame` for per-frame updates. Never use `setInterval` or `requestAnimationFrame` directly inside React components:

```tsx
useFrame(({ clock }, delta) => {
  if (!ref.current) return;
  // Use delta for frame-rate-independent rotation
  ref.current.rotation.y += delta * 0.06;  // Globe auto-rotation speed
});
```

`clock.elapsedTime` drives oscillating effects (pulse, glow). `delta` drives continuous motion.

---

## Lat/Lon to 3D Position

Always use the `latLonToVector3` helper from `earthTexture.ts`:

```ts
import { latLonToVector3 } from './earthTexture';

const position = latLonToVector3(lat, lon, GLOBE_RADIUS * 1.01); // place just above surface
```

Do not compute spherical coordinates manually.

---

## Frame Budget (Always-On Display)

Target: **60 fps** sustained on dedicated display hardware.

- Limit event markers to **30** (`slice(0, 30)`) — see `EventMarkers` component.
- Use `useMemo` for geometry/position calculations that don't change per frame.
- Use `useCallback` for click handlers passed to mesh objects.
- Material opacity is mutated directly on the material ref — do not call `setState` inside `useFrame`.
- Star geometry uses a `Float32Array` buffer attribute for performance (800 stars).

---

## Canvas Setup

```tsx
<Canvas
  camera={{ position: [0, 0.4, 2.6], fov: 45 }}
  style={{ background: 'transparent', width: '100%', height: '100%' }}
  gl={{ antialias: true, alpha: true }}
>
```

- `alpha: true` — the globe sits over the dark `--ob-bg-primary` body background.
- Never set a background color on the Canvas — the CSS body background shows through.
- `antialias: true` — required for edge quality on a 4K display.

---

## Lighting

```tsx
<ambientLight intensity={0.5} />
<directionalLight position={[5, 5, 5]} intensity={0.8} color={OB_COLORS.cyan} />
<hemisphereLight args={['#102030', '#000000', 0.3]} />
```

Do not add more lights without profiling. Always-on rendering is sensitive to overdraw.

---

## Anti-Patterns

- Do not use `@react-three/drei` loaders (`useGLTF`, `useTexture`) without a `<Suspense>` boundary.
- Do not call `set` on Zustand store from inside `useFrame` — it triggers re-renders. Read state via `useAppStore.getState()` inside the animation loop.
- Do not compute normals/UVs manually — use Three.js built-in geometry classes.
- Do not use `instancedMesh` without verifying the marker count stays below the instance limit.
