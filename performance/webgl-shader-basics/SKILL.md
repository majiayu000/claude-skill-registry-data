---
name: webgl-shader-basics
description: Custom GLSL shaders for WebGL backgrounds, gradient meshes, noise textures, and particle effects. Use when building custom visual effects that go beyond standard Three.js materials.
version: "1.0.0"
verified_date: 2026-06-01
category: frontend
---

# WebGL Shader Basics

## Purpose
Teach custom GLSL fragment and vertex shaders for visual effects that standard materials can't achieve: animated gradient backgrounds, noise-driven surfaces, flowing particles, and procedural textures.

## When to Use This Skill
- Animated WebGL backgrounds (gradient mesh, noise, flow fields).
- Custom material effects (holographic, iridescent, distortion).
- Procedural textures (organic patterns without image assets).
- GPU-accelerated particle systems.

**Prerequisite**: This skill assumes an R3F `<Canvas>` is already set up (see `threejs-r3f-fundamentals`).

## Output Format / Delivery
Provide raw, optimized GLSL vertex and fragment shader scripts. Deliver complete shaderMaterial wrappers for integration into React Three Fiber scenes.

## Behavior Rules
1. **Never use highp precision for fragment shaders on mobile devices** — always default to `precision mediump float` to conserve memory bandwidth and battery performance.
2. **Never execute expensive conditional loops or dynamic branches inside main() loops** — calculate smoothsteps or mix calculations to avoid instruction pipeline stalling on GPUs.
3. **Always sanitize and normalize coordinate spaces** (UVs, screen spaces) before applying noise maps or distortion matrices.
4. **Always pass uTime, uResolution, and uMouse as uniform inputs** to allow smooth state interpolation.

## Maintenance Notes
This skill is locked for standard GLSL ES 100 features. Update if WebGL 2 or WebGPU ES 300 standards are systematically mandated.

---

## Phase 1: Shader Structure

### Fragment Shader (Controls Pixel Color)
```glsl
// fragment.glsl
precision mediump float;  // Use mediump on mobile (highp is expensive)

uniform float uTime;        // Elapsed time (seconds)
uniform vec2 uResolution;   // Canvas width/height in pixels
uniform vec2 uMouse;        // Mouse position (normalized 0-1)

void main() {
  // gl_FragCoord.xy = pixel coordinates
  // Normalize to 0-1 range:
  vec2 uv = gl_FragCoord.xy / uResolution;

  // Output color: RGBA
  gl_FragColor = vec4(uv.x, uv.y, 0.5, 1.0);
}
```

### Vertex Shader (Controls Vertex Position)
```glsl
// vertex.glsl
precision mediump float;

uniform float uTime;

void main() {
  vec3 pos = position;  // Built-in: vertex position from geometry

  // Example: wave displacement
  pos.z += sin(pos.x * 3.0 + uTime) * 0.1;

  gl_Position = projectionMatrix * modelViewMatrix * vec4(pos, 1.0);
}
```

### R3F Integration
```tsx
"use client";
import { useRef, useMemo } from "react";
import { useFrame, useThree } from "@react-three/fiber";
import * as THREE from "three";

const vertexShader = `
  precision mediump float;
  varying vec2 vUv;

  void main() {
    vUv = uv;
    gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
  }
`;

const fragmentShader = `
  precision mediump float;
  uniform float uTime;
  uniform vec2 uResolution;
  varying vec2 vUv;

  void main() {
    vec3 color = vec3(vUv.x, vUv.y, sin(uTime) * 0.5 + 0.5);
    gl_FragColor = vec4(color, 1.0);
  }
`;

export function ShaderPlane() {
  const meshRef = useRef<THREE.Mesh>(null);
  const { viewport } = useThree();

  const uniforms = useMemo(() => ({
    uTime: { value: 0 },
    uResolution: { value: new THREE.Vector2(viewport.width, viewport.height) },
  }), []);

  useFrame((state) => {
    uniforms.uTime.value = state.clock.elapsedTime;
  });

  return (
    <mesh ref={meshRef} scale={[viewport.width, viewport.height, 1]}>
      <planeGeometry args={[1, 1, 1, 1]} />
      <shaderMaterial
        vertexShader={vertexShader}
        fragmentShader={fragmentShader}
        uniforms={uniforms}
      />
    </mesh>
  );
}
```

