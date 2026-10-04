---
name: libgdx-box2dlights
description: Use when writing libGDX Java/Kotlin code involving 2D lighting with box2dlights — RayHandler, PointLight, ConeLight, DirectionalLight, ChainLight, ambient light, shadow rendering, soft shadows, light filtering, or attaching lights to Box2D bodies. Use when debugging lights not rendering, wrong light positions, lights not casting shadows, or performance issues with many lights.
---

# libGDX box2dlights

Quick reference for box2dlights — a 2D lighting library using Box2D raycasting for shadow generation. Covers RayHandler, light types, filtering, rendering order, and PPM integration. This is a **separate library**, not part of core libGDX.

**This is NOT the 3D Environment/lighting system.** box2dlights is exclusively for 2D shadow-casting lights using Box2D fixtures as occluders.

## Gradle Dependencies

```gradle
// Core module
implementation "com.badlogicgames.box2dlights:box2dlights:1.5"

// ALSO requires gdx-box2d — add explicitly (do not rely on transitive dep)
implementation "com.badlogicgames.gdx:gdx-box2d:$gdxVersion"
// Plus gdx-box2d-platform natives per target platform (see libgdx-box2d skill)

// GWT/HTML5 — add sources
implementation "com.badlogicgames.box2dlights:box2dlights:1.5:sources"
// GdxDefinition.gwt.xml:
//   <inherits name="Box2DLights" />
```

The published 1.5 POM references libGDX 1.6.2 but works with newer versions. Always add your own `gdx-box2d` dependency at the correct version.

## Class Hierarchy

```
Light (abstract) implements Disposable
  ├── PositionalLight (abstract)
  │     ├── PointLight
  │     └── ConeLight
  ├── DirectionalLight
  └── ChainLight
```

`PositionalLight` is an intermediate abstract class — many position/body methods live there.

## RayHandler

Central manager. Requires a Box2D `World` (used for shadow raycasting). Even if you don't want shadows, you must pass a World.

```java
// Construction — FBO defaults to Gdx.graphics.getWidth()/4 x getHeight()/4
RayHandler rayHandler = new RayHandler(world);
RayHandler rayHandler = new RayHandler(world, options);                      // RayHandlerOptions
RayHandler rayHandler = new RayHandler(world, fboWidth, fboHeight);
RayHandler rayHandler = new RayHandler(world, fboWidth, fboHeight, options); // RayHandlerOptions
```

**`RayHandlerOptions`** — pass to constructor for gamma correction, diffuse mode, pseudo-3D:
```java
RayHandlerOptions options = new RayHandlerOptions();
options.setGammaCorrection(true);
options.setDiffuse(true);
RayHandler rayHandler = new RayHandler(world, fboWidth, fboHeight, options);
```

DO NOT use `RayHandler.setGammaCorrection(boolean)` or `RayHandler.useDiffuseLight(boolean)` — both are **deprecated static methods with EMPTY BODIES** (they do nothing). Use `RayHandlerOptions` at construction, or instance methods `applyGammaCorrection(boolean)` / `setDiffuseLight(boolean)` after construction.

**Ambient light:**
```java
rayHandler.setAmbientLight(0.1f, 0.1f, 0.1f, 0.5f);  // r, g, b, a
rayHandler.setAmbientLight(new Color(0.1f, 0.1f, 0.1f, 0.5f));
rayHandler.setAmbientLight(0.3f);                       // sets ONLY alpha — NOT grayscale
```

**Rendering — AFTER SpriteBatch, NOT inside begin/end:**
```java
// In render():
batch.begin();
// ... draw sprites ...
batch.end();

rayHandler.setCombinedMatrix(camera);   // OrthographicCamera, NOT Camera
rayHandler.updateAndRender();           // NOT render()

// UI on top (optional)
uiBatch.begin();
// ...
uiBatch.end();
```

**`setCombinedMatrix` overloads:**

