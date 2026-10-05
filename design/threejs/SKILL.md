---
name: threejs
description: Three.js and React Three Fiber (R3F) 3D development — scene setup, lighting, materials, physics, performance, and interactive 3D experiences
layer: domain
category: frontend
triggers:
  - "three.js"
  - "threejs"
  - "3d"
  - "react three fiber"
  - "R3F"
  - "WebGL"
  - "3D scene"
  - "shader"
  - "GLSL"
  - "drei"
  - "3D model"
  - "GLTF"
inputs:
  - "3D scene requirements or visual specs"
  - "Performance optimization for 3D rendering"
  - "Interactive 3D feature requests"
  - "Shader or material questions"
outputs:
  - "React Three Fiber scene implementations"
  - "Custom shaders and materials"
  - "Optimized 3D rendering pipelines"
  - "Interactive 3D component patterns"
linksTo:
  - react
  - animation
  - typescript-frontend
linkedFrom:
  - code-writer
  - ui-designer
preferredNextSkills:
  - animation
  - react
  - typescript-frontend
fallbackSkills: []
riskLevel: low
memoryReadPolicy: selective
memoryWritePolicy: none
sideEffects: []
---

# Three.js & React Three Fiber (R3F)

## Purpose

Provide expert guidance on building 3D experiences for the web using Three.js and React Three Fiber (R3F). Covers scene setup, lighting, materials, model loading, physics, shaders, performance optimization, and integration with React applications.

## Key Patterns

### R3F Scene Setup

**Basic scene with Canvas:**

```tsx
import { Canvas } from '@react-three/fiber';
import { OrbitControls, Environment, ContactShadows } from '@react-three/drei';

function Scene3D() {
  return (
    <div className="w-full h-[600px] rounded-xl overflow-hidden">
      <Canvas
        camera={{ position: [0, 2, 5], fov: 50 }}
        dpr={[1, 2]}  // Responsive pixel ratio
        gl={{ antialias: true, alpha: true }}
        shadows
      >
        {/* Lighting */}
        <ambientLight intensity={0.4} />
        <directionalLight
          position={[5, 5, 5]}
          intensity={1}
          castShadow
          shadow-mapSize={[1024, 1024]}
        />

        {/* Environment map for reflections */}
        <Environment preset="city" />

        {/* Scene content */}
        <mesh castShadow receiveShadow>
          <boxGeometry args={[1, 1, 1]} />
          <meshStandardMaterial color="#3b82f6" roughness={0.3} metalness={0.1} />
        </mesh>

        {/* Ground shadows */}
        <ContactShadows
          position={[0, -0.5, 0]}
          opacity={0.4}
          blur={2}
          far={4}
        />

        {/* Camera controls */}
        <OrbitControls
          enableDamping
          dampingFactor={0.05}
          minDistance={2}
          maxDistance={10}
          maxPolarAngle={Math.PI / 2}
        />
      </Canvas>
    </div>
  );
}
```

### Loading 3D Models

**GLTF model with Drei:**

```tsx
import { useGLTF, useAnimations, Center } from '@react-three/drei';
import { useEffect, useRef } from 'react';
import * as THREE from 'three';

// Preload for instant display
useGLTF.preload('/models/robot.glb');

function RobotModel({ action = 'idle' }: { action?: string }) {
  const group = useRef<THREE.Group>(null);
  const { scene, animations } = useGLTF('/models/robot.glb');
  const { actions } = useAnimations(animations, group);

  useEffect(() => {
    // Fade to new animation
    const current = actions[action];
    current?.reset().fadeIn(0.3).play();
    return () => { current?.fadeOut(0.3); };
  }, [action, actions]);

  return (
    <Center>
      <group ref={group}>
        <primitive object={scene} />
      </group>
    </Center>
  );
}
```

**Generate typed component from GLTF (gltfjsx):**

```bash
# Generate a typed React component from a GLTF file
npx gltfjsx model.glb --types --transform
```

### Custom Materials & Shaders

**Custom shader material:**

