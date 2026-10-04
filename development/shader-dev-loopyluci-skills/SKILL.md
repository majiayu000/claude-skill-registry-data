---
name: shader-dev
description: Use when creating GLSL shaders for real-time visual effects
version: 1.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [shader, glsl, webgl, ray-marching, procedural, graphics]
---

# Shader Craft

A unified skill covering GLSL shader techniques (ShaderToy-compatible) for real-time visual effects.

## Quick Start: Generate a Standalone Shader HTML Page

1. Identify the technique from the routing table
2. Apply WebGL2 adaptation rules
3. Generate standalone HTML with full-screen canvas

## Technique Routing Table

| Effect | Technique |
|--------|-----------|
| 3D scenes from math | ray-marching + sdf-3d |
| Organic/warped shapes | domain-warping + procedural-noise |
| Fluid/smoke effects | fluid-simulation |
| Particles (fire, sparks) | particle-system |
| Ocean/water surface | water-ocean + atmospheric-scattering |
| Terrain/landscape | terrain-rendering + procedural-noise |
| Clouds/fog/volumetric | volumetric-rendering |
| Realistic lighting | lighting-model + shadow-techniques |
| Fractals (Mandelbrot/Julia) | fractal-rendering |
| Post-processing | post-processing + multipass-buffer |

## Code Example: Full-Screen Shader HTML

```html
<!DOCTYPE html>
<html>
<head><style>body { margin:0; overflow:hidden; background:#000; }</style></head>
<body>
<canvas id="c"></canvas>
<script>
const canvas = document.getElementById('c');
const gl = canvas.getContext('webgl2');
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

const vsSource = `#version 300 es
in vec2 a_pos;
void main() { gl_Position = vec4(a_pos, 0.0, 1.0); }`;

const fsSource = `#version 300 es
precision highp float;
out vec4 fragColor;
uniform vec2 iResolution;
uniform float iTime;

void mainImage(out vec4 c, in vec2 f) {
    vec2 uv = (2.0 * f - iResolution.xy) / iResolution.y;
    c = vec4(uv, 0.5 + 0.5 * sin(iTime), 1.0);
}
void main() { mainImage(fragColor, gl_FragCoord.xy); }
`;

// Compile and link shaders, render loop...
</script>
</body>
</html>
```

## WebGL2 Adaptation Rules

- Use `#version 300 es` in shaders
- Fragment shader: `out vec4 fragColor;` instead of `gl_FragColor`
- Use `gl_FragCoord.xy` instead of `fragCoord`
- Functions must be declared before use

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Using gl_FragColor in WebGL2 | Use `out vec4 fragColor;` |
| Missing #version directive | Shaders must start with `#version 300 es` |
| Function order (reference before definition) | Define callee functions first |
| TDZ in JS: let/const before functions | Declare state variables at top of script |
| Performance: too many ray steps | Main loop ≤ 128 steps, FBM ≤ 6 octaves |

## Verification Checklist

- [ ] Shader uses correct #version directive
- [ ] Fragment shader declares output variable
- [ ] WebGL2 API used (not WebGL1)
- [ ] Function order correct (callee before caller)
- [ ] Variables declared before functions in JS
- [ ] Performance within budget (steps, octaves, iterations)
- [ ] Canvas auto-resizes on window resize
- [ ] Shader compiles without errors
