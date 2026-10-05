---
name: implementing-cpp
description: Implements C++17 desktop GUI code with wxWidgets, GTK3, or Qt framework patterns and CMake build system. Use when writing C++ desktop application code, creating GUI components, or implementing framework-specific features.
compatibility: Designed for Claude Code
metadata:
  allowed-tools: Read, Write, Edit, Glob, Grep, Bash
  argument-hint: [feature-or-component]
  stability: stable
  content-hash: sha256:4fdd42d49c686f7983e44accff97977741957768915408d403c050ce82380fb8
---

# C++ Desktop Implementation

**Target**: $ARGUMENTS

Implement C++ desktop GUI code following framework conventions, C++17 standards,
and CMake best practices. No over-engineering.

## Workflow

1. **Detect framework:**
   - `wxWidgets` in CMakeLists.txt or `wx/` includes -> wxWidgets
   - `gtk` in pkg-config or CMakeLists.txt -> GTK3
   - `Qt` in CMakeLists.txt or `.pro` file -> Qt
   - None detected -> ask user which framework
2. **Study existing patterns** in `src/` and `include/` structure
3. **Implement minimal solution** matching stated functionality
4. **Build and validate** with CMake
5. **Report** — list created files, build status

## C++ Standards

- **C++17 minimum** — use `std::optional`, `std::variant`, structured bindings
- **RAII** — acquire resources in constructors, release in destructors
- **Smart pointers** — `std::unique_ptr` by default, `std::shared_ptr` only when shared ownership required
- **Const-correctness** — `const` on methods, parameters, and locals where possible
- **No raw `new`/`delete`** — use smart pointers or container types

## Framework Patterns

### wxWidgets

- Use `wxBEGIN_EVENT_TABLE`/`wxEND_EVENT_TABLE` or `Bind()` for events
- Derive frames from `wxFrame`, dialogs from `wxDialog`
- Use sizers (`wxBoxSizer`, `wxGridSizer`) for layout, never absolute positioning
- Parent windows own children (no manual delete)

### GTK3

- Use `g_signal_connect` for signal/slot wiring
- Follow GObject conventions for custom widgets
- Use `GtkBuilder` with `.ui` files for complex layouts
- Proper `g_object_unref` / `g_free` for C API resources

### Qt

- Use signals/slots with `Q_OBJECT` macro and MOC
- Derive from `QWidget`, `QMainWindow`, `QDialog` as appropriate
- Use layouts (`QVBoxLayout`, `QHBoxLayout`, `QGridLayout`)
- Parent-child ownership model — parent deletes children

## CMake Best Practices

- **Target-based** — use `target_link_libraries`, `target_include_directories`
- **No global state** — avoid `include_directories()`, `link_libraries()`
- **Modern find** — `find_package()` with imported targets
- **Minimum version** — `cmake_minimum_required(VERSION 3.16)`
- **Platform conditionals:**

  ```cmake
  if(WIN32)
    # Windows-specific
  elseif(APPLE)
    # macOS-specific
  else()
    # Linux/Unix
  endif()
  ```

## Platform Compilation

Use preprocessor guards for platform-specific code:

```cpp
#ifdef _WIN32
  // Windows
#elif __APPLE__
  // macOS
#else
  // Linux/Unix
#endif
```

## Quality Checks

Before completing any task:

```bash
cmake --build build/ && ctest --test-dir build/ --output-on-failure
```

## Rules

- Follow existing code style (indentation, naming) in the project
- Create header declarations alongside implementations
- Use forward declarations to minimize include dependencies
- Prefer `#pragma once` over include guards
- Keep GUI logic separate from business logic
