---
name: snx-build
description: "Build the ScarletNX runtime and recompile games correctly, avoiding the setups that build \"successfully\" into something that doesn't work. Covers the CPM.cmake dependencies, the Clang-only presets, the deploy into games/, when a game needs recompiling, and the warnings a plain build doesn't show. Use when building, rebuilding, recompiling a game, after pulling or bumping a dependency, or when a build result looks suspicious."
---

# Build

## Order

1. `cmake --preset default -B build && cmake --build build`, into `build/` as the docs have it (without `-B` the
   preset builds into `build/default`). The configure fetches the
   third-party packages (`cmake/dependencies.cmake`) into `.cache/cpm` the first time, so a fresh clone needs the
   network once. They build in the same tree as the runtime: FFmpeg with its own configure and make run by
   `cmake/ffmpeg.cmake` (logs in
   `build/ffmpeg_build-prefix/src/ffmpeg_build-stamp/`), the others through their CMake.
   Clang only: any other compiler stops the configure. FFmpeg is required by the NX runtime. Configure also stops when
   the FFmpeg source path (the checkout, or `CPM_SOURCE_CACHE`) has a space in it, since FFmpeg's configure can't
   build from one, and on x86-64 when NASM is missing (below). On Windows, `scripts\bootstrap.ps1` downloads the
   toolchain (llvm-mingw, CMake, Ninja, NASM, Python, and w64devkit for the sh and GNU make FFmpeg needs) into
   `deps\tools` once, and `. scripts\env.ps1` puts it on PATH in a new PowerShell window. Windows' default execution
   policy runs no scripts, so run `Set-ExecutionPolicy -Scope Process Bypass` in that window first.
2. hactool is ours, in the tree (`src/nx/runtime/driver/hactool`, built by `cmake/hactool.cmake`), and runs inside
   `build/scarletnx -x Game.xci`.
3. The build's last step copies the runtime to `games/<id>/<name>` for every `games/<id>/<name>_code.so` (the game's
   and its update's, `<id>_<update id>`), and to
   `games/<Game>` for an older version's `games/<Game>_code.so` (`cmake/deploy.cmake`). That is the binary that runs.
   The build prints `Runtime deployed to ...` for each: no line means no game got the new runtime.

## Silent failures

| What happens | Why | What to do |
| --- | --- | --- |
| Movies stay black, the log says no H.264 decoder | A runtime built some other way than CMake (the recompiler once had its own build) drops the H.264 decoder without a word | Build the runtime with CMake (`build/scarletnx -r` also does), which includes FFmpeg. |
| The configure stops with "NASM was not found" | FFmpeg's x86-64 assembly needs NASM, and a build without it decodes movies several times slower, so it is never dropped silently | Install `nasm`. `-DSNX_FFMPEG_ASM=OFF` builds FFmpeg without its assembly on purpose (slower movies). |
| A fix has no effect | The game ran an old runtime: the build didn't deploy (no `_code.so` in `games/` yet), or the game was already running | Check the deploy lines. On Linux a running game keeps its old copy (the deploy renames over it). On Windows a running `.exe` can't be replaced, so stop the game before building. |
| Two build folders disagree on what is deployed | Every build folder with `SNX_DEPLOY` on deploys to the same `games/` | The last build wins. Configure extra folders with `-DSNX_DEPLOY=OFF`. The recompiler builds its runtime in `build/native-recomp` or `build/win64-recomp` with deployment off (`src/nx/runtime/driver/toolchain.c`). |
| A test binary next to the game was overwritten | The deploy targets every `*_code.so` in `games/`, symlinks included | Keep A/B copies outside `games/`, or don't build while they exist. |
| A new warning goes unnoticed | The runtime builds with Clang's default warnings only (the third-party packages and the generated game module build with `-w`), and a warning doesn't stop the build | Check a changed file with more warnings on: take the file's line from `build/compile_commands.json` and run it with `-Wall -Wextra -fsyntax-only`. Fix what comes from the change. |
| Game crashes at startup with "recompiled code is from another ScarletNX version" | The game module was built against another `SNX_ABI` (`src/common/cpu/aarch64/cpu.h`) | Recompile the game. |