| Signature | Notes |
|---|---|
| `setCombinedMatrix(OrthographicCamera camera)` | Preferred. Takes `OrthographicCamera`, NOT `Camera` |
| `setCombinedMatrix(Matrix4 combined, float x, float y, float vpW, float vpH)` | For non-ortho cameras. x,y = camera position; vpW/vpH include zoom |
| ~~`setCombinedMatrix(Matrix4 combined)`~~ | **DEPRECATED** — inaccurate viewport calculation |

**Shadows, blur, culling:**
```java
rayHandler.setShadows(true);         // enable shadow casting (default: true)
rayHandler.setBlur(true);            // Gaussian blur on light map (default: true)
rayHandler.setBlurNum(1);            // blur passes, 1-3 safe (default: 1, 0 = no blur)
rayHandler.setCulling(true);         // skip offscreen lights (default: true)
```

**Other methods:**
```java
rayHandler.resizeFBO(newWidth, newHeight);   // resize internal FBOs
rayHandler.removeAll();                       // dispose and remove all lights
rayHandler.setWorld(newWorld);                // change Box2D world
rayHandler.setLightMapRendering(false);       // disable auto lightmap draw (for custom rendering)
rayHandler.getLightMapTexture();               // get lightmap as Texture for custom rendering
rayHandler.pointAtLight(worldX, worldY);      // is point inside any light?
rayHandler.pointAtShadow(worldX, worldY);     // is point in shadow?
rayHandler.dispose();                          // MUST call — disposes all lights, FBOs, shaders
```

**Gotchas:**
- `updateAndRender()` must be called OUTSIDE any `batch.begin()`/`batch.end()` block. RayHandler uses its own FBO and blend state internally.
- `setCombinedMatrix` takes `OrthographicCamera`, not the base `Camera` class. For a generic Camera, use the 5-arg Matrix4 overload.
- `setAmbientLight(float)` sets only the **alpha** channel, not a uniform grayscale. Use the 4-float or Color overload for full control.
- The FBO defaults to 1/4 screen resolution. Call `resizeFBO()` if you resize the window or need sharper lights.
- All light coordinates are in **Box2D meters**, not pixels. Use the same PPM convention as your Box2D world (see libgdx-box2d skill).

## Light Types

### PointLight

Omnidirectional light radiating from a point.

```java
PointLight light = new PointLight(rayHandler, rays, color, distance, x, y);
// rays: more = smoother shadows, more expensive. 8-32 mobile, 64-128 desktop.
// distance: in meters (Box2D world units)
// x, y: in meters

// Minimal constructor (defaults: Color(0.75, 0.75, 0.5, 0.75), distance=15, position=0,0)
PointLight light = new PointLight(rayHandler, rays);
```

`setDirection()` is a **deprecated no-op** on PointLight — it radiates in all directions.

### ConeLight

Directional spotlight with a cone angle.

```java
ConeLight light = new ConeLight(rayHandler, rays, color, distance, x, y,
                                directionDegrees, coneDegrees);
// directionDegrees: center direction of the cone
// coneDegrees: HALF-angle of the cone (total arc = coneDegrees * 2), clamped [0, 180]

light.setDirection(degrees);
light.setConeDegree(halfAngle);     // HALF-angle, NOT full cone width
light.getConeDegree();
```

**Gotcha:** `coneDegrees` is the **half-angle**. Setting `coneDegree=45` creates a 90-degree cone.

### DirectionalLight

Parallel rays covering the entire screen (like sunlight).

```java
DirectionalLight light = new DirectionalLight(rayHandler, rays, color, directionDegrees);
// No position or distance parameters — covers the whole viewport

light.setDirection(degrees);
light.setIgnoreBody(body);   // ignore a specific body's fixtures during raycasting (null to clear)
```

`setPosition()`, `setDistance()`, `attachToBody()` are all **deprecated no-ops** on DirectionalLight. `getX()`/`getY()` always return 0.

### ChainLight

