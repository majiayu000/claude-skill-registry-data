---
name: implementing-firmware
description: Implements ESP-IDF or PlatformIO firmware with mandatory requirement docstring tags and MISRA-C linting. Use when writing embedded C code, implementing firmware features, or adding requirement-traced functions.
compatibility: Designed for Claude Code
metadata:
  allowed-tools: Read, Write, Edit, Glob, Grep, Bash
  argument-hint: [feature-or-requirement]
  stability: stable
  content-hash: sha256:0a0457594dd459c1070c0ea7581055ccd87cfd2999b728cace6c0ab35d44cb86
  last-verified-cc-version: 1.0.34
---

# Firmware Implementation

**Target**: $ARGUMENTS

Implement firmware code with mandatory requirement traceability tags, following ESP-IDF or PlatformIO patterns.

## References (MUST READ)

Read these before proceeding:

- `references/esp-idf-patterns.md` — Component structure, FreeRTOS, sdkconfig, idf.py
- `references/platformio-patterns.md` — platformio.ini, pio commands, library management
- `references/c-safety-rules.md` — MISRA-C cppcheck flags, clang-tidy, tagging rules

## Workflow

1. **Detect framework:**
   - `CMakeLists.txt` + `sdkconfig*` → ESP-IDF
   - `platformio.ini` → PlatformIO
   - Neither → ask user which framework to use
2. **Read existing requirements** — Check for `docs/requirements.md` to understand which SW-REQs need implementing
3. **Implement code** with mandatory docstrings on every new function:

   ```c
   /**
    * @brief <What this function does>
    *
    * @requirement SW-REQ-NNN
    * @parent      PRD-REQ-NNN
    * @test        TEST-NNN
    *
    * @param ...
    * @return ...
    */
   ```

4. **Create test stubs** in `test/` with matching `@test TEST-NNN` references
5. **Lint with cppcheck:**

   ```bash
   cppcheck --addon=misra.py --std=c11 --enable=all --xml src/ 2> misra-report.xml
   ```

6. **Build:**
   - ESP-IDF: `idf.py build`
   - PlatformIO: `pio run`
7. **Report** — Count tagged functions, list any warnings

## Rules

- Every new function **must** have `@requirement`, `@parent`, and `@test` tags
- Follow existing code style (indentation, naming conventions) in the project
- Use ESP-IDF error handling patterns (`ESP_ERROR_CHECK`, `esp_err_t` returns)
- Do not suppress MISRA warnings without documenting the deviation
- Create header declarations alongside implementations
- Test stubs must compile even if test logic is not yet implemented
