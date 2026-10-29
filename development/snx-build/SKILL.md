---
name: snx-build
description: "Build the ScarletNX runtime and recompile games correctly. Avoid the setups that build \"successfully\" into something that does not work. It covers the CPM.cmake dependencies, the presets for Clang only and the deploy into games/. It also tells when a game needs a recompile, and which warnings a plain build does not show. Use it when you build or rebuild the runtime, or recompile a game. Use it also after you pull or bump a dependency, or when a build result looks suspicious."
---

# Build

## Order

1. Run `cmake --preset default -B build && cmake --build build`. It builds into `build/`, as the docs show. Without
   `-B`, the preset builds into `build/default`. The first time, the configure fetches the third-party packages
   (`cmake/dependencies.cmake`) into `.cache/cpm`. Thus a fresh clone needs the network one time.

   The packages build in the same tree as the runtime. FFmpeg builds with its own configure and make, which
   `cmake/ffmpeg.cmake` runs. Its logs are in `build/ffmpeg_build-prefix/src/ffmpeg_build-stamp/`. The other packages
   build through their CMake.

   Use Clang only: any other compiler stops the configure. The NX runtime requires FFmpeg. The configure also stops
   in two other conditions:
   - The FFmpeg source path (the checkout, or `CPM_SOURCE_CACHE`) has a space in it. FFmpeg's configure cannot build
     from such a path.
   - The host is x86-64 and it has no NASM (see below).

   On Windows, `scripts\bootstrap.ps1` downloads the toolchain into `deps\tools` one time. The toolchain is
   llvm-mingw, CMake, Ninja, NASM, Python, and w64devkit for the sh and GNU make that FFmpeg needs. The default
   execution policy of Windows runs no scripts. Thus, in a new PowerShell window, run
   `Set-ExecutionPolicy -Scope Process Bypass` first. Then `. scripts\env.ps1` puts the toolchain on PATH in that
   window.
2. hactool is our own code, in the tree (`src/nx/runtime/driver/hactool`). `cmake/hactool.cmake` builds it. It runs
   inside `build/scarletnx -x Game.xci`.
3. The last step of the build copies the runtime to `games/<id>/<name>` for each `games/<id>/<name>_code.so`. These
   are the module of the game and the module of its update (`<id>_<update id>`). For an older version's
   `games/<Game>_code.so`, the step copies the runtime to `games/<Game>` (`cmake/deploy.cmake`). That copy is the
   binary that runs. The build prints `Runtime deployed to ...` for each copy. If there is no such line, no game got
   the new runtime.

## Silent failures

| What happens | Why | What to do |
| --- | --- | --- |
| Movies stay black. The log says that there is no H.264 decoder. | When a build other than CMake makes the runtime, the runtime drops the H.264 decoder with no message. The recompiler had its own build at one time. | Build the runtime with CMake, which includes FFmpeg. `build/scarletnx -r` also uses CMake. |
| The configure stops with `NASM was not found` | The x86-64 assembly of FFmpeg needs NASM. A build without it decodes movies several times slower. Thus the build never drops the assembly silently. | Install `nasm`. `-DSNX_FFMPEG_ASM=OFF` builds FFmpeg without its assembly on purpose (slower movies). |
| A fix has no effect | The game ran an old runtime. The build did not deploy (there was no `_code.so` in `games/` yet), or the game ran during the build. | Check the deploy lines. On Linux, a game that runs keeps its old copy (the deploy renames the new file over it). On Windows, the deploy cannot replace a `.exe` that runs. Thus stop the game before you build. |
| Two build folders do not agree on the deployed runtime | Every build folder with `SNX_DEPLOY` on deploys to the same `games/` | The last build wins. Configure extra folders with `-DSNX_DEPLOY=OFF`. The recompiler builds its runtime in `build/native-recomp` or `build/win64-recomp` with deployment off (`src/nx/runtime/driver/toolchain.c`). |
| The deploy wrote over a test binary next to the game | The deploy targets every `*_code.so` in `games/`, and symlinks too | Keep A/B copies outside `games/`, or do not build while they exist. |
| Nobody sees a new warning | The runtime builds with only the default warnings of Clang. The third-party packages and the generated game module build with `-w`. A warning does not stop the build. | Check a changed file with more warnings on. Take the line of the file from `build/compile_commands.json`. Run it with `-Wall -Wextra -fsyntax-only`. Fix the warnings that come from the change. |
| The game crashes at startup with `recompiled code is from another ScarletNX version` | The build of the game module used another `SNX_ABI` (`src/common/cpu/aarch64/cpu.h`) | Recompile the game. |

