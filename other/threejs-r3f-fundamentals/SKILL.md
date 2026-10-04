---
name: threejs-r3f-fundamentals
description: React Three Fiber scene setup, model loading, lighting, camera control, scroll-linked 3D, and mobile performance. Use when building 3D heroes, product showcases, or interactive WebGL sections.
version: "1.0.0"
verified_date: 2026-06-01
category: frontend
---

# Three.js & React Three Fiber Fundamentals

## Purpose
Production-ready R3F patterns for building 3D web experiences. Every example is a complete, copy-pasteable React component. After reading this skill, you can build a 3D hero section, load models, and link 3D scenes to scroll.

## When to Use This Skill
- 3D hero sections with animated objects.
- Product showcases with rotating models.
- Interactive WebGL backgrounds.
- Scroll-linked 3D camera movements.
- Particle systems and 3D effects.

**CRITICAL**: All R3F components MUST be `"use client"` components in Next.js. The `<Canvas>` component accesses browser APIs.

## Output Format / Delivery
Provide highly optimized, isolated Client Components wrapping `@react-three/fiber` `<Canvas>` nodes. Render clean Suspense skeletons to prevent unmounted layout shifts.

## Behavior Rules
1. **Never perform heavy allocations (instantiate vectors, materials, matrices) inside useFrame() loops** — perform allocations outside the hook and mutate properties inline to avoid garbage collector lag.
2. **Always cap canvas Device Pixel Ratio to 1.5** (`dpr={[1, 1.5]}`) to prevent rendering slowdowns on high-density mobile screens.
3. **Never load uncompressed GLB/GLTF assets (>2MB)** — compress all models with Draco/Prune.
4. **Always provide clean 2D skeletal fallback components** during Suspense loading.

## Maintenance Notes
This skill is locked for standard React Three Fiber v8+ scenes. Update if Drei helpers or fiber core parameters undergo breaking updates.

---

## Phase 1: Canvas Setup (Next.js)

### Basic Canvas
```tsx
// components/Scene.tsx
"use client";
import { Canvas } from "@react-three/fiber";
import { Suspense } from "react";

export function Scene() {
  return (
    <div className="h-screen w-full">
      <Canvas
        camera={{ position: [0, 0, 5], fov: 45 }}
        dpr={[1, 1.5]}          // Cap pixel ratio (battery + performance)
        gl={{ antialias: true, alpha: true }}
      >
        <Suspense fallback={null}>
          {/* 3D content goes here */}
          <ambientLight intensity={0.4} />
          <mesh>
            <boxGeometry args={[1, 1, 1]} />
            <meshStandardMaterial color="#8b5cf6" />
          </mesh>
        </Suspense>
      </Canvas>
    </div>
  );
}
```

### Next.js Page Integration
```tsx
// app/page.tsx (Server Component)
import dynamic from "next/dynamic";

// Dynamic import with SSR disabled — Canvas requires browser APIs
const Scene = dynamic(() => import("@/components/Scene").then(m => m.Scene), {
  ssr: false,
  loading: () => (
    <div className="h-screen w-full bg-zinc-950 animate-pulse" />
  ),
});

export default function Home() {
  return (
    <main>
      <section className="relative h-screen">
        <Scene />
        <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
          <h1 className="text-6xl font-bold text-white">Hero Title</h1>
        </div>
      </section>
    </main>
  );
}
```

**RULE**: Always use `dynamic(() => import(...), { ssr: false })` for Canvas components in Next.js. Server-side rendering of WebGL causes hydration errors.

---

## 2. Lighting Recipes

### Studio Lighting (General Purpose)
```tsx
export function StudioLighting() {
  return (
    <>
      <ambientLight intensity={0.4} />
      <directionalLight position={[5, 5, 5]} intensity={1} castShadow />
      <pointLight position={[-3, 2, -2]} intensity={0.3} color="#a78bfa" />
    </>
  );
}
```

### Dramatic Lighting (Hero/Showcase)
```tsx
export function DramaticLighting() {
  return (
    <>
      <ambientLight intensity={0.1} />
      <spotLight
        position={[5, 8, 5]}
        angle={0.4}
        penumbra={0.5}
        intensity={1.5}
        castShadow
      />
      <pointLight position={[-4, 2, -3]} intensity={0.4} color="#ec4899" />
      <pointLight position={[3, -1, 2]} intensity={0.2} color="#3b82f6" />
    </>
  );
}
```

