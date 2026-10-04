---
name: libgdx-shaders
description: Use when writing libGDX Java/Kotlin code involving ShaderProgram, GLSL shaders, custom SpriteBatch shaders, Mesh rendering, or uniform/attribute setup. Use when debugging black screen, white screen, shader compilation errors, or "works on desktop but broken on phone" issues.
---

# libGDX ShaderProgram & GLSL

Quick reference for `ShaderProgram`, GLSL authoring, SpriteBatch/Mesh integration, and cross-platform shader compatibility. Covers GL ES 2.0 and GL ES 3.0 targeting.

## ShaderProgram Basics

```java
// Construction — from source strings or FileHandles
ShaderProgram shader = new ShaderProgram(vertexSrc, fragmentSrc);
ShaderProgram shader = new ShaderProgram(Gdx.files.internal("vert.glsl"),
                                         Gdx.files.internal("frag.glsl"));

// ALWAYS check compilation
if (!shader.isCompiled()) {
    Gdx.app.error("Shader", shader.getLog());
    // handle failure — do not proceed
}

// Bind before setting uniforms (standalone usage)
shader.bind();
shader.setUniformf("u_time", elapsed);

// Disposal
shader.dispose();
```

ShaderProgram is a **managed resource** — auto-recompiles on Android GL context loss. Source strings are retained internally.

**DO NOT use `begin()`/`end()`** — they are deprecated. `begin()` just calls `bind()`. `end()` is a no-op. Use `bind()` directly.

## Configuration (Static Fields)

```java
// Strict uniform checking (default: true)
// true  → IllegalArgumentException if uniform name not found in shader
// false → silently ignores missing uniforms (GL no-op on location -1)
ShaderProgram.pedantic = false;

// Prepended to ALL shader source before compilation (default: "")
// Affects every ShaderProgram created after being set, including internal ones
ShaderProgram.prependVertexCode = "#version 150\n";
ShaderProgram.prependFragmentCode = "#version 150\n";
```

`prependVertexCode`/`prependFragmentCode` are useful for injecting `#version` directives globally (e.g., fixing macOS GL 3.2 core profile). Caution: they affect libGDX's internal shaders (SpriteBatch, ShapeRenderer) too.

## Standard Attribute Names

| Constant | Value | Components |
|---|---|---|
| `ShaderProgram.POSITION_ATTRIBUTE` | `"a_position"` | 3 (xyz) |
| `ShaderProgram.COLOR_ATTRIBUTE` | `"a_color"` | 4 (rgba) |
| `ShaderProgram.TEXCOORD_ATTRIBUTE` | `"a_texCoord"` | 2 (uv) — unit appended: `a_texCoord0` |
| `ShaderProgram.NORMAL_ATTRIBUTE` | `"a_normal"` | 3 (xyz) |
| `ShaderProgram.TANGENT_ATTRIBUTE` | `"a_tangent"` | 3 |
| `ShaderProgram.BINORMAL_ATTRIBUTE` | `"a_binormal"` | 3 |
| `ShaderProgram.BONEWEIGHT_ATTRIBUTE` | `"a_boneWeight"` | 2 — unit appended: `a_boneWeight0` |

Note: `TEXCOORD_ATTRIBUTE` is `"a_texCoord"` (no trailing digit). The unit number is appended: `VertexAttribute.TexCoords(0)` produces alias `"a_texCoord0"`.

## Uniforms API

All `setUniform*` methods accept `String name` or `int location`. Locations are cached internally — `glGetUniformLocation` called only once per name.

```java
shader.setUniformf("u_time", 1.5f);                           // float
shader.setUniformf("u_resolution", width, height);             // vec2 (also 3/4 float overloads)
shader.setUniformf("u_tint", myColor);                        // Color → vec4
shader.setUniformf("u_offset", myVector2);                     // Vector2 → vec2
shader.setUniformi("u_texture", 0);                            // sampler2D unit
shader.setUniformMatrix("u_projTrans", matrix4);               // mat4 (also mat3 overload)
shader.setUniform1fv("u_kernel", values, 0, values.length);   // float[] (also 2fv/3fv/4fv)

// Hot path: cache location
int loc = shader.getUniformLocation("u_time");                 // -1 if not found
shader.setUniformf(loc, elapsed);
```

