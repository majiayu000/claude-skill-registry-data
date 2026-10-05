---
name: deep-review
description: Run a deep code review across the manifold-csg crates
user-invocable: true
---

# Deep Review

Run a thorough code review of the manifold-csg workspace. Check all `crates/` source files.

## Arguments

- No arguments: review the entire codebase
- A file path or glob: review only matching files (e.g., `crates/manifold-csg/src/manifold.rs`)
- `since release`: review only files changed since the last release tag (use `git diff --name-only $(git describe --tags --abbrev=0)..HEAD -- '*.rs'` to get the list)
- `staged`: review only staged files (`git diff --cached --name-only -- '*.rs'`)
- `branch`: review only files changed on the current branch vs `main` (`git diff --name-only main...HEAD -- '*.rs'`)

## Review Categories

Work through each category in order. For each finding, cite the file and line number.

### 1. Idiomatic Rust

Review as the pickiest expert Rust reviewer. Look for:
- Anti-patterns and non-idiomatic code
- Misuse of language features (lifetimes, traits, enums, error handling)
- Places where `Result` should replace `bool`/`Option`, enums should replace strings, named structs should replace tuples
- Missing standard trait implementations (Display, From, Default, etc.)
- Unnecessary clones, allocations, or copies
- Iterator chains that could replace manual loops

### 2. Code Smells

- Dead code (unused functions, imports, fields, variants)
- Duplicate code — check across crates, not just within files
- Functions that are too long or do too many things
- Refactoring opportunities (extract function, simplify conditionals)
- Magic numbers that should be named constants

### 3. FFI Safety & Resource Management

This is the highest-risk area for a bindings crate. Verify:
- Every C allocation (`manifold_alloc_*`) is paired with deallocation (`manifold_delete_*`) on ALL paths including error returns and panics
- `Drop` implementations null-check before freeing
- No double-free paths — verify ownership transfer semantics in batch operations, decompose, etc.
- `unsafe impl Send` on `Manifold` and `CrossSection` — justification still valid? Check upstream C++ for any new thread-local state or shared mutable state
- `Sync` is deliberately NOT implemented — verify this is still correct (check for `mutable shared_ptr<CsgNode> pNode_` in upstream)
- No panic-across-FFI risk — if a Rust panic unwinds through C frames, it's UB. Check that no panic-capable code runs inside FFI call sequences
- Integer casts at the FFI boundary (u32↔u64, usize→c_int) — check for truncation/overflow
- Pointer validity — every raw pointer dereference must have a preceding validity argument (allocation or invariant)
- Buffer size correctness — when copying data out via `manifold_meshgl*_vert_properties` / `manifold_meshgl*_tri_verts`, verify buffer sizes match what the C API expects
- `ManifoldManifoldPair` — verify both returned pointers are always consumed (no leak if caller ignores one half of a split)

