---
name: libgdx-2d-rendering
description: Use when writing libGDX Java/Kotlin code involving 2D rendering — SpriteBatch, ShapeRenderer, Texture, TextureRegion, TextureAtlas, Camera, Viewport, draw ordering, blending, or screen clearing. Use when debugging rendering artifacts, missing sprites, stretched graphics, or begin/end errors.
---

# libGDX 2D Rendering

Reference for SpriteBatch, ShapeRenderer, Texture, TextureRegion, TextureAtlas, Camera/Viewport integration, draw ordering, blending, and screen clearing.

## Texture

```java
// Load from internal assets
Texture tex = new Texture(Gdx.files.internal("image.png"));

// With specific filtering and wrapping
Texture tex = new Texture(Gdx.files.internal("image.png"));
tex.setFilter(TextureFilter.Nearest, TextureFilter.Nearest); // pixel art
tex.setFilter(TextureFilter.Linear, TextureFilter.Linear);   // smooth scaling
tex.setWrap(TextureWrap.Repeat, TextureWrap.Repeat);         // tiling
```

**TextureFilter — min/mag:**
| Filter | Use for | Result |
|---|---|---|
| `Nearest` | Pixel art, retro games | Sharp pixels, no blurring |
| `Linear` | Smooth artwork, UI | Bilinear interpolation |
| `MipMapLinearLinear` | Large textures drawn small | Smooth mipmapped (min filter only) |

Default filter is `Nearest`. For smooth-scaled artwork, you must explicitly set `Linear`.

**TextureWrap:** `ClampToEdge` (default), `Repeat`, `MirroredRepeat`. Only `Repeat`/`MirroredRepeat` require power-of-two texture dimensions.

**Power-of-two:** Not required for general use on modern GPUs. Only required when using `Repeat`/`MirroredRepeat` wrap modes or mipmaps. Non-POT textures work fine with `ClampToEdge` (the default).

**Disposal:** Textures hold GPU memory — you MUST call `dispose()` when done. See Disposal section below.

## TextureRegion

A rectangular sub-area of a Texture. Used for sprite sheets, tilesets, and atlas regions. Drawing a TextureRegion does NOT copy pixels — it references the parent Texture with UV coordinates.

```java
Texture sheet = new Texture(Gdx.files.internal("spritesheet.png"));

// Single region: x, y, width, height (pixels, top-left origin)
TextureRegion region = new TextureRegion(sheet, 0, 0, 32, 32);

// Split entire sheet into a 2D array of regions
TextureRegion[][] frames = TextureRegion.split(sheet, 32, 32); // tileWidth, tileHeight
TextureRegion firstFrame = frames[0][0]; // row 0, col 0

// Flip (sprite sheets sometimes have Y flipped)
region.flip(false, true); // flipX, flipY
```

**Do NOT dispose a TextureRegion.** Dispose the parent Texture only. Disposing the Texture invalidates all regions referencing it.

## TextureAtlas

Packs multiple images into one or more textures with a `.atlas` descriptor file (created by libGDX TexturePacker or tools like gdx-texture-packer-gui).

```java
TextureAtlas atlas = new TextureAtlas(Gdx.files.internal("pack.atlas"));

// Get a single region by name (name = original filename without extension)
AtlasRegion hero = atlas.findRegion("hero");

// Get indexed regions: hero_0, hero_1, hero_2 (or hero0, hero1, hero2)
Array<AtlasRegion> runFrames = atlas.findRegions("hero_run");

// Create Animation from atlas regions
Animation<TextureRegion> runAnim = new Animation<>(0.1f, runFrames, PlayMode.LOOP);

atlas.dispose(); // disposes ALL backing textures
```

**Do NOT separately dispose Textures obtained from an atlas.** The atlas owns them — `atlas.dispose()` handles it. In non-trivial projects, prefer loading via `AssetManager` for lifecycle management.

## SpriteBatch

Batches textured quads into a single draw call for GPU efficiency. **All draw calls MUST be between `begin()` and `end()`.** Calling `draw()` outside throws `IllegalStateException`.

```java
SpriteBatch batch = new SpriteBatch();

// REQUIRED: set projection matrix before begin() if using a Camera
batch.setProjectionMatrix(camera.combined);

batch.begin();
// --- All draws here ---
batch.draw(texture, x, y);
batch.draw(texture, x, y, width, height);
batch.draw(region, x, y);
batch.draw(region, x, y, width, height);
batch.draw(region, x, y, originX, originY, width, height, scaleX, scaleY, rotation);
batch.end();
```

