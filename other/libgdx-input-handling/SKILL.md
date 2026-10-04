---
name: libgdx-input-handling
description: Use when writing libGDX Java/Kotlin code involving input handling — InputProcessor, InputAdapter, InputMultiplexer, GestureDetector, polling (isKeyPressed/isTouched), coordinate unprojection, or Android back/menu key catching. Use when debugging missed input events, wrong click positions, or UI not receiving touches.
---

# libGDX Input Handling

Reference for polling vs event-driven input, InputProcessor, InputMultiplexer, GestureDetector, coordinate unprojection, and platform input quirks.

## Polling vs Event-Driven

**Polling** — check input state each frame in `render()`:

```java
// isKeyPressed = true EVERY frame while held → continuous actions (movement)
if (Gdx.input.isKeyPressed(Input.Keys.W)) player.y += speed * delta;
if (Gdx.input.isKeyPressed(Input.Keys.SPACE)) fireBullet();

// isKeyJustPressed = true ONLY on the first frame the key goes down → one-shot actions
if (Gdx.input.isKeyJustPressed(Input.Keys.ESCAPE)) togglePause();
if (Gdx.input.isKeyJustPressed(Input.Keys.SPACE)) jump(); // fires once per press

// Touch/mouse
if (Gdx.input.isTouched()) {
    int screenX = Gdx.input.getX();   // screen coords, Y-down
    int screenY = Gdx.input.getY();
}
if (Gdx.input.isTouched(1)) { /* second finger */ }
if (Gdx.input.justTouched()) { /* first frame of touch only */ }
```

**`isKeyPressed` vs `isKeyJustPressed`:** Using `isKeyJustPressed` for movement causes stuttering (only moves one frame per key press). Using `isKeyPressed` for a one-shot action like jumping causes repeated firing every frame the key is held.

**Event-driven** — implement `InputProcessor` and register it:

```java
Gdx.input.setInputProcessor(myProcessor);
```

Use polling for continuous actions (movement, held buttons). Use event-driven for discrete actions (clicks, key presses, gestures).

## InputProcessor Interface

All 9 methods — every one returns `boolean`:

```java
public interface InputProcessor {
    boolean keyDown(int keycode);                                          // physical key pressed
    boolean keyUp(int keycode);                                            // physical key released
    boolean keyTyped(char character);                                      // Unicode character generated
    boolean touchDown(int screenX, int screenY, int pointer, int button);  // finger/mouse down
    boolean touchUp(int screenX, int screenY, int pointer, int button);    // finger/mouse up
    boolean touchCancelled(int screenX, int screenY, int pointer, int button); // touch cancelled by OS
    boolean touchDragged(int screenX, int screenY, int pointer);           // move while touching
    boolean mouseMoved(int screenX, int screenY);                          // mouse move (desktop only)
    boolean scrolled(float amountX, float amountY);                        // scroll wheel / touchpad
}
```

**Return value:** `true` = event consumed (stops propagation in InputMultiplexer). `false` = event not handled (passes to next processor).

**`keyDown` vs `keyTyped`:** `keyDown(int keycode)` receives `Input.Keys` constants — use for game controls (movement, actions). `keyTyped(char character)` receives the Unicode character produced — use for text input. **Never compare `keyTyped`'s char against `Input.Keys` constants** (e.g., `character == Input.Keys.A` compares a char against int 29, which is silently wrong).

**`touchDragged` vs `mouseMoved`:** `touchDragged` only fires while a finger/button is held down. `mouseMoved` fires on mouse movement with no buttons pressed (desktop only). Do not use `touchDragged` for hover/mouseover detection — it won't fire without a touch.

**`scrolled` direction:** `amountY` is **positive for scroll-down, negative for scroll-up** (on most platforms). Values are typically -1 or +1 per scroll notch, not pixel deltas. Common mistake: inverting the sign when implementing zoom (scroll-up should zoom in, and `amountY` is negative when scrolling up).

**There is NO `onClick()`, `onTap()`, or `onKeyPress()` method.** Clicks are `touchDown` + `touchUp`. For tap detection, use `GestureDetector`.

## InputAdapter

Convenience class with all 9 methods returning `false`. Extend it and override only what you need — same pattern as `ApplicationAdapter`:

```java
Gdx.input.setInputProcessor(new InputAdapter() {
    @Override
    public boolean keyDown(int keycode) {
        if (keycode == Input.Keys.ESCAPE) { togglePause(); return true; }
        return false;
    }

    @Override
    public boolean touchDown(int screenX, int screenY, int pointer, int button) {
        Vector3 world = new Vector3(screenX, screenY, 0);
        camera.unproject(world);      // REQUIRED — see Coordinate Conversion below
        spawnEntity(world.x, world.y);
        return true;
    }
});
```

## InputMultiplexer

Chains multiple `InputProcessor`s. Dispatches events in order; stops when one returns `true`.

