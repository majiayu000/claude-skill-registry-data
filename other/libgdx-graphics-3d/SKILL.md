---
name: libgdx-3d-rendering
description: Use when writing libGDX Java/Kotlin code involving 3D rendering — ModelBatch, ModelInstance, Model loading (G3DJ/G3DB/OBJ), ModelBuilder procedural meshes, Environment and lighting (DirectionalLight/PointLight), PerspectiveCamera, Materials and Attributes (ColorAttribute/TextureAttribute/BlendingAttribute), AnimationController, or camera controllers (CameraInputController/FirstPersonCameraController). Use when debugging black 3D models, missing lighting, wrong camera setup, animation not playing, or model disposal issues.
---

# libGDX 3D Rendering

Quick reference for the libGDX 3D pipeline (`com.badlogic.gdx.graphics.g3d.*`). Covers ModelBatch, Model/ModelInstance, model loading, ModelBuilder, Environment, lights, materials, attributes, PerspectiveCamera, AnimationController, and camera controllers.

## What Stock libGDX 3D Does NOT Have

- **No PBR / glTF** — requires third-party `gdx-gltf` library
- **No shadow mapping** — must implement manually or use third-party
- **No deferred rendering pipeline**
- **No scene graph** — ModelInstance + manual Matrix4 transforms is the full system
- **No spot light support in default shader** — `DefaultShader.Config.numSpotLights` defaults to 0

DO NOT hallucinate PBR classes, shadow renderers, scene graphs, or built-in spot light shading.

## ModelBatch

NOT like SpriteBatch. No `setProjectionMatrix()` — camera is passed to `begin()`.

```java
ModelBatch modelBatch = new ModelBatch();  // uses DefaultShaderProvider, DefaultRenderableSorter

// In render():
modelBatch.begin(camera);
modelBatch.render(instance, environment);   // RenderableProvider, not ModelInstance specifically
modelBatch.render(instances, environment);  // Iterable<? extends RenderableProvider>
modelBatch.end();                           // flushes, sorts, renders

// In dispose():
modelBatch.dispose();  // disposes ShaderProvider (cached shaders) only
```

Environment passed to `render()` overrides whatever the RenderableProvider set. `flush()` can be called between `begin()`/`end()` to force intermediate draws. `setCamera(Camera)` switches cameras mid-batch (flushes first). DefaultRenderableSorter sorts opaque front-to-back, transparent back-to-front.

**Gotchas:**
- `dispose()` only disposes the ShaderProvider's cached shaders — NOT the RenderContext, even if ModelBatch created it.
- Do NOT modify GL state between `begin()` and `end()` — RenderContext manages it.
- `ModelBatch.setProjectionMatrix()` does NOT exist. The projection comes from the Camera passed to `begin()`.

## Model

`Model` implements `Disposable`. Fields: `materials`, `nodes`, `animations`, `meshes`, `meshParts` (all `Array`). Key methods: `getAnimation("id")`, `getMaterial("id")`, `getNode("id")` (all ignoreCase=true), `calculateTransforms()`, `dispose()`.

**Ownership:** When loaded directly (not via AssetManager), Model owns all Meshes and Textures. `dispose()` destroys them. Multiple ModelInstances share the same Model — Model must outlive all its instances.

## ModelInstance

Implements `RenderableProvider`, NOT `Disposable`. The source Model owns GPU resources. Fields: `model`, `transform` (Matrix4, public non-final), `materials` (per-instance copies), `nodes`, `animations`, `userData` (Object).

**Key constructors:** `new ModelInstance(model)`, `(model, "nodeId1", "nodeId2")` (selected root nodes), `(model, x, y, z)` (with translation), `(copyFrom)` (copies nodes/materials/animations).

**Transform:** `instance.transform` is a standard Matrix4 — use `setToTranslation()`, `rotate()`, `scale()`, `setToTranslationAndScaling()`.

**Per-instance materials** — constructor deep-copies materials:
```java
instance.getMaterial("mat_id").set(ColorAttribute.createDiffuse(Color.RED));
// Only affects this instance, not the Model or other instances.
```

**calculateTransforms():** Must be called manually if you modify Node `translation`/`rotation`/`scale` directly after construction. NOT needed if you only modify `instance.transform`.

## Model Loading

**G3dModelLoader** — same class, different reader: `new G3dModelLoader(new JsonReader())` for `.g3dj`, `new G3dModelLoader(new UBJsonReader())` for `.g3db`. **ObjLoader** — for testing only, Javadoc warns "should not be used in production."

**AssetManager (preferred)** — `.g3dj`, `.g3db`, `.obj` loaders pre-registered:
```java
assetManager.load("scene.g3db", Model.class);
assetManager.finishLoading();
Model model = assetManager.get("scene.g3db", Model.class);
```

**Texture ownership with AssetManager:** AssetManager removes Textures from Model's managed disposables (manages them separately). When `assetManager.unload("scene.g3db")` is called, it disposes the Model (meshes) and tracks texture references independently. Default texture parameters: `Linear` filter, `Repeat` wrap.

