---
name: intentumdiff-build
description: >-
  How to build every layer of the IntentumDiff repo from source — the Rust core (PyO3 extension),
  the per-language Wasm parser components, the VS Code extension, and the dbt plugin — plus the
  toolchain pins and the gotchas that silently waste hours. Use this whenever you need to build,
  rebuild, compile, or package any part of the project, when a change requires a rebuild before
  it takes effect, when you hit "Access is denied (os error 5)" / a stale `.pyd`, or when
  something runs suspiciously slowly (debug vs release core). It answers "what do I run, in what
  directory, and do I even need to rebuild for this change?". Read intentumdiff-architecture for
  the layer boundaries; use intentumdiff-testing to run the suites after building.
---

# IntentumDiff — Building from source

Four independently-built layers. **Only rebuild what you changed** — knowing which layer you
touched avoids both stale binaries and pointless rebuilds.

| You changed… | Build step | Rebuild needed? |
|---|---|---|
| `crates/rust-core-host/` (the engine) | `maturin develop --release` (from **repo root**) | **Yes** — the cdylib is stale until you do |
| `crates/<lang>-parser/` (a Wasm parser) | `python build.py` (or per-crate cargo → wasm) | Yes, to refresh `src/intentumdiff/wasm/*.wasm` |
| `plugins/vscode/src/` (extension) | `npm run compile` (`tsc -p ./`) | Yes (compiles TS → `out/`); no maturin |
| `src/intentumdiff/**.py` (Python shell) | none | No — pure Python runs as-is |

## HARD RULE: if you changed a compiled layer, rebuild BEFORE you test or trust any output

Python silently loads the OLD cdylib / OLD `*.wasm` — a test run or a diff you eyeball
against a stale binary is a **false pass/fail**, and this has repeatedly wasted hours in this
repo. So:

- **Touched `crates/rust-core-host/`?** `maturin develop --release` (from the **repo root**, not
  the crate dir) BEFORE running any pytest, any `diff_strings`, or any manual check. The cdylib is
  stale until you do.
- **Touched any `crates/<lang>-parser/` or `crates/sdk/`?** `python build.py` (or the single
  crate → copy to `src/intentumdiff/wasm/`) BEFORE testing. Note `crates/sdk` feeds MANY parsers,
  and `lto=true` means one crate change re-optimizes the whole binary — rebuild the full
  affected surface, not just the language you think you touched.
- **Verify the rebuild took by EXERCISING the changed behavior, not by reading timestamps.**
  Timestamps lie: a `#[cfg(test)]`-only edit does not bump runtime; the `.pyd` can be shadowed
  by a stale `intentumdiff_rust_core/` editable-install dir (see the shadowing section). The
  reliable check is to run a diff that hits the new code path and assert the new result (e.g.
  after adding an intent description, confirm `change.description` is the new wording). If it
  shows the old behavior, the binary is stale — do not proceed.
- **Corollary:** never conclude "the suite is green / the bug is fixed" from a run whose binary
  predates your `crates/` edit. Rebuild, then re-run.
- **The VS Code extension caches a long-running engine.** It spawns a persistent
  `intentumdiff` process (`plugins/vscode/src/processTransport.ts`) that does NOT hot-reload
  editable source or newly-built `*.wasm`. After ANY rebuild (or adding a parser), the
  extension keeps serving the OLD engine — e.g. still parsing `.gitignore` with the generic
  parser — until you **Reload Window** (or restart the IntentumDiff engine). If the CLI /
  Python API shows the fix but the extension does not, it is a stale extension process, not a
  code bug — reload before re-diagnosing.
- **Editable installs snapshot entry-point metadata at install time.** Adding a parser to
  `pyproject.toml [project.entry-points."intentumdiff.parsers"]` does NOT appear in the
  installed `.dist-info` until you re-install (`pip install -e .`, which triggers a full
  maturin build). In-process discovery still works because
  `_FIRST_PARTY_PARSER_ENTRYPOINT_FALLBACKS` (registry.py) re-adds built-ins from the source
  tree — so a new parser routes correctly WITHOUT the reinstall, but `importlib.metadata`
  will under-report it. Add every new parser to that fallback map, not just pyproject.

