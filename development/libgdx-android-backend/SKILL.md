---
name: libgdx-android-backend
description: Use when writing libGDX Java/Kotlin code targeting Android — AndroidApplication launcher, AndroidApplicationConfiguration, AndroidManifest.xml setup, Android lifecycle mapping to libGDX, OpenGL context loss on pause, file access (internal/local/external with permissions), Android input (back button, accelerometer, on-screen keyboard), screen density, safe insets/notch, or GL thread posting. Use when debugging black textures after resume, Activity recreation on rotation, or missing file permissions.
---

# libGDX Android Backend

Reference for Android-specific launcher setup, manifest configuration, lifecycle mapping, file access, input handling, screen density, safe insets, and threading.

## Launcher Setup

`AndroidApplication` extends `Activity`. Call `initialize()` in `onCreate()`:

```java
public class AndroidLauncher extends AndroidApplication {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        AndroidApplicationConfiguration config = new AndroidApplicationConfiguration();
        config.useAccelerometer = true;   // default true — set false to save battery
        config.useCompass = false;        // default true — set false to save battery
        config.useGyroscope = false;      // default false
        config.useImmersiveMode = true;   // hides nav/status bars — libGDX handles it fully
        config.numSamples = 2;            // MSAA anti-aliasing (0 = off)
        config.useWakelock = true;        // keeps screen on during gameplay
        config.useGL30 = false;           // set true for GL ES 3.0 (Gdx.gl30); null if false
        initialize(new MyGame(), config);
    }
}
```

**Do NOT add manual immersive mode code** (deprecated `SYSTEM_UI_FLAG_*` constants, `onWindowFocusChanged()`, visibility listeners). `config.useImmersiveMode = true` is sufficient — libGDX manages the system UI internally. Never show working `SYSTEM_UI_FLAG` code examples, even as a "what not to do" — users will copy them.

For Fragment-based hosting, use `AndroidFragmentApplication` instead of `AndroidApplication`. It extends `Fragment` and works with `FragmentActivity`.

## AndroidManifest.xml

```xml
<activity
    android:name=".AndroidLauncher"
    android:configChanges="keyboard|keyboardHidden|orientation|screenSize"
    android:screenOrientation="landscape"
    android:exported="true">
    <intent-filter>
        <action android:name="android.intent.action.MAIN" />
        <category android:name="android.intent.category.LAUNCHER" />
    </intent-filter>
</activity>
```

**`android:configChanges` is critical.** Without `orientation|screenSize`, Android destroys and recreates the Activity on rotation — a full `dispose()` → `create()` cycle with GL context loss. With it, libGDX handles rotation via `resize()`.

### Permissions

| Permission | When needed |
|---|---|
| `WRITE_EXTERNAL_STORAGE` | `Gdx.files.external()` — also needs **runtime permission** on API 23+ |
| `INTERNET` | Any networking (HttpURLConnection, WebSocket, etc.) |
| `VIBRATE` | Haptic feedback via `Gdx.input.vibrate()` |
| `WAKE_LOCK` | Added automatically when `config.useWakelock = true` |

**Runtime permissions (API 23+):** libGDX has no cross-platform permission API. Request in the launcher:

```java
// In AndroidLauncher (any class extending AndroidApplication works)
if (Build.VERSION.SDK_INT >= 23) {
    requestPermissions(new String[]{Manifest.permission.WRITE_EXTERNAL_STORAGE}, REQUEST_CODE);
}
// Result arrives in onRequestPermissionsResult() — check grantResults before using external()
```

## Lifecycle Mapping

| Android | libGDX | What happens |
|---|---|---|
| `onCreate()` | `create()` | App initialization |
| `onResume()` | `resume()` | App returns to foreground |
| `onPause()` | `pause()` | App goes to background |
| `finish()` / system kill | `dispose()` | App shutting down |

**Use libGDX's `ApplicationListener` callbacks (create/render/pause/resume/dispose), NOT Android Activity lifecycle methods directly.** Override `onCreate()` only for the launcher's `initialize()` call.

**The render loop stops entirely during pause on Android.** Any work in `render()` — timers, heartbeats, network pings — ceases when the app is backgrounded. Use a background thread or Android service for work that must continue.

### OpenGL Context Loss on Pause