**RULE**: Create `uniforms` object with `useMemo` — NOT inside the render body. Recreating uniforms every frame causes GPU stalls.

---

## 2. Noise Functions

Noise is the foundation of organic-looking shaders. Copy these functions directly into your fragment shader.

### Simplex Noise 2D (Complete Implementation)
```glsl
// Paste this ABOVE your main() function
vec3 mod289(vec3 x) { return x - floor(x * (1.0 / 289.0)) * 289.0; }
vec2 mod289(vec2 x) { return x - floor(x * (1.0 / 289.0)) * 289.0; }
vec3 permute(vec3 x) { return mod289(((x * 34.0) + 1.0) * x); }

float snoise(vec2 v) {
  const vec4 C = vec4(0.211324865405187, 0.366025403784439,
                      -0.577350269189626, 0.024390243902439);
  vec2 i  = floor(v + dot(v, C.yy));
  vec2 x0 = v - i + dot(i, C.xx);
  vec2 i1;
  i1 = (x0.x > x0.y) ? vec2(1.0, 0.0) : vec2(0.0, 1.0);
  vec4 x12 = x0.xyxy + C.xxzz;
  x12.xy -= i1;
  i = mod289(i);
  vec3 p = permute(permute(i.y + vec3(0.0, i1.y, 1.0))
                           + i.x + vec3(0.0, i1.x, 1.0));
  vec3 m = max(0.5 - vec3(dot(x0, x0), dot(x12.xy, x12.xy),
                           dot(x12.zw, x12.zw)), 0.0);
  m = m * m;
  m = m * m;
  vec3 x = 2.0 * fract(p * C.www) - 1.0;
  vec3 h = abs(x) - 0.5;
  vec3 ox = floor(x + 0.5);
  vec3 a0 = x - ox;
  m *= 1.79284291400159 - 0.85373472095314 * (a0 * a0 + h * h);
  vec3 g;
  g.x = a0.x * x0.x + h.x * x0.y;
  g.yz = a0.yz * x12.xz + h.yz * x12.yw;
  return 130.0 * dot(m, g);
}
```

### Fractional Brownian Motion (Layered Noise)
```glsl
float fbm(vec2 p) {
  float value = 0.0;
  float amplitude = 0.5;
  float frequency = 1.0;

  for (int i = 0; i < 5; i++) {
    value += amplitude * snoise(p * frequency);
    amplitude *= 0.5;
    frequency *= 2.0;
  }
  return value;
}
```

---

## 3. Ready-Made Shader Patterns

### Pattern 1: Animated Gradient Mesh Background
```glsl
// fragment.glsl
precision mediump float;

uniform float uTime;
varying vec2 vUv;

// Include snoise function from Section 2

void main() {
  // Animated noise-driven gradient
  float n = snoise(vUv * 3.0 + uTime * 0.2);

  // Blend between 3-4 colors based on noise + position
  vec3 color1 = vec3(0.05, 0.02, 0.15);   // Deep purple-black
  vec3 color2 = vec3(0.15, 0.05, 0.30);   // Dark violet
  vec3 color3 = vec3(0.55, 0.35, 0.85);   // Medium purple
  vec3 color4 = vec3(0.93, 0.45, 0.60);   // Pink accent

  float blend = vUv.y + n * 0.3;
  vec3 color = mix(color1, color2, smoothstep(0.0, 0.3, blend));
  color = mix(color, color3, smoothstep(0.3, 0.6, blend));
  color = mix(color, color4, smoothstep(0.7, 1.0, blend));

  gl_FragColor = vec4(color, 1.0);
}
```