## The Vulkan renderer

The renderer is Vulkan. The sdl3 backend is the only window backend on Linux and Windows. The project removed the
OpenGL renderer and the x11, x11es, win32 and android backends on 2026-10-11. A GPU or driver without Vulkan 1.3
stops the runtime at startup with a message.

The runtime always links SDL3. `-H` skips the SDL video initialization and renders offscreen with Vulkan. The
interface is the `Renderer` table in `gpu/renderer.h`, which `vk_renderer` fills in. All other code calls
`g_renderer->draw(...)` and the other functions of the table.

The build also makes `snx-shaderc`. Check a translator change on a shader corpus before you render with it. Record a
corpus with `--shader_corpus=dir`. Then run `build/snx-shaderc dir --validate` (`spirv-val` must be on PATH). Use
`--out` to save direct SPIR-V modules for disassembly or for a comparison between builds.

A corpus holds the shaders of the game. Keep it under `games/` or in the scratchpad, never in a tracked folder of the
repo. `--vk_validation=1` turns on the Khronos validation layer if the layer is on the machine. On Arch, the user
installs it from `vulkan-validation-layers`.

A screenshot (`--shot`) reads back the frame that Vulkan presented. The log gives the hash of the screenshot. Compare
a change against the build before it at the same frame, on a quiet machine. A boot logo is a good frame
(`--seconds 4 --script ""`). Use the same frame because logos animate per frame.

A rebuild can change the runtime: a new commit, or any change in a tree with edits (`pf_key`). The first run after
such a rebuild starts the shader files again from zero. Thus the run translates the game's own shaders again behind
the load screen (`prepare_shaders=2`), before `--seconds` starts to count. It also translates again every shader that
its draws use. Thus the timed presses of a script can miss. Before you suspect the renderer, run again with warm
files.

## Windows

CI (`.github/workflows/build.yml`) builds Windows natively from `scripts/bootstrap.ps1`, and cross-builds it on
Linux. Before you push Windows code, cross-build it here to check it. Put the Linux build of llvm-mingw on PATH. Its
release is `llvm-mingw-<date>-ucrt-ubuntu-22.04-x86_64.tar.xz`, which gives the `x86_64-w64-mingw32-*` names. Then
run `cmake --preset windows-cross && cmake --build --preset windows-cross`.

Only that build checks the code that only Windows compiles: `platform/plat_win32.c`, `platform/profiler_win32.c` and
the `_WIN32` parts of the SDL3 backend. A header that a file needs but does not include, or a global that must be
static, shows only in that build.

The runtime builds with the default warnings of Clang and two errors: `-Werror=missing-prototypes` and
`-Werror=missing-variable-declarations`. When another file uses a function or a global, declare it in the header next
to the file that defines it. That file also includes the header, so the compiler checks that the two agree. All other
functions and globals are static. This rule replaced an older pattern: an `extern` inside a function, or a prototype
copied into another `.c` file. At one time there were 237 of them, and some did not agree with the definition.

The Windows runtime is the SDL3 backend with the Vulkan renderer, as on Linux. Build it with
`cmake --preset windows-cross && cmake --build --preset windows-cross`. In that build, SDL3 is a CPM package, and the
build links it statically.

To run a Windows build, use Wine with a game module for Windows. Keep that module out of `games/`:
- First, make `build/wingame/<id>/<id>_data/romfs` a symlink to the Linux copy. If you do not, the recompiler copies
  13 GB. Then make the module with a Windows `scarletnx.exe -r`, with `--outdir build/wingame`. The recompiler builds
  modules only for the host that it runs on. The Linux recompiler refuses `--target win64`
  (`src/nx/runtime/driver/recompile.c`).
- The Mono and Gecko installers wait for a click and show nothing on screen. Thus use a prefix of its own, without
  these installers. Make the prefix with
  `WINEPREFIX=$PWD/build/wineprefix WINEDLLOVERRIDES="mscoree,mshtml=" WINEDEBUG=-all wineboot -i`. Use the same
  variables for `wine <id>.exe --seconds=20 --shot=shot` in `build/wingame/<id>/`. The log is `<id>.log` next to it.
