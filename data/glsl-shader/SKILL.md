---
name: glsl-shader
description: Create audio-reactive GLSL visualizers for Bice-Box. Provides templates, audio uniforms (iRMSOutput, iRMSInput, iAudioTexture), coordinate patterns, and common shader functions.
---

# GLSL Shader Development

Create audio-reactive GLSL visualizers for Bice-Box.

## Essential Structure

- **GLSL ES 3.00** only
- **DO NOT DECLARE** `#version 300 es` or `precision` directives (system adds these automatically)
- **Main function**: `void mainImage(out vec4 fragColor, in vec2 fragCoord)`
- **File types**:
  - Single-pass: `name.glsl`
  - Multi-pass: `name_bufferA.glsl`, `name_image.glsl`

## Standard Uniforms (DO NOT redeclare)

```glsl
uniform vec3  iResolution;    // Screen resolution (width, height, aspect)
uniform float iTime;          // Shader time (seconds)
uniform vec4  iMouse;         // Mouse coordinates (xy = current, zw = click)
uniform sampler2D iChannel0;  // Buffer A output (in image pass)
uniform sampler2D iChannel1;  // Buffer B output (in image pass)
```

## Audio Uniforms

```glsl
uniform float iRMSInput;      // Real-time input audio (0.0-1.0+) - USE FOR REACTIVITY
uniform float iRMSOutput;     // Real-time output audio (0.0-1.0+) - USE FOR REACTIVITY
uniform float iRMSTime;       // Cumulative time - NOT for reactivity, grows with audio
uniform sampler2D iAudioTexture; // FFT/waveform data
```

### Audio Reactivity - Important Notes

**Use iRMSOutput/iRMSInput for real-time reactivity:**
```glsl
float intensity = 0.3 + 0.7 * iRMSOutput;  // Pulse with audio
float scale = 1.0 + iRMSOutput * 0.5;       // Scale with audio
```

**Do NOT use iRMSTime for reactivity** - it's cumulative time that grows infinitely with audio input.

## Audio Texture Sampling

The `iAudioTexture` provides two rows of data:

```glsl
// FFT (frequency spectrum) - Row 0
// u = 0.0 (bass) to 1.0 (treble), y = 0.25
float bass = texture(iAudioTexture, vec2(0.1, 0.25)).x;
float mid = texture(iAudioTexture, vec2(0.5, 0.25)).x;
float treble = texture(iAudioTexture, vec2(0.9, 0.25)).x;

// Waveform (time domain) - Row 1
// u = time position (0.0 to 1.0), y = 0.75
float waveVal = texture(iAudioTexture, vec2(0.5, 0.75)).x;
float waveValSigned = (waveVal * 2.0) - 1.0; // Convert 0-1 to -1,1

// Loop over frequencies
for(float i = 0.0; i < 1.0; i += 0.01) {
    float fftMag = texture(iAudioTexture, vec2(i, 0.25)).x;
    // Use fftMag for frequency-based visualization
}
```

## Common Coordinate Patterns

```glsl
// Normalized coordinates (0-1)
vec2 uv = fragCoord.xy / iResolution.xy;

// Centered coordinates (-0.5 to 0.5)
vec2 uv_centered = (fragCoord.xy - 0.5 * iResolution.xy) / iResolution.xy;

// Aspect-corrected coordinates (for perfect circles)
vec2 uv_centered = fragCoord.xy - 0.5 * iResolution.xy;
vec2 uv_aspect = uv_centered / iResolution.y;

// Polar coordinates
vec2 centered = fragCoord.xy - 0.5 * iResolution.xy;
float r = length(centered) / iResolution.y;
float theta = atan(centered.y, centered.x);
```

## Single-Pass Template

```glsl
// Optional resolution scaling (0.5 = half res for performance)
// resolution: 0.5

void mainImage(out vec4 fragColor, in vec2 fragCoord) {
    // Normalized coordinates
    vec2 uv = fragCoord.xy / iResolution.xy;

    // Audio reactivity
    float audioLevel = iRMSOutput;

    // Sample audio texture
    float bass = texture(iAudioTexture, vec2(0.1, 0.25)).x;

    // Your visualization here
    vec3 col = vec3(uv.x, uv.y, audioLevel);

    // Output
    fragColor = vec4(col, 1.0);
}
```

## Multi-Pass Template

**Buffer A** (`effect_name_bufferA.glsl`) - Feedback/persistence:
```glsl
void mainImage(out vec4 fragColor, in vec2 fragCoord) {
    vec2 uv = fragCoord.xy / iResolution.xy;

    // Read previous frame from iChannel0 (self-reference)
    vec4 prev = texture(iChannel0, uv);

    // Fade previous frame
    prev *= 0.95;

    // Add new content
    float audioLevel = iRMSOutput;
    vec3 newContent = vec3(0.0);

    // ... your drawing code ...

    // Combine
    vec3 col = prev.rgb + newContent;

    fragColor = vec4(col, 1.0);
}
```

**Image Pass** (`effect_name_image.glsl`) - Final output:
```glsl
void mainImage(out vec4 fragColor, in vec2 fragCoord) {
    vec2 uv = fragCoord.xy / iResolution.xy;

    // Read from Buffer A via iChannel0
    vec4 bufferA = texture(iChannel0, uv);

    // Apply post-processing
    vec3 col = bufferA.rgb;
    col = pow(col, vec3(1.0/2.2)); // Gamma correction

    fragColor = vec4(col, 1.0);
}
```

