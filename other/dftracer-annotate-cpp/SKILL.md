---
name: dftracer-annotate-cpp
description: C++ annotation rules for dftracer — RAII guard, REGION macros for main, UPDATE usage, and quick checklist
---

## C++ Annotation Rules (dftracer)

### C++ Rule 1 — Include and RAII guard for regular functions

Add the include after all existing `#include` lines in the .cpp file (never in a header):
```cpp
#include <dftracer/dftracer.h>
```

**Regular C++ functions** — use the RAII scope guard (no manual END needed):

```cpp
void my_function(const char *path) {
  DFTRACER_CPP_FUNCTION();                      // RAII — END called automatically when scope exits
  DFTRACER_CPP_FUNCTION_UPDATE("path", path);
  ...
  // No explicit END needed
}
```

- `DFTRACER_CPP_FUNCTION()` must be the **first statement** after the opening `{`.
- No manual END required — the destructor fires on scope exit.
- Never mix C and C++ macros in the same file.
- Never annotate header files (.h, .hpp) — only .cpp / .cxx source files.

### C++ Rule 2 — REGION macros only in C++ main; RAII everywhere else

**C++ main** — use `DFTRACER_CPP_REGION_START/END` instead of `DFTRACER_CPP_FUNCTION()`,
because the RAII destructor fires after `DFTRACER_CPP_FINI()`, which is wrong:

```cpp
int main(int argc, char **argv) {
  DFTRACER_CPP_INIT(nullptr, nullptr, nullptr);
  DFTRACER_CPP_REGION_START(main_region);       // ← REGION, not FUNCTION
  ...
  if (error) {
    DFTRACER_CPP_REGION_END(main_region);        // ← close region first
    DFTRACER_CPP_FINI();                         // ← then shut down tracer
    return 1;
  }
  ...
  DFTRACER_CPP_REGION_END(main_region);          // ← close region before normal return
  DFTRACER_CPP_FINI();
  return 0;
}
```

- Order at every exit point in main: **REGION_END → FINI → return/exit**.
- The region name (`main_region`) can be any valid C identifier.

### C++ Rule 3 — Where NOT to use REGION macros

- **C source**: never use `DFTRACER_C_REGION_START` / `DFTRACER_C_REGION_END`.
- **C++ regular functions**: never use `DFTRACER_CPP_REGION_*`. Use `DFTRACER_CPP_FUNCTION()`.
- **C++ main only**: use `DFTRACER_CPP_REGION_START/END`.

### C++ Rule 4 — UPDATE for I/O metadata

```cpp
void my_write(const char *path, size_t size) {
  DFTRACER_CPP_FUNCTION();
  DFTRACER_CPP_FUNCTION_UPDATE("path", path);   // string params only
  ...
}
```

- Use `DFTRACER_CPP_FUNCTION_UPDATE("name", value)` for string (`const char *`) params.
- Good targets: `path`, `filename`, `name`, `dir`, `mode`.

### C++ Quick checklist

- [ ] `#include <dftracer/dftracer.h>` added to .cpp files only (never headers)
- [ ] Regular functions: `DFTRACER_CPP_FUNCTION()` as first statement after `{`
- [ ] main: `DFTRACER_CPP_INIT` → `DFTRACER_CPP_REGION_START` → ... → `DFTRACER_CPP_REGION_END` → `DFTRACER_CPP_FINI` → return
- [ ] REGION_END at every exit point in main (including early returns and exit() calls)
- [ ] No REGION macros in non-main functions
- [ ] No C macros (`DFTRACER_C_*`) in C++ files
