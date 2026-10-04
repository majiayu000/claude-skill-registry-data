---
name: libgdx-particles
description: Use when writing libGDX Java/Kotlin code involving 2D or 3D particle effects — ParticleEffect, ParticleEffectPool, ParticleEmitter, particle loading, AssetManager integration, blend functions, or the 3D particle system (ParticleSystem, BillboardParticleBatch). Use when debugging frozen particles, compounding scale, pooled effect leaks, or wrong blend modes.
---

# libGDX Particle Effects

Quick reference for libGDX particle systems. Covers 2D `ParticleEffect`/`ParticleEmitter`/`ParticleEffectPool`, AssetManager loading, blend function management, and the 3D particle system (`g3d.particles`).

## 2D ParticleEffect

`com.badlogic.gdx.graphics.g2d.ParticleEffect` implements `Disposable`.

### Loading

```java
ParticleEffect effect = new ParticleEffect();

// From loose image files (images directory):
effect.load(Gdx.files.internal("explosion.p"), Gdx.files.internal("particles"));
//          ^ effect file                       ^ directory containing particle images

// From TextureAtlas:
effect.load(Gdx.files.internal("explosion.p"), myAtlas);

// From TextureAtlas with prefix:
effect.load(Gdx.files.internal("explosion.p"), myAtlas, "fx_");
```

The second parameter to `load(FileHandle, FileHandle)` is the **images directory**, NOT the effect file's parent. A common mistake is passing `""` — use `Gdx.files.internal("")` for project root.

File format is `.p` (plain text), created by the Particle Editor tool.

### Core Lifecycle

```java
effect.start();                      // starts all emitters
effect.setPosition(x, y);           // set position on all emitters

// In render():
effect.update(Gdx.graphics.getDeltaTime());
effect.draw(batch);                  // param type is Batch (interface), not SpriteBatch

// Or combined:
effect.draw(batch, delta);           // calls update(delta) then draw(batch)

if (effect.isComplete()) { ... }     // true when ALL emitters are complete

effect.reset();                      // kills particles, resets scaling, restarts
effect.dispose();                    // only frees textures if loaded from directory (not atlas)
```

### Key Methods

| Method | Signature | Notes |
|--------|-----------|-------|
| `start()` | `void` | Starts all emitters. Does NOT kill existing particles. |
| `reset()` | `void` | Kills all particles, resets scale to 1.0, restarts all emitters. |
| `reset(boolean)` | `void reset(resetScaling)` | If false, preserves current scale. |
| `reset(boolean, boolean)` | `void reset(resetScaling, start)` | Full control: reset scale + auto-start. |
| `update(float)` | `void update(delta)` | Must call every frame or particles freeze. |
| `draw(Batch)` | `void draw(batch)` | Draws all emitters. |
| `draw(Batch, float)` | `void draw(batch, delta)` | Combined update + draw. |
| `isComplete()` | `boolean` | True when ALL emitters are complete. |
| `allowCompletion()` | `void` | Tells all continuous emitters to finish gracefully. |
| `setPosition(float, float)` | `void setPosition(x, y)` | Sets on all emitters. Call every frame if following entity. |
| `setFlip(boolean, boolean)` | `void setFlip(flipX, flipY)` | Flips all emitters. |
| `flipY()` | `void` | Convenience for vertical flip. |
| `setDuration(int)` | `void setDuration(millis)` | Sets duration in **milliseconds** on ALL emitters. Forces `continuous=false`. |
| `getEmitters()` | `Array<ParticleEmitter>` | Direct access to emitter array. |
| `findEmitter(String)` | `ParticleEmitter` | Returns first emitter with matching name, or `null`. |
| `preAllocateParticles()` | `void` | Pre-allocates particle arrays in all emitters. |
| `getBoundingBox()` | `BoundingBox` | Enclosing box for all emitters. |

### Scaling

```java
effect.scaleEffect(2f);             // scale size AND motion by 2x
effect.scaleEffect(2f, 1f);         // scale size by 2x, motion by 1x
effect.scaleEffect(2f, 3f, 1f);    // xSize=2x, ySize=3x, motion=1x
```

