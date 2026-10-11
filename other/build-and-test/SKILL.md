---
name: build-and-test
description: Configure, build and test dynamic-neural-field-composer. Use whenever you need to compile the library, run the GoogleTest suite, verify a change builds, or reproduce a test failure.
---

# Build and test

## Where things are

All commands run from the **nested project root**, `dynamic-neural-field-composer/` inside
the repository - not the repository root.

`VCPKG_ROOT` must be set in the environment; the CMake presets read it. If it is unset, run
`scripts/setup.sh` (Linux/macOS) or `scripts/setup.bat` (Windows) once to install the
dependencies. **Neither script leaves `VCPKG_ROOT` set in the shell you ran it from** -
`setup.sh` only `export`s inside its own process, and `setup.bat` writes it via `setx`,
which only reaches shells opened afterward. Open a new shell before configuring, or set the
variable directly for the current session.

On Windows the presets use Ninja with MSVC, so `cl.exe` must be on `PATH`. Run from a shell
that has the MSVC environment loaded (a Developer Command Prompt, or after sourcing
`vcvars64.bat`). See Troubleshooting for which MSVC to load.

**On Windows, re-assert `VCPKG_ROOT` after loading the MSVC environment.** `vcvars64.bat`
overwrites `VCPKG_ROOT` to point at Visual Studio's bundled vcpkg, which does not have this
project's packages installed. The presets expand `$env{VCPKG_ROOT}` *after* that, so they
pick up the wrong toolchain. Snapshot the value before loading MSVC and set it back
afterwards - `scripts/build.bat` does exactly this, for exactly this reason.

On an already-configured tree the cached toolchain wins and the problem stays invisible; a
fresh configure is where it bites.

## Configure

The project ships `CMakePresets.json`. Use it - it resolves the generator, build directory
and vcpkg toolchain for you, so nothing needs a hardcoded path:

```bash
cmake --preset release      # or: debug
```

Presets are `release` and `debug`, both Ninja, writing to `build/release` and `build/debug`.
Confirm what is available with `cmake --list-presets`.

Configure once per checkout. Re-run if `CMakeLists.txt`, `CMakePresets.json`, or the vcpkg
toolchain/dependency set changed - CMake does not watch any of these on its own.

## Build

**Cap parallelism at 4.** Several agents may be building on the same machine at once;
unbounded `--parallel` oversubscribes every core and slows all of them down.

```bash
cmake --build --preset release --target dnf_composer_tests --parallel 4
```

Targets: `dnf_composer_tests`, `dnf_composer_lib`, `dynamic-neural-field-composer` (the GUI
app), `dnf_composer_benchmark`, `dnf_composer_deckbench`, `dnf_composer_profiler`,
`dnf_composer_kernelbench`.

A cold build takes several minutes - run it in the background rather than blocking on a
foreground timeout.

## Test

Run the GoogleTest binary directly. `CMakePresets.json` defines no test presets, so this is
the reliable path:

```bash
./build/release/tests/dnf_composer_tests          # .exe on Windows
./build/release/tests/dnf_composer_tests --gtest_filter="SuiteName.*"    # TDD inner loop
```

`ctest --test-dir build/release --output-on-failure` also works when the available `ctest`
is new enough - see Troubleshooting.

Golden-data tests regenerate with `DNF_UPDATE_GOLDEN=1`. Only do this when the change to
the reference values is intentional and you can explain why each one moved.

## Adding a test file

`tests/CMakeLists.txt` lists the core sources explicitly (`elements/`, `simulation/`,
`tools/`, `exceptions/`, `application/`). A new file there that isn't added to the list is
silently never compiled, and the suite will go green without ever having run it. Add it,
then reconfigure before building.

`golden/`, `user_interface/` and `visualization/` are auto-discovered via
`file(GLOB ... CONFIGURE_DEPENDS ...)` - a new file there just needs a reconfigure, no list
edit.

## Working in an existing build tree

`scripts/build.bat`, `build.sh` and `build_macos.sh` create *different* trees from the
presets - `build/x64-release`, `build/linux-release`, `build/macos-release`. Prefer the
presets. If you must use an existing tree, pick whichever directory under `build/` actually
has a `CMakeCache.txt`, and read that cache for its generator and compiler.

## Troubleshooting

**Every translation unit fails with `STL1001: Unexpected compiler version`.**
The MSVC environment you loaded does not match the compiler the build tree was configured
with, so one toolchain's STL headers are being fed to another's compiler. The rule: **the
vcvars you source must match `CMAKE_CXX_COMPILER` in that tree's `CMakeCache.txt`.** Check
it:

```bash
grep "^CMAKE_CXX_COMPILER:" build/release/CMakeCache.txt
```

Beware `vswhere -latest` when more than one Visual Studio is installed - it can select a
newer one than the tree was configured with. `scripts/build.bat` uses `vswhere -latest` and
carries this latent bug; it survives only because it configures from scratch, so CMake and
vcvars end up agreeing.

**`ctest` fails demanding a newer CMake** (`CMake 3.30 or higher is required`).
The `ctest` on `PATH` is older than the CMake that generated the build tree - common when
an IDE with a bundled CMake configured it. **ctest must be at least the generator's CMake
version.** Either invoke the matching ctest, or just run the gtest binary directly.

## Reporting results

Report what actually happened, with real output:

- Green: say so plainly, with the test count.
- Red: paste the failing assertion and the test name. Do not summarise a failure as "some
  tests failed" - the actual message is the useful part.
- **Check the build's own exit code, not a pipeline's.** Piping cmake into `tail` or
  `Select-Object` returns the *pipe's* status, so a failed build reports success. Capture
  the exit code directly, or scan the output for `FAILED:`.
- Do not claim verification you did not perform. If you only built and did not run the
  suite, say that.
