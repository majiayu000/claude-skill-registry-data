---
name: glsl-shader-development
description: GLSL shader programming expertise for visual effects, 3D graphics, and GPU computing. Use when writing fragment/vertex shaders, implementing ray marching.
---

# GLSL Shader Development

Structured guidance for writing GLSL shaders that produce correct visual output, run efficiently on the GPU, and integrate cleanly with WebGL and Three.js pipelines. Covers shader fundamentals, signed distance functions, ray marching, lighting models, procedural generation, post-processing effects, animation, and integration patterns.

## When to Use This Skill

Use this skill for:

- Writing vertex or fragment shaders in GLSL (ES 1.0, ES 3.0, or desktop GL)
- Implementing ray marching with signed distance functions for 3D scenes
- Building procedural textures and terrain with noise functions and FBM
- Creating post-processing effects (bloom, blur, chromatic aberration, color grading)
- Implementing physically-based rendering (PBR) or classical lighting models in shaders
- Integrating custom shaders into Three.js, WebGL, or ShaderToy
- Optimizing shader performance for mobile and low-end GPUs
- Animating shader parameters with time, mouse input, or audio data

**Trigger phrases**: "GLSL", "shader", "fragment shader", "vertex shader", "ray marching", "SDF", "signed distance function", "procedural generation", "noise function", "post-processing", "bloom", "depth of field", "ShaderToy", "WebGL", "Three.js shader", "PBR shader", "Cook-Torrance", "Perlin noise", "Simplex noise", "domain warping", "FBM", "sphere tracing", "screen-space effects"

## What This Skill Does

Provides GLSL shader development patterns including:

- **Shader Fundamentals**: Data types, precision qualifiers, uniforms, varyings, built-in variables, pipeline stages
- **Signed Distance Functions**: SDF primitives, CSG operations, smooth blending, repetition, domain transforms
- **Ray Marching**: Sphere tracing, camera setup, normal estimation, ambient occlusion, soft shadows
- **Lighting Models**: Phong, Blinn-Phong, PBR Cook-Torrance, Fresnel, environment mapping, HDR
- **Procedural Generation**: Perlin noise, Simplex noise, Worley noise, FBM, domain warping, terrain synthesis
- **Post-Processing**: Bloom, motion blur, depth of field, chromatic aberration, vignette, FXAA, color grading
- **Animation**: Time-based motion, easing functions, mouse interaction, morphing, particle systems
- **Integration**: Three.js ShaderMaterial, raw WebGL setup, uniform management, performance profiling

## Instructions

### Step 1: GLSL Fundamentals

GLSL (OpenGL Shading Language) runs on the GPU in two primary stages: the vertex shader transforms geometry, and the fragment shader computes per-pixel color. Understanding the data flow between these stages and the host application is essential.

**Shader Types and Pipeline**:

| Stage | Purpose | Runs Per | Key Outputs |
|-------|---------|----------|-------------|
| Vertex Shader | Transform vertex positions, pass data to fragment | Vertex | `gl_Position`, varyings |
| Fragment Shader | Compute final pixel color | Fragment/pixel | `gl_FragColor` / `fragColor` |
| Compute Shader | General GPU compute (GL 4.3+, not WebGL) | Work group | Buffer writes |

**Data Types**:

```glsl
// Scalar types
float f = 1.0;        // Always use decimal point (1.0 not 1)
int   i = 42;
bool  b = true;

// Vector types: vec2, vec3, vec4 (float); ivec2..4 (int); bvec2..4 (bool)
vec2 uv = vec2(0.5, 0.5);
vec3 color = vec3(1.0, 0.0, 0.0);        // Red
vec4 rgba = vec4(color, 1.0);             // Construct from vec3 + float

// Swizzling: access components as .xyzw, .rgba, or .stpq
vec3 normal = rgba.xyz;
vec2 rg = color.rg;
vec3 flipped = color.zyx;                 // Reorder components

// Matrix types: mat2, mat3, mat4 (column-major)
mat3 rotation = mat3(
    cos(a), -sin(a), 0.0,
    sin(a),  cos(a), 0.0,
    0.0,     0.0,    1.0
);

// Samplers (texture handles, set from host)
uniform sampler2D uTexture;
uniform samplerCube uEnvMap;
```

**Precision Qualifiers** (critical for mobile/WebGL):

```glsl
// Fragment shaders in GLSL ES require explicit precision
precision highp float;     // 32-bit; use for positions and ray marching
precision mediump float;   // 16-bit; adequate for color, UVs on mobile
precision lowp float;      // 10-bit; sufficient for simple color lookups

// Per-variable override when global precision is mediump
highp vec3 worldPos = uCameraPos + rd * t;
```

**Uniforms, Attributes, and Varyings**:

```glsl
// ---- Vertex Shader (GLSL ES 1.0 / WebGL 1) ----
attribute vec3 aPosition;          // Per-vertex input from buffer
attribute vec2 aTexCoord;
uniform mat4 uModelViewProjection; // Set by host once per draw call
uniform float uTime;
varying vec2 vTexCoord;            // Interpolated to fragment shader
varying vec3 vWorldPos;

void main() {
    vTexCoord = aTexCoord;
    vWorldPos = aPosition;
    gl_Position = uModelViewProjection * vec4(aPosition, 1.0);
}

// ---- Fragment Shader (GLSL ES 1.0 / WebGL 1) ----
precision highp float;
uniform sampler2D uTexture;
uniform vec3 uLightDir;
varying vec2 vTexCoord;
varying vec3 vWorldPos;

void main() {
    vec4 texColor = texture2D(uTexture, vTexCoord);
    gl_FragColor = texColor;
}
```

**GLSL ES 3.0 (WebGL 2) differences**:

```glsl
#version 300 es
precision highp float;

// 'attribute' becomes 'in', 'varying' becomes 'in'/'out'
in vec3 aPosition;          // vertex shader input
out vec2 vTexCoord;          // vertex shader output / fragment shader input

// texture2D() becomes texture()
// gl_FragColor is replaced by a declared output
out vec4 fragColor;

void main() {
    fragColor = texture(uTexture, vTexCoord);
}
```

**ShaderToy vs WebGL vs Three.js Pipeline Comparison**:

| Feature | ShaderToy | Raw WebGL | Three.js ShaderMaterial |
|---------|-----------|-----------|------------------------|
| Entry point | `mainImage(out vec4, in vec2)` | `void main()` | `void main()` |
| Screen coords | `fragCoord` (pixel), `iResolution` | `gl_FragCoord` | `vUv` (0-1 range) |
| Time | `iTime` | Custom `uniform float uTime` | Custom uniform |
| Mouse | `iMouse` (vec4) | Custom uniform | Custom uniform |
| Textures | `iChannel0..3` | Custom sampler2D | Custom sampler2D |
| Output | `fragColor` parameter | `gl_FragColor` / out var | `gl_FragColor` / out var |

