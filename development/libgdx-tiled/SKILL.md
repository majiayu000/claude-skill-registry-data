---
name: libgdx-tiled-maps
description: Use when writing libGDX Java/Kotlin code involving Tiled maps — TmxMapLoader, TiledMap, TiledMapTileLayer, OrthogonalTiledMapRenderer, object layers, MapProperties, unitScale, or collision extraction from map data. Use when debugging wrong tile positions, missing layers, object coordinate issues, or map not rendering.
---

# libGDX Tiled Maps

Quick reference for libGDX Tiled map integration (`com.badlogic.gdx.maps.*`). Covers loading, TiledMap structure, renderers, unit scale, object layers, properties, animated tiles, and collision extraction.

## Loading

### TmxMapLoader (synchronous)

```java
// Direct loading (uses InternalFileHandleResolver by default)
TiledMap map = new TmxMapLoader().load("maps/level1.tmx");

// With parameters
TmxMapLoader.Parameters params = new TmxMapLoader.Parameters(); // 1.12.x
// BaseTiledMapLoader.Parameters params = new BaseTiledMapLoader.Parameters(); // 1.13.1+
params.textureMinFilter = Texture.TextureFilter.Linear;
params.textureMagFilter = Texture.TextureFilter.Linear;
TiledMap map = new TmxMapLoader().load("maps/level1.tmx", params);
```

### AssetManager Loading (preferred)

```java
assetManager.setLoader(TiledMap.class, new TmxMapLoader(new InternalFileHandleResolver()));
assetManager.load("maps/level1.tmx", TiledMap.class);
// ... assetManager.update() in render loop ...
TiledMap map = assetManager.get("maps/level1.tmx", TiledMap.class);
```

When using `AssetManager`, disposal is handled by `assetManager.unload("maps/level1.tmx")`.

### AtlasTmxMapLoader

Loads tiles from a `TextureAtlas` instead of separate tileset images. Reduces draw calls.

Requirements:
- TMX file must have a map-level property named `atlas` with the path to the `.atlas` file
- Atlas regions must be named after tilesets with indexes local to the tileset (not global tile IDs)
- Atlas must NOT use strip-whitespace or rotation

```java
// Direct
TiledMap map = new AtlasTmxMapLoader().load("maps/level1.tmx");

// Via AssetManager
assetManager.setLoader(TiledMap.class, new AtlasTmxMapLoader(new InternalFileHandleResolver()));
```

**Gotcha:** Throws `GdxRuntimeException("The map is missing the 'atlas' property")` if the TMX lacks the `atlas` map property.

### Parameters

| Field | Type | Default | Purpose |
|---|---|---|---|
| `flipY` | boolean | `true` | Converts Tiled y-down to libGDX y-up |
| `convertObjectToTileSpace` | boolean | `false` | Divides object coords by tile dimensions |
| `generateMipMaps` | boolean | `false` | Generate mipmaps for tileset textures |
| `textureMinFilter` | TextureFilter | `Nearest` | Min filter for tileset textures |
| `textureMagFilter` | TextureFilter | `Nearest` | Mag filter for tileset textures |

In 1.12.x: `BaseTmxMapLoader.Parameters` (or `TmxMapLoader.Parameters` which extends it).
In 1.13.1+: `BaseTiledMapLoader.Parameters`. `TmxMapLoader.Parameters` no longer exists — update imports on upgrade.

## TiledMap Structure

```
TiledMap (extends Map, implements Disposable)
├── getLayers() → MapLayers
│   ├── TiledMapTileLayer — tile grid data
│   │   └── Cell[][] → TiledMapTile
│   ├── MapLayer — object layers
│   │   └── MapObjects → MapObject subclasses
│   ├── TiledMapImageLayer — image layers
│   └── MapGroupLayer — group layers (has nested getLayers())
├── getTileSets() → TiledMapTileSets
│   └── TiledMapTileSet → TiledMapTile (by int ID)
├── getProperties() → MapProperties
└── dispose()
```

### Accessing Layers

