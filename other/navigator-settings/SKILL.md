---
name: navigator-settings
description: Navigator's settings -- navigator/settings.py (SETTINGS, Section, Setting, the DN-record sections), navigator.ini under $XDG_CONFIG_HOME/navigator, load_settings and --config in __main__.py, flag/env/ini/default precedence, saving one section through navml's Coder, and the Options setup dialogs in navigator/widgets/setup/ (System, Startup, Interface, Confirmations, Editor/Viewer, File Manager Setup, New Manager defaults). Use when adding a setting, reading one from a widget, or changing a setup dialog.
---

# Settings and navigator.ini

`navigator/settings.py` holds **`SETTINGS`**, the one `Settings` instance, a module singleton like `navml.history.HISTORY`.
It is a container of sections, `SETTINGS.interface.clock`, `SETTINGS.confirmations.erase_single`, and so on.

## The file

- **Where it lives.** `$XDG_CONFIG_HOME/navigator/navigator.ini`, or `~/.config/navigator/navigator.ini`; a relative
  `XDG_CONFIG_HOME` is ignored. `--config PATH` overrides both.
- **Startup.** `main()` calls `load_settings()`:
  - a missing file is written with every default, then read
  - a value that will not parse keeps its default, with a stderr warning before the screen is taken
  - a file that is not ini at all, or cannot be written, means defaults for the session
- **No disk in `Navigator.__init__`.** Loading happens only in `main()`, so tests that build `Navigator` directly never
  touch the disk.
- **An ini file is a departure.** DN kept a binary `DN.CFG` of tagged records (`DNUTIL.PAS` `WriteConfig`). The module
  docstring records why.
- **A setting's `doc` is also its tooltip** on the setup page: a check box group seeded with `to_bits(Data.GROUP)`
  sets `.tooltips = Data.tooltips(Data.GROUP)`, and any other control seeded from `self.section.NAME` sets
  `.tooltip = self.section.tooltip("NAME")` (a field's line shows its field's, plus the whole text while cut). Both
  go through `tr`, and `navigator/locales/__init__.py` yields every setting's doc for the catalogues. So a new
  setting needs a doc that reads as a sentence, and `tools/i18n.py extract` then a translation.
- **Writing.** `Settings.render()` writes through `navml.coder.Coder("ini")`, and `save()` writes it atomically
  (`mkstemp` in the same directory, then `os.replace`).
- **`save(section=name)` re-reads the file first** and replaces only that section. A hand edit made while nav runs
  survives a dialog's OK.
- **What survives a save, and what doesn't.** Unknown keys and sections are kept verbatim (`Settings.extras`). Comments
  written by hand are not: the generated ones replace them.
- **Layout.** A section's comment goes on the line right under its `[section]` header. An option's comment goes on the
  option's own line, starting at `COMMENT_COLUMN` (44), or two spaces after a longer `key = value`.
- **No ` #` or ` ;` inside a value.** The parser is built with `inline_comment_prefixes=("#", ";")` so that those
  comments are stripped when reading. That also means everything from ` #` or ` ;` on is read as comment.

## Precedence

For `[appearance]`, the order is **flag > `NAVKIT_*` environment variable > ini > built-in default**.

- The argparse defaults for `--theme`, `--palette`, `--colors`, `--glyphs`, `--marks` and `--dim-modal` are `None`, so the code can tell
  whether a flag was given.
- The ini's palette, colours and glyphs go into `TerminalInfo.detect()` as its defaults, which lets `NAVKIT_PALETTE`,
  `NAVKIT_COLORS` and `NAVKIT_GLYPHS` still override them. A stated depth also outranks `NO_COLOR` (no-color.org defers
  to user configuration) but never colours a plain (`dumb`/non-tty) terminal.
- A flag is applied over that result. It is session-only and never saved.
- An unknown theme in the ini warns and falls back to `default`. An unknown `--theme` is still an argparse error.

## Declaring a setting

- **Declare it as a field.** A section is a `Section` subclass whose fields are `Setting(default, doc=...,
  choices=..., aliases=...)`, a `navkit.reactive.Reactive` subclass. The schema comes from the class:
  - the attribute name is the ini key
  - the default's type (bool, int or str) is how the value parses
  - `choices` limits a string
  - `doc` is the comment written above the key
- **A setting is added with the code that reads it** -- and with a control (*Every setting has a control*, below).
  There is no "stored, not yet read" state: the `honoured=False` flag that marked one went once every setting was read.
- **Field order matters.** Fields keep DN's dialog order. Tuples on the class (`OPTIONS`, `BEHAVIOR`, `DISPLAY`, ...)
  list a `CheckBoxes`' items in bit order. `to_bits(names)` and `from_bits(names, value)` convert between those fields
  and `CheckBoxes.value`. A departure's checkbox goes last, so the original options' bits stay put:
  `[editor] show_options` / `[viewer] show_options` (the option strip, on by default, bound live by the windows'
  markup as `SETTINGS.editor.show_options`). `show_hidden` in both sections has no checkbox (as `syntax_highlight`);
  it seeds each new editor/viewer, which Editor > Options / View switch.