Emits light along a chain of vertices (e.g., for lava flows, light strips).

```java
float[] vertices = {x1,y1, x2,y2, x3,y3, ...};  // pairs of (x,y) in meters
ChainLight light = new ChainLight(rayHandler, rays, color, distance, rayDirection, vertices);
// rayDirection: 1 = rays go left of chain, -1 = rays go right

// Modify chain at runtime:
light.chain.clear();
light.chain.addAll(newVertices);
light.updateChain();              // MUST call after modifying chain
```

`setDirection()` is a **deprecated no-op** on ChainLight.

## Light Base Class API

All light types inherit these methods from `Light`:

```java
// Position (PointLight, ConeLight, ChainLight only — no-op on DirectionalLight)
light.setPosition(x, y);              // meters
light.setPosition(new Vector2(x, y));
light.getX();
light.getY();

// Appearance
light.setColor(new Color(1, 0.8f, 0.6f, 1));
light.setColor(r, g, b, a);
light.setDistance(distMeters);         // light radius in meters

// Shadows
light.setSoft(true);                   // soft shadow edges
light.setSoftnessLength(2.5f);         // soft shadow penumbra length in world units
light.setXray(false);                  // true = light passes through all fixtures (no shadows)
light.setStaticLight(false);           // true = skip per-frame raycasting (~90% CPU savings)

// State
light.setActive(true);                 // toggle on/off
light.remove();                        // remove from RayHandler and dispose
light.remove(false);                   // remove without disposing (can re-add later)
light.dispose();

// Collision filtering — same system as Box2D fixtures
light.setContactFilter(categoryBits, groupIndex, maskBits);  // all short
light.setContactFilter(filter);                                // Filter object
Light.setGlobalContactFilter(categoryBits, groupIndex, maskBits); // static — default for new lights

// Pseudo-3D (experimental)
light.setHeight(heightDegrees);
```

**CRITICAL: The method is `setSoftnessLength()`, NOT `setSoftLength()`.** The getter is `getSoftShadowLength()`.

## Attaching Lights to Bodies

```java
// Basic — light follows body position and rotation
light.attachToBody(body);

// With offset (PositionalLight only — PointLight, ConeLight)
light.attachToBody(body, offsetX, offsetY);              // offset in world units
light.attachToBody(body, offsetX, offsetY, angleDegrees); // offset + direction offset

// Ignore the attached body's fixtures (light doesn't shadow its own body)
light.setIgnoreAttachedBody(true);
```

After `attachToBody()`, `setPosition()` is relative to the body. The body's rotation affects the offset position and the light direction.

**Gotcha:** `setIgnoreAttachedBody()` is a **deprecated no-op** on DirectionalLight (which cannot attach to bodies).

## Collision Filtering

Lights use the same Box2D `categoryBits`/`groupIndex`/`maskBits` system as fixtures. A light only casts shadows from fixtures whose filters allow collision with the light's filter. **Default: lights interact with all fixtures (no filtering).**

```java
// Light only blocked by walls (category 0x0008)
light.setContactFilter(
    (short) 0x0020,   // categoryBits — what the light "is"
    (short) 0,         // groupIndex
    (short) 0x0008     // maskBits — what fixtures block this light
);
```

Parameter order: `categoryBits`, `groupIndex`, `maskBits` (same order as the Box2D `Filter` fields, but note that `groupIndex` comes second here, not third).

Use `Light.setGlobalContactFilter(...)` to set the default filter applied to all newly created lights.

## Rendering Internals

RayHandler renders into an internal FBO (default: 1/4 screen resolution, RGBA8888). The process:

1. Bind FBO, clear to black
2. Render each light's mesh into FBO with additive blending (GL_SRC_ALPHA, GL_ONE)
3. Apply Gaussian blur passes if enabled
4. Blend FBO texture onto screen backbuffer