```java
// By index
MapLayer layer = map.getLayers().get(0);

// By name — returns null if not found (does NOT throw)
MapLayer layer = map.getLayers().get("ground");

// MUST cast to TiledMapTileLayer for tile operations
TiledMapTileLayer tileLayer = (TiledMapTileLayer) map.getLayers().get("ground");

// Filter by type (single-arg allocates new Array each call)
Array<TiledMapTileLayer> tileLayers = map.getLayers().getByType(TiledMapTileLayer.class);

// Reuse array to avoid allocation
Array<TiledMapTileLayer> fill = new Array<>();
map.getLayers().getByType(TiledMapTileLayer.class, fill);
```

### Tile Layer → Cell → Tile

```java
TiledMapTileLayer layer = (TiledMapTileLayer) map.getLayers().get("ground");

int cols = layer.getWidth();      // map width in tiles
int rows = layer.getHeight();     // map height in tiles
int tw   = layer.getTileWidth();  // tile width in pixels
int th   = layer.getTileHeight(); // tile height in pixels

// getCell() takes TILE coordinates (not pixels). Returns null if empty or out of bounds.
TiledMapTileLayer.Cell cell = layer.getCell(tileX, tileY);
if (cell != null) {
    TiledMapTile tile = cell.getTile();
    TextureRegion region = tile.getTextureRegion();
    MapProperties tileProps = tile.getProperties();

    boolean flipH = cell.getFlipHorizontally();
    boolean flipV = cell.getFlipVertically();
    int rotation = cell.getRotation(); // Cell.ROTATE_0, ROTATE_90, ROTATE_180, ROTATE_270
}
```

**Converting world position to tile coordinates:**

```java
// If unitScale = 1f (camera in pixel units):
int tileX = (int) (worldX / layer.getTileWidth());
int tileY = (int) (worldY / layer.getTileHeight());

// If unitScale = 1/tileWidth (camera in tile units):
int tileX = (int) worldX;
int tileY = (int) worldY;
```

### TiledMapTile Interface

```java
int getId();
TextureRegion getTextureRegion();
float getOffsetX();                // float, not int
float getOffsetY();
MapProperties getProperties();
MapObjects getObjects();           // tile collision shapes from Tiled editor
TiledMapTile.BlendMode getBlendMode(); // NONE or ALPHA
```

Implementations: `StaticTiledMapTile`, `AnimatedTiledMapTile`.

## Renderers

### Class Hierarchy

```
MapRenderer (interface, com.badlogic.gdx.maps)
└── TiledMapRenderer (interface, extends MapRenderer)
      └── BatchTiledMapRenderer (abstract, implements TiledMapRenderer + Disposable)
            ├── OrthogonalTiledMapRenderer
            ├── IsometricTiledMapRenderer       (experimental)
            ├── IsometricStaggeredTiledMapRenderer
            └── HexagonalTiledMapRenderer
```

### Constructor Overloads (same for all four renderers)

```java
// Creates internal SpriteBatch — renderer owns it, dispose() releases it
new OrthogonalTiledMapRenderer(map)                      // unitScale = 1.0f
new OrthogonalTiledMapRenderer(map, unitScale)

// Uses external Batch — renderer does NOT dispose it
new OrthogonalTiledMapRenderer(map, batch)               // unitScale = 1.0f
new OrthogonalTiledMapRenderer(map, unitScale, batch)
```

The `batch` parameter accepts any `Batch` implementation (the interface), not just `SpriteBatch`.

### Render Loop

```java
renderer.setView(camera);             // MUST call before render()
renderer.render();                     // renders all layers

// Selective layer rendering (by index) for sprite interleaving:
int[] bgLayers = {0, 1};
int[] fgLayers = {2, 3};
renderer.setView(camera);
renderer.render(bgLayers);
batch.setProjectionMatrix(camera.combined);
batch.begin();
// ... draw player sprites ...
batch.end();
renderer.render(fgLayers);
```

**`setView()` overloads:**
- `setView(OrthographicCamera camera)` — computes projection + view bounds from camera
- `setView(Matrix4 projection, float x, float y, float width, float height)` — explicit bounds

**`getBatch()`** returns the renderer's `Batch` (return type is `Batch` interface, not `SpriteBatch`).

### renderObject() Is Empty

