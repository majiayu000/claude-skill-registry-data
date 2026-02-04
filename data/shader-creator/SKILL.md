---
name: shader-creator
description: Creating GLSL shaders with interactive parameter exploration. Use this when users request creating shaders, fragment shaders, visual effects, procedural textures, or shader art. Create original shader code that runs in real-time with adjustable parameters.
license: MIT
---

Shaders are GPU-accelerated visual programs that create real-time graphics through mathematical expressions. Output .md files (shader concept), and .html files (interactive shader viewer with live parameter controls).

This happens in two steps:
1. Shader Concept Creation (.md file)
2. Express by creating GLSL shader code (.html file with Three.js)

First, undertake this task:

## SHADER CONCEPT CREATION

To begin, create a SHADER CONCEPT (not static images or templates) that will be interpreted through:
- Mathematical functions and transformations
- UV coordinate manipulation
- Color gradients and blending
- Time-based animation
- Noise functions and fractals
- Distance fields and ray marching

### THE CRITICAL UNDERSTANDING
- What is received: User's description of desired visual effect
- What is created: A shader concept/visual aesthetic philosophy
- What happens next: The same version receives the concept and EXPRESSES IT IN GLSL - creating fragment shaders that are 90% mathematical expression, 10% essential parameters

Consider this approach:
- Write a manifesto for a shader aesthetic
- The next phase involves writing the GLSL code that brings it to life

The concept must emphasize: Mathematical beauty. Real-time execution. GPU-accelerated rendering. Parametric variation.

### HOW TO GENERATE A SHADER CONCEPT

**Name the shader** (1-3 words): "Plasma Waves" / "Fractal Noise" / "Ray Marched Sphere" / "Voronoi Cells"

**Articulate the concept** (4-6 paragraphs - concise but complete):

To capture the SHADER essence, express how this concept manifests through:
- UV coordinate transformations and distortions?
- Mathematical functions (sin, cos, smoothstep, mix)?
- Color theory and gradient blending?
- Time-based animation and evolution?
- Distance functions and signed distance fields?
- Noise functions (Perlin, Simplex, Voronoi)?

**CRITICAL GUIDELINES:**
- **Avoid redundancy**: Each shader technique should be mentioned once
- **Emphasize craftsmanship**: The shader should feel meticulously optimized, refined through countless iterations
- **Leave creative space**: Be specific about the visual direction, but allow room for implementation choices
- **Real-time focus**: Emphasize that this runs at 60fps on GPU

The concept must guide the next version to express ideas through GLSL mathematics, not through textures or images. Beauty lives in the equations.

### CONCEPT EXAMPLES

**"Plasma Waves"**
Concept: Undulating energy fields that pulse and flow across the screen.
Shader expression: Multiple sine waves at different frequencies combine to create interference patterns. UV coordinates are distorted by time-varying functions. Colors cycle through a gradient based on the combined wave values. The result is hypnotic, organic motion that never repeats exactly.

**"Fractal Noise"**
Concept: Self-similar patterns that reveal infinite detail at every scale.
Shader expression: Layered noise functions (FBM - Fractional Brownian Motion) create complex textures. Each octave adds finer detail. UV coordinates are scaled and rotated for each layer. Colors map to noise values creating terrain-like or cloud-like effects. Zoom and pan reveal endless variation.

**"Ray Marched Sphere"**
Concept: 3D geometry rendered through mathematical distance functions.
Shader expression: Ray marching algorithm steps through 3D space. Signed distance function defines a sphere. Lighting calculated from surface normals. Shadows and ambient occlusion add depth. All computed per-pixel in real-time - no 3D models, pure math.

**"Voronoi Cells"**
Concept: Organic cellular patterns based on closest-point calculations.
Shader expression: For each pixel, find the nearest point from a grid of random positions. Color based on distance to nearest and second-nearest points. Creates cell-like structures. Animate the points for living, breathing patterns. Edge detection highlights cell boundaries.

*These are condensed examples. The actual shader concept should be 4-6 substantial paragraphs.*

### ESSENTIAL PRINCIPLES
- **SHADER CONCEPT**: Creating a visual philosophy to be expressed through GLSL
- **REAL-TIME EXECUTION**: Always emphasize that this runs at 60fps on GPU
- **MATHEMATICAL EXPRESSION**: Ideas communicate through functions, not assets
- **PARAMETRIC CONTROL**: Expose key values as uniforms for real-time adjustment
- **PURE SHADER ART**: This is about GPU-accelerated mathematics, not image processing
- **EXPERT CRAFTSMANSHIP**: The final shader must feel optimized, refined, professional

**The shader concept should be 4-6 paragraphs long.** Output this concept as a .md file.

---

