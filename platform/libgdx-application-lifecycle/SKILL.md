---
name: libgdx-application-lifecycle
description: Use when writing a libGDX ApplicationListener or ApplicationAdapter, structuring a game's main class, or debugging lifecycle issues like missing disposal, initialization crashes, or incorrect pause/resume behavior. Use when asking where to put initialization code, how to get delta time, or which types need dispose().
---

# libGDX Application Lifecycle

Reference for ApplicationListener, ApplicationAdapter, lifecycle method order, frame-independent updates, resource disposal, and platform-specific pause/resume behavior.

## ApplicationListener Interface

```java
public interface ApplicationListener {
    void create();             // App created — OpenGL context now available
    void resize(int w, int h); // Window/viewport resized
    void render();             // Called every frame (update + draw combined)
    void pause();              // App losing focus / going to background
    void resume();             // App regaining focus / returning to foreground
    void dispose();            // App shutting down — release all resources
}
```

**There is no `update()` method.** All game logic and drawing happen in `render()`.

## ApplicationAdapter (Use This)

`ApplicationAdapter` implements `ApplicationListener` with empty defaults. Extend it and override only what you need — avoids boilerplate empty methods.

```java
// YES — extend ApplicationAdapter
public class MyGame extends ApplicationAdapter { ... }

// NO — don't implement ApplicationListener directly unless you need all 6 methods
public class MyGame implements ApplicationListener { ... }
```

## Lifecycle Order

```
create() → resize(w,h) → [render() loop] → pause() → dispose()
                          ↕
                   pause() ↔ resume()
```

**Startup:** `create()` → `resize(w, h)` → `render()` ...
**Exit:** `pause()` → `dispose()`

On Android, `dispose()` may **not** be called if the OS kills the process while backgrounded. Save critical state in `pause()`, not `dispose()`.

## Initialization: create(), Not the Constructor

**All GPU/audio/file initialization must happen inside `create()`.** The OpenGL context and libGDX subsystems (`Gdx.graphics`, `Gdx.audio`, `Gdx.files`, etc.) do not exist until `create()` is called. Constructing a `Texture`, `SpriteBatch`, or any GL-dependent object as a field initializer or in the constructor will crash.

```java
// WRONG — crashes: no GL context at field-init time
public class MyGame extends ApplicationAdapter {
    SpriteBatch batch = new SpriteBatch();   // CRASH
    Texture img = new Texture("pic.png");    // CRASH
}

// RIGHT — create() has a valid GL context
public class MyGame extends ApplicationAdapter {
    SpriteBatch batch;
    Texture img;

    @Override
    public void create() {
        batch = new SpriteBatch();
        img = new Texture("pic.png");
    }
}
```

## render() = Update + Draw

There is no separate `update()` callback. Combine logic and rendering in `render()`:

```java
@Override
public void render() {
    // 1. Delta time for frame-independent movement
    float dt = Gdx.graphics.getDeltaTime();  // seconds since last frame

    // 2. Update
    x += 100 * dt;  // 100 pixels/second regardless of frame rate

    // 3. Draw — ScreenUtils.clear() is the modern shorthand (since 1.10.0)
    //    replacing the verbose Gdx.gl.glClearColor() + Gdx.gl.glClear() pattern
    ScreenUtils.clear(0, 0, 0, 1);
    batch.begin();
    batch.draw(img, x, 0);
    batch.end();
}
```

`getDeltaTime()` is on **`Gdx.graphics`**, not `Gdx.app`.

## pause() / resume() — Platform Differences

| Event | Desktop (LWJGL3) | Android | iOS (RoboVM) |
|---|---|---|---|
| Window minimized / Home button | `pause()` fires | `pause()` fires | `pause()` fires |
| Window loses focus (Alt+Tab) | **Nothing** — render continues | — | — |
| Incoming call / screen off | — | `pause()` fires | `pause()` fires |
| render() during pause | **Continues running** | **Stops entirely** | **Stops entirely** |
| GL context on pause | **Retained** | **Destroyed** — managed resources auto-reloaded | **Retained** |
| dispose() on kill | Called | **May not be called** | Called |

**Desktop:** `pause()` only fires on **iconification**, not on focus loss. `render()` keeps running even when iconified — if you have network timers or other continuous work in `render()`, it won't stop on desktop. Check the pause state explicitly if needed.

**Android:** The render loop **stops entirely** during pause. Any work in `render()` (heartbeats, timers, network pings) ceases. Use a background thread or Android service for work that must continue. The GL context is destroyed during pause; libGDX automatically reloads *managed* resources on resume. Only raw, unmanaged GL handles need manual recreation.

