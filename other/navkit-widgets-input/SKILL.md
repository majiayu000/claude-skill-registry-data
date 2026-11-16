---
name: navkit-widgets-input
description: navkit's widget tree and input routing (navkit/widget.py, application.py, events.py, commands.py, screen.py) -- the event loop and frame order, Widget geometry and render_tree, focus and dispatch_key, emitting events, async `on_*` handlers, mounted()/unmounting(), modal and overlay, the cursor, mouse routing and capture, raise_child, shadows, double-click, call_every timers, hover, commands, key tables, enables()/checks(), and the key bar. Use when handling keys, mouse or events, adding a command or key binding, or debugging focus.
---

# Widgets, events, focus and commands

## The loop and the tree

- `Application` owns the only asyncio loop. Input arrives through `loop.add_reader` into `InputParser`. **One turn:
  dispatch the whole batch, flush the reactive effects it queued, then paint one frame** -- a paste or drag costs one
  repaint. `SIGWINCH` becomes a `ResizeEvent`; events reach `Application.on_*` hooks first and the tree second.
- `Surface` is what widgets paint into; `ScreenBuffer` owns cells; `surface.view(x, y, w, h)` is a clipped window.
  `render_tree` hands each widget a view of its own area, so **widgets paint from `0, 0` in their own size and cannot
  draw outside themselves**. Wide characters occupy a cell plus a continuation; at a right edge one degrades to a blank.
  `render_diff()` emits only changed escapes. `Widget.render_after` paints over children.
- `Widget` geometry, `visible`, `style` and `parent` are reactive. **All coordinates are relative to the parent**
  (`x`/`y`, `contains()`, a `MouseClickEvent`'s position, shifted by `dispatch_mouse`); the root sits at the origin.
  `render(surface)` paints; `layout(width, height)` is called on the root at every resize and steps around any size
  that carries a binding (no `self.x +` arithmetic anywhere).
- **Placing a widget from Python binds its sides**, because `add()` lays a new child out into its parent and steps
  around only a bound side: an assigned rectangle becomes the parent's whole area. Three `Widget` methods say the
  common shapes; each binds every side it is given, replacing a binding there:
  - `pin_rect(x, y, w, h)`: a popup at a computed spot (history, date/time pickers, completion list, fast rename);
  - `fill_parent()`: an overlay over its parent, following a resize, 0x0 with no parent (menus, grabber, savers);
  - `pin_edges(left=, right=, top=, bottom=)`: parent insets with markup's `anchors:` rules (Info panel's bar,
    Settings' and Attributes' row). Siblings and `center` are markup's alone.

  The names avoid `anchor` and `inset`, which `Tooltip`, `InputLine` and `ListViewer` already use. Real layout
  arithmetic stays hand-written: windows, the Miller columns, toasts on the desktop's corner.

## Pictures (kitty graphics, sixel)

- **A widget never paints a picture.** It calls `surface.place_image(picture, x, y, style)` in `render()` with a
  `navkit.graphics.Picture` (`cols`, `rows`, `png` for kitty, a ready `sixel` DCS string -- built off the loop). That
  fills the cells with blanks whose `Style.image` is the picture's id (never declared by a sheet) and records
  `{id: (picture, y)}` in `ScreenBuffer.placements` through the views; `copy_from`/`mirrored` carry it, `clear` empties it.
- `Application._render` hands the frame to `GraphicsLayer.compose` **between composing and diffing**: escapes to go
  before the diff (a kitty placement deleted, so text written next is not under it) and after it (pictures written
  over the blanks the diff has just written), all before the cursor. **A picture is shown only while every stamp
  survives** -- found in the buffer as it goes out, so a mirrored screen and a widget kept left to right
  (`mirrors = False`) put it where its cells went. Painted over at all (a window, a menu, a shadow) or clipped by a
  view, it is hidden whole; a sixel one also keeps off the last line (it would scroll).