**Built-in Functions** (most commonly used):

```glsl
// Math
float a = mix(x, y, t);          // Linear interpolation: x*(1-t) + y*t
float b = clamp(x, 0.0, 1.0);   // Constrain to range
float c = smoothstep(e0, e1, x); // Hermite interpolation (smooth clamp)
float d = step(edge, x);         // 0.0 if x < edge, else 1.0
float e = fract(x);              // x - floor(x)
float f = mod(x, y);             // x - y * floor(x/y)

// Vector operations
float  len = length(v);
vec3   n   = normalize(v);
float  d   = dot(a, b);
vec3   c   = cross(a, b);
float  dst = distance(a, b);
vec3   r   = reflect(incident, normal);
vec3   rf  = refract(incident, normal, eta);

// Trigonometry
float s = sin(x);   float c = cos(x);   float t = tan(x);
float a = asin(x);  float a = acos(x);  float a = atan(y, x);
```

### Step 2: Signed Distance Functions (SDFs)

A signed distance function returns the shortest distance from a point to the surface of an object. Negative values indicate the point is inside the object. SDFs are the building blocks for ray marched scenes.

**SDF Primitives**:

```glsl
// Sphere centered at origin with given radius
float sdSphere(vec3 p, float r) {
    return length(p) - r;
}

// Box centered at origin with half-extents b
float sdBox(vec3 p, vec3 b) {
    vec3 q = abs(p) - b;
    return length(max(q, 0.0)) + min(max(q.x, max(q.y, q.z)), 0.0);
}

// Round box: box with rounded edges
float sdRoundBox(vec3 p, vec3 b, float r) {
    vec3 q = abs(p) - b + r;
    return length(max(q, 0.0)) + min(max(q.x, max(q.y, q.z)), 0.0) - r;
}

// Torus centered at origin, lying in the XZ plane
// t.x = major radius, t.y = minor radius
float sdTorus(vec3 p, vec2 t) {
    vec2 q = vec2(length(p.xz) - t.x, p.y);
    return length(q) - t.y;
}

// Infinite cylinder along the Y axis
float sdCylinder(vec3 p, float r) {
    return length(p.xz) - r;
}

// Capped cylinder with height h and radius r
float sdCappedCylinder(vec3 p, float h, float r) {
    vec2 d = abs(vec2(length(p.xz), p.y)) - vec2(r, h);
    return min(max(d.x, d.y), 0.0) + length(max(d, 0.0));
}

// Plane with normal n (must be normalized) at height h
float sdPlane(vec3 p, vec3 n, float h) {
    return dot(p, n) + h;
}

// Capsule from point a to point b with radius r
float sdCapsule(vec3 p, vec3 a, vec3 b, float r) {
    vec3 pa = p - a, ba = b - a;
    float h = clamp(dot(pa, ba) / dot(ba, ba), 0.0, 1.0);
    return length(pa - ba * h) - r;
}
```

**CSG (Constructive Solid Geometry) Operations**:

```glsl
// Union: combine two shapes (take the closer surface)
float opUnion(float d1, float d2) {
    return min(d1, d2);
}

// Intersection: keep only the overlapping region
float opIntersection(float d1, float d2) {
    return max(d1, d2);
}

// Subtraction: cut d2 out of d1
float opSubtraction(float d1, float d2) {
    return max(d1, -d2);
}

// Smooth union: blend two shapes with smooth transition
// k controls the blending radius (try 0.1 to 0.5)
float opSmoothUnion(float d1, float d2, float k) {
    float h = clamp(0.5 + 0.5 * (d2 - d1) / k, 0.0, 1.0);
    return mix(d2, d1, h) - k * h * (1.0 - h);
}

// Smooth subtraction
float opSmoothSubtraction(float d1, float d2, float k) {
    float h = clamp(0.5 - 0.5 * (d2 + d1) / k, 0.0, 1.0);
    return mix(d2, -d1, h) + k * h * (1.0 - h);
}

// Smooth intersection
float opSmoothIntersection(float d1, float d2, float k) {
    float h = clamp(0.5 - 0.5 * (d2 - d1) / k, 0.0, 1.0);
    return mix(d2, d1, h) + k * h * (1.0 - h);
}
```

**Domain Operations** (transform space, not geometry):

```glsl
// Infinite repetition along all axes with spacing s
float opRep(vec3 p, vec3 s) {
    vec3 q = mod(p + 0.5 * s, s) - 0.5 * s;
    return sdSphere(q, 0.25); // Replace with any SDF
}

// Limited repetition: repeat n times in each direction
float opRepLimited(vec3 p, vec3 s, vec3 n) {
    vec3 q = p - s * clamp(round(p / s), -n, n);
    return sdSphere(q, 0.25);
}

// Symmetry: mirror across the YZ plane
float opSymX(vec3 p) {
    p.x = abs(p.x);
    return sdBox(p - vec3(1.0, 0.0, 0.0), vec3(0.5));
}

// Twist around the Y axis
vec3 opTwist(vec3 p, float k) {
    float c = cos(k * p.y);
    float s = sin(k * p.y);
    mat2 m = mat2(c, -s, s, c);
    return vec3(m * p.xz, p.y);
}

// Bend along the X axis
vec3 opBend(vec3 p, float k) {
    float c = cos(k * p.x);
    float s = sin(k * p.x);
    mat2 m = mat2(c, -s, s, c);
    vec2 bent = m * p.xy;
    return vec3(bent, p.z);
}
```

**Complete SDF Scene Example**:

```glsl
// Scene: a sphere sitting on a plane with a smooth-blended torus
float map(vec3 p) {
    float ground = sdPlane(p, vec3(0.0, 1.0, 0.0), 0.0);
    float sphere = sdSphere(p - vec3(0.0, 1.0, 0.0), 1.0);
    float torus  = sdTorus(p - vec3(0.0, 1.0, 0.0), vec2(1.2, 0.3));
    float blob   = opSmoothUnion(sphere, torus, 0.3);
    return opUnion(ground, blob);
}
```

### Step 3: Ray Marching

Ray marching (sphere tracing) evaluates the scene SDF along each ray, stepping forward by the distance returned by the SDF. When the distance falls below a threshold, the ray has hit a surface.

**Core Sphere Tracing Algorithm**:

```glsl
const int MAX_STEPS = 128;
const float MAX_DIST = 100.0;
const float SURF_DIST = 0.001;  // Hit threshold

// Returns the distance along the ray to the nearest surface,
// or MAX_DIST if no hit was found.
float rayMarch(vec3 ro, vec3 rd) {
    float t = 0.0;
    for (int i = 0; i < MAX_STEPS; i++) {
        vec3 p = ro + rd * t;
        float d = map(p);       // Scene SDF
        if (d < SURF_DIST) break;
        t += d;
        if (t > MAX_DIST) break;
    }
    return t;
}
```

**Camera Setup** (look-at camera for ray marched scenes):

```glsl
// Build a camera matrix from eye position, target, and up vector.
// Returns the ray direction for a given screen coordinate.
mat3 setCamera(vec3 eye, vec3 target, float roll) {
    vec3 cw = normalize(target - eye);              // Forward
    vec3 cp = vec3(sin(roll), cos(roll), 0.0);      // Up with roll
    vec3 cu = normalize(cross(cw, cp));              // Right
    vec3 cv = normalize(cross(cu, cw));              // True up
    return mat3(cu, cv, cw);
}

void mainImage(out vec4 fragColor, in vec2 fragCoord) {
    // Normalized coordinates: [-aspect, aspect] x [-1, 1]
    vec2 uv = (fragCoord - 0.5 * iResolution.xy) / iResolution.y;

    // Camera position orbiting the origin
    float angle = iTime * 0.3;
    vec3 ro = vec3(4.0 * cos(angle), 2.5, 4.0 * sin(angle));
    vec3 target = vec3(0.0, 0.5, 0.0);

    // Camera-to-world matrix; 1.5 is the focal length (zoom)
    mat3 cam = setCamera(ro, target, 0.0);
    vec3 rd = cam * normalize(vec3(uv, 1.5));

    // Ray march
    float t = rayMarch(ro, rd);

    // Shade
    vec3 col = vec3(0.0);
    if (t < MAX_DIST) {
        vec3 p = ro + rd * t;
        vec3 n = getNormal(p);
        col = shade(p, n, rd);
    }

    // Gamma correction
    col = pow(col, vec3(1.0 / 2.2));
    fragColor = vec4(col, 1.0);
}
```

**Normal Estimation** (central differences on the SDF):

```glsl
vec3 getNormal(vec3 p) {
    vec2 e = vec2(0.0001, 0.0);
    return normalize(vec3(
        map(p + e.xyy) - map(p - e.xyy),
        map(p + e.yxy) - map(p - e.yxy),
        map(p + e.yyx) - map(p - e.yyx)
    ));
}

// Tetrahedron technique (4 samples instead of 6, slightly cheaper):
vec3 getNormalTet(vec3 p) {
    const vec2 e = vec2(1.0, -1.0) * 0.0001;
    return normalize(
        e.xyy * map(p + e.xyy) +
        e.yyx * map(p + e.yyx) +
        e.yxy * map(p + e.yxy) +
        e.xxx * map(p + e.xxx)
    );
}
```

**Ambient Occlusion** (approximated via SDF sampling along the normal):

```glsl
float calcAO(vec3 p, vec3 n) {
    float occ = 0.0;
    float decay = 1.0;
    for (int i = 1; i <= 5; i++) {
        float h = 0.01 + 0.12 * float(i);
        float d = map(p + n * h);
        occ += (h - d) * decay;
        decay *= 0.95;
    }
    return clamp(1.0 - 3.0 * occ, 0.0, 1.0);
}
```

**Soft Shadows** (penumbra via closest approach during marching):

```glsl
// March from surface point toward the light.
// k controls shadow softness (higher = harder, try 8.0-32.0).
float softShadow(vec3 ro, vec3 rd, float mint, float maxt, float k) {
    float res = 1.0;
    float t = mint;
    for (int i = 0; i < 64; i++) {
        float d = map(ro + rd * t);
        if (d < 0.001) return 0.0;   // Fully in shadow
        res = min(res, k * d / t);
        t += clamp(d, 0.02, 0.2);
        if (t > maxt) break;
    }
    return clamp(res, 0.0, 1.0);
}
```

### Step 4: Lighting Models

Lighting models compute surface color from material properties, light direction, view direction, and surface normals.

**Blinn-Phong Lighting** (classical model, suitable for non-photorealistic rendering):

```glsl
struct Light {
    vec3 direction;  // Normalized direction toward the light
    vec3 color;
    float intensity;
};

vec3 blinnPhong(vec3 p, vec3 n, vec3 viewDir, vec3 albedo) {
    Light sun;
    sun.direction = normalize(vec3(0.8, 0.4, 0.6));
    sun.color = vec3(1.0, 0.95, 0.9);
    sun.intensity = 1.2;

    // Ambient
    vec3 ambient = 0.15 * albedo;

    // Diffuse (Lambertian)
    float diff = max(dot(n, sun.direction), 0.0);
    vec3 diffuse = diff * albedo * sun.color * sun.intensity;

    // Specular (Blinn-Phong half-vector)
    vec3 halfDir = normalize(sun.direction + viewDir);
    float spec = pow(max(dot(n, halfDir), 0.0), 64.0);
    vec3 specular = spec * sun.color * 0.5;

    // Shadow
    float shadow = softShadow(p + n * 0.01, sun.direction, 0.01, 20.0, 16.0);

    // Ambient occlusion
    float ao = calcAO(p, n);

    return ambient * ao + (diffuse + specular) * shadow;
}
```

**Physically-Based Rendering (PBR) with Cook-Torrance BRDF**:

```glsl
// Material parameters
struct Material {
    vec3  albedo;      // Base color
    float metallic;    // 0.0 = dielectric, 1.0 = metal
    float roughness;   // 0.0 = mirror, 1.0 = diffuse
    float ao;          // Ambient occlusion (pre-baked or computed)
};

const float PI = 3.14159265359;

// Normal Distribution Function (GGX/Trowbridge-Reitz)
float distributionGGX(vec3 N, vec3 H, float roughness) {
    float a  = roughness * roughness;
    float a2 = a * a;
    float NdotH = max(dot(N, H), 0.0);
    float NdotH2 = NdotH * NdotH;
    float denom = NdotH2 * (a2 - 1.0) + 1.0;
    return a2 / (PI * denom * denom);
}

// Geometry function (Smith's method with Schlick-GGX)
float geometrySchlickGGX(float NdotV, float roughness) {
    float r = roughness + 1.0;
    float k = (r * r) / 8.0;
    return NdotV / (NdotV * (1.0 - k) + k);
}

float geometrySmith(vec3 N, vec3 V, vec3 L, float roughness) {
    float NdotV = max(dot(N, V), 0.0);
    float NdotL = max(dot(N, L), 0.0);
    return geometrySchlickGGX(NdotV, roughness)
         * geometrySchlickGGX(NdotL, roughness);
}

// Fresnel (Schlick approximation)
vec3 fresnelSchlick(float cosTheta, vec3 F0) {
    return F0 + (1.0 - F0) * pow(clamp(1.0 - cosTheta, 0.0, 1.0), 5.0);
}

// Fresnel with roughness correction for ambient term
vec3 fresnelSchlickRoughness(float cosTheta, vec3 F0, float roughness) {
    return F0 + (max(vec3(1.0 - roughness), F0) - F0)
         * pow(clamp(1.0 - cosTheta, 0.0, 1.0), 5.0);
}

// Full PBR shading for a single point light
vec3 pbrShade(vec3 p, vec3 N, vec3 V, Material mat,
              vec3 lightPos, vec3 lightColor) {
    vec3 L = normalize(lightPos - p);
    vec3 H = normalize(V + L);

    float dist = length(lightPos - p);
    float attenuation = 1.0 / (dist * dist);
    vec3 radiance = lightColor * attenuation;

    // F0: reflectance at normal incidence
    // Dielectrics use 0.04; metals tint F0 with albedo
    vec3 F0 = mix(vec3(0.04), mat.albedo, mat.metallic);

    // Cook-Torrance specular BRDF
    float D = distributionGGX(N, H, mat.roughness);
    float G = geometrySmith(N, V, L, mat.roughness);
    vec3  F = fresnelSchlick(max(dot(H, V), 0.0), F0);

    vec3 numerator = D * G * F;
    float denominator = 4.0 * max(dot(N, V), 0.0)
                            * max(dot(N, L), 0.0) + 0.0001;
    vec3 specular = numerator / denominator;

    // Energy conservation: diffuse component
    vec3 kD = (vec3(1.0) - F) * (1.0 - mat.metallic);
    float NdotL = max(dot(N, L), 0.0);

    return (kD * mat.albedo / PI + specular) * radiance * NdotL;
}
```

**Environment Mapping** (approximate image-based lighting):

```glsl
// Sample a cubemap for reflections
vec3 envReflection(vec3 N, vec3 V, float roughness, samplerCube envMap) {
    vec3 R = reflect(-V, N);
    // Approximate LOD from roughness for pre-filtered env maps
    float lod = roughness * 6.0;
    vec3 envColor = textureLod(envMap, R, lod).rgb;
    return envColor;
}

// Simple sky gradient as a procedural environment (no cubemap needed)
vec3 skyColor(vec3 rd) {
    float t = 0.5 * (rd.y + 1.0);
    vec3 horizon = vec3(0.8, 0.85, 0.95);
    vec3 zenith  = vec3(0.3, 0.5, 0.9);
    return mix(horizon, zenith, t);
}
```

### Step 5: Procedural Generation

Procedural generation uses mathematical functions to create textures, terrain, and organic forms without pre-authored image data. Noise functions are the fundamental building blocks.

**Hash and Value Noise**:

```glsl
// Integer hash (for noise seed generation)
float hash(vec2 p) {
    vec3 p3 = fract(vec3(p.xyx) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return fract((p3.x + p3.y) * p3.z);
}

// 2D value noise
float valueNoise(vec2 p) {
    vec2 i = floor(p);
    vec2 f = fract(p);
    // Hermite interpolation (smoother than linear)
    vec2 u = f * f * (3.0 - 2.0 * f);

    float a = hash(i + vec2(0.0, 0.0));
    float b = hash(i + vec2(1.0, 0.0));
    float c = hash(i + vec2(0.0, 1.0));
    float d = hash(i + vec2(1.0, 1.0));

    return mix(mix(a, b, u.x), mix(c, d, u.x), u.y);
}
```

**Gradient Noise (Perlin-style)**:

```glsl
// 2D gradient noise
vec2 hashGrad(vec2 p) {
    p = vec2(dot(p, vec2(127.1, 311.7)),
             dot(p, vec2(269.5, 183.3)));
    return -1.0 + 2.0 * fract(sin(p) * 43758.5453123);
}

float gradientNoise(vec2 p) {
    vec2 i = floor(p);
    vec2 f = fract(p);
    vec2 u = f * f * f * (f * (f * 6.0 - 15.0) + 10.0); // Quintic curve

    return mix(
        mix(dot(hashGrad(i + vec2(0.0, 0.0)), f - vec2(0.0, 0.0)),
            dot(hashGrad(i + vec2(1.0, 0.0)), f - vec2(1.0, 0.0)), u.x),
        mix(dot(hashGrad(i + vec2(0.0, 1.0)), f - vec2(0.0, 1.0)),
            dot(hashGrad(i + vec2(1.0, 1.0)), f - vec2(1.0, 1.0)), u.x),
        u.y
    );
}
```

**Simplex Noise** (3D, fewer artifacts than Perlin):