### Pattern 2: Flowing Noise Surface
```glsl
// fragment.glsl
precision mediump float;

uniform float uTime;
varying vec2 vUv;

// Include snoise and fbm functions from Section 2

void main() {
  // Domain warping: feed noise into noise for organic flow
  vec2 q = vec2(
    fbm(vUv + vec2(0.0, 0.0) + uTime * 0.1),
    fbm(vUv + vec2(5.2, 1.3) + uTime * 0.15)
  );

  float f = fbm(vUv + 4.0 * q);

  // Color mapping
  vec3 baseColor = vec3(0.05, 0.02, 0.1);
  vec3 highlight = vec3(0.5, 0.2, 0.8);
  vec3 accent = vec3(0.9, 0.4, 0.5);

  vec3 color = mix(baseColor, highlight, clamp(f * 2.0, 0.0, 1.0));
  color = mix(color, accent, clamp(length(q) * 0.5, 0.0, 1.0));

  gl_FragColor = vec4(color, 1.0);
}
```

### Pattern 3: Vertex Displacement (Wavy Surface)
```glsl
// vertex.glsl
precision mediump float;

uniform float uTime;
varying vec2 vUv;
varying float vElevation;

// Include snoise from Section 2

void main() {
  vUv = uv;
  vec3 pos = position;

  // Displace vertices based on noise
  float elevation = snoise(pos.xy * 2.0 + uTime * 0.3) * 0.15;
  pos.z += elevation;
  vElevation = elevation;

  gl_Position = projectionMatrix * modelViewMatrix * vec4(pos, 1.0);
}
```

```glsl
// fragment.glsl — paired with displacement vertex shader
precision mediump float;

varying vec2 vUv;
varying float vElevation;

void main() {
  // Color based on elevation
  vec3 low = vec3(0.05, 0.02, 0.15);
  vec3 high = vec3(0.6, 0.3, 0.9);
  vec3 color = mix(low, high, vElevation * 3.0 + 0.5);

  gl_FragColor = vec4(color, 1.0);
}
```

Use with a high-resolution plane:
```tsx
<mesh rotation={[-Math.PI / 4, 0, 0]}>
  <planeGeometry args={[5, 5, 128, 128]} />  {/* 128 segments for smooth waves */}
  <shaderMaterial
    vertexShader={vertexShader}
    fragmentShader={fragmentShader}
    uniforms={uniforms}
    side={THREE.DoubleSide}
  />
</mesh>
```

---

## 4. Fullscreen Background Shader

Complete pattern for a WebGL background that fills the entire viewport behind page content.

```tsx
"use client";
import { useRef, useMemo } from "react";
import { Canvas, useFrame, useThree } from "@react-three/fiber";
import * as THREE from "three";

const vertexShader = `
  varying vec2 vUv;
  void main() {
    vUv = uv;
    gl_Position = vec4(position.xy, 0.0, 1.0);
  }
`;

const fragmentShader = `
  precision mediump float;
  uniform float uTime;
  varying vec2 vUv;

  // ... paste snoise + fbm from Section 2 ...

  void main() {
    vec2 uv = vUv;
    float n = fbm(uv * 3.0 + uTime * 0.15);
    vec3 color = mix(vec3(0.02, 0.01, 0.08), vec3(0.15, 0.05, 0.35), n * 0.5 + 0.5);
    gl_FragColor = vec4(color, 1.0);
  }
`;

function Background() {
  const meshRef = useRef<THREE.Mesh>(null);

  const uniforms = useMemo(() => ({
    uTime: { value: 0 },
  }), []);

  useFrame((state) => {
    uniforms.uTime.value = state.clock.elapsedTime;
  });

  return (
    <mesh ref={meshRef}>
      <planeGeometry args={[2, 2]} />
      <shaderMaterial
        vertexShader={vertexShader}
        fragmentShader={fragmentShader}
        uniforms={uniforms}
        depthWrite={false}
        depthTest={false}
      />
    </mesh>
  );
}

export function WebGLBackground() {
  return (
    <div className="fixed inset-0 -z-10">
      <Canvas
        dpr={[1, 1.5]}
        gl={{ antialias: false, alpha: false }}  // No antialias needed for fullscreen
        camera={{ position: [0, 0, 1] }}
      >
        <Background />
      </Canvas>
    </div>
  );
}

// Usage in layout:
// <body>
//   <WebGLBackground />
//   <main className="relative z-10">{children}</main>
// </body>
```

---

## 5. Mouse-Reactive Shaders

