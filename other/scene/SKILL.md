---
name: scene
description: Manipulate Godot scene trees and nodes via the AgentBridge execute tool — use when adding, removing, or inspecting nodes programmatically.
type: implementation
---

# Godot Scene Manipulation

> You are an expert Godot editor automation engineer who manipulates live scene trees through AgentBridge GDScript execution.

```bash
GDEXEC="bash ${CLAUDE_SKILL_DIR}/../runner/scripts/godot-exec.sh"
```

## Overview

Use `$GDEXEC --execute` to run GDScript inside the live Godot editor process via AgentBridge. All scene manipulations happen in the currently open scene. Changes are not persisted until you explicitly save. Always assign `node.owner = root` for any node that must be serialized to disk.

## Common Patterns

**Get the edited scene root:**
```bash
$GDEXEC --execute 'print(EditorInterface.get_edited_scene_root().name)'
```

**Add a node to the scene:**
```bash
$GDEXEC --execute - <<'GD'
var root = EditorInterface.get_edited_scene_root()
var node = MeshInstance3D.new()
node.name = "MyMesh"
root.add_child(node, true)
node.owner = root  # required for serialization
GD
```

**Find a node by name:**
```bash
$GDEXEC --execute - <<'GD'
var root = EditorInterface.get_edited_scene_root()
var player = root.get_node_or_null("Player")
if player:
    print("Found: ", player.get_class())
GD
```

**Remove a node:**
```bash
$GDEXEC --execute - <<'GD'
var root = EditorInterface.get_edited_scene_root()
var node = root.get_node_or_null("OldNode")
if node:
    node.queue_free()
GD
```

**Set a node property:**
```bash
$GDEXEC --execute - <<'GD'
var root = EditorInterface.get_edited_scene_root()
var mesh: MeshInstance3D = root.get_node("MyMesh")
mesh.position = Vector3(0, 1, 0)
GD
```

**Query node metadata:**
```bash
$GDEXEC --execute - <<'GD'
var root = EditorInterface.get_edited_scene_root()
var node = root.get_node("Player")
print("Meta keys: ", node.get_meta_list())
if node.has_meta("team"):
    print("team = ", node.get_meta("team"))
GD
```

**Check if a node is queued for deletion before accessing it:**
```bash
$GDEXEC --execute - <<'GD'
var root = EditorInterface.get_edited_scene_root()
var node = root.get_node_or_null("Temporary")
if node and not node.is_queued_for_deletion():
    print("Safe to access: ", node.name)
GD
```

**Select a node in the Scene panel:**
```bash
$GDEXEC --execute - <<'GD'
var root = EditorInterface.get_edited_scene_root()
var node = root.get_node("Player")
EditorInterface.select_node(node)
GD
```

## Bulk Operations

**Set a property on all children of a given type:**
```bash
$GDEXEC --execute - <<'GD'
var root = EditorInterface.get_edited_scene_root()
for child in root.get_children():
    if child is Light3D:
        child.light_energy = 2.0
        print("Updated: ", child.name)
GD
```

**Rename all nodes matching a prefix:**
```bash
$GDEXEC --execute - <<'GD'
var root = EditorInterface.get_edited_scene_root()
var index = 0
for child in root.get_children():
    if child.name.begins_with("Enemy"):
        child.name = "Enemy_%02d" % index
        index += 1
GD
```

**Recursively collect all nodes of a type:**
```bash
$GDEXEC --execute - <<'GD'
func collect(node: Node, type: String, result: Array) -> void:
    if node.get_class() == type:
        result.append(node)
    for child in node.get_children():
        collect(child, type, result)

var root = EditorInterface.get_edited_scene_root()
var meshes = []
collect(root, "MeshInstance3D", meshes)
print("Found %d MeshInstance3D nodes" % meshes.size())
GD
```

## Resource Operations