```glsl
// 3D Simplex noise (based on Ashima Arts implementation)
vec3 mod289(vec3 x) { return x - floor(x * (1.0 / 289.0)) * 289.0; }
vec4 mod289(vec4 x) { return x - floor(x * (1.0 / 289.0)) * 289.0; }
vec4 permute(vec4 x) { return mod289(((x * 34.0) + 10.0) * x); }
vec4 taylorInvSqrt(vec4 r) { return 1.79284291400159 - 0.85373472095314 * r; }

float snoise(vec3 v) {
    const vec2 C = vec2(1.0 / 6.0, 1.0 / 3.0);
    const vec4 D = vec4(0.0, 0.5, 1.0, 2.0);
    vec3 i  = floor(v + dot(v, C.yyy));
    vec3 x0 = v - i + dot(i, C.xxx);
    vec3 g = step(x0.yzx, x0.xyz);
    vec3 l = 1.0 - g;
    vec3 i1 = min(g.xyz, l.zxy);
    vec3 i2 = max(g.xyz, l.zxy);
    vec3 x1 = x0 - i1 + C.xxx;
    vec3 x2 = x0 - i2 + C.yyy;
    vec3 x3 = x0 - D.yyy;
    i = mod289(i);
    vec4 p = permute(permute(permute(
        i.z + vec4(0.0, i1.z, i2.z, 1.0))
      + i.y + vec4(0.0, i1.y, i2.y, 1.0))
      + i.x + vec4(0.0, i1.x, i2.x, 1.0));
    float n_ = 0.142857142857;
    vec3 ns = n_ * D.wyz - D.xzx;
    vec4 j = p - 49.0 * floor(p * ns.z * ns.z);
    vec4 x_ = floor(j * ns.z);
    vec4 y_ = floor(j - 7.0 * x_);
    vec4 x = x_ * ns.x + ns.yyyy;
    vec4 y = y_ * ns.x + ns.yyyy;
    vec4 h = 1.0 - abs(x) - abs(y);
    vec4 b0 = vec4(x.xy, y.xy);
    vec4 b1 = vec4(x.zw, y.zw);
    vec4 s0 = floor(b0) * 2.0 + 1.0;
    vec4 s1 = floor(b1) * 2.0 + 1.0;
    vec4 sh = -step(h, vec4(0.0));
    vec4 a0 = b0.xzyw + s0.xzyw * sh.xxyy;
    vec4 a1 = b1.xzyw + s1.xzyw * sh.zzww;
    vec3 p0 = vec3(a0.xy, h.x);
    vec3 p1 = vec3(a0.zw, h.y);
    vec3 p2 = vec3(a1.xy, h.z);
    vec3 p3 = vec3(a1.zw, h.w);
    vec4 norm = taylorInvSqrt(vec4(dot(p0,p0), dot(p1,p1), dot(p2,p2), dot(p3,p3)));
    p0 *= norm.x; p1 *= norm.y; p2 *= norm.z; p3 *= norm.w;
    vec4 m = max(0.5 - vec4(dot(x0,x0), dot(x1,x1), dot(x2,x2), dot(x3,x3)), 0.0);
    m = m * m;
    return 105.0 * dot(m * m, vec4(dot(p0,x0), dot(p1,x1), dot(p2,x2), dot(p3,x3)));
}
```

**Worley (Cellular) Noise**:

```glsl
// 2D Worley noise: returns distance to nearest cell center
vec2 worley(vec2 p) {
    vec2 i = floor(p);
    vec2 f = fract(p);
    float d1 = 1.0;  // Nearest distance
    float d2 = 1.0;  // Second nearest distance

    for (int y = -1; y <= 1; y++) {
        for (int x = -1; x <= 1; x++) {
            vec2 neighbor = vec2(float(x), float(y));
            vec2 cellCenter = hash2(i + neighbor); // Random offset 0..1
            vec2 diff = neighbor + cellCenter - f;
            float d = length(diff);
            if (d < d1) {
                d2 = d1;
                d1 = d;
            } else if (d < d2) {
                d2 = d;
            }
        }
    }
    return vec2(d1, d2); // .x = nearest, .y = second nearest
}

vec2 hash2(vec2 p) {
    p = vec2(dot(p, vec2(127.1, 311.7)), dot(p, vec2(269.5, 183.3)));
    return fract(sin(p) * 43758.5453);
}
```

**Fractal Brownian Motion (FBM)** (layered noise octaves):

```glsl
// FBM with configurable octaves, lacunarity, and gain
float fbm(vec2 p, int octaves) {
    float value = 0.0;
    float amplitude = 0.5;
    float frequency = 1.0;
    float lacunarity = 2.0;   // Frequency multiplier per octave
    float gain = 0.5;         // Amplitude multiplier per octave (persistence)

    for (int i = 0; i < octaves; i++) {
        value += amplitude * gradientNoise(p * frequency);
        frequency *= lacunarity;
        amplitude *= gain;
    }
    return value;
}
```

**Domain Warping** (feed noise into itself for organic distortion):

```glsl
// Single-pass domain warp
float warpedNoise(vec2 p) {
    vec2 q = vec2(
        fbm(p + vec2(0.0, 0.0), 6),
        fbm(p + vec2(5.2, 1.3), 6)
    );
    return fbm(p + 4.0 * q, 6);
}

// Double-pass domain warp (more complex, painterly look)
float doubleWarp(vec2 p) {
    vec2 q = vec2(
        fbm(p + vec2(0.0, 0.0), 6),
        fbm(p + vec2(5.2, 1.3), 6)
    );
    vec2 r = vec2(
        fbm(p + 4.0 * q + vec2(1.7, 9.2), 6),
        fbm(p + 4.0 * q + vec2(8.3, 2.8), 6)
    );
    return fbm(p + 4.0 * r, 6);
}
```

**Terrain Generation** (height field from FBM for a ray marched landscape):

```glsl
float terrainHeight(vec2 xz) {
    float h = 0.0;
    float amp = 1.0;
    float freq = 0.005;
    for (int i = 0; i < 8; i++) {
        h += amp * gradientNoise(xz * freq);
        freq *= 2.0;
        amp *= 0.5;
    }
    // Ridge noise variant: fold the noise for sharp peaks
    // h = abs(h);
    return h * 40.0; // Scale to world units
}

// SDF for terrain: compare y against the height field
float mapTerrain(vec3 p) {
    return p.y - terrainHeight(p.xz);
}
```

### Step 6: Post-Processing Effects

Post-processing effects operate on the rendered image as a full-screen fragment shader pass. The scene is first rendered to a framebuffer texture, then processed.

**Bloom** (glow from bright areas):

```glsl
// Step 1: Extract bright pixels (threshold pass)
vec3 brightnessThreshold(vec3 color, float threshold) {
    float brightness = dot(color, vec3(0.2126, 0.7152, 0.0722)); // Luminance
    return (brightness > threshold) ? color : vec3(0.0);
}

// Step 2: Gaussian blur (two-pass separable, horizontal then vertical)
vec3 gaussianBlur(sampler2D tex, vec2 uv, vec2 direction, vec2 resolution) {
    vec3 result = vec3(0.0);
    float weights[5] = float[](0.227027, 0.1945946, 0.1216216, 0.054054, 0.016216);
    vec2 texelSize = 1.0 / resolution;

    result += texture(tex, uv).rgb * weights[0];
    for (int i = 1; i < 5; i++) {
        vec2 offset = direction * texelSize * float(i);
        result += texture(tex, uv + offset).rgb * weights[i];
        result += texture(tex, uv - offset).rgb * weights[i];
    }
    return result;
}

// Step 3: Combine original + blurred bright pixels
vec3 applyBloom(sampler2D sceneTex, sampler2D bloomTex, vec2 uv, float strength) {
    vec3 scene = texture(sceneTex, uv).rgb;
    vec3 bloom = texture(bloomTex, uv).rgb;
    return scene + bloom * strength;
}
```

**Depth of Field** (circle of confusion based on depth):

