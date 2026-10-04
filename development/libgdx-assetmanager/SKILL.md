---
name: libgdx-asset-manager
description: Use when writing libGDX Java/Kotlin code involving AssetManager — loading assets (Texture, TextureAtlas, Sound, Music, BitmapFont, Skin, Model, TiledMap, ParticleEffect, ShaderProgram, I18NBundle), async loading screens, reference counting, screen transitions, custom loaders, or FreeType font loading via AssetManager. Use when debugging assets not loading, double-dispose crashes, missing textures after Android resume, or loading screen patterns.
---

# libGDX AssetManager

Quick reference for `com.badlogic.gdx.assets.AssetManager`. Covers loading, retrieval, disposal, reference counting, loading screens, parameters, custom loaders, and error handling.

## Core Concepts

`load()` **queues** an asset. Nothing is loaded until `update()` or `finishLoading()` is called.

```
load() → queues request
update() → processes one step per call, returns true when ALL done
finishLoading() → blocks until ALL queued assets are loaded
finishLoadingAsset(name) → blocks until ONE specific asset is loaded, returns it
get() → retrieves a loaded asset (throws if not loaded)
unload() → decrements ref count, disposes at zero
dispose() → disposes ALL assets and kills the executor
```

**There is no `loadSync()` method.** Do not invent one.

## Constructors

```java
AssetManager manager = new AssetManager();                              // InternalFileHandleResolver, all default loaders
AssetManager manager = new AssetManager(resolver);                      // custom resolver, all default loaders
AssetManager manager = new AssetManager(resolver, false);               // custom resolver, NO default loaders
```

## Loading Assets

```java
// Queue assets (nothing loaded yet)
manager.load("texture.png", Texture.class);
manager.load("atlas.atlas", TextureAtlas.class);
manager.load("click.wav", Sound.class);
manager.load("theme.mp3", Music.class);
manager.load("font.fnt", BitmapFont.class);
manager.load("ui.json", Skin.class);

// With parameters
TextureLoader.TextureParameter param = new TextureLoader.TextureParameter();
param.minFilter = TextureFilter.Linear;
param.magFilter = TextureFilter.Linear;
param.genMipMaps = true;
manager.load("texture.png", Texture.class, param);
```

## Retrieving Assets

```java
// After loading is complete:
Texture tex = manager.get("texture.png", Texture.class);

// Without type (unchecked cast — less safe):
Texture tex = manager.get("texture.png");

// Non-throwing variant (returns null if not loaded):
Texture tex = manager.get("texture.png", Texture.class, false);

// Check first:
if (manager.isLoaded("texture.png")) {
    Texture tex = manager.get("texture.png", Texture.class);
}

// Get all assets of a type:
Array<Texture> textures = new Array<>();
manager.getAll(Texture.class, textures);
```

**Calling `get()` before the asset is loaded throws `GdxRuntimeException`.** Always use `isLoaded()`, `finishLoading()`, or check `update()` return value first.

## Loading Screen Pattern

```java
public class LoadingScreen implements Screen {
    private final MyGame game;
    private final AssetManager manager;

    public LoadingScreen(MyGame game) {
        this.game = game;
        this.manager = game.manager;

        // Queue game assets
        manager.load("game.atlas", TextureAtlas.class);
        manager.load("music.mp3", Music.class);
        manager.load("click.wav", Sound.class);
    }

    @Override
    public void render(float delta) {
        ScreenUtils.clear(0, 0, 0, 1);

        if (manager.update()) {
            // ALL assets loaded — transition
            game.setScreen(new GameScreen(game));
            return;
        }

        float progress = manager.getProgress();  // 0.0 to 1.0
        // Draw progress bar using progress
    }
    // ...
}
```

**`update()`**: Processes one loading step per call. Returns `true` when all queued assets are done. Must be called every frame.

**`update(int millis)`**: Loops `update()` for up to `millis` milliseconds. May block longer than specified depending on the current asset. On GWT/WebGL, degrades to a single `update()` call (no threading).

**`getProgress()`**: Returns 0.0–1.0. Accounts for partial progress within the current asset, not just completed asset count.

**`finishLoading()`**: Blocks the render thread until ALL queued assets are loaded. Only use for small loads or splash screens.

**`finishLoadingAsset(String fileName)`**: Blocks until the specific asset is loaded and returns it. Useful for loading the loading screen's own assets before entering the async loop:

```java
// Block-load the loading screen's own background
manager.load("loading-bg.png", Texture.class);
Texture bg = manager.finishLoadingAsset("loading-bg.png");

// Now queue game assets (these load asynchronously via update())
manager.load("game.atlas", TextureAtlas.class);
```

## Default Loaders (registered automatically)

| Type | Loader | Async | Parameter Class |
|---|---|---|---|
| `Texture` | `TextureLoader` | Yes | `TextureLoader.TextureParameter` |
| `TextureAtlas` | `TextureAtlasLoader` | Yes | `TextureAtlasLoader.TextureAtlasParameter` |
| `BitmapFont` | `BitmapFontLoader` | Yes | `BitmapFontLoader.BitmapFontParameter` |
| `Sound` | `SoundLoader` | Yes | (empty — no fields) |
| `Music` | `MusicLoader` | Yes | (empty — no fields) |
| `Skin` | `SkinLoader` | Yes | `SkinLoader.SkinParameter` |
| `Pixmap` | `PixmapLoader` | Yes | (empty — no fields) |
| `ParticleEffect` | `ParticleEffectLoader` | **No** (sync) | `ParticleEffectLoader.ParticleEffectParameter` |
| `I18NBundle` | `I18NBundleLoader` | Yes | `I18NBundleLoader.I18NBundleParameter` |
| `ShaderProgram` | `ShaderProgramLoader` | Yes | `ShaderProgramLoader.ShaderProgramParameter` |
| `Cubemap` | `CubemapLoader` | Yes | — |
| `Model` | `G3dModelLoader` / `ObjLoader` | Yes | `ModelLoader.ModelParameters` |
| `PolygonRegion` | `PolygonRegionLoader` | — | `PolygonRegionLoader.PolygonRegionParameters` |

## Loaders Requiring Manual Registration

### TiledMap

```java
manager.setLoader(TiledMap.class, new TmxMapLoader(new InternalFileHandleResolver()));

BaseTiledMapLoader.Parameters params = new BaseTiledMapLoader.Parameters();
params.textureMinFilter = TextureFilter.Linear;
params.textureMagFilter = TextureFilter.Linear;
manager.load("map.tmx", TiledMap.class, params);
```

`AtlasTmxMapLoader` is an alternative that loads tiles from a TextureAtlas (requires `atlas` property in the TMX file).

### FreeType Fonts via AssetManager

Two loaders must be registered:

```java
FileHandleResolver resolver = new InternalFileHandleResolver();
manager.setLoader(FreeTypeFontGenerator.class, new FreeTypeFontGeneratorLoader(resolver));
manager.setLoader(BitmapFont.class, ".ttf", new FreetypeFontLoader(resolver));
```

The `.ttf` suffix ensures only keys ending in `.ttf` route to `FreetypeFontLoader`. The default `BitmapFontLoader` still handles `.fnt` keys.

```java
FreetypeFontLoader.FreeTypeFontLoaderParameter param = new FreetypeFontLoader.FreeTypeFontLoaderParameter();
param.fontFileName = "fonts/arial.ttf";       // actual file on disk
param.fontParameters.size = 24;
param.fontParameters.minFilter = TextureFilter.Linear;
param.fontParameters.magFilter = TextureFilter.Linear;
manager.load("arial-24.ttf", BitmapFont.class, param);  // key (must end in .ttf)
```

**The key is a virtual identifier** — it does not need to match the real filename. `fontFileName` points to the actual `.ttf` file. This enables loading multiple sizes of the same font:

```java
param16.fontFileName = "fonts/arial.ttf";
param16.fontParameters.size = 16;
manager.load("arial-16.ttf", BitmapFont.class, param16);

param32.fontFileName = "fonts/arial.ttf";
param32.fontParameters.size = 32;
manager.load("arial-32.ttf", BitmapFont.class, param32);
```

**The parameter is mandatory.** Passing `null` throws `RuntimeException`.

## Key Parameter Classes

### TextureLoader.TextureParameter

| Field | Type | Default |
|---|---|---|
| `minFilter` | `TextureFilter` | `Nearest` |
| `magFilter` | `TextureFilter` | `Nearest` |
| `wrapU` | `TextureWrap` | `ClampToEdge` |
| `wrapV` | `TextureWrap` | `ClampToEdge` |
| `genMipMaps` | `boolean` | `false` |
| `format` | `Pixmap.Format` | `null` |
| `texture` | `Texture` | `null` (for reloading into existing texture) |

