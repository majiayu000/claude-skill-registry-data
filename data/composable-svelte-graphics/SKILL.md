---
name: composable-svelte-graphics
description: 3D graphics and WebGPU/WebGL rendering with Composable Svelte. Use when building 3D scenes, working with cameras, lights, meshes, materials, or implementing WebGPU/WebGL graphics. Covers Scene, Camera, Light, Mesh components, geometry types (box, sphere, cylinder, torus, plane), material properties, and state-driven 3D rendering.
---

# Composable Svelte Graphics

State-driven 3D graphics for Composable Svelte using WebGPU/WebGL with Babylon.js.

---

## PACKAGE OVERVIEW

**Package**: `@composable-svelte/graphics`

**Purpose**: Declarative 3D graphics with automatic WebGPU/WebGL renderer selection.

**Technology Stack**:
- **Babylon.js**: Industry-standard 3D engine
- **WebGPU**: Modern high-performance graphics API (auto-detected)
- **WebGL**: Fallback for broader browser support

**Renderer Selection**:
1. Try WebGPU (if browser supports it)
2. Fallback to WebGL (universal support)
3. Transparent to the user

**Core Components**:
- `Scene` - Root container, manages renderer lifecycle
- `Camera` - Viewpoint and projection
- `Light` - Illumination (ambient, directional, point, spot)
- `Mesh` - 3D objects with geometry and materials

**State Management**:
- `graphicsReducer` - Pure reducer for all graphics state
- `createInitialGraphicsState()` - Initial state factory
- Store-driven updates sync automatically to Babylon.js

---

## QUICK START

```typescript
import { createStore } from '@composable-svelte/core';
import {
  Scene,
  Camera,
  Light,
  Mesh,
  graphicsReducer,
  createInitialGraphicsState
} from '@composable-svelte/graphics';

// Create graphics store
const store = createStore({
  initialState: createInitialGraphicsState({
    backgroundColor: '#1a1a2e'
  }),
  reducer: graphicsReducer,
  dependencies: {}
});

// Track rotation for animation
let rotation = $state(0);

function rotateShapes() {
  rotation += Math.PI / 4;
}

// Render 3D scene
<Scene {store} height="500px">
  <Camera {store} position={[0, 4, 12]} lookAt={[0, 0, 0]} fov={45} />
  <Light {store} type="ambient" intensity={0.4} />
  <Light {store} type="directional" position={[5, 10, 7.5]} intensity={1.2} />

  <Mesh
    {store}
    id="rotating-box"
    geometry={{ type: 'box', size: 1.5 }}
    material={{ color: '#ff6b6b', metallic: 0.7, roughness: 0.3 }}
    position={[0, 1.5, 0]}
    rotation={[0, rotation, 0]}
  />
</Scene>

<button onclick={rotateShapes}>Rotate 45°</button>
```

---

## SCENE COMPONENT

**Purpose**: Root container for 3D rendering. Manages Babylon.js engine lifecycle and syncs store state to the renderer.

**Props**:
- `store: Store<GraphicsState, GraphicsAction>` - Graphics store (required)
- `width: string | number` - Canvas width (default: '100%')
- `height: string | number` - Canvas height (default: '600px')
- `children: Snippet` - Child components (Camera, Light, Mesh)

**Behavior**:
1. Creates canvas element
2. Initializes Babylon.js engine
3. Attempts WebGPU, falls back to WebGL
4. Dispatches `rendererInitialized` action with capabilities
5. Syncs store updates to Babylon.js scene
6. Cleans up engine on unmount

**Usage**:
```typescript
<Scene {store} height="500px">
  <!-- Children render here -->
</Scene>
```

**State Synchronization**:
Scene uses manual subscription (like MapPrimitive) to avoid infinite loops:
- Tracks previous state values
- Only updates Babylon.js when state actually changes
- Uses JSON.stringify for deep comparison

**Renderer Info**:
Access renderer info from store:
```typescript
$store.renderer.activeRenderer // 'webgpu' | 'webgl'
$store.renderer.isInitialized  // boolean
$store.renderer.capabilities   // { maxTextureSize, ... }
$store.renderer.error          // string | null
```

---

## CAMERA COMPONENT

**Purpose**: Defines the viewpoint and projection for the scene.

**Props**:
- `store: Store<GraphicsState, GraphicsAction>` - Graphics store (required)
- `type: 'perspective' | 'orthographic'` - Camera type (default: 'perspective')
- `position: [number, number, number]` - Camera position (required)
- `lookAt: [number, number, number]` - Target point to look at (required)
- `fov: number` - Field of view in degrees (default: 45, perspective only)
- `near: number` - Near clipping plane (optional)
- `far: number` - Far clipping plane (optional)

