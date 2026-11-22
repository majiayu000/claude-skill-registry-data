---
name: yuzu-plugin-abi
description: Guard Yuzu's stable C plugin ABI, descriptor contract, and loader compatibility. Use when changing `sdk/include/yuzu/plugin.h`, `plugin.hpp`, plugin descriptors, `agents/core/src/plugin_loader.cpp`, built-in plugins, or plugin action surfaces that affect compatibility.
---

# Yuzu Plugin ABI

## Treat The Boundary As Hard

- Treat `sdk/include/yuzu/plugin.h` as the stable C ABI.
- Do not reorder or remove struct fields.
- Append new struct fields only at the end.
- Do not let C++ types, exceptions, or STL containers cross the C boundary.
- Bump `YUZU_PLUGIN_ABI_VERSION` when the binary contract changes.

## Keep The Runtime Contract Aligned

- Keep `plugin.hpp` convenience wrappers aligned with `plugin.h`.
- Keep `agents/core/src/plugin_loader.cpp` compatibility checks aligned with the declared ABI range.
- Preserve `yuzu_plugin_descriptor()` expectations and exported symbol names.

## Watch Action Surface Changes

- If a plugin adds, removes, or renames actions, inspect corresponding instruction definitions under `content/definitions/`.
- Keep descriptor strings, action arrays, and tests consistent.
- Recheck plugin loader diagnostics if the descriptor layout or SDK version fields change.

## Validate

- Build the agent targets.
- Run descriptor and loader coverage first, especially `tests/unit/test_new_plugins.cpp` and `tests/unit/test_plugin_loader.cpp`.
- Run the narrowest relevant agent suite before expanding outward.

## Invoke Sibling Skills

- Invoke `$yuzu-meson` for build-graph changes.
- Invoke `$yuzu-windows-msvc` if the change affects Windows export or loading behavior.
- Invoke `$yuzu-build` for compile and test flow.

## Read On Demand

- `sdk/include/yuzu/plugin.h`
- `sdk/include/yuzu/plugin.hpp`
- `agents/core/src/plugin_loader.cpp`
- `tests/unit/test_new_plugins.cpp`
- `tests/unit/test_plugin_loader.cpp`
- `content/definitions/`