`BatchTiledMapRenderer.renderObject(MapObject)` is intentionally a no-op. **Object layers are not rendered visually.** They exist only as data for collision, spawn points, triggers, etc. Tile objects placed in object layers will NOT appear on screen.

## Unit Scale

`unitScale` controls how tileset pixels map to world units: `worldUnits = pixels * unitScale`.

| unitScale | Meaning | Camera setup example |
|---|---|---|
| `1f` | 1 pixel = 1 world unit | `camera.setToOrtho(false, 800, 480)` |
| `1/32f` | 32 pixels = 1 world unit | `camera.setToOrtho(false, 25, 15)` — sees 25x15 tiles |
| `1/16f` | 16 pixels = 1 world unit | `camera.setToOrtho(false, 50, 30)` |

```java
float unitScale = 1 / 32f;
OrthogonalTiledMapRenderer renderer = new OrthogonalTiledMapRenderer(map, unitScale);

OrthographicCamera camera = new OrthographicCamera();
camera.setToOrtho(false, 30, 20); // sees 30x20 tiles
```

**When unitScale != 1f, object layer coordinates are still in pixels by default.** Scale them yourself or set `convertObjectToTileSpace = true` in loader parameters.

## Object Layers

### MapObject Subclasses

| Class | Accessor | Returns |
|---|---|---|
| `RectangleMapObject` | `getRectangle()` | `Rectangle` |
| `EllipseMapObject` | `getEllipse()` | `Ellipse` |
| `CircleMapObject` | `getCircle()` | `Circle` |
| `PolygonMapObject` | `getPolygon()` | `Polygon` |
| `PolylineMapObject` | `getPolyline()` | `Polyline` |
| `PointMapObject` | `getPoint()` | `Vector2` |
| `TiledMapTileMapObject` | `getTile()` | `TiledMapTile` (extends `TextureMapObject`) |

All inherit from `MapObject` which provides `getName()`, `getProperties()`, `getColor()`, `getOpacity()`, `isVisible()`.

### Extracting Objects

```java
MapLayer collisionLayer = map.getLayers().get("collision");
MapObjects objects = collisionLayer.getObjects();

for (MapObject object : objects) {
    if (object instanceof RectangleMapObject) {
        Rectangle rect = ((RectangleMapObject) object).getRectangle();
        // rect.x, rect.y = bottom-left in pixels (with default flipY=true)
    } else if (object instanceof PolygonMapObject) {
        float[] verts = ((PolygonMapObject) object).getPolygon().getTransformedVertices();
    } else if (object instanceof PolylineMapObject) {
        float[] verts = ((PolylineMapObject) object).getPolyline().getTransformedVertices();
    } else if (object instanceof EllipseMapObject) {
        Ellipse ellipse = ((EllipseMapObject) object).getEllipse();
    }
}

// Filter by type (2-arg overload reuses array):
Array<RectangleMapObject> rects = new Array<>();
objects.getByType(RectangleMapObject.class, rects);
```

### Y-Axis and Coordinate Space

Tiled uses y-down (origin top-left). libGDX uses y-up (origin bottom-left). With default `flipY = true`, the loader converts coordinates automatically:

- Tile layers: cells are in correct y-up order
- Rectangles/Ellipses: `y = mapHeightPx - tiledY - objectHeight` (bottom-left corner)
- Polygons/Polylines: vertex Y values are negated
- Object coordinates are in **pixels** unless `convertObjectToTileSpace = true`

**Do NOT manually flip Y when `flipY = true` (the default).** Coordinates are already converted.

### Box2D Collision Extraction

```java
float scale = 1 / 32f; // match renderer unitScale

for (RectangleMapObject rmo : objects.getByType(RectangleMapObject.class)) {
    Rectangle rect = rmo.getRectangle();

    BodyDef bodyDef = new BodyDef();
    bodyDef.type = BodyDef.BodyType.StaticBody;
    // rect (x,y) is bottom-left; Box2D setAsBox uses center + half-dimensions
    bodyDef.position.set(
        (rect.x + rect.width / 2) * scale,
        (rect.y + rect.height / 2) * scale
    );

    PolygonShape shape = new PolygonShape();
    shape.setAsBox(rect.width / 2 * scale, rect.height / 2 * scale);

    Body body = world.createBody(bodyDef);
    body.createFixture(shape, 0f);
    shape.dispose();
}
```