**Behavior**:
- Dispatches `updateCamera` action on mount
- Re-dispatches when props change
- Does not render visual output (state-only component)

**Usage**:
```typescript
<!-- Perspective camera (default) -->
<Camera
  {store}
  position={[0, 4, 12]}
  lookAt={[0, 0, 0]}
  fov={45}
/>

<!-- Orthographic camera -->
<Camera
  {store}
  type="orthographic"
  position={[0, 10, 0]}
  lookAt={[0, 0, 0]}
/>
```

**Common Camera Positions**:
- Front view: `position={[0, 0, 10]}, lookAt={[0, 0, 0]}`
- Top-down: `position={[0, 10, 0]}, lookAt={[0, 0, 0]}`
- Isometric: `position={[5, 5, 5]}, lookAt={[0, 0, 0]}`
- Close-up: `position={[0, 2, 5]}, lookAt={[0, 1, 0]}`

---

## LIGHT COMPONENT

**Purpose**: Add illumination to the scene. Supports multiple light types.

**Light Types**:

### Ambient Light
Uniform light from all directions (no position/direction).

**Props**:
- `type: 'ambient'`
- `intensity: number` - Light intensity (0-1 typical, can exceed)
- `color: string` - Light color (hex or CSS color, default: '#ffffff')

**Usage**:
```typescript
<Light {store} type="ambient" intensity={0.4} color="#ffffff" />
```

### Directional Light
Parallel rays from a specific direction (like sunlight).

**Props**:
- `type: 'directional'`
- `position: [number, number, number]` - Light position (defines direction)
- `intensity: number` - Light intensity
- `color: string` - Light color (optional)

**Usage**:
```typescript
<Light {store} type="directional" position={[5, 10, 7.5]} intensity={1.2} />
```

### Point Light
Emits light in all directions from a point (like a light bulb).

**Props**:
- `type: 'point'`
- `position: [number, number, number]` - Light position
- `intensity: number` - Light intensity
- `radius: number` - Light radius/range (optional)
- `color: string` - Light color (optional)

**Usage**:
```typescript
<Light {store} type="point" position={[0, 3, 0]} intensity={1.5} radius={10} />
```

### Spot Light
Cone-shaped light (like a flashlight).

**Props**:
- `type: 'spot'`
- `position: [number, number, number]` - Light position
- `direction: [number, number, number]` - Light direction vector
- `angle: number` - Cone angle in radians (default: Math.PI / 4)
- `intensity: number` - Light intensity
- `color: string` - Light color (optional)

**Usage**:
```typescript
<Light
  {store}
  type="spot"
  position={[0, 5, 0]}
  direction={[0, -1, 0]}
  angle={Math.PI / 6}
  intensity={2.0}
/>
```

**Common Lighting Setups**:

```typescript
<!-- Three-point lighting (photography standard) -->
<Light {store} type="ambient" intensity={0.3} />
<Light {store} type="directional" position={[5, 5, 5]} intensity={1.0} />     <!-- Key -->
<Light {store} type="directional" position={[-3, 3, -3]} intensity={0.5} />   <!-- Fill -->
<Light {store} type="directional" position={[0, 2, -5]} intensity={0.3} />    <!-- Back -->

<!-- Outdoor scene (sun + ambient) -->
<Light {store} type="ambient" intensity={0.4} color="#87ceeb" />
<Light {store} type="directional" position={[10, 20, 10]} intensity={1.5} color="#fff8dc" />

<!-- Indoor scene (ambient + point lights) -->
<Light {store} type="ambient" intensity={0.2} />
<Light {store} type="point" position={[0, 3, 0]} intensity={1.0} radius={5} />
<Light {store} type="point" position={[5, 2, 5]} intensity={0.8} radius={4} />
```

---

## MESH COMPONENT

**Purpose**: Render 3D objects with geometry and materials.

**Props**:
- `store: Store<GraphicsState, GraphicsAction>` - Graphics store (required)
- `id: string` - Unique identifier (required)
- `geometry: GeometryConfig` - Geometry configuration (required)
- `material: MaterialConfig` - Material configuration (required)
- `position: [number, number, number]` - Position (required)
- `rotation: [number, number, number]` - Rotation in radians (default: [0, 0, 0])
- `scale: [number, number, number]` - Scale (default: [1, 1, 1])
- `visible: boolean` - Visibility (default: true)