### setProjectionMatrix — REQUIRED with Camera

**If you use an `OrthographicCamera` or `Viewport`, you MUST call `batch.setProjectionMatrix(camera.combined)` before `batch.begin()`.** Without it, SpriteBatch draws in a default pixel-coordinate projection that ignores your camera's position, zoom, and viewport.

```java
// In render():
camera.update();
batch.setProjectionMatrix(camera.combined);  // BEFORE begin()
batch.begin();
// draws use camera's coordinate system
batch.end();
```

Call `setProjectionMatrix()` BEFORE `begin()`, not between `begin()`/`end()` — calling it mid-batch forces a flush (performance hit).

### Draw Overloads

| Method | Use |
|---|---|
| `draw(Texture, x, y)` | Full texture at position, original size |
| `draw(Texture, x, y, w, h)` | Full texture, scaled to w×h |
| `draw(TextureRegion, x, y)` | Region at position, original size |
| `draw(TextureRegion, x, y, w, h)` | Region, scaled |
| `draw(TextureRegion, x, y, originX, originY, w, h, scaleX, scaleY, rotation)` | Full transform |

`originX`/`originY` are relative to position (x, y), not to the texture. Rotation is in degrees, counter-clockwise.

### setColor / Tinting

`batch.setColor(r, g, b, a)` tints all subsequent draws by multiplying texture colors by the given color. White (1,1,1,1) = no tint. **The tint persists until you change it again** — the most common bug is forgetting to reset after tinting one sprite, which causes everything drawn after it to be tinted.

```java
batch.begin();
batch.draw(background, 0, 0);           // drawn with current color (white by default)

batch.setColor(1, 0, 0, 1);             // red tint
batch.draw(hitEnemy, ex, ey);            // drawn red

batch.setColor(Color.WHITE);            // RESET — always do this after tinting
batch.draw(player, px, py);             // drawn normally
batch.end();
```

**Pattern:** `setColor(tint)` → `draw()` → `setColor(Color.WHITE)`. Always reset to `Color.WHITE` after tinting.

### Batching Efficiency

SpriteBatch has a default capacity of 1000 quads. A texture switch (drawing from a different `Texture` object) forces a flush — a new draw call to the GPU. This is why `TextureAtlas` packing matters: drawing many sprites from one atlas texture avoids flushes. Minimizing texture switches is the single most impactful batching optimization.

## Sprite

`Sprite` extends `TextureRegion` and bundles position, size, rotation, origin, color, and flip into one object. Call `sprite.draw(batch)` instead of passing all parameters to `batch.draw()` manually.

**Use `Sprite` when** you need per-entity transforms (position, rotation, scale, tint) that change each frame. **Use raw `TextureRegion` draws** when you're just blitting from an atlas with no per-sprite state (tiles, static UI).

## Camera & Viewport

**Default coordinate system:** `OrthographicCamera` centers at (0,0), so the visible area spans (-halfWidth, -halfHeight) to (+halfWidth, +halfHeight). Many users expect (0,0) to be the bottom-left corner. Use `viewport.update(width, height, true)` in `resize()` to center the camera at (worldWidth/2, worldHeight/2), which shifts (0,0) to the bottom-left.

```java
// In create():
OrthographicCamera camera = new OrthographicCamera();
Viewport viewport = new FitViewport(worldWidth, worldHeight, camera);

// In resize():
viewport.update(width, height, true); // true = centerCamera → (0,0) at bottom-left

// In render():
camera.update();
batch.setProjectionMatrix(camera.combined);
```

**`viewport.update(width, height, true)`** — the `true` parameter centers the camera at (worldWidth/2, worldHeight/2). Without it, the camera stays at its current position — which defaults to (0,0), meaning the visible area is centered at the origin. This causes the classic "everything renders in the top-right corner" bug when you place sprites at positive coordinates expecting (0,0) to be bottom-left.

**Common Viewport types:**

| Viewport | Behavior |
|---|---|
| `FitViewport` | Maintains aspect ratio, letterboxes/pillarboxes |
| `FillViewport` | Maintains aspect ratio, crops edges |
| `StretchViewport` | Fills screen, may distort |
| `ExtendViewport` | Extends world to fill screen, no distortion |
| `ScreenViewport` | 1:1 pixel mapping (commonly used with Scene2D Stage for UI) |

**`viewport.update(width, height)`** must be called in `resize()` — without it, the viewport won't adapt to window size changes.

## Draw Ordering

