---
name: undo-dev
description: >
  Undo/redo implementation guide for frename. Use when: implementing the undo infrastructure
  in frename-core, adding a new undoable command, wiring Ctrl+Z/Ctrl+Y in the UI, or
  understanding how History, UndoContext, and commands interact.
disable-model-invocation: false
---

# Undo / Redo Implementation Guide — frename

## WHEN to use this skill
- Implementing or modifying anything in `crates/frename-core/src/undo/`
- Adding a new undoable command (`NavigateFileCommand`, `ReorderTagCommand`, future commands)
- Wiring `Message::Undo` / `Message::Redo` in `FolderWorkspace`
- Debugging undo/redo behavior

Read `UNDO_DESIGN.md` first for rationale, decisions, and data-flow diagrams.

---

## Module layout

```
crates/frename-core/src/undo/
  mod.rs              // pub use all public types
  traits.rs           // Undoable, CommandSink
  history.rs          // History
  context.rs          // UndoContext<'a, S>
  error.rs            // UndoError
  commands/
    mod.rs            // pub use NavigateFileCommand, ReorderTagCommand
    navigate_file.rs
    reorder_tag.rs
  wrappers/
    mod.rs            // (empty initially; Option C wrappers go here)
```

Add `pub mod undo;` to `crates/frename-core/src/lib.rs` and re-export:
`History`, `UndoContext`, `UndoError`, `NavigateFileCommand`, `ReorderTagCommand`.

---

## Core type definitions (reference)

```rust
// traits.rs
pub trait Undoable: Send {
    fn undo(&mut self, ctx: &mut UndoContext<impl AppStateStore + Clone>) -> Result<(), UndoError>;
    fn redo(&mut self, ctx: &mut UndoContext<impl AppStateStore + Clone>) -> Result<(), UndoError>;
}

pub trait CommandSink {
    fn push(&mut self, cmd: Box<dyn Undoable>);
}

// context.rs
pub struct UndoContext<'a, S> {
    pub directory: &'a mut Directory<S>,
    pub tag_list:  &'a mut TagList<S>,
}

// history.rs — peek-then-commit: run command first, then move between stacks on Ok
pub struct History { undo_stack: Vec<Box<dyn Undoable>>, redo_stack: Vec<Box<dyn Undoable>>, max_depth: usize }
impl History {
    pub fn push(&mut self, cmd: Box<dyn Undoable>);      // clears redo stack
    pub fn undo<S: ...>(&mut self, ctx: &mut UndoContext<S>) -> Result<(), UndoError>;
    pub fn redo<S: ...>(&mut self, ctx: &mut UndoContext<S>) -> Result<(), UndoError>;
    pub fn can_undo(&self) -> bool;
    pub fn can_redo(&self) -> bool;
}
```

---

## Initial commands

### `NavigateFileCommand`  (`commands/navigate_file.rs`)

```rust
pub struct NavigateFileCommand {
    pub from_index:      usize,
    pub to_index:        usize,
    pub path_before:     PathBuf,
    pub path_after:      PathBuf,
    pub snapshot_before: FileSnapshot,
    pub snapshot_after:  FileSnapshot,
}
```

**`undo`:**
1. `std::fs::rename(&self.path_after, &self.path_before)?` — restore file name on disk.
2. `ctx.directory.update_file(&self.path_before, &self.snapshot_before)` — sync in-memory.
3. `ctx.directory.select_index(self.from_index).ok_or(UndoError::IndexOutOfRange(self.from_index))?`

**`redo`:** same steps swapped (`path_before↔path_after`, `from_index↔to_index`).

**Where to push (binary: `FolderWorkspace::apply_file_updated`):**
```rust
fn apply_file_updated(&mut self, path: PathBuf, snapshot: FileSnapshot, from_index: Option<usize>) -> Task<Message> {
    let (path_after, snapshot_after) = snapshot.save_and_reparse(&path);
    if let Some(dir) = self.directory.as_mut() {
        dir.update_file(&path_after, &snapshot_after);
        if let (Some(fi), Some(ti)) = (from_index, dir.selected_index()) {
            self.history.push(Box::new(NavigateFileCommand {
                from_index: fi, to_index: ti,
                path_before: path.clone(), path_after: path_after.clone(),
                snapshot_before: snapshot.clone(), snapshot_after: snapshot_after.clone(),
            }));
        }
    }
    Task::none()
}
```

**Required change to `pending_file_updated`:**
```rust
// Before
pending_file_updated: Option<(PathBuf, FileSnapshot)>,
// After
pending_file_updated: Option<(PathBuf, FileSnapshot, Option<usize>)>,
```

Capture `from_index = self.directory.as_ref().and_then(|d| d.selected_index())` in
`select_next()`, `select_previous()`, and `select_file_at()` **before** advancing.

### `ReorderTagCommand`  (`commands/reorder_tag.rs`)

```rust
pub struct ReorderTagCommand {
    pub moved_id:   TagId,
    pub from_index: usize,
    pub to_index:   usize,
}
```

