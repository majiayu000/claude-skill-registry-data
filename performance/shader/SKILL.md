---
name: shader
description: Write Godot Shading Language shaders — use when creating spatial, canvas_item, or particle shaders.
type: implementation
---

# Godot Shader

> Expert Godot Shading Language engineer specializing in spatial, canvas_item, and particle shaders with deep knowledge of GLSL patterns and GPU performance.

## Overview

Godot uses a GLSL-based shading language with built-in variables for each shader type. Shaders are written in `.gdshader` files or inline in ShaderMaterial resources. The language is close to GLSL ES 3.0 with Godot-specific built-ins for geometry, lighting, and screen-space access. Uniform hints control inspector presentation and texture interpretation.

## Shader Types

| Type | Use Case | Key Built-ins |
|------|----------|---------------|
| `shader_type spatial;` | 3D objects, PBR surfaces, world effects | `VERTEX`, `NORMAL`, `ALBEDO`, `ROUGHNESS`, `METALLIC`, `EMISSION`, `NORMAL_MAP`, `VIEW`, `FRAGCOORD` |
| `shader_type canvas_item;` | 2D sprites, UI elements, post-process | `VERTEX`, `UV`, `COLOR`, `TEXTURE`, `SCREEN_TEXTURE`, `FRAGCOORD`, `TIME` |
| `shader_type particles;` | GPU particle simulation | `TRANSFORM`, `VELOCITY`, `COLOR`, `CUSTOM`, `ACTIVE`, `DELTA`, `LIFETIME`, `INDEX` |

## Core Patterns

### 1. Wave Vertex Deformation (Spatial)

Displaces vertices in the vertex shader for animated geometry like water or flags.

```glsl
shader_type spatial;

uniform float wave_amplitude : hint_range(0.0, 1.0) = 0.1;
uniform float wave_frequency : hint_range(0.1, 10.0) = 2.0;
uniform float wave_speed : hint_range(0.0, 5.0) = 1.0;
uniform vec4 albedo : source_color = vec4(0.1, 0.4, 0.8, 1.0);
uniform sampler2D normal_tex : hint_normal;

void vertex() {
    VERTEX.y += sin(VERTEX.x * wave_frequency + TIME * wave_speed) * wave_amplitude;
    VERTEX.y += cos(VERTEX.z * wave_frequency * 0.7 + TIME * wave_speed * 1.3) * wave_amplitude * 0.5;
}

void fragment() {
    ALBEDO = albedo.rgb;
    NORMAL_MAP = texture(normal_tex, UV).rgb;
    ROUGHNESS = 0.1;
    METALLIC = 0.0;
}
```

### 2. Billboard Sprite (Spatial)

Forces a mesh to always face the camera, useful for imposters or particle sprites.

```glsl
shader_type spatial;
render_mode unshaded, cull_disabled;

uniform sampler2D sprite_tex : hint_default_white;
uniform vec4 modulate : source_color = vec4(1.0);

void vertex() {
    // Extract billboard matrix: use camera axes, keep world position
    vec3 world_pos = (MODEL_MATRIX * vec4(0.0, 0.0, 0.0, 1.0)).xyz;
    vec3 cam_right = normalize(vec3(INV_VIEW_MATRIX[0][0], INV_VIEW_MATRIX[1][0], INV_VIEW_MATRIX[2][0]));
    vec3 cam_up    = normalize(vec3(INV_VIEW_MATRIX[0][1], INV_VIEW_MATRIX[1][1], INV_VIEW_MATRIX[2][1]));
    vec3 offset = cam_right * VERTEX.x + cam_up * VERTEX.y;
    POSITION = VIEW_MATRIX * vec4(world_pos + offset, 1.0);
    POSITION = PROJECTION_MATRIX * POSITION;
}

void fragment() {
    vec4 col = texture(sprite_tex, UV) * modulate;
    if (col.a < 0.01) discard;
    ALBEDO = col.rgb;
    ALPHA = col.a;
}
```

### 3. Rim Lighting / Fresnel Emission (Spatial)

Adds an emissive glow on silhouette edges, common for force-fields and sci-fi materials.

