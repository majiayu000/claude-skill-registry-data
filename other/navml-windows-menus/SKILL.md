---
name: navml-windows-menus
description: Overlapping windows and menus -- navml's Window, Desktop, Modal stacking, raising, dragging/resizing/zooming, shadows, Window > List (Windows Manager), Tile/Cascade/Close all, `must_ask`/`ask_to_close`, and MenuBar/MenuBox/SubMenu/MenuItem/MenuLine, the MenuContainer API, menu ticks, a window's own menu joining the bar (`MenuBar.context`), and the command palette (Alt+Shift+P, `CommandPalette`, `navml/fuzzy.py`). Use when touching the desktop, a window, or Navigator's main menu.
---

# Windows, the desktop and menus

## The desktop

The root is `navigator/widgets/shell/shell/` -- menu bar, `Console`, navml's `Desktop` over it, key bar -- and
`Manager` is a frameless `Window` on that desktop, opened zoomed, which the user can drag, resize from its corner, zoom
with `[↕]`/`[↑]`, close with `[■]`, and bring forward by clicking. **The console is the background and is always
showing**; Ctrl+O hides the desktop (one `visible` binding). `Modal` is the old framed window (fixed, centred, bound
geometry, `modal = True`); `Dialog` derives from it.

Four rules from building it:
- **A window's rectangle is state, never bound** -- drag, resize and zoom assign it.
- **Raising is `Widget.raise_child`, a reorder** -- `add()` would unmount.
- **Which control a window or a dialog starts on is `first_focus`** (a property of `Window` and `Modal`), set in the
  root of its markup. `Window.take_keyboard` reads it on every activation, never from `mounted()`: that runs inside
  `Desktop.open`'s `add()`, before `activate` has saved which panel the window below had, so closing the window
  would hand the keyboard to the left panel. Do not override `take_keyboard` just to focus one child.
- **A window's right-click menu is `local_menu`**, naming one of its own menus in the root of its markup:
  `local_menu: volumes_menu`. The bar's menu and the context menu are then one list.
  - `Window` implements the host hooks itself: `context_menu()`, `prepare_context`, `context_point` and the two
    handlers.
  - `Window.enables` greys Shift+F10 where there is no menu, without building one.
  - A window whose context menu differs from its bar menu (a shorter list: Services, Sync, Processes) or is built at
    run time (Calendar) overrides `context_menu()` and both handlers, as before.
- **A shadow is `Widget.shadow`**, painted by `render_tree` into the parent's surface before the widget, after a
  modal's dim (on for `Window`, `Modal`, `MenuBox`, `HistoryList`).
- **The application's own `on_key`/`on_mouse_click` must step aside while `app.modal` is set**, because they run before
  navkit's modal routing (the application's *key table* does this by itself).

navkit grew `raise_child`/`lower_child`, `Application.capture_mouse` and `Widget.render_after` for it (see
`navkit-widgets-input`).

- **A window's title keeps clear of its icons** (`Window._title_span`): between `[■]` and `[↑]`/`[↕]`, a blank from
  each, cut by painted width with `…` (`_fit`), centred on the whole top edge where it fits and slid clear where it does
  not; the title tooltip names the whole title when it was cut. A `Modal`'s `[■]` is at the same column (`CLOSE_X`, 2:
  Turbo Vision's `TFrame` drew a dialog's close icon at the left like any window's), its centred title slid clear of it.
- Closing the last window (`Desktop` raises `EmptiedEvent`) leaves the console showing and focused; opening any window
  (`OpenedEvent`) hides the console again -- no command that opens one checks `console_visible` itself.