- Under Wine 11.19 on this machine, the SDL3 backend with Vulkan works.

## When you must recompile the game module

Recompile it only when the generated code or its contract changes. The code and the contract are in
`src/common/cpu/recompiler/`, `src/nx/loader/`, the module compile flags in `src/nx/runtime/driver/toolchain.c`,
`src/common/cpu/aarch64/cpu.h`, `cpu_helpers.c` and the files under `src/common/cpu/aarch64/helpers/`. Other runtime
changes usually need only a runtime rebuild. The runtime checks only `SNX_ABI`. Thus, after an ABI change that kept
`SNX_ABI`, an older module still loads and runs the old code. A bump of `SNX_ABI` makes the runtime refuse every
module from before the bump.

A recompile of a large game takes several minutes. A successful recompile removes its temporary objects. `--keep-ir`
keeps the generated code (LLVM IR) in `<outdir>/<id>/<id>_build/` for inspection.

```bash
build/scarletnx -r work/<Game>             # runtime and game module, both with Clang, into games/<id>/
```

`scarletnx -r` uses the LLVM backend, which is the only backend. The backend does not keep its objects in a cache.
Each recompile builds every unit again.

`llvm_qemu_differential` checks against `qemu-aarch64` a change to the profile of the decoder
(`src/common/cpu/aarch64/decode/a64.profile`) or to an emitter. The emitters are
`src/common/cpu/recompiler/llvm/ir_int.c`, `ir_ldst.c`, `ir_fpu.c` and `ir_vec*.c`, which the project ported from
QEMU. Run it with `ctest -R llvm_qemu_differential`. The `--sweep` option of the binary takes more words and states.
A difference that is not in `tests/llvm_qemu_expected.txt` makes the test fail. A listed difference that no longer
occurs also makes it fail.

## To add or bump a third-party package

Add a `CPMAddPackage` to `cmake/dependencies.cmake` with the URL of the release archive and its `URL_HASH SHA256=`.
The URL names a tag, or a commit for projects without tags. Get the hash from the digest of the release asset
(`gh api repos/OWNER/REPO/releases/tags/TAG --jq '.assets[].digest'`), or download the archive one time. Never trust
the next configure for the hash. Then:
- For projects without CMake (FFmpeg) or with a CMake too old for CMake 4, prefer `DOWNLOAD_ONLY` and our own
  targets.
- For the other projects, prefer `EXCLUDE_FROM_ALL YES`. Do not use `SYSTEM`. A system copy of the headers that an
  `-I` in CFLAGS finds would win over the `-isystem` headers. SDL3 on Windows is the one exception, because there is
  no system copy for it to collide with.
- Put `snx_quiet(target...)` on the targets that the package builds.

`OPTIONS` are cache variables of the whole build, not only of that package. Then add the license to the table in
docs/CREDITS.md and to the install (see below). Give the version in the commit message. CI caches `.cache/cpm` on the
hash of the file.

## The AppImage

The `appimage` job of CI installs the build into `/usr` in the Arch container of pkgforge. Then it runs
`scripts/make-appimage.sh`. This script bundles `scarletnx` with quick-sharun. It also checks that a copy with the
name `Probe.AppImage` looks for `Probe_code.so` next to itself. The `release` job replaces the `nightly` prerelease
with it on every push to `main` that passed every other job.

On this machine, quick-sharun works from the libraries of the host and needs patchelf on PATH. It bundles the full
Mesa. Thus the local AppImage is several times bigger than the AppImage of CI, which uses the debloated packages of
pkgforge. Inside an AppImage, argv[0] points into its mount. Thus code that finds files next to the runtime must use
`g_exedir`, which `main.c` takes from `$APPIMAGE`.

`cmake --install` puts the license files in `share/licenses/scarletnx`. First is `LICENSE`. Then there is a folder
for each library or ported code in the runtime or the driver. The license files for code without its own license file
come from `dist/licenses/`, for example Noto Sans and the default Miis of Ryujinx.

The AppImage copies that folder and adds the licenses of the Arch packages that it bundles. Their list is in
`share/licenses/bundled-packages.txt`. The CI artifacts are the install tree. A new package needs a new
`install(...)` line for its license in `CMakeLists.txt`.

## Never delegate builds to subagents

Reviewer and investigator agents read and grep. Only the main session builds and runs, one job at a time. Two builds
at the same time fight over `build/` and the deploy. A build during a test run changes how fast the test runs.
