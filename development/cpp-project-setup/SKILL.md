---
name: cpp-project-setup
description: "Modern C++ project setup: CMake/CMakePresets, vcpkg, Ninja, VS Code/clangd, GoogleTest, clang-format/tidy, Doxygen, CI, macOS/Linux/Windows. Use for bootstrapping or modernizing host-side C++ apps and libraries; prefer embedded-project-setup for MCU firmware and cross-debug flows."
---

# Modern C++ Project Setup

## Overview

Create or modernize a C++ project around a reproducible toolchain:

```text
Git -> GitHub -> VS Code -> CMakePresets + vcpkg -> Ninja -> compiler -> tests/lint/docs
```

Prefer project-local, repeatable setup over global machine assumptions. First classify the user's working directory and host platform, then either generate a greenfield scaffold or patch the existing project without erasing its current pipeline.

## Workflow

1. Determine the user's working directory and whether a project already exists.
   - Check the user-provided path or current working directory before writing files.
   - Treat the directory as an existing project if it already has source files, `CMakeLists.txt`, build scripts, package metadata, editor config, CI, docs, or a git history.
   - For existing work, inventory the full development pipeline before editing: build system, dependency manager, compiler and standard, presets/tasks/scripts, tests, format/lint/static analysis, docs, debugger/editor integration, CI, packaging/install rules, and generated artifacts.
   - For greenfield work, default to an app plus reusable library target, C++20, Ninja, vcpkg manifest mode, GoogleTest, clang-format, clang-tidy, Doxygen, and VS Code settings.
   - If the request is about MCU firmware, OpenOCD, linker scripts, startup code, `arm-none-eabi`, or Cortex-Debug, switch to `embedded-project-setup`.

2. Detect the user's host development environment.
   - Determine OS and architecture: macOS/Linux/Windows plus arm64 or x64. Use local commands such as `uname -s`, `uname -m`, `sysctl -n machdep.cpu.brand_string`, or PowerShell/.NET runtime information where appropriate.
   - Select a host profile: `macos-arm64`, `macos-x64`, `linux-x64`, `linux-arm64`, `windows-x64`, or `windows-arm64`.
   - If the agent is running somewhere other than the user's real development machine, ask for the user's OS/architecture instead of assuming the sandbox matches their workstation.

3. Generate or update the project.
   - For greenfield scaffolding, run from this skill directory:

```bash
python3 scripts/scaffold_cpp_project.py \
  --name my_app \
  --out /path/to/workspace/my_app \
  --host-platform macos-arm64
```

   - The scaffold script renders reusable standard configuration from `assets/` for CMake, CMake presets, vcpkg, and VS Code. Update those assets when the shared project standard changes; update the Python script when generation logic, arguments, or dynamic source files change.
   - For existing projects, use `references/cpp-project-blueprint.md` as a checklist and adapt to the repository's current style instead of replacing unrelated files.
   - Omit `--host-platform` only when generating on the same machine where the project will be developed; the script will auto-detect that host.

4. Keep the toolchain contract explicit.
   - Use `CMakePresets.json` for configure/build profiles.
   - Use vcpkg manifest mode through `vcpkg.json`.
   - Use host-specific vcpkg triplets such as `arm64-osx`, `x64-osx`, `x64-linux`, `arm64-linux`, `x64-windows`, and `arm64-windows`.
   - Use Ninja as the generator unless the user or platform requires otherwise.
   - Use Clang on macOS, GCC on Linux, and MSVC on Windows by default.

5. Wire editor support.
   - Recommend VS Code extensions: CMake Tools, clangd, CodeLLDB for macOS/Linux, and Microsoft C/C++ debugging support for Windows.
   - Disable competing IntelliSense when clangd is responsible for semantic analysis.
   - Make `compile_commands.json` available through CMake configure output and point clangd at the active preset's build directory.
   - Add launch configurations for the generated executable on macOS/Linux and Windows when creating a cross-platform scaffold.

6. Add quality gates.
   - Add GoogleTest tests with `ctest`.
   - Add `.clang-format` and `.clang-tidy`.
   - Add a Doxygen configuration path, but do not require docs generation for a normal build.
   - Add CI only when requested or when the project setup task includes GitHub/GitHub Actions.

## Validation

Run the strongest available validation for the target machine:

```bash
cmake --list-presets
bash scripts/bootstrap_vcpkg.sh
cmake --preset macos-arm64-debug
cmake --build --preset macos-arm64-debug
ctest --test-dir build/macos-arm64-debug --output-on-failure
bash scripts/format.sh --check
cmake --preset macos-arm64-tidy
cmake --build --preset macos-arm64-tidy
cmake --build --preset macos-arm64-debug --target docs
```

Adjust preset names for the selected host profile. On Windows, use `pwsh scripts/bootstrap_vcpkg.ps1` and `pwsh scripts/format.ps1 -Check`. If vcpkg, compilers, or Doxygen are unavailable, report exactly what was skipped and why.

## References

- Read `references/cpp-project-blueprint.md` when choosing project layout, presets, dependency policy, editor settings, tests, formatting, linting, docs, or CI details.
- Read the scaffold script before changing its generated files or adding new options.
- Read `assets/` before changing standard generated configuration files; treat those files as templates and keep project-specific values behind `@PLACEHOLDER@` variables.
