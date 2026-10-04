---
name: libgdx-camera-viewport
description: Use when writing libGDX Java/Kotlin code involving Camera, OrthographicCamera, PerspectiveCamera, Viewport (FitViewport, FillViewport, StretchViewport, ExtendViewport, ScreenViewport), coordinate unprojection, resize handling, or multiple camera/viewport setups. Use when debugging wrong click positions, stretched graphics, offset rendering, or (0,0) not at bottom-left.
---

# libGDX Camera & Viewport

Quick reference for Camera, OrthographicCamera, PerspectiveCamera, the Viewport hierarchy, coordinate conversion, and resize handling.

## Camera Base Class

`com.badlogic.gdx.graphics.Camera` — abstract base for both orthographic and perspective cameras.

### Public Fields

| Field | Type | Default | Notes |
|---|---|---|---|
| `position` | `final Vector3` | `(0, 0, 0)` | Mutable object, immutable reference |
| `direction` | `final Vector3` | `(0, 0, -1)` | Points into the screen |
| `up` | `final Vector3` | `(0, 1, 0)` | |
| `near` | `float` | `1` | Near clipping plane |
| `far` | `float` | `100` | Far clipping plane |
| `viewportWidth` | `float` | `0` | |
| `viewportHeight` | `float` | `0` | |
| `combined` | `final Matrix4` | | Projection × View matrix |
| `projection` | `final Matrix4` | | Projection matrix only |
| `view` | `final Matrix4` | | View matrix only |
| `invProjectionView` | `final Matrix4` | | Inverse of combined |
| `frustum` | `final Frustum` | | View frustum for culling |

All `Vector3` and `Matrix4` fields are `final` — the objects are mutable but the references cannot be reassigned. **There is no `setPosition()`, `moveTo()`, `setDirection()`, or `setFov()` method.** Modify fields directly:

```java
camera.position.set(x, y, 0);        // set position
camera.position.add(dx, dy, 0);      // move by delta
camera.direction.set(0, 0, -1);      // reset direction
```

### Key Methods

```java
// MUST call after changing ANY camera property (position, zoom, etc.)
void update()
void update(boolean updateFrustum)     // false = skip frustum update (minor perf gain)

// Orientation
void lookAt(float x, float y, float z)
void lookAt(Vector3 target)
void normalizeUp()

// Transform
void rotate(float angle, float axisX, float axisY, float axisZ)
void rotate(Vector3 axis, float angle)
void rotate(Matrix4 transform)
void rotate(Quaternion quat)
void rotateAround(Vector3 point, Vector3 axis, float angle)
void translate(float x, float y, float z)
void translate(Vector3 vec)
void transform(Matrix4 transform)

// Coordinate conversion — see Coordinate Conversion section
Vector3 unproject(Vector3 screenCoords)
Vector3 project(Vector3 worldCoords)
Ray getPickRay(float screenX, float screenY)
```

## OrthographicCamera

### Construction

```java
OrthographicCamera camera = new OrthographicCamera();
// Sets near=0 only. viewportWidth/Height = 0, position = (0,0,0). Does NOT call update().

OrthographicCamera camera = new OrthographicCamera(viewportWidth, viewportHeight);
// Sets viewportWidth, viewportHeight, near=0. Calls update().
// Position remains at (0,0,0) — center of the viewport is at origin.
```

### Zoom

```java
public float zoom = 1;  // default
```

| `zoom` value | Effect |
|---|---|
| `1.0` | Normal (default) |
| `0.5` | Zoomed **in** — see half as much world |
| `2.0` | Zoomed **out** — see twice as much world |

**Zoom direction is counterintuitive:** smaller values = zoom in, larger values = zoom out. The `zoom` field directly scales the orthographic projection extents.

### setToOrtho()

```java
camera.setToOrtho(false);                              // uses Gdx.graphics.getWidth/Height()
camera.setToOrtho(false, viewportWidth, viewportHeight); // explicit size
```

`setToOrtho(false, w, h)` does three things:
1. Sets `up = (0,1,0)`, `direction = (0,0,-1)` (Y-up orientation)
2. **Moves camera position** to `(zoom * w/2, zoom * h/2, 0)` — so (0,0) is at bottom-left
3. Calls `update()`

With `yDown = true`: flips `up` to (0,-1,0) and `direction` to (0,0,1) — Y-down coordinate system.

### Additional Convenience Methods

```java
void rotate(float angle)              // rotates around direction vector (z-axis by default)
void translate(float x, float y)      // calls translate(x, y, 0)
void translate(Vector2 vec)           // calls translate(vec.x, vec.y, 0)
```