## The Vulkan renderer

The renderer is Vulkan, and the sdl3 backend is the only window backend on Linux and Windows (the OpenGL renderer
and the x11, x11es, win32 and android backends were removed on 2026-10-11). A GPU or driver without Vulkan 1.3 stops
the runtime at startup with a message. SDL3 is always linked; `-H` skips SDL video initialization and renders offscreen
with Vulkan. The interface is the `Renderer` table in `gpu/renderer.h`, which `vk_renderer` fills in: everything else calls
`g_renderer->draw(...)` and so on.

The build also makes `snx-shaderc`. A translator change is checked on a shader corpus before rendering: record one
with `--shader_corpus=dir`, then run `build/snx-shaderc dir --validate` (`spirv-val` on PATH). Use `--out`
to save direct SPIR-V modules for disassembly or comparison between builds. A corpus is the game's own shaders: keep it
under `games/` or in the scratchpad, never in a tracked folder of the repo. `--vk_validation=1`
turns on the Khronos validation layer when it is installed (Arch: `vulkan-validation-layers`, which the user
installs). A screenshot (`--shot`) reads back the frame Vulkan presented, and its hash is in the
log: compare a change against the build before it at the same frame (a boot logo, `--seconds 4 --script
""`), on a quiet machine, since logos animate per frame. The first run after a rebuild that changes the
runtime (a new commit, or any change in a tree with edits: `pf_key`) starts the shader files over, so it translates
the game's own shaders again behind the loading screen (`prepare_shaders=2`) before `--seconds` starts counting, and
every shader its draws use again; a script's timed presses can miss. Run again with the files warm before suspecting
the renderer.

## Windows

CI (`.github/workflows/build.yml`) builds Windows natively from `scripts/bootstrap.ps1`, and cross-builds it on
Linux. To check Windows code before pushing, cross-build it here: with the Linux build of llvm-mingw on PATH (its
release `llvm-mingw-<date>-ucrt-ubuntu-22.04-x86_64.tar.xz`, which provides the `x86_64-w64-mingw32-*` names), run
`cmake --preset windows-cross && cmake --build --preset windows-cross`. Code that only Windows compiles
(`platform/plat_win32.c`, `platform/profiler_win32.c`, the `_WIN32` parts of the SDL3 backend) is checked only there:
a missing header, or a global that should be static, shows up only in that build.

The runtime builds with Clang's default warnings plus two errors: `-Werror=missing-prototypes` and
`-Werror=missing-variable-declarations`. A function or global another file uses
goes in the header next to the file that defines it, which that file includes too, so the compiler checks the two
agree. Anything else is static. An `extern` inside a function, or a prototype copied into another `.c` file, is the
pattern this replaced: there were once 237 of them, and some disagreed with the definition.

The Windows runtime is the SDL3 backend with the Vulkan renderer, as on Linux: `cmake --preset windows-cross &&
cmake --build --preset windows-cross` (SDL3 is then a CPM package, linked statically).

To run a Windows build, use Wine with a game module built for Windows, kept out of `games/`:
- The module comes from a Windows `scarletnx.exe -r`, with `--outdir build/wingame`: the recompiler builds modules
  for the host it runs on only, and the Linux one refuses `--target win64` (`src/nx/runtime/driver/recompile.c`).
  Make `build/wingame/<id>/<id>_data/romfs` a symlink to the Linux copy first, or it copies 13 GB.
- Use a prefix of its own, made without the Mono and Gecko installers, which otherwise wait for a click with nothing
  on screen: `WINEPREFIX=$PWD/build/wineprefix WINEDLLOVERRIDES="mscoree,mshtml=" WINEDEBUG=-all wineboot -i`, and
  the same variables for `wine <id>.exe --seconds=20 --shot=shot` in `build/wingame/<id>/`. The log is `<id>.log` next to it.