### Passing Mouse Position to Shader
```tsx
import { useFrame, useThree } from "@react-three/fiber";

function InteractiveBackground() {
  const uniforms = useMemo(() => ({
    uTime: { value: 0 },
    uMouse: { value: new THREE.Vector2(0.5, 0.5) },
  }), []);

  useFrame((state) => {
    uniforms.uTime.value = state.clock.elapsedTime;

    // Normalize mouse to 0-1 range
    const { x, y } = state.pointer; // -1 to 1 range from R3F
    uniforms.uMouse.value.set(x * 0.5 + 0.5, y * 0.5 + 0.5);
  });

  return (
    <mesh>
      <planeGeometry args={[2, 2]} />
      <shaderMaterial
        vertexShader={vertexShader}
        fragmentShader={fragmentShader}
        uniforms={uniforms}
      />
    </mesh>
  );
}
```

### Fragment Shader with Mouse Interaction
```glsl
uniform vec2 uMouse;
uniform float uTime;
varying vec2 vUv;

void main() {
  // Distance from mouse creates a radial effect
  float dist = distance(vUv, uMouse);
  float glow = 0.05 / dist;  // Inverse distance = radial glow

  vec3 baseColor = vec3(0.02, 0.01, 0.08);
  vec3 glowColor = vec3(0.5, 0.2, 0.9);

  vec3 color = baseColor + glowColor * glow * 0.3;

  gl_FragColor = vec4(color, 1.0);
}
```

---

## 6. GLSL Quick Reference

### Types
```glsl
float a = 1.0;           // Scalar
vec2 b = vec2(1.0, 2.0); // 2D vector
vec3 c = vec3(1.0);      // 3D vector (all components = 1.0)
vec4 d = vec4(c, 1.0);   // 4D vector (RGB + alpha)
mat4 m;                   // 4x4 matrix
```

### Useful Functions
```glsl
mix(a, b, t)          // Linear interpolation: a*(1-t) + b*t
smoothstep(e0, e1, x) // Smooth Hermite interpolation between e0 and e1
clamp(x, min, max)    // Constrain x to [min, max]
step(edge, x)         // 0.0 if x < edge, 1.0 if x >= edge
fract(x)              // Fractional part: x - floor(x)
length(v)             // Vector magnitude
distance(a, b)        // Distance between two points
normalize(v)          // Unit vector
dot(a, b)             // Dot product
cross(a, b)           // Cross product (vec3 only)
abs(x)                // Absolute value
sin(x), cos(x)        // Trigonometry
pow(x, y)             // x raised to power y
mod(x, y)             // Modulo
```

### Swizzling
```glsl
vec4 color = vec4(1.0, 0.5, 0.3, 1.0);
color.rgb    // vec3(1.0, 0.5, 0.3)
color.rg     // vec2(1.0, 0.5)
color.r      // float 1.0
color.xy     // same as .rg — position notation
color.yzx    // vec3(0.5, 0.3, 1.0) — reorder
```

---

## 7. Performance Rules

| Rule | Why |
|------|-----|
| Use `precision mediump float` | `highp` is 2x slower on mobile GPUs |
| Minimize `if` statements in shaders | GPU branches are expensive (both paths execute) |
| Use `step()` / `smoothstep()` instead of `if` | Branchless alternatives |
| Keep noise octaves ≤ 5 | Each FBM octave doubles computation |
| Use `depthWrite: false` for fullscreen quads | Prevents unnecessary depth buffer writes |
| Avoid `discard` in fragment shader | Breaks early-z optimization on mobile |
| Cap geometry segments (128x128 max for planes) | More vertices = more vertex shader invocations |

---

## 8. Verification Checklist

- [ ] Uniforms created with `useMemo` (not recreated every frame)
- [ ] `precision mediump float` used (not `highp`)
- [ ] Noise function octaves ≤ 5
- [ ] No `if` statements in hot shader paths (use `step`/`smoothstep`)
- [ ] Fullscreen quads use `depthWrite: false`
- [ ] Mobile tested — shader compiles and runs > 30fps
- [ ] `prefers-reduced-motion` handled (stop time uniform, show static frame)
- [ ] No division by zero risk (guard `distance()` calls)