- kitty: transmitted once per id (`q=2` everywhere: an answer would be typed), placed at a CUP with `C=1`, deleted
  (`d=i`) when hidden or moved, freed (`d=I`) once no frame places it; a full repaint deletes every placement and
  places again; `release_terminal` frees all and `reclaim_terminal` forgets (the alternate screen took them). sixel:
  pixels in the cells, so written again on any full repaint or move, and the cells of one that goes are invalidated
  in `_front` (`ScreenBuffer.invalidate`) so the diff blanks them. Tests: `tests/test_graphics.py`, a `FakeTerminal`
  whose info says `graphics="kitty"`.

## Failures: never silent

- **Every exception escaping application code goes through `Application.fail(error, fatal=False)`**: handlers
  (`_handle`), ticks, effects (`_flush_effects`), a widget's `render`/`render_after` (`Widget._guarded`), spawned tasks
  (`_finished`), loop callbacks (`loop.set_exception_handler`, installed by `run_async`) and raw threads
  (`threading.excepthook`). Before this, a spawned task's failure was re-raised inside a done-callback: asyncio printed
  it into the alternate screen, which was then wiped, and `run()` returned 0.
- `fail` calls `log_error(error)` (does nothing in navkit) every time, then offers `report_error(error)`. If that
  returns True, the application carries on. Otherwise the error is kept, `exit()` is called, and **`run_async` raises it
  after `terminal.stop()`**, so the traceback reaches a normal screen. The default `report_error` returns False, which
  keeps tests strict.
- **`Navigator.on_stop` runs each shutdown step on its own**: autosave, `remember_windows`, the console, terminal
  views, dirwatch, sessions, archives, root's helper -- a step that raises is `errorlog.append`ed with its name as
  context and counted in `shutdown_failures`, and the next still runs; `main()` prints the count and the log's path
  on stderr after `run()`. Only `Exception` is caught, so a cancel or Ctrl+C still goes through.
- It always stops when `fatal` is true (`on_start`, `on_stop`, the frame machinery in `_paint`), when the loop is not
  running, when a failure occurs inside `report_error`, or after more than `ERROR_STORM_LIMIT` (5) failures in
  `ERROR_STORM_WINDOW` (10 s).
- **A widget whose paint fails does not take the frame down.** It is retried every frame and reported only when its
  `(type, message)` changes, so one broken window is one box, not one per frame.
- An effect that fails puts the rest of its batch back on the queue (`Scheduler.flush`), and `_flush_effects` runs
  them in the same turn.
- **A stall is logged too, though nothing failed.** `_main_loop` sets `handling_since`/`handling` from taking a batch
  until it is painted, and `_handle` keeps the last 64 input events in `recent_events` (`describe_event`: key names,
  never paste text; no ticks or bare motion). Navigator's `errorlog.Watchdog`, a daemon thread, reads only those
  plain fields. When a batch is older than `[system] stall_report` seconds (default 2, 0 off) it writes one `STALL`
  entry to `errors.log`: the recent input, every thread's stack (faulthandler), and every task's stack, asked of the
  loop with `call_soon_threadsafe`. When the loop does not answer within 1 s, the entry says the loop thread is
  blocked (a syscall on the loop: look at the threads); when it answers, a handler is awaiting something (look at the
  tasks). `STALL ENDED after N s` follows. `kill -USR1 <pid>` dumps every thread's stack there at any moment.

## Focus and keys

- `Application.focused` holds the widget keys go to; `Widget.can_focus` (False by default) says who may; `focus()` takes
  it, `Application.focus_next()` moves it. `Widget.focused` is a computed (so `:focused` is a sheet state).
  `dispatch_key` walks the focus path, nearest first -- **with nothing focused a key reaches no widget at all**.
  Eligibility is decided when the key arrives.

## Events and handlers

- `Widget.emit(event)` walks from the widget up through ancestors to the application, stopping at the first handler
  returning True. An event class names its handler (`ClickEvent` -> `on_click`, `Event.handler`). A widget declares
  what it raises with `emits = (ClickEvent,)`, read through `navkit.events.emitted(cls)`, which unions down the MRO.
- **Every `on_*` handler is `async def`**; navkit refuses a synchronous one (at class creation, or at the call for one
  assigned onto an instance). **A hook that cannot be awaited where it is called gets no `on_*` name**: `mounted()` and
  `unmounting()` are plain sync callbacks. `Application.on_start`/`on_stop` are awaited by `run_async`. An awaiting
  handler lets the loop run mid-batch but **cannot cause a repaint**.