```java
InputMultiplexer multiplexer = new InputMultiplexer();
multiplexer.addProcessor(stage);          // Stage FIRST — UI eats events before game
multiplexer.addProcessor(gameInput);      // game input SECOND
Gdx.input.setInputProcessor(multiplexer);
```

**Stage MUST be first.** If game input is first, it may return `true` and the Stage never receives the event — UI buttons stop working. Stage returns `true` only when a UI actor handles the event, so game input still receives clicks on empty areas.

## Key Constants

`com.badlogic.gdx.Input.Keys`:

| Constant | Value | Notes |
|---|---|---|
| `Input.Keys.A` .. `Z` | 29..54 | Letters |
| `Input.Keys.NUM_0` .. `NUM_9` | 7..16 | Number row |
| `Input.Keys.SPACE` | 62 | |
| `Input.Keys.ENTER` | 66 | |
| `Input.Keys.ESCAPE` | 131 | Desktop; no equivalent on mobile |
| `Input.Keys.BACK` | 4 | Android back button |
| `Input.Keys.MENU` | 82 | Android menu button |
| `Input.Keys.SHIFT_LEFT/RIGHT` | 59/60 | |
| `Input.Keys.CONTROL_LEFT/RIGHT` | 129/130 | |
| `Input.Keys.ALT_LEFT/RIGHT` | 57/58 | |
| `Input.Keys.UP/DOWN/LEFT/RIGHT` | 19/20/21/22 | Arrow keys |

## Touch / Mouse

**Parameters in touchDown/touchUp/touchDragged:**
- `screenX`, `screenY` — **screen coordinates** (Y-down, origin at top-left). NOT world coordinates.
- `pointer` — finger index for multi-touch (0 = first finger, 1 = second, etc.). Always 0 for mouse.
- `button` — which mouse button. On touch devices, always `LEFT`.

**Button constants** (`Input.Buttons`):
| Constant | Value |
|---|---|
| `Input.Buttons.LEFT` | 0 |
| `Input.Buttons.RIGHT` | 1 |
| `Input.Buttons.MIDDLE` | 2 |
| `Input.Buttons.BACK` | 3 |
| `Input.Buttons.FORWARD` | 4 |

## Coordinate Conversion (CRITICAL)

**`touchDown` coordinates are screen pixels (Y-down, top-left origin).** To interact with game world objects, you MUST unproject through the camera:

```java
// Reuse a single Vector3 — do NOT allocate in touchDown every frame
private final Vector3 touchPos = new Vector3();

@Override
public boolean touchDown(int screenX, int screenY, int pointer, int button) {
    touchPos.set(screenX, screenY, 0);
    camera.unproject(touchPos);           // converts to world coords
    placeTower(touchPos.x, touchPos.y);   // now in world space
    return true;
}
```

**Using raw `screenX`/`screenY` for game logic is always a bug.** The Y axis is flipped (screen Y-down vs world Y-up), and camera position/zoom are ignored.

**With a Viewport** (preferred when using FitViewport, ExtendViewport, etc. with letterboxing/pillarboxing — accounts for viewport offset automatically):

```java
private final Vector2 touchPos2 = new Vector2();

@Override
public boolean touchDown(int screenX, int screenY, int pointer, int button) {
    touchPos2.set(screenX, screenY);
    viewport.unproject(touchPos2);            // Vector2, not Vector3
    placeTower(touchPos2.x, touchPos2.y);
    return true;
}
```

**Note:** `viewport.unproject()` takes a `Vector2`. `camera.unproject()` takes a `Vector3`. Don't mix them up.

## GestureDetector

Wraps an `InputProcessor` to detect complex gestures. **GestureDetector implements `InputProcessor`** — so it plugs directly into `setInputProcessor()` or `InputMultiplexer`.

```java
GestureDetector detector = new GestureDetector(new GestureDetector.GestureAdapter() {
    @Override
    public boolean tap(float x, float y, int count, int button) {
        // count = tap count (double-tap = 2)
        return true;
    }

    @Override
    public boolean fling(float velocityX, float velocityY, int button) {
        // swipe gesture; velocity in pixels/sec
        return true;
    }

    @Override
    public boolean longPress(float x, float y) {
        return true;
    }

    @Override
    public boolean pan(float x, float y, float deltaX, float deltaY) {
        // finger drag
        return true;
    }

    @Override
    public boolean pinch(Vector2 initialPointer1, Vector2 initialPointer2,
                         Vector2 pointer1, Vector2 pointer2) {
        return true;
    }

    @Override
    public boolean zoom(float initialDistance, float distance) {
        // pinch-to-zoom; compute ratio = distance / initialDistance
        return true;
    }
});

// Works directly in InputMultiplexer:
multiplexer.addProcessor(stage);
multiplexer.addProcessor(detector);     // GestureDetector IS an InputProcessor
multiplexer.addProcessor(gameInput);
Gdx.input.setInputProcessor(multiplexer);
```