**libGDX has NO automatic z-sorting or depth testing for 2D.** SpriteBatch uses the painter's algorithm: sprites are drawn in submission order. Later draws appear on top of earlier draws.

```java
batch.begin();
batch.draw(background, 0, 0);  // drawn first = behind
batch.draw(player, px, py);     // drawn second = on top
batch.draw(hud, hx, hy);        // drawn last = in front
batch.end();
```

For y-sorting (top-down games where lower entities appear in front):
```java
entities.sort((a, b) -> Float.compare(b.y, a.y)); // higher y drawn first
batch.begin();
for (Entity e : entities) {
    batch.draw(e.region, e.x, e.y);
}
batch.end();
```

## Blending

SpriteBatch **enables GL blending by default** (`GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA`). This is correct for transparent sprites.

```java
// Disable blending for fully opaque layers (background) — small perf gain
batch.disableBlending();
batch.begin();
batch.draw(opaqueBackground, 0, 0);
batch.end();

// Re-enable for sprites with transparency
batch.enableBlending();
batch.begin();
batch.draw(transparentSprite, x, y);
batch.end();
```

Disable blending only when drawing fully opaque textures where you're certain no alpha is needed. The performance gain is minor in most games.

## ShapeRenderer

Draws geometric primitives (rectangles, circles, lines). Same begin/end contract as SpriteBatch.

```java
ShapeRenderer shapes = new ShapeRenderer();
shapes.setProjectionMatrix(camera.combined); // same as SpriteBatch

shapes.begin(ShapeType.Filled);
shapes.setColor(Color.RED);
shapes.rect(x, y, width, height);
shapes.circle(cx, cy, radius);
shapes.end();

shapes.begin(ShapeType.Line);
shapes.setColor(Color.WHITE);
shapes.line(x1, y1, x2, y2);
shapes.rectLine(x1, y1, x2, y2, lineWidth);
shapes.end();
```

**ShapeType:** `Filled` (solid), `Line` (outlines), `Point` (dots). You cannot change ShapeType between `begin()` and `end()` — you must end and begin again.

### ShapeRenderer Does NOT Enable Blending

Unlike SpriteBatch, **ShapeRenderer does NOT enable GL blending by default.** Alpha values in `setColor()` are silently ignored — shapes render fully opaque. To draw semi-transparent shapes, you must enable blending manually:

```java
Gdx.gl.glEnable(GL20.GL_BLEND);
Gdx.gl.glBlendFunc(GL20.GL_SRC_ALPHA, GL20.GL_ONE_MINUS_SRC_ALPHA);
shapes.begin(ShapeType.Filled);
shapes.setColor(0, 0, 0, 0.5f);         // 50% transparent black
shapes.rect(0, 0, worldWidth, worldHeight); // pause overlay
shapes.end();
Gdx.gl.glDisable(GL20.GL_BLEND);        // optional: restore default
```

### NEVER Intermix SpriteBatch and ShapeRenderer

**You CANNOT have SpriteBatch and ShapeRenderer open at the same time.** Each maintains its own GL state. Nesting or interleaving their begin/end blocks causes rendering corruption or crashes.

```java
// WRONG — nested begin/end
batch.begin();
batch.draw(texture, x, y);
shapes.begin(ShapeType.Filled);  // WRONG: batch is still open
shapes.rect(x, y, w, h);
shapes.end();
batch.end();

// RIGHT — sequential begin/end blocks
batch.setProjectionMatrix(camera.combined);
batch.begin();
batch.draw(texture, x, y);
batch.end();                     // batch CLOSED first

shapes.setProjectionMatrix(camera.combined);
shapes.begin(ShapeType.Filled);  // then shapes opens
shapes.rect(x, y, w, h);
shapes.end();
```

**Order tip:** Draw all SpriteBatch content first, then all ShapeRenderer content (or vice versa) to minimize begin/end switches.

## ScreenUtils.clear()

**Use `ScreenUtils.clear()` (since libGDX 1.10.0) instead of the verbose `Gdx.gl.glClearColor()` + `Gdx.gl.glClear()` pattern.**

```java
// Modern — use this
ScreenUtils.clear(0.15f, 0.15f, 0.2f, 1f);           // RGBA floats
ScreenUtils.clear(Color.SKY);                           // named Color constant

// Old verbose pattern — DO NOT USE in new code
Gdx.gl.glClearColor(0, 0, 0, 1);
Gdx.gl.glClear(GL20.GL_COLOR_BUFFER_BIT);
```