### HDRI Environment (Realistic Reflections)
```tsx
import { Environment } from "@react-three/drei";

export function HDRILighting() {
  return (
    <>
      <Environment preset="city" background={false} />
      {/* Presets: "apartment", "city", "dawn", "forest", "lobby",
          "night", "park", "studio", "sunset", "warehouse" */}
      <directionalLight position={[5, 5, 5]} intensity={0.5} />
    </>
  );
}
```

---

## 3. Geometry & Materials

### Basic Shapes
```tsx
// Sphere
<mesh position={[0, 0, 0]}>
  <sphereGeometry args={[1, 64, 64]} />
  <meshStandardMaterial color="#8b5cf6" metalness={0.3} roughness={0.4} />
</mesh>

// Torus
<mesh rotation={[Math.PI / 4, 0, 0]}>
  <torusGeometry args={[1, 0.4, 32, 100]} />
  <meshStandardMaterial color="#ec4899" metalness={0.5} roughness={0.2} />
</mesh>

// Plane (for backgrounds/floors)
<mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, -1, 0]} receiveShadow>
  <planeGeometry args={[20, 20]} />
  <meshStandardMaterial color="#1e1e2e" />
</mesh>
```

### Glass/Transparent Material
```tsx
import { MeshTransmissionMaterial } from "@react-three/drei";

<mesh>
  <sphereGeometry args={[1, 64, 64]} />
  <MeshTransmissionMaterial
    backside
    thickness={0.5}
    roughness={0.05}
    transmission={1}
    chromaticAberration={0.06}
    anisotropy={0.1}
    distortion={0.3}
    temporalDistortion={0.1}
    color="#ffffff"
  />
</mesh>
```

---

## 4. Model Loading (GLTF/GLB)

### Load and Display a Model
```tsx
"use client";
import { useRef } from "react";
import { useGLTF } from "@react-three/drei";
import { useFrame } from "@react-three/fiber";
import type * as THREE from "three";

// Preload during module initialization (starts download immediately)
useGLTF.preload("/models/product.glb");

export function ProductModel() {
  const { scene } = useGLTF("/models/product.glb");
  const groupRef = useRef<THREE.Group>(null);

  useFrame((_, delta) => {
    if (groupRef.current) {
      groupRef.current.rotation.y += delta * 0.3; // Slow continuous rotation
    }
  });

  return (
    <group ref={groupRef} scale={1.5} position={[0, -0.5, 0]}>
      <primitive object={scene.clone()} />
    </group>
  );
}
```

### Model with Draco Compression
```tsx
import { useGLTF } from "@react-three/drei";

export function CompressedModel() {
  const { scene } = useGLTF("/models/hero.glb", "/draco/");
  // Second arg = Draco decoder path. Use CDN or local:
  // "/draco/" → local (copy from node_modules/three/examples/jsm/libs/draco/)
  // "https://www.gstatic.com/draco/versioned/decoders/1.5.6/" → Google CDN

  return <primitive object={scene} />;
}
```

**RULE**: Always use Draco-compressed GLB files. Uncompressed models > 5MB are a performance failure. Compress with: `npx gltf-pipeline -i model.gltf -o model.glb -d`

---

## 5. Animation

### useFrame — Per-Frame Updates
```tsx
import { useRef } from "react";
import { useFrame } from "@react-three/fiber";
import type * as THREE from "three";

export function FloatingObject() {
  const meshRef = useRef<THREE.Mesh>(null);

  useFrame((state) => {
    if (!meshRef.current) return;

    // Sine-wave bob (floating effect)
    meshRef.current.position.y = Math.sin(state.clock.elapsedTime * 0.8) * 0.15;

    // Gentle rotation
    meshRef.current.rotation.y = state.clock.elapsedTime * 0.2;

    // RULE: Never create objects inside useFrame (GC thrashing)
    // ❌ const vec = new THREE.Vector3()
    // ✅ Create refs outside, reuse inside
  });

  return (
    <mesh ref={meshRef}>
      <torusKnotGeometry args={[1, 0.3, 128, 32]} />
      <meshStandardMaterial color="#8b5cf6" metalness={0.4} roughness={0.3} />
    </mesh>
  );
}
```