- **Sections are named after DN's records**, the dialogs after DN's `dlg*` resources, and the commands after DN's `cm*`:

| Section | Class (DN record) | Page (`navigator/widgets/setup/`, DN's dialog) | Command (opens that page) |
|---|---|---|---|
| `[appearance]` | `AppearanceData` (the flags) | only `colors` and `marks`, on `InterfacePage` (*Colours*, *Marks*) | `InterfaceSetup` |
| `[system]` | `SystemData` | `SystemSetupPage` (`dlgSystemSetup`) | `SystemSetup` |
| `[startup]` | `StartupData` | `StartupPage` (`dlgStartupSetup`) | `StartupSetup` (`cmStartup`) |
| `[interface]` | `InterfaceData` | `InterfacePage` (`dlgInterfaceSetup`) | `InterfaceSetup` |
| `[confirmations]` | `ConfirmsData` | `ConfirmationsPage` (`dlgConfirmations`) | `SetupConfirmation` |
| `[editor]` + `[viewer]` | `EditorDefaultsData`, `ViewerDefaultsData` | `EditorDefaultsPage` (`dlgEditorDefaults`) | `EditorDefaults` |
| `[file_manager]` | `FMSetupData` | `FMSetupPage` (`dlgFMSetup`) | `FileManagerSetup` (`cmFMSetup`) |
| `[panel_defaults]` | `PanelDefaultsData` | `FMDefaultsPage` (`dlgFMDefaults`) | `FileManagerDefaults` (`cmFMDefaults`) |
| `[drive_info]` | `DriveInfoData` | `DriveInfoPage` (`dlgDriveInfoSetup`) | `DriveInfoSetup` |
| `[column_defaults]` | `ColumnDefaultsData` (`ColumnsDefaults`) | `ColumnDefaultsPage` (`dlgColumnsDefaults`) | `ColumnDefaults` (`cmColumnDefaults`) |
| `[savers]` | `SaversData` (`TSaversData`) | `SaversPage` (`TSaversDialog`, built in code in DN) | `SaversSetup` (`cmSaversSetup`); ≡ > Screen rest is `ScreenRest` |
| `[country]` | `CountryData` (`CountryInfo`) | `CountryPage` (`dlgCountrySetup`) | `CountrySetup` (`cmCountrySetup`) |
| `[uucode]` | `UUCodeData` (`TUUEncodeData`, `UUDecodeOptions`) | `UUEncodeDialog`, `UUDecodeDialog` (`dlgUUEncode`, `dlgUUDecode`, under `file_ops/`) | `UuEncode`, `UuDecode` -- saved by `Manager._keep_uucode`, not `Shell.setup` |
| `[checksum]` | `ChecksumData` (not DN's) | `CalculateChecksumsDialog` (under `file_ops/`) | `CalculateChecksums` -- saved by `Manager._keep_section`, not `Shell.setup` |
| `[highlight_groups]` | `HighlightGroupsData` (`CustomMask1`..`5`) | `HighlightPage` (`dlgHighlightGroups`) | `HighlightGroups` (`cmHighlightGroups`) |

`FMSetup` would be handled by `on_f_m_setup`, which is why those two commands are spelled out.

**DOS-only items are left out** of both the ini and the dialogs:

- XMS/EMS
- the video modes
- overlays
- Int28
- the CD player
- the per-drive list
- *"Fast" command execution* and *Advanced copy*
- *Enable blinking* and the *Timeslicing* group
- the *Drive line*, *Alt/Ctrl difference*, the *Quick search* key, and `descript.ion` descriptions

The keys an older `navigator.ini` may still hold are listed in `settings.OBSOLETE`. `Settings.load()` drops them
without a warning, so the next save leaves them out of the file. Unknown keys, by contrast, are kept as extras. A
choice that was renamed (`sort_by = group`, `left_panel = drive`) is mapped by `Setting(aliases=...)` and written
back under its new word. DN's *~D~rive* is *File ~p~anel* on *New Manager defaults*: `d` is *~D~etailed*'s there,
and every letter of *Files* is taken on the page.
- *Restore screen mode*
- the VGA palette boxes
- *OS-dependent disk access*
- *Clear read-only from CD*

Printer, Mouse and Terminal stay greyed in the menu.

**Defaults are DN's** (`STARTUP.PAS`) except where Navigator already behaved otherwise. Each exception carries a `#:`
note:

| Setting | Default here | DN's default |
|---|---|---|
| `show_hidden` | on | off |
| `hide_menu_bar` | off | on |
| `bs_upper_dir` | on | off |
| `sort_by` | name | extension |
| `line_divisor` | lf | crlf |

## The dialogs

- **Help**: each page names its section of `docs/en/settings.md` (`class help_topic: "settings.md#system"`), and
  the dialog has OK, Cancel and Help (`navigator-help`, *Settings*). A new setting gets a line in its page's
  section there; a new page, a section and the `class help_topic` line.
- **One dialog, a page per section.** Options > Settings (`SettingsDialog`, `navigator/widgets/setup/settings_dialog/`,
  command `Settings`) holds the thirteen setup pages behind navml's `TabView`. Each menu item under Options >
  Configuration and Options > File Manager, and its command, still exists and opens it on its own page
  (`Shell.settings(tab)`). This is a departure: DN had a resource to each. Colors and Key bindings stay dialogs of
  their own.
- **A page's controls say which setting each edits: `key: "temp_dir"`** (`"remote.upload_changed"` for another
  section), on a page whose root is `XPage(SettingsPage):` with `class section_name: "system"`
  (`navigator/widgets/setup/settings_page.py`).
  - In `built()`, `SettingsPage` seeds each keyed control's value and tooltip.
  - `accept()` reads them back: flat for one section, `{section: {...}}` for several.
  - The conversion comes from the control's kind and the setting's declaration:
    - `CheckBoxes` ↔ a bit group (`OPTIONS`) or one `bool`;
    - `RadioButtons` ↔ `choices`, by index (the page must list them in the setting's order: *Time* does not, so it
      stays manual);
    - `MaskedField` ↔ `int`, padded to the mask's 9s, a blank place counting as nought;
    - `Field` ↔ `str`, stripped.
  - A control needing more (a list made at run time, a floor, a value kept when blank) is seeded in the page's
    `__init__` after `super().__init__()` and added in an `accept()` override that starts from `super().accept()`.
  - Every page is a `SettingsPage`. System, Startup, Confirmations, Drive info, Panel defaults and Column defaults
    are wholly keyed. The others key what fits and keep the rest:
    - Interface: the run-time lists, and History size's floor of 1;
    - Editor/Viewer: the fallback encoding, and Tab's floor of 1;
    - Country: *Time* in DN's order, and the custom date kept when blank;
    - Communications: the connect timeout's floor of 1;
    - File Manager Setup: the tag character and the Miller width;
    - Tools: the identities and the service manager;
    - Savers: the two lists;
    - Highlight: one shared tooltip, and the masks tidied;
    - Viewer types: the masks tidied.
  - A one-box `CheckBoxes` for a `bool` gets the tooltip as the box's own (`tooltips = [doc]`) and as the cluster's.
  - `RadioButtons` get `sel` with `value`, so the keyboard starts on the choice made.
- **What a page does.** Each is a two-half component on a plain `Widget` (`*_page/`, `XPage`), laid out as the dialog
  it was, from `y: 1` (row 0 is the tab rule). `__init__` seeds the controls from its section (an optional section
  argument, else `SETTINGS.<name>`). `accept()` returns `{key: value}`. `EditorDefaultsPage` covers two sections and
  returns `{"editor": {...}, "viewer": {...}}`; its editor cluster is 16 boxes in 8 rows since *Tab key inserts
  tabs* and *Line numbers* (`insert_tabs`, `line_numbers`, kept before `show_options` so the strip's box stays last;
  *Line numbers* has no hot key, every letter of it being taken on the page). Its tab caption (`title`) is given by `settings_dialog.nml`, where a
  literal is translated live.
- **Pages by id.** `settings_dialog.PAGES` maps each page id (`interface`, `editor_viewer`, ...) to its sections, and
  `SECTIONS` lists them all. Reach a page's controls as `dialog.interface.options` or `dialog.page("interface")`.
  **Every setting has a control** (no section is the ini file's alone): *Interface* also answers `[appearance]
  dim_modal` (*Dim behind dialogs*, applied at once in `Shell.settings`, a flag still winning for its session);
  *Viewer types* (`viewer_types_page`, `("viewer",)`, merged with *Editor/Viewer*'s half) the seven `render_*`
  switches and their masks and `database_masks`; *Tools* (`tools_page`, four sections by name) `[encryption]
  age_identities`, `[processes] refresh`, `[services] manager/refresh/journal_lines` and `[monitor] refresh` (an open
  window's next tick reads a new interval; a new manager applies at Services' next open). A setting added without
  a control says why in its section's docstring. A tab's title is short: the left-hand column is as wide as the
  longest, and the buttons' centring under the pages was shifted by a 17-letter one.
- **Size.** Its markup is 76 by 24 with boxed tabs (`settings_tabs = top`), so it fits an 80x24 terminal: one
  scrolled row of tabs over the tallest page (*Panel defaults*). With `interface.settings_tabs = left` it is 80 by 24: a column of at most 20 for the tabs, and 57 left
  for a page, which every page fits (*File panels*' second column is the tightest). There the tabs' rule runs the
  frame's whole height into its tees (`TabView.joins_frame`), and OK and Cancel are centred under the pages
  (`SettingsDialog._buttons_under_pages`, the base's `row` rebound). With `simple`, the default, it is 76 by 23
  (`settings_dialog.SIMPLE_HEIGHT`): the rule under the captions is each page's first row, a row nearer the top than the boxed tabs' baseline, so
  every page keeps the 17 rows it has.
  **The key bar says *Ctrl-PgUp/PgDn Tabs*** (`TabView.key_hints`, so every tabbed dialog; a departure, asked for):
  a tab title cannot take a letter, Alt+letter being the page's controls'.
  The Screen savers page keeps *Time* under its lists, as DN had it, with the lists three rows shorter to stay that
  short.
- **What OK does.** `Shell.setup(dialog, *sections)` spawns the dialog. For a multi-section answer it keeps only the
  sections whose values changed. It assigns those onto `SETTINGS` (reactive, so bindings repaint), then calls
  `SETTINGS.save(section=...)` for each. An `OSError` shows an *Error* box, and the values stay applied for the
  session. **A setting a window keeps as it is used** (the calculator's face, a dialog's last choices through
  `Manager._keep_section(name, values, app)`, *Setup game*, Synchronize's options) saves through
  `settings.save_or_say(section, app)`: a failure logged and toasted once a session per file -- a box per save would
  be one per click; never `contextlib.suppress(OSError)`. A changed `interface.language` is applied after (`Shell.settings`).
- **Tests.** Open the dialog with `lambda a: a.spawn(a.run_command(InterfaceSetup))`, then reach the page through
  `a.modal.interface`. Build a page alone (`InterfacePage(section=...)`) to test its seeding and `accept()`.
- **Numbers are three-digit `MaskedField`s.** Width is the label plus 5: three digits and the line's two columns.

## Reading a setting from a widget

- **Markup binds to `SETTINGS`**: a line reading an imported instance or module is followed even when it reads nothing
  of its widget (`navml-markup`), so `visible: SETTINGS.interface.clock` in `shell.nml` follows Interface's *Clock*, as
  the key bar's, the command line's, the menu bar's and the window strip's lines do.
- **The menu bar comes after the desktop in `shell.nml`** so a floating bar paints over it. Its `width`/`height` are
  bound to the top row, which docked or floating it keeps; its `inline_style` (`dock: top` or `dock: none`) and its
  `visible` (`not hide_menu_bar or current >= 0`) are lines there too.
- **A per-widget value is seeded, not bound**, for example `Panel.show_hidden` (Ctrl+H toggles it) and
  `FileEditor.tab_size`. Read it in `__init__` after `super().__init__()`.
- **An operation reads the setting when it runs.** For example, `Manager.delete_files` reads `confirmations.erase_*`,
  and `Navigator.on_quit` reads `confirmations.exit`.

## Honoured now

| Setting | Effect |
|---|---|
| `system.internal_viewer` / `internal_editor` | Off: F3/F4 run `viewers.ini`/`editors.ini`'s entry for the file, else `$PAGER` (default `less`) / `$EDITOR` (default `vi`) on the console; Alt+F3/Alt+F4 do the other (`navigator-user-menu`) |
| `system.show_hidden` | A new panel's `show_hidden` |
| `system.temp_dir` | `navigator.lib.system.tempdir.temp_root()`, read each time: the user menu's private directory and the subshell's rc files; empty is `$TMPDIR` |
| `system.system_clipboard` | On (a departure: DN's default was off): copies go to OSC 52 and the desktop's tool, pastes read them. Off: `Application.system_clipboard` false, a clipboard private to Navigator (`Shell._choose_clipboard`, an effect) |
| `system.flush_buffers` | Copy and a cross-device move `fsync` each file written (`CopyRequest.flush`, set by `CopyDialog.accept`) before it counts as done or a move deletes its source; a sync error fails that file like a write error. `EINVAL`/`ENOTSUP` (a file system with nothing to sync) is not an error. A rename-move writes nothing, so syncs nothing. A departure: DN flushed once, at the end (`int 21h` `0Dh`, *Flushing buffers...*), after a move had deleted its sources |
| `system.internal_terminal` | Off: Ctrl+O hands the real terminal to the shell, as Midnight Commander does, and commands from the line run there (a departure: not DN's; `console-command-line` has the mechanism). Also a System Setup box, *Use internal terminal* |
| `system.command_window_zoomed`, `system.command_window_modal` | How a command run in a window of its own opens (`&cmd`, Shift+Enter, a user menu item's `<&` without its own words): zoomed (default on) or 80×24, and modal (default off) or one among the windows (a departure; `console-command-line`, *Commands in a window*). System Setup's *Command windows zoomed* / *modal*, the 7th and 8th bits of its *Options* box, which grew to four rows into the one that was spare |
| `confirmations.close_command_window` | Ask (Yes/No) before closing a command window whose command is still running -- the close icon, Ctrl+F4, Close all and Alt+X (`TerminalWindow.must_ask`). Default on. A departure; Confirmations' *Close command window*, its tenth box |
| `system.on_error` | `dialog` (default): an unexpected exception opens `ErrorDialog` (`navigator/widgets/shell/error_dialog/`) with the traceback, *Continue*, *Copy* (the whole traceback to the clipboard) and *Quit*. `crash`: Navigator quits, printing the traceback once the terminal is restored, and exits with status 1. `--on-error` overrides it for the session. Either way, `Navigator.log_error` appends the failure to `errors.log` beside the database (`navigator/lib/system/errorlog.py`, opened by `main()`, which also points `faulthandler` at it). A second failure while the box is up quits. A departure: DN had Turbo Pascal's *Runtime error*. Shown in System Setup as *Unexpected failures*. Tests run with `crash` (conftest) |
| `system.stall_report` | Seconds (default 2, 0 off) the frame loop may stay on one batch before `errorlog.Watchdog` writes a `STALL` entry to `errors.log` (`navkit-widgets-input`, *Failures*). A departure, not DN's. The watchdog thread reads a plain `threshold`, which `Navigator._follow_stall_report` (an effect) keeps in step, so a change applies at once. System Setup's *Report a stall after*, a three-digit `MaskedField` |
| `system.notifications` | `auto` (default: the terminal's guessed way, `TerminalInfo.notifications`), `terminal` (that OSC, else OSC 9), `notify-send`, `off`: how a long `_watch_job` operation's end, or its waiting question, is told to the desktop -- only while the terminal has reported it lost the focus (`Shell.notify_away`; `navigator-file-ops`, *In the background*). A departure, not DN's. On *Communications*' page beside *Desktop integration*, which answers `system` too |
| `interface.clock`, `interface.hide_status_line` | Clock and key bar visibility |
| `interface.hide_menu_bar` | The desktop takes the top row; the bar floats over it only while a menu is open |
| `interface.hide_command_line` | The desktop takes its row; it takes no keys (but a Shift+character starts the panel's quick search, as DN's did), and its commands (Enter, Home, End, Tab, Ctrl+Enter) are disabled so those keys go to the panel; a paste and Commands history's *Drop* put nothing on it, and text it holds never takes the panel's keys (Space, Del, the Gray keys: `Manager._command_line_has_text`, Space's `enables`) |
| `interface.auto_hide_command_line` | The line shows only while it holds text; typing, and Shift+Up/Down's recall, still go to it and bring it back (DN 1.51 never read this bit -- transcribed from `CheckSize`/`ToggleCmdLine`) |
| `interface.esc_user_screen` | Esc with an empty command line shows the user screen until any key or click (Alt+F5's `UserScreenPeek`, `Shell.show_user_screen`), DN's `cmShowUserScreen`; with Ctrl+O's console up it stays; Esc on a line with text clears it, and does nothing with the line hidden |
| `interface.block_insert_cursor` | The command line's caret is a block (`Shell:block_insert { caret: block }` in `navigator.nss`; on `Shell` because it answers `cursor_position` for the line). Unticked, the terminal's own shape |
| `interface.track_viewing` / `track_editing` | On (a departure: on by default): viewers/editors are recorded and restored, and Alt+PgDn / Alt+PgUp list them; off, the lists say DN's `dlSetViewHistory`/`dlSetEditHistory` (`navigator-viewer`, `navigator-editor`) |
| `interface.store_viewer_position` | On (a departure, as the Track pair): a tracked file reopens in the viewer at its recorded window rectangle, scroll and cursor. Off, it is still recorded and listed and its mode/wrap/filter still come back, but it opens at the top in a fresh window. Without Track there is no record, so nothing to restore |
| `interface.store_editor_position` | On (a departure, as the Track pair): DN's `ouiStoreEditorPosition` -- a new editor opens at the last editor window's rectangle (`TempBounds`, the `window_bounds` table), scaled; off, the whole desktop. A tracked file's record (rectangle, scroll, cursor, modes) comes back under *Track editing* alone, either way (`navigator-editor`) |
| `interface.track_directories` | On (a departure, as the Track pair): each directory a panel comes to goes first into the `directories` history, Alt+Backspace's list; off, Alt+Backspace says DN's `dlSetDirHistory` (`navigator-panels`) |
| `startup.autosave_desktop` | Off by default: on, the desktop is saved on exit and restored at the next start (`navigator-desktop`); DN restored it at every start |
| `startup.auto_user_menu` | F2's user menu opens once the start's desktop is in place (`Navigator.on_start`, DN's `RunMenu`) |
| `startup.clear_history` | `main()` calls `clear_histories()` before the screen is taken: every unpinned input-line, command and directory history entry and view/edit record goes; pinned ones stay (`ClearHistories`) |
| `startup.inactivity_exit` | An hour with no key, click or paste (`Navigator.idle_exit_after`, looked at every `idle_check_every`) exits without asking, or runs `$DNIDLE` instead when it is set (`ExecExit`). Not while a command runs on the console, and (a departure) not while an editor holds a changed text. Pointer motion alone does not count, as it never reaches `on_event` |
| `startup.preserve_directory` | Off (DN's): after a command the active panel follows the shell's directory (`Shell._follow_shell`), and a restored desktop's topmost manager opens its active panel in the current directory -- the start one, or the panel's for Load desktop (`desktop_state.restore(here=)`). On: it keeps its own. DN decided at `Store`; here at restore, so the saved desktop loses nothing |
| `interface.settings_tabs` | `simple` (default), `top` or `left`: where *Settings* puts its tabs (`TabView.side`), read as it opens. `left` widens the box to 80 (`settings_dialog.LEFT_WIDTH`) so a page keeps its width beside the column; `simple` (bare captions over a rule) shortens it to 23 (`SIMPLE_HEIGHT`). Not DN's. Interface's *Settings tabs* radio buttons |
| `interface.window_strip` | `off`, `numbers` (default, asked for; nothing shows until a second window opens) or `full`: the windows on the menu bar by number, kept to the clock's end, or with their names (`Shell`'s `WindowStrip`, see `navml-windows-menus`). Not DN's. Interface's *Window strip* radio buttons |
| `appearance.colors` | The colour depth sent, replacing detection's guess (precedence above). Interface Setup's *Colours* (a departure: DN's was the video mode); a change applies at once, over a session's `--colors` as *Language* does over `--language` (`Navigator.use_color_depth`: re-detected with the new depth, `NAVKIT_COLORS` still winning, then `redraw()`). `InterfacePage` is two-section: it answers `{"interface": ..., "appearance": {"colors": ..., "marks": ...}}` |
| `appearance.marks` | How check boxes and radio buttons are drawn (`MARK_LOOKS`: `dos`, `brackets` -- the default --, `boxes`), a departure. `main()` sets `Navigator.marks` from it or `--marks`; Interface Setup's *Marks* applies a change at once (`Shell.settings`: `application.marks`, then `invalidate()`). A `Navigator` built without `main()` -- the tests' -- keeps navkit's `dos` |
| `interface.history_size` | 50 (a departure: DN fixed 20): entries kept per history list -- `HISTORY.limit` (set by `Shell._size_histories`) and `FileRecord.store`. A `MaskedField` under Interface Setup's boxes |
| `confirmations.erase_single` | Off: one entry goes with no Delete dialog, and so no *Recursive delete* (`cfSingleErase`) |
| `confirmations.erase_multiple` | On: DN's second box, *OK to delete N files?* (or *to the Trash*), after the Delete dialog's Yes (`cfMultiErase`). The dialog for several is always shown, as DN's `ValidErase` always asked *these files?* |
| `confirmations.erase_non_empty_dir` / `erase_read_only` | Off: the eraser's question is answered Yes |
| `confirmations.create_dir` | Off: copy and link create a missing target directory without asking |
| `confirmations.exit` | On: Alt+X asks DN's `dlQueryExit` first |
| `editor.tab_size`, `editor.vertical_blocks` | Seed a new editor |
| `editor.highlight_line` / `highlight_column` | Seed a new editor's current line and column highlight (Editor > Options switches one editor's) |
| `editor.optimal_fill` | Seeds a new editor's *Optimal fill* (Editor > Options switches one editor's): blanks written as tabs on save and ^K W |
| `editor.auto_brackets` | Seeds a new editor's *AutoBrackets* (Editor > Options switches one editor's) |
| `editor.autowrap` / `justify_on_wrap` | Seed a new editor's *Auto wrap* and *Justify on wrap* (Editor > Options switches one editor's) |
| `editor.left_margin` / `right_margin` / `paragraph` | Seed a new editor's `margins` for paragraph formatting (Alt+J/R/L/C); *Format Margins* changes one editor's alone |
| `viewer.hex_mode`, `viewer.wrap_lines` | Seed F3's viewer |
| `editor.fallback_encoding` | A departure: what a file that is not valid UTF-8 is read as by the editor -- `utf-8` (default) keeps its bytes as they are, else one of `encodings.LEGACY` (`navigator/lib/codepages.py`); the Editor setup's *Fallback encoding* choice (`navigator-editor`, *Encodings*) |
| `text_conversion.*` | File > Encoding > Convert text's last choices: `encoding` (`keep` or a `CODECS` key), `ending` (`keep`/`lf`/`crlf`/`cr`), `fallback`, `keep_times` (`navigator-file-ops`) |
| `editor.line_divisor` | The terminator a text with no line break yet takes (`FileEditor.open` sets `Document.newline` from `document.NEWLINES`): a new file, an empty one, a single line. A file with breaks keeps its most common one |
| `editor.persistent_blocks` | On (DN's default): the block stays as the cursor moves and edits go round it. Off: a movement without Shift, typing, Enter, Backspace and Del unmark it (`BlockOff`) |
| `editor.overwrite_blocks` | Only with *Persistent blocks* off (DN's `(ebfPbl + ebfObl) = ebfObl`): typing and pastes replace the block (one undo), Del deletes it alone; Backspace never does |
| `editor.create_backup` | F2 (and saving on close, Ctrl+F2) keeps the old file as `NAME.bak` (`save.backup_of`); Save as and ^K W never back up, as DN's never did |
| `editor.lock_file` | Read at each `LockFile`: an editor holds its file with an exclusive advisory `flock` (`navigator/lib/editor/lock.py`) from open to close, re-taken after every save. A write to a file another program holds is refused whatever this says |
| `editor.auto_indent` | Seeds a new editor's *Autoindent* (`FileEditor.auto_indent`; Editor > Options switches one editor's): Enter's `MakeEnter` rules (`navigator-editor`) |
| `editor.backspace_unindents` | Seeds a new editor's *Backspace indents* (`FileEditor.back_indent`; Editor > Options switches one editor's): `MakeBack`'s `BackIndent` (`navigator-editor`) |
| `file_manager.drag_drop_columns` | DN's *Drag-and-drop* (`fmoDragAndDrop`, off as DN's): files can be dragged out of a panel with the mouse (`navigator-panels`) |
| `confirmations.drag_and_drop` | DN's `cfMouseConfirm`: a drop puts up the Copy dialog aimed at it; off, it copies at once in the dialog's session mode |
| `confirmations.delete_bookmark` | A departure, asked for: Del in the bookmarks box asks *Delete bookmark* first, with *Don't ask again* (`navigator-bookmarks`); `conftest` turns it off |
| `confirmations.save` | A departure, asked for: the editor's F2/Ctrl+S asks *Confirm file save* first (`navigator-editor`) |
| `file_manager.use_arrows` | On: Left/Right/Home/End edit a command line with text, Shift+ them the panel; off, reversed (`navigator-panels`). DN's expression read for its intent: as compiled (`and` before `xor`) it did the reverse |
| `file_manager.auto_change_dir` | On: a cursor resting in the manager's tree takes the active panel there (`Manager._panel_follows_tree`); off, only Enter does |
| `file_manager.beep_after_copy` | A copy or move that was not aborted rings the terminal's bell (`Application.bell`, BEL; DN's `BeepAfterCopy`) |
| `file_manager.space_toggles_selection` / `bs_upper_dir` / `del_erases` | Space tags, Backspace goes up, Del erases while the command line is empty; off, the command is disabled in `Shell.enables`/`Manager.enables` so the key falls through to the line. Shift+Backspace/Ctrl+PgUp and F8 are unaffected |
| `file_manager.column_titles` | The detailed and list modes' heading row (`Panel._follow_column_titles`, an effect, so it applies at once); the dividers stay |
| `file_manager.tag_character` / `tag_sign` | The tagged row's gutter mark: `tag_sign`'s first character (empty: `√`; `+` on the ASCII tier when it is not ASCII); off, the colour alone |
| `drive_info.*` | Each line of Ctrl+L's information panel (`diskinfo.lines`), read at every paint. The field is `directory_title`, not `title`: a field named `title` would hide the section's own `title` |
| `column_defaults.*` | A new panel's `columns` (*Disk Drive*) and each *Find:* listing's `find_columns` (*File find*), `ColumnDefaultsData.columns(listing)`. *Archives* gives an archive's `archive_columns` (`columns(False, archive=True)`, `ARC`: original and packed size,
ratio, attributes, owner, date). *TEMP:* and *TDR View* are left out as DOS-only; every box defaults on (DN's were 0, its brief panel) |
| `savers.*` | `selected` (names, commas: `star_flight`, `flash_light`, `clock`, `blackness`, or a program in `savers/` beside `navigator.ini`), `time` and `mouse`: `Navigator._check_saver` (every `saver_check_every`) calls `Shell.rest` after *Time* idle or when the pointer comes into the top right corner, never with it in the bottom right, nor while the console runs a command. Empty by default, as DN's list was; Screen rest with none selected is *Star flight* (a departure). `navigator/lib/appearance/savers.py`, `widgets/shell/screen_saver.py` |
| `country.*` | *Country support* (`navigator/lib/config/country.py`): `date_format` `european` (default, `DD-MM-YYYY`), `us` (`MM/DD/YYYY`), `iso` (`YYYY-MM-DD`) or `custom` (`custom_date`, `strftime`'s directives, empty is European); `time_format` `24h` (default) or `12h`, spelled by hand, not `%p`, in DN's two ways: **a file's stamp**
(`country.stamp`/`stamp_in`, `time_text(file=True)`: the panels, *Current file*, the info panel, the Trash, the
overwrite query, the file dialogs) is `MakeDate`'s -- a blank before a one-digit hour (` 9:05`) and one letter, ` 5:05p`
-- the day keeping its leading zero, a departure, asked for (DN blanked it in the day-first order); **the clock**
(`time_text`) is `TClockView`'s `09:05am`. `first_day` `monday` (default), `sunday` or `saturday` (not DN's, which had no calendar): `country.first_weekday()`, which `Shell.__init__` puts on `CalendarView.default_first_weekday` for every dropped calendar and the *Calendar* window's markup binds. `calendar_view` (*Calendar view*; `CountryData.VIEWS`: `only`, `gregorian_grid`, `selected_grid` default, `both`): `country.calendar_view()`, what the *Calendar* window shows beside the Gregorian until its menu chooses. `calendar` (*Calendar system*; `CountryData.CALENDARS`: `auto` default, or a `navml.calendars.SYSTEMS` key): `country.calendar_system()` resolves `auto` from `LOCALE.code` each call (`LANGUAGE_CALENDARS`, language_REGION before language: he → hebrew, ar → ummalqura, zh → chinese, zh_TW → roc, ko → korean, vi → vietnamese, ja → japanese, th → thai, bn → bengali, ne → nepali, tr → diyanet, id → mabims_id, ms → mabims_my, my → burmese, bo/dz → tibetan, km/lo → chhankitek, ps/prs/fa_AF → afghan, else gregorian), which the *Calendar* window's month binds until its menu chooses (`CalendarWindow.chosen`, kept in a saved desktop). Read at each paint by the panels' *Date* column (`DirEntry.display_date` = `country.stamp`; `Panel.detail_columns` measures its width with `country.stamp_width`, so it follows a change), the overwrite query and the clock (`shell.nml` binds its width, 5 or 7). A departure, asked for: DN had the three orders with a separator of its own; the presets carry theirs, and *Custom* replaces the separator lines. File Attributes' date is typed and read back in `country.typed_date_format()` -- the chosen order, or European where a mask cannot hold it (a name, a missing or repeated part) -- through `DateField.date_format` and `fileattr.parse_mtime(..., date_format)`; its time is `country.typed_time_format()` -- `%H:%M:%S`, or `%I:%M:%S%p` in 12 hours (`fileattr.time_text`/`parse_mtime(time_format=)`, the field two cells wider for it). The editor's *Insert date* (^Q D) writes `country.format_date`, custom included, and *Insert time* (^Q T) `country.format_time(seconds=True)`: `H:M:S` in 24 hours, `hh:mm:ssam`/`pm` in 12. SmartPad's stamp (`smartpad.stamp_text`) takes both, with the seconds (`country.format_time(seconds=True)`). navml's file dialogs' info pane writes through `FileInfoPane.stamp`, a class-level hook (DN's `DD-MM-YY hh:mm` by default) that `Shell.__init__` points at `country.stamp`, navml knowing no settings |
| `uucode.*` | What UU Encode and UU Decode open on and run with (`navigator-file-ops`); `line_ends` defaults to `lf` (a departure: DN's was DOS's CR+LF) |
| `make_list.*` | Alt+L's two boxes, `store_paths` and `auto_paths`, DN's `MakeListFileOptions` (`cfgMakeListFile`); a remembered `store_paths` is dropped for files from one directory (`navigator-panels`, *Make list*) |
| `checksum.*` | File > Encoding > Checksums > Calculate's last `algorithm` (`sha256` by default) and `mode` (`combined` or `each`) (`navigator-file-ops`) |
| `highlight_groups.*` | The five custom file-type masks (`filetypes.use_masks`, from `Shell._use_highlight_groups`): row colours and *Group* order; a change re-reads every panel. The lines are named after Navigator's groups, not DN's *Custom 1*..*5*; a mask is kept with blanks and empty patterns dropped (`DelSpaces`) |
| `panel_defaults.sort_by` | Seeds each new panel's `sort_mode` (Alt+B changes one panel's) |
| `panel_defaults.view_mode` | Seeds each new panel's `view_mode`: `simple`, `detailed` (the default) or `list` (Ctrl+Y changes one panel's). Not DN's -- *Panel mode* closes *New Manager defaults*. `conftest`'s `_default_settings` pins `simple`, which the panel tests were written against, and `tools/screenshot.py` pins it too: the README screenshot stays in the simple layout by decision, whatever the default |
| `panel_defaults.executables_first` / `archives_first` | Read at each panel read (`Panel._rescan`, untracked): those files lead by name, extension and type |
| `panel_defaults.files_highlight` | File-type row colours (`Panel.row_style`) |
| `panel_defaults.current_file` / `selected_files` | What the panel's info line (its footer) may show; neither, it is empty |
| `panel_defaults.totals` / `free_space` | DN's `TInfoView` lines under the listing (`Panel.info_lines`, parts `totals`/`free-space` and their `-numbers` on `[122]`-`[125]`): *Total: N files with B bytes* (files only, `CalcTotalInfo`) and *SIZE free on MOUNT* (read with the directory, `free_space_of`; not over a *Find:* listing). SIZE is `human_size`'s `df -h` form, `977K`/`9.5G`/`384G` (a departure: DN gave every digit); under a kilobyte it stays *B free bytes*. Free space is on by default, as DN's was |
| `file_manager.info_divider` | A `─` row over those lines, `┴` where a column divider comes down (`Panel.render_info`); the frame then takes no bottom tee. No lines, no divider |
| `panel_defaults.directory_length` | Every read counts each directory's bytes into its size (`scan_directory(dir_length=)`, `..` the one listed), on the scan thread; Esc while *Reading directory...* stops it and turns the box off for that panel, as DN's `Abort` did |
| `panel_defaults.left_panel` | `Manager.apply_left_panel`, run for Ctrl+F3's manager and the start's own (not a restored one): the right panel takes the keys and the information panel or tree stands in the left's place, or the left side is hidden (`TDoubleWindow.Init`) |

The `panel_defaults` *Display* boxes above are read live by every panel (`Panel.shows`) **until Alt+S's *Panel
Options* gives that panel its own** (`Panel.display`), a departure: DN copied *New Manager defaults* into each
manager it made.

## Tests

`tests/conftest.py`'s autouse `_default_settings` resets `SETTINGS` and points `XDG_CONFIG_HOME` into `tmp_path`, so
no test reads or writes the real file. Open a dialog in a test with `lambda a: a.spawn(a.run_command(InterfaceSetup))`.
Posting the command as an event does not reach the Shell.
