---
name: docs
description: Look up Godot 4.x API documentation via Context7 — use when API behavior is uncertain before writing code.
---

# Godot Docs

Use Context7 to retrieve up-to-date Godot 4.x documentation before implementing unfamiliar APIs.

## Workflow

1. **Resolve the library ID:**

```
mcp__plugin_context7_context7__resolve-library-id(libraryName="godot")
```

2. **Query for the specific API:**

```
mcp__plugin_context7_context7__query-docs(
  context7CompatibleLibraryId="<id from step 1>",
  query="Timer class autostart one_shot",
  tokens=3000
)
```

3. **Cite the version** from the returned docs before using the API.

## Common Queries

| Topic | Query string |
|---|---|
| Node lifecycle | `"_ready _process _physics_process lifecycle order"` |
| Signal patterns | `"signal emit connect callable"` |
| Resource loading | `"load preload ResourceLoader"` |
| Scene instantiation | `"PackedScene instantiate add_child"` |
| Physics | `"CharacterBody3D move_and_slide collision"` |
| Timer | `"Timer autostart one_shot timeout"` |
| Tweens | `"Tween create_tween PropertyTweener"` |
| Input | `"Input is_action_pressed get_axis"` |
| Shader globals | `"shader built-in TIME FRAGCOORD UV"` |
| UI anchors | `"Control anchor offset set_anchor_and_offset"` |

## When to Use

- Before implementing an API you haven't used in Godot 4.x
- When a method name or signature is uncertain
- When debugging and the error references an unknown built-in
- When the coder/shader/ui/architect skill's example doesn't cover your case