### BitmapFontLoader.BitmapFontParameter

| Field | Type | Default |
|---|---|---|
| `flip` | `boolean` | `false` |
| `genMipMaps` | `boolean` | `false` |
| `minFilter` | `TextureFilter` | `Nearest` |
| `magFilter` | `TextureFilter` | `Nearest` |
| `atlasName` | `String` | `null` (use atlas for font texture) |

### SkinLoader.SkinParameter

| Field | Type | Default |
|---|---|---|
| `textureAtlasPath` | `String` (final) | `null` |
| `resources` | `ObjectMap<String, Object>` (final) | `null` |

If `textureAtlasPath` is null, Skin automatically loads `<skinname>.atlas` (same directory, same base name). The `resources` map injects objects (e.g., FreeType-generated fonts) into the Skin before JSON parsing:

```java
ObjectMap<String, Object> resources = new ObjectMap<>();
resources.put("default-font", myGeneratedFont);
manager.load("ui.json", Skin.class, new SkinLoader.SkinParameter(resources));
```

### ModelLoader.ModelParameters

| Field | Type | Default |
|---|---|---|
| `textureParameter` | `TextureLoader.TextureParameter` | `Linear` filter, `Repeat` wrap |

### ParticleEffectLoader.ParticleEffectParameter

| Field | Type | Default |
|---|---|---|
| `atlasFile` | `String` | `null` (load images from effect file's directory) |
| `atlasPrefix` | `String` | `null` |
| `imagesDir` | `FileHandle` | `null` |

## Dependencies

AssetManager resolves dependencies automatically. When you load a `TextureAtlas`, it loads all referenced `Texture` files. When you load a `Skin`, it loads its `TextureAtlas`. When you load a `BitmapFont`, it loads its texture page(s).

**Do NOT manually load or dispose dependency resources.** The AssetManager owns them.

```java
// WRONG — double-managing the atlas
manager.load("game.atlas", TextureAtlas.class);     // loads atlas + its textures
manager.load("sheet.png", Texture.class);            // if sheet.png is IN the atlas, this creates a conflict

// RIGHT — let the atlas manage its textures
manager.load("game.atlas", TextureAtlas.class);
// Access textures through the atlas, not directly
```

## Reference Counting

Loading the same asset path and type twice increments its reference count:

```java
manager.load("click.wav", Sound.class);   // ref count will be 1
manager.load("click.wav", Sound.class);   // ref count will be 2 (not loaded twice)
manager.finishLoading();

manager.getReferenceCount("click.wav");   // returns 2

manager.unload("click.wav");              // ref count → 1 (still alive)
manager.unload("click.wav");              // ref count → 0 (disposed)
```

**Loading the same path with a DIFFERENT type throws `GdxRuntimeException` immediately.**

`unload()` behavior:
- Decrements ref count. If ref count reaches 0, disposes the asset.
- Recursively unloads dependencies (each checks its own ref count).
- Can also cancel assets that are queued but not yet loaded.
- Throws `GdxRuntimeException` if the asset is not found.

## Disposal

| Method | Effect | Manager usable after? |
|---|---|---|
| `unload(name)` | Decrements ref count for one asset; disposes at 0 | Yes |
| `clear()` | Disposes ALL loaded assets, clears queue | Yes |
| `dispose()` | Calls `clear()` + kills async executor | **No** |

**Where to call `dispose()`:** In `Game.dispose()`, not in `Screen.dispose()`. Disposing the AssetManager in a Screen destroys all assets, breaking other screens.

```java
public class MyGame extends Game {
    public AssetManager manager;

    @Override
    public void create() {
        manager = new AssetManager();
        setScreen(new LoadingScreen(this));
    }

    @Override
    public void dispose() {
        getScreen().dispose();
        manager.dispose();      // disposes ALL loaded assets
    }
}
```

## Error Handling

```java
manager.setErrorListener(new AssetErrorListener() {
    @Override
    public void error(AssetDescriptor asset, Throwable throwable) {
        Gdx.app.error("Assets", "Failed to load: " + asset.fileName, throwable);
    }
});
```

When an asset fails during `update()`:
1. The failed task is removed.
2. Dependencies loaded for the failed asset are unloaded.
3. **All remaining tasks in the current task stack are cleared.**
4. If an `AssetErrorListener` is set: `error()` is called. Loading continues (future `update()` calls process remaining queued assets).
5. If NO listener is set: **throws `GdxRuntimeException`**, crashing the app.

Always set an error listener in production.

## Custom Loaders

```java
// SynchronousAssetLoader — everything on render thread
public class JsonDataLoader extends SynchronousAssetLoader<JsonData, JsonDataLoader.Params> {
    public JsonDataLoader(FileHandleResolver resolver) { super(resolver); }

    @Override
    public JsonData load(AssetManager manager, String fileName, FileHandle file, Params parameter) {
        return new JsonData(file.readString());
    }

    @Override
    public Array<AssetDescriptor> getDependencies(String fileName, FileHandle file, Params parameter) {
        return null;  // no dependencies
    }

    static public class Params extends AssetLoaderParameters<JsonData> {}
}

// Register
manager.setLoader(JsonData.class, new JsonDataLoader(new InternalFileHandleResolver()));
```

`setLoader(type, suffix, loader)` registers a loader for a specific file suffix. The longest matching suffix wins. Pass `null` for suffix to register as the default loader for that type.

### AsynchronousAssetLoader

Two abstract methods: `loadAsync()` (worker thread, no GL) and `loadSync()` (render thread, GL available). Temporary state between these two methods must be nulled at the start of `loadAsync()` to prevent stale data from a previous load cycle.

## Android Resume

```java
Texture.setAssetManager(manager);
```

Call this once after creating the AssetManager. On Android resume, managed textures loaded via AssetManager are reloaded on a separate thread. Without this call, the default managed texture mechanism still works but uses the render thread.

## FileHandleResolver

| Resolver | Resolves to |
|---|---|
| `InternalFileHandleResolver` (default) | `Gdx.files.internal()` |
| `ExternalFileHandleResolver` | `Gdx.files.external()` |
| `LocalFileHandleResolver` | `Gdx.files.local()` |
| `AbsoluteFileHandleResolver` | `Gdx.files.absolute()` |
| `ClasspathFileHandleResolver` | `Gdx.files.classpath()` |
| `PrefixFileHandleResolver` | Prepends prefix, delegates to wrapped resolver |
| `ResolutionFileResolver` | Selects resolution-specific folder based on screen size |

## Common Mistakes

1. **Calling `get()` before loading is complete** — `load()` only queues. You must call `update()` until it returns `true`, or use `finishLoading()`/`finishLoadingAsset()`, before calling `get()`.
2. **Inventing `loadSync()`** — This method does not exist on AssetManager. Use `finishLoadingAsset(fileName)` to block on a single asset.
3. **Disposing assets manually AND via AssetManager** — Calling `texture.dispose()` on an AssetManager-owned asset corrupts internal state. Always use `manager.unload()` instead.
4. **Disposing AssetManager in Screen.dispose()** — This destroys all assets across all screens. Dispose AssetManager only in `Game.dispose()`.
5. **Using `finishLoading()` for large asset sets** — Blocks the render thread, causing ANR on Android. Use `update()` in `render()` for async loading.
6. **Forgetting `update()` entirely** — Calling `load()` then `get()` without any `update()` or `finishLoading()` in between. Nothing is loaded yet.
7. **Manually loading dependency resources** — Loading a texture that belongs to a TextureAtlas via a separate `load()` call creates a duplicate. Let the AssetManager resolve dependencies.
8. **Not setting an error listener** — Without one, a single failed asset crashes the app via `GdxRuntimeException`.
9. **Making AssetManager static** — On Android, static fields survive Activity restarts, causing stale references to disposed native resources. Use an instance field on your Game class.
10. **Forgetting to register FreeType loaders** — Both `FreeTypeFontGeneratorLoader` and `FreetypeFontLoader` must be registered. The load key must end in `.ttf`. The `FreeTypeFontLoaderParameter` is mandatory (not optional).
11. **Forgetting to register TmxMapLoader** — `TiledMap` has no default loader. You must call `setLoader(TiledMap.class, new TmxMapLoader(...))` before loading `.tmx` files.
12. **Calling `unload()` on an asset that was never loaded** — Throws `GdxRuntimeException`. Check with `contains()` or `isLoaded()` first if unsure.
