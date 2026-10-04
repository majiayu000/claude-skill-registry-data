---
name: libgdx-lwjgl3-desktop
description: Use when writing libGDX Java/Kotlin code targeting the LWJGL3 desktop backend — Lwjgl3Application launcher, Lwjgl3ApplicationConfiguration, window management, fullscreen toggle, multi-window, file access (internal/local/external on desktop), desktop-specific pause/resume behavior, cursor customization, or clipboard access. Use when debugging wrong file paths, FPS/vsync configuration, or pause() not firing on focus loss.
---

# libGDX LWJGL3 Desktop Backend

Reference for the LWJGL3 desktop launcher, window configuration, fullscreen/windowed management, desktop lifecycle behavior, file access, and common gotchas.

**LWJGL3 is the current desktop backend.** The old `LwjglApplication` / `LwjglApplicationConfiguration` classes are the legacy LWJGL2 backend — do NOT use them. Always use `Lwjgl3Application` and `Lwjgl3ApplicationConfiguration`.

## Launcher Class

The desktop launcher lives in the **desktop module**, not in core. It contains the `main()` method.

```java
package com.example.game.lwjgl3;

import com.badlogic.gdx.backends.lwjgl3.Lwjgl3Application;
import com.badlogic.gdx.backends.lwjgl3.Lwjgl3ApplicationConfiguration;
import com.example.game.MyGame;

public class DesktopLauncher {
    public static void main(String[] args) {
        Lwjgl3ApplicationConfiguration config = new Lwjgl3ApplicationConfiguration();
        config.setTitle("My Game");
        config.setWindowedMode(1280, 720);
        config.useVsync(true);
        config.setForegroundFPS(60);
        config.setWindowIcon("icons/icon128.png", "icons/icon32.png", "icons/icon16.png"); // JPEG, PNG, or BMP
        config.setIdleFPS(15); // reduce CPU when unfocused/iconified
        new Lwjgl3Application(new MyGame(), config);
    }
}
```

**Never put `main()` in the core module.** Core is cross-platform; the launcher is platform-specific.

## Configuration Quick Reference

| Method | Purpose |
|---|---|
| `setTitle(String)` | Window title bar text |
| `setWindowedMode(w, h)` | Initial window size in pixels |
| `useVsync(boolean)` | Sync frame rate to monitor refresh rate |
| `setForegroundFPS(int)` | Software cap on render loop FPS |
| `setWindowIcon(String...)` | Window/taskbar icons — JPEG, PNG, or BMP |
| `setIdleFPS(int)` | Render rate when unfocused/iconified (default 60) |
| `setResizable(boolean)` | Allow user to resize window |
| `setDecorated(boolean)` | Show/hide title bar and borders |
| `setFullscreenMode(DisplayMode)` | Start in fullscreen |
| `setBackBufferConfig(r,g,b,a,depth,stencil,samples)` | Color/depth/stencil bits and MSAA |
| `pauseWhenLostFocus(boolean)` | When true, fires pause()/resume() on focus loss/gain (not just iconify). Default: false |
| `setWindowListener(Lwjgl3WindowListener)` | Window event callbacks (focus, iconify, file drop) |

## setForegroundFPS() vs useVsync()

These are independent controls:

- **`useVsync(true)`** — Syncs buffer swaps to the monitor's refresh rate (e.g., 60Hz). Eliminates screen tearing. Hardware-driven.
- **`setForegroundFPS(n)`** — Software cap: sleeps between frames to limit render() calls to n per second. Works independently of vsync.

Use both together, or either alone:
- `useVsync(true)` + `setForegroundFPS(60)` — Vsync for smoothness, FPS cap as a safety net
- `useVsync(false)` + `setForegroundFPS(120)` — No vsync, software-limited to 120fps
- `useVsync(true)` + `setForegroundFPS(0)` — Vsync only, no software cap

**`setForegroundFPS(0)` means unlimited — the render loop spins as fast as possible, using 100% CPU.** Always set a reasonable cap unless you have a specific reason not to.

**`setIdleFPS(n)`** — Controls the render rate when the window is **unfocused or iconified**. Default is 60. Since `render()` continues running even when the window is minimized, use `setIdleFPS(15)` or similar to reduce background CPU usage without stopping the loop entirely.

## Back Buffer Configuration

`setBackBufferConfig(r, g, b, a, depth, stencil, samples)` controls the color depth, depth buffer, stencil buffer, and MSAA samples for the OpenGL context. The default config has **no stencil buffer**. If you use `FrameBuffer` with stencil operations, you must request stencil bits here — otherwise stencil writes silently fail:

```java
// Request 8-bit stencil buffer (default has 0)
config.setBackBufferConfig(8, 8, 8, 8, 16, 8, 0);
//                         R  G  B  A  depth stencil MSAA
```

## Fullscreen and Windowed Mode

**Start in fullscreen:**
```java
config.setFullscreenMode(Lwjgl3ApplicationConfiguration.getDisplayMode());
```

**Toggle at runtime:**
```java
// To fullscreen
Gdx.graphics.setFullscreenMode(Gdx.graphics.getDisplayMode());

// To windowed
Gdx.graphics.setWindowedMode(1280, 720);
```

**Monitor enumeration:**
```java
Graphics.Monitor[] monitors = Lwjgl3ApplicationConfiguration.getMonitors();
Graphics.DisplayMode[] modes = Lwjgl3ApplicationConfiguration.getDisplayModes(monitors[0]);
```

