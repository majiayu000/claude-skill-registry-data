---
name: cpp
description: Use when writing C++ (C++17 or later) for games, simulations or tools — native and WebAssembly builds with raylib and Emscripten, CMake or Make, deterministic simulation with headless tests and benchmarks, runtime data fetching, and keeping WASM size and start-up fast. Also use when a native build works but the browser build misbehaves (missed input, blocking loops, file access, memory growth).
---

# C++

Default: C++17, warnings high (`-Wall -Wextra -Wpedantic`), one `Makefile` or `CMakeLists.txt` that builds native, test and web targets, no exceptions across the main loop.

## Layout

```text
src/        game or app code; sim/ is pure logic, draw/ talks to the renderer
tests/      plain executables returning non-zero on failure (or a light framework)
web/        shell HTML for the Emscripten build
Makefile    targets: run, test, bench, web, smoke
```

Keep the simulation free of renderer calls so `make test` and `make bench` run headless on any machine.

## Native and web from one codebase

- Write the frame as a function (`void frame()`) and drive it with `while (!WindowShouldClose()) frame();` natively and `emscripten_set_main_loop(frame, 0, 1)` on the web. A blocking `while` loop freezes the browser tab.
- Build web with `emcc ... -sUSE_GLFW=3 -sALLOW_MEMORY_GROWTH=1 -O2` (plus `-sASYNCIFY` only if you really need to block; it costs size and speed).
- Fetch runtime data (tiles, levels) with `emscripten_fetch` or JS interop, cache it, and fall back to generated content when the network fails. Show attribution for open data on screen when its licence requires it.
- Report WASM size per build and set a budget; strip unused code with `-O2`/`-Os` and `--closure 1` for the JS glue when size matters.

## Determinism and measurement

- Use one seeded RNG (`std::mt19937` or a small xorshift) owned by the simulation; never `rand()`.
- Use fixed time steps for simulation; render with interpolation if needed.
- `make bench`: run many seeds headlessly and print the measured outcomes (time to first event, success rate, worst case). Assert thresholds in `make test` so regressions fail loudly.
- Measure real frame time over a window; headless browsers use software GL, so their fps is only a relative signal.

## Verification loop

1. Native build with zero warnings.
2. `make test` (unit + threshold checks), `make bench` for numbers.
3. `make web` then a browser smoke test that checks the console for errors and takes a screenshot.

## Pitfalls

- **Fast taps on the web:** a press and release inside one frame can be missed if you poll `IsMouseButtonPressed`. Queue pointer events from JS (or the platform callback) and consume the queue each frame.
- **Filesystem on the web** is in-memory unless you mount persistent storage; saves need IndexedDB (IDBFS) or `localStorage` via JS and an explicit sync.
- **Undefined behaviour** (signed overflow, out-of-range indexing) often "works" natively and breaks under `-O2` or on WASM. Build tests with `-fsanitize=address,undefined` natively.
- **Static initialisation order** across translation units is unspecified; prefer function-local statics.
- **Text:** raylib's default font is ASCII; load a font with the code points you actually display, and keep UTF-8 throughout.
- **Large generated meshes** should be split into chunks so off-screen parts can be culled; one huge mesh is drawn (and shadowed) every frame.
- **Writing your own decoder** (e.g. vector tiles) is fine for small formats, but test it against fixtures from the reference implementation.