**On Android, the OpenGL context IS destroyed when the app is paused.** This is not limited to older devices — it happens on ALL Android versions.

- **Managed resources** (Texture, SpriteBatch, ShaderProgram, BitmapFont, FrameBuffer loaded via libGDX APIs) are **automatically reloaded** by libGDX on resume. You do not need to manually reload them.
- **Custom non-managed GL resources** (raw GL handles created via `Gdx.gl.glGenTexture()`, `Gdx.gl.glCreateProgram()`, etc.) **must be recreated manually** — register an invalidation callback or recreate in `resume()`.

```java
// WRONG — unnecessary manual reloading
@Override
public void resume() {
    texture = new Texture("sprite.png");  // libGDX already reloaded it
}

// RIGHT — only recreate raw GL handles if you have any
@Override
public void resume() {
    if (customGLHandle != 0) {
        customGLHandle = createRawGLResource();  // only for non-managed resources
    }
}
```

**Save critical game state in `pause()`, not `dispose()`.** On Android, `dispose()` may not be called if the OS kills the backgrounded process.

## File Access

| FileType | Maps to | Permission needed |
|---|---|---|
| `Gdx.files.internal("file")` | Android `assets/` folder | None (read-only, bundled with APK) |
| `Gdx.files.local("file")` | `Context.getFilesDir()` (app-internal storage) | None (private to app) |
| `Gdx.files.external("file")` | App-specific external storage (`getExternalFilesDir()`) | `WRITE_EXTERNAL_STORAGE` + runtime permission on API 23+ |
| `Gdx.files.absolute("/path")` | Literal filesystem path | Discouraged on Android — use `local()` or `external()` |

```java
// Save game — use local(), not external() (no permission needed)
FileHandle saveFile = Gdx.files.local("savegame.json");
saveFile.writeString(json, false);

// Load game
if (Gdx.files.local("savegame.json").exists()) {
    String json = Gdx.files.local("savegame.json").readString();
}

// Read bundled asset (from android/assets/)
String levelData = Gdx.files.internal("levels/level1.json").readString();
```

**Do NOT use desktop-style paths** like `"./saves/game.sav"` or `System.getProperty("user.home")` on Android. These don't map to accessible storage.

## Input

### Back Button

By default, the Android back button exits the Activity. To intercept it:

```java
// In create() or show()
Gdx.input.setCatchKey(Input.Keys.BACK, true);

// In your InputProcessor.keyDown()
@Override
public boolean keyDown(int keycode) {
    if (keycode == Input.Keys.BACK) {
        // show pause menu, go to previous screen, etc.
        return true;
    }
    return false;
}
```

**`setCatchBackKey(boolean)` is deprecated.** Use `setCatchKey(Input.Keys.BACK, true)` instead.

### Touch Input

Touch is the primary input on Android. Multi-touch uses the pointer index (0 = first finger, 1 = second, etc.):

```java
// Polling
if (Gdx.input.isTouched(0)) {
    float x = Gdx.input.getX(0);
    float y = Gdx.input.getY(0);
}
```

### Accelerometer / Gyroscope

Must be enabled in `AndroidApplicationConfiguration` (accelerometer is enabled by default):

```java
float ax = Gdx.input.getAccelerometerX();  // tilt left/right
float ay = Gdx.input.getAccelerometerY();  // tilt forward/back
float az = Gdx.input.getAccelerometerZ();  // up/down (gravity)
```

### On-Screen Keyboard

```java
// Show/hide soft keyboard
Gdx.input.setOnscreenKeyboardVisible(true);

// Dialog-based text input (shows native Android dialog)
Gdx.input.getTextInput(new Input.TextInputListener() {
    @Override
    public void input(String text) { /* user entered text */ }
    @Override
    public void canceled() { /* user cancelled */ }
}, "Title", "default value", "hint");
```

## Screen Density

`Gdx.graphics.getWidth()`/`getHeight()` returns the actual pixel resolution, which varies widely across Android devices. Use `getDensity()` to convert between density-independent units (dp) and pixels:

```java
float density = Gdx.graphics.getDensity();
// 1.0 = mdpi (160 dpi), 1.5 = hdpi, 2.0 = xhdpi, 3.0 = xxhdpi, 4.0 = xxxhdpi
float pixelSize = 48 * density;  // 48dp → pixels
```