- What works under Wine 11.19 here: the SDL3 backend with Vulkan.

## When the game module must be recompiled

Only when generated code or its contract changes: `src/common/cpu/recompiler/`, `src/nx/loader/`, the module compile flags in
`src/nx/runtime/driver/toolchain.c`, `src/common/cpu/aarch64/cpu.h`, `cpu_helpers.c` and
the files under `src/common/cpu/aarch64/helpers/`. Other runtime changes normally need a runtime rebuild only. The runtime
only checks `SNX_ABI`: a module built before an ABI change that kept it still loads and runs the old code, and a
bump makes the runtime refuse every module built before it. A recompile of
a large game takes several minutes. A successful recompile removes its temporary objects. `--keep-ir` keeps the
generated code (LLVM IR) in `<outdir>/<id>/<id>_build/` for inspection.

```bash
build/scarletnx -r work/<Game>             # runtime and game module, both with Clang, into games/<id>/
```

`scarletnx -r` uses the LLVM backend, the only one. Its objects aren't
cached: each recompile builds every unit again. A change to the decoder's profile
(`src/common/cpu/aarch64/decode/a64.profile`) or to an emitter (`src/common/cpu/recompiler/llvm/ir_int.c`,
`ir_ldst.c`, `ir_fpu.c`, `ir_vec*.c`, ported from QEMU) is checked against `qemu-aarch64` by
`llvm_qemu_differential` (`ctest -R llvm_qemu_differential`; the binary's `--sweep` takes more words and states). A
difference not listed in `tests/llvm_qemu_expected.txt` fails it, and so does a listed one that is gone.

## Adding or bumping a third-party package

A `CPMAddPackage` in `cmake/dependencies.cmake` with the release archive's URL (a tag, or a commit for projects
without one) and its `URL_HASH SHA256=`. Get the hash from the release asset's digest (`gh api
repos/OWNER/REPO/releases/tags/TAG --jq '.assets[].digest'`) or by downloading the archive once, never by trusting
the next configure. Prefer `DOWNLOAD_ONLY` plus our own targets for projects without CMake (FFmpeg) or
with a CMake too old for CMake 4, `EXCLUDE_FROM_ALL YES` for the rest (not `SYSTEM`: a system copy of the headers
found through an `-I` in CFLAGS would win over `-isystem` ones; SDL3 on Windows is the one exception, since there is
no system copy to collide with), and `snx_quiet(target...)` on what it
builds. `OPTIONS` are cache variables of the whole build, not just that package. Then the license in docs/CREDITS.md's
table and in the install (below), and the version in the commit message. CI caches `.cache/cpm` on the file's hash.

## The AppImage

CI's `appimage` job installs the build into `/usr` in pkgforge's Arch container and runs `scripts/make-appimage.sh`,
which bundles `scarletnx` with quick-sharun and checks that a copy named `Probe.AppImage` looks for
`Probe_code.so` next to itself. The `release` job replaces the `nightly` prerelease with it on every push to `main`
that passed every other job. Locally, quick-sharun works from the host's libraries (it wants patchelf on PATH) and
bundles the full Mesa, so the AppImage comes out several times bigger than CI's, which uses pkgforge's debloated
packages. Inside an AppImage argv[0] points into its mount: anything that finds files next to the runtime goes
through `g_exedir`, which `main.c` takes from `$APPIMAGE`.

`cmake --install` puts the license files in `share/licenses/scarletnx`: `LICENSE`, then a folder per library or
ported code built into the runtime or the driver (those with no license file of their own, like DejaVu Sans and
Ryujinx's default Miis, from `dist/licenses/`). The AppImage copies that folder and adds the licenses of
the Arch packages it bundles, with their list in `share/licenses/bundled-packages.txt`, and the CI artifacts are the
install tree. A new package means a new `install(...)` line for its license in `CMakeLists.txt`.

## Never delegate builds to subagents

Reviewer and investigator agents read and grep. The main session builds and runs, once, serially: concurrent builds
fight over `build/` and the deploy, and a build during a test run changes its timing.