**Lifecycle**:
- `onMount`: Dispatches `addMesh` action
- Props change: Dispatches `updateMesh` action
- `onDestroy`: Dispatches `removeMesh` action

**Usage**:
```typescript
<Mesh
  {store}
  id="my-cube"
  geometry={{ type: 'box', size: 1.5 }}
  material={{ color: '#ff6b6b', metallic: 0.7, roughness: 0.3 }}
  position={[0, 1, 0]}
  rotation={[0, Math.PI / 4, 0]}
  scale={[1, 1, 1]}
/>
```

---

## GEOMETRY TYPES

### Box
Rectangular prism.

**Config**:
```typescript
{ type: 'box'; size: number }
```

**Example**:
```typescript
<Mesh
  {store}
  id="cube"
  geometry={{ type: 'box', size: 1.5 }}
  material={{ color: '#ff6b6b' }}
  position={[0, 1, 0]}
/>
```

### Sphere
Spherical geometry.

**Config**:
```typescript
{
  type: 'sphere';
  radius: number;
  segments?: number; // Default: 32 (higher = smoother)
}
```

**Example**:
```typescript
<Mesh
  {store}
  id="ball"
  geometry={{ type: 'sphere', radius: 0.8, segments: 32 }}
  material={{ color: '#4ecdc4', metallic: 0.8, roughness: 0.2 }}
  position={[0, 1, 0]}
/>
```

**Segments**: Higher values create smoother spheres but increase draw calls.
- Low poly (16 segments): Retro/stylized look
- Medium (32 segments): Default, good balance
- High poly (64 segments): Smooth, more expensive

### Cylinder
Cylindrical geometry.

**Config**:
```typescript
{
  type: 'cylinder';
  height: number;
  diameter: number;
}
```

**Example**:
```typescript
<Mesh
  {store}
  id="pillar"
  geometry={{ type: 'cylinder', height: 2, diameter: 1 }}
  material={{ color: '#95e1d3' }}
  position={[0, 1, 0]}
/>
```

### Torus
Donut-shaped geometry.

**Config**:
```typescript
{
  type: 'torus';
  diameter: number;      // Outer diameter
  thickness: number;     // Tube thickness
  segments?: number;     // Default: 32
}
```

**Example**:
```typescript
<Mesh
  {store}
  id="ring"
  geometry={{ type: 'torus', diameter: 1.5, thickness: 0.3, segments: 32 }}
  material={{ color: '#f38181', metallic: 0.9, roughness: 0.1 }}
  position={[0, 1, 0]}
/>
```

### Plane
Flat rectangular surface.

**Config**:
```typescript
{
  type: 'plane';
  width: number;
  height: number;
}
```

**Example**:
```typescript
<!-- Ground plane (rotated to horizontal) -->
<Mesh
  {store}
  id="ground"
  geometry={{ type: 'plane', width: 12, height: 12 }}
  material={{ color: '#aa96da', metallic: 0.3, roughness: 0.7 }}
  position={[0, 0, 0]}
  rotation={[Math.PI / 2, 0, 0]}
/>
```

**Note**: Planes are initially vertical (facing Z-axis). Rotate by `[Math.PI / 2, 0, 0]` to make horizontal (ground).

---

## MATERIAL PROPERTIES

**MaterialConfig Interface**:
```typescript
interface MaterialConfig {
  color: string;           // Hex or CSS color
  metallic?: number;       // 0-1 (default: 0.5)
  roughness?: number;      // 0-1 (default: 0.5)
  emissive?: string;       // Emissive color (optional)
  alpha?: number;          // 0-1 transparency (optional)
  wireframe?: boolean;     // Wireframe mode (default: false)
}
```

**PBR Workflow**:
Materials use Physically Based Rendering (PBR) with metallic/roughness workflow.

### Metallic (0-1)
Controls how metal-like the surface appears.

- `0.0`: Non-metallic (plastic, rubber, wood, stone)
- `0.5`: Semi-metallic (painted metal, worn surfaces)
- `1.0`: Fully metallic (polished metal, chrome)

**Examples**:
```typescript
// Plastic
{ color: '#ff0000', metallic: 0.0, roughness: 0.5 }

// Painted metal
{ color: '#4ecdc4', metallic: 0.5, roughness: 0.4 }

// Polished chrome
{ color: '#ffffff', metallic: 1.0, roughness: 0.1 }
```

### Roughness (0-1)
Controls surface smoothness/reflectivity.

