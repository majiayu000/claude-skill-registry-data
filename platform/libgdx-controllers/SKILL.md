---
name: libgdx-controllers
description: Use when writing libGDX Java/Kotlin code involving gamepad or controller input — gdx-controllers extension, Controller discovery, ControllerListener events, ControllerMapping for cross-controller button/axis mapping, dead zones, or multi-controller support. Use when debugging controller not detected, wrong button mappings, or stick drift.
---

# libGDX gdx-controllers Extension (2.x)

Reference for the gdx-controllers 2.x extension — controller discovery, input polling, event-driven input, cross-controller mapping, and common patterns.

**This covers gdx-controllers 2.x (the current standalone extension).** The old 1.x API bundled with libGDX core is deprecated and has a completely different interface. Do NOT use the old API.

## 1.x vs 2.x — Critical Differences

| | Old 1.x (DEPRECATED) | New 2.x (USE THIS) |
|---|---|---|
| **Gradle group** | `com.badlogic.gdx:gdx-controllers` | `com.badlogicgames.gdx-controllers:gdx-controllers-core` |
| **ControllerListener** | 8 methods: `povMoved`, `xSliderMoved`, `ySliderMoved`, `accelerometerMoved`, etc. | **5 methods only**: `connected`, `disconnected`, `buttonDown`, `buttonUp`, `axisMoved` |
| **Mapping** | None — hardcode button numbers | `controller.getMapping()` → `ControllerMapping` |
| **D-pad** | `PovDirection` enum | Buttons via `mapping.buttonDpadUp/Down/Left/Right` |
| **Package** | `com.badlogic.gdx.controllers` | `com.badlogic.gdx.controllers` (same package, different artifact) |

**If you see `PovDirection`, `xSliderMoved`, `ySliderMoved`, or `accelerometerMoved` — that's the old 1.x API. Stop and switch to 2.x.**

## Gradle Dependencies

```gradle
// In gradle.properties:
controllersVersion=2.2.5

// core module:
implementation "com.badlogicgames.gdx-controllers:gdx-controllers-core:$controllersVersion"

// desktop (lwjgl3) module:
implementation "com.badlogicgames.gdx-controllers:gdx-controllers-desktop:$controllersVersion"

// android module:
implementation "com.badlogicgames.gdx-controllers:gdx-controllers-android:$controllersVersion"

// ios module:
implementation "com.badlogicgames.gdx-controllers:gdx-controllers-ios:$controllersVersion"
```

**The group ID is `com.badlogicgames.gdx-controllers`, NOT `com.badlogic.gdx`.** The old `com.badlogic.gdx:gdx-controllers` is the deprecated 1.x API.

## Controller Discovery

```java
// Get all currently connected controllers
Array<Controller> controllers = Controllers.getControllers();

// Never assume a controller is available at startup
if (controllers.size > 0) {
    Controller controller = controllers.first();
    Gdx.app.log("Input", "Found: " + controller.getName());
}
```

Controllers may connect/disconnect at any time. Always null-check before use and listen for connect/disconnect events.

## ControllerMapping — Cross-Controller Button/Axis Codes

**NEVER hardcode button or axis numbers.** Raw codes differ across controllers and platforms. Always use `controller.getMapping()`:

```java
ControllerMapping mapping = controller.getMapping();

// Buttons — use these named constants
mapping.buttonA           // Xbox A / PS Cross
mapping.buttonB           // Xbox B / PS Circle
mapping.buttonX           // Xbox X / PS Square
mapping.buttonY           // Xbox Y / PS Triangle
mapping.buttonL1          // Left bumper / L1
mapping.buttonR1          // Right bumper / R1
mapping.buttonL2          // Left trigger as button / L2
mapping.buttonR2          // Right trigger as button / R2
mapping.buttonLeftStick   // Left stick click / L3
mapping.buttonRightStick  // Right stick click / R3
mapping.buttonStart       // Start / Options
mapping.buttonBack        // Back / Select / Share
mapping.buttonDpadUp      // D-pad directions
mapping.buttonDpadDown
mapping.buttonDpadLeft
mapping.buttonDpadRight

// Axes — return float from -1.0 to 1.0
mapping.axisLeftX         // Left stick horizontal
mapping.axisLeftY         // Left stick vertical
mapping.axisRightX        // Right stick horizontal
mapping.axisRightY        // Right stick vertical
```

## Polling Input

```java
// In render() — poll current state
ControllerMapping m = controller.getMapping();

boolean jumping = controller.getButton(m.buttonA);
float moveX = controller.getAxis(m.axisLeftX);
float moveY = controller.getAxis(m.axisLeftY);
```

## Event-Driven Input

### ControllerListener (2.x — 5 methods only)

```java
public interface ControllerListener {
    void connected(Controller controller);
    void disconnected(Controller controller);
    boolean buttonDown(Controller controller, int buttonCode);
    boolean buttonUp(Controller controller, int buttonCode);
    boolean axisMoved(Controller controller, int axisCode, float value);
}
```