```glsl
shader_type spatial;

uniform vec4 albedo : source_color = vec4(0.05, 0.05, 0.1, 1.0);
uniform vec4 rim_color : source_color = vec4(0.2, 0.6, 1.0, 1.0);
uniform float rim_power : hint_range(0.5, 8.0) = 3.0;
uniform float rim_strength : hint_range(0.0, 4.0) = 2.0;

void fragment() {
    float rim = 1.0 - dot(NORMAL, VIEW);
    ALBEDO = albedo.rgb;
    EMISSION = rim_color.rgb * pow(rim, rim_power) * rim_strength;
    ROUGHNESS = 0.8;
    METALLIC = 0.0;
}
```

### 4. Dissolve / Cutout with Noise (Spatial)

Clips pixels below a threshold sampled from a noise texture for burn/dissolve effects.

```glsl
shader_type spatial;
render_mode cull_disabled;

uniform sampler2D albedo_tex : hint_default_white;
uniform sampler2D noise_tex : hint_default_white;
uniform float threshold : hint_range(0.0, 1.0) = 0.5;
uniform vec4 edge_color : source_color = vec4(1.0, 0.4, 0.0, 1.0);
uniform float edge_width : hint_range(0.0, 0.2) = 0.05;

void fragment() {
    float noise = texture(noise_tex, UV).r;
    if (noise < threshold) discard;
    vec4 col = texture(albedo_tex, UV);
    float edge = smoothstep(threshold, threshold + edge_width, noise);
    ALBEDO = mix(edge_color.rgb, col.rgb, edge);
    EMISSION = edge_color.rgb * (1.0 - edge) * 2.0;
    ROUGHNESS = 0.8;
}
```

### 5. Outline via Inverted Hull (Spatial — separate pass)

Renders a back-face-only scaled mesh to produce a world-space outline. Apply to a duplicate mesh or use a second material pass.

```glsl
shader_type spatial;
render_mode cull_front, unshaded;

uniform float outline_width : hint_range(0.0, 0.1) = 0.02;
uniform vec4 outline_color : source_color = vec4(0.0, 0.0, 0.0, 1.0);

void vertex() {
    // Expand along normal in view space to avoid perspective distortion
    vec3 normal_view = normalize((MODELVIEW_MATRIX * vec4(NORMAL, 0.0)).xyz);
    POSITION = PROJECTION_MATRIX * (MODELVIEW_MATRIX * vec4(VERTEX, 1.0) + vec4(normal_view * outline_width, 0.0));
}

void fragment() {
    ALBEDO = outline_color.rgb;
}
```

### 6. Screen-Space Refraction / Distortion (Spatial)

Reads `SCREEN_TEXTURE` with a UV offset for glass, heat-haze, or water refraction. In Godot 4 the screen UV origin is top-left; flip Y when needed.

```glsl
shader_type spatial;
render_mode unshaded, blend_mix;

uniform sampler2D normal_tex : hint_normal;
uniform float refraction_strength : hint_range(0.0, 0.1) = 0.02;
uniform float scroll_speed : hint_range(0.0, 2.0) = 0.3;

void fragment() {
    vec2 anim_uv = UV + vec2(TIME * scroll_speed * 0.1, TIME * scroll_speed * 0.07);
    vec3 n = texture(normal_tex, anim_uv).rgb * 2.0 - 1.0;

    // SCREEN_UV goes 0..1 top-left to bottom-right.
    // Offset by the XY of the decoded normal for distortion.
    vec2 screen_uv = SCREEN_UV + n.xy * refraction_strength;
    // Clamp to avoid sampling outside the screen.
    screen_uv = clamp(screen_uv, vec2(0.001), vec2(0.999));

    ALBEDO = texture(SCREEN_TEXTURE, screen_uv).rgb;
}
```

### 7. Depth-Based Foam / Intersection (Spatial)

Uses `DEPTH_TEXTURE` to detect where a surface intersects geometry for shoreline foam.

```glsl
shader_type spatial;
render_mode unshaded, blend_mix;

uniform vec4 water_color : source_color = vec4(0.1, 0.5, 0.7, 0.8);
uniform vec4 foam_color : source_color = vec4(1.0);
uniform float foam_distance : hint_range(0.01, 2.0) = 0.3;
uniform sampler2D depth_texture : hint_depth_texture, filter_linear_mipmap;

void fragment() {
    float raw_depth = texture(depth_texture, SCREEN_UV).r;
    // Reconstruct scene depth in view space
    vec4 ndc = vec4(SCREEN_UV * 2.0 - 1.0, raw_depth, 1.0);
    vec4 view_pos = INV_PROJECTION_MATRIX * ndc;
    view_pos /= view_pos.w;
    float scene_depth = -view_pos.z;
    float frag_depth  = -VERTEX.z;
    float depth_diff  = scene_depth - frag_depth;
    float foam_factor = 1.0 - smoothstep(0.0, foam_distance, depth_diff);
    ALBEDO = mix(water_color.rgb, foam_color.rgb, foam_factor);
    ALPHA  = water_color.a;
}
```

