---
name: raylib-emscripten
description: Use when building games or interactive programs in C or C++ with raylib and shipping them to the browser via Emscripten (WebAssembly) as well as natively — building raylib for the web, the main-loop pattern, shell HTML, asset and data loading, input quirks, persistent saves, size budgets and browser smoke tests. Also use when a raylib game works natively but freezes, loses input or cannot save in the browser.
---

# raylib + Emscripten

Default: raylib built once for `PLATFORM_DESKTOP` and once for `PLATFORM_WEB`, the Emscripten SDK activated per shell, one Makefile with `run`, `test`, `bench`, `web` and `smoke` targets.

## Toolchain

1. Install the Emscripten SDK (`emsdk install latest && emsdk activate latest`), then `source emsdk_env.sh` in the shell that builds. Pin the version you tested in the README.
2. Build raylib for the web: `make -C raylib/src PLATFORM=PLATFORM_WEB` → `libraylib.web.a`.
3. Link the game:
   ```bash
   emcc src/*.cpp -O2 -Iraylib/src raylib/src/libraylib.web.a \
     -sUSE_GLFW=3 -sALLOW_MEMORY_GROWTH=1 -sFORCE_FILESYSTEM=1 \
     --shell-file web/shell.html -o build/index.html
   ```

## Main loop

```cpp
static void Frame() { Update(); BeginDrawing(); Draw(); EndDrawing(); }
int main() {
  InitWindow(960, 540, "game");
#if defined(PLATFORM_WEB)
  emscripten_set_main_loop(Frame, 0, 1);
#else
  SetTargetFPS(60);
  while (!WindowShouldClose()) Frame();
#endif
}
```

A native `while` loop on the web blocks the browser's event loop: nothing renders and the tab hangs.

## Data and saves

- Bundle small assets with `--preload-file assets` (or generate everything in code to keep the build small).
- Fetch runtime data (map tiles, levels) with `emscripten_fetch` or a JS helper; cache it (Cache API or IndexedDB) and fall back to generated content if the fetch fails.
- Saves: mount IDBFS at a directory, then `FS.syncfs(false, ...)` after writing; or write through JS to `localStorage`. Version the save format.

## Input

- Browsers deliver events between frames; a tap that presses and releases within one frame can be missed by polling. Record pointer down/up events in a queue (via a JS callback) and consume it each frame.
- Keyboard focus: the canvas must be focused; call `canvas.focus()` on click in the shell page.
- Audio starts only after a user gesture; start the audio device on the first click.

## Size and speed

- Report `.wasm` + `.js` + `.data` sizes per build; set a budget (e.g. a few MB) and fail when exceeded.
- `-O2` or `-Os`; avoid `-sASYNCIFY` unless you need blocking calls — it grows code and slows it down.
- Keep the simulation headless-testable natively (`make test`, `make bench`) — far faster than testing in a browser.

## Verification loop

1. Native: build with warnings as errors, `make test` and `make bench` with asserted thresholds.
2. Web: `make web`, serve `build/` over HTTP (not `file://`), and run a Playwright smoke test that waits for the first frame, presses keys and taps, checks for console errors and saves a screenshot.
3. Reload the page and confirm the save is restored.

## Pitfalls

- **`file://` does not work** — WASM must be served over HTTP with the right MIME type.
- **Memory growth** must be enabled for anything that loads data at runtime; the default heap is small.
- **Text:** the default font is ASCII; load a font with the code points you display.
- **High-DPI:** set `FLAG_WINDOW_HIGHDPI` or size the canvas yourself, or the game looks blurry.
- **Software rendering in CI** gives low, noisy fps; compare runs, do not gate on absolute numbers.