**WARNING: `scaleEffect()` is MULTIPLICATIVE.** Each call multiplies onto the existing tracked scale. Calling `scaleEffect(2f)` twice results in 4x scale, not 2x. Call it **once** after loading.

`reset(true)` (the default) reverts scale to 1.0 by applying the inverse. `reset(false)` preserves the current scale — this is what `ParticleEffectPool.free()` uses.

### Disposal

`dispose()` only frees textures when `ownsTexture` is true — i.e., when loaded via `load(FileHandle, FileHandle)` (directory). When loaded from a `TextureAtlas`, the atlas owns the textures and `dispose()` is a no-op. Dispose the atlas separately.

## ParticleEmitter

`com.badlogic.gdx.graphics.g2d.ParticleEmitter` — each effect contains one or more emitters.

### Key Methods

```java
ParticleEmitter emitter = effect.findEmitter("sparks");

emitter.setContinuous(true);         // emitter loops
emitter.isContinuous();

emitter.allowCompletion();           // gracefully finish: stops spawning, existing particles live out
emitter.isComplete();                // true when done spawning AND all particles dead
emitter.getPercentComplete();        // 0.0–1.0

emitter.setPosition(x, y);
emitter.getX();  emitter.getY();

emitter.setAdditive(true);           // additive blending (default: true)
emitter.setPremultipliedAlpha(false); // premultiplied alpha (default: false)
emitter.setCleansUpBlendFunction(b); // restore blend state after draw (default: true)

emitter.getMaxParticleCount();
emitter.setMaxParticleCount(500);
emitter.getActiveCount();
```

### Emitter Value Properties

All return value objects (not primitives). Modify via their setters.

| Getter | Return Type | What It Controls |
|--------|-------------|------------------|
| `getEmission()` | `ScaledNumericValue` | Particles per second |
| `getLife()` | `IndependentScaledNumericValue` | Particle lifetime |
| `getLifeOffset()` | `IndependentScaledNumericValue` | Life start offset |
| `getXScale()` | `ScaledNumericValue` | Horizontal size |
| `getYScale()` | `ScaledNumericValue` | Vertical size |
| `getRotation()` | `ScaledNumericValue` | Rotation |
| `getVelocity()` | `ScaledNumericValue` | Speed |
| `getAngle()` | `ScaledNumericValue` | Emission angle |
| `getWind()` | `ScaledNumericValue` | Horizontal drift |
| `getGravity()` | `ScaledNumericValue` | Vertical drift |
| `getTransparency()` | `ScaledNumericValue` | Alpha over lifetime |
| `getTint()` | `GradientColorValue` | Color over lifetime |
| `getDuration()` | `RangedNumericValue` | How long emitter runs |
| `getDelay()` | `RangedNumericValue` | Start delay |
| `getSpawnShape()` | `SpawnShapeValue` | Spawn area shape |

The `duration` and `durationTimer` fields are **public floats** (milliseconds) and can be accessed directly.

**There is NO `setColor()` on ParticleEmitter.** Color is set via `getTint()` which returns a `GradientColorValue`.

### SpriteMode Enum

`ParticleEmitter.SpriteMode`: `single`, `random`, `animated` — controls multi-sprite behavior per emitter.

## ParticleEffectPool

`com.badlogic.gdx.graphics.g2d.ParticleEffectPool` extends `Pool<PooledEffect>`. Use to avoid GC from repeatedly creating/disposing effects.

```java
// Create pool from a template effect (loaded once):
ParticleEffect template = new ParticleEffect();
template.load(Gdx.files.internal("explosion.p"), Gdx.files.internal("particles"));

ParticleEffectPool pool = new ParticleEffectPool(template, 4, 16);
//                                               effect  initial  max

// Obtain and use:
ParticleEffectPool.PooledEffect effect = pool.obtain();
effect.setPosition(x, y);

// In render():
effect.update(delta);
effect.draw(batch);

// When done (isComplete or manually):
effect.free();     // returns to pool — calls reset(false) internally (preserves scale matching)

// DO NOT call effect.dispose() — that would break the pool.
```