### 8. Particle Color Over Lifetime (Particles)

Interpolates between two colors using `CUSTOM.y`, which Godot writes as normalized lifetime (0..1).

```glsl
shader_type particles;

uniform vec4 color_start : source_color = vec4(1.0, 0.5, 0.0, 1.0);
uniform vec4 color_end : source_color = vec4(1.0, 0.0, 0.0, 0.0);
uniform float gravity : hint_range(-20.0, 0.0) = -9.8;
uniform float spread : hint_range(0.0, 5.0) = 1.0;

void start() {
    // CUSTOM.y is set to 0.0 at birth and 1.0 at death by Godot
    VELOCITY = vec3(
        (RANDOM_SEED.x * 2.0 - 1.0) * spread,
        (RANDOM_SEED.y + 0.5) * 3.0,
        (RANDOM_SEED.z * 2.0 - 1.0) * spread
    );
    COLOR = color_start;
}

void process() {
    VELOCITY.y += gravity * DELTA;
    TRANSFORM.origin += VELOCITY * DELTA;
    // CUSTOM.y holds normalized lifetime fraction
    COLOR = mix(color_start, color_end, CUSTOM.y);
}
```

### 9. Canvas Item Scroll with `#include`

Shared utilities can live in a `.gdshaderinc` file and be `#include`-d.

`res://shaders/utils.gdshaderinc`:
```glsl
// Shared utility: luminance
float luminance(vec3 c) {
    return dot(c, vec3(0.2126, 0.7152, 0.0722));
}
```

`res://shaders/scroll.gdshader`:
```glsl
shader_type canvas_item;
#include "res://shaders/utils.gdshaderinc"

uniform float scroll_speed : hint_range(0.0, 10.0) = 1.0;
uniform float desaturate : hint_range(0.0, 1.0) = 0.0;

void fragment() {
    vec2 uv = UV;
    uv.x = mod(uv.x + TIME * scroll_speed * 0.05, 1.0);
    vec4 col = texture(TEXTURE, uv) * COLOR;
    float lum = luminance(col.rgb);
    col.rgb = mix(col.rgb, vec3(lum), desaturate);
    COLOR = col;
}
```

## Common Pitfalls

- **Gamma / linear space mismatch.** Godot renders in linear light. Without `source_color` on color uniforms, colors entered in the inspector are treated as linear even though the picker shows sRGB — this makes them appear too dark at runtime. Always annotate: `uniform vec4 tint : source_color`.
- **`SCREEN_TEXTURE` requires `hint_screen_texture`, and coordinates are top-left origin.** Sampling without the hint causes a blank texture. Y is NOT flipped in Godot 4 compared to some older Godot 3 expectations — verify by testing, not assuming.
- **`discard` in a shadow-casting shader breaks shadows.** If using `discard` for cutout opacity, add `render_mode shadows_disabled;` or use a separate unshaded pass; otherwise the object casts a full solid shadow regardless of the discard condition.
- **Writing to `VERTEX` in `fragment()` has no effect.** Vertex position must be set in `vertex()`. A common mistake is computing a displaced position in `fragment()` and assigning it to `VERTEX` — nothing happens.
- **Particle `CUSTOM.y` is only available when the GPUParticles3D node has "Amount Ratio" > 0 and the process material uses it.** If `CUSTOM.y` always reads 0, check that the Godot-side process material emits lifetime data into the `CUSTOM` channel.
- **Normal maps need `hint_normal`, not `hint_default_white`.** Using the wrong hint causes Godot to skip the sRGB-to-linear conversion expected for normal maps, producing incorrect lighting. Always: `uniform sampler2D normal_tex : hint_normal;`.
- **`POSITION` overrides the full clip-space transform; `VERTEX` only affects the pre-projection position.** When writing billboard or custom projection shaders, assign to `POSITION` (vec4, clip space) — not `VERTEX` — to bypass the model-view-projection pipeline entirely.