```tsx
import { shaderMaterial } from '@react-three/drei';
import { extend, useFrame } from '@react-three/fiber';
import { useRef } from 'react';
import * as THREE from 'three';

// Define custom shader material
const GradientMaterial = shaderMaterial(
  // Uniforms
  {
    uTime: 0,
    uColor1: new THREE.Color('#3b82f6'),
    uColor2: new THREE.Color('#8b5cf6'),
    uNoiseScale: 2.0,
  },
  // Vertex shader
  /* glsl */ `
    varying vec2 vUv;
    varying vec3 vPosition;

    void main() {
      vUv = uv;
      vPosition = position;
      gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
    }
  `,
  // Fragment shader
  /* glsl */ `
    uniform float uTime;
    uniform vec3 uColor1;
    uniform vec3 uColor2;
    uniform float uNoiseScale;

    varying vec2 vUv;

    // Simple noise function
    float noise(vec2 p) {
      return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453);
    }

    void main() {
      float n = noise(vUv * uNoiseScale + uTime * 0.2);
      vec3 color = mix(uColor1, uColor2, vUv.y + n * 0.2);
      gl_FragColor = vec4(color, 1.0);
    }
  `
);

extend({ GradientMaterial });

// TypeScript declaration
declare module '@react-three/fiber' {
  interface ThreeElements {
    gradientMaterial: JSX.IntrinsicElements['meshStandardMaterial'] & {
      uTime?: number;
      uColor1?: THREE.Color;
      uColor2?: THREE.Color;
      uNoiseScale?: number;
    };
  }
}

function GradientSphere() {
  const materialRef = useRef<any>(null);

  useFrame((state) => {
    if (materialRef.current) {
      materialRef.current.uTime = state.clock.elapsedTime;
    }
  });

  return (
    <mesh>
      <sphereGeometry args={[1, 64, 64]} />
      <gradientMaterial ref={materialRef} />
    </mesh>
  );
}
```

### Animation with useFrame

```tsx
import { useFrame } from '@react-three/fiber';
import { useRef } from 'react';
import * as THREE from 'three';

function FloatingCube() {
  const meshRef = useRef<THREE.Mesh>(null);

  useFrame((state, delta) => {
    if (!meshRef.current) return;

    // Smooth floating animation
    meshRef.current.position.y = Math.sin(state.clock.elapsedTime * 0.8) * 0.3;
    meshRef.current.rotation.y += delta * 0.5;

    // Lerp scale on hover (if using pointer events)
    const targetScale = meshRef.current.userData.hovered ? 1.1 : 1;
    meshRef.current.scale.lerp(
      new THREE.Vector3(targetScale, targetScale, targetScale),
      0.1
    );
  });

  return (
    <mesh
      ref={meshRef}
      onPointerEnter={(e) => {
        e.stopPropagation();
        e.object.userData.hovered = true;
        document.body.style.cursor = 'pointer';
      }}
      onPointerLeave={(e) => {
        e.object.userData.hovered = false;
        document.body.style.cursor = 'auto';
      }}
    >
      <boxGeometry args={[1, 1, 1]} />
      <meshStandardMaterial color="#3b82f6" />
    </mesh>
  );
}
```

### Physics with Rapier

```tsx
import { Physics, RigidBody, CuboidCollider } from '@react-three/rapier';

function PhysicsScene() {
  return (
    <Physics gravity={[0, -9.81, 0]} debug={false}>
      {/* Falling boxes */}
      {Array.from({ length: 10 }).map((_, i) => (
        <RigidBody
          key={i}
          position={[Math.random() * 4 - 2, 5 + i * 1.5, Math.random() * 4 - 2]}
          restitution={0.3}
        >
          <mesh castShadow>
            <boxGeometry args={[0.5, 0.5, 0.5]} />
            <meshStandardMaterial color={`hsl(${i * 36}, 70%, 60%)`} />
          </mesh>
        </RigidBody>
      ))}

      {/* Ground plane */}
      <RigidBody type="fixed">
        <CuboidCollider args={[10, 0.1, 10]} position={[0, -0.1, 0]} />
        <mesh receiveShadow position={[0, -0.1, 0]}>
          <boxGeometry args={[20, 0.2, 20]} />
          <meshStandardMaterial color="#e2e8f0" />
        </mesh>
      </RigidBody>
    </Physics>
  );
}
```

### Post-Processing

```tsx
import { EffectComposer, Bloom, ChromaticAberration, Vignette } from '@react-three/postprocessing';
import { BlendFunction } from 'postprocessing';

function PostProcessingScene() {
  return (
    <Canvas>
      {/* Scene content */}
      <SceneContent />

      {/* Post-processing effects */}
      <EffectComposer>
        <Bloom
          intensity={0.5}
          luminanceThreshold={0.8}
          luminanceSmoothing={0.3}
        />
        <ChromaticAberration
          blendFunction={BlendFunction.NORMAL}
          offset={[0.001, 0.001]}
        />
        <Vignette
          eskil={false}
          offset={0.1}
          darkness={0.5}
        />
      </EffectComposer>
    </Canvas>
  );
}
```

### Responsive 3D

```tsx
import { useThree } from '@react-three/fiber';
import { useEffect } from 'react';

function ResponsiveCamera() {
  const { camera, size } = useThree();

  useEffect(() => {
    // Adjust camera for mobile
    if (size.width < 768) {
      camera.position.set(0, 3, 8); // Pull back on mobile
    } else {
      camera.position.set(0, 2, 5);
    }
    camera.updateProjectionMatrix();
  }, [size, camera]);

  return null;
}

// Canvas with responsive DPR
<Canvas
  dpr={[1, Math.min(window.devicePixelRatio, 2)]}
  performance={{ min: 0.5 }} // Allow frame rate to drop gracefully
>
```