**Load a PackedScene and instantiate it into the scene:**
```bash
$GDEXEC --execute - <<'GD'
var root = EditorInterface.get_edited_scene_root()
var packed: PackedScene = load("res://scenes/enemy.tscn")
var instance = packed.instantiate()
instance.name = "Enemy"
root.add_child(instance, true)
instance.owner = root
GD
```

**Set an exported Resource property on a node:**
```bash
$GDEXEC --execute - <<'GD'
var root = EditorInterface.get_edited_scene_root()
var node = root.get_node("Terrain")
var mat: StandardMaterial3D = load("res://materials/ground.tres")
node.set("material_override", mat)
GD
```

**Scan the filesystem after creating files programmatically:**
```bash
$GDEXEC --execute 'EditorInterface.get_resource_filesystem().scan()'
```

Call this any time you create or modify files on disk outside of the editor (e.g., via a shell script) so the editor's FileSystem dock picks them up immediately.

## Editor Operations

**Save the current scene (active scene only):**
```bash
$GDEXEC --execute 'EditorInterface.save_scene()'
```

Use `EditorInterface.save_scene()` to save only the currently edited scene. Use `--save-all` to flush every open and dirty resource to disk.

**Save all open resources:**
```bash
$GDEXEC --save-all
```

**Perform an undoable operation with EditorUndoRedoManager:**
```bash
$GDEXEC --execute - <<'GD'
var root = EditorInterface.get_edited_scene_root()
var node = root.get_node("Player")
var undo_redo = EditorInterface.get_editor_undo_redo()

undo_redo.create_action("Move Player")
undo_redo.add_do_method(node, "set", "position", Vector3(5, 0, 0))
undo_redo.add_undo_method(node, "set", "position", node.position)
undo_redo.commit_action()
GD
```

`create_action` names the entry in Edit > Undo history. Always pair every `add_do_method` with a corresponding `add_undo_method` so Ctrl+Z works correctly.

## Common Pitfalls

- **Missing `node.owner = root`** — nodes added via `add_child()` without setting `owner` are invisible to the scene serializer and will silently disappear on save/reload. Set `owner` recursively for instantiated subscenes.
- **`queue_free()` is deferred** — the node is not freed until the end of the current frame. Accessing it immediately after calling `queue_free()` is safe, but guard with `is_queued_for_deletion()` if another code path may have already freed it.
- **`load()` returns `null` on a bad path** — always check the return value. Typos in `res://` paths fail silently if you skip the null check, causing a null dereference crash on the next property access.
- **`EditorInterface.save_scene()` only saves the root scene** — it does not save modified sub-resources or inherited scenes that live in separate files. Use `ResourceSaver.save()` explicitly for those, or call `--save-all` to catch everything.
- **Filesystem not refreshed after external file writes** — if you create `.tscn`/`.tres`/`.gd` files from a shell script, call `EditorInterface.get_resource_filesystem().scan()` afterwards or the editor will not see them and `load()` will return `null`.
- **`get_node()` throws on missing paths** — prefer `get_node_or_null()` and check the result; `get_node()` crashes the script on an invalid NodePath, which silently aborts the entire `--execute` invocation.

## References

- [SceneTree — Godot docs](https://docs.godotengine.org/en/stable/classes/class_scenetree.html)
- [Node — Godot docs](https://docs.godotengine.org/en/stable/classes/class_node.html)
- [EditorInterface — Godot docs](https://docs.godotengine.org/en/stable/classes/class_editorinterface.html)
- [EditorUndoRedoManager — Godot docs](https://docs.godotengine.org/en/stable/classes/class_editorundoredomanager.html)
- [PackedScene — Godot docs](https://docs.godotengine.org/en/stable/classes/class_packedscene.html)
- [ResourceFilesystem — Godot docs](https://docs.godotengine.org/en/stable/classes/class_editorfilesystem.html)
- [ResourceSaver — Godot docs](https://docs.godotengine.org/en/stable/classes/class_resourcesaver.html)
