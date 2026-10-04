---
name: libgdx-scene2d-ui
description: Use when writing libGDX Java/Kotlin code involving Scene2D UI — Stage, Table layout, Skin, widgets (Label, TextButton, TextField, CheckBox, Slider, SelectBox, ScrollPane, Dialog, Window), input handling (ClickListener, ChangeListener, InputListener), Actions animations, or InputMultiplexer. Use when debugging UI not responding to input, layout issues, or coordinate conversion problems.
---

# libGDX Scene2D UI

Reference for Stage, Table layout, Skin, widgets, input handling, Actions system, coordinate conversion, and Viewport integration.

## Stage

A scene graph that manages Actors, handles input events, and owns an internal SpriteBatch. In each frame you must call `act(delta)` then `draw()`.

```java
// In create() or show():
Stage stage = new Stage(new FitViewport(800, 480));
Gdx.input.setInputProcessor(stage);  // REQUIRED — without this, no UI input works

// In render():
ScreenUtils.clear(0.2f, 0.2f, 0.2f, 1f);
stage.act(Gdx.graphics.getDeltaTime());  // update Actions, fire pending events
stage.draw();                             // render all Actors

// In resize():
stage.getViewport().update(width, height, true);  // true = center camera

// In dispose():
stage.dispose();  // disposes internal SpriteBatch and all Actor resources
```

**`stage.act(delta)` MUST be called before `stage.draw()`.** `act()` advances Actions (animations, timers), processes pending events, and updates Actor state. Skipping it means Actions don't run and events don't fire.

**Stage disposal:** `stage.dispose()` disposes the Stage's SpriteBatch **only when Stage created it** (default constructor or `Stage(viewport)`). If you pass an external SpriteBatch via `new Stage(viewport, batch)`, `stage.dispose()` does **not** dispose it — you must dispose that batch yourself. This matters when sharing a SpriteBatch between Stage and game rendering. Dispose Skin separately — Stage does not own it.

## Actor

Base class for everything in the scene graph. Has position, size, rotation, origin, color, visibility, and name.

```java
actor.setPosition(x, y);
actor.setSize(width, height);
actor.setRotation(degrees);     // counter-clockwise
actor.setColor(Color.RED);      // tints the actor
actor.setVisible(false);        // hides actor AND skips input
actor.setTouchable(Touchable.disabled);  // disables input, still visible
actor.addAction(action);        // attach an Action
actor.addListener(listener);    // attach an event listener
```

**Touchable:** `Touchable.enabled` (default — receives input), `Touchable.disabled` (ignores input, still visible and drawn), `Touchable.childrenOnly` (group passes input to children only). Use `setTouchable(Touchable.disabled)` to disable a button without hiding it — do not use `setVisible(false)` for this.

## Group

An Actor that contains other Actors. Transforms are relative — child positions are in the parent Group's local coordinate space.

```java
Group group = new Group();
group.addActor(child1);
group.addActor(child2);
group.setPosition(100, 200);  // children move with the group

// Convert between coordinate spaces
Vector2 stageCoords = child.localToStageCoordinates(new Vector2(0, 0));
Vector2 localCoords = child.stageToLocalCoordinates(new Vector2(stageX, stageY));
```

## Table — THE Layout Mechanism

**All Scene2D UI layout uses Table.** Table uses a row/cell model. `add()` returns a `Cell` for chaining layout constraints. Start a new row with `row()` — either standalone or chained on the last cell:

```java
Table table = new Table();
table.setFillParent(true);  // fill the entire Stage
stage.addActor(table);

// Row 1: title — .row() chained on last cell (idiomatic)
table.add(titleLabel).colspan(2).expandX().padBottom(20).row();

// Row 2: two columns — standalone table.row() also valid
table.add(nameLabel).right().padRight(10);
table.add(nameField).width(200).fillX();
table.row();

// Row 3: button centered across both columns
table.add(submitButton).colspan(2).width(150).height(50).padTop(20);
```

Both `table.row()` and `.row()` chained on a Cell are equivalent. Use whichever is more readable.

### Cell Chaining API

`table.add(actor)` returns a `Cell`. Chain layout methods on it:

| Method | Effect |
|---|---|
| `.width(w).height(h)` | Fixed widget size |
| `.pad(all)` / `.pad(top,left,bottom,right)` | Padding around cell |
| `.padTop(t).padBottom(b)` | Individual padding |
| `.expand()` / `.expandX()` / `.expandY()` | Cell claims extra space |
| `.fill()` / `.fillX()` / `.fillY()` | Widget fills cell |
| `.colspan(n)` | Cell spans n columns |
| `.left()` / `.right()` / `.center()` / `.top()` / `.bottom()` | Widget alignment within cell |
| `.uniform()` / `.uniformX()` / `.uniformY()` | All uniform cells share same size |
| `.grow()` | Shorthand for `expand().fill()` |

**`expand()` makes the CELL bigger. `fill()` makes the WIDGET fill the cell.** Without both, the widget stays at its preferred size even if the cell is large.

```java
// Common patterns:
table.add(label).expandX().left();           // push to left edge
table.add(widget).grow();                     // fill all available space
table.add(button).width(100).height(40);      // fixed-size button
table.add().expandX();                        // empty spacer cell (no actor)
```

**Empty spacer cell:** `table.add()` with no actor creates an invisible cell that participates in layout. Use with `.expandX()` to push other cells to edges — e.g., back button left, title center, empty spacer right for a balanced header bar.

**Table defaults:** Set defaults for all cells in a table:
```java
table.defaults().pad(5).expandX().fillX();
// now all subsequent add() calls inherit these defaults
```

**Debug layout:** `table.setDebug(true)` draws cell outlines. Essential when layout isn't working as expected.

## Skin

Loads UI styles (fonts, colors, drawables) from a JSON file + TextureAtlas. Passed to widget constructors.

```java
// Load skin (requires uiskin.json + uiskin.atlas + uiskin.png in assets)
Skin skin = new Skin(Gdx.files.internal("uiskin.json"));

// All widgets require a Skin:
Label label = new Label("Hello", skin);
TextButton button = new TextButton("Click", skin);
TextField field = new TextField("", skin);
CheckBox check = new CheckBox("Enable", skin);
Slider slider = new Slider(0, 100, 1, false, skin);
SelectBox<String> select = new SelectBox<>(skin);

// Dispose when done (separately from Stage)
skin.dispose();
```

**Every widget constructor takes a `Skin`.** Constructing widgets without a Skin (e.g., `new TextButton("Click")`) does not compile — there is no such constructor.

**Named styles:** Widgets default to the `"default"` style in the Skin JSON. Use a second parameter for variants: `new TextButton("Click", skin, "toggle")`.

## Common Widgets

| Widget | Constructor | Notes |
|---|---|---|
| `Label` | `new Label("text", skin)` | Display text. See `setFontScale()` caveat below. |
| `TextButton` | `new TextButton("text", skin)` | Clickable button with text. |
| `TextField` | `new TextField("", skin)` | Text input. `setPasswordCharacter('*')` for passwords. |
| `Image` | `new Image(drawable)` or `new Image(texture)` | Does NOT require Skin. |
| `CheckBox` | `new CheckBox("label", skin)` | Toggle. `isChecked()` for state. |
| `Slider` | `new Slider(min, max, step, vertical, skin)` | `getValue()` for current. |
| `SelectBox` | `new SelectBox<>(skin)` | Dropdown. `.setItems("A","B","C")` |
| `ScrollPane` | `new ScrollPane(actor, skin)` | Scrollable container. Child must have preferred size (see below). |
| `Dialog` | `new Dialog("Title", skin)` | Modal popup. `.button("OK").show(stage)`. See result pattern below. |
| `Window` | `new Window("Title", skin)` | Draggable window. Add content directly (Window extends Table). Use `getTitleTable()` for title bar customization. |

**Note:** `Image` is the exception — it takes a `Drawable` or `Texture`, not a `Skin`.

**Dialog result pattern:** Override `result()` to determine which button was pressed. The second parameter to `.button()` is the `Object` passed to `result()`:

```java
new Dialog("Confirm", skin) {
    @Override
    protected void result(Object object) {
        if ((Boolean) object) { /* user pressed Yes */ }
    }
}.button("Yes", true).button("No", false).show(stage);
```

**ScrollPane gotcha:** The child actor inside ScrollPane must have a **preferred size** (via Table cell constraints like `.width()/.height()`, or widget content that implies a size). If the child has no preferred size, ScrollPane collapses to zero and content is invisible. When wrapping a Table in ScrollPane, ensure the inner Table's cells give it a preferred size.

**`setFontScale()` caveat:** `label.setFontScale()` scales the bitmap font and produces blurry text at large scales. It's acceptable for minor adjustments (0.8–1.5x) but not for large headings. For crisp text at different sizes, generate separate `BitmapFont` instances at the needed sizes (or use FreeType at runtime) and define multiple Skin styles.