- `0.0`: Mirror-smooth (glossy, high reflections)
- `0.5`: Semi-rough (satin finish)
- `1.0`: Very rough (matte, diffuse)

**Examples**:
```typescript
// Glass/mirror
{ color: '#ffffff', metallic: 0.0, roughness: 0.0 }

// Satin finish
{ color: '#ff6b6b', metallic: 0.3, roughness: 0.5 }

// Matte rubber
{ color: '#333333', metallic: 0.0, roughness: 1.0 }
```

### Common Material Presets

```typescript
// Polished gold
const gold = { color: '#ffd700', metallic: 1.0, roughness: 0.2 };

// Brushed aluminum
const aluminum = { color: '#c0c0c0', metallic: 1.0, roughness: 0.4 };

// Copper
const copper = { color: '#b87333', metallic: 1.0, roughness: 0.3 };

// Wood
const wood = { color: '#8b4513', metallic: 0.0, roughness: 0.8 };

// Plastic
const plastic = { color: '#ff6b6b', metallic: 0.0, roughness: 0.4 };

// Stone
const stone = { color: '#808080', metallic: 0.0, roughness: 0.9 };

// Rubber
const rubber = { color: '#1a1a1a', metallic: 0.0, roughness: 1.0 };
```

---

## COMPLETE EXAMPLE

Full scene with all geometry types:

```typescript
<script lang="ts">
import { createStore } from '@composable-svelte/core';
import {
  Scene,
  Camera,
  Light,
  Mesh,
  graphicsReducer,
  createInitialGraphicsState
} from '@composable-svelte/graphics';

// Create graphics store
const store = createStore({
  initialState: createInitialGraphicsState({
    backgroundColor: '#1a1a2e'
  }),
  reducer: graphicsReducer,
  dependencies: {}
});

// Track rotation for animation
let rotation = $state(0);

function rotateShapes() {
  rotation += Math.PI / 4;
}
</script>

<!-- Renderer info -->
<div>
  {#if $store.renderer.isInitialized}
    <span>Renderer: {$store.renderer.activeRenderer?.toUpperCase()}</span>
    <span>Max Texture: {$store.renderer.capabilities.maxTextureSize}px</span>
  {:else if $store.renderer.error}
    <span>Error: {$store.renderer.error}</span>
  {:else}
    <span>Initializing...</span>
  {/if}
</div>

<!-- 3D Scene -->
<Scene {store} height="500px">
  <Camera {store} position={[0, 4, 12]} lookAt={[0, 0, 0]} fov={45} />
  <Light {store} type="ambient" intensity={0.4} color="#ffffff" />
  <Light {store} type="directional" position={[5, 10, 7.5]} intensity={1.2} color="#ffffff" />

  <!-- Row 1: Box, Sphere, Cylinder -->
  <Mesh
    {store}
    id="box"
    geometry={{ type: 'box', size: 1.5 }}
    material={{ color: '#ff6b6b', metallic: 0.7, roughness: 0.3 }}
    position={[-4, 1.5, 0]}
    rotation={[0, rotation, 0]}
  />

  <Mesh
    {store}
    id="sphere"
    geometry={{ type: 'sphere', radius: 0.8, segments: 32 }}
    material={{ color: '#4ecdc4', metallic: 0.8, roughness: 0.2 }}
    position={[-1.5, 1.5, 0]}
    rotation={[0, rotation, 0]}
  />

  <Mesh
    {store}
    id="cylinder"
    geometry={{ type: 'cylinder', height: 2, diameter: 1 }}
    material={{ color: '#95e1d3', metallic: 0.6, roughness: 0.4 }}
    position={[1, 1.5, 0]}
    rotation={[0, rotation, 0]}
  />

  <!-- Row 2: Torus, Plane -->
  <Mesh
    {store}
    id="torus"
    geometry={{ type: 'torus', diameter: 1.5, thickness: 0.3, segments: 32 }}
    material={{ color: '#f38181', metallic: 0.9, roughness: 0.1 }}
    position={[3.5, 1.5, 0]}
    rotation={[0, rotation, 0]}
  />

  <!-- Ground plane -->
  <Mesh
    {store}
    id="plane"
    geometry={{ type: 'plane', width: 12, height: 12 }}
    material={{ color: '#aa96da', metallic: 0.3, roughness: 0.7 }}
    position={[0, -0.5, 0]}
    rotation={[Math.PI / 2, 0, 0]}
  />
</Scene>

<button onclick={rotateShapes}>Rotate All Shapes 45°</button>
```