## Do I actually need to rebuild? (decision rule)

Before running maturin, confirm a rebuild is warranted — recompiling unchanged Rust is a
multi-minute no-op:
- **Did any `crates/` source change?** `git status --short crates/` — if empty, no rebuild.
- **Is the installed core already current?** Compare timestamps: the installed
  `src/intentumdiff/intentumdiff_rust_core.pyd` should be **newer** than the newest
  `crates/rust-core-host/src/*.rs`. If it is, and nothing changed, it's up to date.
- **A pure-Python fix in `src/intentumdiff/analysis/` is oracle-only.** Those modules are the
  parity test-oracle; the authoritative behavior is in the Rust core, which may **already be
  correct** (e.g. the `suppress_low_signal_reorders` group emits `raw_change_indices: []` in
  both `refinement.py` and `lib.rs`). So a Python analysis fix often needs **neither** a Rust
  change **nor** a rebuild — verify against `crates/rust-core-host/src/lib.rs` before assuming.
  Only when you edit `crates/` does the rebuild rule below apply.

## Rust core (`crates/rust-core-host` → `intentumdiff_rust_core` C-ABI cdylib)

The crate is **pyo3-free** (#B.6): it builds a bare cdylib exposing the C ABI (`intentumdiff_call`),
which `rust_core.py` ctypes-loads. maturin is driven by the **repo-root `pyproject.toml`**
(`bindings = "cffi"`), so run it from the **repo root** — `cd crates/rust-core-host && maturin …`
now **errors** (no pyproject there).

```bash
rustup toolchain install 1.95.0          # first time only
python -m pip install maturin            # first time only
RUSTUP_TOOLCHAIN=1.95.0 maturin develop --release    # from the REPO ROOT
```
This compiles the core and installs the cdylib as
`.venv/Lib/site-packages/intentumdiff/intentumdiff_rust_core/intentumdiff_rust_core.<ext>`
(`.dll` on Windows, `.so` Linux, `.dylib` macOS) — **not** a top-level `.pyd`.

**Traps that waste hours:**
- **Always `--release`.** Plain `maturin develop` builds a *debug* core — functionally
  identical but ~20–50× slower on compute paths (the perceptual image diff goes ~6 s → ~0.3 s
  on a 1050×700 image). Use plain `maturin develop` only when iterating on Rust and compile
  speed matters more than runtime.
- **Windows cdylib lock:** the extension/CLI keeps the core `.dll` loaded, so the install step
  fails with `Access is denied (os error 5)` if a process holds it. Stop it first:
  `Get-Process -Name intentumdiff -ErrorAction SilentlyContinue | Stop-Process -Force` (and
  reload the VS Code extension host).
- **OneDrive-locked `.pdb` breaks the install (this repo's `.venv` is under OneDrive).** A Windows
  release build still emits a large `intentumdiff_rust_core.pdb`; OneDrive grabs a lock while syncing
  it, so maturin's install rename can die with `Access is denied (os error 5)` **even with no
  `intentumdiff` process running** — after maturin has already *uninstalled* the old package, leaving
  a half-installed core (the loaded `.dll` is missing / mismatched, so the ctypes loader reports
  `function 'intentumdiff_call' not found`). ctypes loads only the `.dll`, never the `.pdb`, so
  sidestep it: build a `.pdb`-free wheel and force-install it:
  ```bash
  export VIRTUAL_ENV=<repo>/.venv && export PATH="$VIRTUAL_ENV/Scripts:$PATH"
  export CARGO_PROFILE_RELEASE_DEBUG=false        # no .pdb in the artifact
  RUSTUP_TOOLCHAIN=1.95.0 maturin build --release -b cffi --out /tmp/idwheel
  "$VIRTUAL_ENV/Scripts/python.exe" -m pip install --force-reinstall --no-deps /tmp/idwheel/*.whl
  ```
  Then `rm -f src/intentumdiff/*.pyd` (shadow check below) and verify with the backend probe below.
  (Real fix: move `.venv` out of OneDrive.)
- **`maturin develop` installs into the venv named by `$VIRTUAL_ENV`, not `.venv` by name.**
  From a non-activated shell (e.g. the Bash tool) `VIRTUAL_ENV` is unset and maturin *guesses* —
  it can pick a broken sibling like `.venv2` and die with `Need a Python interpreter to compile`
  / `could not determine version from interpreter name`. `develop` has **no** `--interpreter`
  flag (that's `build`), so the fix is to set the env explicitly, not pass a flag:
  `export VIRTUAL_ENV=<repo>/.venv && export PATH="$VIRTUAL_ENV/Scripts:$PATH"` before `maturin
  develop`. Confirm it installed into `.venv`, not the guessed one.
- **Stale-shadow check (the loader-order trap, issue #28 — inverted since #B.6):** the pyo3 era's
  fix was to *copy* a `.pyd` into `src/intentumdiff/`; post-#B.6 that same file is now the **bug**.
  `_load_backend()` uses `find_spec` to detect a pyo3 *extension* (origin ending in an extension
  suffix) and prefers it over the ctypes path — so a leftover `src/intentumdiff/intentumdiff_rust_core.pyd`
  from the old era (or a `pip install`ed standalone `intentumdiff_rust_core`) **silently shadows the
  fresh cdylib** and you test yesterday's engine. Remedy after every core build:
  ```bash
  rm -f src/intentumdiff/*.pyd
  .venv/Scripts/python.exe -m pip uninstall -y intentumdiff_rust_core 2>$null
  ```
  Verify which backend the DIFFER loads (not a bare import, which can lie):
  `python -c "import intentumdiff.rust_core as r; print(type(r._load_backend()).__name__)"` must print
  `_CtypesBackend`.
- **Release build OOM on Windows (issue #29):** `maturin develop --release` can crash rustc
  1.95.0 (`handle_alloc_error` / `STATUS_STACK_BUFFER_OVERRUN`) — the ~12k-line `lib.rs` at
  opt-level=3 + codegen-units=1 is one giant codegen unit. A **debug** build (`maturin develop`)
  is valid for correctness verification; only perf-sensitive work needs release. Lower-memory
  local override: `CARGO_PROFILE_RELEASE_CODEGEN_UNITS=16 maturin develop --release`.
- **Toolchain pin:** Rust **1.95.0** (the RC native-wheel dry run is pinned to it; local
  Windows release packaging has hit a `rustc 1.95.0` metadata ICE on optimized wheel builds).
- **No Python engine fallback exists** (removed in #B.3/#90/#91): the Rust core is the only engine,
  so a build failure means a broken engine, not a silent degrade. Backend *selection* is the only
  override left: `INTENTUMDIFF_RUST_CORE_CTYPES=1` forces the pure-ctypes proxy (the default once pyo3
  is gone), `INTENTUMDIFF_RUST_CORE_PYO3=1` forces a pyo3 extension if one is still present.

Details: `docs/BUILDING.md`.

## Wasm parser components (`crates/<lang>-parser/` → `src/intentumdiff/wasm/<lang>_parser.wasm`)

Parsers are compiled to WebAssembly components (target `wasm32-wasip2`). The repo build hook
(`build.py`, a Hatch build hook, `build-backend = "maturin"` in `pyproject.toml`) drives
`cargo` → `.wasm` and stages the binaries into `src/intentumdiff/wasm/`. End users never build
these — published wheels ship the pre-built `.wasm` files. Build them locally only when working
on a grammar/parser crate:
```bash
python build.py                 # builds/refreshes the bundled .wasm parser set
```
For a single parser, build that crate for the wasm target and copy its artifact into
`src/intentumdiff/wasm/`. **Names differ at every step** (guessing them costs a cycle):
package = `intentumdiff-<lang>-parser`, artifact = `intentumdiff_<lang>_parser.wasm`, staged
name = `<lang>_parser.wasm` (whatever `plugins/builtins.py` references):
```bash
RUSTUP_TOOLCHAIN=1.95.0 cargo build --release --target wasm32-wasip2 -p intentumdiff-<lang>-parser
cp target/wasm32-wasip2/release/intentumdiff_<lang>_parser.wasm src/intentumdiff/wasm/<lang>_parser.wasm
```
Never pipe the cargo build through `tail`/`grep` inside a `&&` chain — the pipe's exit status
masks a failed build, the `cp` then re-stages the STALE wasm, and every downstream test
"passes" against yesterday's binary (this happened; check for `error` in full output).

**New tree-sitter grammar dep fails with `ToolNotFound: clang` on wasm32-wasip2** — that's
expected; grammar build scripts need a WASI C compiler. The repo pattern is a patch crate
`crates/patches/tree-sitter-<lang>/` with a zig-prebuilt static lib: vendor the registry
source, custom `Cargo.toml` (`autolib = false`, `tree-sitter-language` dep) + target-aware
`build.rs` (wasip2 → link `lib/libtree_sitter_<lang>.a`; native → `cc` compile), compile with
`zig cc --target=wasm32-wasi -O2 -fsanitize-trap=undefined -fvisibility=hidden` + `zig ar rcs`,
and register under `[patch.crates-io]` in the root `Cargo.toml`. Full recipe + zig commands:
`docs/WASM_BUILD_PATCHES.md`; ~10 existing examples under `crates/patches/`.

Dormant crates (e.g. FreeBASIC) stay disabled until their grammar meets
the shipped-example contract. See `docs/PLUGIN_GUIDE.md` / `docs/WASM_BUILD_PATCHES.md`.

## VS Code extension (`plugins/vscode`, TypeScript, no bundler)

```bash
cd plugins/vscode
npm install          # first time
npm run compile      # tsc -p ./  → out/     (npm run watch for incremental)
npm run lint         # tsc -p ./ --noEmit  (type-check only)
```
No bundler and no maturin — `tsc` only. Packaging for the marketplace: `npm run vsix`
(`vsce package`). Local install / dev host: `npm run install:local` / `npm run sync:local`
(PowerShell scripts under `scripts/`). The extension talks to the engine over the LiveServer
protocol, so a built/installed core makes live diffs fast (see the Rust-core section).

## dbt plugin (`plugins/intentumdiff_dbt`, separate pip package)

Its own `build.py` (Hatch hook: `cargo` → `.wasm`) builds the dbt parser/enricher crates into
`plugins/intentumdiff_dbt/src/intentumdiff_dbt/wasm/`. Build it only when working on the dbt plugin;
it ships as its own wheel.

## Packaging / wheels (release)

The main wheel bundles the Rust core + `.wasm` parsers. `maturin build --release` produces the
wheel; the publish workflow (`.github/workflows/publish.yml`) always builds `--release`, so
end users are never on a debug core. This matters only for release validation — day-to-day you
use `maturin develop --release`.

## After building — verify

Run the suites for the layer you built (see `intentumdiff-testing`): `pytest tests/unit`,
`cargo test -p rust-core-host`, and/or `cd plugins/vscode && npm run test`. For engine changes,
also sanity-check with a real diff: `intentumdiff file old.py new.py --profile-phases`.

## Stale-wasm debt: full rebuilds surface old source bugs (2026-07-07)

Wasm artifacts in `src/intentumdiff/wasm/` are gitignored and rebuilt ad hoc, so a parser
crate's SOURCE can drift for months while tests keep passing against an old binary. The
first full `python build.py` then "breaks" tests that were never actually protecting the
current source (seen 2026-07: graphql child-blind frame hashes, quoted literal labels in
csharp/powershell fixtures, fuel-threshold drift). Two rules:

1. After changing ANY crate under `crates/` (sdk included), rebuild and gate the FULL
   affected surface, not just the languages you touched — `lto = true` +
   `codegen-units = 1` means any crate change re-optimizes the whole binary, shifting
   wasm fuel by ±10-15% for unrelated parsers.
2. When a full rebuild breaks a test that "used to pass", first ask when that language's
   wasm was last actually built — the failure usually reveals committed-but-never-built
   source, and the fix belongs at the source (parser bug or stale fixture), not in a
   revert of the rebuild.