## PerspectiveCamera

```java
PerspectiveCamera camera = new PerspectiveCamera();
// fieldOfView = 67 (vertical, degrees). near=1, far=100.

PerspectiveCamera camera = new PerspectiveCamera(fieldOfViewY, viewportWidth, viewportHeight);
// Sets fieldOfView, viewportWidth, viewportHeight. Calls update().
// Does NOT set near/far — inherits Camera defaults (near=1, far=100).
```

`fieldOfView` is **vertical** FOV in degrees. Horizontal FOV is derived from the aspect ratio. For 3D, you typically need to set `near` and `far` explicitly:

```java
PerspectiveCamera camera = new PerspectiveCamera(67, Gdx.graphics.getWidth(), Gdx.graphics.getHeight());
camera.near = 0.1f;
camera.far = 1000f;
camera.position.set(10, 10, 10);
camera.lookAt(0, 0, 0);
camera.update();
```

For 3D camera controls, see `CameraInputController` in `com.badlogic.gdx.graphics.g3d.utils` — extends `GestureDetector`, provides orbit/pan/zoom via mouse.

## Coordinate Conversion

### Screen → World (unproject)

Input events (`touchDown`, `Gdx.input.getX/Y()`) give **screen coordinates**: Y-down, (0,0) at top-left. Game logic uses **world coordinates**: Y-up, origin depends on camera setup. You MUST convert.

**With Viewport (preferred — handles letterboxing/pillarboxing correctly):**

```java
private final Vector2 touchPos = new Vector2();  // reuse — don't allocate per event

@Override
public boolean touchDown(int screenX, int screenY, int pointer, int button) {
    touchPos.set(screenX, screenY);
    viewport.unproject(touchPos);            // Vector2 — accounts for viewport offset
    spawnEntity(touchPos.x, touchPos.y);
    return true;
}
```

**With Camera directly (no viewport offset handling):**

```java
private final Vector3 touchPos = new Vector3();  // reuse

@Override
public boolean touchDown(int screenX, int screenY, int pointer, int button) {
    touchPos.set(screenX, screenY, 0);       // z=0 for 2D
    camera.unproject(touchPos);              // Vector3 — mutates and returns same instance
    spawnEntity(touchPos.x, touchPos.y);
    return true;
}
```

**`viewport.unproject(Vector2)` vs `camera.unproject(Vector3)`:**
- Viewport version takes `Vector2`, handles letterbox/pillarbox offset automatically
- Camera version takes `Vector3`, assumes viewport fills the entire screen
- **Prefer `viewport.unproject()` when using Viewports**

### World → Screen (project)

```java
Vector3 worldPos = new Vector3(entity.x, entity.y, 0);
camera.project(worldPos);  // now contains screen coordinates (Y-up from bottom-left)
```

`viewport.project(Vector2)` is also available for the viewport-aware variant.

## Viewport

`com.badlogic.gdx.utils.viewport.Viewport` — manages a Camera and handles screen-to-world mapping on resize.

### Viewport Types

| Viewport | Behavior | Black bars? | Distortion? | Cropping? |
|---|---|---|---|---|
| `FitViewport` | Letterbox/pillarbox | Yes | No | No |
| `FillViewport` | Fills screen, crops edges | No | No | Yes |
| `StretchViewport` | Stretches to fill | No | **Yes** | No |
| `ExtendViewport` | Extends world to fill | No | No | No |
| `ScreenViewport` | 1:1 pixel mapping | No | No | No |

### Construction

All viewport constructors optionally accept a Camera. **If you omit the Camera, the viewport creates a default `OrthographicCamera`.** If you have your own camera, pass it to avoid disconnection:

```java
// GOOD — your camera is used by the viewport
OrthographicCamera camera = new OrthographicCamera();
FitViewport viewport = new FitViewport(800, 480, camera);

// BAD — viewport creates its own internal camera, yours is disconnected
OrthographicCamera camera = new OrthographicCamera();
FitViewport viewport = new FitViewport(800, 480);  // viewport.getCamera() != camera
```

Constructor signatures:

```java
FitViewport(float worldWidth, float worldHeight)
FitViewport(float worldWidth, float worldHeight, Camera camera)

FillViewport(float worldWidth, float worldHeight)
FillViewport(float worldWidth, float worldHeight, Camera camera)

StretchViewport(float worldWidth, float worldHeight)
StretchViewport(float worldWidth, float worldHeight, Camera camera)

ExtendViewport(float minWorldWidth, float minWorldHeight)
ExtendViewport(float minWorldWidth, float minWorldHeight, Camera camera)
ExtendViewport(float minWorldWidth, float minWorldHeight, float maxWorldWidth, float maxWorldHeight)
ExtendViewport(float minWorldWidth, float minWorldHeight, float maxWorldWidth, float maxWorldHeight, Camera camera)

ScreenViewport()
ScreenViewport(Camera camera)

ScalingViewport(Scaling scaling, float worldWidth, float worldHeight)
ScalingViewport(Scaling scaling, float worldWidth, float worldHeight, Camera camera)
```

`FitViewport`, `FillViewport`, and `StretchViewport` all extend `ScalingViewport` with `Scaling.fit`, `Scaling.fill`, and `Scaling.stretch` respectively.

### ScreenViewport

Maps 1 world unit = 1 pixel (by default). World dimensions change with window size. Common for UI/Scene2D.

```java
ScreenViewport viewport = new ScreenViewport();
viewport.setUnitsPerPixel(0.5f);  // 1 world unit = 2 pixels (DPI scaling)
float upp = viewport.getUnitsPerPixel();
```

### ExtendViewport

Extends the world in one direction to fill the screen. Guarantees at least `minWorldWidth × minWorldHeight` is visible. With `maxWorldWidth`/`maxWorldHeight`, caps the extension.

### update() and apply()

```java
// In resize() — REQUIRED:
viewport.update(width, height);          // centerCamera defaults to false
viewport.update(width, height, true);    // true = center camera at (worldW/2, worldH/2)

// Before each render pass (when using multiple viewports):
viewport.apply();                        // centerCamera defaults to false
viewport.apply(true);                    // true = center camera
```

### The `centerCamera` Parameter — Critical

**`viewport.update(w, h, true)`** repositions the camera to `(worldWidth/2, worldHeight/2, 0)`, placing (0,0) at the bottom-left corner of the viewport.

**`viewport.update(w, h)` (no third arg / `false`)** does NOT move the camera. It stays at its current position — which defaults to (0,0) from Camera construction. This means the camera is centered at the origin, so the visible area spans from `(-halfW, -halfH)` to `(+halfW, +halfH)`. **Sprites placed at positive coordinates appear in the top-right quadrant only** — the classic "everything is offset" bug.

**Rule of thumb:** Pass `true` unless you are manually managing camera position (e.g., following a player).

### Key Viewport Methods

```java
Camera getCamera()
void setCamera(Camera camera)               // yes, setCamera() DOES exist

float getWorldWidth() / getWorldHeight()     // world-space dimensions
int getScreenX() / getScreenY()              // viewport position on screen (for letterbox offset)
int getScreenWidth() / getScreenHeight()     // viewport size on screen

Vector2 unproject(Vector2 screenCoords)      // screen → world (handles viewport offset)
Vector2 project(Vector2 worldCoords)         // world → screen
Vector3 unproject(Vector3 screenCoords)      // 3D variant
Vector3 project(Vector3 worldCoords)         // 3D variant
Ray getPickRay(float screenX, float screenY) // for 3D picking

// Gutter (black bar) queries
int getLeftGutterWidth() / getRightGutterWidth()
int getBottomGutterHeight() / getTopGutterHeight()
```

## Standard Setup Pattern

```java
public class MyGame extends ApplicationAdapter {
    OrthographicCamera camera;
    FitViewport viewport;
    SpriteBatch batch;

    @Override
    public void create() {
        camera = new OrthographicCamera();
        viewport = new FitViewport(800, 480, camera);
        batch = new SpriteBatch();
    }

    @Override
    public void render() {
        ScreenUtils.clear(0, 0, 0, 1);
        camera.update();                                  // MUST call every frame
        batch.setProjectionMatrix(camera.combined);       // MUST set before begin()
        batch.begin();
        // draw...
        batch.end();
    }

    @Override
    public void resize(int width, int height) {
        viewport.update(width, height, true);             // true = (0,0) at bottom-left
    }
}
```

## Multiple Viewports (Game + UI)

