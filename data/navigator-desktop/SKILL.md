---
name: navigator-desktop
description: Saving and restoring the desktop -- Options > Save desktop / Load desktop (DN's cmSaveDesk/cmLoadDesk, SaveDesktop/RetrieveDesktop), navigator/lib/config/desktop_state.py (snapshot, save, load, restore), the SavedDesktop model, and Startup's Autosave desktop (save on exit in Navigator.on_stop, restore in on_start, the command line's directories winning). Use when changing what a saved desktop keeps or when it comes back.
---

# The saved desktop

- **What it is**: DN streamed every window to `DN.DSK`; here `navigator/lib/config/desktop_state.py` makes a dict --
  `{"version", "windows": [...bottom to top], "front": index}` -- kept as JSON in the `SavedDesktop` model
  (`desktops` table, one row a name, `default`). A `version` other than `VERSION` is not read.
- **What a window keeps** (`_window`): its rectangle (`file_history.window_values`, put back by `place_window`), and
  - `Manager`: per panel `path` (a *Find:* listing's origin -- a departure: DN's `TFindDrive.Store` kept the listing whole; an archive's own directory, the cursor on it), `local`
    (where a panel on another drive falls back to), `view_mode`, `sort_mode`, `sort_reverse`, `show_hidden`,
    `show_info`, `file_mask`, `columns`, `display`, `cursor` (entry name, via `_return_to`); `active` side, `split`
    (the divider), `hidden` side, `view` standing in (tree/quick/info, put back through `switch_view` after the
    active panel is focused), `miller` (path, cursor, side); and from `_manager_extras`: `view_focused` (the view had
    the keyboard, read off `_saved_focus` for a manager behind another), `collapse` (DN's `OldBounds`: `_collapse`'s
    `before` rectangle, widths and `exact` -- untouched since the hide) and `view_zoom` (Alt+Z's zoom over the hide).
    **These three go back after `place_window`** (`_manager_placed`): the hide in `_manager` ran on the unplaced
    window, so `_collapse` is stamped again on the placed one, `before` scaled as the rectangle is, and `after` the
    placed (unzoomed) rectangle only when `exact`. `place_window` zooms first and then sets `_restore`, since zooming
    sets aside the rectangle the window has;
  - `EditWindow`: `path` and `state` -- `EditWindow.desktop_state()`, DN's `TFileEditor.Store`: cursor, scroll,
    markers, margins and every mode (`DESKTOP_MODES`; not insert mode, not the block), whatever *Track editing* says,
    put back over the file's record by `restore_desktop_state` (`Awaken`); an older entry without `state` opens on its
    path alone. SmartPad as SmartPad, not stamped again (`open_smartpad(stamp=False)`). A file gone is left out (a
    departure: DN reopened it empty under its name, which F2 would save over a deleted file's name). And `view_of` -- the
    index of the earlier window on the same text, for a Window > *New view* -- which `restore` makes again with that
    window's `open_view()` rather than a second document (`made_at`); `FileWindow`: `path`,
    `mode`; `TreeWindow`: the directory and hidden; `VolumesWindow` (`kind="volumes"`): `all` and `free`; `CalculatorWindow`: the expression; `CalendarWindow`: only that
    it was open (it comes back on today);
  - `DBWindow` (`kind="database"`, DN's `TDBViewer.Store`): its own `kept_state()` -- `path`, `source`
    (`dbf`/`sqlite`/`csv`), `record` in the file's order and `field`, `top`/`first_field` (unsorted only), `widths`,
    the F7 `search`; dBase's `codec` only when Shift+F6 chose one over the file's (`DBFile.detected`), SQLite's
    `table` or `query` (`SQLTable.sql`), a CSV's `dialect`. An F8 sort is not kept (re-sorting reads every row at
    start), and a window on a fetched copy (`use_set`) is left out, as DN dropped `KillAfterUse` files.
    `_database` reopens through `open_database`/`open_sqlite(table=, query=)`/`open_csv(dialect=)`, with no
    *Tables* box; `restore_state(kept)` runs after `place_window` and a layout, so the scroll clamps to the real
    height. A table dropped or a query refused (`DBFError`, a `ValueError`) leaves it out silently.
  Anything else is not kept. A window that cannot be made again (a file or directory gone) is left out.
- The trash can's showing and place are kept too (`snapshot`'s `trash`), as `SaveDesktop` wrote them.
- **Save desktop** (`SaveDesktop`) writes over the saved one. **Load desktop** (`LoadDesktop`) says *No desktop has
  been saved* with none, else closes every window as Close all does (`close_all_asking`; a Cancel keeps the desktop)
  and `restore`s.
- **Startup's *Autosave desktop*** (off by default; a departure: DN restored `DN.DSK` at every start whenever there was
  one) saves in `Navigator.on_stop` -- the windows are still open there, as quitting only asks -- and restores in
  `on_start`, replacing the file manager the start opened once a manager has come back. Directories given on the
  command line (`Navigator(given=True)`) go to the first manager restored, its cursors dropped.
- **The topmost manager's active panel opens in the current directory** (`restore(here=)`: the start directory, or
  the active panel's for Load desktop) unless Startup's *Preserve directory* is ticked -- DN's `TFilePanelRoot.Store`
  wrote that panel's drive as nil. Decided at restore rather than save, so the saved directory is never lost.
