---
name: clangd-lsp
description: >-
  Set up and verify C/C++ language intelligence with clangd in Cursor (extension,
  compile_commands.json, CMake) or Claude Code (clangd-lsp plugin). Use for .cpp/.h
  files, missing completions, or Blunder Engine C++20 development.
---

# clangd LSP (clangd-lsp)

C/C++ language server ([clangd](https://clangd.llvm.org/)) for code intelligence, diagnostics, and formatting.

**Source:** [anthropics/claude-plugins-official — clangd-lsp](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/clangd-lsp) (adapted for Cursor).

## Important: Cursor vs Claude Code

| Environment | How C/C++ intelligence works |
|-------------|------------------------------|
| **Cursor IDE** | **clangd** extension + `compile_commands.json` (often via CMake) |
| **Claude Code** | Official `clangd-lsp` plugin + `clangd` on PATH + LSP enabled |

In **Cursor**, this skill guides extension + compilation database setup. It does not replace the editor LSP with a skill file.

## Supported extensions

`.c`, `.h`, `.cpp`, `.cc`, `.cxx`, `.hpp`, `.hxx`, `.C`, `.H`

## Install clangd binary

### Windows (recommended)

```powershell
winget install LLVM.LLVM
clangd --version
```

Ensure LLVM `bin` is on PATH (e.g. `C:\Program Files\LLVM\bin`).

Download: [LLVM releases](https://github.com/llvm/llvm-project/releases) · [clangd install guide](https://clangd.llvm.org/installation)

### macOS

```bash
brew install llvm
export PATH="/opt/homebrew/opt/llvm/bin:$PATH"
clangd --version
```

### Linux

```bash
# Ubuntu/Debian
sudo apt install clangd
# Fedora: sudo dnf install clang-tools-extra
# Arch: sudo pacman -S clang
```

## Cursor setup (recommended)

### 1. Install extensions

| Extension | ID |
|-----------|-----|
| clangd | `llvm-vs-code-extensions.vscode-clangd` |
| CMake Tools | `ms-vscode.cmake-tools` |

```powershell
cursor --install-extension llvm-vs-code-extensions.vscode-clangd
cursor --install-extension ms-vscode.cmake-tools
```

**Note:** Disable or avoid running **Microsoft C/C++** IntelliSense alongside clangd (conflicts). Prefer clangd as the sole C++ language server.

### 2. Provide `compile_commands.json`

clangd requires a compilation database at the project root (or via `.clangd` `CompileFlags`).

**CMake (Ninja generator — best for clangd):**

```cmake
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
```

After configure, symlink or copy to repo root:

```powershell
# Example: from build tree to workspace root
cmd /c mklink compile_commands.json build\vs2026-debug\compile_commands.json
```

**Visual Studio multi-config generators** may not emit `compile_commands.json` by default. Options:

- Use a **Ninja** CMake preset for editor/CI analysis only, or
- Run CMake with `-DCMAKE_EXPORT_COMPILE_COMMANDS=ON` and a generator that supports it, or
- Use **CMake Tools** “Scan for Kits” + configure; some setups export via `cmake.compileCommands` setting.

### 3. Optional `.clangd` (repo root)

```yaml
CompileFlags:
  Add: [-std=c++20]
Diagnostics:
  UnusedIncludes: Strict
```

Tune includes for large trees (e.g. skip heavy `engine/3rdparty/` indexing) with `If` blocks or `Index` settings as needed.

### 4. Verify

- Open a `.cpp` file → hover, go-to-definition, diagnostics after index completes.
- **Output** → **clangd** for log errors.
- Command palette: `clangd: Restart language server` after regenerating `compile_commands.json`.

### 5. Suggested Cursor / VS Code settings

```json
{
  "clangd.path": "clangd",
  "clangd.arguments": ["--background-index", "--clang-tidy"],
  "cmake.configureOnOpen": true,
  "C_Cpp.intelliSenseEngine": "disabled"
}
```

## Blunder Engine notes

- **Stack:** C++20, CMake 4+, Vulkan, VS 2026 — see [AGENTS.md](https://github.com/BearThreeStones/Blunder-Engine/blob/main/AGENTS.md) build presets (`vs2026-debug`, etc.).
- **Configure:** `cmake --preset vs2026-debug` from Developer PowerShell.
- **Headers:** Many includes under `engine/src/runtime/`; compile DB must reflect actual target include paths (`engine_runtime`, `engine_editor`).
- **Regenerate** `compile_commands.json` after CMake option or dependency changes (Slint submodule, new targets).

## Claude Code setup (if also using Claude Code CLI)

1. Install `clangd` on PATH (see above).
2. Enable LSP: `ENABLE_LSP_TOOL=1` in shell or `~/.claude/settings.json`.
3. Install marketplace plugin `clangd-lsp` via `/plugin` in Claude Code.
4. Open workspace from directory containing `compile_commands.json` or `.clangd`.

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| “No compile commands” | Generate/link `compile_commands.json`; restart clangd |
| Wrong headers / millions of errors | Reconfigure CMake; check DB matches active preset (Debug vs Release) |
| Slow indexing | `.clangd` `Index: Background: Skip` for vendored trees; exclude `build/`, `.cmake_deps/` |
| Two C++ plugins fighting | Disable MS C/C++ IntelliSense; use clangd only |
| MSVC-only flags in DB | Prefer Ninja + clang-cl or fix flags in `.clangd` `CompileFlags` |

## When helping the user

1. Detect environment: Cursor vs Claude Code.
2. Readonly checks: `clangd --version`, `Test-Path compile_commands.json`, CMake presets.
3. Do not install LLVM/extensions or edit project CMake without approval.
4. For non-C++ repos, state clangd does not apply.