### Scroll-Linked Camera (Drei ScrollControls)
```tsx
"use client";
import { Canvas } from "@react-three/fiber";
import { ScrollControls, useScroll } from "@react-three/drei";
import { useFrame } from "@react-three/fiber";
import { useRef } from "react";
import * as THREE from "three";

function CameraRig() {
  const scroll = useScroll();

  useFrame((state) => {
    const offset = scroll.offset; // 0 at top, 1 at bottom

    // Orbit camera around scene based on scroll
    const angle = offset * Math.PI * 2;
    state.camera.position.x = Math.sin(angle) * 5;
    state.camera.position.z = Math.cos(angle) * 5;
    state.camera.position.y = 2 - offset * 3;
    state.camera.lookAt(0, 0, 0);
  });

  return null;
}

export function ScrollScene() {
  return (
    <div className="h-[400vh]"> {/* Height determines scroll length */}
      <div className="sticky top-0 h-screen">
        <Canvas camera={{ position: [0, 2, 5], fov: 45 }} dpr={[1, 1.5]}>
          <ScrollControls pages={4} damping={0.25}>
            <CameraRig />
            {/* Scene objects */}
            <ambientLight intensity={0.4} />
            <directionalLight position={[5, 5, 5]} />
            <mesh>
              <torusKnotGeometry args={[1, 0.3, 128, 32]} />
              <meshStandardMaterial color="#8b5cf6" />
            </mesh>
          </ScrollControls>
        </Canvas>
      </div>
    </div>
  );
}
```

### Object Animation Triggered by Scroll
```tsx
import { useScroll } from "@react-three/drei";
import { useFrame } from "@react-three/fiber";
import { useRef } from "react";
import * as THREE from "three";

export function ScrollAnimatedObject() {
  const meshRef = useRef<THREE.Mesh>(null);
  const scroll = useScroll();

  useFrame(() => {
    if (!meshRef.current) return;
    const progress = scroll.offset;

    // Scale up as user scrolls
    const scale = THREE.MathUtils.lerp(0.5, 1.5, progress);
    meshRef.current.scale.setScalar(scale);

    // Rotate based on scroll
    meshRef.current.rotation.y = progress * Math.PI * 2;

    // Move vertically
    meshRef.current.position.y = THREE.MathUtils.lerp(2, -2, progress);
  });

  return (
    <mesh ref={meshRef}>
      <dodecahedronGeometry args={[1, 0]} />
      <meshStandardMaterial color="#ec4899" metalness={0.5} roughness={0.2} />
    </mesh>
  );
}
```

---

## 6. Post-Processing

```tsx
import { EffectComposer, Bloom, Vignette, ChromaticAberration } from "@react-three/postprocessing";
import { BlendFunction } from "postprocessing";

export function PostProcessing() {
  return (
    <EffectComposer>
      <Bloom
        intensity={0.5}
        luminanceThreshold={0.8}
        luminanceSmoothing={0.9}
      />
      <Vignette
        offset={0.3}
        darkness={0.6}
        blendFunction={BlendFunction.NORMAL}
      />
      <ChromaticAberration
        offset={[0.0005, 0.0005]}
        blendFunction={BlendFunction.NORMAL}
      />
    </EffectComposer>
  );
}

// Add inside Canvas, after scene objects:
// <Canvas>
//   <Scene />
//   <PostProcessing />
// </Canvas>
```

**RULE**: Post-processing is expensive on mobile. Disable or reduce on mobile devices (see Performance section).

---

## 7. Particles

### Simple Particle Field
```tsx
"use client";
import { useMemo, useRef } from "react";
import { useFrame } from "@react-three/fiber";
import * as THREE from "three";

export function ParticleField({ count = 2000 }: { count?: number }) {
  const pointsRef = useRef<THREE.Points>(null);

  const positions = useMemo(() => {
    const pos = new Float32Array(count * 3);
    for (let i = 0; i < count; i++) {
      pos[i * 3] = (Math.random() - 0.5) * 20;     // x
      pos[i * 3 + 1] = (Math.random() - 0.5) * 20; // y
      pos[i * 3 + 2] = (Math.random() - 0.5) * 20; // z
    }
    return pos;
  }, [count]);

  useFrame((state) => {
    if (!pointsRef.current) return;
    pointsRef.current.rotation.y = state.clock.elapsedTime * 0.03;
    pointsRef.current.rotation.x = state.clock.elapsedTime * 0.01;
  });

  return (
    <points ref={pointsRef}>
      <bufferGeometry>
        <bufferAttribute
          attach="attributes-position"
          count={count}
          array={positions}
          itemSize={3}
        />
      </bufferGeometry>
      <pointsMaterial
        size={0.03}
        color="#a78bfa"
        transparent
        opacity={0.6}
        sizeAttenuation
        depthWrite={false}
      />
    </points>
  );
}
```