---

## STATE MANAGEMENT

### GraphicsState Interface

```typescript
interface GraphicsState {
  // Renderer
  renderer: {
    activeRenderer: 'webgpu' | 'webgl' | null;
    isInitialized: boolean;
    capabilities: {
      supportsWebGPU: boolean;
      supportsWebGL: boolean;
      maxTextureSize: number;
      maxVertexAttributes: number;
    };
    error: string | null;
  };

  // Scene
  scene: SceneNode;
  backgroundColor: string;

  // Camera
  camera: CameraConfig;

  // Lights
  lights: LightConfig[];

  // Meshes
  meshes: MeshConfig[];

  // Animations (future)
  animations: AnimationState[];

  // Loading
  isLoading: boolean;
  loadingProgress: number; // 0-1
}
```

### GraphicsAction Types

```typescript
type GraphicsAction =
  // Renderer
  | { type: 'rendererInitialized'; renderer: 'webgpu' | 'webgl'; capabilities: RendererCapabilities }
  | { type: 'rendererError'; error: string }

  // Camera
  | { type: 'updateCamera'; camera: Partial<CameraConfig> }
  | { type: 'setCameraPosition'; position: Vector3 }
  | { type: 'setCameraLookAt'; lookAt: Vector3 }

  // Mesh
  | { type: 'addMesh'; mesh: MeshConfig }
  | { type: 'removeMesh'; id: string }
  | { type: 'updateMesh'; id: string; updates: Partial<MeshConfig> }
  | { type: 'setMeshPosition'; id: string; position: Vector3 }
  | { type: 'setMeshRotation'; id: string; rotation: Vector3 }
  | { type: 'setMeshScale'; id: string; scale: Vector3 }
  | { type: 'toggleMeshVisibility'; id: string }

  // Light
  | { type: 'addLight'; light: LightConfig }
  | { type: 'removeLight'; index: number }
  | { type: 'updateLight'; index: number; light: Partial<LightConfig> }

  // Scene
  | { type: 'setBackgroundColor'; color: string }
  | { type: 'clearScene' };
```

### Reducer Pattern

Graphics reducer is pure and testable:

```typescript
import { graphicsReducer } from '@composable-svelte/graphics';
import { TestStore } from '@composable-svelte/core';

const store = new TestStore({
  initialState: createInitialGraphicsState(),
  reducer: graphicsReducer,
  dependencies: {}
});

// Add mesh
await store.send({
  type: 'addMesh',
  mesh: {
    id: 'test-cube',
    geometry: { type: 'box', size: 1 },
    material: { color: '#ff0000' },
    position: [0, 0, 0]
  }
}, (state) => {
  expect(state.meshes.length).toBe(1);
  expect(state.meshes[0].id).toBe('test-cube');
});

// Update position
await store.send({
  type: 'setMeshPosition',
  id: 'test-cube',
  position: [1, 2, 3]
}, (state) => {
  expect(state.meshes[0].position).toEqual([1, 2, 3]);
});
```

---

## PERFORMANCE CONSIDERATIONS

### Geometry Complexity

**Segments**: Higher segment counts create smoother geometry but increase draw calls.

```typescript
// Low poly (fast, retro look)
geometry={{ type: 'sphere', radius: 1, segments: 16 }}

// Default (good balance)
geometry={{ type: 'sphere', radius: 1, segments: 32 }}

// High poly (slow, smooth)
geometry={{ type: 'sphere', radius: 1, segments: 64 }}
```

### Draw Calls

Each mesh = 1 draw call. Minimize meshes for better performance.

**Good**:
```typescript
// 3 meshes = 3 draw calls
<Mesh id="obj1" ... />
<Mesh id="obj2" ... />
<Mesh id="obj3" ... />
```

**Bad**:
```typescript
// 1000 meshes = 1000 draw calls (very slow!)
{#each items as item}
  <Mesh id={item.id} ... />
{/each}
```

**Solution**: Use instancing for many similar objects (future feature).

### Update Frequency

Scene sync uses deep comparison (JSON.stringify). Avoid updating mesh props every frame.

**Good**:
```typescript
// Update rotation only when button clicked
let rotation = $state(0);
function rotate() { rotation += Math.PI / 4; }

<Mesh rotation={[0, rotation, 0]} ... />
```

**Bad**:
```typescript
// Updates every frame (60 FPS) - expensive!
let time = $state(0);
setInterval(() => { time += 0.01; }, 16);

<Mesh rotation={[0, time, 0]} ... />
```

