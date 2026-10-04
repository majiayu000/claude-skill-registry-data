---
name: core-dev
description: >
  Core development guide for frename-core. Use when: adding or changing traits (StoredTagStore,
  AppStateStore), modifying TagList logic, working with OrderedCollection, adding Tag fields,
  changing FileSnapshot/FileTagger, writing core tests, or adding database schema/migrations.
disable-model-invocation: false
---

# Core Development Guide — frename-core

## WHEN to use this skill
- Adding or changing a `StoredTagStore` or `AppStateStore` method
- Modifying `TagList` (ordering, filtering, toggle, create, save, remove, reorder)
- Working with `OrderedCollection` (insert, insert_before, rebalance)
- Adding fields to `Tag`, `File`, `Directory`, or `FileSnapshot`
- Changing file name parsing/saving (`FileTagger`)
- Writing core tests
- Adding database tables, columns, or migrations

For undo/redo infrastructure (`crates/frename-core/src/undo/`), use the **`undo-dev`** skill instead.

---

## Crate boundary

`frename-core` is a pure library. **No iced, no UI types.** It exposes:

```
frename_core::
  AppDatabase, LoggingAppStateStore, FakeAppStorage (test)
  AppStateStore, StoredTagStore, Initializable  (traits)
  Directory<S>, File, FileSnapshot, FolderAndFile
  TagList<S>, Tag, TagId, StoredTag, TagColorMapping
  OrderedCollection<K,V>, OrderKey, OrderedThing
  FileTagger, SaveAndReparse
```

---

## Traits

### `StoredTagStore` (`db/traits.rs`)
All methods return `Result<_, Box<dyn Error + Send + Sync>>`.

| Method | What it does |
|---|---|
| `get_stored_tags()` | Returns all stored tags ordered by `sort_order` |
| `get_tag_color_mapping()` | Returns tag-name → color-index mapping |
| `save_tag(tag, color)` | **Upsert** by tag id: insert or update name + sort_order + color |
| `remove_stored_tag_by_id(uuid)` | Delete tag and its color mapping by id |
| `update_tag_orders(&[(uuid, i64)])` | Bulk-update `sort_order` after rebalance |

`TagList` always calls `save_tag()` (upsert). Never call `add_stored_tag` from production code.

Trait is `Send + Sync` — safe to hold in `FileWorkspace<S>` and clone.

### `AppStateStore` (`db/traits.rs`)
| Method | What it does |
|---|---|
| `get_last_session()` | Returns `Option<FolderAndFile>` (last opened folder + file) |
| `set_last_folder_and_file(&FolderAndFile)` | Persist or update session |

### `Initializable` (`db/traits.rs`)
`fn initialize(&self) -> Result<(), rusqlite::Error>` — run migrations once at startup.
Always call via `LoggingAppStateStore::initialize()`.

---

## Adding a method to StoredTagStore

1. Add to trait in `db/traits.rs`
2. Implement in `impl StoredTagStore for AppDatabase` in `db/app_database.rs`
3. Implement in `impl StoredTagStore for FakeAppStorage` in `db/fake_app_storage.rs`
4. (If TagList needs to call it) add a wrapper to `TagList<S>` in `tags/tag_list.rs`
5. (If UI needs it) expose via `FileWorkspace<S>` in `src/features/file_workspace/state.rs`

---

## TagList

`TagList<S: StoredTagStore + Clone>` is the source of truth for all tag state.

### Internal structure
| Field | Type | Purpose |
|---|---|---|
| `tags_by_id` | `HashMap<TagId, Tag>` | All tag data; only place tag fields are stored |
| `display_tag_ids` | `OrderedCollection<TagId, ()>` | Display order (tag panel); set at init, only grows at front via `create_new_tag`; used for persistence |
| `selected_tag_ids` | `OrderedCollection<TagId, ()>` | File-name-panel order; same set as display; reorderable via `reorder_tag_to_index` |
| `filtered_display_tag_ids` | `Vec<TagId>` | Display after search filter; rebuilt by `rebuild_filtered_display_tag_ids()` after every mutation |

### Initialization order (critical — don't change)
1. Stored tags from DB → `tags_by_id` (checked = has_tag in snapshot, order = DB sort_order)
2. Snapshot tags not in stored → `tags_by_id` (checked = true, order = 0, stored = false)
3. Stored-but-not-in-snapshot tags → `display_tag_ids` (order from DB)
4. Snapshot tags (reversed, deduped) → `display_tag_ids` via `insert_before` so they appear first in snapshot order
5. `selected_tag_ids = display_tag_ids.clone()`
6. `rebuild_filtered_display_tag_ids()`

