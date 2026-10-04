---
name: app-guide
description: >
  Application overview for frename. Use when: orienting to the project for the first time,
  deciding which crate or module to touch, understanding what the app does end-to-end,
  looking up where a concept lives (tags, files, ordering, colors), or understanding
  keyboard shortcuts and the tag/file lifecycle.
disable-model-invocation: false
---

# Application Overview — frename

## WHEN to use this skill
- Orienting to the project for the first time
- Deciding which crate or module to touch for a given change
- Understanding what the app does end-to-end
- Looking up where a concept lives (tags, files, ordering, colors, sessions)
- Understanding keyboard shortcuts or the tag/file lifecycle

---

## What the app does

**frename** is a Windows desktop app for renaming video files using a tag-based system.

File name format: `tag1.tag2.name.ext`

The user opens a folder, browses video files, assigns tags by clicking checkboxes, optionally reorders tags by dragging chips in the rename panel, and the file is renamed when they move to the next file.

---

## Cargo workspace

```
C:\Work\my\frename\
  Cargo.toml              workspace manifest
  crates\frename-core\    library: pure business logic (no iced)
  src\                    binary: UI (iced 0.14, gstreamer video)
```

### frename-core dependencies
`rusqlite` (SQLite, bundled), `tokio` (async file scan), `uuid`, `indexmap`, `log`

### frename (binary) dependencies
`iced` 0.14, `iced_video_player` (GStreamer), `frename-core`

---

## Source map

### frename-core (`crates/frename-core/src/`)
| Path | What lives here |
|---|---|
| `lib.rs` | All public exports |
| `db/traits.rs` | `AppStateStore`, `StoredTagStore`, `Initializable` traits |
| `db/app_database.rs` | `AppDatabase` — SQLite implementation |
| `db/fake_app_storage.rs` | `FakeAppStorage` — in-memory test double |
| `db/migrations.rs` | Schema creation (3 tables) |
| `ordered/collection.rs` | `OrderedCollection<K,V>` — ordered dict with rebalance |
| `tags/tag_list.rs` | `TagList<S>` — all tag state and operations |
| `tags/tag.rs` | `Tag`, `TagId` structs |
| `tags/file_snapshot.rs` | `FileSnapshot` — checked tags + name + ext |
| `tags/file_tagger.rs` | `FileTagger::parse`, `SaveAndReparse` — file name ↔ snapshot |
| `tags/stored_tag.rs` | `StoredTag`, `TagColorMapping` |
| `file.rs` | `File` — path + metadata + snapshot |
| `directory.rs` | `Directory<S>` — folder with sorted file list + selection |
| `folder_file.rs` | `FolderAndFile` — session: folder path + optional file path |
| `demo.rs` | `DemoScenario` — stage a demo folder and seed the app state for it |

### frename binary (`src/`)
| Path | What lives here |
|---|---|
| `main.rs` | Logging init, GStreamer check, `iced::application` |
| `app/` | `FrenameApp` root: routes messages, global subscription |
| `demo.rs` | Demo mode (`--demo`): wait for the video, set up the scenario, screenshot, exit |
| `features/folder_workspace/` | Main coordinator: directory, file workspace, layout |
| `features/file_workspace/` | Current file + `TagList` + tag operations |
| `features/tag_panel/` | Tag selection grid: cursor, bounds, scroll state |
| `features/tag_grid/` | Tag grid view (used when panel is wide enough) |
| `features/file_name_panel/` | Rename chips panel: drag, trash zone, name line |
| `features/folder/` | File list panel: selection messages |
| `features/folder_controls/` | Folder navigation controls |
| `features/video_player/` | GStreamer video playback state |
| `features/video_controls/` | Progress bar, play/pause |
| `features/drag_drop/` | OS file drag-drop → `OpenPath(path)` |
| `widgets/` | 5 reusable widgets (search_bar, tag_chip, splitter, etc.) |
| `ui/` | The design system (`docs/design/design-system.md`): tokens, fonts, icons, components, styles; `ui/palette.rs` holds the 16-color tag palette and the marker colors |