```glsl
vec3 depthOfField(sampler2D sceneTex, sampler2D depthTex, vec2 uv,
                  vec2 resolution, float focusDist, float aperture) {
    float depth = texture(depthTex, uv).r;
    float coc = abs(depth - focusDist) * aperture; // Circle of confusion
    coc = clamp(coc, 0.0, 1.0);

    vec3 result = vec3(0.0);
    float total = 0.0;
    int samples = 16;

    // Poisson disk sampling for bokeh shape
    for (int i = 0; i < samples; i++) {
        float angle = float(i) * 2.39996323;  // Golden angle
        float radius = sqrt(float(i) / float(samples)) * coc;
        vec2 offset = vec2(cos(angle), sin(angle)) * radius / resolution;
        result += texture(sceneTex, uv + offset).rgb;
        total += 1.0;
    }
    return result / total;
}
```

**Chromatic Aberration** (color channel separation):

```glsl
vec3 chromaticAberration(sampler2D tex, vec2 uv, float intensity) {
    vec2 dir = uv - 0.5; // Direction from center
    float d = length(dir);
    vec2 offset = dir * d * intensity;

    float r = texture(tex, uv + offset).r;
    float g = texture(tex, uv).g;
    float b = texture(tex, uv - offset).b;
    return vec3(r, g, b);
}
```

**Vignette** (darken edges):

```glsl
vec3 vignette(vec3 color, vec2 uv, float intensity, float smoothness) {
    float d = distance(uv, vec2(0.5));
    float vig = smoothstep(0.5, 0.5 - smoothness, d * (1.0 + intensity));
    return color * vig;
}
```

**Color Grading** (tone mapping and color adjustment):

```glsl
// ACES filmic tone mapping (standard for HDR to LDR conversion)
vec3 acesToneMap(vec3 x) {
    float a = 2.51;
    float b = 0.03;
    float c = 2.43;
    float d = 0.59;
    float e = 0.14;
    return clamp((x * (a * x + b)) / (x * (c * x + d) + e), 0.0, 1.0);
}

// Reinhard tone mapping (simpler alternative)
vec3 reinhardToneMap(vec3 color) {
    return color / (color + vec3(1.0));
}

// Color temperature adjustment (warm = positive, cool = negative)
vec3 colorTemperature(vec3 color, float temperature) {
    color.r *= 1.0 + temperature * 0.1;
    color.b *= 1.0 - temperature * 0.1;
    return clamp(color, 0.0, 1.0);
}

// Contrast and saturation
vec3 adjustContrast(vec3 color, float contrast) {
    return 0.5 + (color - 0.5) * contrast;
}

vec3 adjustSaturation(vec3 color, float saturation) {
    float luma = dot(color, vec3(0.2126, 0.7152, 0.0722));
    return mix(vec3(luma), color, saturation);
}

// Complete post-processing chain
vec3 postProcess(vec3 color, vec2 uv) {
    color = acesToneMap(color);                         // Tone map HDR to LDR
    color = adjustContrast(color, 1.1);                // Slight contrast boost
    color = adjustSaturation(color, 1.15);             // Slight saturation boost
    color = colorTemperature(color, 0.3);              // Warm tint
    color = vignette(color, uv, 0.3, 0.4);            // Subtle vignette
    color = pow(color, vec3(1.0 / 2.2));               // Gamma correction
    return color;
}
```

**FXAA** (Fast Approximate Anti-Aliasing):

```glsl
// Simplified single-pass FXAA
vec3 fxaa(sampler2D tex, vec2 uv, vec2 resolution) {
    vec2 texel = 1.0 / resolution;

    // Sample luminance at center and four neighbors
    float lumC  = dot(texture(tex, uv).rgb, vec3(0.299, 0.587, 0.114));
    float lumN  = dot(texture(tex, uv + vec2(0.0,  texel.y)).rgb, vec3(0.299, 0.587, 0.114));
    float lumS  = dot(texture(tex, uv + vec2(0.0, -texel.y)).rgb, vec3(0.299, 0.587, 0.114));
    float lumE  = dot(texture(tex, uv + vec2( texel.x, 0.0)).rgb, vec3(0.299, 0.587, 0.114));
    float lumW  = dot(texture(tex, uv + vec2(-texel.x, 0.0)).rgb, vec3(0.299, 0.587, 0.114));

    float lumMin = min(lumC, min(min(lumN, lumS), min(lumE, lumW)));
    float lumMax = max(lumC, max(max(lumN, lumS), max(lumE, lumW)));
    float lumRange = lumMax - lumMin;

    // Skip anti-aliasing if contrast is low
    if (lumRange < max(0.0312, lumMax * 0.125)) {
        return texture(tex, uv).rgb;
    }

    // Determine blur direction from gradient
    vec2 dir;
    dir.x = -((lumN + lumS) - 2.0 * lumC);
    dir.y =  ((lumE + lumW) - 2.0 * lumC);
    float dirReduce = max((lumN + lumS + lumE + lumW) * 0.25 * 0.25, 1.0 / 128.0);
    float rcpDirMin = 1.0 / (min(abs(dir.x), abs(dir.y)) + dirReduce);
    dir = clamp(dir * rcpDirMin, -8.0, 8.0) * texel;

    // Two-tap filter along the edge
    vec3 rgbA = 0.5 * (texture(tex, uv + dir * (1.0 / 3.0 - 0.5)).rgb
                      + texture(tex, uv + dir * (2.0 / 3.0 - 0.5)).rgb);
    vec3 rgbB = rgbA * 0.5 + 0.25 * (
                texture(tex, uv + dir * -0.5).rgb
              + texture(tex, uv + dir *  0.5).rgb);

    float lumB = dot(rgbB, vec3(0.299, 0.587, 0.114));
    return (lumB < lumMin || lumB > lumMax) ? rgbA : rgbB;
}
```

### Step 7: Animation and Interaction

Shaders run every frame. Animation is driven by uniforms (time, mouse position, audio data) that the host application updates each frame.

**Time-Based Animation**:

```glsl
// Oscillation patterns
float pulse    = sin(iTime * 2.0) * 0.5 + 0.5;       // 0..1 sine wave
float sawtooth = fract(iTime * 0.5);                    // 0..1 repeating ramp
float triangle = abs(fract(iTime * 0.5) * 2.0 - 1.0);  // 0..1..0 triangle

// Animate an SDF object position
vec3 animatedPos = vec3(
    sin(iTime) * 2.0,
    abs(sin(iTime * 2.0)) + 0.5,   // Bouncing (abs(sin) for always positive)
    cos(iTime) * 2.0
);

// Smooth start/stop with easing
float t = clamp(iTime / 3.0, 0.0, 1.0); // 0 to 1 over 3 seconds
float easeInOut = t * t * (3.0 - 2.0 * t);             // Smoothstep easing
float easeOutBounce = 1.0 - pow(1.0 - t, 3.0);         // Decelerate
float easeInElastic = pow(2.0, 10.0 * (t - 1.0))
                    * sin((t - 1.075) * 2.0 * PI / 0.3); // Elastic snap
```