**There is no `setUniform()` method.** Always `setUniformf`, `setUniformi`, or `setUniformMatrix`.

Introspection: `hasUniform(name)`, `hasAttribute(name)`, `getUniforms()`, `getAttributes()`.

## SpriteBatch Integration

```java
SpriteBatch batch = new SpriteBatch();
ShaderProgram myShader = new ShaderProgram(vertSrc, fragSrc);

batch.begin();
batch.setShader(myShader);
// SpriteBatch calls myShader.bind() and sets u_projTrans + u_texture automatically.
// Set your custom uniforms AFTER setShader() or after begin():
myShader.setUniformf("u_time", elapsed);
batch.draw(texture, x, y);
batch.setShader(null);  // reverts to default shader (flushes pending draws first)
batch.end();
```

### Uniforms SpriteBatch Sets Automatically

| Uniform | Type | Value |
|---|---|---|
| `u_projTrans` | `mat4` | `projectionMatrix * transformMatrix` |
| `u_texture` | `sampler2D` | Texture unit `0` |

Your custom shader **must** declare these exact names. SpriteBatch calls `bind()` in `begin()` and in `setShader()` — you do NOT call `bind()` yourself.

### SpriteBatch Default Vertex Attributes

| Attribute | Type | Name |
|---|---|---|
| Position | `vec4` | `a_position` |
| Color | `vec4` | `a_color` |
| TexCoords | `vec2` | `a_texCoord0` |

### SpriteBatch Default Shader Summary

The default vertex shader passes `a_position` through `u_projTrans`, forwards `a_color` and `a_texCoord0` as varyings (`v_color`, `v_texCoords`). It applies alpha correction: `v_color.a * (255.0/254.0)` to compensate for packed float color encoding.

The default fragment shader outputs `v_color * texture2D(u_texture, v_texCoords)` with the standard `#ifdef GL_ES` precision block.

When writing replacement shaders, match these attribute names and uniform names exactly.

### Multi-Texture with SpriteBatch

```java
batch.begin();
batch.setShader(myShader);

normalMap.bind(1);                                // bind normal map to unit 1
myShader.setUniformi("u_normalMap", 1);           // tell shader
Gdx.gl.glActiveTexture(GL20.GL_TEXTURE0);        // MUST reset to unit 0!
// SpriteBatch.flush() calls texture.bind() (no arg) — binds to currently active unit.
// If you don't reset to unit 0, the diffuse texture goes to the wrong unit.

batch.draw(diffuseTexture, x, y);
batch.end();
```

## ShapeRenderer Note

ShapeRenderer's shader is set **only at construction**: `new ShapeRenderer(5000, myShader)`. There is **no** `setShader()`. Default uses `a_position` and `a_color` only (no texcoords).

## GLSL Version Differences

| Feature | GL ES 2.0 / GLSL 100 | GL ES 3.0 / GLSL 300 es | Desktop GLSL 120 | Desktop GLSL 150+ |
|---|---|---|---|---|
| Version directive | None (optional) | `#version 300 es` (required, first line) | `#version 120` | `#version 150` |
| Vertex input | `attribute` | `in` | `attribute` | `in` |
| Vertex→Fragment | `varying` | `out` (vert) / `in` (frag) | `varying` | `out` / `in` |
| Fragment output | `gl_FragColor` | Declare `out vec4 fragColor;` | `gl_FragColor` | Declare `out vec4 fragColor;` |
| Texture sampling | `texture2D()` | `texture()` | `texture2D()` | `texture()` |
| Layout qualifiers | No | Yes | No | Yes (GLSL 330+) |
| `precision` required | Yes (fragment float) | Yes (fragment float) | **No — syntax error in 110/120** | Accepted but no effect (130+) |
| `GL_ES` defined | Yes | Yes | No | No |

### Critical Rules

- `#version 300 es` must be the **very first line** — before any comments or directives.
- `gl_FragColor` **does not exist** in GLSL 300 es. You must declare `out vec4 fragColor;` (any name except `gl_`-prefixed).
- `texture2D()` **does not exist** in GLSL 300 es. Use `texture()`.
- `attribute`/`varying` **do not exist** in GLSL 300 es. Use `in`/`out`.
- Desktop GLSL 110/120 **rejects** `precision mediump float;` as a syntax error.

## Cross-Platform Precision Pattern

