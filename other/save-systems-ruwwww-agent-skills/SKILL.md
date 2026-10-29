---
name: save-systems
description: >
  Design save/load for game state — choosing what to serialize, file formats,
  save slots, atomic crash-safe writes, schema versioning and migration, and
  autosave. Engine-neutral. Use when the user mentions save system, save/load,
  game state persistence, save slots, autosave, save file corruption, or
  migrating old saves to a new version.
---

# Save systems

A save file is a **serialized snapshot of game state** that survives restarts.
The hard parts aren't writing bytes — they're choosing *what* to save, writing it
so a crash mid-save can't corrupt it, and reading *old* saves after you ship a
patch. Get those three right and the rest is plumbing.

## When to use

- Use to persist progress: player stats, inventory, world flags, settings,
  positions — across sessions and game updates.
- Use to design save slots, quicksave/autosave, and crash-safe writes.
- Use when old save files break after a content/code change (versioning &
  migration).

**When *not* to use:** for Roblox cloud persistence specifics, use
`roblox-datastores`. For the data model the save serializes (resources/SOs), use
`godot-resources` / `unity-scriptableobjects`. For Godot's `FileAccess`/
`ResourceSaver` and `user://` paths, defer to the Godot engine skill while
applying the patterns here.

## Core workflow

1. **Decide what state is authoritative.** Save the *data* (hp, position, seed,
   unlocked flags), not engine objects or scene nodes. You will reconstruct
   objects from data on load — never serialize live node references.
2. **Define a versioned schema.** Every save embeds a `version` integer. This is
   the single most important field for a game you intend to patch.
3. **Pick a format.** JSON/text for readability and debuggability; a binary
   format for size/speed or mild tamper-resistance. Start with JSON.
4. **Write atomically.** Serialize to a temp file, flush, then rename over the
   real file. A crash leaves either the old save or the new one — never a
   half-written one.
5. **Load defensively.** Read version → migrate up to current → validate →
   instantiate. Keep a backup of the last good save and fall back on parse error.
6. **Autosave on safe boundaries** (level change, checkpoint), throttled, and to a
   separate slot so it can't clobber a manual save.
7. **Verify**: save, fully quit, relaunch, load — and confirm by inspection that
   state matches. Test loading a save from the previous version.

## Patterns

### 1. Serialize state as plain data (not engine objects)

```gdscript
# Build a dictionary of pure data. Each savable object reports its own state.
func capture_state() -> Dictionary:
    return {
        "version": SAVE_VERSION,                 # ALWAYS stamp the schema version
        "player": { "hp": player.hp, "pos": [player.position.x, player.position.y] },
        "inventory": player.inventory.to_array(),  # ids + counts, not Item nodes
        "flags": world.flags,                    # e.g. {"met_guard": true}
        "seed": world.seed,                      # regenerate procedural content
    }

# On load, RECONSTRUCT objects from the data — do not expect live references back.
func apply_state(data: Dictionary) -> void:
    player.hp = data["player"]["hp"]
    player.position = Vector2(data["player"]["pos"][0], data["player"]["pos"][1])
    player.inventory.from_array(data["inventory"])
    world.flags = data["flags"]
```

### 2. Atomic, crash-safe write (temp + rename)

```gdscript
# Godot 4.7. Write a temp file, keep the previous save as .bak, then rename.
func save_atomic(path: String, data: Dictionary) -> Error:
    var tmp := path + ".tmp"
    var f := FileAccess.open(tmp, FileAccess.WRITE)
    if f == null:
        return FileAccess.get_open_error()       # disk full, read-only, no permission...
    if not f.store_string(JSON.stringify(data)):
        return ERR_FILE_CANT_WRITE
    f.close()                                    # flushes Godot's buffer to the OS
    if FileAccess.file_exists(path):
        DirAccess.rename_absolute(path, path + ".bak")   # keep the last good save
    return DirAccess.rename_absolute(tmp, path)

func load_save(path: String) -> Dictionary:      # empty = nothing loadable
    for p in [path, path + ".bak"]:              # .bak covers a crash between renames
        if FileAccess.file_exists(p):
            var data = JSON.parse_string(FileAccess.get_file_as_string(p))
            if data is Dictionary and data.has("version"):
                data["version"] = int(data["version"])   # JSON numbers load as float
                return data
    return {}
# WRONG: opening `path` directly and writing in place — a crash mid-write leaves a
# truncated, unloadable save and destroys the player's progress.
```