## GLSL SHADER IMPLEMENTATION

With the concept established, express it through code. Use only the shader concept created and the instructions below.

### TECHNICAL REQUIREMENTS

**Shader Structure**:
```glsl
// Uniforms (parameters from JavaScript)
uniform float u_time;
uniform vec2 u_resolution;
uniform float u_param1;
uniform vec3 u_color1;

// Varying (from vertex shader)
varying vec2 vUv;

void main() {
    // Normalize coordinates
    vec2 uv = vUv;
    
    // Your shader logic here
    
    // Output color
    gl_FragColor = vec4(color, 1.0);
}
```

**Essential Uniforms**:
- `u_time` - Time in seconds for animation
- `u_resolution` - Canvas resolution (width, height)
- Custom parameters for user control

**Common Shader Functions**:
```glsl
// Smooth interpolation
float smoothstep(float edge0, float edge1, float x);

// Mix two values
vec3 mix(vec3 a, vec3 b, float t);

// Fractional part
float fract(float x);

// Absolute value
float abs(float x);

// Sine/Cosine
float sin(float x);
float cos(float x);

// Length of vector
float length(vec2 v);

// Dot product
float dot(vec2 a, vec2 b);

// Clamp value
float clamp(float x, float min, float max);
```

**Noise Functions** (include if needed):
```glsl
// 2D Noise function
float noise(vec2 p) {
    vec2 i = floor(p);
    vec2 f = fract(p);
    f = f * f * (3.0 - 2.0 * f);
    float a = random(i);
    float b = random(i + vec2(1.0, 0.0));
    float c = random(i + vec2(0.0, 1.0));
    float d = random(i + vec2(1.0, 1.0));
    return mix(mix(a, b, f.x), mix(c, d, f.x), f.y);
}

// Random function
float random(vec2 st) {
    return fract(sin(dot(st.xy, vec2(12.9898,78.233))) * 43758.5453123);
}
```

### CRAFTSMANSHIP REQUIREMENTS

**CRITICAL**: Create shaders that feel professionally crafted:
- **Optimized**: Minimize expensive operations (avoid loops when possible)
- **Smooth**: Use smoothstep for anti-aliasing and smooth transitions
- **Balanced**: Visual complexity without performance issues
- **Colorful**: Thoughtful color palettes, not random RGB
- **Animated**: Smooth, purposeful motion (if animated)

### OUTPUT FORMAT

Output:
1. **Shader Concept** - As markdown explaining the visual aesthetic
2. **Single HTML Artifact** - Self-contained interactive shader viewer with Three.js

The HTML artifact contains everything: Three.js (from CDN), the GLSL shader, parameter controls, and UI - all in one file.

---

## INTERACTIVE SHADER VIEWER

Create a single, self-contained HTML artifact that works immediately in claude.ai or any browser.

### REQUIRED STRUCTURE

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Shader Name</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: #f5f5f5;
            overflow: hidden;
        }
        #container {
            display: flex;
            height: 100vh;
        }
        #canvas-container {
            flex: 1;
            position: relative;
        }
        canvas {
            display: block;
            width: 100%;
            height: 100%;
        }
        #controls {
            width: 320px;
            background: white;
            padding: 24px;
            overflow-y: auto;
            box-shadow: -2px 0 8px rgba(0,0,0,0.1);
        }
        h1 {
            font-size: 24px;
            font-weight: 600;
            margin-bottom: 8px;
            color: #191919;
        }
        .description {
            font-size: 14px;
            color: #666;
            margin-bottom: 24px;
            line-height: 1.5;
        }
        .control-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            font-size: 13px;
            font-weight: 500;
            color: #191919;
            margin-bottom: 8px;
        }
        input[type="range"] {
            width: 100%;
            height: 4px;
            border-radius: 2px;
            background: #e0e0e0;
            outline: none;
            -webkit-appearance: none;
        }
        input[type="range"]::-webkit-slider-thumb {
            -webkit-appearance: none;
            appearance: none;
            width: 16px;
            height: 16px;
            border-radius: 50%;
            background: #191919;
            cursor: pointer;
        }
        input[type="color"] {
            width: 100%;
            height: 40px;
            border: 1px solid #e0e0e0;
            border-radius: 4px;
            cursor: pointer;
        }
        .value-display {
            display: inline-block;
            font-size: 12px;
            color: #666;
            margin-left: 8px;
        }
        button {
            width: 100%;
            padding: 12px;
            background: #191919;
            color: white;
            border: none;
            border-radius: 4px;
            font-size: 14px;
            font-weight: 500;
            cursor: pointer;
            margin-top: 8px;
        }
        button:hover {
            background: #333;
        }
        .section-title {
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: #999;
            margin: 24px 0 12px 0;
        }
    </style>
