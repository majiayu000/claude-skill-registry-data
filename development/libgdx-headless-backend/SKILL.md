---
name: libgdx-headless-backend
description: Use when writing libGDX Java/Kotlin code that runs without a display — dedicated game servers, CI/testing of non-rendering logic, procedural generation at build time, or headless simulation. Use when asking about HeadlessApplication, HeadlessApplicationConfiguration, updatesPerSecond, or what libGDX APIs work without OpenGL.
---

# libGDX Headless Backend

Reference for running libGDX without a display, audio, or input — for servers, CI/testing, procedural generation, and headless simulation. Lives in the `gdx-backend-headless` module.

## Setup

```java
import com.badlogic.gdx.backends.headless.HeadlessApplication;
import com.badlogic.gdx.backends.headless.HeadlessApplicationConfiguration;

public class ServerLauncher {
    public static void main(String[] args) {
        HeadlessApplicationConfiguration config = new HeadlessApplicationConfiguration();
        config.updatesPerSecond = 20;  // render() called 20 times/sec
        new HeadlessApplication(new MyServerListener(), config);
    }
}
```

**Dependency (Gradle):**
```gradle
implementation "com.badlogicgames.gdx:gdx-backend-headless:$gdxVersion"
implementation "com.badlogicgames.gdx:gdx-platform:$gdxVersion:natives-desktop"
```

## HeadlessApplicationConfiguration

The only important field is **`updatesPerSecond`** — an `int` controlling how often `render()` is called.

| `updatesPerSecond` value | Behavior | Use case |
|---|---|---|
| `20` | render() called 20 times/sec | Game server at 20 tick rate |
| `60` (default) | render() called 60 times/sec | **Wastes CPU on a server — always set explicitly** |
| `0` | Never sleep between calls (run as fast as possible) | Batch processing, benchmarking |
| Negative (e.g. `-1`) | render() is NOT called at all | One-shot tasks that do all work in `create()` |

**CRITICAL — use `updatesPerSecond`, not the old float field:**

```java
// ✅ CORRECT — updatesPerSecond is an int
config.updatesPerSecond = 20;

// ❌ WRONG — renderInterval was removed; this will not compile on 1.9.14+
// config.renderInterval = 1 / 20f;   // DO NOT USE
```

**For servers:** Always set `updatesPerSecond` to match your desired tick rate. The default (60) runs at 60fps which wastes CPU on a headless server.

**For one-shot tasks** (generate data then exit): Do all work in `create()` and call `Gdx.app.exit()`. Set `updatesPerSecond = -1` so `render()` is never called, or leave it at default — if your `create()` calls `exit()`, it won't matter.

## What Works in Headless

These APIs are fully functional without OpenGL:

- **ApplicationListener lifecycle** — `create()`, `render()`, `resize()`, `pause()`, `resume()`, `dispose()` all fire normally
- **File I/O** — `Gdx.files.internal()`, `.local()`, `.external()`, `.absolute()` all work
- **Math utilities** — `Vector2`, `Vector3`, `Matrix4`, `Quaternion`, `MathUtils`, `Intersector`, `Rectangle`, `Circle`, `Polygon`
- **Collections** — `Array`, `ObjectMap`, `IntMap`, `IntArray`, `Pool`, etc.
- **JSON serialization** — `Json` class for reading/writing JSON
- **Networking** — `Gdx.net` for HTTP requests
- **Preferences** — `Gdx.app.getPreferences("name")` for key-value storage
- **Application utilities** — `Gdx.app.postRunnable()`, `Gdx.app.log()`, `Gdx.app.getType()`
- **Color** — `Color` class (it's just data, no GPU)

## What Does NOT Work

**`Gdx.gl` is `null`.** Any call touching OpenGL will throw `NullPointerException`.

These classes/APIs **will crash or silently fail** in headless mode:

| Category | Broken classes | Reason |
|---|---|---|
| **Rendering** | `Texture`, `TextureRegion`, `TextureAtlas`, `SpriteBatch`, `ShapeRenderer`, `FrameBuffer`, `Mesh`, `Shader` | Require OpenGL context |
| **Fonts** | `BitmapFont` | Loads a Texture internally |
| **UI** | `Skin`, `Stage`, all Scene2D widgets | Skin loads textures; Stage needs a SpriteBatch |
| **Screen size** | `Gdx.graphics.getWidth()` / `getHeight()` | Returns `0` — there is no screen |
| **Audio** | `Gdx.audio.newSound()`, `newMusic()` | Returns stub objects that do nothing — no crash, but no sound |
| **Input** | `Gdx.input.getX()`, `isKeyPressed()`, etc. | Returns stub values — no crash, but no real input |

**Key traps:**
- `BitmapFont` looks like a data class but it loads a `Texture` internally — **it will crash headless**.
- `Skin` loads a `TextureAtlas` — **it will crash headless**.
- `Gdx.graphics.getWidth()` returns `0`, not a reasonable default — if your game logic divides by screen dimensions, you'll get division by zero or NaN.

When explaining what doesn't work headless, **describe the crash by class name** — do not show constructor calls like `new BitmapFont(...)` or `new Skin(...)` as negative examples. Users copy code from examples regardless of warnings.

## Common Use Cases

### Dedicated Game Server
```java
public class GameServer extends ApplicationAdapter {
    private GameWorld world;

    @Override
    public void create() {
        world = new GameWorld();
        Gdx.app.log("Server", "Started");
    }

    @Override
    public void render() {
        float delta = Gdx.graphics.getDeltaTime();
        world.update(delta);       // shared game logic with client
        // network: broadcast state to connected clients
    }

    @Override
    public void dispose() {
        Gdx.app.log("Server", "Shutting down");
    }
}

// Launcher:
HeadlessApplicationConfiguration config = new HeadlessApplicationConfiguration();
config.updatesPerSecond = 20;  // 20 tick server
new HeadlessApplication(new GameServer(), config);
```

### Procedural Generation at Build Time
```java
public class MapGenerator extends ApplicationAdapter {
    @Override
    public void create() {
        // Generate map using libGDX math
        Array<Vector2> points = new Array<>();
        for (int i = 0; i < 100; i++) {
            points.add(new Vector2(MathUtils.random(1000f), MathUtils.random(1000f)));
        }

        // Serialize and write
        Json json = new Json();
        Gdx.files.local("generated-map.json").writeString(json.prettyPrint(points), false);
        Gdx.app.log("Gen", "Map written");

        Gdx.app.exit();  // done — shut down
    }

    @Override public void render() {}  // never called if create() exits
}

// Launcher:
HeadlessApplicationConfiguration config = new HeadlessApplicationConfiguration();
config.updatesPerSecond = -1;  // don't call render() — all work done in create()
new HeadlessApplication(new MapGenerator(), config);
```

### Unit Testing Non-Rendering Logic
```java
// In your test setup — initialize headless once:
HeadlessApplicationConfiguration config = new HeadlessApplicationConfiguration();
new HeadlessApplication(new ApplicationAdapter() {}, config);

// Now libGDX types work in tests:
Vector2 v = new Vector2(3, 4);
assertEquals(5f, v.len(), 0.001f);

Json json = new Json();
String s = json.toJson(myGameState);
GameState loaded = json.fromJson(GameState.class, s);
```

This initializes the libGDX environment so `Vector2`, `MathUtils`, `Json`, and other utility classes function. You do **not** need Mockito to mock GL — just don't call anything that needs GL.

## Common Mistakes

1. **Using the wrong config field** — The field is `updatesPerSecond` (an `int`), not a float interval. For 20 ticks/sec: `config.updatesPerSecond = 20`.
2. **Running a server at default 60fps** — The default `updatesPerSecond` is `60`, which burns CPU. Always set it explicitly for servers.
3. **Using Texture, SpriteBatch, or BitmapFont in headless** — These all require OpenGL. `Gdx.gl` is `null` in headless mode, so any GL call throws `NullPointerException`.
4. **Using Skin or Scene2D in headless** — `Skin` loads a `TextureAtlas` (needs GL). `Stage` creates a `SpriteBatch` (needs GL). Neither works headless.
5. **Dividing by `Gdx.graphics.getWidth()`** — Returns `0` in headless. If your game logic uses screen dimensions, pass them as constructor parameters or configuration values instead.
6. **Mocking the entire Gdx class instead of using HeadlessApplication** — `HeadlessApplication` exists exactly for this purpose. It initializes `Gdx.files`, `Gdx.app`, `Gdx.net`, etc. properly. You don't need to mock them.
7. **Forgetting `Gdx.app.exit()` in one-shot tasks** — The application loop keeps running after `create()`. Call `Gdx.app.exit()` when your generation/export is done, or the process will hang.