---

## Key concepts

### Tags
- **Stored tag**: persisted in DB with a UUID, sort_order, and color (by tag name)
- **Snapshot-only tag**: exists in the current file name but not in DB; shown as unsaved (○ button to save)
- **Checked tag**: applied to the current file; appears in the rename panel as a chip
- **Unchecked tag**: in the tag panel but not applied to this file

### Tag ordering (two independent orders)
- `display_tag_ids` — display order in the tag panel; set at file-open, never reordered; used for persistence
- `selected_tag_ids` — order of chips in the file name panel; reorderable via drag; determines file name tag order

### File lifecycle
`ScanFolder` → async scan → `FolderLoaded` → `FileOpened` → user edits tags → `switch file` → `FileUpdated` (disk rename)

Tags are **never written to disk while editing**. The rename happens only when the user moves to another file (or the app closes). Video must unload before rename on Windows (GStreamer holds a file handle).

### Session persistence
Last opened folder + file stored in `folder_history` SQLite table. Restored on startup via `LoadLastSession`.

---

## Keyboard shortcuts

| Key | Action |
|---|---|
| `Space` | Toggle the selected tag (strips trailing space from filter first) |
| `Escape` | Clear the search filter |
| `←` / `→` / `↑` / `↓` | Move tag grid cursor (wraps at edges) |
| `PageUp` / `PageDown` | Previous / next file |
| `Delete` | Remove the selected tag from DB and UI |
| `Enter` | Save the selected unsaved tag to DB |
| Any char / Backspace | Focus search bar and emulate the key into the filter |

---

## Tag colors

`ui::tokens::TAG_PALETTE` (resolved by `ui::palette::TagPalette`) — 16 fixed colors (grays, blues, greens, ambers, etc.).
`TagColors::color(index: u8) -> Color` — wraps index modulo 16.
Color is assigned **randomly** when a tag is saved for the first time (`random_color_index()` in core).
Colors are stored by tag **name** in `tag_color_mapping` table, so they survive renames if done via `save_tag`.

---

## Startup sequence

```
main() → init logging + check GStreamer
iced::application(FrenameApp::new)
  → FrenameApp::new() → FolderWorkspace::new()
  → WindowReady event → LoadLastSession
  → LoadLastSession → AppStateStore::get_last_session() → ScanFolder(session)
  → ScanFolder → async Directory::open() → FolderLoaded { directory, target_file }
  → FolderLoaded → select target file → FileOpened(file)
  → FileOpened → FileWorkspace::set_file(file) → TagList::new(store, snapshot)
  → video_player.load_video(path)
```

---

## Demo mode (screenshots of any state)

`frename --demo <scenario.toml> --out <file.png>` copies the clips a scenario names into a temp
folder, stores the window size, panel widths and settings it asks for in a temp database
(`FRENAME_DATA_DIR`), opens the folder, pauses the video at `seek`, optionally turns on batch mode,
and saves a PNG of the window (iced `window::screenshot`, no window frame). Scenarios and the
annotated templates for the README are in `docs/screenshots/`. The README images are rendered by
hand with `docs/screenshots/render.sh` (Windows or Linux), only when a change makes them wrong; CI
does not make them. Arrows in the templates are the one shape from the original PSD, only rotated
or mirrored (see the comment in `main.svg`). Use demo mode to look at a screen past the folder
picker: write a scenario for it and run it (under Xvfb on a headless Linux).

## Common patterns

**Open a folder/file from outside:** emit `Message::FolderWorkspace(OpenPath(path))` or drop a folder/file on the window (handled by `drag_drop` feature).

**The `LoggingAppStateStore<AppDatabase>` wrapper:** used in production to log all store operations. Passed to `Directory::open()`. The underlying `AppDatabase` is used directly in `FileWorkspace`.

**Generic type resolution:** `FolderWorkspace` uses `type Directory = frename_core::Directory<LoggingAppStateStore<AppDatabase>>`. All generics are pinned at this level; the rest of the UI is concrete.