## Desktop Lifecycle: pause() / resume()

| Event | What happens |
|---|---|
| Window **minimized/iconified** | `pause()` fires |
| Window **restored** from taskbar | `resume()` fires |
| Window **loses focus** (Alt+Tab) | **Nothing** — `pause()` does NOT fire |
| Window **closed** | `pause()` → `dispose()` |
| render() while iconified | **Continues running** |

**Key difference from Android:** On desktop, `pause()` fires ONLY on iconification (minimize), NOT on focus loss. The render loop keeps running even when the window is iconified or unfocused. To detect focus loss, use `Lwjgl3WindowListener` (see below). To receive `pause()`/`resume()` on focus loss (matching Android behavior), call `config.pauseWhenLostFocus(true)`. This is `false` by default.

## Window Listener

`Lwjgl3WindowListener` provides callbacks for window events that `ApplicationListener` doesn't cover. Register via `config.setWindowListener()`. Use `Lwjgl3WindowAdapter` to override only what you need:

```java
config.setWindowListener(new Lwjgl3WindowAdapter() {
    @Override public void focusLost() { paused = true; }
    @Override public void focusGained() { paused = false; }
});
```

Available callbacks: `focusLost()`, `focusGained()`, `iconified(boolean)`, `maximized(boolean)`, `filesDropped(String[])`, `closeRequested()` (return false to cancel close).

`filesDropped()` enables drag-and-drop file support — a desktop-only feature useful for editors and tools. **Do NOT use raw GLFW calls** (e.g., `glfwSetWindowFocusCallback`) — use `Lwjgl3WindowListener` instead.

## Multi-Window Support

LWJGL3 supports multiple windows — each gets its own `ApplicationListener`:

```java
Lwjgl3Application app = (Lwjgl3Application) Gdx.app;
Lwjgl3WindowConfiguration windowConfig = new Lwjgl3WindowConfiguration();
windowConfig.setTitle("Debug Window");
windowConfig.setWindowedMode(400, 300);
app.newWindow(new MyDebugListener(), windowConfig);
```

All windows update on the same thread, sequentially. `Gdx.graphics` / `Gdx.input` point to whichever window is currently being updated. This is desktop-only — do not use in cross-platform core code.

## File Access on Desktop

| Method | Reads from | Writable | Notes |
|---|---|---|---|
| `Gdx.files.internal("x")` | `assets/` on classpath | No | Bundled game assets |
| `Gdx.files.local("x")` | Working directory | Yes | **Depends on where JVM launched from** |
| `Gdx.files.external("x")` | User home directory | Yes | `~/<x>` on Linux/macOS, `C:\Users\<name>\<x>` on Windows |

**Working directory gotcha:** `Gdx.files.local()` resolves relative to the JVM working directory. In IntelliJ or Gradle run configurations, you must explicitly set the working directory to the `assets/` folder (or core project root) — otherwise local file paths will resolve to unexpected locations.

## Clipboard

```java
// Read
String text = Gdx.app.getClipboard().getContents();
// Write
Gdx.app.getClipboard().setContents("copied text");
```

## Custom Cursor

```java
// System cursor
Gdx.graphics.setSystemCursor(Graphics.Cursor.SystemCursor.Crosshair);

// Custom cursor from Pixmap
Pixmap pm = new Pixmap(Gdx.files.internal("cursor.png"));
Cursor cursor = Gdx.graphics.newCursor(pm, hotspotX, hotspotY);
Gdx.graphics.setCursor(cursor);
pm.dispose(); // Pixmap can be disposed after creating cursor
```

## Common Mistakes

1. **Using `LwjglApplication` / `LwjglApplicationConfiguration`** — Those are the legacy LWJGL2 backend. Always use `Lwjgl3Application` / `Lwjgl3ApplicationConfiguration`.
2. **Putting `main()` in the core module** — The launcher class with `main()` belongs in the desktop module. Core is cross-platform.
3. **Assuming focus loss triggers `pause()`** — On LWJGL3 desktop, only iconification (minimize) triggers `pause()`. Alt+Tab / focus loss does nothing.
4. **Setting `setForegroundFPS(0)` without knowing the effect** — Zero means unlimited. The CPU will spin at 100%. Always set a cap.
5. **Expecting `Gdx.files.local()` to find files in the assets folder** — `local()` uses the working directory, which may not be `assets/`. Set the working directory in your IDE/Gradle run config, or use `internal()` for read-only assets.
6. **Assuming `render()` stops when the window is minimized** — On desktop, `render()` continues running even when iconified. Check pause state explicitly if you need to stop updates.
7. **Using LWJGL2-era `Display` or `Monitor` APIs** — Use `Lwjgl3ApplicationConfiguration.getMonitors()` and `getDisplayModes()` for monitor enumeration.
8. **Not setting `setIdleFPS()` and wondering why the game uses 100% CPU when minimized** — `render()` keeps running at `setForegroundFPS` rate even when iconified. Use `setIdleFPS(15)` or similar to reduce background CPU usage.
9. **Using raw GLFW calls or polling to detect focus loss instead of `Lwjgl3WindowListener`** — libGDX provides `focusLost()` and `focusGained()` callbacks via `Lwjgl3WindowAdapter`. Don't go behind the framework with `GLFW.glfwSetWindowFocusCallback()` or direct LWJGL3 imports.