## ModelBuilder

Instance methods (not static). Every returned Model must be disposed.

```java
ModelBuilder mb = new ModelBuilder();
long attr = VertexAttributes.Usage.Position | VertexAttributes.Usage.Normal;
Material mat = new Material(ColorAttribute.createDiffuse(Color.GREEN));

// Convenience methods: createBox, createSphere, createCylinder, createCone,
// createCapsule, createArrow, createLineGrid, createXYZCoordinates, createRect
Model box = mb.createBox(5f, 5f, 5f, mat, attr);
```

**Custom geometry** via `begin()`/`part()`/`end()`:
```java
mb.begin();
MeshPartBuilder mpb = mb.part("partId", GL20.GL_TRIANGLES, attr, mat);
mpb.box(5f, 5f, 5f);  // also: sphere, cylinder, cone, capsule, rect, line, triangle, vertex
Model model = mb.end();
```

`part()` auto-creates a node if none exists. Only one part at a time. `createRect` requires explicit normal (4 corners + normal vector).

## Environment

```java
public class Environment extends Attributes
```

```java
Environment environment = new Environment();
environment.set(new ColorAttribute(ColorAttribute.AmbientLight, 0.4f, 0.4f, 0.4f, 1f));
environment.add(new DirectionalLight().set(0.8f, 0.8f, 0.8f, -1f, -0.8f, -0.2f));
environment.add(new PointLight().set(1f, 1f, 1f, position, intensity));
```

Lights are stored internally in `DirectionalLightsAttribute`, `PointLightsAttribute`, `SpotLightsAttribute`. Ambient light is a `ColorAttribute` with type `ColorAttribute.AmbientLight`.

**`environment.add(light)` / `environment.remove(light)`** — fluent API, returns `this`.

`Environment.shadowMap` field exists (type `ShadowMap` interface) but stock libGDX provides no implementation.

## Lights

`DirectionalLight` (color, direction), `PointLight` (color, position, intensity), `SpotLight` (color, position, direction, intensity, cutoffAngle, exponent). All extend `BaseLight<T>`.

**Gotchas:**
- `set()` overloads normalize direction. `setDirection()` does NOT normalize.
- `set(float r, g, b, ...)` overloads hardcode alpha to `1f`.
- SpotLight: "Note that the default shader doesn't support spot lights." Must increase `DefaultShader.Config.numSpotLights`.

## Materials and Attributes

`Material` extends `Attributes` (container). `Attributes` stores `Attribute` objects keyed by `long type` bitmasks.

```java
Material mat = new Material(
    ColorAttribute.createDiffuse(Color.BLUE),
    ColorAttribute.createSpecular(Color.WHITE),
    FloatAttribute.createShininess(16f)
);
```

**ColorAttribute types:** `Diffuse`, `Specular`, `Ambient`, `Emissive`, `Reflection` (material), `AmbientLight`, `Fog` (environment). **Critical:** `ColorAttribute.Ambient` (material) and `ColorAttribute.AmbientLight` (environment) are different types.

**TextureAttribute types:** `Diffuse`, `Specular`, `Bump`, `Normal`, `Ambient`, `Emissive`, `Reflection` — factory methods accept `Texture` or `TextureRegion`.

**Other attributes:** `BlendingAttribute(true, opacity)`, `FloatAttribute.createShininess()`, `FloatAttribute.createAlphaTest()`, `IntAttribute.createCullFace()` (0=no cull, GL_BACK=default), `DepthTestAttribute`.

## PerspectiveCamera

```java
PerspectiveCamera camera = new PerspectiveCamera(67f, Gdx.graphics.getWidth(), Gdx.graphics.getHeight());
camera.position.set(10f, 10f, 10f);
camera.lookAt(0, 0, 0);
camera.near = 1f;      // default
camera.far = 300f;     // default is only 100 — usually too small
camera.update();       // MUST call after any property change
```

Fields: `fieldOfView` (67, vertical degrees), `near` (1), `far` (100 — increase for large scenes), `position`, `direction`, `up`. `update()` recomputes matrices and frustum — **must call every frame** if camera moves.

## DefaultShaderProvider

```java
DefaultShader.Config config = new DefaultShader.Config();
config.numDirectionalLights = 2;    // default
config.numPointLights = 5;          // default
config.numSpotLights = 0;           // default — spot lights DISABLED
config.numBones = 12;               // default max bones for skeletal animation
ModelBatch modelBatch = new ModelBatch(new DefaultShaderProvider(config));
```

Customize when:
- Scene uses more than 2 directional or 5 point lights
- Using spot lights (must set `numSpotLights > 0`)
- Skeletal meshes have more than 12 bones
- Using custom GLSL shaders

## Camera Controllers