**Only 5 methods.** If you see `povMoved`, `xSliderMoved`, `ySliderMoved`, or `accelerometerMoved`, you're using the old 1.x API.

### ControllerAdapter

`ControllerAdapter` implements `ControllerListener` with empty defaults — override only what you need:

```java
Controllers.addListener(new ControllerAdapter() {
    @Override
    public void connected(Controller controller) {
        activeController = controller;
    }

    @Override
    public void disconnected(Controller controller) {
        if (activeController == controller) activeController = null;
    }

    @Override
    public boolean buttonDown(Controller controller, int buttonCode) {
        ControllerMapping m = controller.getMapping();
        if (buttonCode == m.buttonA) {
            player.jump();
            return true;
        }
        return false;
    }
});
```

### Listener Scope

- **`Controllers.addListener()`** — Global: receives events from ALL controllers, including connect/disconnect.
- **`controller.addListener()`** — Per-controller: receives events only from that specific controller. Does NOT receive connect/disconnect.

## Dead Zones

Analog sticks have hardware noise — they rarely rest exactly at 0. Apply a dead zone:

```java
private static final float DEAD_ZONE = 0.2f;

float x = controller.getAxis(mapping.axisLeftX);
float y = controller.getAxis(mapping.axisLeftY);

if (Math.abs(x) < DEAD_ZONE) x = 0;
if (Math.abs(y) < DEAD_ZONE) y = 0;
```

Without dead zones, characters will drift when the stick is untouched. Values between 0.15 and 0.25 are typical thresholds.

## Complete Example

```java
import com.badlogic.gdx.controllers.*;
import com.badlogic.gdx.utils.Array;

public class GameScreen {
    private Controller activeController;
    private static final float DEAD_ZONE = 0.2f;

    public void create() {
        // Check for already-connected controllers
        Array<Controller> controllers = Controllers.getControllers();
        if (controllers.size > 0) {
            activeController = controllers.first();
        }

        // Listen for connect/disconnect
        Controllers.addListener(new ControllerAdapter() {
            @Override
            public void connected(Controller controller) {
                if (activeController == null) {
                    activeController = controller;
                }
            }

            @Override
            public void disconnected(Controller controller) {
                if (activeController == controller) {
                    activeController = null;
                    // Fall back to another controller if available
                    Array<Controller> remaining = Controllers.getControllers();
                    if (remaining.size > 0) activeController = remaining.first();
                }
            }
        });
    }

    public void update(float dt) {
        // Always support keyboard as fallback
        handleKeyboard(dt);

        if (activeController == null) return;

        ControllerMapping m = activeController.getMapping();

        // Analog stick with dead zone
        float moveX = activeController.getAxis(m.axisLeftX);
        float moveY = activeController.getAxis(m.axisLeftY);
        if (Math.abs(moveX) < DEAD_ZONE) moveX = 0;
        if (Math.abs(moveY) < DEAD_ZONE) moveY = 0;

        player.x += moveX * SPEED * dt;
        player.y += moveY * SPEED * dt;

        // Buttons via mapping — works across Xbox, PlayStation, etc.
        if (activeController.getButton(m.buttonA)) player.jump();
        if (activeController.getButton(m.buttonX)) player.attack();
        if (activeController.getButton(m.buttonStart)) togglePause();
    }
}
```

## Common Mistakes

1. **Using the old 1.x controller API** — If your `ControllerListener` has `povMoved`, `xSliderMoved`, `ySliderMoved`, or `accelerometerMoved`, you're using the deprecated 1.x API. The 2.x listener has only 5 methods. Check your Gradle dependency: the group must be `com.badlogicgames.gdx-controllers`, not `com.badlogic.gdx`.
2. **Hardcoding button/axis numbers** — `controller.getButton(0)` or `controller.getAxis(1)` will break across controllers and platforms. Always use `controller.getMapping().buttonA`, `.axisLeftX`, etc.
3. **Assuming a controller is always connected** — Controllers can be disconnected at any time. Null-check before use, listen for disconnect events, and always support keyboard as fallback.
4. **No dead zone on analog sticks** — Without a dead zone (0.15–0.25), characters drift from hardware noise on idle sticks.
5. **Building a custom mapping system** — `ControllerMapping` already abstracts Xbox/PlayStation/generic differences. Don't build your own mapping layer with hardcoded per-controller button tables.
6. **Using invented constants** — `ControllerButton.A`, `ControllerAxis.LeftX`, `Axes.leftX` do NOT exist. The correct API is `controller.getMapping().buttonA`, `controller.getMapping().axisLeftX`.
7. **Only listening per-controller** — `controller.addListener()` does not receive connect/disconnect events. Use `Controllers.addListener()` for global events including hotplug.