Both are functionally identical. **Always use `ScreenUtils.clear()` in new code.** Do not present the `glClearColor`+`glClear` pattern as an alternative — it is the legacy approach replaced by `ScreenUtils.clear()` in 1.10.0.

## Disposal

These types hold GPU/native resources and MUST be disposed:

| Type | What it holds |
|---|---|
| `Texture` | GPU texture memory |
| `SpriteBatch` | Mesh + shader |
| `ShapeRenderer` | Mesh + shader |
| `TextureAtlas` | All backing Texture(s) |
| `BitmapFont` | Texture(s) |
| `FrameBuffer` | GL framebuffer + texture |
| `Skin` | Textures, fonts |

**Do NOT dispose:**
- `TextureRegion` — does not own the Texture
- `AtlasRegion` — owned by the TextureAtlas
- Textures obtained from a `TextureAtlas` — the atlas disposes them

**Dispose in reverse creation order** when possible. In non-trivial projects, use `AssetManager` to handle disposal via `unload()` and `clear()`.

## Minimal Working Example

```java
import com.badlogic.gdx.ApplicationAdapter;
import com.badlogic.gdx.Gdx;
import com.badlogic.gdx.graphics.OrthographicCamera;
import com.badlogic.gdx.graphics.Texture;
import com.badlogic.gdx.graphics.g2d.SpriteBatch;
import com.badlogic.gdx.utils.ScreenUtils;
import com.badlogic.gdx.utils.viewport.FitViewport;

public class MyGame extends ApplicationAdapter {
    SpriteBatch batch;
    Texture img;
    OrthographicCamera camera;
    FitViewport viewport;

    @Override
    public void create() {
        camera = new OrthographicCamera();
        viewport = new FitViewport(800, 480, camera);
        batch = new SpriteBatch();
        img = new Texture(Gdx.files.internal("player.png"));
    }

    @Override
    public void render() {
        ScreenUtils.clear(0.15f, 0.15f, 0.2f, 1f);
        camera.update();
        batch.setProjectionMatrix(camera.combined);
        batch.begin();
        batch.draw(img, 100, 100);
        batch.end();
    }

    @Override
    public void resize(int width, int height) {
        viewport.update(width, height, true); // true = center camera, (0,0) at bottom-left
    }

    @Override
    public void dispose() {
        batch.dispose();
        img.dispose();
    }
}
```

## Common Mistakes

1. **Nesting SpriteBatch and ShapeRenderer begin/end blocks** — Never open one while the other is still open. End the first before beginning the second.
2. **Forgetting `batch.setProjectionMatrix(camera.combined)`** — Without this, SpriteBatch uses default pixel coordinates and ignores your camera entirely. Must be called BEFORE `begin()`.
3. **Not disposing Textures** — Textures hold GPU memory. Forgetting `dispose()` leaks VRAM. Use AssetManager for non-trivial projects.
4. **Disposing TextureRegion or atlas-owned Textures** — TextureRegion doesn't own the texture. Atlas-owned textures are disposed by `atlas.dispose()`. Only dispose what you directly created.
5. **Using old `Gdx.gl.glClearColor()` + `glClear()` pattern** — Use `ScreenUtils.clear()` instead (since 1.10.0). Same result, less boilerplate.
6. **Expecting automatic z-sorting** — libGDX draws in submission order. There is no z-buffer for 2D. Sort entities yourself before drawing.
7. **Calling `setProjectionMatrix()` between begin/end** — This forces a batch flush. Call it BEFORE `begin()`.
8. **Not calling `viewport.update()` in `resize()`** — Viewport won't adapt to window changes, causing stretched or misplaced graphics.
9. **Using Nearest filter for smooth artwork (or Linear for pixel art)** — Nearest preserves sharp pixels; Linear smooths. Default is Nearest. Set explicitly based on art style.
10. **Forgetting `camera.update()` before drawing** — Camera matrix won't reflect position/zoom changes made since last update.
11. **Forgetting to reset `batch.setColor()` to `Color.WHITE` after tinting** — All subsequent draws remain tinted. Always reset: `setColor(tint)` → `draw()` → `setColor(Color.WHITE)`.
12. **Drawing semi-transparent shapes with ShapeRenderer without enabling GL blending** — Alpha is ignored, shapes render opaque. Call `Gdx.gl.glEnable(GL20.GL_BLEND)` before the ShapeRenderer block.
13. **Not passing `true` to `viewport.update(width, height, true)` and wondering why content appears offset** — Without `centerCamera`, the camera stays at (0,0) center, not bottom-left origin. Sprites at positive coordinates appear in the top-right corner.