## Performance

**Precision hints** — Use `lowp` or `mediump` qualifiers on non-critical intermediates in mobile targets. For desktop targets Godot promotes most precision automatically, but being explicit avoids issues on mobile GPUs.

```glsl
// Prefer this on mobile:
lowp vec4 col = texture(TEXTURE, UV);
mediump float rim = 1.0 - dot(NORMAL, VIEW);
```

**Texture lookups** — Each `texture()` call is a potential cache miss. Batch UV-derived lookups together rather than interleaving with arithmetic. Avoid sampling in loops unless count is known-small and compile-time constant.

**Overdraw** — Canvas item and transparent spatial shaders contribute to overdraw. For large transparent surfaces (water, fog volumes):
- Use `render_mode depth_prepass_alpha;` on spatial shaders where possible so opaque pixels early-out.
- Use `render_mode blend_premul_alpha;` instead of `blend_mix` when the source texture is premultiplied — avoids a multiply.
- Cull back-faces unless double-sided is truly required: `render_mode cull_back;` is the default; do not disable it without reason.

**Branch divergence** — `if` statements inside shaders cause all GPU threads in a warp to execute both paths. Replace sharp conditionals with `mix()` and `step()` where possible.

```glsl
// Slow (branch divergence):
if (noise < threshold) ALBEDO = color_a;
else ALBEDO = color_b;

// Fast (branchless):
ALBEDO = mix(color_b, color_a, step(noise, threshold));
```

**Avoid `discard` in the general case** — `discard` prevents the GPU's early-Z optimization. If the effect only needs transparency, use `ALPHA` instead where the blend mode permits.

## Anti-Patterns

**Wrong — color uniform without `source_color` (gamma bug):**
```glsl
uniform vec4 tint = vec4(1.0, 0.5, 0.0, 1.0); // Inspector shows sRGB, runtime gets raw linear values
```
**Right:**
```glsl
uniform vec4 tint : source_color = vec4(1.0, 0.5, 0.0, 1.0);
```

---

**Wrong — sampling `SCREEN_TEXTURE` without the required hint:**
```glsl
uniform sampler2D screen_tex; // Blank at runtime
void fragment() { ALBEDO = texture(screen_tex, SCREEN_UV).rgb; }
```
**Right:**
```glsl
uniform sampler2D screen_tex : hint_screen_texture, filter_linear_mipmap;
void fragment() { ALBEDO = texture(screen_tex, SCREEN_UV).rgb; }
```

---

**Wrong — modifying `VERTEX` in `fragment()` (no effect):**
```glsl
void fragment() {
    VERTEX.y += sin(TIME); // silently ignored
}
```
**Right:**
```glsl
void vertex() {
    VERTEX.y += sin(TIME);
}
```

---

**Wrong — using `hint_default_white` on a normal map texture:**
```glsl
uniform sampler2D bump : hint_default_white; // Incorrect color space handling
```
**Right:**
```glsl
uniform sampler2D bump : hint_normal; // Correct: Godot converts from sRGB and sets default flat normal
```

---

**Wrong — per-fragment `for` loop over a large dynamic count:**
```glsl
uniform int light_count; // dynamic, could be 100
void fragment() {
    for (int i = 0; i < light_count; i++) { /* ... */ } // GPU hangs / extreme slowdown
}
```
**Right:** Use a fixed compile-time loop bound or restructure to a texture-based lookup. Dynamic loop lengths are expensive on GPU.

## References

- Shading language reference: https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/shading_language.html
- Spatial shader built-ins: https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/spatial_shader.html
- Canvas item shader built-ins: https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/canvas_item_shader.html
- Particle shader built-ins: https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/particle_shader.html
- Screen-reading shaders (SCREEN_TEXTURE, DEPTH_TEXTURE): https://docs.godotengine.org/en/stable/tutorials/shaders/screen-reading_shaders.html
- Your first shader tutorial: https://docs.godotengine.org/en/stable/tutorials/shaders/your_first_shader/index.html
- Converting GLSL to Godot shaders: https://docs.godotengine.org/en/stable/tutorials/shaders/converting_glsl_to_godot_shaders.html
- Shader include files: https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/shader_preprocessor.html

## Delegate to

- `godot:docs` (Context7) — look up specific built-in variable names, render modes, or uniform hints before writing unfamiliar shader code.