## Input Handling

### Stage as InputProcessor

```java
// Scene2D-only input:
Gdx.input.setInputProcessor(stage);

// Scene2D + game input (e.g., camera controls):
InputMultiplexer multiplexer = new InputMultiplexer();
multiplexer.addProcessor(stage);        // UI gets priority
multiplexer.addProcessor(gameInput);    // game gets remaining events
Gdx.input.setInputProcessor(multiplexer);
```

**InputMultiplexer** passes events to processors in order. If Stage consumes the event (user clicked a button), the game input processor won't receive it. Always add Stage first so UI has priority.

### Listener Types

**ChangeListener** — for buttons, checkboxes, sliders, select boxes. Fires when the widget's value/state changes.

```java
button.addListener(new ChangeListener() {
    @Override
    public void changed(ChangeEvent event, Actor actor) {
        Gdx.app.log("UI", "Button clicked");
    }
});
```

The signature is `changed(ChangeEvent event, Actor actor)` — not an ActionListener/ActionEvent pattern.

**ClickListener** — for click/tap events with detailed info (button, count, position).

```java
actor.addListener(new ClickListener() {
    @Override
    public void clicked(InputEvent event, float x, float y) {
        Gdx.app.log("UI", "Clicked at " + x + ", " + y);
    }
});
```

**InputListener** — low-level touch/keyboard events.

```java
actor.addListener(new InputListener() {
    @Override
    public boolean keyDown(InputEvent event, int keycode) {
        return true; // return true = event consumed
    }

    @Override
    public boolean touchDown(InputEvent event, float x, float y, int pointer, int button) {
        return true;
    }
});
```

**Use ChangeListener for UI widgets (buttons, sliders, checkboxes).** Use ClickListener for generic click detection. Use InputListener for raw keyboard/touch.

## Actions System

Fluent builder pattern for animations and sequenced logic. Apply to any Actor.

```java
import static com.badlogic.gdx.scenes.scene2d.actions.Actions.*;

// Fade in over 0.5 seconds
actor.addAction(fadeIn(0.5f));

// Move to position over 1 second with interpolation
actor.addAction(moveTo(200, 100, 1f, Interpolation.smooth));

// Sequence: fade out, then run callback
actor.addAction(sequence(
    fadeOut(0.3f),
    run(() -> game.setScreen(new MenuScreen(game)))
));

// Parallel: fade + move at the same time
actor.addAction(parallel(
    fadeIn(0.5f),
    moveTo(100, 200, 0.5f)
));

// Delay, then action
actor.addAction(sequence(
    delay(2f),
    removeActor()
));

// Common combinators
actor.addAction(forever(sequence(
    fadeOut(1f),
    fadeIn(1f)
)));
```

**Key Actions:** `fadeIn()`, `fadeOut()`, `moveTo()`, `moveBy()`, `scaleTo()`, `rotateTo()`, `rotateBy()`, `sizeTo()`, `color()`, `alpha()`, `delay()`, `sequence()`, `parallel()`, `run()`, `removeActor()`, `forever()`.

**`stage.act(delta)` drives all Actions.** If you forget to call it, no Actions will execute.

## Coordinate System

**Stage coordinates:** Y-up, (0,0) at bottom-left — same as libGDX default.

**Screen coordinates** (from `Gdx.input.getX/Y()` or raw touch events): Y-down, (0,0) at top-left.

```java
// Convert screen coords to stage coords:
Vector2 coords = stage.screenToStageCoordinates(new Vector2(screenX, screenY));

// Convert between actor local coords and stage coords:
Vector2 stagePos = actor.localToStageCoordinates(new Vector2(0, 0));
Vector2 localPos = actor.stageToLocalCoordinates(new Vector2(stageX, stageY));
```

**Inside Scene2D listeners**, coordinates are already in the correct space — `InputEvent.getStageX()` and `getStageY()` return stage coordinates. You only need `screenToStageCoordinates()` when converting raw `Gdx.input` values.

## Viewport Integration

```java
// In create() or show():
stage = new Stage(new FitViewport(800, 480));

// In resize() — REQUIRED:
stage.getViewport().update(width, height, true);  // true = center camera
```

**You MUST call `stage.getViewport().update()` in `resize()`.** Without it, the Stage viewport won't adapt to window changes and UI will be misaligned.

