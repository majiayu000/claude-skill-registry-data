---
name: source-sdk
license: MIT
description: Edit and review Valve Source SDK C/C++ code with AlliedModders conventions. Use for SDK headers and libraries, binary-compatible class reconstruction, signatures and vtables, project CMake, builds, tests and commit messages.
---

# Source SDK

This skill covers Valve/Source SDK C and C++ code with AlliedModders-specific modernizations.
Public headers may describe layouts used by shipped game binaries; successful compilation alone
does not establish binary compatibility.

Keep edits local, conservative and consistent with the surrounding file. Apply repository
instructions before this skill where they differ. Read the references relevant to the task;
the detailed examples and procedures remain there rather than being loaded for every edit.

## Repository Orientation

- Treat the SDK root as the working directory unless the task points elsewhere.
- Library code and public headers live under `common/`, `entity2/`, `game/`, `interfaces/`,
  `kv3lib/`, `mathlib/`, `networksystem/`, `public/` and `tier1/`.
- Project-owned build files live under `cmake/` and in `CMakeLists.txt`.
  `CMakeGameManifests.json` selects game definitions; `CMakePresets.json` defines build presets.
- `lib/<platform>/` holds imported binaries, `sym/` holds export maps and `devtools/bin/`
  holds per-platform `protoc` executables.
- Project targets use C17 / C++17; `tests/` uses the in-repo runner and C++23.
- Treat `thirdparty/` as vendored code unless the task explicitly concerns it.

## Formatting

Follow `.clang-format` first, then the local file style. Read the
[code style reference](references/style.md) when writing, reviewing or reformatting C/C++.

- Use tabs, Allman braces and spaces inside parentheses, square and angle brackets:
  `vec[ i ]`, `int m_nChild[ 2 ];`, `CUtlVector< int >`, `static_cast< int >( nValue )`.
  Empty brackets stay tight: `[]`, `<>`, `()`.
- Bind pointer and reference markers to the variable name.
- Keep includes in their existing order; `SortIncludes: false` is intentional.
- Preserve line endings and encoding. Avoid unrelated reformatting or alignment changes.

```cpp
void SetValue( int nValue );

if ( bReady )
{
	SetValue( nValue );
}
```

## Naming

Preserve Source naming: `p`, `n`, `b`, `m_`, `C`, `I`, `M` and `_t` where applicable.
See the [naming conventions](references/style.md#naming) for meanings and examples.

## C++ Practices

- Prefer existing project helpers, container types, allocation patterns and platform abstractions.
  Read the [container reference](references/containers.md) when selecting or using strings, containers,
  buffers or `KeyValues3`.
- Preserve ownership and lifetime expectations, including fixed-buffer and stack-buffer storage.
- Preserve public ABI/API names, binary layout, exported symbols and calling conventions.
- Use modern C++ facilities only where nearby code already uses them or the task requires them.
- Avoid exceptions and RTTI-dependent designs unless the subsystem already uses them.
- Keep platform guards precise; consider compile-time cost and overload ambiguity in public headers.

## Reverse Engineering and Binary Work

Read the [reverse engineering reference](references/reverse-engineering.md) for signatures, offsets,
vtables, gamedata, disassembly or binary-reconstructed declarations.

- Check whether `ida-pro-mcp` is available before editing binary-derived code or gamedata.
  Use it as the primary source for IDA facts when available.
- Use functions, xrefs, strings, types and decompiler output as evidence. Never invent offsets,
  addresses, signatures, symbol names or vtable indexes.
- If IDA is unavailable, state the limitation and use repository evidence only.
- Preserve exact field offsets, padding and virtual slot order. Keep unknown signatures opaque.
- Add a `COMPILE_TIME_ASSERT` for every reconstructed type with a verified size, near the
  declaration that owns its layout. Guard platform- or branch-specific sizes appropriately.
- Record important binary-derived assumptions in the final response or a useful technical comment.

### Schema Declarations

Read the [schema reference](references/schema.md) when determining whether a class is registered
in the schema system, recovering class and field metadata, or identifying `noschema` members.

## CMake Conventions

Read the [CMake reference](references/cmake.md) for source lists, targets, build options, game manifests
or protobuf generation.

- Use lowercase built-in commands, uppercase project variables and tabs.
- Append to the nearest existing `SOURCESDK_<MODULE>_*`, `SOURCESDK_*` or `PLATFORM_*` list.
- Keep platform detection in `cmake/platform/shared.cmake` and platform flags in their modules.
- Reuse existing import, clangd and protobuf helpers. Keep binary compatibility flags deliberate.
- Keep generated protobuf output out of commits unless the task or repository requires it.

## Build and Verification

Read the [build and workflow reference](references/workflow.md) for verification commands, presets and test routing.

- Use the narrowest useful check: formatting or targeted compilation for headers, the smallest
  relevant target for implementation changes, configure for CMake, JSON and binary checks for gamedata.
- Run full builds only when the risk justifies them or the user asks.
- Report exactly what was verified and what could not be run.

## Git and Workspace Safety

- Inspect `git status --short` before and after edits. Preserve existing user changes.
- Keep commits, branch operations, rebases and force updates out of scope unless requested.
- Do not rewrite unrelated files or modify generated files without a task-specific reason.

## Commit Message Style

Use a short imperative subject beginning with `Add`, `Update`, `Remove`, `Fix`, `Correct`,
`Move` or `Actualize`. Put C++ symbols and important file-like identifiers in backticks.
A `CMake:` prefix is acceptable for CMake-only changes. See
[commit message conventions](references/workflow.md#commit-messages) for examples and the co-author trailer.

## Documentation

Write technical documentation in clear English. Keep examples short and consistent with the
project style; update nearby documentation when behavior, APIs or build flags change.

## Tools

- Use `rg` for text searches and `rg --files` for file discovery.
- For structural codebase exploration, use the installed `codebase-memory` skill when available
  and follow its coverage and source-verification guidance.
- Use the shell for build, test and git commands; make focused edits to existing files.