**`undo`:** `ctx.tag_list.reorder_tag_to_index(self.moved_id, self.from_index)`
**`redo`:** `ctx.tag_list.reorder_tag_to_index(self.moved_id, self.to_index)`

**Where to push (binary: `FolderWorkspace::handle_file_name_panel`, `DragEnded` branch):**
```rust
if let (Some(did), Some(idx)) = (dragged_id, drop_index) {
    let from_index = self.file_workspace.tag_list().checked_index_of(did);
    self.file_workspace.reorder_tag_to_index(did, idx);
    if let Some(fi) = from_index {
        self.history.push(Box::new(ReorderTagCommand {
            moved_id: did, from_index: fi, to_index: idx,
        }));
    }
}
```

`TagList::checked_index_of(id) -> Option<usize>` must exist (add if missing — returns position in `selected_tag_ids`).

---

## Binary wiring

### Fields to add to `FolderWorkspace`

```rust
history: History,
```

### New method to add to `FileWorkspace<S>`

```rust
pub fn tag_list_mut(&mut self) -> &mut TagList<S> { &mut self.tag_list }
```

### New messages (in `folder_workspace::messages.rs`)

```rust
Undo,
Redo,
```

### Keyboard bindings (in `src/app/` subscription)

```rust
// Ctrl+Z → Undo,  Ctrl+Y or Ctrl+Shift+Z → Redo
// Add alongside the existing PageUp/PageDown bindings
```

### Handler pattern

```rust
Message::Undo => {
    if !self.history.can_undo() { return Task::none(); }
    let Some(dir) = self.directory.as_mut() else { return Task::none(); };
    let tl = self.file_workspace.tag_list_mut();
    let mut ctx = UndoContext { directory: dir, tag_list: tl };
    match self.history.undo(&mut ctx) {
        Ok(()) => self.refresh_after_undo_redo(),
        Err(e) => { log::warn!("Undo failed: {}", e); Task::done(Message::ReportError(e.to_string())) }
    }
}
// Message::Redo: symmetric
```

### Post-undo/redo refresh

```rust
fn refresh_after_undo_redo(&self) -> Task<Message> {
    // Re-open the now-selected file — handles both navigate undo (different file)
    // and reorder undo (same file; file_workspace.set_file re-reads tag order from core).
    let file = self.directory.as_ref().and_then(|d| d.selected_file()).cloned();
    match file {
        Some(f) => Task::done(Message::FileOpened(f)),
        None    => Task::none(),
    }
}
```

---

## Failure handling

- `Undoable::undo/redo` returns `Result<(), UndoError>`.
- `History` leaves stacks unchanged on `Err` (peek-then-commit).
- Binary: emit `Message::ReportError(e.to_string())`, call `log::warn!`, skip UI refresh.

---

## Unit test pattern

Use `FakeAppStorage` in `frename-core` tests:

```rust
#[test]
fn undo_reorder_tag() {
    let store = FakeAppStorage::new();
    let snapshot = snapshot_with_tags(&["A", "B", "C"]);
    let mut tag_list = TagList::new(store.clone(), snapshot);
    let id_b = tag_list.find_by_name("B").unwrap().id();

    let fi = tag_list.checked_index_of(id_b).unwrap(); // 1
    tag_list.reorder_tag_to_index(id_b, 2);

    let mut history = History::new(50);
    history.push(Box::new(ReorderTagCommand { moved_id: id_b, from_index: fi, to_index: 2 }));

    let mut dir = Directory::new_empty(store);
    let mut ctx = UndoContext { directory: &mut dir, tag_list: &mut tag_list };
    history.undo(&mut ctx).unwrap();
    assert_eq!(tag_list.checked_index_of(id_b).unwrap(), 1); // back to B

    history.redo(&mut ctx).unwrap();
    assert_eq!(tag_list.checked_index_of(id_b).unwrap(), 2); // C, B, A
}
```

---

## Adding a new command (checklist)

1. [ ] Create `undo/commands/<name>.rs` with `pub struct <Name>Command { ... }`
2. [ ] Implement `Undoable` (both `undo` and `redo`)
3. [ ] `undo/commands/mod.rs`: `pub mod <name>; pub use <name>::<Name>Command;`
4. [ ] Push `Box::new(<Name>Command { ... })` at the right handler in the binary
5. [ ] Add `pub use` in `undo/mod.rs` and `lib.rs` if the app needs it directly
6. [ ] Write unit test: do → push → undo → assert; redo → assert

## Adding a new undoable core class (checklist)

1. [ ] Core type stays clean — no undo in its API
2. [ ] Create `undo/wrappers/<name>.rs`: `pub struct UndoableXxx<S, H: CommandSink> { inner: Xxx<S>, sink: H }`
3. [ ] Mutating methods: capture before-state → call `self.inner.method(...)` → push command → return same value
4. [ ] Read-only methods: delegate to `self.inner`
5. [ ] Add command types in `undo/commands/` for each undoable operation
6. [ ] App holds `UndoableXxx` instead of `Xxx`; call sites unchanged