**CameraInputController** (orbit) — extends `GestureDetector`. Left drag=orbit, right drag=pan, scroll/middle drag=zoom, WASD=move/rotate. `target` field is orbit center. Must call `update()` each frame.

**FirstPersonCameraController** — extends `InputAdapter`. WASD=move, QE=up/down, mouse drag=look. `setVelocity(float)`, `setDegreesPerPixel(float)`. Must call `update()` each frame.

Both require `Gdx.input.setInputProcessor(controller)`.

## AnimationController

```java
AnimationController controller = new AnimationController(modelInstance);
controller.update(Gdx.graphics.getDeltaTime());  // MUST call every frame
```

**You do NOT need to call `modelInstance.calculateTransforms()`** — AnimationController calls it internally.

**Key methods:**
- `setAnimation(id)` — immediate switch, plays once. `(id, loopCount)` — `-1` = loop forever. `(id, loopCount, speed, listener)` — negative speed = reverse.
- `animate(id, transitionTime)` — crossfade. `animate(id, loopCount, speed, listener, transitionTime)` — full control.
- `queue(...)` — plays after current finishes (one slot). `action(...)` — one-shot overlay, resumes previous (**throws if loopCount < 0**).

**AnimationListener:** `onEnd(AnimationDesc)` when loopCount reaches 0, `onLoop(AnimationDesc)` each loop boundary.

**Key fields:** `current`/`queued`/`previous` (AnimationDesc), `paused` (boolean), `allowSameAnimation` (default false — re-setting same animation preserves current time).

## Minimal 3D Skeleton

```java
// create(): camera + modelBatch + environment + model/instance
camera = new PerspectiveCamera(67f, Gdx.graphics.getWidth(), Gdx.graphics.getHeight());
camera.position.set(10f, 10f, 10f); camera.lookAt(0,0,0); camera.far = 300f; camera.update();
modelBatch = new ModelBatch();
environment = new Environment();
environment.set(new ColorAttribute(ColorAttribute.AmbientLight, 0.4f, 0.4f, 0.4f, 1f));
environment.add(new DirectionalLight().set(0.8f, 0.8f, 0.8f, -1f, -0.8f, -0.2f));

// render():
ScreenUtils.clear(0.3f, 0.3f, 0.3f, 1f, true); // 5th arg true = clear depth buffer (ESSENTIAL for 3D)
modelBatch.begin(camera);
modelBatch.render(instance, environment);
modelBatch.end();

// dispose(): modelBatch.dispose(); model.dispose(); // ModelInstance is NOT disposable
```

## Disposal Rules

| Resource | Owns | dispose() does |
|----------|------|----------------|
| `Model` (direct load) | Meshes + Textures | Disposes all managed disposables |
| `Model` (AssetManager) | Meshes only | Textures managed by AssetManager |
| `ModelInstance` | Nothing (NOT Disposable) | N/A — source Model owns GPU resources |
| `ModelBatch` | Cached shaders | Disposes ShaderProvider only |
| `ModelBuilder` | Nothing (NOT Disposable) | N/A — returned Models own resources |

## Common Mistakes

1. **Using `ModelBatch.setProjectionMatrix()`** — Does not exist. Camera is passed to `begin(Camera)`. This is the #1 difference from SpriteBatch.
2. **Forgetting `camera.update()`** — Must be called after changing any camera property (position, direction, near, far, FOV) and every frame if the camera moves.
3. **Disposing Model while ModelInstances still reference it** — ModelInstance shares the Model's meshes/textures. Dispose Model only after all instances are no longer rendered.
4. **Not clearing the depth buffer** — Use `ScreenUtils.clear(r, g, b, a, true)` with the fifth `boolean` argument `true` for 3D scenes. Without depth clearing, 3D rendering produces artifacts.
5. **Using SpotLight without configuring the shader** — `DefaultShader.Config.numSpotLights` defaults to 0. SpotLights are silently ignored unless you increase this.
6. **Confusing `ColorAttribute.Ambient` with `ColorAttribute.AmbientLight`** — `Ambient` is a per-material attribute. `AmbientLight` is an environment-level attribute. They have different type bitmasks.
7. **Not calling `AnimationController.update(delta)` every frame** — Animations will not advance. Must be called before `modelBatch.render()`.
8. **Calling `action()` with negative loopCount** — Throws `GdxRuntimeException("An action cannot be continuous")`. Actions must have finite loop counts.
9. **Using ObjLoader in production** — Javadoc explicitly says "should not be used in production." Convert to G3DB/G3DJ format instead.
10. **Calling `calculateTransforms()` when using AnimationController** — AnimationController calls it internally. Manual calls are only needed when modifying Node transforms outside of the animation system.
11. **Using wrong `VertexAttributes.Usage` flags** — Lighting requires `Usage.Normal`. Texturing requires `Usage.TextureCoordinates`. Missing flags produce black or untextured models.
12. **Setting `camera.far = 100` for large scenes** — Default `far` is 100, which clips anything beyond that distance. Set to 300+ for typical scenes.