- `navkit/events.py` carries only events navkit itself raises (terminal input, the loop's wake); everything a widget
  means belongs to the library.
- `dispatch_mouse` offers to the topmost child first under `event.handler` (so a refinement reaches its own handler).
  `Application.capture_mouse` gives a dragging widget the mouse.
- **A held button repeats through `Application.hold_mouse(widget, event, step, *, delay, every, moves, done)`**,
  Turbo Vision's `evMouseAuto`, which a terminal cannot send (it reports a press, moves and a release, nothing while
  the pointer rests). It takes the capture. After `REPEAT_DELAY` (8/18.2 s, TV's `RepeatDelay` ticks), it awaits
  `step(x, y, True)` every `REPEAT_EVERY` (1/18.2 s) at the pointer's last place, in the widget's coordinates. With
  `moves`, a move awaits `step(x, y, False)` too.
  - The press is the caller's to act on.
  - While it holds, the captured moves and the release go to it, not to the handler. A double click still reaches
    the handler.
  - `step` returning False stops the ticks but keeps the capture.
  - It ends, calling `done` once, with whatever ends the capture: the release, `release_mouse`, unmounting, or a
    modal opening (`_set_capture` is the one place the capture changes).
  - Users: `ScrollBar`, `ListViewer` (so every list and the panels), the panel's held marking, and F3's and the
    dBase viewer's quarters.
  - Tests patch `navkit.application.REPEAT_DELAY`/`REPEAT_EVERY` (`tests/test_mouse_hold.py`).
  - A departure: where DN zeroed `RepeatDelay` (it then repeated as fast as it polled), the first delay is kept,
    except for edge scrolling, which starts with the pointer already outside.

## Lifecycle, modal, cursor

- `Widget.is_mounted` says whether a widget is in an application's tree; `mounted()`/`unmounting()` are called by the
  walks `Application.root`, `add()` and `remove()` drive. **`remove()` disposes the subtree's effects** -> effects go in
  `mounted()`.
- `Widget.modal` makes a widget take all input while mounted (the mount walks maintain `Application.modal`);
  `Application.overlay(widget)` puts one on top, closed with `app.root.remove(widget)`. Focus is confined and handed
  back. `Widget.dims_behind = False` keeps a modal layer from dimming (`--no-dim-modal` turns dimming off globally).
  **The dimmed twin of a style is kept across frames** (`Application._dimmed`): `render_diff` rules out an unchanged
  row with one list comparison only while its cells hold the *same* style objects as last frame, and a fresh twin
  per frame made it compare every cell's style field by field -- tripling a frame's cost under a progress box.
- **A frame reuses what lies beneath the top modal** (`Application._underlay`, taken in `_painting_modal` after the dim
  while `_render` paints the whole tree) and paints only the modal and what stands above it (`_render_above`: the
  modal's subtree, then each ancestor's later children and `render_after`). Only when nothing beneath can have
  changed: `Widget.invalidate` passes itself to `Application.invalidate(widget)`, and anything outside the top modal,
  an `invalidate()` naming no widget, a modal pushed or popped, a resize, or **any event but a timer's `_Tick`** sets
  `_below_dirty`. Input is excluded because per-widget damage misses derived values (a key bar's enabled command
  reading a field); a tick says through `invalidate` what it changed. What it buys: a progress box over the desktop
  costs its own subtree per tick, not the whole tree. A widget beneath a modal that changes **plain** state on a tick
  must call `invalidate()` itself -- nothing else repaints it now.
- **A frame only `paints_alone` widgets asked for repaints only their cells** (`Application._render_damage`).
  - **Opting in:** a widget class sets `paints_alone = True` to promise that a change to its own reactive state
    changes only its own cells: nothing else reads that state and it paints nothing outside itself. The clock does.
  - **Tracking:** `Application._damage` holds the widgets that asked. It becomes None (paint the whole frame) on the
    same triggers as `_below_dirty`, and whenever any other widget, or no widget, invalidates.
  - **Painting:** the tree is painted as always, through a `screen.Clip` covering the bounds of each damaged widget's
    rectangle now and where it was last painted (`_painted_at`, recorded in `render_tree`). `Surface.touches` lets
    `render_tree` skip widgets wholly outside the clip; one overlapping it paints in its usual order, so a tooltip or
    menu over the clock stays on top.
  - **Falls back to a full repaint:** under a modal (the dim would be applied twice), on a mirrored screen, with a
    picture shown, or when `Clip.spoiled` is set (a wide character or a copy cut by the clip's edge, or a picture
    placed).
  - **What it buys:** the clock's colon costs ~2 ms twice a second instead of ~26 ms.
  - **The cost of opting in:** a widget that shows something time-based and relied on the clock's whole-frame
    repaints to refresh would now freeze. It needs a timer of its own (none did when this was added).
- **Raising is a reorder**: `raise_child`/`lower_child`, never re-`add()` (that unmounts). `Widget.shadow` is painted by
  `render_tree` into the parent's surface.
- `Widget.cursor_position()` says where the terminal cursor belongs; the application asks **the whole focus path,
  nearest first**, at the end of each frame, so a caret only shows where keys go. The `caret` property sets DECSCUSR
  from a sheet, and `::caret`'s `fg` the cursor's colour (OSC 12, `navkit-terminal`).

## Double-click and timers

- `ClickTracker` synthesises `DoubleClickEvent` from two presses and a clock. **The press is still delivered** (the
  double-click is additional); dispatched inline after that press, re-entering `_handle` so `on_event` sees it; navkit's rather than the library's
  because `Application._loop.time()` is the only clock event handling can reach; keyed on exact cell and button; counts upward
  (a triple click raises one); forgotten on wheel, resize or modal push/pop. `DOUBLE_CLICK_TIMEOUT` 0.4, overridable via
  `Application(double_click=...)`. Clockless by construction (told `now`).
- **VTE's middle click** (xfce4-terminal, found with keyprobe): under mouse tracking VTE reports no middle *press*; it
  pastes the primary selection (a `PasteEvent`) and reports only the release. A widget that wants the middle button
  at a spot says `claims_middle_click(x, y)` (own coordinates, False by default). A terminal paste while
  `Application.pointer` rests on such a spot is held `MIDDLE_PASTE_WINDOW` (0.5 s, `_hold_paste`); a middle release
  with no press (`_middle_down`) there drops it and is preceded by the press it lost (`_lone_middle_release`),
  anywhere else lets it go at once. A paste with no release after it (Ctrl+Shift+V over a panel row) arrives late.
- **A right press is offered twice**: as itself, then inline as a `ContextMenuEvent` (`on_context_menu`) along the
  same route. It is not raised when a widget held the capture before the press, when the press took it, or for a
  press outside the modal. navkit says where a menu was asked for; navml's `ContextMenuHost` decides what it is
  (`navml-windows-menus`). `run_command(binding, start=)` runs a command from a widget other than the focus.
- **`bindings(app, start)` / `key_for`** add the application's table only when there is no modal or *start* lies
  outside it (asking about the focus behind it); a *start* inside the modal gets the modal's keys, as a key would.
- **The one clock is `Application.call_every(seconds, async_callback)`**, returning a cancellable `Repeat`; callable
  before the loop runs; every tick is posted and awaited inside a dispatch.
- Hover: a position the application keeps (`hovered` state). `Application.pointer` is the last reported `(x, y)` of
  any mouse report, plain motion included -- a plain attribute, not reactive (the screen savers' corners read it).
- **Tooltips**: `Widget.tooltip` (a string, `""` for none; translated in markup) shows beside the pointer after it
  rests `Application.tooltip_delay` milliseconds (1000, `TOOLTIP_DELAY`; 0 off). Asked through `Widget.tooltip_at(x, y)`,
  own coordinates, from `hovered` up -- the nearest non-empty wins; a widget painting several things (navml's
  `OptionStrip`, and `Window`'s chrome icons through `chrome_hit`) overrides it. A widget with `tooltip_passes = False` stops the
  climb: navml's `ScrollBar`, which its list would otherwise answer for with the row at that height. **Only a plain motion arms it** (`Application.call_later`, a one-shot `Repeat`);
  **any other input but a tick drops it**, shown or pending. Shown as navkit's `Tooltip` overlaid as the root's last
  child (so over a modal too), geometry bound, flipping left/up at the edges. No mode 1003, no tooltips from the
  pointer -- Shift+F11 instead (below).
  Navigator follows Interface Setup's *Tooltip delay* (`[interface] tooltip_delay`) by an effect in `on_start`.
- **A tooltip follows on**: one taken down by the pointer moving on leaves the next quick for `TOOLTIP_FOLLOW_ON`
  (2 s): armed with `TOOLTIP_FOLLOW_ON_DELAY` (0.08 s), not the whole delay. A key or a press ends that.
- **A key is set apart only in `navkit.tooltip.Markup`**, a `str` whose `~` runs paint in `Tooltip::key`
  (`caption_runs`, now `navkit/text.py`, navml re-exporting it). Build one with `with_keys(text, keys)` --
  never `f"{text} ({key})"` -- and join lines with `navkit.tooltip.lines()`, which keeps it Markup and escapes the
  plain parts; concatenating a Markup gives a plain `str`. A plain `str` is painted as it is, so a file name or a path
  is never escaped. Tests compare `plain(text)`.
- **Shift+F11 shows the tooltip of where the keyboard is** (`navkit.tooltip.ShowTooltip`, bound in `Navigator.keys`
  and so in `keybindings.ini`'s `[global]`), until the next key. The application looks it up in its own table
  itself, so it works past a modal, where that table otherwise stands aside. Where is
  `Widget.tooltip_anchor()` of the focused widget -- the caret, else the corner; a list's cursor row, a cluster's
  `sel`, a tab, a panel's cursor name, a calendar's day, an open menu's row override it -- asked as the pointer
  would be there (`Application.tooltip_from`). A focusable widget that paints several things needs an anchor.
- **A greyed command says why**: `Widget.refusal(command) -> str`, `""` when it will run; `enables` is
  `not refusal(...)` by default, so override `refusal`, not `enables`, and the reason cannot drift from the veto.
  `commands.disabled_reason` / `Application.command_disabled_reason` ask the widget `target()` would. A greyed menu
  row (`MenuBox.hint`), key bar item and option strip item add it to their tooltip; a button has none (buttons do
  not go through commands). A widget overriding only `enables` greys with no reason.
- **A `refusal` is asked every frame** a menu is open, and the key bar's always: it must cost nothing per frame. In
  Navigator a program's presence is `navigator.lib.system.which.which` (kept `TTL` 5 s, keyed on `$PATH` and
  `shutil.which`'s identity, so a patched one and a new install are both seen) -- never bare `shutil.which`, which
  walks `$PATH` each time; a per-listing walk goes on a computed (`navigator-panels`); nothing stats a path on the loop.
- **While a menu is open the key bar is its hint line**, TV's `THintStatusLine`: `MenuBar.hint()` (the top box's
  row, its reason, else the bar caption's tooltip) painted across `KeyBar` (`menu_hint()`), the items and their
  tooltips standing aside. The menu session answers for the bar beneath it (`MenuSession.tooltip_at`).

## Commands and key tables

- A command is an `Event` subclass (`class MakeDirectory(Command)` -> `on_make_directory`), emitted from the focused
  widget up. A key table is a class attribute `keys = {"f7": MakeDirectory}` or a markup `keys:` block, consulted at
  each step of the focus path before that widget's `on_key`; the application's table before the tree, **never under a
  modal**.
- **The nearest widget with the handler decides whether the command is enabled** (`enables(command)`); a command nobody
  handles is disabled, and a disabled command's key falls through as if unbound. `checks(command)` gives menu ticks.
- **Run-time overrides**: `override_keys(cls, table, base)` makes `cls`'s keys `key_table(base) | table` in place of
  what the classes between bind (so a key can be removed); `restore_keys()`, `default_keys()`, `own_keys()`,
  `check_table()`. `key_table` honours them at every lookup, so they are live at once. Navigator's `keybindings.ini`
  is the user of it (`navigator-keybindings`).
- Where bindings sit: `Navigator.keys` holds Ctrl+O, F1, F10 (the menu), Alt+X, and Enter/Home/End for the command
  line (Alt+X is on the application because a way out cannot live on a window the user can close); `manager.nml`
  holds Tab, Alt+R/Ctrl+R and F2-F8; `Desktop.keys` the window keys; `dialog.nml` Esc, Enter and Tab.
- **Chords**: a spec may be keys separated by a blank, `"ctrl+k b"` (`parse_key`, `key_label` -> `Ctrl-K B`). A table
  may not bind a key both alone and as a chord's start. `Application._chord_key` runs before the key tables: a key
  that begins a chord bound by a table *on the current path* (the application's unless a modal is up, then the focus
  path's) is held in the reactive `Application.chord`; the next key completes it -- looked up in the same tables,
  same order -- or is swallowed with it, never typed. Off the path a prefix key is an ordinary key, so Ctrl+K still
  reaches a program in the console.
- **`Widget.takes_raw_keys()`** (False by default): a widget on the focus path answering True -- the console and a
  terminal window while a program runs -- means no chord starts there (`Application._raw_keys`), so a chord the
  application's own table binds (Ctrl+J, the key macros) still leaves Ctrl+J to the program. Keys bound alone
  are unaffected.
- **`Application.input_tap`**: a plain callable, when set, given every `KeyEvent` and `PasteEvent` before
  `on_event` -- what Navigator's key recorder hangs off (`navigator-macros`). Called on the loop; it must not
  raise or block.
- An instance in a table (`GoParent(by_key=True)`) lets `enables` treat the key and the menu differently.
- Key names: a bare `+` is `plus`, a bare Space is named `space` (its `key` is `" "`), keypad operators
  `kp_plus`/`kp_minus`/`kp_multiply`/`kp_divide`.
- **Where commands live**: with the group that handles them, one `commands.py` per group (`navigator/widgets/shell/`,
  `manager/`, `viewer/`, `editor/`, `file_ops/`); `navigator/commands.py` keeps Help, Quit, ToggleConsole.
  `navml/commands.py` holds the window set, `navml/widgets/dialog/commands.py` and `navml/widgets/menu/commands.py`
  theirs. Per group because a component's `__init__.py` imports its widget.
- **The key bar reads captions off the bindings** (`app.bindings()`), greys disabled commands in `$bar-disabled`, and a
  click runs the command. While Alt/Ctrl/Shift is held it shows that modifier's row (`StatusDef hcFilePanel`'s `-`/`+`/`:` items, bound in
  `manager.nml`) (`Application.modifiers`, needs the
  kitty protocol -- see `navkit-terminal`).
- **Every key hint goes on the key bar, never in a frame** (the user's rule). Keys a widget takes that no key table
  names -- a list's Space, a mode's arrows, a popup's `keys=` -- are `Widget.key_hints()`: `(label, caption)` pairs,
  translated, read from state. The bar (`navigator/widgets/shell/keybar/keybar.py`) asks every widget from the focus
  out, the nearest winning a label; a hint labelled `F2` takes F2's slot, the rest lead before the function keys
  (they say what the keyboard does now; a panel's ten F-keys fill 80 columns, so the last give way). Hints are
  `Hint` items: never greyed, a click does nothing. Tests read them with conftest's `key_bar_hints(app)`.
- **A key bar item's tooltip is its command's menu path** (`File > Make directory`, `...` dropped) through
  `KeyBar.menu.path_to()`; a command in no menu shows its caption, a hint nothing.

## Read when

| Reference | Read when |
|---|---|
| `reference/cursor.md` | the cursor and its shape |
| `reference/modal-and-overlay.md` | modality, keys and mouse under a modal, focus confinement, overlay |
| `reference/windows-raising.md` | raising, mouse capture, `render_after`, shadows |
| `reference/mounting.md` | mount/unmount order, why not an event, disposing effects |
| `reference/focus.md` | focus pointer, eligibility, bubbling, tab order |
| `reference/emitting.md` | emit, handler names, async rule, what belongs in events.py |
| `reference/double-click.md` | the double-click detector |
| `reference/timers.md` | `call_every` |
| `reference/commands.md` | commands, key tables, enabled-by-nearest-handler |
| `reference/hover.md` | hover, tooltips |
| `reference/still-open.md` | navkit's open questions |