</head>
<body>
    <div id="container">
        <div id="canvas-container"></div>
        <div id="controls">
            <h1>Shader Name</h1>
            <p class="description">Brief description of what this shader does.</p>
            
            <div class="section-title">Parameters</div>
            
            <!-- Parameter controls go here -->
            <div class="control-group">
                <label>Parameter Name</label>
                <input type="range" id="param1" min="0" max="1" step="0.01" value="0.5">
                <span class="value-display" id="param1-value">0.5</span>
            </div>
            
            <div class="section-title">Colors</div>
            
            <!-- Color controls go here -->
            <div class="control-group">
                <label>Color 1</label>
                <input type="color" id="color1" value="#ff0000">
            </div>
            
            <div class="section-title">Actions</div>
            <button onclick="resetParameters()">Reset to Defaults</button>
            <button onclick="downloadImage()">Download PNG</button>
        </div>
    </div>

    <script>
        // Shader parameters
        const params = {
            param1: 0.5,
            color1: new THREE.Color(0xff0000),
            // Add more parameters
        };

        // Three.js setup
        const scene = new THREE.Scene();
        const camera = new THREE.OrthographicCamera(-1, 1, 1, -1, 0, 1);
        const renderer = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true });
        
        const container = document.getElementById('canvas-container');
        renderer.setSize(container.clientWidth, container.clientHeight);
        container.appendChild(renderer.domElement);

        // Shader material
        const material = new THREE.ShaderMaterial({
            uniforms: {
                u_time: { value: 0 },
                u_resolution: { value: new THREE.Vector2(container.clientWidth, container.clientHeight) },
                u_param1: { value: params.param1 },
                u_color1: { value: params.color1 },
                // Add more uniforms
            },
            vertexShader: `
                varying vec2 vUv;
                void main() {
                    vUv = uv;
                    gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
                }
            `,
            fragmentShader: `
                uniform float u_time;
                uniform vec2 u_resolution;
                uniform float u_param1;
                uniform vec3 u_color1;
                
                varying vec2 vUv;
                
                void main() {
                    vec2 uv = vUv;
                    
                    // YOUR SHADER CODE HERE
                    vec3 color = vec3(uv.x, uv.y, 0.5);
                    
                    gl_FragColor = vec4(color, 1.0);
                }
            `
        });

        // Create plane
        const geometry = new THREE.PlaneGeometry(2, 2);
        const plane = new THREE.Mesh(geometry, material);
        scene.add(plane);

        // Animation loop
        function animate() {
            requestAnimationFrame(animate);
            material.uniforms.u_time.value = performance.now() / 1000;
            renderer.render(scene, camera);
        }
        animate();

        // Handle window resize
        window.addEventListener('resize', () => {
            const width = container.clientWidth;
            const height = container.clientHeight;
            renderer.setSize(width, height);
            material.uniforms.u_resolution.value.set(width, height);
        });

        // Parameter update functions
        function updateParam(name, value) {
            params[name] = parseFloat(value);
            material.uniforms['u_' + name].value = params[name];
            document.getElementById(name + '-value').textContent = value;
        }

        function updateColor(name, value) {
            params[name].setStyle(value);
            material.uniforms['u_' + name].value = params[name];
        }

        // Reset function
        function resetParameters() {
            // Reset all parameters to defaults
            document.getElementById('param1').value = 0.5;
            updateParam('param1', 0.5);
            // Reset other parameters
        }

        // Download function
        function downloadImage() {
            const link = document.createElement('a');
            link.download = 'shader.png';
            link.href = renderer.domElement.toDataURL();
            link.click();
        }

        // Initialize UI
        document.getElementById('param1').addEventListener('input', (e) => {
            updateParam('param1', e.target.value);
        });
        
        document.getElementById('color1').addEventListener('input', (e) => {
            updateColor('color1', e.target.value);
        });
    </script>
</body>
</html>
```

### REQUIRED FEATURES

**1. Parameter Controls**
- Sliders for numeric parameters (speed, scale, intensity, etc.)
- Color pickers for color parameters
- Real-time updates when parameters change
- Value displays next to sliders
- Reset button to restore defaults

**2. Shader Uniforms**
- `u_time` - Animated time value
- `u_resolution` - Canvas resolution
- Custom parameters as uniforms
- Color parameters as vec3

**3. Actions**
- Reset button (restore default parameters)
- Download PNG button (save current frame)

**4. Responsive**
- Canvas fills available space
- Sidebar fixed width (320px)
- Handles window resize
- Mobile-friendly (if possible)

### SHADER BEST PRACTICES

**Performance**:
- Avoid loops when possible (unroll or use mathematical tricks)
- Minimize texture lookups
- Use built-in functions (smoothstep, mix, etc.)
- Keep fragment shader simple for real-time performance

**Visual Quality**:
- Use smoothstep for anti-aliasing
- Blend colors smoothly with mix()
- Add subtle animation with u_time
- Consider aspect ratio (u_resolution.x / u_resolution.y)

**Code Organization**:
- Define helper functions at top of shader
- Comment complex mathematical operations
- Use meaningful variable names
- Keep main() function clean and readable

---

## SHADER TECHNIQUES

### Common Patterns

**1. UV Manipulation**:
```glsl
// Center coordinates
vec2 uv = vUv * 2.0 - 1.0;
uv.x *= u_resolution.x / u_resolution.y; // Aspect ratio

