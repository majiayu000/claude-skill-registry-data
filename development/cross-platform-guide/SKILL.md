---
name: cross-platform-guide
description: "Use when making native C/C++ software portable across operating systems and targets: isolating all OS/windowing/input/audio calls behind one platform-abstraction interface, ordering a port to a new OS, building to the web via Emscripten/WebAssembly (cooperative main loop, async file/network, GL ES/WebGPU mapping, 32-bit pointers, memory growth), and reading input devices like gamepads. Triggers on scattered platform #ifdefs, function-pointer OS interfaces, porting to Linux/web, emscripten_set_main_loop, ALLOW_MEMORY_GROWTH, WebGL from a Vulkan engine, /dev/input, evdev, gamepad hotplug, even when the user doesn't say 'portable'."
---

# Cross-platform / portability Guidelines

How to make native C/C++ software portable across operating systems and targets by concentrating every OS dependency behind a thin abstraction, porting one backend at a time, and reaching new targets including the web and new input hardware. The renderer architecture itself lives in gpu-rendering-guide (and gpu-rendering-vulkan-guide for one API); build-system mechanics live in cmake-guide; the C dialect's per-platform file-naming in c99-opinionated-guide.

## Requirements

- A codebase where OS access can be (or already is) funneled through interfaces, not called inline throughout app/engine code.
- A build system that can select one backend translation unit per target and define per-platform macros.

## Essentials

- **One interface for all OS calls** - A function-pointer struct (or build-selected header) per concern; callers never `#ifdef` or call an OS API directly, see [references/platform-abstraction-layer.md](references/platform-abstraction-layer.md)
- **Stub, then fill, in interactivity order** - Window → input → OS services → audio; the program links against stubs from hour one, see [references/porting-strategy.md](references/porting-strategy.md)
- **The web is a backend with hard constraints** - Cooperative main loop, async I/O, GL ES mapping, 32-bit pointers, see [references/web-wasm-builds.md](references/web-wasm-builds.md)
- **Devices are a backend too** - Enumerate, probe, poll non-blocking, map by code, behind the input-source interface, see [references/input-devices.md](references/input-devices.md)

## Abstraction and Porting

- **No scattered `#ifdef`** - Platform variance lives in backend translation units, not in portable logic, see [references/platform-abstraction-layer.md](references/platform-abstraction-layer.md)
- **Design the interface first** - Shape it before any backend so it doesn't bake in one platform's assumptions, see [references/platform-abstraction-layer.md](references/platform-abstraction-layer.md)
- **Toolchain differences are real bugs** - Stricter compilers, pointer width, struct padding; fix at the root, see [references/porting-strategy.md](references/porting-strategy.md)
- **CI per target** - A platform not in the build matrix regresses silently on the next portable-code edit, see [references/porting-strategy.md](references/porting-strategy.md)

## Web / WebAssembly

- **Yield the frame to the browser** - Replace the blocking native loop with a per-frame callback, see [references/web-wasm-builds.md](references/web-wasm-builds.md)
- **All I/O is async** - Preload assets into the virtual FS or fetch at runtime; no blocking file/network reads, see [references/web-wasm-builds.md](references/web-wasm-builds.md)
- **Renderer maps down to GL ES/WebGPU** - Route the 2D/UI stream through WebGL; defer or stream 3D, see [references/web-wasm-builds.md](references/web-wasm-builds.md)
- **32-bit, committed, growable memory** - Re-pad structs, enable memory growth, drop reserve-then-commit allocators, see [references/web-wasm-builds.md](references/web-wasm-builds.md)

## Input Devices

- **Enumerate from the device directory** - Read `/dev/input`, prefer stable `by-id`/`by-path` symlinks over `eventN`, see [references/input-devices.md](references/input-devices.md)
- **Probe before trusting** - Confirm capability bits (e.g. `BTN_GAMEPAD`) and read per-axis range/deadzone, see [references/input-devices.md](references/input-devices.md)
- **Poll non-blocking + hotplug** - `select`/`poll` then `read`; watch the directory for plug/unplug, see [references/input-devices.md](references/input-devices.md)
- **Map by code, not conditionals** - A table keyed on the OS code handles 1:1, 2:1, 1:2 mappings, see [references/input-devices.md](references/input-devices.md)

## Gotchas

- A backend that leaks a raw OS handle (file descriptor, window handle, connection) re-couples callers to one platform: keep the type opaque at the interface boundary.
- Reverse-engineering the abstraction from one platform bakes that platform's assumptions in (one global clipboard, OS-reported relative mouse motion); design the interface before the first backend.
- A stricter target compiler surfacing new warnings almost always means the warnings were always real: fix `void f()` → `void f(void)`, unused vars, and declaration mismatches rather than suppressing.
- 32-bit pointers (Wasm) silently change struct padding, breaking any hash/`memcmp` keyed on the byte layout; widen keys and re-pad for that build.
- A blocking `while (running)` loop hangs the browser tab; the browser owns the frame clock, so the frame must be a callback that returns each iteration.
- `fopen` that "works natively" returns nothing in the browser unless the file was preloaded into the virtual filesystem or fetched asynchronously first.
- A device node under `/dev/input` is not necessarily the device you want: a keyboard and a gamepad both appear there; verify capability bits before mapping.
- Raw `eventN` numbers and per-device axis ranges are not stable or symmetric; bind off the `by-id` symlink and normalize using the queried min/max and `flat` deadzone.

## Progressive Disclosure

- Read [references/platform-abstraction-layer.md](references/platform-abstraction-layer.md) - Load when designing or refactoring the OS-abstraction interface, removing scattered `#ifdef`s, or adding a per-platform backend
- Read [references/porting-strategy.md](references/porting-strategy.md) - Load when bringing the software up on a new OS: ordering the work, stubbing, handling compiler/toolchain and pointer-width differences, CI matrix
- Read [references/web-wasm-builds.md](references/web-wasm-builds.md) - Load when compiling to the web via Emscripten/WebAssembly: main loop, async I/O, GL ES/WebGPU mapping, memory growth, build flags, static linking
- Read [references/input-devices.md](references/input-devices.md) - Load when enumerating/reading input devices (gamepads via evdev), handling hotplug, or mapping buttons/axes behind the input interface