### Key methods
| Method | Effect on fields |
|---|---|
| `set_filter(query)` | Rebuilds `filtered_display_tag_ids` |
| `toggle_by_id(id)` | Flips `tag.checked` in `tags_by_id` |
| `create_new_tag(name)` | Inserts at front of both ordered collections; rebuilds filter |
| `save_tag(id)` | Calls `store.save_tag()`; sets `tag.stored=true`, assigns random color if new; if `display_tags_rebalanced`, also calls `store.update_tag_orders()` |
| `remove_stored_tag_by_id(id)` | Removes from store + both collections + map; rebuilds filter |
| `reorder_tag_to_index(moved_id, index)` | Moves in `selected_tag_ids` only (file name panel order) |
| `file_snapshot()` | Builds `FileSnapshot` from checked tags in `selected_tag_ids` order |

**After any mutation that changes the display set:** always call `rebuild_filtered_display_tag_ids()`.

### `display_tags_rebalanced`
Set to `true` when `OrderedCollection::insert_before()` triggers a rebalance.
Cleared in `save_tag()` after calling `update_tag_orders()`. Signals that all stored tag sort_orders must be re-persisted.

---

## OrderedCollection

`OrderedCollection<K, V>` is an ordered dictionary backed by `HashMap + BTreeSet`.
`OrderKey = i64`.

| Method | Behavior |
|---|---|
| `insert(key, value, order)` | Insert or replace at exact order key |
| `insert_before(key, value, before_id)` | Insert immediately before `before_id`; if `None`, insert before the first element; returns `true` if rebalanced |
| `remove(key)` | Remove; returns value |
| `get_order(key)` | Returns current `OrderKey` for the key |
| `iter()` | Yields `(id, value, order)` in ascending order |

**Rebalance:** when no integer fits between two adjacent order keys, all items are respread across `[1, i64::MAX-1]` with equal gaps. Callers check the return value of `insert_before` to know if orders need re-persisting.

---

## Tag

```rust
pub struct Tag {
    id: TagId,          // UUID wrapper
    tag: String,        // display name
    checked: bool,      // applied to current file
    color_index: u8,    // index into 16-color palette
    stored: bool,       // persisted in DB (false = snapshot-only or just created)
    order: OrderKey,    // matches display_tag_ids order at creation
}
```

- `stored = false` means the tag exists only in the UI / current file's snapshot.
- `toggle()` flips `checked`.
- `set_stored(true)` + `set_color_index(c)` called in `save_tag()`.

---

## FileSnapshot

Built by `TagList::file_snapshot()`. Contains:
- `tags: Vec<String>` — names of checked tags in `selected_tag_ids` order
- `name_without_extension: String`
- `extension: String`
- `initial_file_name: String`

`FileSnapshot::file_name()` = `tags.join(".") + "." + name + "." + ext`

**Parsing** (loading a file): `FileTagger::parse(path)` splits the file name by `.`: last segment = extension, second-to-last = name, rest = tags.

**Saving** (writing to disk): `snapshot.save_and_reparse(&path)` renames the file and re-parses to get the canonical snapshot.

---

## Database schema

Three tables (defined in `db/migrations.rs`):

| Table | Columns | Key |
|---|---|---|
| `folder_history` | `opened_at`, `folder_path`, `last_file_path` | `folder_path` unique |
| `stored_tags` | `id` (UUID text), `name`, `sort_order` | `id` unique |
| `tag_color_mapping` | `tag_name`, `color_index` | `tag_name` unique |

Colors are keyed by tag **name** (not id), so renaming a tag requires deleting the old mapping and inserting the new one — `save_tag()` handles this.

### Migrations: numbers collide across branches

Migrations run in version order, once each (`db/migrations.rs`). Two branches that each took
"the next number" collide: a database already at that version never runs the second one, so its
columns never appear and reading the settings fails. Before merging, and after every rebase,
check `migrations.rs` on `main` and renumber yours to follow its last one (the migration
constant's name, the list entry, and the version asserted by `running_migrations_twice_is_a_no_op`).

---

## Disk paths in a debug build

A debug build (or `--debug`) installs `InMemoryFileTagger`: renames and comment/metadata writes
happen in memory only, and `File::file_path()` is the name the file *would* have. Anything that
opens the real file — GStreamer, `std::fs`, another program — must go through
`FileTagger::disk_path(path)` first, as the media viewer and Describe with AI do; otherwise a file
renamed during the session (tag spacing, a tag toggle) is "not found". `--production` makes a
debug build write to disk.

Requests to paid APIs (Anthropic, Soniox) from a debug build are still real and billed; only
their results stay in memory.

---

## Tests

All core tests use `FakeAppStorage` (in `db/fake_app_storage.rs`).
Builder pattern:

```rust
let store = FakeAppStorage::new()
    .add_stored_tag(StoredTag::with_sort_order(Uuid::new_v4(), "Action", 1), 0)
    .add_stored_tag(StoredTag::with_sort_order(Uuid::new_v4(), "Comedy", 2), 1);
let list = TagList::new(store, FileSnapshot::default());
```

`FakeAppStorage::add_stored_tag(self, tag, color)` is a builder method (takes `self` by value), separate from the `StoredTagStore` trait.