- **Size/Move (Ctrl+F5) is `Window.begin_move`**, TV's `dmDragMove`: the window takes the keyboard, arrows move,
  Shift+arrows size, Enter keeps, Esc puts it back, every other key swallowed (`Window.on_key`, no key table). **While
  it lasts the key bar names those keys** (`Window.key_hints`; a departure, asked for: TV said nothing). A subclass's
  `render_after` must call `super()` (`Manager`'s does).
- **Closing asks** through `Window.must_ask`/`ask_to_close` (`Valid(cmClose)`), which `request_close`, Close all and
  Alt+X all go through.
- **Window > List (Alt+0) is DN's *Windows Manager*** (`cmWindowManager`, `dlgWindowManager`;
  `navml/widgets/window_manager/` and `window_list/`): windows top first, named by `Window.list_name()` (`cmGetName`; a
  file manager is `File Manager left,right`, each cut to 20, as DN's was); OK switches, Close closes while the dialog stays up.
- **Tile, Cascade, Close all** are DN's `TDesktop.Tile`/`Cascade` and `cmClearDesktop` from `DNAPP.PAS`; every window is
  arranged unless it says `tileable: False` (on by default, where DN's `ofTileable` was opt-in).
- `Desktop.keys` holds the window keys; `navml/commands.py` holds the window command set `Desktop` runs.
- **Every window has a `number`** (TV's `TWindow.Number`): `Desktop.open()` gives the lowest of 1..9 free, kept while
  raised, 0 for a tenth and again once closed. A close renumbers the rest 1..n in order (`Desktop._renumber`, a
  departure: TV left the gap, which the window strip made read as a fault), a tenth taking the freed 9. **Win+1..9 is `SelectWindow(number)`** (TV's `cmSelectWindowNum`, whose
  Alt+digits DN commented out for its quick directories) and Win+0 the list, which prefixes each row with its number.
  Only a kitty-protocol terminal sends Super (Ghostty does; xfce4-terminal and other VTE ones never do), and desktops
  (GNOME, KDE) grab Super+digit for their dock by default -- so **Alt+Shift+F1..F9** are bound too, which every
  terminal sends, and **a digit in the Window list** (`WindowList.on_key`) chooses that window outright: Alt+0, 2.
- **`Desktop.open_windows`** is the reactive tuple of windows (the children list is not), replaced on open and close,
  not on raise -- what anything showing all the windows reads.
- **`WindowStrip`** (`navml/widgets/window_strip/`, Python alone) paints a desktop's numbered windows as chips, the top
  one `::chip:selected` (the number is `::number`), and a click activates (the wheel anywhere over it steps to the next/previous number, wrapping); `labels` adds `Window.short_name()`
  (`list_name()` unless a window says it shorter -- Manager its directory's last part, viewer/editor the file name),
  cut evenly when short of room, then the rest counted as `+k`; `align: "right"` keeps them to the far end. Nothing
  under two windows. Navigator's `Shell` floats it on the menu bar between the last menu and the clock, right-aligned
  against the clock, under Interface's *Window strip* (`interface.window_strip`: `off`/`numbers` (default)/`full`), hidden with *Hide menu bar* and under Ctrl+O. Not DN's: OSP put the number in `[■]`.
- With several file managers open, **`Shell.active_manager`** (nearest the top) is "the file manager";
  `shell.manager`/`app.manager` stay the first one. Manager > New (Ctrl+F3, `cmCreatePanel`) opens another zoomed
  `Manager` on the active panel's directory; Ctrl+F3 is on the application's table so it works with none open.

## Menus

`navml/widgets/menu/` (slots `[2-7]`): `MenuBar`, `MenuBox`, and `SubMenu`/`MenuItem`/`MenuLine` blocks -- invisible
data widgets; the tree is markup. An open menu is a modal layer. Navigator's menu is DN 1.51's `dlgMainMenu`,
transcribed into `navigator/widgets/shell/main_menu/main_menu.nml`, with every entry whose feature does not exist
greyed. F10 opens it (`OpenMenu`, `navml/widgets/menu/commands.py`): the bar's first entry, unless the active window
names its own menu as `f10_menu` -- only the editor does, its *Editor* entry dropped, as DN's editor alone had a bar
of its own. `MainMenu` (`cmMainMenu`) is the way back to the bar's first entry; the Shell handles both.

- **Every submenu has an id** (`app.shell.menu.file`, `menu.file_view`). `MenuBar`/`SubMenu` share `MenuContainer`'s
  Python API for plugins: `add_item`/`add_submenu`/`add_line` with `before=`/`after=` anchors (an entry, a caption, or
  a command), `remove_entry`, `move_entry`, `entry`, `item_for(command)`, plus reactive `hidden`/`disabled` on every
  entry. `path_to(command)` is the shown entries down to the item asking for it (the bar's spliced-in window menus
  included, hidden ones never; the exact instance first, then its class) -- what the key bar's tooltips read.
- **A bar caption's tooltip** is its entry's `tooltip` (markup `tooltip:`, translated) plus its `Alt-<letter>`
  (`MenuBar.tooltip_at`); a window menu joining the bar brings its own. Give a new top-level menu one.
- **A menu box row's tooltip** is its entry's `tooltip` (`MenuBox.tooltip_at`), shown over the open menu. Write one
  only where the caption does not explain itself (*Panelize command*, *Optimal fill*); most items have none. A
  greyed row adds why on a line of its own (`MenuBox.hint`, the command's `refusal`). While a menu is open the key
  bar shows the highlighted row's hint (`MenuBar.hint()`); never a tooltip that only repeats the caption (a test
  sweeps for it).
- **A submenu can show a key**: `SubMenu.key_command` names a command that opens its entries some other way, and
  `MenuBox` paints that command's live key (`key_caption`, else `SubMenu.key`) just before the `►` -- a departure,
  TV's submenus had none. Display only; choosing the entry still opens the submenu.
- **A menu tick** is navkit's `Widget.checks(command)` (True/False/None), asked of the same widget `enables` is
  (`Application.command_checked`); `MenuBox` paints `√` (`+` in ASCII) in the blank column left of the caption, so a
  tick costs no width. A `MenuItem` with `ticked` set is ticked whatever its command says -- for a popup's choices,
  which have no command to ask (Alt+B's current order).
- **A window's own menu joins the bar while it is in use**: `SubMenu` children of a window join through
  `MenuBar.context`, which `shell.nml` binds to the desktop's active window, each placing itself with `before:`/`after:`.
  The viewer's *View* and the editor's *Editor* menus go after *File*.
- **Panel is the file manager's own menu** (`manager.nml`, `manager.panel_menu`, after *Utilities* only while a file
  manager is active); *Directory tree*, *Info* and *Quick view* moved into it from *Manager* (under *Other panel*) --
  a departure; *Manager* stays global for *New*.
- **Every box fits an 80x25 screen** (at most 22 entry rows under the bar; `test_every_menu_box_fits_an_80_by_25_screen`
  measures the bar's, Panel's, the viewer's and the editor's). A departure in how, not what: DN's own entries stay
  at the top in DN's order, and additions go into submenus -- Panel > *Display*/*Selection*/*Other panel*, File >
  *Multi-rename*/*Archive*/*Encoding* (UU, Checksums, Encryption), the viewer's View > *Mode*/*Filters*, the sync
  window's Synchronize > *Show* (measured in `test_compare_dirs.py`). A new entry that would overflow a box joins or
  makes a submenu; a box filled at run time from a long list scrolls.
- **A popup menu** is `PopupMenu` (`TMenuPopup`): one `MenuBox` anywhere, run like a dialog -- spawn
  `execute(app)`, which answers the `MenuItem` chosen or None; a command-less item is a choice, not greyed. `keys=`
  adds keys that close it on the selected entry (enabled or not), setting `pressed` and `selected`, for a caller that
  acts and reopens -- in a nested box the entry is that box's; `submenu=(index, current)` reopens with the first
  box's entry *index* dropped and *current* selected in it; a `SubMenu`'s own `footer` goes in the frame of the
  nested box it opens (a bar's boxes ignore it). `title=`/`footer=` go centred in the first box's top/bottom frame, widening it (`measure`
  takes both). The bookmarks box is its first user (`navigator-bookmarks`). A `SubMenu` entry opens a nested
  box beside it (Enter/Right/click; Esc/Left closes the top one), `MenuSession`'s way; `box` stays the first box,
  `boxes` is the stack, and the answer is the item chosen at any depth (`navigator-user-menu`).
- **A context menu** (right click, Menu key, Shift+F10; a departure, since DN had none) is a `ContextMenu` from a
  `ContextMenuHost`'s `context_menu()`, run in a `PopupMenu` at the pointer. Its choice runs with `start=host`. A
  right press is delivered first, then offered again as navkit's `ContextMenuEvent`, so a widget that uses the right
  button keeps it; one that captures the press for a drag (the editor's ruler) opens the menu itself on a release
  that never moved, `open_on_click(host, ContextMenuEvent.of(press))`. A component (`InputLine`) cannot take the mixin and writes the handlers out. A `ContextMenu` never
  joins the bar. See `reference/menus.md`, *A widget's context menu opens where the user points*.
- **A `MenuBox` opened shorter than `measure()` scrolls** (a departure; TV boxes never outgrew the screen): `top` is
  the first entry shown, a plain attribute `scroll()` derives from `current` while painting and in `entry_at` -- never
  assign it. `▲`/`▼` on the frame mark hidden entries. `move(n)`/`page(n)` move without wrapping, unlike `step`.
  `PopupMenu` cuts one to the screen; the bar's `MenuSession._drop` cuts one to the rows below the bar (never over
  it), a nested box opening beside its entry's *shown* row. Both: PgUp/PgDn, and the wheel moves the top box.
- **A `filterable` submenu's popup box filters as it is typed in** (`SubMenu.filterable`, a departure for long
  unmarked lists: *Open with*'s *Other applications*). `PopupBox.filter` is the text; the first printable key (Space
  only once there is text) shows its line under the top frame -- `head()` is then 1, which `rows()`, `entry_at` and
  painting skip -- and `entries()` keeps captions holding it, any case, lines dropped. Backspace edits, Esc or a press
  on its `×` empties it (Esc closes only an empty one); marked letters do not choose there. `set_filter` keeps the
  selection's entry if shown, and fits the box: `opened_height` empty, else up to `room` (one row more, as the screen
  allows). `PopupMenu.cursor_position` puts the caret at the text's end.
- **A `centred` submenu's popup box** (`SubMenu.centred`) opens in the middle of the screen's height, beside its
  entry still, and `set_filter` keeps it there as it shrinks or grows.
- **The command palette** (Alt+Shift+P, ≡ > *Command palette*; `OpenCommandPalette`; a departure, asked for --
  DN had none) is the main menu, searchable. `CommandPalette` (`navigator/widgets/shell/command_palette/`)
  `gather`s from `behind` -- `app.focused` recorded by `Shell.command_palette` **before** the box opens, as
  `MenuBar.open` records it -- every `MenuItem` with a command under `app.shell.menu.entries()` (so the context
  window's menus join, hidden ones do not; title from the live-translated `text`, key from `menu_box.key_caption`),
  then each titled command in `app.bindings(behind)` whose **class** no item holds (the editor's Ctrl+A, the macro
  slots; a key's variant of an item's command, Alt+F6's *Ren*, is left to the item). Enabled and the reason are
  `command_enabled`/`command_disabled_reason` from `behind`. `narrow` ranks by `navml/fuzzy.py` (subsequence,
  word-start/consecutive/prefix bonuses, gaps cost), the menu path at a third, menu order between equals. The
  filter line keeps the keyboard; Up/Down/PgUp/PgDn go to the list (`CommandList.row_selected` shows its cursor
  while the dialog holds the focus). Enter on a greyed row stays, the hint saying why; the answer is run with
  `app.run_command(command, start=behind)`. A new command needs nothing here: a menu item or a titled key binding
  is enough.

## Read when

| Reference | Read when |
|---|---|
| `reference/windows-desktop-modal.md` | window/desktop/modal design, tile/cascade, window list |
| `reference/menus.md` | menu geometry, the modal layer, ids and the Python API, context menus |