---

## 8. Text in 3D

```tsx
import { Text, Text3D, Center } from "@react-three/drei";

// 2D Text Billboard (always faces camera)
<Text
  position={[0, 2, 0]}
  fontSize={0.8}
  color="#f8fafc"
  font="/fonts/Geist-Bold.woff"
  maxWidth={8}
  textAlign="center"
>
  Hero Headline
</Text>

// 3D Extruded Text
<Center>
  <Text3D
    font="/fonts/Geist_Bold.json"
    size={1.5}
    height={0.3}
    bevelEnabled
    bevelSize={0.02}
    bevelThickness={0.01}
  >
    HERO
    <meshStandardMaterial color="#8b5cf6" metalness={0.5} roughness={0.3} />
  </Text3D>
</Center>
```

---

## 9. Performance

### Performance Budgets

| Metric | Mobile | Desktop |
|--------|--------|---------|
| Triangle count | < 100K | < 500K |
| Draw calls | < 50 | < 200 |
| Texture memory | < 32MB | < 128MB |
| Model file size (GLB) | < 2MB | < 5MB |
| Canvas DPR | 1.0 | 1.5 |
| Target FPS | 30fps | 60fps |
| Particle count | < 1000 | < 5000 |

### Mobile Detection & Fallback
```tsx
"use client";
import { useState, useEffect } from "react";

function useIsMobile() {
  const [isMobile, setIsMobile] = useState(false);

  useEffect(() => {
    const mq = window.matchMedia("(max-width: 767px)");
    setIsMobile(mq.matches);
    const handler = (e: MediaQueryListEvent) => setIsMobile(e.matches);
    mq.addEventListener("change", handler);
    return () => mq.removeEventListener("change", handler);
  }, []);

  return isMobile;
}

export function AdaptiveHero() {
  const isMobile = useIsMobile();

  if (isMobile) {
    return (
      <section className="h-screen relative bg-zinc-950">
        <img src="/hero-fallback.webp" alt="" className="w-full h-full object-cover" />
        <div className="absolute inset-0 flex items-center justify-center">
          <h1 className="text-4xl font-bold text-white">Hero Title</h1>
        </div>
      </section>
    );
  }

  return <DesktopCanvas />;
}
```

### Performance Optimizations
```tsx
<Canvas
  dpr={[1, 1.5]}              // Cap DPR — 2x is rarely worth the GPU cost
  frameloop="demand"           // Only render when something changes (static scenes)
  performance={{ min: 0.5 }}   // Auto-reduce quality under load
  gl={{
    powerPreference: "high-performance",
    antialias: true,
    alpha: true,
  }}
>
  <Suspense fallback={null}>
    <Bvh>                        {/* Bounding volume hierarchy — fast frustum culling */}
      <SceneContent />
    </Bvh>
  </Suspense>
</Canvas>
```

---

## 10. Click & Hover Interaction (Raycasting)

R3F has built-in pointer event handlers on meshes — no manual raycasting needed.

```tsx
"use client";
import { useState, useRef } from "react";
import { useFrame } from "@react-three/fiber";
import type * as THREE from "three";

export function InteractiveSphere() {
  const meshRef = useRef<THREE.Mesh>(null);
  const [hovered, setHovered] = useState(false);
  const [clicked, setClicked] = useState(false);

  useFrame(() => {
    if (!meshRef.current) return;
    // Smooth scale transition
    const target = clicked ? 1.3 : hovered ? 1.1 : 1;
    meshRef.current.scale.lerp({ x: target, y: target, z: target } as THREE.Vector3, 0.1);
  });

  return (
    <mesh
      ref={meshRef}
      onClick={() => setClicked(!clicked)}
      onPointerOver={(e) => {
        e.stopPropagation();  // Prevent event from hitting objects behind
        setHovered(true);
        document.body.style.cursor = "pointer";
      }}
      onPointerOut={() => {
        setHovered(false);
        document.body.style.cursor = "auto";
      }}
    >
      <sphereGeometry args={[1, 64, 64]} />
      <meshStandardMaterial
        color={clicked ? "#ec4899" : hovered ? "#a78bfa" : "#8b5cf6"}
        metalness={0.3}
        roughness={0.4}
      />
    </mesh>
  );
}
```