**Mouse Interaction** (ShaderToy conventions):

```glsl
void mainImage(out vec4 fragColor, in vec2 fragCoord) {
    vec2 uv = fragCoord / iResolution.xy;

    // iMouse: .xy = current position (while pressed), .zw = click position
    vec2 mouse = iMouse.xy / iResolution.xy;

    // Use mouse to control camera orbit angle
    float yaw   = (mouse.x - 0.5) * PI * 2.0;
    float pitch  = (mouse.y - 0.5) * PI * 0.5;
    vec3 ro = vec3(
        5.0 * cos(yaw) * cos(pitch),
        5.0 * sin(pitch) + 1.0,
        5.0 * sin(yaw) * cos(pitch)
    );

    // Or use mouse to control a parameter (e.g., roughness slider)
    float roughness = mouse.x;
    float metallic  = mouse.y;
}
```

**Morphing Between Shapes** (SDF interpolation):

```glsl
float morphScene(vec3 p) {
    float sphere = sdSphere(p, 1.0);
    float box    = sdBox(p, vec3(0.8));
    float torus  = sdTorus(p, vec2(1.0, 0.3));

    // Cycle through shapes over time
    float t = fract(iTime * 0.2);  // 0..1 repeating
    float phase = t * 3.0;          // 0..3

    float d;
    if (phase < 1.0) {
        d = mix(sphere, box, smoothstep(0.0, 1.0, phase));
    } else if (phase < 2.0) {
        d = mix(box, torus, smoothstep(0.0, 1.0, phase - 1.0));
    } else {
        d = mix(torus, sphere, smoothstep(0.0, 1.0, phase - 2.0));
    }
    return d;
}
```

**Simple Particle System** (stateless, computed from time and index):

```glsl
// Stateless particle: position derived from hash and time
vec3 particlePos(int id, float time) {
    float fid = float(id);
    vec3 seed = vec3(
        hash(vec2(fid, 0.0)),
        hash(vec2(fid, 1.0)),
        hash(vec2(fid, 2.0))
    );

    float lifetime = 2.0 + seed.z * 3.0;           // 2-5 seconds
    float t = mod(time + seed.x * lifetime, lifetime) / lifetime; // 0..1

    vec3 origin = vec3(seed.x - 0.5, 0.0, seed.y - 0.5) * 4.0;
    vec3 velocity = vec3(0.0, 2.0, 0.0) + (seed - 0.5) * 0.5;
    vec3 gravity = vec3(0.0, -1.0, 0.0);

    return origin + velocity * t * lifetime + 0.5 * gravity * t * t * lifetime * lifetime;
}

// Render particles as glowing spheres in a ray marched scene
float particleField(vec3 p, float time) {
    float d = 1e10;
    for (int i = 0; i < 50; i++) {
        vec3 pp = particlePos(i, time);
        float fid = float(i);
        float lifetime = 2.0 + hash(vec2(fid, 2.0)) * 3.0;
        float t = mod(time + hash(vec2(fid, 0.0)) * lifetime, lifetime) / lifetime;
        float radius = 0.05 * sin(t * PI); // Grow then shrink
        d = min(d, sdSphere(p - pp, radius));
    }
    return d;
}
```

**Fluid Simulation Basics** (2D advection with noise for visual effect, not physical simulation):

```glsl
// Pseudo-fluid: advect UVs through a time-varying velocity field
vec3 fluidEffect(vec2 uv, float time) {
    vec2 vel = vec2(
        gradientNoise(uv * 3.0 + vec2(time * 0.3, 0.0)),
        gradientNoise(uv * 3.0 + vec2(0.0, time * 0.3))
    );

    // Advect the UV coordinates
    vec2 advected = uv + vel * 0.05;

    // Layer multiple noise scales for turbulence appearance
    float n1 = gradientNoise(advected * 4.0 + time * 0.2);
    float n2 = gradientNoise(advected * 8.0 - time * 0.15) * 0.5;
    float n3 = gradientNoise(advected * 16.0 + time * 0.1) * 0.25;
    float turbulence = n1 + n2 + n3;

    // Color map
    vec3 color = mix(
        vec3(0.0, 0.2, 0.4),  // Deep blue
        vec3(0.1, 0.6, 0.9),  // Light blue
        smoothstep(-0.5, 0.5, turbulence)
    );
    return color;
}
```

### Step 8: Integration and Optimization

This step covers integrating custom shaders into real applications and ensuring they perform well across devices.

**Three.js ShaderMaterial Integration**:

```javascript
// JavaScript: create a custom shader material in Three.js
import * as THREE from "three";

const vertexShader = `
    varying vec2 vUv;
    varying vec3 vWorldPos;

    void main() {
        vUv = uv;
        vWorldPos = (modelMatrix * vec4(position, 1.0)).xyz;
        gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
    }
`;

const fragmentShader = `
    precision highp float;
    uniform float uTime;
    uniform vec2 uResolution;
    uniform vec3 uCameraPos;
    varying vec2 vUv;
    varying vec3 vWorldPos;

    // Paste GLSL functions here (noise, SDFs, lighting, etc.)

    void main() {
        vec2 uv = vUv;
        vec3 color = vec3(0.0);
        // Your shader logic here
        gl_FragColor = vec4(color, 1.0);
    }
`;

const material = new THREE.ShaderMaterial({
    vertexShader,
    fragmentShader,
    uniforms: {
        uTime: { value: 0.0 },
        uResolution: { value: new THREE.Vector2(window.innerWidth, window.innerHeight) },
        uCameraPos: { value: new THREE.Vector3() },
    },
    // Optional settings:
    transparent: true,           // Enable if using alpha
    side: THREE.DoubleSide,      // Render both faces
    depthWrite: false,           // Disable for transparent overlays
});

// Update uniforms in the render loop
function animate(time) {
    material.uniforms.uTime.value = time * 0.001; // ms to seconds
    material.uniforms.uCameraPos.value.copy(camera.position);
    renderer.render(scene, camera);
    requestAnimationFrame(animate);
}

// Handle window resize
window.addEventListener("resize", () => {
    material.uniforms.uResolution.value.set(window.innerWidth, window.innerHeight);
});
```