### HTML Overlays in 3D

```tsx
import { Html } from '@react-three/drei';

function AnnotatedModel() {
  return (
    <group>
      <mesh>
        <sphereGeometry args={[1, 32, 32]} />
        <meshStandardMaterial color="#3b82f6" />
      </mesh>

      {/* HTML label positioned in 3D space */}
      <Html
        position={[1.5, 0.5, 0]}
        center
        distanceFactor={8}
        className="pointer-events-none"
      >
        <div className="px-4 py-2 rounded-lg bg-white/90 backdrop-blur-sm shadow-md text-sm whitespace-nowrap">
          Click to interact
        </div>
      </Html>
    </group>
  );
}
```

## Performance Optimization

### Geometry & Mesh

1. **Instance meshes** — Use `<instancedMesh>` for many identical objects (trees, particles, buildings):

```tsx
function Particles({ count = 1000 }) {
  const meshRef = useRef<THREE.InstancedMesh>(null);
  const tempObject = new THREE.Object3D();

  useEffect(() => {
    for (let i = 0; i < count; i++) {
      tempObject.position.set(
        (Math.random() - 0.5) * 20,
        (Math.random() - 0.5) * 20,
        (Math.random() - 0.5) * 20
      );
      tempObject.scale.setScalar(Math.random() * 0.1 + 0.05);
      tempObject.updateMatrix();
      meshRef.current!.setMatrixAt(i, tempObject.matrix);
    }
    meshRef.current!.instanceMatrix.needsUpdate = true;
  }, [count]);

  return (
    <instancedMesh ref={meshRef} args={[undefined, undefined, count]}>
      <sphereGeometry args={[1, 8, 8]} />
      <meshStandardMaterial color="#3b82f6" />
    </instancedMesh>
  );
}
```

2. **Merged geometries** — Use `<Merged>` from Drei for static scenes.
3. **LOD (Level of Detail)** — Show lower-poly models at distance:

```tsx
import { Detailed } from '@react-three/drei';

<Detailed distances={[0, 20, 50]}>
  <HighPolyModel />
  <MedPolyModel />
  <LowPolyModel />
</Detailed>
```

### Rendering

4. **DPR capping** — `dpr={[1, 2]}` caps pixel ratio at 2x (Retina is enough).
5. **Adaptive performance** — Use `<PerformanceMonitor>` to auto-adjust quality:

```tsx
import { PerformanceMonitor } from '@react-three/drei';

<Canvas>
  <PerformanceMonitor
    onIncline={() => setQuality('high')}
    onDecline={() => setQuality('low')}
    flipflops={3}
    onFallback={() => setQuality('low')}
  >
    <Scene quality={quality} />
  </PerformanceMonitor>
</Canvas>
```

6. **Frustum culling** — Enabled by default. Ensure large objects have correct bounding boxes.
7. **Texture optimization** — Use KTX2/Basis compressed textures, power-of-two sizes.
8. **Dispose resources** — Clean up geometries, materials, and textures when unmounting.

## Best Practices

1. **R3F over vanilla Three.js** — In React apps, always use R3F for proper lifecycle management.
2. **Drei for common needs** — Check `@react-three/drei` before building from scratch (controls, loaders, helpers).
3. **Suspend loading** — Use `useGLTF` / `useTexture` with React Suspense for loading states.
4. **Delta-based animation** — Use `delta` from `useFrame` for frame-rate independent animation.
5. **No state in useFrame** — Read state via refs, not `useState`. Setting state in `useFrame` causes re-renders at 60fps.
6. **Preload assets** — `useGLTF.preload()` and `useTexture.preload()` at module level.
7. **Compress models** — Use `gltf-transform` or Draco compression. Target < 1MB for hero models.
8. **Test on mobile** — 3D performance varies massively. Always test on real devices.
9. **Fallback for no WebGL** — Detect WebGL support and show a static image fallback.
10. **Accessibility** — Add `aria-label` to the Canvas container, provide alternative content for screen readers.

## Common Pitfalls

| Pitfall | Problem | Fix |
|---------|---------|-----|
| setState in useFrame | Re-render loop at 60fps | Use `useRef` for mutable values in animation loop |
| New objects in useFrame | GC thrashing | Create objects outside the loop, reuse with `.set()` |
| Missing dispose | GPU memory leaks | Dispose geometries, materials, textures on unmount |
| Uncompressed models | Huge download, slow parse | Draco/Meshopt compression, gltf-transform |
| Too many draw calls | Low FPS | Instance meshes, merge static geometry, reduce materials |
| Full-res shadows | Expensive | Limit shadow map size, use contact shadows for simple scenes |
| Missing Suspense | Canvas shows nothing during load | Wrap model components in `<Suspense fallback={<Loader />}>` |
| Canvas re-creating | Entire scene rebuilds | Keep Canvas mounted, change content not the canvas |