**The `true` parameter** centers the camera so (0,0) is at bottom-left. Without it, the camera defaults to (0,0) center and UI appears offset.

## Minimal Working Example

```java
import com.badlogic.gdx.ApplicationAdapter;
import com.badlogic.gdx.Gdx;
import com.badlogic.gdx.scenes.scene2d.Actor;
import com.badlogic.gdx.scenes.scene2d.Stage;
import com.badlogic.gdx.scenes.scene2d.ui.*;
import com.badlogic.gdx.scenes.scene2d.utils.ChangeListener;
import com.badlogic.gdx.utils.ScreenUtils;
import com.badlogic.gdx.utils.viewport.FitViewport;

public class MyGame extends ApplicationAdapter {
    Stage stage;
    Skin skin;

    @Override
    public void create() {
        stage = new Stage(new FitViewport(800, 480));
        Gdx.input.setInputProcessor(stage);
        skin = new Skin(Gdx.files.internal("uiskin.json"));

        Table table = new Table();
        table.setFillParent(true);
        stage.addActor(table);

        Label title = new Label("My Game", skin);
        title.setFontScale(1.5f); // acceptable for minor scaling — use FreeType for larger sizes

        TextButton playBtn = new TextButton("Play", skin);
        playBtn.addListener(new ChangeListener() {
            @Override
            public void changed(ChangeEvent event, Actor actor) {
                Gdx.app.log("Game", "Play pressed");
            }
        });

        table.add(title).padBottom(40).row();
        table.add(playBtn).width(200).height(50);
    }

    @Override
    public void render() {
        ScreenUtils.clear(0.15f, 0.15f, 0.2f, 1f);
        stage.act(Gdx.graphics.getDeltaTime());
        stage.draw();
    }

    @Override
    public void resize(int width, int height) {
        stage.getViewport().update(width, height, true);
    }

    @Override
    public void dispose() {
        stage.dispose();
        skin.dispose();
    }
}
```

## Common Mistakes

1. **Forgetting `stage.act(delta)` before `stage.draw()`** — Actions won't run, events won't fire, animations freeze. Always call `act()` first.
2. **Not calling `Gdx.input.setInputProcessor(stage)`** — UI looks correct but nothing responds to clicks/taps. Must be set in `create()` or `show()`.
3. **Constructing widgets without Skin** — `new TextButton("Click")` does not compile. All widgets (except Image) require a Skin parameter.
4. **Using absolute positioning instead of Table** — `actor.setPosition(x, y)` does not adapt to screen size. Use Table with `setFillParent(true)` for all UI layout.
5. **Not calling `stage.getViewport().update(width, height, true)` in `resize()`** — UI becomes misaligned on window resize. The `true` centers the camera.
6. **Not disposing Stage** — Stage owns an internal SpriteBatch. Forgetting `stage.dispose()` leaks GPU resources. Dispose Skin separately.
7. **Confusing screen coords with stage coords** — Screen Y-down (0,0 top-left) vs Stage Y-up (0,0 bottom-left). Use `stage.screenToStageCoordinates()` when converting raw `Gdx.input` values. Inside Scene2D listeners, coords are already in the correct space.
8. **Wrong ChangeListener signature** — It's `changed(ChangeEvent event, Actor actor)`, not `actionPerformed(ActionEvent)` or similar. ChangeEvent is `com.badlogic.gdx.scenes.scene2d.utils.ChangeListener.ChangeEvent`.
9. **Not using InputMultiplexer when combining Stage with game input** — Setting `Gdx.input.setInputProcessor(stage)` overrides any previous processor. Use `InputMultiplexer` to combine Stage (first, for UI priority) with game input processors.
10. **Using old `Gdx.gl.glClearColor()` + `glClear()` pattern** — Use `ScreenUtils.clear()` instead (since 1.10.0). Same result, less boilerplate.
11. **Using `setFontScale()` for large text** — Produces blurry results because it scales the bitmap. Generate separate `BitmapFont` instances at needed sizes (or use FreeType). `setFontScale()` is only acceptable for minor scaling (0.8–1.5x).
12. **ScrollPane child has no preferred size** — Content is invisible because ScrollPane collapses to zero. Ensure the child Table has cell constraints (`.width()`, `.height()`, content) that give it a preferred size.
13. **Using `setVisible(false)` to disable a button instead of `setTouchable(Touchable.disabled)`** — `setVisible(false)` hides the actor entirely. Use `setTouchable(Touchable.disabled)` to disable input while keeping the actor visible and drawn.