**GestureListener methods:** `touchDown`, `tap`, `longPress`, `fling`, `pan`, `panStop`, `zoom`, `pinch`, `pinchStop`. Use `GestureAdapter` for empty defaults.

**Swipe detection:** Use `fling(velocityX, velocityY, button)`. Compare velocity components to determine direction (e.g., `Math.abs(velocityX) > Math.abs(velocityY)` → horizontal swipe). There is no `onSwipe()`, `SwipeListener`, or `SwipeDetector` class — `fling()` is the swipe handler.

**GestureDetector coordinates are also screen coordinates.** Unproject them through the camera for world-space use.

## Mobile Text Input

`Gdx.input.setOnscreenKeyboardVisible(true)` shows the soft keyboard on mobile (no-op on desktop). `Gdx.input.getTextInput()` shows a native text input dialog:

```java
Gdx.input.getTextInput(new Input.TextInputListener() {
    @Override public void input(String text) { playerName = text; }
    @Override public void canceled() { /* user dismissed */ }
}, "Enter Name", "Player1", "Your name here");
```

On desktop this shows a Swing dialog. Non-blocking — callbacks fire asynchronously. For in-game text fields, use Scene2D's `TextField` widget instead (covered by Scene2D skill).

## Accelerometer

Mobile only. Returns device tilt in m/s² (gravity ~ 9.8).

```java
if (Gdx.input.isPeripheralAvailable(Input.Peripheral.Accelerometer)) {
    float ax = Gdx.input.getAccelerometerX();
    float ay = Gdx.input.getAccelerometerY();
    float az = Gdx.input.getAccelerometerZ();
}
```

Returns 0 on desktop. Always check `isPeripheralAvailable()` or provide keyboard fallback.

## Android Back / Menu Keys

**Use `setCatchKey()` (the modern API).** `setCatchBackKey()` and `setCatchMenuKey()` are **deprecated**.

```java
// In create() or show():
Gdx.input.setCatchKey(Input.Keys.BACK, true);   // prevent default "exit app"
Gdx.input.setCatchKey(Input.Keys.MENU, true);    // prevent default menu

// Then handle in your InputProcessor:
@Override
public boolean keyDown(int keycode) {
    if (keycode == Input.Keys.BACK) {
        showPauseMenu();
        return true;
    }
    return false;
}
```

**Do NOT use** `Gdx.input.setCatchBackKey(true)` — it is deprecated. Use `setCatchKey(Input.Keys.BACK, true)`.

## Common Mistakes

1. **Using screen coordinates for game logic without unprojecting** — `touchDown` gives screen pixels (Y-down). Always `camera.unproject()` before using with game world.
2. **Putting game input before Stage in InputMultiplexer** — Stage must be first so UI buttons receive events. Game input goes after Stage.
3. **Forgetting to return true from InputProcessor methods** — If your processor doesn't return `true`, InputMultiplexer passes the event to the next processor. Events get handled twice or by the wrong processor.
4. **Inventing methods that don't exist on InputProcessor** — There is no `onClick()`, `onTap()`, `onKeyPress()`, `onTouch()`, `onSwipe()`, `onSwipeLeft()`, `onSwipeRight()`, `onSwipeUp()`, or `onSwipeDown()`. Use `touchDown`/`touchUp` for clicks, `GestureDetector` for taps/flings. **Swipe detection = `GestureDetector.fling()`** — there is no dedicated swipe method or SwipeListener class.
5. **Not knowing GestureDetector implements InputProcessor** — GestureDetector IS an InputProcessor. Add it directly to InputMultiplexer. No adapter or wrapper needed.
6. **Using deprecated `setCatchBackKey()`/`setCatchMenuKey()`** — Use `setCatchKey(Input.Keys.BACK, true)` and `setCatchKey(Input.Keys.MENU, true)` instead.
7. **Allocating `new Vector3()` in every touchDown call** — Reuse a field-level Vector3. Allocating per-event creates garbage and triggers GC pauses on Android.
8. **Not unprojecting GestureDetector coordinates** — GestureDetector's tap/pan/fling/longPress coordinates are also screen coordinates. Unproject them just like touchDown coords.
9. **Using `isKeyJustPressed` for continuous movement** — Only true for one frame per press, causing stuttering. Use `isKeyPressed` for held actions (movement, firing).
10. **Using `touchDragged` for hover/mouseover on desktop** — `touchDragged` only fires while a finger/button is held. Use `mouseMoved` for mouse hover without clicking.
11. **Comparing `keyTyped` char against `Input.Keys` constants** — `keyTyped` receives a Unicode character, not a key constant. `character == Input.Keys.A` compares char to int 29, which is silently wrong. Use `keyDown` for key identity checks.
12. **Inverting scroll direction** — `scrolled()` `amountY` is positive for scroll-down, negative for scroll-up. When implementing zoom, scroll-up (negative `amountY`) should zoom in (decrease `camera.zoom`).
