---
name: aiwf-c-coding
description: Use for C source, headers, libraries, build flags, ABI, memory safety, and ISO C compatibility work before editing or reviewing C code.
---

# AIWF C Coding

## Core Rule

Treat C as its own language and toolchain lane. Before patching, identify the actual compiler, configured C standard, build system, target OS/architecture, and ABI boundary. Do not apply C++ patterns or newer C features unless the project already opts into them.

## Workflow

1. Inspect the repo-native build surface: `CMakeLists.txt`, `meson.build`, `Makefile`, compiler wrappers, CI files, headers, exported symbols, and any `-std=` or `/std:` flags.
2. Confirm the target C level from configuration, not preference. If it is missing, keep code compatible with the surrounding file style and note the ambiguity.
3. Patch narrowly around ownership, lifetime, bounds, integer conversion, nullability, alignment, volatile/atomic usage, and error paths.
4. Keep public headers stable unless the task is explicitly an API or ABI change.
5. Validate with the repo's normal build and tests. If no native check exists, compile the touched translation unit or a small probe with the detected compiler and warnings enabled.

## C Guardrails

- Keep C and C++ linkage explicit at boundaries. Use `extern "C"` only inside C++ guards in headers intended for both languages.
- Do not introduce VLAs, anonymous structs/unions, designated initializers, `_Generic`, `_Static_assert`, or C23 features unless the configured standard supports them.
- Prefer explicit sizes and ownership comments at allocation boundaries. Do not hide allocation ownership behind ambiguous helper names.
- Check allocation, I/O, parsing, and conversion failures. Use `errno`, return codes, or project-local error types consistently.
- Watch for undefined behavior: signed overflow, invalid aliasing, out-of-bounds pointer arithmetic, use-after-free, uninitialized reads, format string mismatches, and lifetime of stack-backed buffers.
- Keep warning cleanliness. New code should survive the existing warning level; when practical, test with `-Wall -Wextra -Wpedantic` or the project equivalent.

## Validation Defaults

Prefer existing commands. Useful fallbacks:

```powershell
cmake --build <build-dir>
ctest --test-dir <build-dir> --output-on-failure
clang -std=c17 -Wall -Wextra -Wpedantic -c <file.c>
gcc -std=c17 -Wall -Wextra -Wpedantic -c <file.c>
```

Use sanitizers only when the project already supports them or the user asks; do not rewrite the build system just to add one.

## Primary Source Anchors

- ISO WG14 project status and C working drafts: https://www.open-std.org/jtc1/sc22/wg14/www/projects
- ISO WG14 document log: https://www.open-std.org/jtc1/sc22/wg14/www/wg14_document_log

When the answer depends on a current standard status or compiler support matrix, verify the current official source before finalizing.