## Safe Insets (Notch / Cutout)

libGDX provides safe inset values directly — **no need for a custom platform interface** or raw Android `DisplayCutout` API:

```java
int top = Gdx.graphics.getSafeInsetTop();
int bottom = Gdx.graphics.getSafeInsetBottom();
int left = Gdx.graphics.getSafeInsetLeft();
int right = Gdx.graphics.getSafeInsetRight();
```

Available since libGDX 1.9.10+. Returns pixels. Use these to offset UI elements away from notches and rounded corners.

## Threading

**`render()` runs on the GL thread.** All OpenGL calls must happen on this thread.

To run code on the GL thread from another thread (e.g., network callback, Android UI thread):

```java
// From a network thread:
Gdx.app.postRunnable(new Runnable() {
    @Override
    public void run() {
        // Runs on the GL thread next frame — safe to create textures, update game state
        Pixmap pixmap = new Pixmap(downloadedBytes, 0, downloadedBytes.length);
        texture = new Texture(pixmap);
        pixmap.dispose();
    }
});
```

**Never create or modify GL resources from a non-GL thread.** This causes silent corruption or crashes.

## Gradle / Android Studio

The `android` module has its own `build.gradle` with the Android plugin:

```groovy
android {
    compileSdkVersion 34
    minSdkVersion 19        // libGDX minimum
    targetSdkVersion 34

    defaultConfig {
        applicationId "com.yourpackage.game"
    }
}

dependencies {
    implementation project(":core")
    implementation "com.badlogicgames.gdx:gdx-backend-android:$gdxVersion"
    natives "com.badlogicgames.gdx:gdx-platform:$gdxVersion:natives-armeabi-v7a"
    natives "com.badlogicgames.gdx:gdx-platform:$gdxVersion:natives-arm64-v8a"
    natives "com.badlogicgames.gdx:gdx-platform:$gdxVersion:natives-x86"
    natives "com.badlogicgames.gdx:gdx-platform:$gdxVersion:natives-x86_64"
}
```

**Note:** The exact dependency syntax depends on the project generator (gdx-liftoff vs older gdx-setup). The `natives` configuration above is from the standard template — newer generators may use different syntax.

## Common Mistakes

1. **Adding manual immersive mode code** — `config.useImmersiveMode = true` is all you need. Don't add `SYSTEM_UI_FLAG_*` listeners or `onWindowFocusChanged()` overrides.
2. **Thinking GL context loss is only on old devices** — It happens on ALL Android versions when the app is paused. Managed resources are auto-reloaded; only raw GL handles need manual recreation.
3. **Manually reloading managed textures in `resume()`** — libGDX handles this. Creating new `Texture` objects in `resume()` leaks the originals.
4. **Using Activity lifecycle methods instead of libGDX callbacks** — Use `create()`/`render()`/`pause()`/`resume()`/`dispose()`, not `onStart()`/`onResume()`/`onPause()`.
5. **Missing `configChanges` in manifest** — Without `keyboard|keyboardHidden|orientation|screenSize`, rotation destroys and recreates the Activity instead of calling `resize()`.
6. **Using `Gdx.files.external()` without permissions** — Needs `WRITE_EXTERNAL_STORAGE` in manifest AND runtime permission request on API 23+. Prefer `Gdx.files.local()` for save data.
7. **Using desktop-style file paths on Android** — `"./saves/"`, `System.getProperty("user.home")` don't work. Use `Gdx.files.local()` or `Gdx.files.internal()`.
8. **Creating GL resources off the GL thread** — Network callbacks and Android UI callbacks are NOT on the GL thread. Use `Gdx.app.postRunnable()` to marshal work to the GL thread.
9. **Using deprecated `setCatchBackKey()`** — Use `Gdx.input.setCatchKey(Input.Keys.BACK, true)` instead.
10. **Saving critical state only in `dispose()`** — On Android, `dispose()` may not be called if the OS kills the process. Save in `pause()`.
11. **Building a custom platform interface for safe insets** — libGDX has `Gdx.graphics.getSafeInsetTop()` etc. built in (since 1.9.10+). No need for `DisplayCutout` API directly.