**JSON Configuration** (`effect_name.json`):
```json
{
    "shader": "shaders/effect_name"
}
```

## Multi-Pass Setup Notes

- **Buffer A** self-references via `iChannel0` (previous frame)
- **Image pass** reads buffers via `iChannel0` (Buffer A), `iChannel1` (Buffer B), etc.
- Use for: trails, feedback, persistence, fluid simulation
- JSON uses base name without `_bufferA` or `_image` suffix

## Audio-Reactive Patterns

### Pulsing/Scaling
```glsl
float pulse = 0.5 + 0.5 * iRMSOutput;
float scale = 1.0 + iRMSOutput * 0.3;
```

### Color Modulation
```glsl
vec3 col = vec3(0.5) + 0.5 * vec3(
    sin(iTime + iRMSOutput * 2.0),
    sin(iTime + iRMSOutput * 3.0 + 2.0),
    sin(iTime + iRMSOutput * 4.0 + 4.0)
);
```

### Frequency-Based Visualization
```glsl
// Spectrum analyzer style
for(float i = 0.0; i < 1.0; i += 0.02) {
    float fft = texture(iAudioTexture, vec2(i, 0.25)).x;
    if(abs(uv.x - i) < 0.01 && uv.y < fft) {
        col = vec3(1.0, 0.5, 0.0);
    }
}
```

### Waveform Visualization
```glsl
float wave = texture(iAudioTexture, vec2(uv.x, 0.75)).x;
wave = (wave * 2.0) - 1.0; // Convert to -1,1
float dist = abs(uv.y - 0.5 - wave * 0.3);
if(dist < 0.01) {
    col = vec3(0.0, 1.0, 0.5);
}
```

## MCP Workflow

**Workflow for creating/updating shaders:**

1. **Create shader file(s)** in `shaders/` directory
   - Single-pass: `shaders/my_shader.glsl`
   - Multi-pass: `shaders/my_shader_bufferA.glsl`, `shaders/my_shader_image.glsl`
   - Use Write tool to create files directly

2. **Activate visualizer**
   ```
   mcp__bice-box__set_visualizer(visualizerName: "my_shader")
   ```

3. **Link to audio effect** - Add shader comment in `.sc` file
   ```supercollider
   // shader: my_shader
   (
       var defName = \my_effect;
       // ... rest of effect code
   )
   ```
   This auto-loads the shader when the effect activates.

4. **List available visualizers**
   ```
   mcp__bice-box__list_visualizers()
   ```
   Returns p5.js sketches and GLSL shaders

5. **Iterate** - Edit and save, hot-reload handles the rest
   - Changes auto-reload when files are saved
   - No need to manually reload

## Common Shader Functions

```glsl
// Smooth minimum (blend shapes)
float smin(float a, float b, float k) {
    float h = clamp(0.5 + 0.5 * (b - a) / k, 0.0, 1.0);
    return mix(b, a, h) - k * h * (1.0 - h);
}

// Rotate 2D
vec2 rotate(vec2 v, float angle) {
    float c = cos(angle);
    float s = sin(angle);
    return vec2(v.x * c - v.y * s, v.x * s + v.y * c);
}

// Hash function (pseudo-random)
float hash(vec2 p) {
    return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453);
}

// Smooth step
float smoothstep(float edge0, float edge1, float x) {
    float t = clamp((x - edge0) / (edge1 - edge0), 0.0, 1.0);
    return t * t * (3.0 - 2.0 * t);
}
```

## Performance Tips

- **Use resolution scaling** for complex shaders:
  ```glsl
  // resolution: 0.5  // Half resolution
  ```

- **Minimize texture lookups** - Cache results when possible
  ```glsl
  vec4 prev = texture(iChannel0, uv);  // Once per fragment
  ```

- **Avoid loops when possible** - Unroll or use noise functions

- **Use built-in functions** - `smoothstep`, `mix`, `clamp` are optimized

- **Test on target hardware** - Raspberry Pi has different performance characteristics

## Common Gotchas

- **Don't declare `#version 300 es`** - System adds it automatically
- **Don't declare `precision`** - System handles this
- **iRMSTime is NOT for reactivity** - Use iRMSOutput/iRMSInput instead
- **Audio texture Y coordinates** - FFT at 0.25, waveform at 0.75 (not 0.0 and 1.0)
- **Multi-pass naming** - Must use `_bufferA`, `_image` suffixes exactly
- **Aspect ratio** - Divide by `iResolution.y` for circular shapes, not `iResolution.x`

## Debugging

- **Check shader compilation** - Look for errors in console logs
  ```
  mcp__bice-box__read_logs(lines: 100, filter: "shader")
  ```

- **Test with simple output** - Start with solid colors to verify structure
  ```glsl
  fragColor = vec4(1.0, 0.0, 0.0, 1.0);  // Red
  ```

- **Visualize UVs** - Debug coordinates
  ```glsl
  fragColor = vec4(uv, 0.0, 1.0);
  ```

- **Check audio uniforms** - Verify audio is flowing
  ```glsl
  fragColor = vec4(vec3(iRMSOutput), 1.0);  // Should pulse with audio
  ```
