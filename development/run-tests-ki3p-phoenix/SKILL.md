---
name: run-tests
description: Compile and run the PhoenixSketch unit tests under code/test using CMake + Google Test. Use when the user asks to run, build, or check the unit tests / ctest / Google Test suite for the radio firmware.
---

# run-tests

Builds and runs the host-side unit tests in `code/test/` using CMake and `ctest`. The tests use mocked Arduino/hardware interfaces and run on the development machine — they do **not** touch the Teensy.

| Setting | Value |
| --- | --- |
| Source dir | `code/test/` |
| Build dir | `code/test/build/` |
| Test runner | `ctest` (Google Test discovered via CMake) |

## Steps

1. **Ensure the build directory exists.** If `code/test/build/` is missing, create it. If the user passed `clean`, remove it first and recreate.
   ```bash
   mkdir -p code/test/build
   ```

2. **Configure (if needed).** From `code/test/build/`, run cmake. CMake re-configures itself on subsequent runs as needed, so it's safe to run unconditionally:
   ```bash
   cmake ..
   ```

3. **Build.** From `code/test/build/`:
   ```bash
   make
   ```
   Builds can take a while on a clean tree; use a generous Bash timeout (e.g. 600000 ms). If the build fails, surface the first error and stop — do not run tests on a broken build.

4. **Run tests.** From `code/test/build/`:
   ```bash
   ctest --output-on-failure
   ```
   Add `-R <pattern>` if the user passed a filter arg, and `-V` if they passed `verbose`.

5. **Report.** Summarise in 1–2 lines: how many tests passed/failed, and the names of any failing tests. If a specific filter was used, mention what it matched.

## Args

- `clean` — wipe `code/test/build/` and reconfigure from scratch before building. Use when CMake state seems stale or the user explicitly asks for a clean build.
- `verbose` — pass `-V` to ctest so individual test output is shown even on success.
- *Any other arg* — treat as a ctest `-R` regex filter (e.g. `RFBoard` runs `ctest -R RFBoard --output-on-failure`). Multiple words can be combined into one regex with `|`.

`clean` and `verbose` may be combined with a filter arg.

## Notes

- Always run from `code/test/build/` once it exists — relative paths in `CMakeLists.txt` assume that.
- This skill is for host unit tests only. To build/flash the firmware itself, use the `flash-radio` skill instead.
- The CMake test build lives under `code/test/build/`; the firmware build artifacts (`code/build/`, `ArduinoOutput/`) are unrelated and should not be touched here.