| Mode | Blend Func | Effect |
|---|---|---|
| Default (shadows=true) | GL_ONE, GL_ONE_MINUS_SRC_ALPHA | Lit areas show light color; shadowed areas show ambient |
| Diffuse | GL_DST_COLOR, GL_ZERO | Multiplicative — darkens scene, only lit areas retain color |
| No shadows | GL_SRC_ALPHA, GL_ONE | Pure additive — lights brighten scene, no darkening |

## Performance

| Lever | Effect | Notes |
|---|---|---|
| **Ray count** | Main CPU cost | 8–32 mobile, 64–128 desktop. Each ray = one Box2D raycast |
| **`setStaticLight(true)`** | ~90% CPU reduction | Skips per-frame raycasting. Recalculates only when properties change. Does NOT follow attached body |
| **`setXray(true)`** | ~70–80% CPU reduction | Skips raycasting entirely (no shadows) |
| **FBO size** | GPU fill rate | Default 1/4 screen. Smaller = faster but blurrier |
| **Blur passes** | GPU cost | 0 = off, 1–3 safe. Each pass = extra FBO blit |
| **`setCulling(true)`** | Skips offscreen lights | Enabled by default |
| **`setActive(false)`** | Disables light entirely | No raycasting, no rendering |

## Platform Differences

| Aspect | Desktop/Android/iOS | GWT/HTML5 |
|---|---|---|
| **Box2D backend** | JNI (native C++) | jBox2D (pure Java) — slower raycasting |
| **FBO support** | Full | WebGL 1.0+ required (all modern browsers) |
| **Performance** | Full speed | Noticeably slower with many lights due to jBox2D raycasts |
| **Shaders** | GLSL ES + GLSL 330 fallback | GLSL ES only (330 fallback not available) |
| **Setup** | `box2dlights` artifact | `box2dlights:sources` + `<inherits name="Box2DLights" />` |

## Common Mistakes

1. **Calling `updateAndRender()` inside `batch.begin()`/`end()`** — RayHandler binds its own FBO and changes blend state. Always call after `batch.end()`.
2. **Using `render()` instead of `updateAndRender()`** — `render()` exists but only draws the lightmap without updating light raycasts. Use `updateAndRender()` for the standard case.
3. **Using pixel coordinates for light positions** — box2dlights uses Box2D's meter-based coordinate system. A light at `(400, 300)` means 400 meters, not pixels.
4. **Forgetting `setCombinedMatrix()` before rendering** — Lights render at wrong positions or don't appear. Must call every frame before `updateAndRender()`.
5. **Passing `Camera` to `setCombinedMatrix()`** — The method requires `OrthographicCamera` specifically. For a generic Camera, use the 5-arg `(Matrix4, x, y, vpW, vpH)` overload.
6. **Using deprecated static `setGammaCorrection()`/`useDiffuseLight()`** — These are no-ops (empty bodies). Use `RayHandlerOptions` at construction or instance methods `applyGammaCorrection()`/`setDiffuseLight()`.
7. **Expecting `setAmbientLight(0.3f)` to set gray ambient** — The single-float overload sets only the alpha channel. Use `setAmbientLight(0.3f, 0.3f, 0.3f, 1f)` for gray ambient.
8. **Not disposing shapes/RayHandler** — `RayHandler.dispose()` disposes all lights, FBOs, and shaders. Omitting it leaks GPU resources.
9. **Using `setSoftLength()` instead of `setSoftnessLength()`** — The method is `setSoftnessLength(float)`. `setSoftLength` does not exist.
10. **Setting `coneDegree` to the full cone angle** — `ConeLight.setConeDegree()` takes the **half-angle**. A value of 45 creates a 90-degree cone.
11. **Expecting `setStaticLight(true)` lights to follow bodies** — Static lights skip `updateBody()`. They only recalculate when you explicitly change a property. Use for lights on static geometry only.
12. **Creating/destroying lights during `updateAndRender()`** — Like Box2D's contact callbacks, avoid modifying the light list while the handler is iterating. Create/remove lights outside the render call.