`PooledEffect` extends `ParticleEffect`. The `free()` method is a convenience that calls `pool.free(this)`. The pool's `free()` resets the effect without resetting scaling, then re-matches scale to the template.

### Standard Pool Pattern

```java
Array<ParticleEffectPool.PooledEffect> activeEffects = new Array<>();

// Spawn:
ParticleEffectPool.PooledEffect effect = pool.obtain();
effect.setPosition(x, y);
activeEffects.add(effect);

// Update/draw:
for (int i = activeEffects.size - 1; i >= 0; i--) {
    ParticleEffectPool.PooledEffect effect = activeEffects.get(i);
    effect.draw(batch, delta);
    if (effect.isComplete()) {
        effect.free();
        activeEffects.removeIndex(i);
    }
}
```

## AssetManager Loading

`com.badlogic.gdx.assets.loaders.ParticleEffectLoader` — synchronous loader for 2D effects.

```java
// Default: images from effect file's parent directory
manager.load("particles/explosion.p", ParticleEffect.class);

// With TextureAtlas:
ParticleEffectLoader.ParticleEffectParameter param =
    new ParticleEffectLoader.ParticleEffectParameter();
param.atlasFile = "particles/particles.atlas";  // String, not FileHandle
// param.atlasPrefix = "fx_";                   // optional prefix for region names
manager.load("particles/explosion.p", ParticleEffect.class, param);

// With explicit images directory:
ParticleEffectLoader.ParticleEffectParameter param =
    new ParticleEffectLoader.ParticleEffectParameter();
param.imagesDir = Gdx.files.internal("particles/images");  // FileHandle, not String
manager.load("particles/explosion.p", ParticleEffect.class, param);
```

**`ParticleEffectParameter` fields:**

| Field | Type | Notes |
|-------|------|-------|
| `atlasFile` | `String` | Atlas file path. Takes priority over `imagesDir`. Atlas auto-loaded as dependency. |
| `atlasPrefix` | `String` | Optional prefix for atlas region lookups. Only used with `atlasFile`. |
| `imagesDir` | `FileHandle` | Image directory. Ignored if `atlasFile` is set. |

Default (no param): loads images from the `.p` file's parent directory.

## Blend Function Management

Particle emitters default to **additive blending** (`additive=true`). After drawing, the emitter restores the batch's blend function to standard alpha blending — controlled by `cleansUpBlendFunction` (default: `true`).

```java
// Disable cleanup for performance when drawing many additive effects in sequence:
effect.setEmittersCleanUpBlendFunction(false);
// ... draw multiple effects ...
// Manually restore blend function:
batch.setBlendFunction(GL20.GL_SRC_ALPHA, GL20.GL_ONE_MINUS_SRC_ALPHA);
```

Setting `cleansUpBlendFunction=false` avoids redundant batch flushes between effects that share the same blend mode. You MUST restore the blend function manually before drawing non-particle sprites.

## Particle Editor

**Standalone tool** for creating/editing `.p` files.

