---
name: ui-core
description: >
  UI + core combination guide for frename. Use when: wiring a new feature that spans both UI state
  and core data, deciding where logic lives (core vs UI), connecting a new message to a core
  operation, changing how file workspace or folder workspace coordinates with TagList or AppDatabase,
  or understanding the data flow between a user action and disk write.
disable-model-invocation: false
---

# UI + Core Combination Guide — frename

## WHEN to use this skill
- Wiring a new feature that spans both UI state and core data
- Deciding whether logic belongs in `frename-core` or `src/features/`
- Connecting a new `Message` to a core operation (TagList, AppDatabase)
- Changing how `FileWorkspace` or `FolderWorkspace` coordinates features
- Understanding when/how data is written to disk

For wiring `Message::Undo` / `Message::Redo` or implementing undo commands, use the **`undo-dev`** skill instead.

---

## The bridge: FileWorkspace

`FileWorkspace<S>` (`src/features/file_workspace/state.rs`) is the only place in the UI that directly holds a `TagList<S>`. It exposes all tag operations as thin wrappers:

| FileWorkspace method | Delegates to |
|---|---|
| `set_file(file)` | Rebuilds `TagList::new(store, snapshot)` |
| `set_tag_filter(query)` | `tag_list.set_filter(query)` |
| `toggle_tag_by_id(id)` | `tag_list.toggle_by_id(id)` |
| `save_tag(id)` | `tag_list.save_tag(id)` |
| `create_and_save_new_tag(name)` | `tag_list.create_new_tag(name)` then `tag_list.save_tag(id)` |
| `remove_stored_tag_by_id(id)` | `tag_list.remove_stored_tag_by_id(id)` |
| `reorder_tag_to_index(id, idx)` | `tag_list.reorder_tag_to_index(id, idx)` |
| `get_snapshot()` | `tag_list.file_snapshot()` → `Option<(PathBuf, FileSnapshot)>` |
| `has_tag_with_name(name)` | `tag_list.has_tag_with_name(name)` |

**The UI never calls `TagList` or `AppDatabase` directly.**

---

## Message routing

Every user action follows this chain:

```
keyboard/mouse event
  → app::Message (App::update)
    → folder_workspace::Message (FolderWorkspace::update)
      → handle_tag_panel(msg)      [for tag-related actions]
      → handle_file_name_panel(msg) [for chip drag / trash]
      → handle_folder_message(msg) [for file list selection]
        → FileWorkspace method
          → TagList method
            → StoredTagStore method (if persisting)
```

Views emit `Element<'_, feature::Message>`; folder_workspace maps them up via `.map(Message::TagPanel)` etc.

---

## Where logic lives

| Decision | Location |
|---|---|
| Tag data, ordering, filter | `frename-core` (`TagList`) |
| When to toggle / save / delete | `folder_workspace::handle_tag_panel` |
| UI cursor (selected row) | `TagPanelState.selected_tag_id` (UI only) |
| Drag order (file name panel) | `FileNamePanelState` + `tag_list.reorder_tag_to_index()` |
| Layout dimensions for hit-testing | `const` in feature `mod.rs`, used by both state.rs and view.rs |
| File persistence (disk write) | Only in `folder_workspace::apply_file_updated` via `SaveAndReparse` |
| Session persistence (last folder/file) | `AppStateStore::set_last_folder_and_file` called in `FolderWorkspace` |

---

## File save flow (deferred, not immediate)

**Tags are NEVER written to disk while editing.** The save happens only when the user switches to another file:

```
1. User selects different file
   → FolderWorkspace::select_file_at → Task::done(Message::FileOpened(file))

2. Message::FileOpened(file)
   → apply_file_opened():
       snapshot = file_workspace.get_snapshot()  // snapshot of the PREVIOUS file
       file_workspace.set_file(Some(new_file))   // load new file
       if snapshot: pending_file_updated = Some(snapshot)
                    return Task::done(Message::VideoPlayer(Unload))

3. Message::VideoPlayer(VideoUnloaded)
   → on_video_unloaded():
       (path, snapshot) = pending_file_updated.take()
       return Task::batch([
           Task::done(Message::FileUpdated { path, snapshot }),
           video_player.load_video(new_file_path),
       ])

4. Message::FileUpdated { path, snapshot }
   → apply_file_updated():
       (new_path, snapshot_after) = snapshot.save_and_reparse(&path)
       directory.update_file(&new_path, &snapshot_after)
```

**Video must unload before the file rename** because GStreamer holds a file handle on Windows.

In a debug build `save_and_reparse` renames in memory only; code that then opens the file on disk
needs `FileTagger::disk_path` (see core-dev, "Disk paths in a debug build").

---

## Selection after tag operations

After every `set_selected()` call, emit `Message::ScrollTagListToSelection` to scroll the tag into view:

```rust
// In folder_workspace::handle_tag_panel
self.tag_panel.set_selected(Some(id));
Task::done(Message::ScrollTagListToSelection)
```

After `CreateTag`: clear filter first (done inside `create_and_save_new_tag`), then set selection, then scroll.
After `SetFilter`: clamp selection to filtered list (`clamp_selection_to_filtered()`), then scroll.

---

## Adding a new tag operation — step by step

1. **Core:** add method to `TagList<S>` in `crates/frename-core/src/tags/tag_list.rs`
2. **Core trait (if DB access needed):** add method to `StoredTagStore` in `db/traits.rs` + implement in `AppDatabase` + `FakeAppStorage`
3. **Bridge:** add thin wrapper to `FileWorkspace<S>` in `src/features/file_workspace/state.rs`
4. **Message:** add variant to `tag_panel::Message` (or `folder_workspace::Message` for workspace-level actions)
5. **Handle:** add arm in `folder_workspace::handle_tag_panel` (or `update` for workspace-level)
6. **View:** emit the message from the relevant view (`tag_grid/view.rs` or `tag_panel/view.rs`)
7. **Scroll:** if the operation changes selection, emit `ScrollTagListToSelection`

---

## Adding a new UI-only state field

Add to the relevant feature state struct:
- Tag panel cursor / layout → `TagPanelState`
- File name panel drag / drop → `FileNamePanelState`
- Workspace-level layout → `FolderWorkspace`

UI-only state (no core counterpart) stays entirely in `src/features/`.
No need to touch `frename-core` for pure UI state.

---

## Generics pattern

Both `Directory<S>` and `TagList<S>` are generic over `S: StoredTagStore + Clone`.
`FileWorkspace<S>` is similarly generic.
In production: `S = AppDatabase` (via `LoggingAppStateStore<AppDatabase>`).
In tests: `S = FakeAppStorage`.

`FolderWorkspace` pins the generic: `file_workspace: FileWorkspace<AppDatabase>`.
The UI crate never needs to be generic — the generic type is resolved at the `FolderWorkspace` level.