**Solution**: Use animation system (future feature) or throttle updates.

---

## COMMON PATTERNS

### Rotation Animation

```typescript
let rotation = $state(0);

function rotateObject() {
  rotation += Math.PI / 4; // 45 degrees
}

<Mesh rotation={[0, rotation, 0]} ... />
<button onclick={rotateObject}>Rotate 45°</button>
```

### Camera Controls

```typescript
let cameraDistance = $state(12);

function zoomIn() {
  cameraDistance = Math.max(5, cameraDistance - 2);
}

function zoomOut() {
  cameraDistance = Math.min(20, cameraDistance + 2);
}

<Camera position={[0, 4, cameraDistance]} lookAt={[0, 0, 0]} />
<button onclick={zoomIn}>Zoom In</button>
<button onclick={zoomOut}>Zoom Out</button>
```

### Dynamic Lighting

```typescript
let lightIntensity = $state(1.0);

function adjustBrightness(delta: number) {
  lightIntensity = Math.max(0, Math.min(2, lightIntensity + delta));
}

<Light type="directional" position={[5, 10, 7.5]} intensity={lightIntensity} />
<button onclick={() => adjustBrightness(0.2)}>Brighter</button>
<button onclick={() => adjustBrightness(-0.2)}>Dimmer</button>
```

### Toggle Visibility

```typescript
let showObject = $state(true);

// Option 1: Conditional rendering
{#if showObject}
  <Mesh id="object" ... />
{/if}

// Option 2: Visible prop
<Mesh id="object" visible={showObject} ... />

<button onclick={() => showObject = !showObject}>
  {showObject ? 'Hide' : 'Show'}
</button>
```

---

## FUTURE FEATURES

These features are planned but not yet implemented:

### Custom Shaders
```typescript
// Future API
<Mesh
  id="custom"
  geometry={{ type: 'sphere', radius: 1 }}
  material={{
    type: 'custom',
    vertexShader: '...',
    fragmentShader: '...',
    uniforms: { time: 0.0 }
  }}
  position={[0, 0, 0]}
/>
```

### Textures
```typescript
// Future API
<Mesh
  id="textured"
  geometry={{ type: 'box', size: 1 }}
  material={{
    color: '#ffffff',
    albedoTexture: '/textures/wood.jpg',
    normalMap: '/textures/wood_normal.jpg'
  }}
  position={[0, 0, 0]}
/>
```

### Animations
```typescript
// Future API
<Mesh
  id="animated"
  geometry={{ type: 'box', size: 1 }}
  material={{ color: '#ff6b6b' }}
  position={[0, 0, 0]}
  animation={{
    property: 'rotation',
    from: [0, 0, 0],
    to: [0, Math.PI * 2, 0],
    duration: 2000,
    loop: true,
    easing: 'linear'
  }}
/>
```

### Post-Processing
```typescript
// Future API
<Scene {store} postProcessing={{
  bloom: { enabled: true, intensity: 0.5 },
  ssao: { enabled: true, radius: 2 },
  fxaa: true
}}>
  ...
</Scene>
```

---

## CROSS-REFERENCES

**Related Skills**:
- **composable-svelte-core**: Store, reducer, Effect system
- **composable-svelte-components**: UI components that complement 3D scenes
- **composable-svelte-testing**: TestStore for testing graphics reducers

**When to Use Each Package**:
- **graphics**: 3D scenes, WebGPU/WebGL rendering
- **charts**: 2D data visualization (see composable-svelte-charts)
- **maps**: Geospatial data (see composable-svelte-maps)
- **code**: Code editors, syntax highlighting (see composable-svelte-code)

---

## TROUBLESHOOTING

**Scene not rendering**:
- Check browser WebGPU/WebGL support
- Verify store is created with `graphicsReducer`
- Check console for renderer errors in `$store.renderer.error`

**Objects not visible**:
- Ensure Camera is pointing at objects (`lookAt` prop)
- Add at least one Light (scene is dark by default)
- Check mesh `visible` prop
- Verify position values (objects might be off-screen)

**Poor performance**:
- Reduce segment counts on spheres/toruses
- Minimize number of meshes (each mesh = 1 draw call)
- Avoid updating mesh props every frame
- Use simpler geometry (box vs sphere)

**TypeScript errors**:
- Ensure `@composable-svelte/graphics` is installed
- Check geometry config matches type (e.g., `box` requires `size`, not `radius`)
- Verify Vector3 arrays are exactly 3 numbers `[x, y, z]`