A crash now leaves the old save, the new one, or (between the two renames) only
the `.bak` — which the loader tries next. Two limits to know: `rename()` replaces
the target atomically on POSIX (same volume), but Godot's Windows `rename_absolute`
deletes the target and then moves, so that platform relies on the `.bak` too; and
neither `flush()` nor `close()` calls `fsync`, so a power cut right after a save
can still lose the newest file. Check the returned `Error` and tell the player
when a save fails instead of carrying on.

### 3. Versioned load with migration

```python
SAVE_VERSION = 3

def load_save(raw_bytes):
    data = parse(raw_bytes)                  # JSON/binary -> dict
    v = int(data.get("version", 1))          # no field = the first shipped schema
    if v > SAVE_VERSION:
        raise NewerSaveError(v)              # save is from a newer build; refuse
    while v < SAVE_VERSION:                   # apply migrations in order, v -> v+1
        data = MIGRATIONS[v](data)
        v += 1
        data["version"] = v
    validate(data)                            # check required keys / ranges
    return data

# Each migration is a pure function from one version's shape to the next.
def migrate_1_to_2(d):
    d["flags"] = {k: True for k in d.pop("completed_quests", [])}  # list -> set-map
    return d
def migrate_2_to_3(d):
    d.setdefault("difficulty", "normal")      # new field: old saves get the default
    return d
MIGRATIONS = {1: migrate_1_to_2, 2: migrate_2_to_3}
```

### 4. Save slots + throttled autosave

```gdscript
const SLOT_PATH := "user://save_%d.json"      # manual slots 0..N
const AUTOSAVE_PATH := "user://autosave.json"  # separate file: never clobbers a slot
var _autosave_cooldown := 0.0

func autosave_if_due(dt: float) -> void:
    _autosave_cooldown -= dt
    if _autosave_cooldown <= 0.0:
        save_atomic(AUTOSAVE_PATH, capture_state())
        _autosave_cooldown = 60.0             # throttle: at most once a minute
# Trigger an immediate autosave on checkpoints/level transitions, not mid-combat.
```

## Pitfalls

- **Serializing engine objects/node paths** ties saves to scene structure;
  renaming a node breaks every old save. Save data, rebuild objects on load.
- **No version field.** The day you ship a patch, every existing save is a
  guessing game. Stamp `version` from version 1.
- **In-place writes** corrupt saves on crash/power loss. Always temp-write then
  rename; keep a `.bak`.
- **Trusting the file blindly.** Saves get truncated, hand-edited, or
  cloud-synced stale. Validate on load and fall back to backup on failure.
- **Floats and locale.** Text serializers can drop precision or use comma
  decimal separators in some locales. Use a locale-invariant serializer.
- **Godot JSON turns every number into a float**: `version` 3 loads as `3.0`,
  so `migrations.has(data["version"])` is false and integers above 2^53 (64-bit
  IDs, big seeds) lose digits. Convert with `int()` on load, store IDs as
  strings, or wrap the state in `JSON.from_native()` / `JSON.to_native()`, which
  round-trip `int`, `Vector2` and other engine types exactly.
- **Loading objects from save files.** Godot `str_to_var`/`get_var` with objects
  allowed, a `ConfigFile` that stores objects, or `ResourceLoader` on a `.tres`
  the player can swap will instantiate an object with a script attached, and that
  script runs during the load. Saves get shared online; keep them plain data.
- **Autosave clobbering manual saves**, or firing mid-action and saving an
  inconsistent state. Use a dedicated autosave slot and save on safe boundaries.
- **Storing secrets or trusting client saves in multiplayer.** A local save is
  player-controlled; never treat it as authoritative for online state. For cloud,
  handle the device's data limits and conflicts (`roblox-datastores`).

## References

- `references/versioning-and-migration.md` — schema evolution strategies, the
  migration chain, backups/rollback, format trade-offs (JSON vs binary), a
  load-time validation checklist, and where saves live per engine plus Steam
  Cloud setup.

## Related skills

- `roblox-datastores` — cloud persistence, request limits, session locking.
- `godot-resources`, `unity-scriptableobjects` — the data model you serialize.
- `procedural-gen` — store the seed to regenerate worlds instead of saving them.
- `rpg`, `survival-crafting`, `visual-novel` — genres that compose this skill.
