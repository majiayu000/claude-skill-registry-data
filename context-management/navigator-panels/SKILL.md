---
name: navigator-panels
description: The file manager window and its panels -- Manager (manager.nml/manager.py), Panel and DirEntry, view modes (Ctrl+Y simple/detailed/list), name scrolling, tagging (Insert, Space, Gray +/-/*, Select/Unselect group, SelectDialog), Ctrl+S quick search, Ctrl+H hidden files, type marks and icons, Backspace to parent, re-read keeping the cursor, settings and the cursor remembered per directory (directory_settings), Ctrl+F1/Ctrl+F2/Ctrl+P hiding sides, the draggable divider between the sides (Alt+Left/Alt+Right), switch_view, active/passive panel. Use when changing how files are listed, selected or navigated.
---

# The file manager and its panels

`navigator/widgets/manager/`: the `manager/` window, `panel/` (whose `panel.py` carries `DirEntry` beside `Panel`), and
`select_dialog/`. `Panel` and `MillerView` are components: `panel.nml` declares the option strip (`options`) and
`miller_view.nml` the file preview (`preview_file`); everything else is their hand-written halves'. A component's
`.py` has one base, its markup's, so `Panel` writes `ContextMenuHost`'s hooks out (`on_context_menu`,
`on_show_context_menu`) rather than mixing it in. **`manager.py` is the worked example of a converted screen**: the document holds the tree and
geometry; Python holds the keys, `active_panel` and the paths markup may not bind (`left.path`, `right.path` are seeded
after `super().__init__()` -- see `navml-markup`). `Panel` assigns `path` and lets listing, cursor and scroll follow.
`Manager.passive_panel` names the other panel. `manager.nml` holds Tab, Alt+R/Ctrl+R and F2-F8. Commands live in
`navigator/widgets/manager/commands.py`.

## Movement and reading

- Arrows/PgUp/PgDn/Home/End move, Enter descends, Ctrl+R/Alt+R re-reads. **A re-read keeps the cursor on its entry**
  (`Panel.reload`, DN's `RereadDir`); only a change of directory starts at the top.
- **Enter and Backspace work by the letters, never `resolve()`** on the loop (it stats each component: a hung mount
  froze the screen): `Panel._entered` -- `..` is `normpath(path/..)`, a link to a directory its `link_target` taken
  from here, else `path/name`; `go_up` `normpath(path/..)`. A link to a link is followed one step (a departure: the
  same directory shown by another path, as bash's `cd`). Paste and a drop resolve their target on a thread
  (`manager._real_place`; `on_dropped` spawns `_dropped`).
- **A directory is read on a thread** (`scan_directory`, on `panel._SCANNER`). `_rescan`, the effect, takes the
  cursor notes (`_return_to`, `_keep`) into a `_ScanRequest`, waits `SCAN_GRACE` (50 ms) and applies inline if the
  read is done -- nearly always, so a frame never shows a half state -- **only for somewhere new on a drive with
  `quick_listing`** (disk, archive, memory, `root:`, Trash; `_answers_here`): a re-read of the same place keeps its
  rows and never waits, and a step on a drive a round trip away shows *scanning* at once rather than 50 ms later
  (Miller's preview and PollWatch paid it every step). Otherwise it spawns `_await_scan`, which applies only
  if no later read was asked for (`_generation`). **With no application running it waits for the read**, so model
  tests' `reload()` + `settle()` still see the listing at once (and so does Navigator's first listing, before the loop
  starts). Meanwhile a re-read of the same directory keeps its rows; a new directory shows *Reading directory...*
  (`scanning`) with no rows, so nothing acts on the last directory's entries. Departure: DN blocked until the read was
  done, so keys typed meanwhile acted on the new listing; here they act on the empty one.
- `Panel.on_double_click` chooses the clicked row as Enter does -- a directory or `..` is entered, a file run or
  opened (`Panel.choose`: `ExecuteFile`/`OpenFile`) -- the press already moved the cursor. What needs
  the desktop (activating the other panel on a press, the wheel, console scrollback) stays on
  `Navigator.on_mouse_click`, which returns False while `app.modal` is set.
- **Backspace goes to the parent** (`GoParent(by_key=True)`, DN's `kbBack` under `fmoBackGoesBack`, `Panel.go_up`,
  cursor on the directory left) while the line is empty; Ctrl+PgUp (`_CtrlPgUp`) and Shift+Backspace whatever it holds, both under *BS upper dir*. Shift+Backspace goes up under *BS upper dir* too (`GoParent(backspace=True)`: DN's Shift
  test sat inside `fmoBackGoesBack`); only Ctrl+PgUp ignores the setting. Home also scrolls the names back (`DeltaX :=
  0`); PgUp/PgDn step the whole view, every row of every column (`Panel.page`, DN's scroll bar page). Shift+Enter
  (`EnterWithoutArchive`) is Enter on a file without the archive or disk-image test (DN's `ShiftState and 3 = 0`),
  in a *Find:* listing `ChangeInactive`, which Ctrl+Shift+PgDn is too (`_CtrlPgDn` with Shift); with text on the
  line it falls to the line run in a window. Ctrl+\\ (`GoRoot`, `kbCtrlBSlsh`, `Panel.go_root`) is
  `ChangeRoot`: the disk's `/`, an archive's own root (staying in it), another drive's `/`, a *Find:* listing left
  for `/`; the cursor on the first entry whatever was remembered (`_return_to = ""`), re-read when already there.
  Ctrl+PgDn (`GoInto`, `_CtrlPgDn`) is Enter on a directory, `..` or a *Find:* entry, and on a file opens it as an
  archive whatever its name (`navigator-drives`).
  At the disk's root all three read it again with the cursor on top, as DN's `_CtrlPgUp` did
  (`GotoFile(DirectoryName)`); at another drive's root with nowhere to go they only move the cursor to the top,
  a departure: DN did nothing there.
  A departure: the Backspace held or tapped to clear the line does not go on climbing once it is empty --
  `Manager.on_go_parent` swallows it while `CommandLine.holds_backspace()` says it is within `BACKSPACE_RUN` (0.6 s)
  of the last one the line took or swallowed; each swallowed one restarts the wait, so a held key never gets through.
- **Enter on an executable runs it**; Ctrl+Enter inserts the name (see `console-command-line`).
- **A read-only file system is marked in the title**: `path [R/O] [mask]` (`read_only_mark`: a lock, `icons.READ_ONLY`
  nf-fa-lock, at the Nerd tier), and the title's tooltip says *A read-only file system: nothing here can be changed*.
  `Panel.read_only` comes with each read: `_read_location` asks `_is_read_only` (`os.statvfs`'s `ST_RDONLY`) on the
  scan thread, the disk only and never over a *Find:* listing; `_apply` takes it as a fourth value. A departure, made
  for mounted disk images and CDs. Test: `tests/test_tooltip.py`.
- **Enter on a disk image mounts it** (`.iso`/`.img`, `udisks.is_image_name`; a departure, DOS had no loop devices):
  `Panel._may_mount_image` -- `[file_manager] enter_mounts_images` (File Manager Setup's *ENTER mounts disc images*,
  default on), the local disk outside an archive, a regular file, `udisks.program()` -- is asked before
  `_may_enter_archive`. `navigator/widgets/drives/disk_image.py`'s `enter_image` runs `udisks.attach_image` under
  *Mounting image*, says it in a toast titled with the image's name (*Mounted at PATH*, or *N file systems
  mounted* -- before any box asks, as Cancel leaves them mounted), and takes the panel to the mount point; with several file systems a centred `PopupMenu` (*Mount
  NAME*: label, size, mount point) asks which, Cancel staying put with all mounted. A failure is a box. Without
  udisksctl it falls back to the archive (if *Enter opens archive*) and then `OpenFile`, as before. The library side
  is `navigator-trees`' udisks paragraph. Tests: `tests/test_udisks.py` (`image_desk`).
- **Disk > *~M~ount image*** (`MountImage`, `Manager.on_mount_image`): Enter's mounting (`enter_image`) of the image
  at the cursor (`Panel.image_file`: a local `.iso`/`.img`, not in an archive or a *Find:* listing), whatever
  *ENTER mounts disc images* says; `Manager.refusal` greys it with *No disk image at the cursor* or *udisksctl
  (udisks2) is not installed*. Greyed in Miller columns. The right-click menu offers it too (no hotkey), on an image
  at the cursor that is not mounted, nothing tagged and `udisksctl` there; a mounted one gets *Unmount image*
  instead, never both.
- **Unmount image** (`UnmountImage`: the right-click menu, no hotkey -- every letter of it is taken there -- and
  Disk > *~U~nmount image* under *Volumes*, greyed by `Manager.enables` outside one):
  offered while `Panel.image_here()` answers -- the panel inside a mounted image, or (nothing tagged) a mounted
  `.iso`/`.img` at the cursor -- from `udisks.image_at` (`/proc/self/mounts` and sysfs's `loop/backing_file`, never a
  disk, so the menu asks as it is built; only mounts under `/media/`, `/run/media/`, `/mnt/`). `Manager.unmount_image` →
  `disk_image.unmount_image` takes every Manager's panels inside it back to the image file (`Panel.go_to_file`), then `udisks.eject(device)` on a thread --
  again after `UNMOUNT_WAIT` while it says *busy*, up to `UNMOUNT_TRIES`, the shell's `cd` out taking a moment --
  then a toast *Unmounted*, or a box. Greyed in Miller columns.

## Auto refresh (`[file_manager] auto_refresh`)

- **A panel watches the directory it shows** (the watch set up on the scan's pool, `_watch_directory`: the Trash's
  `watch` reads `.trashinfo`s, inotify on a dead mount waits; one landing after the panel moved on is cancelled by
  `_watch_generation`) and re-reads it when that changes on disk. It is on by default, and is the
  ninth Behavior item in Options > File Manager > Setup. **A departure**: DN re-read a panel only on the `cmRereadDir`
  that whatever changed the directory broadcast (`RereadDirectory`), so another program's file waited for Ctrl+R.
- `navigator/lib/system/dirwatch.py` puts one `watchdog` observer behind the whole process, with one **non-recursive**
  watch per directory however many panels show it (refcounted; the last `Watch.cancel()` unschedules). Only created,
  deleted, moved and modified pass; watchdog's opened/closed are dropped, or F3 opening a file would re-read its panel.
  A directory that cannot be watched (the inotify limit, a gone directory, a filesystem with no events) gets an inert
  `Watch`, and its panel is what it was before.
- **The notify runs on the observer's thread**, and only calls `Application.call_from_thread(panel._changed_on_disk)`,
  which queues on the loop and wakes it, and drops the call while no loop runs. **Only the first change after a
  re-read is handed over** (`Panel._heard`, set on the thread, cleared by `_refresh_now` just before it reads): a copy
  into the directory shown is a change per block written, and handing each one to the loop cost a quarter of a core. `_changed_on_disk` arms one
  `call_later(REFRESH_DELAY)` (0.3 s), so a burst is a single re-read. `_refresh_now` calls `reload()`, which keeps the
  cursor, tags and quick search, and it waits again while a slow read is `_pending`.
- `Panel._watch_directory` is an effect on `path`, `found` and the setting: turning the setting off, or showing a
  *Find:* listing, stops the watch. With no application it watches nothing, so model tests stay deterministic.
  `Panel.unmounting()` cancels the watch, `Navigator.on_stop` calls `dirwatch.shutdown()`, and so does an autouse
  fixture in `tests/conftest.py`, because each watch holds an inotify instance and a user gets 128 of them.

## Git status (`[file_manager] git_status`)

A departure (asked for): DN knew no git. In a work tree, each row ends in a letter, and the title names the branch.
- **The letters** are `M` modified, `A` added, `D` deleted, `R` renamed or copied, `?` untracked, `!` ignored and `U`
  unmerged. A directory takes the strongest letter beneath it (`gitstatus.PRIORITY`, `U M D R A ?`). An ignored file
  inside says nothing of its directory.
- **Where the letter goes**: it sits in the middle of `Panel.GIT_CELLS` (3: a blank, the letter, a blank keeping it
  off the column divider) at the end of the name's cells, in every view mode (`_draw_name`). `name_room` and `list_columns` give those cells up while `git` is
  set.
- **Colours**: the letter is coloured by `Panel::git.<class>` (`gitstatus.CLASSES`), the `git-*` `DERIVED` entries.
  Under the cursor bar it takes the row's own colours.
- **The title** reads `path [mask]  branch ↑N↓M` (`git_text`; `^`/`v` at the ASCII tier). A detached HEAD shows a
  7-character commit. The branch is dropped before the path would be cut under `MIN_NAME_WIDTH` cells.
- **How it is read**: `navigator/lib/system/gitstatus.py`'s `read` runs `git rev-parse` and then
  `git status --porcelain=v2 -z --branch --ignored=matching -- .` on `_SCANNER`. The result is `Panel.git`, a
  `GitState`, or None.
  - It runs with **`GIT_OPTIONAL_LOCKS=0`**, so a read never writes the index. Without it, a read would take the
    user's `index.lock`, and its own write would set off the `.git` watch below, for ever.
- **When it is read**:
  - **After a listing lands, never inside the scan**: `_follow_git` is an effect on `items`, `error`, `found`,
    `location`, `scanning` and the setting. This way a slow `git status` never holds up a listing.
  - It runs only for the local disk outside an archive, and never for a *Find:* listing. With no application it
    reads nothing; before the loop runs it waits for the read, as the first listing does.
  - A change of directory clears `git` in `_apply`, so the last directory's letters never land on new names.
- **The `.git` watch**: `git add`/`commit`/`checkout` change the git directory and not the directory shown.
  `_watch_git` therefore watches `GitState.git_dir` (non-recursive: index and HEAD) under *Auto refresh panels*, and
  reads git again after `REFRESH_DELAY`. It uses the same one-shot hop to the loop as the directory watch.
  An edit in a subdirectory the panel does not show is heard only by Ctrl+R or the next listing.
- **The setting** is File Manager Setup's sixth *Display* box. The README screenshot turns it off.

## View modes (Ctrl+Y, DN's `cmToggleShowMode`)

Per panel: `Panel.view_mode`, `cycle_view_mode`, and *Panel > Display > View mode* (a menu entry DN never had).
- *simple*: name and size.
- *detailed*: Name taking the rest │ Size │ Attr `rwxr-xr-x` │ Owner `user:group` │ Date (**modification** time,
  `DD-MM-YYYY hh:mm`, since Linux has no portable creation time; the four-digit year is a departure). Owner is a departure, 5-17 cells as the longest listed
  (`DirEntry.display_owner`, names cached, a number where there is none). Links, then Owner, then Attr, then Date drop when the name
  would fall under 12 cells. **Size is 8 cells, K/M/G/T 1024-based** (`DirEntry.display_size`), a departure: DN's
  `FileSizeStr` gave every digit with separators under 10,000,000 then `N,NNNK`, in 10-11 cells; the exact bytes are
  in *Current file*'s tooltip.
- **Links** (`ls -l`'s second column, a departure, asked for; **off by default**): `DirEntry.nlink`, the hard link
  count, between Attr and Owner, right-aligned, at least 5 cells and as wide as its translated heading. It comes from the
  stat the row already has (the target's for a symlink, as `mode` and the size are): `make_entry`, `entry_at`, the
  root helper's `listing` (an 11th field) and `ExecDrive.scan`. A drive that does not say leaves 0, shown blank, as
  is `..`. Never in an archive. No sort mode. File > Links > *Show hard links* lists the names (`navigator-file-ops`).
- *list*: names alone in columns, each as wide as its longest name capped at half the panel; Left/Right move a column as DN's `kbLeft`/`kbRight` did.
- **Departures in the modes**, each kept:
  - Ctrl+Y cycles simple → detailed → list; DN's `CM_ToggleShowMode` toggled Full and Brief, a custom set going to Full.
  - A wide panel widens the name; DN repeated the whole line across it (`Size.X div LineLength`, FLPANEL.PAS:603,
    635: two Full sets in an 80-cell panel). Asked about and kept: one set reads wider names whole.
  - A narrow panel drops columns (`DROP_ORDER`); DN scrolled the whole line sideways (`DeltaX`).
  - No hidden/system mark between name and extension (DN's `▒`/`▓` in the name's ninth cell, FILESCOL.PAS:478-479):
    a POSIX name has no 8.3 split to put one in, and a dot-file says it is hidden by its name.
- A too-long name ends in `…` (`fit_text`, in cells) and starts with one while scrolled (`window_text`); `...` at the
  ASCII tier (`Panel.ellipsis`, `glyphs.ellipsis`). The title's path is cut in its middle with the same marker,
  its drive part kept (`Panel._cut_title`, DN's `TTopView.Draw` writing `C:\...\tail`): `/…/deep/dir`,
  `ZIP:a.zip:/…src`; only one too narrow for that, and the footer's and a *Find:* title, cut their start. In simple and detailed, Left/Right scroll every name a cell (`ScrollNames`, `Panel.name_scroll`, clamped, reset by directory or mode
  change) -- disabled while the command line has text, so the caret moves.
  **The names' scroll has a bar** (`Panel.hbar`, a departure, asked for, as the editor's). It runs on the bottom frame
  from a cell in to a cell short of the option strip, with value `name_offset` and range `max_name_scroll`, the
  longest name in the directory, which is the clamp Left/Right already use. It is shown only while a name is cut or
  scrolled, never in the list mode, and not while a quick search's label stands on that row. `on_hbar_scroll` sets
  `name_scroll`. The right bar is the `ListViewer`'s own, shown only while there are more entries than fit.
- A name is shown through `Panel.shown_name` (`navkit.bidi.reveal`): a direction override, isolate or control in it is a
  `⁇` (`?` in ASCII) painted reversed out of the row, which reorders nothing -- `photo⁇gpj.exe`, not `photoexe.jpg`.
  Widths, scrolling, list columns, tooltips and the info line measure the shown name; anything that *uses* the name
  (copy, rename, Ctrl+Enter) keeps it whole. A departure: DOS names had no such characters.
- **The left button held** follows the pointer with the cursor (`ListViewer`'s drag) only while Drag-and-drop is off
  (`Panel.follows_drag`, DN's `fmoDragAndDrop` branch). Past the top or bottom it scrolls a row a tick from the
  start (`edge_ticks = 1`, `edge_delay = REPEAT_EVERY`). A press on the column titles sorts, a departure kept: DN
  moved the cursor up while held there.
- **Drag-and-drop** (File Manager Setup's box, **on by default** -- a departure, DN's `fmoDragAndDrop` was off;
  `panel/drag.py`): a left press on a row captures the mouse; the first
  move with the button held makes a `DragLabel` overlay (` name ` or ` N selected files `, `$30`, shadow) that follows
  it -- the tagged files if the row is tagged, else the row's own, never `..`. The release finds the target with
  `drop_target` (a panel's directory row or its directory, its own panel only on a directory row; a tree's node) and
  the panel emits `Dropped` (with the drop's screen `x`, `y`). `Manager.on_dropped` puts up `_drop_menu`, a
  `PopupMenu` at the drop titled with the drag label and with `To <directory>` in its bottom frame (`footer`, home as `~` by `title.tilde`, the
  path's start cut to keep the box on the screen): *Copy here* / *Move here* / *Symlink here* / *Relative symlink
  here* / *Cancel*, into `copy_entries` or `link_entries` (Shift+F5's body, shared). A departure: DN copied at once
  and Shift moved; here Shift only opens the menu on *Move*. Confirmations' *Drag and drop* puts up the Copy or Create
  symlink dialog after the choice (`LinkDialog(relative=...)` ticks its box), and a directory is never dropped into
  itself.
- **The trash can** (≡ > Trashcan on/off, `ToggleTrashCan`, DN's `TTrashCan`/`cmHideShowTools`, ticked while shown):
  `widgets/shell/trash_can.py`, a `Shell` child over the desktop bound to the desktop's bottom right corner by
  `gap_x`/`gap_y` (so a resize keeps it there, `gfGrowAll`), dragged by the mouse, `TrashCan:dragging` in the frame
  icons' colour. A drop on it is `Dropped(trash=True)` (`drag.TRASH`): `Manager._drop_on_trash` asks a Yes/No
  *Do you wish to delete NAME?* (a departure: DN erased at once), then `erase_entries(dialog=False, quiet=...)` --
  *quiet* (Yes to non-empty and read-only) unless Confirmations' *Drag and drop* is ticked, as DN set
  `Confirms := 0`. Shown and placed are saved with the desktop (`desktop_state`'s `trash`). DN's double click
  ran the *Reanimator* undelete, which has nothing to do here.
- **Left, Right, Home and End go to a command line with text** under File Manager Setup's *Use arrows* (on, DN's
  default), and Shift+ them to the panel; off, the other way round (`Panel.arrows_to_line`, `Panel.LINE_KEYS`;
  `Manager.enables(ScrollNames)`, `Shell.enables(CommandLineHome/End)`, and `Shell._panel_keeps` stopping a plain one
  a panel declined from reaching the line, as DN's `TSpecScroll` did). DN's expression is read for its intent:
  compiled, `and` binding before `xor` made it `Shift xor (off and arrow)`, the reverse (`FLPANEL.PAS:1149-1151`). Ctrl+Home and Ctrl+End go to a line with text
  whatever *Use arrows* says (DN's line took them as Home/End); with the line empty they're the panel's top and bottom.
- Non-simple modes have a heading row in *Column title* `[165]` (`Panel::heading`) and single `│` rules in the frame's
  colours (`Panel::divider` on `$panel-fg`/`$panel-bg`, a departure from DN's `[86]`), meeting the frame in the tee
  `Widget.box_joins()` gives (`┬┴`/`╤╧`) wherever title/footer does not stand.
- **A column title's tooltip** is `Panel.column_description(key)` and the order a click sorts by next
  (`next_column_sort`, which `sort_by_column` applies, so the tooltip cannot promise another). A new column needs a
  description there.
- **An info line's tooltip** says whole what the line cut or rounded (`info_line_at`, `_info_tooltip`): *Current file*
  the name, every byte, the date and a link's target; the line under it the whole directory/origin/target; *Free
  space* the exact bytes; any other its text while wider than the panel. A new kind of line decides its own there.
- **A row's tooltip** (`_row_tooltip_at`): over the name, the whole name while cut or scrolled (`_name_room`, the
  room `_draw_name` gives it, in every mode) and a link's `-> target`; over the detailed mode's owner and path, their
  whole text while cut; nothing over `..`, sizes, dates or attributes.
- **The title's tooltip** (`_title_tooltip`, over the title's own cells): the whole path where its start was cut,
  the mask in words with Alt+Del's key, the git branch (or detached HEAD) and ahead/behind spelled out -- even where
  a narrow title dropped the branch. A title that says it all has none.
- **A press on the title** (`Panel.title_part_at`, DN's `TTopView.HandleEvent`): the panel takes the keyboard, then
  its drive part opens the bookmarks (`ChangeDrive`, DN's `cmChangeDrive`) and the rest *Change directory*
  (`ChangeDirectory`, `cmChangeDir`). DN's drive part was `C:`; here it is the path up to its first `/` (`/`, `~/`,
  `ZIP:a.zip:/`), kept by a title cut in its middle; only the first cell when the title is cut at its start or is a *Find:*
  listing's. The titles sit
  on the window's top row, so `Manager.chrome_hit` gives up its "move" over a title's text: the rest of the row
  still drags the window.
- **The divider's tooltip** is `Manager.tooltip_at`, over exactly what `divider_hit` grabs: drag, Alt+Left/Right (read
  off the key table) and the double click that evens the split. A panel's frame has none, so the lookup climbs to it.
- **Shift+F11 on a panel** shows its cursor row's tooltip (`Panel.tooltip_anchor`: the name, the list mode's
  column too). A greyed panel command says why: `Manager.refusal`, which `enables` is derived from -- give a new
  veto a reason there, not a bare `False`.
- **Miller columns inherit both** -- a `MillerColumn` is a `Panel`: a row's whole name while cut (`_name_room`
  reads the column's own `name_width`), and the title, its directory's name alone, gives the whole path. No code of
  their own; `tests/test_miller.py` holds it.
- **The mouse on the info lines is `TInfoView.HandleEvent`'s** (`Panel.info_part_at`, `_info_press`): a press on the
  divider row scrolls down while held (`hold_mouse`, the first row on the press; the tagging button -- middle, or right
  under *Right button* select -- tags each row passed with the first row's flag; on the inactive panel the press only
  selects it); a left press on *Current file*, *Selected* or *Totals* starts the row drag with its files given
  (`_drag["entries"]`: the cursor's, the tagged, every one but `..`, labelled `N files` for *Totals*), under
  *Drag-and-drop* as a row drag is. *Free space* and the clipboard line take nothing.
- **The info lines are DN's `TInfoView`**, between the listing and the bottom frame under the *Info divider*, in its
  order, each behind its *Display* box (`Panel.info_lines`, `(text, part)`: the computed `_info_lines` with the
  current file's text filled in as it is read, because the gutter it follows is not reactive):
  - *Current file* (`::current-file`, `[119]`): **laid out on `detail_columns` in every mode** -- the columns *Columns
    Setup* (Alt+K) shows, at their places and widths, a blank where each divider stands, the name past the rows'
    gutter. DN's `GetDown` was always name, size, date, time; following the columns is Navigator's. The size is
    `DirEntry.info_size` (every digit, or DN's `<UP--DIR>`/`<SUB-DIR>`), right-aligned on its column's edge and taking cells
    from the name where wider. Drawn as it is, never split on `~` (`PLAIN_INFO`). **Except in the detailed mode**,
    whose rows show those columns already: there the line is the whole name (`_full_name_text`), under the rows'
    names past the gutter, or from the panel's left edge where it is longer than that leaves room for.
  - a second line under it: a *Find:* entry's directory (DN's find drive), the panel's whole width -- **there is no path column**: it was
    Navigator's, too narrow for a path, and is gone (`[column_defaults] find_path` is `OBSOLETE`) -- or
    `-> target` on a symlink under `[file_manager] link_line` (Navigator's; File Manager Setup's *Display* boxes), or in
    the Trash (`trash:///`, Navigator's) `From {path}, deleted {when}`, the path giving up its start, the date kept. It
    is **kept while the listing could need it** -- always on a *Find:* listing, while the listing holds a symlink or a
    trashed entry otherwise -- so the listing never changes height as the cursor moves.
    **Inside an archive** it is DN's `dtArc` line instead (`Panel._packed_line`, part `::packed`, the selection's
    colours): `~Packed:~ 1,234      ~Ratio:~ 56%`, from the left, the labels bright; always kept there, blank on a
    directory or a member that does not say its packed size.
  - *Selected files* (`::selected-files`, `[120]`/`[121]`): `No files selected`, or `~X~ bytes in ~N~ selected files`,
    only the numbers bright as DN's were; in an archive `~X(P)~ bytes in ~N~ ...` where the packed total differs.
    With files tagged and the box off, the selection takes *Current file*'s line, as DN's `Goto 1` did.
  - *Totals* and *Free space* (`navigator-settings`), centred as the selection is.
  **Nothing per entry per cursor move or frame** (a 100k listing walked ~4 times a keypress, and the key bar's F5/F6/F8
  questions walked it every frame): `_info_lines` reads `self.selected`, so it reads only `_marked_tuple` (the
  tagged entries, a computed of `items`+`marked`, `()` without walking when nothing is tagged) and `_listing_facts`
  (`ListingFacts.of(items)`: entries at all, files and their bytes, any trashed, any link -- one walk per listing).
  `marked_entries` is `list(_marked_tuple)`, so `Manager.selection` costs what is tagged. Ctrl+L's `InfoPanel._totals`
  (`diskinfo.totals`, passed as `lines(counted=)`) is counted once per listing, and `shown()` builds `lines()` once.
  A new per-cursor computed must not walk `items` itself: put the walk on a computed of `items`/`marked`.
  The bottom frame carries the quick search's label, the names' scroll bar (`hbar`) and the option strip -- no info
  line any more. `Panel.rows` is computed less `info_height`, so the list, scroll
  bar and list-mode columns shrink, and the column rules end in `┴` on the divider rather than on the frame. Tests
  that pin a listing down to the frame turn `free_space`, `current_file` and `selected_files` off; anything painting a
  real directory headless pins `free_space_of` and the date and time (the golden test, screenshot). An entry's size
  changing where it stands (Alt+G) bumps `Panel.sizes_token`: the same list of the same entries is no change to
  `items`.
  **Alt+I hides that footer** -- divider and lines -- per panel (`ToggleInfoLines`, `Panel.show_info`/`toggle_info`,
  *Panel > Display > Show/hide footer*, ticked while shown, kept with the desktop); a departure, DN had only the *Display* boxes,
  and its Alt+I was a second, uncaptioned *Info* (`cmDiskInfo`, Ctrl+L's) key, taken for this.
  The command has no `title`, so the Alt key bar keeps *Z Zoom*.
- **The option strip** (a departure, as the editor's and viewer's): each panel's bottom frame carries navml's
  `OptionStrip` (`Panel.options`, added in Python in `Panel.__init__` -- Panel has no markup), right-aligned 3 cells
  before the corner: `[Hid]` (Ctrl+H) and `[Info]` (Alt+I) lit while on, then the view mode and the order
  (`Name↑`), never lit, a click doing Ctrl+Y / Alt+B (`panel/option_items.py`'s `panel_items`; word / symbol / Nerd
  icon by `option_label`). **Lit is read off the strip's own panel** (`lit=`), not `Manager.checks`, which answers
  for the active panel. `PanelOptionStrip` focuses its panel on a press before running the command, so Manager's
  handlers -- which act on `active_panel` -- switch the panel clicked. A quick search's centred label wins: the strip's
  `room` ends before it (`Panel._options_room`) and items drop from the last. File Manager Setup's *Option flags*
  (`[file_manager] show_options`) shows it. The golden desktop fixture and the README screenshot carry it.
- Every mode keeps a gutter left of the name: the Nerd tier's two-cell icon, or one cell of mc's type mark
  (`DirEntry.type_mark`: `/ * @ ~ ! = - + |`). A bookmarked directory (`Panel.is_bookmarked`) gets its own glyph in
  either -- see `colours-themes-glyphs` -- and a tag still wins over both. Rows are coloured by file type -- see `colours-themes-glyphs`.

## Directory history (Alt+Backspace) and quick directories (Alt+1..9)

- **Panel > Change drive** is `ChangeDrive` (Alt+C's bookmarks box, `navigator-bookmarks`).
- **`DirHistory`** (Alt+Backspace, Panel > History of directories), DN's `cmDirHistory` -> `DirHistoryMenu`: every
  directory a panel comes to (a new listing, not a re-read or a *Find:* listing) goes first into navml's `HISTORY`
  list `directories` (`Panel._remember_directory`, DN's `AddToDirectoryHistory`) while Interface's *Track
  directories* is on (on by default, a departure; off, Alt+Backspace says DN's `dlSetDirHistory`).
  `DirHistoryDialog` (`dlgDirectoryHistory`): *Go to* (Enter, a double click), *Delete record* (stays open), Cancel.
- **`JumpToDirectory`** (Alt+J, Panel > Jump to directory; a departure): fzf on the console over zoxide's
  directories and this same history, the active panel to the one chosen (`console-command-line`, *fzf and zoxide*).
  `_remember_directory` also tells zoxide (`[interface] feed_zoxide`).
- **Quick directories are the bookmarks** (a merge, a departure: DN's nine `DirsToChange` slots and its drive
  letters' box were two things; Navigator's bookmarks already replaced the letters with directories). Alt+1..9
  `QuickChange(slot)` go to the *N*-th bookmark with no box (none that far: nothing); Alt+Shift+1..9
  `StoreQuickDir(slot)` ask DN's `dlPromptForQDir` (*as bookmark N*) and `place_bookmark` the panel's directory at
  place *N*, moving it if already bookmarked (disabled in a listing); Alt+Shift+0 / Panel > Quick dirs `ListOfDirs`
  is the bookmarks box (`choose_bookmark`). These keys sit in `Manager.keys` (Python) because a terminal without the
  kitty protocol sends Alt with the *shifted* character -- `alt+!`..`alt+(` and `alt+)` are bound beside
  `alt+shift+N` for a US layout. A directory gone is said, not entered (`Manager._go_to`).

## Settings remembered per directory, and the cursor left in one

A departure, asked for: DN's `SortMode`/`FileMask`/`PanelFlags` belonged to the panel and went wherever it went,
and nothing was kept by path. `navigator/lib/config/directory_settings.py` has the rules; the tables are
`DirectorySettings` (`navigator/models/directory_settings/`) and `DirectoryCursor` (`navigator/models/directory_cursor/`),
both keyed by `bookmarks.key_of` of the `root.on_disk` place (a `root:` directory is the disk's).
- **File Manager Setup's *Remember directory settings*** (`[file_manager] remember_directories`): `off` (DN's
  behaviour), `marked` (the default: only those Panel > *Remember for this directory* marks) or `all` (any directory a
  setting is changed in). A record holds `directory_settings.KEPT`: view mode, sort and its direction, mask, hidden
  files, columns and the *Display* boxes. It does not hold Alt+I's footer, which is the panel's.
- **Panel > *Remember for this directory*** (`RememberDirectory`, `Manager.remember_directory`) is ticked by
  `Manager.checks` while `Panel.remembers_here` is true. Unticked, it asks `RememberDirectoryDialog` (*Also for its
  subdirectories*) and calls `Panel.remember_here`; ticked, it calls `Panel.forget_here`. `refusal` greys it under
  `off`, over a *Find:* listing and inside an archive. **Panel > *Remembered directory list*** (`RememberedDirectories`)
  is a `PopupMenu` of the records shaped like the bookmarks box: Enter goes there, Del forgets one.
- **One choke point**: `Panel.location` is an `_Arrival` reactive whose `__set__` calls `Panel._arriving` before the
  write. Every move runs through it (Enter, `..`, bookmarks, the tree, `cd`). It keeps the cursor left in the old
  directory, calls `settle_directory` (a record found by `directory_settings.find`, the directory's own or the nearest
  ancestor's with `subdirs`, is put over the panel's own, which are held in `Panel._base`; with none, `_base` comes back),
  and sets `_return_to` from the kept cursor if the move set none. **The settings change in the same call as the place,
  so `_rescan` reads once, with them**; an effect doing it would read twice or depend on effect order.
- `Panel.remembered` is the key of the record shown (`""` for none). The title starts with `remembered_mark()`:
  `◆`/`◇` for own/inherited, `*`/`+` in ASCII, `icons.REMEMBERED`/`REMEMBERED_ABOVE` at the Nerd tier. The title's
  tooltip says which.
- **A change inside a remembered directory is the record's**: the effect `_keep_directory_settings` writes it,
  and an inherited record's change goes to the ancestor. Under `all`, it makes a record of an unremembered directory.
  Because a change and a move in one batch reach the effect as a move only, `_arriving` also writes what a remembered
  directory was left showing. `remember_here` sets `_kept_dir` itself for the same reason.
- **Marking keeps the panel's arrival settings as its own**: `settle_directory` notes `Panel._arrival` (what the
  panel came to a directory with no record with), and `remember_here` makes that `_base`. So a sort changed in a
  directory and then remembered stays with the directory, and does not follow the panel out (a reported bug).
- **The side state and a saved desktop keep the panel's own settings** (`Panel.own_settings()`: `_base` if held), never
  a record's. `panel_state.recall` and `desktop_state._seed_panel` call `drop_directory_settings()` first and
  `settle_directory()` after, so the record goes back over what they seed.
- ***Return to last cursor position*** (`[file_manager] restore_cursor`, on by default, a Behavior box) keeps the
  entry the cursor was left on in every directory (`DirectoryCursor`), and a remembered directory always keeps it.
  An explicit `_return_to` (going up, `go_to_file`) wins. Only the newest `CURSORS` (2000) are kept.
- Tests: `tests/test_directory_settings.py` (mounted `Manager`, `settle()`).

## Advanced filter (Alt+Del)

`AdvancedFilter`, `Manager.advanced_filter`, DN's `cmAdvFilter` -> `CM_AdvancedFilter`: `FilterDialog`
(`dlgAdvancedFilter`) over a `FilterList` (DN's `TSelectList`: Space/Ins mark and step, `+`/`-`/`*` all/none/invert,
right click) of `advfilter.extensions` -- `*` and each `*.ext` of the directory read again on a thread whatever the
mask hides (a listing's own entries in a *Find:* listing). *Show*/*Hide* take the marked masks, or the one at the
cursor, into `Panel.file_mask` through `advfilter.combine` (DN's intent without its string surgery: `*` sets the
whole mask; from show-all, *Show* narrows to the chosen and *Hide* excludes them; otherwise a chosen pattern replaces
what the mask said of it, appended so it decides) and `Panel.set_file_mask` (re-read, cursor kept). The box comes back
on the same mask after each, until *Close*.

## Columns Setup (Alt+K)

`SetupColumns`, `Manager.setup_columns`, DN's `cmSetupColumns` -> `CM_SetShowParms` (also Panel > Setup columns):
`ColumnsDialog` (`dlgDiskParms`; `dlgFindParms` less its *Path* box, the directory being the footer's line) over
**`Panel.shown_columns`**, the detailed mode's columns per panel (DN's `ShowFlags`): size, attributes, links, owner, date. OK shows the detailed mode with those -- none ticked is the list mode, DN's brief; *Brief* is the
list mode; *Full* every column but *Links* (`columns_dialog.ALL_COLUMNS`) -- DN's `GetFullFlags` was size, date
and time (packed and ratio in an archive), the attributes and owner kept as the POSIX facts, a departure. `DROP_ORDER` still drops columns (links, owner, attributes, ratio, packed, date) to keep the name
`MIN_NAME_WIDTH`.

A *Find:* listing was a drive of its own in DN, with its own `ShowFlags`, and so was an archive (`dlgArcParms`), so
a panel holds three sets: `Panel.columns` over a directory, `Panel.find_columns` over a listing and
`Panel.archive_columns` inside an archive; `shown_columns` reads and writes whichever is showing. **Options > File Manager > Column defaults** (`ColumnDefaults`, `dlgColumnsDefaults`,
`[column_defaults]`) seeds them: `columns` when a panel is made, `find_columns` by every `show_found` (DN's
`TFindDrive.Init`), `archive_columns` from its *Archives* set when a panel is made and on entering each archive
(`TArcDrive.Init`). Only `columns` goes into the saved desktop.

## Hidden files (Ctrl+H)

`ToggleHidden`, `Panel.show_hidden`, `toggle_hidden`, per panel, shown by default -- our key (it took DN's *Directory
Branch*, whose caption was dropped), where DN's `ossShowHidden` was a system option. The re-read keeps the cursor; a tag
on a name it hides is dropped. *Panel > Display > Show/hide hidden files* is **ticked** while the active panel shows them. Every
directory tree follows it (see `navigator-trees`). Ctrl+H decoding: `navkit-terminal`.

**Hidden files, the footer, the view mode and the order are remembered per side** (a departure): the effect
`Manager._keep_panel_state` writes a side to the `PanelState` model (one row a side,
`navigator/lib/config/panel_state.py`'s `remember`) whenever one of the five changes there -- by key, menu, Alt+S, a
column title or Ctrl+U -- its first run only noting them, so opening a file manager writes nothing. `Manager.__init__`
seeds both panels of every new file manager from it (`recall`). A side with no row follows System Setup's *Show hidden
files*, shows its footer and takes *New Manager defaults*' view mode and order; a restored desktop is seeded after, so
it wins.

## Sorting (Alt+B)

`Panel.sort_mode`, one of `SORT_MODES` (name, extension, size, time, attributes, owner, type, unsorted -- `PanelDefaultsData.SORT_BY`), is
DN's per-panel `SortMode`, seeded from *New Manager defaults* > *Sort by*. `order_entries` is `TFilesCollection.Compare`
and runs on the scan thread: `..` first; directories first except by *Type* (DN's *Group*: directory, executable,
archive, the `filetypes.CATEGORIES` after it, the rest -- `filetypes.GROUPS`); size and time largest/newest first;
*Attributes* by the permission bits (`S_IMODE`, fewest first) and *Owner* by `display_owner` case-folded, both
then name (departures: DN sorted by neither);
names case-folded. *Executables first*/*Archives first* lead the files except by size, time, attributes and owner, read at each read (not
followed). *Unsorted* is `scandir`'s order, without the two flags (DN's compare was no order there). Alt+B and *Panel >
Sort by* are `Manager.choose_sort`: `CM_SortBy`'s `PopupMenu`, centred on the panel (DN put it at the panel's top left), on the current order, captions
`sort_captions()` (*Type* is T~y~pe). **Each mode is in it twice** (`sort_orders()`: its own direction, then reversed;
*Unsorted* once), the own direction plain and the reversed one with its arrow in the key column
(`Panel.direction_arrow`, as Alt+S's captions with *Reverse order* ticked), the reversed caption without its hot key
(`sort_order_captions()`) so the letter picks the own direction, and the panel's order ticked (`MenuItem.ticked`). *Sort by*'s radio group in Alt+S and *New Manager defaults* is three rows of
three columns, so the Russian and Latvian captions fit 52 columns. `Panel.sort_by(mode, reverse=False)` re-reads keeping the cursor on its entry.

**Clicking a column title sorts by it** (a departure: DN had no descending order nor clickable titles):
`Panel.heading_at` finds the column on the heading row and `sort_by_column` steps through its `COLUMN_SORTS` modes,
each up then reversed (`Panel.sort_reverse`), wrapping: Name is name ↑ → name ↓ → extension ↑ → extension ↓ (there
being no extension column), Size, Attr, Owner and Date (time) just flip; the others sort nothing. From another column's order a
click starts at the first step.
`order_entries(reverse=True)` turns only the order *within* each group: `..`, directories before files and the
*Executables/Archives first* flags stay put; *Unsorted* ignores it. The sorted column's title ends in `↑` (ascending)
or `↓` (`^`/`v` at the ASCII tier), Name's with a `.` before it while the extension sorts (`Name.↑`) -- `Panel.sort_arrow`, with `SORT_ASCENDS` saying size and time run descending
unreversed. Alt+S's *Panel Options* has *Reverse order* (`PanelSetupDialog.reverse`, on the *Sort by* caption's row): ticked,
each order's caption ends in the arrow of the way it then runs, unticked they are plain (`sort_radio_captions()`,
bound to that box); *New Manager defaults*
has the same box and arrows, as `[panel_defaults] sort_reverse`, which seeds `Panel.sort_reverse` with `sort_by`; both
dialogs share `sort_radio_captions()` (`manager/manager/helpers.py`) and are 56 columns, for those arrows in Russian and Latvian.
`set_options` takes the direction with the mode; `direction_arrow()` and `SORT_ASCENDS` are module-level in panel.py. `sort_reverse` is kept with the desktop.

## Tagging

- **Insert tags** (`ToggleMark`, DN's `kbIns`): the entry joins `Panel.marked` (names, never `..`), cursor steps down,
  the gutter shows `√` (`+` in ASCII) in *Selected text* `[87]` / *Selected cursor* `[89]`; the *Selected files* info line
  reads `N bytes in M selected files`. A re-read keeps tags; a change of directory drops them. **Space tags too while the command line is
  empty** (`ToggleMarkBySpace`, DN's `fmoSpaceToggle`, gated by `Shell`, which owns the line).
- **Gray `+`/`-` are *Select*/*Unselect group*** (`SelectGroup`/`UnselectGroup`, `cmPanelSelect`, on Panel's menu):
  `SelectDialog` asks for a mask -- `;`-separated shell patterns matched as a POSIX glob (`filetypes.matches`: case
  counts and `*.*` needs a dot, a departure from DN's `InMask`) -- seeded from `HISTORY["select"]` or `*`, *Except mask* ticked by Shift. Selecting passes directories over,
  unselecting does not (`Panel.select_group`).
- **Gray `*` inverts** (`InvertSelection`, `cmPanelInvertSel`, `Panel.invert_marks`): files flip, directories keep their
  tag; Ctrl+Gray `*` (`kbCtrlGAst`) flips directories too -- bound as `ctrl+*` as well, which is how a terminal
  may report it with Num Lock on.
- **Alt/Ctrl + Gray ± tag entries like the cursor's** (`SelectSimilar`/`UnselectSimilar(by=, invert=)`,
  `Panel.select_similar`, DN's `SelectExt`/`SelecType`): Alt the same name, any extension (`os.path.splitext`'s
  stem), Alt+Shift those with another name, Ctrl the same type (`filetypes.category_of`, DN's `TType`: on a directory,
  the directories), Ctrl+Shift the same extension. Directories count, as DN's `Sel` passed none over (Gray+ does);
  `..` never, nor the cursor on it. Bound on `kp_plus`/`kp_minus` and the bare `plus`/`-` with the modifiers.
- **Ctrl+A selects all** (`SelectAll`, `Panel.select_all`, Panel > *Select all files* and the context menu, no hot key --
  only `j` is free there): every file and directory, never `..`, whatever was tagged. A departure, asked for: DN had
  none, and Ctrl+Gray `*` inverts (untagging what was tagged) and needs a terminal that reports the keypad.
- **With text on the command line the Gray keys type instead** (a departure): bound in `manager.py` as `by_key=True`
  instances that `Manager.enables` disables while the line has text; the menu's instances are unaffected. **The plain
  `+`, `-`, `*` are bound the same way** (mc's rule), because VTE and PyCharm send Gray `+` as bare `+`.

- **Shift+ or Ctrl+left click tags a range** (`Panel._shift_select`, a departure, asked for: DN's left button only
  moved the cursor): every row from the cursor to the one clicked, both ends, added to what was tagged, `..` never;
  the cursor goes to the row clicked and no drag starts. Ctrl because VTE (xfce4-terminal) and kitty never report
  Shift+click; xterm and Ghostty do once asked (`MOUSE_ON`'s XTSHIFTESCAPE, `CSI > 1 s`). A Ctrl+double click
  (Insert name) puts back the tags its first press changed (`_before_range`).
- **The right button** follows File Manager Setup's *Right button* (`[file_manager] right_button`, a departure).
  `menu`, the default, opens the panel's context menu (`Panel.context_menu`, built from DN's `GetSelection`). `select`
  is DN's own (`FLPANELX.PAS`): a press toggles the row's tag and captures the mouse, and a drag gives every row it
  passes the same tag, scrolling past either end (`Panel._right_marking`). Held still past an end it goes on, a row a
  tick (`hold_mouse`, `_right_marking_at`; DN's loop with `RepeatDelay := 0`). The Menu key and Shift+F10 open the menu
  under either setting.
- **The middle button (the wheel pressed) always tags as DN's right button did** (`on_mouse_click` sends its press
  to `_right_marking`, a departure, asked for: the right button's default is the menu): a press toggles the row's
  tag, a drag gives every row it passes the same one. Either button's press makes its panel the active one. On VTE (xfce4-terminal), which pastes on a middle
  press and reports only the release, `Panel.claims_middle_click` (a row) has navkit drop the paste and deliver the
  press (`navkit-widgets-input`, *VTE's middle click*); a drag with it held cannot work there.

## Copy, cut and paste through the clipboard (Ctrl+C/Ctrl+X/Ctrl+V)

A departure, asked for -- only Ctrl+Ins is DN's (`FLPANELX.PAS` `_CtrlIns`, `cmPutInClipboard`: the names, nothing
kept). DN's panel Ctrl+Del (take entries off the listing) was never ported, so it is *cut* here.

- **Ctrl+C/Ctrl+Ins** (`PutInClipboard`) and **Ctrl+X/Ctrl+Del** (`CutToClipboard`) put the selection's full paths on
  the clipboard, one a line (`Manager.clip_files`), and keep the entries in the app-wide
  `navigator.lib.file_ops.clip.CLIP` (where they were listed, `here`, and `move`). Tags stay.
  **Ctrl+V/Shift+Ins** (`PasteFromClipboard`) runs F5's or F6's dialog on them into the active panel
  (`Manager.paste_files`, see `navigator-file-ops`). **Esc** (`ClearClipboard`) forgets them.
- **All four are `by_key=True` and step aside while the command line has text** (the `fmoDelErase` rule), so the line
  keeps copy/paste, and Ctrl+X still walks the history (a recall always puts text on the line). For Ctrl+Ins that's a
  departure: DN's panel always took it (`_CtrlIns`); here it copies the line's selection or the whole line
  (`console-command-line`). Paste and Esc are
  disabled with no clip, so Shift+Ins pastes text and Esc does what it did.
- **Any other copy forgets the clip** (`Navigator.copy_to_clipboard` compares with `CLIP.text`), so the next paste is
  that text; a paste that moved forgets it too, a copy can be pasted again.
- **The cue**: rows get `clip-cut` (dim) / `clip-copy` (italic) classes, after `.marked` in `navigator.nss`, the cursor
  bar keeping its colours; the gutter shows `Panel.CLIP_MARKS` per glyph tier (`✂`/`❐`, nerd `md-content_cut/copy`,
  ASCII `x`/`c`) below a tag's sign; every panel's info lines add *Clipboard: N files to move/copy*. The context menu
  offers the three.

## Quick search (Ctrl+S)

mc's quick search (`QuickSearch`, `Panel.quick_search`, *Panel > Quick search*): typing moves the cursor to the first
name from it that begins so (case folded, `*`/`?`, `..` never found); a character naming nothing is refused, Backspace
drops one, Ctrl+S again finds the next, wrapping. Shows as ` Search: … ` on the footer with the caret (a departure:
DN's caret sat in the cursor row's name, over what matched); with the command line hidden, a character typed with
Shift starts it (`Shell._search_with_the_line_hidden`, DN's `ouiHideCmdLine` path; not `\`); with text
typed the key bar leads with *Ctrl+S Next* (`Panel.key_hints`; a departure, asked for). Esc ends it;
any other key ends it and does its job -- Enter descends into (or runs) what was found in one press -- as do a click, a
directory change and losing the keyboard. While it runs `edits_text` is True. Matching rules: `navml/quick_search.py`.

DN's keys while searching (`FLPANEL.PAS:1268-1330`, `Panel._search_key`): **Ins and the keypad Gray +/−/\*** tag as
ever and the search stays on (`GotoKb`) -- unless the key's box (Gray ±'s *Select*) takes the keyboard, which ends
it; a bare `+`/`-`/`*` character is searched (names hold them; some terminals send the Gray keys so). **`\`** ends the
search and opens *Change directory* with the letters typed into its tree's search (`ChangeDirectory(search=)`,
`ChangeDirDialog` replaying them once its start directory has its rows -- as typing them there would; DN's
`PutEvent` replay). Departures: **Ctrl+Enter** ends the search and inserts the name (DN: next match -- Ctrl+S is
that), **Space** is searched (DN ended the search and tagged; POSIX names hold spaces), **`.`** is a character (DN
jumped to the 8.3 extension).

## Hiding sides and replacing a side

- **Ctrl+F1/Ctrl+F2 are `cmHideLeft`/`cmHideRight`** (`Manager.toggle_side`, `hidden_side`): a side (`side_view` -- the
  panel or the tree/quick view in its place) is hidden and **the window shrinks** to the other side's rectangle, so the
  console shows through (`SwitchLeft`'s `Locate`). Again restores the old rectangle (zoomed if it was, or grows by the
  share lost). Hiding the only side left shows the console (`cmShowOutput`), and the key from the console brings the
  manager back with that side alone (`cmPostHideLeft`, `Shell.show_manager_side`) -- both keys are on the application's
  table. Tab is disabled while a side is hidden. Ctrl+T/Q/L follow `SwitchView`'s order (`switch_view`): the view on
  the hidden side shows that side with the view kept, the keyboard unmoved; the view showing is put away and a hidden
  other side stays hidden; otherwise the hidden side is shown first and the view goes in.
- **The quick view is made on first use, not in the markup.** `Manager.quick` builds it and adds it, hidden, last in
  the `panels` row. `MillerView.preview_file` is built the same way, in `open_at`. So a start loads no viewer code
  (~6 ms); `test_no_quick_view_is_made_or_imported_until_one_is_wanted` guards it in a fresh interpreter.
  - **To ask whether a view is the quick view without building it**, use `Manager.is_quick(view)` and
    `MillerView.file_preview_focused()`, never `x is self.quick`. An effect or a comparison would otherwise build it
    at mount, and `replacement is self._quick` is true while both are None. is `TDoubleWindow`'s `cmZoom`** (`Manager.on_zoom_window`):
  - The side the view follows is hidden, then the window zooms (DN's uncleared `cmZoom` went on to `TWindow`'s), so
    the view fills the desktop. `_view_zoom` notes the rectangle.
  - Alt+Z again shows the side. `show_side` first undoes that zoom (`_unzoom_view`) while the window is as it left
    it, so the window gets back the rectangle and zoom it had before. A departure: DN's arithmetic there didn't come
    back to it.
  - Every way a side comes back goes through `show_side`, so Ctrl+F1/F2 and Ctrl+P do the same. Ctrl+Q there puts the
    view away and leaves the side hidden (`SwitchView`'s rule); Ctrl+F1/F2 then brings it and the window back.
  - Anywhere else, and in the quick view without the keyboard, the command passes on to the desktop's zoom.
    `Manager.refusal` answers for `ZoomWindow` now that the handler is here.
- **Ctrl+P is `cmSwitchOther`** (`toggle_inactive_side`, on `manager.nml`'s table): the side without the keyboard; it
  never falls back to the console.
- `Manager.switch_view` is DN's `SwitchView`, shared by Ctrl+T (tree) and Ctrl+Q (quick view): `replaced`/`replacement`;
  `tree_replaces` is a computed over them. **One view at a time**, a departure (asked about and kept): DN kept a type
  per side (`LType`/`RType`), and a view opened while another held the keyboard took the opposite panel's place
  (DBLWND.PAS:541-556), so a tree and a quick view could stand together with no panel showing. Here the new view
  puts the old one away; `active_panel` and every panel command need a panel showing.

## Find file (Alt+F7) and the *Find:* listing

`FindFile`, `Manager.find_file`, DN's `FindFile`/`FindFiles` (also File > Find...): `FindFileDialog` (`dlgFileFind`,
own OK / *Advanced...* / Cancel row, mask, text, options, scope and limits kept for the session (DN's `FindRec`, written back on OK only, first `*`; OK in *Advanced search* writes it all at once, Find cancelled or not -- DN's `RSearchAdvance`, `_remember`), opening on *Recursive* + *Current directory*) and
`AdvancedSearchDialog` (`dlgAdvanceSearch`: ISO dates, sizes, POSIX kinds, *Clear all*) give a `FindRequest`;
`navigator/lib/file_ops/filefind.py`'s `search` walks on a thread (with Ctrl+H off a dot-directory never entered -- a departure from DN's *Security*, which still recursed -- and a dot-file found only by the *hidden* kind, `_hidden_skipped`; mask via `in_filter`, a bare item -- no wildcard, no dot -- made a prefix by `find_mask`, DN's `MaskSearch`, case kept and a dotted item exact as departures, text by chunked regex in regular files only -- plain text through the viewer's `compile_search` (any alphabet's case, `WORD_BYTES` word breaks: DN's Find called `SearchFileStr`), a *Regular expression* folding ASCII only (a departure) -- the text then handed to the viewer's `last_search` and the editor's `SEARCH` by `hand_on` (DN's `SearchString`/`SearchData`; not when empty, not a regex to the viewer) -- (*Regular expression* gathers the file chunked, Stop between chunks, up to `WHOLE_LARGEST`, 64 MiB shared with Replace in files' `LARGEST`, larger ones passed over; the one `re.search` can't be stopped) -- a FIFO, socket or device never opened, `holds` opening `O_NONBLOCK` and re-checking against a swap -- never through a symlink, an error listing a directory halfway ending only that directory (`_listed`, DN's `FindNext` loop),
one file system for *Entire disk* / *All drives*; *All drives* is the panel's own file system, `/`, then every disk kind in `/proc/self/mounts` (`DISK_KINDS`, `searchable_mounts`) -- kernel, memory, image and network mounts left out unless the panel is on one, network a departure; *Current directory* crosses mounts below it, as `find` does, never into a kernel file system (`VIRTUAL_KINDS`, `/proc`, `/sys`, `/dev`... -- the table read at the first crossing), though a search started in one walks it; on a server, container or device, by name: never into its `/proc`, `/sys`, `/dev`, `/run` -- `SYSTEM_PLACES`, on a `Drive.system_root`) under `FindProgress` (its button DN's `~S~top`) through `_watch_job(..., abort="Cancel
search?")`. **Results are a `FindListing` in `Panel.found`** (DN's `TFindDrive`): the panel lists its entries -- live
while searching, re-`stat`ed by `restat_found` on a re-read (the info panel, Ctrl+L, says *File Find results*, *Mask: …* -- another listing's title where it has none -- and the files shown, no drive's lines: `InfoPanel.show_listing`, DN's `TFindDrive.GetDirInfo`, whose count 1.51 had commented out, here counted; nothing goes *into* a listing, which has no one place: F5/F6/Shift+F5/Extract/Archive open with no target from it -- `Manager._push_first_name`, DN's empty `GetRealName` -- Ctrl+V into one is refused, *Not in a Find listing*, DN's empty `CopyFilesInto`, and drops are refused; masked by the panel's file mask both live and settled, directories excepted: `shown_in_listing`, DN's `GetDirectory`), gone ones dropped -- under a `..` that leads back -- to the listing it was made from when one was shown (`FindListing.previous`, DN's `Prev`: any listing made over a listing stacks, Ctrl+R's re-panelize replaces in place with `stack=False`, a directory gone to drops the stack), else to the origin with `_way_back`'s cursor, a listing's own way back when made from one; the cursor placed by key first, then name --
(`leave_found`, cursor where it was); title `Find: mask`, the info line under *Current file* the entry's directory. Enter, Shift+Enter, Ctrl+PgUp, Ctrl+PgDn and Ctrl+Shift+PgDn (DN tested `..` before Shift; *Show in other panel* therefore not greyed there) on `..`
leave; Enter on an entry `go_to_entry` (its directory, cursor on it); Shift+Enter `ChangeInactive` sends the other
panel there -- DN's `cmFindGotoFile`: its file mask back to all files (`FileMask := x_x`) so the file is listed, and
the keyboard with it (`Owner^.Select; Select`), the listing kept in its own panel. A listing belongs to the path it was shown at: going elsewhere drops it -- but a command's `cd` doesn't move it (`Shell._follow_shell`), as DN's find drive kept its place. Nothing found: *No files found*,
the panel untouched. F7 is disabled in a listing, as DN's `TFindDrive.MakeDir` made nothing; Compare directories too -- a departure: DN's
`CM_CompareDirs` compared whatever two panels held, a find drive's included, where here the comparison (and its
recursive *Window*) reads directories, and a listing is none.

**Panel > Directory Branch** (`DirBranch`, `Manager.directory_branch`, DN's `CM_Branch`/`OpenDirectory`): every
file below the panel's directory, directories left out (`FindRequest(directories=False)`), searched through the same
`_search_into` as Alt+F7 into a listing titled `Branch: <dir>`. Menu only: DN's Ctrl+H is Navigator's hidden-files
key. Disabled in a listing, as `CM_Branch` acted on a disk alone.

**Alt+V, Panel > Read file list** (`ReadFileList`, `Manager.read_file_list`, DN's `cmPanelMakeList` ->
`TFindDrive.InitList`): the list file at the cursor read on a thread by `filefind.read_list` -- a line a name (whole,
blanks included: a departure, DN cut at the first blank), relative to the panel's directory, `~` expanded, masks
globbed as a shell does (no dot-files for `*`), missing names skipped, each file once -- into a `FindListing` titled
with the list's path. Nothing there: *No files found*. Enabled on a file only.

**Alt+Y, Panel > Panelize command** (`Panelize`, `Manager.panelize`; a departure, MC's *External panelize*):
`PanelizeDialog` (history `panelize`, seeded with `Manager.last_panelized`), then `navigator/lib/file_ops/panelize.py`'s
`capture` runs `$SHELL -c command` in the panel's directory on a thread -- off the console's pty, stdin `/dev/null`,
its own session so *Stop* (`FindProgress` retitled, the count row hidden) kills the group (`_end`: TERM, then KILL,
each given `STOP_GRACE` 3 s, then the pipes let go of unread if a `setsid` child still holds them -- Stop never
waits past that) -- and
`filefind.list_from_lines` (Alt+V's reading, split out of `read_list`) turns the lines (NUL-split when the output has
a NUL: `find -print0`) into a `FindListing(command=...)` titled `Panel: <command>`. Nothing listed: *No files found*,
with the first stderr line when the command failed. **Ctrl+R in such a listing runs the command again** (`on_rescan`),
columns and cursor kept. Enabled only on the local disk. Two more ways in: a command line starting `|`
(`console-command-line`) and a user-menu item with a `<|` line (`navigator-user-menu`).

**Panel > Find duplicates** (`FindDuplicates`, `Manager.find_duplicates`; a departure, asked for -- DN had none):
`DuplicatesDialog` (mask, history `find_mask`; minimum size, default 1 so empty files are out, `valid()` refusing a
non-number; *Search subdirectories*; kept for the session), then `navigator/lib/file_ops/duplicates.py`'s
`find_duplicates` on a thread, **on any drive** (a `Location` start walks the drive and reads through `open_read`; the
listing is built from the walk's `DirEntry`s, `DuplicatesJob.listed`): the walk is `filefind.search` (hidden files follow the panel's Ctrl+H), symlinks and
non-regular files dropped, **hard links collapsed to the first name by path** (erasing one frees nothing), then
narrowed by size, a quick blake2b of the first and last `CHUNK` (a file of at most 2×CHUNK is then read whole and
skips the next step), and a full blake2b. Stop raises `Stopped`: half a result is no answer. **The listing keeps its
own order** (`FindListing(keep_order=True)`: `Panel.reload` reads it `unsorted`, whatever `sort_mode` says): the
groups wasting most bytes first, each by path. Nothing is tagged. Ctrl+R re-`stat`s, dropping erased files; a group
left with one file stays until the next search. Menu only (every letter of the name is taken), no key; local disk
and not in a listing. Nothing alike: *No duplicate files found*.

**Find's *Regular expression*** (bit 16 of the options, a departure, asked for): `FindRequest.regex`;
`filefind.text_pattern(..., regex=True)` compiles the text as Python's `re` (bytes, `MULTILINE`, *Whole words* wrapping
it in a group), and `holds`/`holds_on_drive(whole=True)` match the file read whole, since nothing bounds a pattern's
span for the chunk overlap. `FindFileDialog.refusal()` puts an invalid pattern in an Error box before closing.

**Alt+Shift+F7, File > Replace in files** (`ReplaceInFiles`, `Manager.replace_in_files`; a departure, asked for -- DN
had none; not Ctrl+Alt+F7, the desktop's VT switch): `FindFileDialog(replacing=True)` -- *Rep~l~ace with* (history
`replace_text`) under the text, the rest two rows lower, its own session (`_replace_session`) so its ticks are not
Find's -- gives a `filereplace.ReplaceRequest`. `navigator/lib/file_ops/filereplace.py`'s `replace` is `filefind.search`
with a **`match` hook** in place of `holds`: each file is read whole (skipped: a NUL in the first `BINARY_PROBE` bytes,
or over `LARGEST`), `plan` makes the new bytes as `re.sub` would (a template with *Regular expression*, the literal
bytes without -- backslashes and all) and the `Change`s (line spans touched, before/after, made `printable`, the first
`SHOWN`), and a `ReplaceQuestion` goes through `Job.ask` to `ReplaceQuery` (`navigator/widgets/file_ops/replace_query/`:
counts, a `ChangeList` coloured by `::line.removed`/`::line.added` on the viewer's colours, *Yes* (default) / *All* /
*Skip* / *Cancel*). All stops the asking (`ReplaceJob.all`); Cancel raises `Stopped`, and what was written stays.
**Written from the planned bytes**, after checking size and `st_mtime_ns` again (changed while asked: a `Failure`,
Skip/Cancel): on the disk by the editor's `save.write_file` (temp + rename, mode/owner kept, links followed, a locked
file refused), elsewhere by `drive.open_write`; an `OSError` is a `Failure` through `_answer_copy_question`. It runs
through `_search_into(job=, work=, answer=, nothing=)`, so the files changed fill a live `Replaced: <text>` listing;
a toast says the files and the replacements; none changed says *No files changed* (*No files found* if none held it).
Not in Miller columns.

**Entries can live elsewhere**: `DirEntry.directory` (None in a directory listing), **`DirEntry.path_in(here)`** for
its path -- never `here / entry.name` -- and **`DirEntry.key`** (name, or whole path when elsewhere) for tags,
`marked`, `_keep` and `reload(key=...)`. Untag through `Panel.untag(entries)` / `untag_paths(paths)`; `tag_paths(locations)` tags (Verify checksums' failures).

## Make list (Alt+L)

`MakeList`, `Manager.make_list`, DN's `CM_MakeList` -> `MakeListFile` (also Panel > Make list file): nothing tagged,
`SelectDialog` first; then `MakeListDialog` (`dlgMakeList`: file name, history `make_list`, opened on its last entry
or `makelist.DEFAULT_NAME` `dnlist.txt` -- DN's `DNLIST.BAT` -- and *Action*, history `command`, opened on the last
command run; *Store path names* / *Autodetermine*, kept in `[make_list]` (`store_paths`, `auto_paths`,
`_keep_section`) as DN kept `MakeListFileOptions` in its configuration; a *Store path names* left ticked opens
unticked when every file is from one directory, ticked only for a *Find:* listing that spans several -- DN's
`cmlPathNames` check -- and OK keeps the untick). DN's FidoNet file requests (a name starting `+`, `%` or `/`,
`FILECOPY.PAS:488`) are dropped: no POSIX meaning. `navigator/lib/file_ops/makelist.py`: one line per file, or per file per `;` template (`;;` a `;`) with
`! .! !\ !/ !: !!`, values shell-quoted, a template without macros followed by the quoted file; *Autodetermine* adds
paths for files outside the list's directory and puts `!\` before a bare name macro. An existing file asks Yes /
A~p~pend / Cancel. Written files are untagged and `FileSaved` re-reads the panels showing the list's directory.

## Fast rename (Alt+F6)

`FastRename`, `Manager.fast_rename`, DN's `CM_RenameSingle`: `fast_rename.FastRenameLine`, an `InputLine` run as a
modal overlay over `Panel.name_cell()` (one cell further left, for its scroll arrow), the name all selected. Enter
renames; Up, Down, Left at the start and Right at the end rename and then are posted to the panel (DN's `PutEvent`,
after the rename was tried, gone or refused); Esc cancels, as DN's `cmCancel`; a name left as it was is cancelled too
and its key dropped (`FLTOOLS.PAS:982`); a click outside cancels; `/` is not typed. Departures: the whole name
selected at the start (DN: none, overwrite mode); a change of case alone renames (DN compared upper-cased); any
writable drive (DN: disk, temp, find and list panels). Never `..`. A name already taken
is refused (DOS's rename refused it, POSIX's replaces). The tag follows the file; `Panel.reload(name=new)` keeps the
cursor on it; `FileSaved` re-reads the other panels.

## Panel Options (Alt+S)

`PanelSetup`, `Manager.panel_setup`, DN's `cmPanelSetup` -> `Setup` (also Panel > Setup Panel): `PanelSetupDialog`
(`dlgPanelSetup`, laid out as `FMDefaultsPage` plus *File mask*, history `file_mask`) opens on the panel's own
values and OK is `Panel.set_options(sort, display, mask)`: one re-read keeping the cursor. **`Panel.display`** is None
while the panel follows the *New Manager defaults* live and a frozenset of `PanelDefaultsData.DISPLAY` names once set;
ask `Panel.shows(option)`, never `SETTINGS.panel_defaults` directly. **`Panel.file_mask`** (DN's `FileMask`, `*` for
all) filters files, never directories, in `scan_directory` through `filetypes.in_filter` (`InFilter`: `;` patterns,
`-` excludes, the last match decides, nothing matching is out; case counts). A mask other than `*` follows the path in the
title, `/src [*;-*.bak]` (`title_text`; the path is cut first) -- a departure: DN's panel said nothing of it. *Directory length* drives Alt+G's counting and *Totals* and *Free
space* are info lines (*The info lines* above).

## Directory length (Alt+G)

`CountLength`, `Manager.count_length`, DN's `cmCountLen` (also Panel > Count directory length): the directory at the
cursor (`..` counts the one listed) and every tagged directory get the bytes beneath them, counted on a thread by
`navigator/lib/file_ops/dirlength.py` (`CountDirLen`: dot-files count, symlinks count as themselves and are never followed, unreadable
directories count as nothing) under `run_with_progress`'s *Counting directory length* box; Esc keeps what was counted.
That box is `navigator/widgets/file_ops/count_progress/` (`CountProgress`, a departure from DN's bare wait box): bytes,
files and directories met so far, summed over every target through one `CountJob` that `count_dir_length` adds to
(any other job, such as the panel scan's, only stops it). The *Display* box's *Directory length* counts a *Find:* listing's directories too, on its settled re-read (`restat_found(dir_length=)`, DN's `GetDirectory`; never while it fills, nor `..`, nor an entry on another drive; Esc's `Abort` as in a directory). With more than one target it also names the directory being
counted and shows a *This directory* column (`CountJob.here_*`, restarted per target) beside *Total*. The counts are
one unwrapped `StaticText` (`CountProgress.counts`): columns as wide as their longest entry, the total against the right
edge, so a size gaining a digit (99G -> 100G) widens its column instead of pushing past the frame. `modal_width` is
bound to `box_width` -- the table's natural width plus the frame, at least 50 (one directory) or 60 (several) -- so the
box grows, re-centred, as the counts gain digits, capped at `parent.width` (the screen, once overlaid); a row too long
for that loses its label, never its end.
The entry gets `size` and `counted` (DN's `Attr or $80`), its size column shows the size where `DIR` was (DN's column said `<SUB-DIR>`; `DIR` is a departure, asked for;
*Current file* says `<SUB-DIR>`/`<UP--DIR>` as DN did), the tagged
total includes it, and *Size* sorts by it. **A re-read keeps the counts** (a departure, asked for: DN's went with the
old entries, so sorting by size -- itself a re-read -- lost them): `Panel._apply` hands a re-read of the directory
listed to `_keep_counts`, which copies each counted directory's bytes onto the new entry by `key` and re-orders when
the order is by size. A change of directory forgets them. Alt+G's answer goes through `Panel.set_lengths`, which,
sorting by size, re-orders the listing at once with the cursor on its entry (on its screen row); otherwise bumps
`sizes_token`. `panel_defaults.directory_length` (count every
directory at each read, `fmiDirLen`) is not written yet.

## Information panel (Ctrl+L)

`DiskInfo`, `Manager.on_disk_info`, DN's `cmDiskInfo` -> `SwitchView(dtInfo)` (also Panel > Other panel > Info): `InfoPanel`
(`manager/info_panel`, Python-only, framed like the quick view, `::highlight` for DN's `~` runs) takes the passive
panel's place as the tree and quick view do. **With the keyboard in it** (`TDiskInfo.HandleEvent`): F4 is *Edit
DirInfo*, the `DirInfo`/`File_ID.DIZ` it shows (`InfoPanel.info_path`, from `DiskFacts.info_file`) in the editor
(`Manager.edit_info_file`), greyed with none (*No DirInfo or File_ID.DIZ here*); F5/F6/F8 and the panel's other file
commands are refused (`_aside_focused` counts it), as DN's info view did nothing with them.
`Manager._info_follows_panel` (an effect on the active panel's path,
items and `reload_token`; not while it shows a *Find:* listing) calls `InfoPanel.show`, which reads the disk and the
machine on a thread (`navigator/lib/system/diskinfo.py`'s `gather`: `disk_usage`, the longest mount in `/proc/self/mounts`, a
`/dev/disk/by-label` label, `/proc/meminfo`, the resident set, `DirInfo` else `File_ID.DIZ` in any case) and keeps
the last answer up meanwhile. `diskinfo.lines` lays them out as `TDiskInfo.Draw`, each behind a `[drive_info]` box;
totals come from the listing (entries counted as `CountDirLen` counted them, bytes the files'). DN's EMS/XMS lines
are left out; its memory three are read for POSIX.

**A departure: it scrolls.** `InfoPanel.top` is the first line drawn, clamped at draw time (`shown()`, `last_top()`), so
a shorter description after a cursor move never leaves it blank and a longer one keeps the place; a new directory
resets it to 0. Focused (Tab, `Manager.switch_panel`) it takes Up/Down/PgUp/PgDn/Home/End; the wheel works anywhere
over it; a navml `ScrollBar` child on the right frame column, bound to `top`/`last_top()` and visible only while the
lines overflow, emits `ScrollEvent` to `on_scroll` (drag, arrows, page). It is plain `ScrollBar`-coloured, as
Ctrl+Q's is. `tooltip_at` reads `shown()`, so a tooltip names the scrolled row.

**A departure**: a *Current file* section (rule, then `Label: ~value~` lines, left-aligned) follows the directory
block, behind the `current_file` box (*File under the cursor*). Of the file under the cursor DN's `TDiskInfo` said
only its description, `ReadInfoBBS` (DISKINFO.PAS:267-339) reading the entry's lines from `descript.ion`/`files.bbs`
on each `cmLoadViewFile`; that went with `descript.ion` (`dn-porting`), so no description is shown -- a departure.
`Manager._info_follows_cursor` is a separate effect on the active panel's `selected` and calls `InfoPanel.show_file`,
so a cursor move never re-runs `gather`. Name, type, size, mtime, attributes (+ octal), owner and link target come
from the `DirEntry`. `diskinfo.stat_file` on the same thread adds the MIME guess (stdlib `mimetypes`, whose table is
read on first use, hence the thread) and, for a local entry only, the `lstat`'s atime, ctime, links and inode.
Nothing for `..`.

Media details (`[drive_info] media_info`, *Media information*) join the same table:
`navigator/lib/system/mediainfo.py`. Its `read` runs as a **second** `_READER` job after `stat_file` answers, so the
table never waits for it. It is only for a local file whose MIME guess is audio, video, an image or a PDF. Audio and
video come from `ffprobe` JSON (optional, looked up at the call like `gio`; without it, nothing). Images come from the
stdlib, which reads the first 128 KB: the size of a PNG/GIF/BMP/WebP/JPEG, and a JPEG's EXIF camera and date taken,
which ffprobe does not give. Any other image gets ffprobe's size. PDFs come from pypdf. The thread returns a plain
`Media`; `pairs()` formats it on the loop because `tr` reads a reactive. `read` asks `wanted()` first, so a held-down
key does not queue one ffprobe run per file behind the single worker. Labels are in `mediainfo.LABELS`, which the
catalogues read through `navigator/locales/__init__.py`.

Programs join it too, behind the same box: `navigator/lib/system/programinfo.py`. `mimetypes` guesses nothing for an
ELF file (`.so` gets `application/octet-stream`), so `stat_file` calls `programinfo.sniff`, which reads the first
4 KB of a regular file (the link's target) that is executable or named `*.so[.N]`/`.o`/`.ko`. Its MIME type
(`application/x-executable`, `x-pie-executable`, `x-sharedlib`, `x-object`, `x-coredump`) is the `program` kind of
`mediainfo.kind`; `mediainfo.read`/`pairs` hand a `Program` to `programinfo`. The rows are machine and kind, the
interpreter, each `DT_NEEDED` library (`~name~ (not found)` when missing) and *Symbols* (stripped = no `.symtab`;
`.debug_info` noted). Everything is read from the headers with seeks: **never `ldd`**, which on glibc may execute the
file, and no `readelf`/`file` dependency. A library is looked for in glibc's order (RPATH only without RUNPATH,
`LD_LIBRARY_PATH`, RUNPATH with `$ORIGIN`/`$LIB`, `/etc/ld.so.cache` parsed by `parse_cache`, musl's
`/etc/ld-musl-*.path` else the default and multiarch directories) and counts only if its ELF class, byte order and
machine match. Direct needs only, not the transitive tree. An empty label in `pairs` is a continuation row: `table()`
lines its value up under the row above; a value already holding `~` keeps its own marks.

## Comparing directories (Panel menu)

Panel > Compare directories (DN's `cmCompareDir`), its *Window, recursive* Synchronize window and File > Compare
files are the `navigator-compare` skill.

## Same directory in other panel (Alt+=)

`EqualizePanels`, `Manager.equalize_panels`, Panel > Other panel > Same directory in other panel: the passive panel goes to the
active panel's directory, and the keyboard stays. **A departure**: DN 1.51 had no such command; it is Midnight
Commander's *Sync panels*. MC's Alt+I is the footer here and every Alt+letter can be a menu-bar accelerator (Alt+O
opens *Options*), hence Alt+=. The passive side is brought as Alt+F1/F2 bring theirs (`bring_side`: a hidden side is
shown, the tree or quick view gives way) and leaves a *Find:* listing; greyed while the active panel is one.

## Miller columns (Alt+F12)

`ToggleMiller`, `Manager.toggle_miller`, Manager > *Miller columns* (ticked while on). **A departure, asked for**:
DN had two panels and nothing else; this is Finder's column browser. `navigator/widgets/manager/miller/miller_view.py`.

- **`MillerView`** (Python-only, `id: miller`, hidden in the `panels` row) takes both panels' place; a hidden side or a
  tree/quick/info view is put back first. **Empty while off**: `open_at` makes the columns, `close` removes them, so
  nothing is read or watched for a layout not showing. Off again, the side that was active (`_miller_side`) goes to
  the directory browsed, the cursor on its entry; the other side is untouched.
- **Every column is a `MillerColumn(Panel)`**, so commands need nothing new: **`Manager.active_panel` is
  `miller.current`** (the chain's last), and **`passive_panel` is the active one too** -- F5/F6 offer the directory
  browsed, Ctrl+C/Ctrl+V go between two. `Manager.miller_mode` is the flag; `_NOT_IN_MILLER` greys what needs two
  panels (swap, hide sides, tree/quick/info, divider, Ctrl+Y, Alt+I, Alt+K, *Find:*-style listings). `bring_side`
  (Alt+F1/F2) answers the column, `show_only` does nothing (Ctrl+F1/F2 fall through to `Shell`). Anything that must
  reach every panel -- a re-read after a copy, a drive closing, *FileSaved* -- loops over **`Manager.all_panels`**,
  never `(left, right)`.
- **The chain** (`MillerView.chain`, root first, replaced to change) comes from `_up` -- `Location.parent`, and at a
  drive's root its `change_up`, as `Panel.go_up`. `_rebuild` keeps columns already on the way and makes the rest.
  Right/Enter on a directory `step_in` (the **preview column becomes the chain's last**, a new preview is made);
  Left/Backspace `step_out` (the last column becomes the preview, cursor kept). A press on an earlier column drops the
  ones after it (`column_pressed`). **Any other move of the current column** -- a shell `cd`, a bookmark, Alt+T, Enter
  on an archive -- moves the panel as it always did, and `_follow_moves` rebuilds the chain around it (`home` is
  where the view last put a column).
- **The preview** (`_follow_cursor`): a directory in `preview_dir`, a file in the view's own `QuickViewer`
  (`preview_file`), or the quick view empty. Tab moves the keyboard into the file and back (`switch_focus`).
  `_aside_focused` counts it with the tree and quick view.
- **Layout** (`_place`): columns `[file_manager] miller_width` wide (File Manager Setup's *Miller column width*,
  at least `MIN_WIDTH` 12), as many as leave the preview a column's width, the leftmost giving way; the preview takes
  the rest. The first visible column and the preview keep `title_margin` 5 for the window icons.
- **A column's look**: simple mode drawn narrow -- gutter, name, `▸` (`>` in ASCII) after a directory; title the
  directory's own name; no footer, option strip, `..` (filtered in `_apply`) or git letters (`_read_git`). The entry
  the next column lists is `Panel::row.trail` (`reverse`) while another column has the keyboard, via the
  `Panel.row_classes` hook. Ctrl+H and the order apply to every column at once.
- **Only the column browsed** offers *As root* (`_offer_root`) and goes into Alt+Backspace's history (columns'
  `_remember_directory` is a no-op; `step_in`/`_rebuild` remember) -- the preview moves with every cursor step.
- Kept with the desktop as the window's `miller` (path, cursor, side), on the local disk only.

## Swapping panels (Ctrl+U)

`SwapPanels`, `Manager.swap_panels`, DN's `cmSwapPanels` (also Manager > Swap panels): the two panel objects change
places in the `panels` row, whole, and **`Manager.left`/`right` are swapped with them** -- they name sides, not panels,
so Alt+F1, Ctrl+F1 and the rest act on whatever is on that side now. A tree or quick view goes beside the panel it
stands in for; the keyboard stays with its panel. **With a side hidden, one side stays hidden and the visible panel
goes across**: DN's `HandleEvent` read `LVisible`/`RVisible` once at its top, so the `cmHide*` after the swap -- chosen
by those flags -- found both showing and hid the other side. `swap_panels` shows the hidden side, swaps, then
`hide_side`s the opposite one; Ctrl+U again restores the start exactly (`_collapse`). The row
is re-`arrange()`d by hand: reordering `children` in place is not something its layout follows.

## The divider between the sides

DN's `TSeparator` (FLPANEL.PAS, `TDoubleWindow.HandleCommand` in DBLWND.PAS). These are the two columns where the
sides meet: the left side's right frame edge and the right side's left one. Dragging them with the mouse moves the
divider. Alt+Left and Alt+Right (`MoveSeparator(step)`, DN's `kbAltLeft`/`kbAltRight`) move it one column.

- **The split is a proportion.** `Manager.split` is the first side's share of the row, or `None` for the even split.
  It is DN's `OldX/OldW`, so resizing or zooming keeps it. `MIN_SIDE` (3) is the narrowest a side can go.
- **It is applied as a layout hint.** `place_divider()` is an effect that reads the split, the row's width and which
  views are showing. It gives the first *showing* view `basis: N; grow: 0`, and every other view the defaults.
  - The hint therefore follows the side, not the panel object: it lands on a tree or quick view that stands in, and
    after Ctrl+U it moves to the panel that is now on the left.
  - `swap_panels` calls `place_divider()` itself, because reordering children is not reactive.
  - With one side hidden, no view gets a hint.
- **It is hit-tested before the chrome and the children** (`Manager.dispatch_mouse`, `divider_hit`). A panel claims
  a press anywhere in its rectangle, frame included. The left side's edge column counts only where its `bar` is not
  showing; on the scroll bar's rows a press there scrolls the list. The drag captures the mouse onto the Manager and
  is handled in `on_mouse_click`, ahead of `Window`'s own move and resize.
- **A double click on the divider resets the split to `None` (the even split).** This is a departure: DN had no way
  back except dragging. The second press has already taken hold of the divider and captured the mouse, so the
  `DoubleClickEvent` reaches `Manager.on_double_click`. It lets go of the divider and clears the split. A double click
  anywhere else falls through to `Window` (zoom on the title).
- **While held, the divider is drawn with single lines** (DN's `sfDragging` look). `Manager.render_after` runs after
  the sides have painted. It swaps each double-vertical box character on the two divider columns for its single one,
  so junctions keep their shape and scroll bar cells are left alone.
- **`Panel.on_key` in list mode leaves Alt+Left and Alt+Right alone.** Its bare `left`/`right` check would otherwise
  take them.
- A saved desktop keeps `split` (`desktop_state`).

- **Every feature key is on a menu** (departures, asked for): Panel > Display > *Move divider left/right* (`MoveSeparator(step=∓1)`,
  Alt+Left/Right; no hotkeys, `j` being the only free letter), and the panel's right-click menu ends with *Insert name*
  / *Insert path* (`InsertName`/`InsertPath`, Ctrl+Enter / Ctrl+Shift+Enter, answered by the shell). Left off on
  purpose: Alt+1..9 / Alt+Shift+1..9 (the bookmarks box has them), Alt+F6 (*Quick rename* is its menu form),
  Shift+Enter (Enter without the archive test, a *Find:* listing's *Show in other panel*), Ctrl+Shift+F1..F10 (user-defined), and navigation. F1 (`Help`) is bound but has no
  handler yet. In an archive the right-click menu adds *Extract to...*/*Test archive* (`navigator-drives`).
  In a *Find:* listing it starts with *Go to ~f~ile* (`GoToFile`, Enter's `go_to_entry`, a command only for the menu --
  Enter stays `Panel.choose`) and *Show in ~o~ther panel* (`ChangeInactive`, Shift+Enter), which is also Panel >
  *Show in other panel*, enabled only in a listing.
  *Select group*, *Unselect group* and *Invert selection* pass their keypad keys as static keys (`key_label("kp_plus")`
  ...): their bindings are the `by_key=True` commands, which the menu's plain ones are not equal to, so no live key is
  found -- the Panel menu's static `Gray "+"` is the same fallback.

## Read when

No DESIGN reference of its own; panel-related library notes are in
`.claude/skills/navml-library/reference/widget-library.md` (*What the library took from `Panel`*).