// Polar coordinates
float angle = atan(uv.y, uv.x);
float radius = length(uv);

// Repeat/tile
vec2 tiled = fract(uv * 5.0);
```

**2. Shapes**:
```glsl
// Circle
float circle = 1.0 - smoothstep(0.4, 0.41, length(uv));

// Rectangle
float rect = step(abs(uv.x), 0.5) * step(abs(uv.y), 0.5);

// Smooth shapes
float smoothCircle = smoothstep(0.5, 0.4, length(uv));
```

**3. Patterns**:
```glsl
// Stripes
float stripes = sin(uv.x * 10.0) * 0.5 + 0.5;

// Checkerboard
float checker = mod(floor(uv.x * 10.0) + floor(uv.y * 10.0), 2.0);

// Waves
float wave = sin(uv.x * 10.0 + u_time) * 0.5 + 0.5;
```

**4. Colors**:
```glsl
// Gradient
vec3 color = mix(color1, color2, uv.x);

// HSV to RGB
vec3 hsv2rgb(vec3 c) {
    vec4 K = vec4(1.0, 2.0 / 3.0, 1.0 / 3.0, 3.0);
    vec3 p = abs(fract(c.xxx + K.xyz) * 6.0 - K.www);
    return c.z * mix(K.xxx, clamp(p - K.xxx, 0.0, 1.0), c.y);
}

// Palette
vec3 palette(float t) {
    vec3 a = vec3(0.5, 0.5, 0.5);
    vec3 b = vec3(0.5, 0.5, 0.5);
    vec3 c = vec3(1.0, 1.0, 1.0);
    vec3 d = vec3(0.0, 0.33, 0.67);
    return a + b * cos(6.28318 * (c * t + d));
}
```

**5. Noise** (include helper functions):
```glsl
// FBM (Fractional Brownian Motion)
float fbm(vec2 p) {
    float value = 0.0;
    float amplitude = 0.5;
    for(int i = 0; i < 5; i++) {
        value += amplitude * noise(p);
        p *= 2.0;
        amplitude *= 0.5;
    }
    return value;
}
```

---

## THE CREATIVE PROCESS

**User request** → **Shader concept** → **GLSL implementation**

Each request is unique. The process involves:

1. **Interpret the user's intent** - What visual effect is being sought?
2. **Create a shader concept** (4-6 paragraphs) describing the approach
3. **Implement it in GLSL** - Write the fragment shader
4. **Design appropriate parameters** - What should be adjustable?
5. **Build matching UI controls** - Sliders/color pickers for those parameters

**The constants**:
- Three.js setup and structure
- Clean, minimal UI
- Real-time parameter updates
- Self-contained HTML artifact

**Everything else is variable**:
- The shader code itself
- The parameters
- The visual outcome
- The animation (if any)

To achieve the best results, trust creativity and let the concept guide the implementation.

---

## EXAMPLES OF SHADER TYPES

**Procedural Textures**:
- Noise-based patterns
- Fractals and FBM
- Voronoi cells
- Perlin noise variations

**Animated Effects**:
- Plasma waves
- Flowing patterns
- Pulsing shapes
- Rotating elements

**Geometric Patterns**:
- Grids and tiles
- Radial patterns
- Kaleidoscope effects
- Mandala-like designs

**Ray Marching** (advanced):
- 3D shapes from distance functions
- Lighting and shadows
- Reflections
- Volumetric effects

**Post-Processing**:
- Color grading
- Distortion effects
- Glitch effects
- Chromatic aberration

---

## FINAL NOTES

- **Keep it real-time**: Shaders must run at 60fps
- **Make it interactive**: Parameters should meaningfully affect the output
- **Optimize**: GPU time is precious, avoid expensive operations
- **Document**: Comment complex math or techniques
- **Test**: Ensure it works in claude.ai artifacts and browsers

The goal is to create beautiful, real-time, GPU-accelerated visual effects that users can explore through parameter adjustment.