## Properties

`MapProperties` appears on maps, layers, tiles, and objects.

```java
MapProperties props = object.getProperties();

// Raw (returns Object, null if missing)
Object val = props.get("name");

// Typed (ClassCastException if wrong type, null if missing)
String name = props.get("name", String.class);

// Typed with default — signature: get(key, defaultValue, clazz)
int hp     = props.get("hp", 100, Integer.class);
float speed = props.get("speed", 1.0f, Float.class);
boolean solid = props.get("solid", false, Boolean.class);

props.containsKey("name");  // boolean
props.put("custom", 42);
```

**Tiled type mapping:** int→`Integer`, float→`Float`, bool→`Boolean`, string→`String`, color→`Color`.

The loader also stores standard attributes on objects: `x`, `y`, `width`, `height`, `type`, `id`, `rotation`.

## Animated Tiles

Animations defined in Tiled's tileset editor are loaded automatically — no manual setup needed.

```java
// Manual creation (rare — usually auto-loaded from TMX):
// Uniform duration (interval in seconds, converted to ms internally)
new AnimatedTiledMapTile(0.25f, frameTiles);  // Array<StaticTiledMapTile>

// Per-frame durations (in milliseconds)
new AnimatedTiledMapTile(intervals, frameTiles); // IntArray, Array<StaticTiledMapTile>
```

**Gotchas:**
- All animated tiles share a **static** clock. The renderer calls `AnimatedTiledMapTile.updateAnimationBaseTime()` in `beginRender()`. You cannot offset individual tile animations.
- `setTextureRegion()`, `setOffsetX()`, `setOffsetY()` throw `GdxRuntimeException` on animated tiles.
- Frame tiles must be `StaticTiledMapTile` instances.

## Disposal

```java
map.dispose();       // disposes owned tileset textures
renderer.dispose();  // disposes batch ONLY if renderer created it (ownsBatch)

// Via AssetManager:
assetManager.unload("maps/level1.tmx"); // handles everything
```

**Do NOT dispose tileset textures separately.** TmxMapLoader's textures are owned by TiledMap — calling `texture.dispose()` on them causes use-after-free when `map.dispose()` runs.

If you passed an external `Batch` to the renderer constructor, dispose it yourself — the renderer won't.

## Common Mistakes

1. **Using `layer.getTile(x, y)`** — Does not exist. Use `layer.getCell(x, y).getTile()`. Always null-check `getCell()` — returns `null` for empty or out-of-bounds cells.
2. **Passing pixel coordinates to `getCell()`** — Takes tile coordinates (column, row), not pixel positions. Divide world position by tile dimensions first.
3. **Forgetting `unitScale` in the renderer constructor** — Default is `1.0f` (pixels). Pass `1f / tilePixelSize` if your camera operates in tile/world units.
4. **Not calling `setView(camera)` before `render()`** — Renderer needs the camera's projection matrix. Without it, nothing renders or stale view bounds are used.
5. **Assuming `getLayers().get("name")` returns a typed layer** — Returns `MapLayer`. Cast to `TiledMapTileLayer` for `getCell()` access.
6. **Expecting object layers to render visually** — `renderObject()` is intentionally empty. Object layers are data-only. Tile objects in object layers are NOT drawn.
7. **Mixing up pixel and tile coordinates for objects** — Default `convertObjectToTileSpace = false` means `getRectangle()` etc. return **pixel** coordinates. Scale by `unitScale` to match your world.
8. **Disposing tileset textures separately** — TmxMapLoader textures are owned by TiledMap. Call only `map.dispose()`.
9. **Manually flipping Y on object coordinates** — With default `flipY = true`, coordinates are already converted. Flipping again puts objects in the wrong position.
10. **Using gzip/zlib TMX encoding on GWT** — Compressed tile data is not supported on the HTML5 backend. Use CSV or uncompressed base64.
11. **Allocating `getByType()` arrays every frame** — Single-arg `getByType(Class)` allocates a new `Array` each call. Cache at load time or use the two-arg overload.
12. **Not disposing the renderer** — If the renderer created its own internal `SpriteBatch`, you must call `renderer.dispose()` to release it.