### Available Pointer Events
```
onClick           — Click/tap
onDoubleClick     — Double click
onPointerOver     — Mouse enters mesh (hover start)
onPointerOut      — Mouse leaves mesh (hover end)
onPointerDown     — Mouse button pressed
onPointerUp       — Mouse button released
onPointerMove     — Mouse moves over mesh
onPointerMissed   — Click that missed all meshes (useful for deselect)
```

**RULE**: Always call `e.stopPropagation()` in `onPointerOver` to prevent events from hitting objects behind the one you're interacting with.

---

## 11. Shadow Setup

```tsx
export function ShadowScene() {
  return (
    <Canvas shadows dpr={[1, 1.5]}>
      {/* 1. Enable shadows on the Canvas with the `shadows` prop */}

      {/* 2. Light must have castShadow + shadow camera configured */}
      <directionalLight
        castShadow
        position={[5, 8, 5]}
        intensity={1.5}
        shadow-mapSize-width={1024}
        shadow-mapSize-height={1024}
        shadow-camera-left={-10}
        shadow-camera-right={10}
        shadow-camera-top={10}
        shadow-camera-bottom={-10}
        shadow-camera-near={0.1}
        shadow-camera-far={50}
        shadow-bias={-0.0001}    // Prevent shadow acne (dark spots on surfaces)
      />

      {/* 3. Objects that CAST shadows */}
      <mesh castShadow position={[0, 1, 0]}>
        <sphereGeometry args={[1, 64, 64]} />
        <meshStandardMaterial color="#8b5cf6" />
      </mesh>

      {/* 4. Objects that RECEIVE shadows */}
      <mesh receiveShadow rotation={[-Math.PI / 2, 0, 0]} position={[0, -1, 0]}>
        <planeGeometry args={[20, 20]} />
        <meshStandardMaterial color="#1e1e2e" />
      </mesh>
    </Canvas>
  );
}
```

### Shadow Checklist
- `<Canvas shadows>` — enables the shadow rendering system
- Light: `castShadow` + `shadow-mapSize` (1024 for quality, 512 for performance)
- Casting objects: `castShadow` prop
- Receiving objects: `receiveShadow` prop
- `shadow-bias={-0.0001}` — prevents shadow acne artifacts

**RULE**: Shadows are expensive on mobile. Disable shadows entirely on mobile fallback or reduce `shadow-mapSize` to 512.

---

## 12. Anti-Patterns

| ❌ Don't | ✅ Do | Why |
|---------|-------|-----|
| Create objects inside `useFrame` | Create refs outside, mutate inside `useFrame` | GC thrashing kills frame rate |
| Use `OrbitControls` on scroll pages | Use `ScrollControls` or custom camera rig | OrbitControls conflicts with page scroll |
| Skip `Suspense` boundary around Canvas content | Always wrap in `<Suspense>` with fallback | Missing Suspense causes white flash during load |
| Load uncompressed GLTF (> 5MB) | Draco-compress: `gltf-pipeline -d` | Uncompressed models are a bandwidth failure |
| Render Canvas with SSR | `dynamic(() => ..., { ssr: false })` | Canvas requires browser APIs |
| Use DPR > 1.5 | Cap at `dpr={[1, 1.5]}` | 2x DPR quadruples pixel count for minimal visual gain |
| Animate all objects every frame | Use `frameloop="demand"` for static scenes | Continuous rendering drains battery |
| Skip mobile fallback | Detect mobile → render 2D image | 3D on low-end mobile = 10fps or crash |
| Forget `e.stopPropagation()` on hover | Always stop propagation in `onPointerOver` | Events leak to objects behind, causing flicker |

---

## 13. Verification Checklist

- [ ] Canvas is in a `"use client"` component
- [ ] Canvas is loaded with `dynamic(..., { ssr: false })` in Next.js
- [ ] `<Suspense>` boundary wraps all Canvas content with deterministic-height fallback
- [ ] DPR capped at `[1, 1.5]`
- [ ] Model files are Draco-compressed and under 5MB
- [ ] `useGLTF.preload()` called for critical models
- [ ] Mobile fallback renders a static image instead of 3D
- [ ] No object creation inside `useFrame`
- [ ] `prefers-reduced-motion` check disables or pauses 3D animations
- [ ] Post-processing disabled on mobile
- [ ] Triangle count verified within budget (100K mobile / 500K desktop)
- [ ] Interactive meshes have pointer events with `stopPropagation()`
- [ ] Shadows use `shadow-bias` to prevent acne
- [ ] Shadows disabled or reduced on mobile