**Raw WebGL Shader Setup** (minimal boilerplate):

```javascript
// Compile and link a shader program from source strings
function createShaderProgram(gl, vertSrc, fragSrc) {
    function compileShader(type, source) {
        const shader = gl.createShader(type);
        gl.shaderSource(shader, source);
        gl.compileShader(shader);
        if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
            const log = gl.getShaderInfoLog(shader);
            gl.deleteShader(shader);
            throw new Error(`Shader compile error: ${log}`);
        }
        return shader;
    }

    const vert = compileShader(gl.VERTEX_SHADER, vertSrc);
    const frag = compileShader(gl.FRAGMENT_SHADER, fragSrc);
    const program = gl.createProgram();
    gl.attachShader(program, vert);
    gl.attachShader(program, frag);
    gl.linkProgram(program);

    if (!gl.getProgramParameter(program, gl.LINK_STATUS)) {
        const log = gl.getProgramInfoLog(program);
        gl.deleteProgram(program);
        throw new Error(`Program link error: ${log}`);
    }

    gl.deleteShader(vert);
    gl.deleteShader(frag);
    return program;
}

// Set uniform values by type
function setUniforms(gl, program, uniforms) {
    for (const [name, value] of Object.entries(uniforms)) {
        const loc = gl.getUniformLocation(program, name);
        if (loc === null) continue; // Uniform optimized away

        if (typeof value === "number") {
            gl.uniform1f(loc, value);
        } else if (value.length === 2) {
            gl.uniform2fv(loc, value);
        } else if (value.length === 3) {
            gl.uniform3fv(loc, value);
        } else if (value.length === 4) {
            gl.uniform4fv(loc, value);
        }
    }
}
```

**Uniform Management Pattern** (typed wrapper for shader uniforms):

```typescript
// TypeScript: type-safe uniform manager
interface UniformDefs {
    [name: string]: "float" | "vec2" | "vec3" | "vec4" | "mat4" | "sampler2D";
}

class UniformManager<T extends UniformDefs> {
    private locations: Map<string, WebGLUniformLocation | null> = new Map();

    constructor(
        private gl: WebGL2RenderingContext,
        private program: WebGLProgram,
        defs: T,
    ) {
        for (const name of Object.keys(defs)) {
            this.locations.set(name, gl.getUniformLocation(program, name));
        }
    }

    set(name: keyof T, value: number | Float32Array): void {
        const loc = this.locations.get(name as string);
        if (loc === null || loc === undefined) return;

        if (typeof value === "number") {
            this.gl.uniform1f(loc, value);
        } else {
            switch (value.length) {
                case 2:  this.gl.uniform2fv(loc, value); break;
                case 3:  this.gl.uniform3fv(loc, value); break;
                case 4:  this.gl.uniform4fv(loc, value); break;
                case 16: this.gl.uniformMatrix4fv(loc, false, value); break;
            }
        }
    }
}
```

**Performance Profiling and Optimization**:

GPU shaders are limited by ALU (arithmetic), texture fetches, and bandwidth. Profile with browser DevTools (Chrome GPU profiling) or `EXT_disjoint_timer_query` for per-draw-call timing.

Common optimizations:

```glsl
// 1. Reduce ray march steps for distant objects (LOD)
float rayMarchLOD(vec3 ro, vec3 rd) {
    float t = 0.0;
    for (int i = 0; i < MAX_STEPS; i++) {
        vec3 p = ro + rd * t;
        float d = map(p);
        // Increase threshold with distance (distant detail is invisible)
        float threshold = SURF_DIST * (1.0 + t * 0.1);
        if (d < threshold) break;
        t += d;
        if (t > MAX_DIST) break;
    }
    return t;
}

// 2. Avoid expensive functions in inner loops
// BAD: calling pow() per step
for (int i = 0; i < 128; i++) {
    float d = pow(length(p), 2.0); // pow is expensive
}
// GOOD: use multiplication
for (int i = 0; i < 128; i++) {
    float l = length(p);
    float d = l * l; // Same result, cheaper
}

// 3. Use step/smoothstep instead of if/else (avoids branch divergence)
// BAD:
if (d < 0.5) { color = vec3(1.0, 0.0, 0.0); }
else { color = vec3(0.0, 0.0, 1.0); }
// GOOD:
color = mix(vec3(0.0, 0.0, 1.0), vec3(1.0, 0.0, 0.0), step(d, 0.5));

// 4. Precompute constants outside loops
float invRes = 1.0 / iResolution.y; // Compute once, not per pixel

// 5. Reduce texture samples: combine lookups, use mipmaps
// Use textureLod() with explicit LOD when you know the needed detail level

// 6. Use half-precision where full precision is unnecessary (mobile)
// mediump is 16-bit; sufficient for colors and UVs
mediump vec3 color = texture(uTex, uv).rgb;
```

**Mobile and WebGL Considerations**:

| Concern | Guideline |
|---------|-----------|
| Precision | Use `mediump` globally, `highp` only for positions and ray marching |
| Loop limits | Keep ray march steps under 64 on mobile; use early exit |
| Texture size | Power-of-two textures for WebGL 1 compatibility |
| Fragment cost | Target under 50 ALU operations per pixel for 60fps on mobile |
| Extensions | Check `gl.getExtension()` before using OES_texture_float, etc. |
| Overdraw | Minimize transparent layers; each adds a full-screen pass |
| Compile time | Large shaders may cause visible hitches on first use; warm up off-screen |

**Common Pitfalls**:

1. **Floating-point precision**: On mobile, `sin(largeNumber)` produces garbage. Reduce the input range: `sin(mod(iTime, 6.2831))`.
2. **Uninitialized varyings**: If the vertex shader does not write to a varying, the fragment shader reads undefined values. Always initialize all varyings.
3. **Integer division**: GLSL ES does not guarantee integer division behavior for negative values. Cast to float, divide, then floor.
4. **Texture coordinate clamping**: Use `clamp(uv, 0.0, 1.0)` or set the sampler wrap mode to avoid sampling outside [0,1].
5. **Depth buffer precision**: Z-fighting occurs when near/far planes are too far apart. Keep the near plane as large as practical.
6. **Shader compilation errors**: Compilation errors are only available via `gl.getShaderInfoLog()`. Always check after `compileShader()`.
7. **Missing precision qualifier**: WebGL fragment shaders require an explicit `precision` declaration. Omitting it is a compile error on mobile.
8. **Loop unrolling limits**: Some drivers refuse to compile loops with non-constant bounds. Use `#define MAX_STEPS 128` or `const int`.