Use in **every fragment shader** for GL ES 2.0 compatibility:

```glsl
#ifdef GL_ES
#define LOWP lowp
precision mediump float;
#else
#define LOWP
#endif
```

`GL_ES` is defined by the GLSL compiler on ES platforms (not injected by libGDX). For GL ES 3.0, `precision mediump float;` is still required after `#version 300 es`.

## Mesh + ShaderProgram

Direct rendering without SpriteBatch. You manage vertex data and shader binding.

### VertexAttribute Setup

```java
// Static factory methods (preferred) — aliases must match vertex shader names
VertexAttribute.Position()           // 3 floats, alias "a_position"
VertexAttribute.ColorPacked()        // 4 bytes as 1 float, alias "a_color", normalized
VertexAttribute.ColorUnpacked()      // 4 floats, alias "a_color"
VertexAttribute.TexCoords(0)         // 2 floats, alias "a_texCoord0"
VertexAttribute.Normal()             // 3 floats, alias "a_normal"
// Manual: new VertexAttribute(Usage.Position, 3, "a_position")
```

### Render Pattern

```java
// Setup: new Mesh(isStatic, maxVertices, maxIndices, ...VertexAttributes)
mesh = new Mesh(true, 4, 6,
    VertexAttribute.Position(), VertexAttribute.ColorUnpacked(), VertexAttribute.TexCoords(0));
mesh.setVertices(floatArray);       // interleaved: x,y,z, r,g,b,a, u,v per vertex
mesh.setIndices(new short[] { 0, 1, 2, 2, 3, 0 });

// Render loop
texture.bind();
shader.bind();
shader.setUniformMatrix("u_projTrans", camera.combined);
shader.setUniformi("u_texture", 0);
mesh.render(shader, GL20.GL_TRIANGLES);   // also accepts offset, count, autoBind params
```

Mesh `render()` auto-binds vertex attributes (`autoBind` defaults to `true`). Mesh is a **managed resource** — re-uploads after GL context loss.

## ModelBatch Integration (Brief)

ModelBatch uses `ShaderProvider` (not `setShader()`). Custom shaders: `new ModelBatch(new DefaultShaderProvider(vertSrc, fragSrc))`.

## Common Mistakes

1. **Skipping `isCompiled()` check** — Shader silently fails. Everything renders white or black with no error. Always check and log `getLog()`.
2. **Missing `precision mediump float;` in fragment shader** — Compiles on desktop, black screen on Android/iOS. Use the `#ifdef GL_ES` pattern.
3. **Wrong SpriteBatch uniform names** — The uniform is `u_projTrans`, NOT `u_projectionViewMatrix`. The texture sampler is `u_texture`, NOT `u_tex0` or `u_sampler`. Exact names required.
4. **Forgetting `shader.bind()` before `setUniform*`** — Required for standalone Mesh rendering. NOT needed with SpriteBatch (it calls `bind()` in `begin()`/`setShader()`).
5. **Using `varying`/`attribute` in GLSL 300 es** — Must use `in`/`out`. Using old keywords is a compilation error.
6. **Using `gl_FragColor` in GLSL 300 es** — Does not exist. Declare `out vec4 fragColor;` and write to that.
7. **Using `texture2D()` in GLSL 300 es** — Does not exist. Use `texture()`.
8. **Not resetting active texture unit after multi-texture binding** — After `normalMap.bind(1)`, call `Gdx.gl.glActiveTexture(GL20.GL_TEXTURE0)` before SpriteBatch draws. Otherwise SpriteBatch binds the diffuse texture to the wrong unit.
9. **Calling `setShader()` outside `begin()`/`end()` and expecting uniforms to work** — `setShader()` only binds and sets auto-uniforms when called between `begin()`/`end()`. Outside that block, you must call `bind()` manually before setting uniforms.
10. **Vertex attribute name mismatch** — VertexAttribute alias (e.g., `"a_texCoord0"`) must match the vertex shader's `attribute`/`in` variable name exactly. Typo = attribute silently not bound.
11. **Using `begin()`/`end()` instead of `bind()`** — `begin()`/`end()` are deprecated. `begin()` just calls `bind()`. `end()` does nothing. Use `bind()` directly.
12. **Not disposing ShaderProgram** — Leaks native GL resources. Always `dispose()` in your `dispose()` method.