**iOS (RoboVM):** Behaves like Android for pause triggers (home button, incoming call, app switcher), but the GL context is **retained** like desktop. `render()` stops during pause.

## resize() on Android — configChanges Gotcha

On Android, device rotation triggers `resize()` **only** if `android:configChanges` includes `orientation|screenSize` in the manifest. Without it, Android destroys and recreates the Activity — a full `dispose()` → `create()` cycle, not a `resize()`. The Android backend skill covers manifest setup.

## Gdx.app.exit()

`Gdx.app.exit()` schedules a **graceful shutdown** — it is NOT immediate. Code after `exit()` still executes in the current frame. The shutdown triggers `pause()` → `dispose()`. On Android, it calls `finish()` on the Activity.

```java
if (Gdx.input.isKeyJustPressed(Input.Keys.ESCAPE)) {
    Gdx.app.exit();
    return;  // necessary — exit() is non-blocking
}
```

## Disposal: Types That Need dispose()

These types allocate native memory or GPU resources outside the JVM heap. The garbage collector **cannot** free them — you must call `dispose()` explicitly, typically in your `ApplicationAdapter.dispose()`.

| Type | Resource held |
|---|---|
| `Texture` | GPU texture |
| `SpriteBatch` | Mesh + shader |
| `BitmapFont` | Texture(s) |
| `ShaderProgram` | GL shader program |
| `FrameBuffer` | GL framebuffer + texture |
| `Sound` | Native audio buffer |
| `Music` | Native audio stream |
| `Pixmap` | Native pixel buffer |
| `TextureAtlas` | Texture(s) |
| `Skin` | Textures + fonts |
| `Stage` | SpriteBatch (if owns it) |

**Rule of thumb:** if you created it, dispose it. Dispose in reverse order of creation when possible. In non-trivial projects, `AssetManager` handles disposal via `unload()` and `clear()` — prefer it over manual tracking.

## Lifecycle Debugging with Gdx.app.log()

```java
Gdx.app.setLogLevel(Application.LOG_DEBUG); // in create()

Gdx.app.log("Game", "info message");    // LOG_INFO level
Gdx.app.debug("Game", "debug message"); // LOG_DEBUG level
Gdx.app.error("Game", "error message"); // LOG_ERROR level
```

**Log level constants** (`com.badlogic.gdx.Application`):

| Constant | Value | Shows |
|---|---|---|
| `LOG_NONE` | 0 | Nothing |
| `LOG_ERROR` | 1 | error() only |
| `LOG_INFO` | 2 | error() + log() |
| `LOG_DEBUG` | 3 | All messages |

Default level is `LOG_INFO`. Output goes to stdout (desktop), LogCat (Android), or NSLog (iOS).

## Minimal Working Example

```java
import com.badlogic.gdx.ApplicationAdapter;
import com.badlogic.gdx.Gdx;
import com.badlogic.gdx.graphics.Color;
import com.badlogic.gdx.utils.ScreenUtils;

public class MyGame extends ApplicationAdapter {
    @Override
    public void create() {
        Gdx.app.log("MyGame", "create()");
    }

    @Override
    public void render() {
        // ScreenUtils.clear() replaces the old glClearColor()+glClear() pattern (since 1.10.0)
        ScreenUtils.clear(Color.CORAL);
    }

    @Override
    public void dispose() {
        Gdx.app.log("MyGame", "dispose()");
    }
}
```

## Common Mistakes

1. **Initializing GL objects in constructor or as field initializers** — No OpenGL context exists yet. Move to `create()`.
2. **Looking for an `update()` method** — It doesn't exist. Put logic in `render()`.
3. **Using `Gdx.app.getDeltaTime()`** — Wrong location. It's `Gdx.graphics.getDeltaTime()`.
4. **Forgetting to dispose native resources** — Texture, SpriteBatch, BitmapFont, Sound, Music, etc. all leak if not disposed. Use `AssetManager` for non-trivial projects.
5. **Implementing `ApplicationListener` directly** — Use `ApplicationAdapter` to avoid empty method stubs.
6. **Assuming desktop pause() fires on focus loss** — On LWJGL3, only iconification (minimize) triggers it. Focus loss alone does nothing.
7. **Manually reloading textures on Android resume** — libGDX reloads managed resources automatically. Only raw GL handles need manual recreation.
8. **Assuming render() keeps running on Android during pause** — The render loop stops entirely. Use a background thread or Android service for work that must continue.
9. **Treating Gdx.app.exit() as immediate** — It schedules shutdown. Code after `exit()` still executes in the current frame.
10. **Missing configChanges in Android manifest** — Without `orientation|screenSize` in `android:configChanges`, rotation destroys and recreates the Activity instead of calling `resize()`.