- Legacy: `com.badlogic.gdx.tools.particleeditor.ParticleEditor` in `gdx-tools` (Swing + LWJGL2, issues on macOS/Apple Silicon).
- Recommended: [gdx-particle-editor](https://github.com/libgdx/gdx-particle-editor) — pure Scene2D UI, works on all platforms. Exports same `.p` format.

## 3D Particle System (Brief)

**Package:** `com.badlogic.gdx.graphics.g3d.particles` — entirely separate from 2D particles. Different classes, different APIs, different file format.

**DO NOT confuse** `com.badlogic.gdx.graphics.g2d.ParticleEffect` (2D) with `com.badlogic.gdx.graphics.g3d.particles.ParticleEffect` (3D). They share the same simple class name but are unrelated.

### Architecture

| Concept | 2D | 3D |
|---------|----|----|
| Effect | `g2d.ParticleEffect` | `g3d.particles.ParticleEffect` |
| Sub-unit | `ParticleEmitter` | `ParticleController` (with Emitter + Influencers + Renderer) |
| Rendering | Draws to `Batch` directly | Uses `ParticleSystem` + `ParticleBatch` + `ModelBatch` |
| File format | `.p` (plain text) | `.pfx` (JSON) |
| Position | `setPosition(x, y)` | `setTransform(Matrix4)`, `translate(Vector3)` |
| Editor | Particle Editor | Flame Editor |
| System manager | None needed | `ParticleSystem` required |

### 3D Setup Pattern

```java
// ParticleSystem manages batches and effects
ParticleSystem particleSystem = new ParticleSystem();

// Create a batch (camera-facing quads):
BillboardParticleBatch billboardBatch = new BillboardParticleBatch();
billboardBatch.setCamera(camera);
particleSystem.add(billboardBatch);

// Other batch types:
// PointSpriteParticleBatch   — GPU point sprites (efficient, less flexible)
// ModelInstanceParticleBatch — 3D model instances (expensive, most versatile)

// Load via AssetManager:
Array<ParticleBatch<?>> batches = new Array<>();
batches.add(billboardBatch);
ParticleEffectLoader.ParticleEffectLoadParameter loadParam =
    new ParticleEffectLoader.ParticleEffectLoadParameter(batches);
manager.load("effect.pfx", com.badlogic.gdx.graphics.g3d.particles.ParticleEffect.class, loadParam);

// Render loop:
particleSystem.update();
particleSystem.begin();
particleSystem.draw();
particleSystem.end();
modelBatch.render(particleSystem);  // ParticleSystem implements RenderableProvider
```

The 3D `ParticleEffectLoader` is at `com.badlogic.gdx.graphics.g3d.particles.ParticleEffectLoader` — a SEPARATE class from the 2D loader. You MUST pass batches via `ParticleEffectLoadParameter`.

**Note:** The 3D particle system is complex and less commonly used. See the [libGDX wiki on 3D particle effects](https://libgdx.com/wiki/graphics/3d/3d-particle-effects) for detailed documentation.

## Common Mistakes

1. **Calling `scaleEffect()` every frame** — It multiplies onto existing scale. Calling `scaleEffect(2f)` twice = 4x scale. Call it once after loading, or track and undo with `reset(true)`.
2. **Forgetting `update(delta)`** — Particles freeze in place. Must call every frame (or use `draw(batch, delta)` which combines both).
3. **Calling `dispose()` on pooled effects** — Use `effect.free()` to return to pool. `dispose()` destroys the textures and breaks the pool.
4. **Loading in `render()`** — `new ParticleEffect()` + `load()` is expensive. Load once in `create()`, then reuse or pool.
5. **Wrong second argument to `load()`** — The second parameter is the images **directory** (FileHandle), not the effect file path. Pass `Gdx.files.internal("particles")` for images in `assets/particles/`.
6. **Calling `setPosition()` only once** — Position is not inherited from a parent. If the effect follows a moving entity, call `setPosition()` every frame.
7. **Disposing atlas-loaded effects** — `dispose()` is a no-op when loaded from `TextureAtlas` (atlas owns the textures). Dispose the atlas instead.
8. **Inventing `effect.setColor()`** — Does not exist. Color is per-emitter via `emitter.getTint()` which returns a `GradientColorValue`.
9. **Not calling `start()` after loading** — A freshly loaded effect needs `start()` before particles emit. (Pool's `obtain()` calls `start()` automatically.)
10. **Confusing 2D and 3D ParticleEffect** — Same simple class name, different packages (`g2d` vs `g3d.particles`), completely different APIs. Wrong import = compile errors or wrong behavior.
11. **Using `allowCompletion()` on non-continuous emitters** — Only meaningful for continuous emitters. On non-continuous emitters it just sets `durationTimer = duration`, which may cause them to stop prematurely if called early.
12. **Rendering particles outside SpriteBatch begin/end** — `effect.draw(batch)` must be called between `batch.begin()` and `batch.end()`. The effect uses the batch's current projection matrix and blend state.