```java
OrthographicCamera gameCamera = new OrthographicCamera();
FitViewport gameViewport = new FitViewport(800, 480, gameCamera);

Stage stage = new Stage(new ScreenViewport());  // Stage creates its own camera

@Override
public void render() {
    ScreenUtils.clear(0, 0, 0, 1);

    // --- Game pass ---
    gameViewport.apply();                          // sets glViewport for game
    gameCamera.update();
    batch.setProjectionMatrix(gameCamera.combined);
    batch.begin();
    // draw game world...
    batch.end();

    // --- UI pass ---
    stage.getViewport().apply(true);               // sets glViewport for UI
    stage.act(Gdx.graphics.getDeltaTime());
    stage.draw();
}

@Override
public void resize(int width, int height) {
    gameViewport.update(width, height, true);
    stage.getViewport().update(width, height, true);
}
```

**You MUST call `viewport.apply()` before each render pass** when using multiple viewports. Each viewport sets the OpenGL viewport (`glViewport`) to its screen bounds. Without `apply()`, the second pass renders into the first viewport's bounds.

## Camera Follow Pattern

```java
// Snap follow (instant, can feel jerky)
camera.position.set(player.x, player.y, 0);

// Smooth follow (lerp)
float alpha = 0.1f;  // 0 = no movement, 1 = instant snap. Adjust to taste.
camera.position.x += (player.x - camera.position.x) * alpha;
camera.position.y += (player.y - camera.position.y) * alpha;

// Clamped to world bounds (prevent showing outside the map)
float halfW = camera.viewportWidth * camera.zoom / 2f;
float halfH = camera.viewportHeight * camera.zoom / 2f;
camera.position.x = MathUtils.clamp(camera.position.x, halfW, worldWidth - halfW);
camera.position.y = MathUtils.clamp(camera.position.y, halfH, worldHeight - halfH);

camera.update();  // AFTER all position changes
```

**Note on lerp alpha:** The pattern above uses a fixed alpha, which is framerate-dependent. For framerate-independent smoothing, use `alpha = 1 - (float)Math.pow(1 - speed, delta * 60)` or similar.

## Cross-References

- **SpriteBatch integration** (`batch.setProjectionMatrix(camera.combined)`) — see **libgdx-2d-rendering** skill
- **Input coordinate unprojection** — see **libgdx-input-handling** skill
- **Stage Viewport** — Stage has its own Viewport; see **libgdx-scene2d-ui** skill
- **3D rendering** with PerspectiveCamera + ModelBatch — see 3D rendering docs

## Common Mistakes

1. **Forgetting `camera.update()` after changing position/zoom** — The combined matrix is not recalculated until `update()` is called. Nothing moves or zooms on screen.
2. **Not passing `true` to `viewport.update(w, h, true)` in `resize()`** — Camera stays centered at (0,0). Sprites at positive coordinates render in the top-right quadrant only.
3. **Using screen coordinates for game logic without unprojecting** — `touchDown` gives screen pixels (Y-down, top-left origin). Always unproject through camera or viewport. See input handling skill.
4. **Passing `Vector2` to `camera.unproject()`** — `camera.unproject()` takes `Vector3`, not `Vector2`. Use `viewport.unproject(Vector2)` for the 2D convenience variant.
5. **Inventing `camera.setPosition()` or `camera.moveTo()`** — These methods do not exist. `position` is a public `final Vector3` field — modify it directly: `camera.position.set(x, y, 0)`.
6. **Creating a Viewport without passing your Camera** — The viewport creates a default `OrthographicCamera` internally. Your separate camera is disconnected from the viewport, and `batch.setProjectionMatrix(camera.combined)` won't match the viewport's transform.
7. **Not calling `viewport.apply()` with multiple viewports** — Each viewport must `apply()` before its render pass to set the correct `glViewport`. Without it, the second pass renders into the wrong screen region.
8. **Confusing `zoom` direction** — `zoom < 1` zooms **in** (less world visible), `zoom > 1` zooms **out** (more world visible). This is the opposite of what most developers expect.
9. **Using `Gdx.graphics.getWidth()/getHeight()` for world dimensions** — These return screen pixel dimensions, not world units. Use `viewport.getWorldWidth()/getWorldHeight()` or `camera.viewportWidth/viewportHeight` for world-space dimensions.
10. **Forgetting `batch.setProjectionMatrix(camera.combined)` before `batch.begin()`** — SpriteBatch uses a default pixel-coordinate projection. Without this call, your camera's position, zoom, and viewport are ignored. See 2D rendering skill.
11. **Not calling `viewport.update()` in `resize()`** — The viewport doesn't adapt to window size changes. Graphics appear stretched or clipped after resizing.
12. **Forgetting to multiply by `camera.zoom` when clamping position** — The effective visible area is `viewportWidth * zoom` × `viewportHeight * zoom`. Clamping without the zoom factor lets the camera show outside world bounds when zoomed out.