**Build script (`build.rs`) correctness for cross-compile:**
- `cfg!(target_os = ...)` / `cfg!(target_arch = ...)` / `cfg!(target_env = ...)` in `build.rs` is a footgun *when used to detect the target* — these macros evaluate at the build-script-host's compile time, NOT the target's. Coincidentally correct as long as we never cross-compile; fails silently the moment we do (e.g. wasm). Use `env::var("CARGO_CFG_TARGET_OS")` / `..._ARCH` / `..._ENV` instead. (`cfg!` is fine when you genuinely want host-side detection — e.g., picking a shell command for the build script's own use.)
- `cargo:rustc-link-arg=FLAG` from a sys crate's `build.rs` does NOT propagate to downstream link invocations — only `rustc-link-lib` and `rustc-link-search` do. The proper sys-crate idiom for forwarding link flags: emit `cargo:KEY=VALUE` (Cargo translates this into `DEP_<UPPERCASE_LINKS>_<UPPERCASE_KEY>` env var visible to dependents), and have the safe wrapper crate's `build.rs` read it and re-emit `cargo:rustc-link-arg=...`. End-user binaries then need a similar build.rs (or `.cargo/config.toml`). Flag any `cargo:rustc-link-arg=...` in a sys crate that isn't backed by this pattern.
- The artifact-typed variants (`cargo:rustc-link-arg-bins=`, `-tests=`, `-cdylib=`) are only legal from crates that declare those targets — a library-only sys crate can't use them (cargo rejects with "package does not have a bin target"). Flag any of these in a crate that doesn't have the matching target.

**CI cache key correctness (`actions/cache` + cmake builds):**
- cmake's `CMakeCache.txt` records absolute paths (toolchain file, source dir, `-D` options). If a cached `target/` is restored on a run where any of those paths differ — including from a different OUT_DIR layout, a different emsdk install location, or a different CMakeLists.txt source dir — cmake refuses with "source does not match the source used to generate cache." We've been bitten by this twice: once on the Emscripten lane (emsdk path moved between runs), once on the wasm32-uu lane (source dir moved when adopting the shim's CMake helper).
- The footgun is **`restore-keys` being too permissive**. `restore-keys` does prefix matching, so if the prefix is just `${runner.os}-cargo-<lane>-<cache-version>-`, ANY old cache for that lane gets pulled in — even one built with an incompatible cmake source dir.
- Fix pattern: split the cache `key` so layout-affecting inputs (env vars like `EMSDK`, files like `build.rs` and `wasm32-uu/**`) are part of the `restore-keys` PREFIX, while frequently-changing inputs (`Cargo.lock`, lower-level `build.rs` files) live in the suffix. That way changing a layout input shifts the prefix → no incompatible cache restored. Look for any cache stanza whose `restore-keys` doesn't include the same prefix-segments as the `key` for inputs that affect cmake's recorded paths.
- The `cache-version` bump file is the manual escape hatch when caches go bad — it busts every lane's cache. Useful as a one-shot recovery, but not a substitute for fixing the key structure.

### 4. Numerical Precision

Precision is our key differentiator (f64/MeshGL64). Verify:
- f64 precision is used by default everywhere — no accidental f32 narrowing
- `from_mesh_f32` / `to_mesh_f32` paths are clearly documented as lossy
- No unnecessary f64→f32→f64 round-trips in internal code paths
- Extrude and other operations that bridge CrossSection↔Manifold don't silently lose precision through intermediate polygon representations
- Tolerance/epsilon values used in triangulation and offset operations are documented and appropriate

### 5. API Completeness

We bind the complete manifold3d v3.4.1 C API (256 functions in `manifold-csg-sys`). The review focus is on **maintaining** completeness and ensuring the safe layer covers everything useful.

**Sys crate vs upstream header:**
- Read the manifold3d C header (`manifoldc.h`, built during compilation at `target/*/build/manifold-csg-sys-*/out/build/_deps/manifold-src/bindings/c/include/manifold/manifoldc.h`) and diff against `manifold-csg-sys/src/lib.rs`
- If we've updated the pinned manifold version, check for newly added C API functions that need binding
- Verify all function signatures still match the header (parameter types, return types) — ABI drift from upstream changes

**Safe wrapper coverage:**
- For every function group bound in `manifold-csg-sys`, verify there is a corresponding safe method in `manifold-csg`. Flag sys-level functions that have no safe wrapper yet. Prioritize by usefulness.
- Specifically check: are all callback-based APIs (warp, set_properties, level_set, write_obj) wrapped safely? These are the hardest to get right.
- Are all MeshGL/MeshGL64 advanced accessors (merge, run_index, face_id, tangents) exposed through the safe `MeshGL`/`MeshGL64` types?
- Are the quality globals (`set_min_circular_angle`, `set_circular_segments`, etc.) exposed? If so, are they documented as affecting global state?

**Feature flag coverage:**
- Does the `nalgebra` feature cover all methods that take/return geometric types (vectors, points, matrices)?
- Are there other popular geometry crates that should have optional integration (e.g., `glam`, `mint`)?

### 6. API Ergonomics

Review the safe API from a user's perspective:
- Are method signatures intuitive? Would a first-time user understand the parameter order?
- Are there missing convenience methods? (e.g., `Manifold::translate_z()`, `CrossSection::offset_round()`)
- Should any methods accept `impl Into<T>` for flexibility?
- Are builder patterns appropriate anywhere? (e.g., extrude with optional twist/scale)
- Error types — are they specific enough to be actionable? Can users match on error variants?
- Does the re-export structure in `lib.rs` give users a clean import experience?
- Are operator overloads (`+`, `-`, `^`) discoverable and documented?
- Should `Manifold::extrude` be an associated function or a method on `CrossSection`?

**C/C++ API parity (critical — many users will transition from the C/C++ library):**
- For every safe wrapper method, compare parameter order and types against the corresponding C function in `manifoldc.h`. Flag any reordering, renamed parameters, or hidden defaults that would surprise a C/C++ user.
- Check that optional/defaulted parameters match C API defaults. If a Rust wrapper omits a C parameter (e.g., `center`, `slices`, `twist`), verify there's either a sensible default or a `_with_options` variant that exposes full control.
- Check consistency: do similar functions handle the same parameter the same way? (e.g., `cube`, `cylinder`, and `CrossSection::square` should all handle `center` identically — not some hardcoded and some exposed)
- Verify the layout/ordering of array parameters matches C conventions (e.g., `transform`'s column-major `[f64; 12]` should document the mapping to C's 12 individual params)
- Check that enum variant names are recognizable to C users (e.g., `JoinType::Round` maps obviously to `MANIFOLD_JOIN_TYPE_ROUND`)
- Where Rust packs multiple C params into an array (e.g., `normal: [f64; 3]` instead of `nx, ny, nz`), verify this is documented

### 7. Test Coverage & Quality

Assess the test suite:
- Untested public functions — every public method in the safe API should have at least one test
- Edge cases — empty inputs, zero-size primitives, very large/small values, degenerate geometry
- Negative testing — do error paths get exercised? (invalid meshes, empty polygons, etc.)
- Thread safety — is Send tested with actual thread spawning, not just compile-time assertions?
- Round-trip fidelity — are mesh export→import round-trips tested for volume/vertex preservation?
- Test isolation — do tests depend on execution order or shared mutable state?
- `#[ignore]` tests — are they still relevant or should they be deleted/fixed?
- Assertion quality — are tests checking meaningful properties or just "doesn't panic"?
- Multi-target gating: tests that depend on host-OS facilities (`std::thread::spawn`, filesystem, sockets, signals) should be gated with `#[cfg_attr(target_os = "...", ignore = "explanation")]` for targets that lack them. The ignore reason should explain *why* it's ignored on this target, not just *that* it is.
- For cross-compiled targets without a native runner (wasm, embedded), check whether `CARGO_TARGET_<TRIPLE>_RUNNER` is configured (`.cargo/config.toml`, CI workflow env). Without a runner, "build clean" doesn't tell us tests pass.

### 8. Examples & Documentation Artifacts

Verify the documentation artifacts are consistent with the code:

**Examples (`crates/manifold-csg/examples/`):**
- Do all examples compile and run without errors? (`cargo run -p manifold-csg --example basics`, etc.)
- Do examples cover the main entry points: primitives, booleans, transforms, 2D cross-sections, extrusion, SDF, OBJ I/O, and threading?
- Are examples free of `unwrap()` on fallible operations without explanation?
- Do examples demonstrate idiomatic usage patterns that new users should follow?

**API coverage table (`API_COVERAGE.md`):**
- Does the table account for every function declared in `manifold-csg-sys/src/lib.rs`?
- Are the safe wrapper links accurate (correct file and line number)?
- Are "Internal" and "Not wrapped" statuses correct?
- Does the summary count match the detailed tables?
- Has the table been updated after any API additions or removals?

**README:**
- Are feature descriptions accurate and consistent with the code?
- Do quick-start examples compile?
- Are links to examples/, API_COVERAGE.md, and source files valid?

### 9. Packaging & Publishing Correctness

Review everything a crate maintainer needs for correct, user-friendly publishing:

**Versioning scheme (see CLAUDE.md):**
- `manifold-csg-sys` version = `{upstream_major}.{upstream_minor}.{100+our_release}` (e.g., `3.4.100`). Verify the version matches the manifold3d tag pinned in `build.rs`.
- `manifold-csg` version = standard semver (`0.x.y`), independent of upstream. Its dependency on `manifold-csg-sys` must pin the correct sys version.
- When the manifold3d pin is bumped, the sys crate version MUST be updated to match. Flag any mismatch.

**Cargo.toml correctness:**
- `package.description` — present, concise, accurate for both crates
- `package.documentation` — points to docs.rs (or will auto-generate)
- `package.readme` — set if README exists
- `package.keywords` and `package.categories` — set and relevant (max 5 keywords). Good keywords for discoverability: `csg`, `geometry`, `mesh`, `manifold`, `3d`
- `package.exclude` / `package.include` — exclude test fixtures, build artifacts, CI config from the published crate
- `links` key in sys crate — correctly set to prevent duplicate linking
- Edition — using latest stable edition? (currently 2024)

**Dependency hygiene:**
- Are all dependencies at their latest compatible versions? (`cargo update --dry-run`)
- Are dev-dependencies correctly scoped? (nothing test-only leaking into the main dependency tree)
- `build-dependencies` — `cmake` version current?
- Feature flags — are there any that should exist? (e.g., `parallel` for TBB, `nalgebra` for convenience conversions)

**Publishing readiness:**
- `cargo publish --dry-run` for both crates — does it succeed?
- Crate size — is the published crate reasonably small? (no vendored C++ source, no build artifacts)
- License files — `LICENSE-APACHE` and `LICENSE-MIT` present and referenced in Cargo.toml
- `links = "manifold"` — will this conflict with other `-sys` crates linking the same library? Document how users should handle this.

**Ecosystem & Cargo evolution:**
- Is the `resolver = "2"` setting still the recommended default, or has a newer resolver landed?
- Are there new Cargo features (e.g., artifact dependencies, public/private dependencies via `dep:`, lints table changes) that would improve the crate?
- Are there upcoming Rust edition changes that affect this code? (e.g., new `unsafe extern` syntax was stabilized in 2024 edition — are we using it?)
- Check `rust-version` (MSRV) — should we declare one? What's the minimum Rust version that compiles this?
- Are there new crates.io policies (e.g., trusted publishing, provenance attestations) we should adopt?

**Documentation:**
- Crate-level `//!` docs — present, has example code, links to upstream manifold3d
- `#[doc(hidden)]` on internal items that leak through `pub(crate)`
- Do doc-tests compile? (currently ignored with `rust,ignore` — can they be made runnable?)

### 10. Upstream Compatibility

This crate tracks manifold3d upstream. Verify:
- Pinned version in `build.rs` — what version are we on? What's latest? What changed?
- ABI compatibility — have any C API function signatures changed in newer manifold3d releases?
- Deprecated functions — are we binding any C API functions that upstream has deprecated?
- **wasm32-unknown-unknown cfg-gates may need revisiting.** Grep for `target_os = "unknown"` across the workspace. Each gated FFI declaration / safe wrapper / test is gated because that C API surface postdates the shim's tested manifold pin. When the shim's tested pin moves to (or past) our host pin, those gates can be removed. The OBJ I/O gates (`manifold_*_obj`) are gated for a different reason (iostream patches strip them) and stay regardless.
- New capabilities — has upstream added significant new C API surface (new types, new operations) that we're missing?
- Build system changes — has manifold3d changed its CMake structure, added/removed FetchContent deps, changed library names?
- Known upstream bugs — check manifold3d issues for bugs affecting functions we bind (especially boolean operations, MeshGL64, CrossSection offset)

### 11. Dependency Audit

- Check all Cargo dependencies are at their latest published version — run `cargo update --dry-run` and flag anything that can be bumped
- Check C++ dependencies in `build.rs` — the manifold3d tag is pinned there. Check [github.com/elalish/manifold/releases](https://github.com/elalish/manifold/releases) for newer releases. Manifold also pulls Clipper2 and TBB via CMake FetchContent (versions controlled by manifold's CMakeLists.txt)
- Known issues in upstream crates or C++ libraries
- License concerns — warn on any copyleft/viral license (GPL, LGPL, AGPL, SSPL). Note: manifold3d is Apache-2.0, Clipper2 is Boost, TBB is Apache-2.0 — all compatible
- Unnecessary or redundant dependencies

## Output Format

Group findings by category. For each finding:

```
**[Category] file.rs:123** — Short description of the issue.
Suggested fix or explanation.
```

Assign each finding a severity:
- **error**: Correctness bug, unsoundness, undefined behavior, memory safety violation
- **warning**: Likely bug, missing safety check, precision loss, incomplete API
- **note**: Style, ergonomics, documentation, nice-to-have improvement

At the end, provide a summary: total findings per category, severity breakdown (error/warning/note), and recommended priority order for fixes.

If a category has zero findings, say so explicitly — don't skip it silently.
