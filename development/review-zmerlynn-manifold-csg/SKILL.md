---
name: review
description: Run a deep code review across the manifold-csg crates
user-invocable: true
---

# Review

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
- Stale comments — references to upstream PR/issue numbers or transient implementation details that will go stale. These belong in CLAUDE.md or API_COVERAGE.md, not code comments.
- Stale docs — hardcoded counts (test count, function count, version numbers) in README or API_COVERAGE.md that will go stale on the next change. Prefer prose over numbers, or make them easy to regenerate.

### 3. FFI Safety & Resource Management

This is the highest-risk area for a bindings crate. Verify:
- Every C allocation (`manifold_alloc_*`) is paired with deallocation (`manifold_delete_*`) on ALL paths including error returns and panics
- `Drop` implementations null-check before freeing
- No double-free paths — verify ownership transfer semantics in batch operations, decompose, etc.
- `unsafe impl Send` — justification still valid? Check upstream C++ for any new thread-local state or shared mutable state
- `unsafe impl Sync` — verify the justification holds. Check that whatever synchronization mechanism upstream uses (carry-patch or merged) is actually present in the pinned commit or applied via patch.
- No panic-across-FFI risk — if a Rust panic unwinds through C frames, it's UB. Check that all FFI callback trampolines use `catch_unwind`
- Integer casts at the FFI boundary (u32↔u64, usize→c_int) — check for truncation/overflow
- Pointer validity — every raw pointer dereference must have a preceding validity argument (allocation or invariant)
- Buffer size correctness — when copying data out via length+copy accessor pairs, verify buffer sizes match what the C API expects
- `ManifoldManifoldPair` — verify both returned pointers are always consumed (no leak if caller ignores one half of a split)
- Mutable FFI methods (those taking `*mut`) — verify the safe wrapper requires `&mut self` to prevent aliasing

### 4. Numerical Precision

Precision is our key differentiator (f64/MeshGL64). Verify:
- f64 precision is used by default everywhere — no accidental f32 narrowing
- f32 code paths are clearly documented as lossy
- No unnecessary f64→f32→f64 round-trips in internal code paths
- Operations that bridge CrossSection↔Manifold don't silently lose precision through intermediate representations
- Tolerance/epsilon values are documented and appropriate

### 5. API Completeness

We bind the manifold3d C API (pinned to a specific upstream commit in `build.rs`). The review focus is on **maintaining** completeness.

**Sys crate vs upstream header:**
- Find the built C header (`manifoldc.h`) under `target/*/build/manifold-csg-sys-*/out/` and diff against `manifold-csg-sys/src/lib.rs`
- Check for newly added C API functions that need binding
- Verify all function signatures still match the header — ABI drift from upstream changes

**Safe wrapper coverage:**
- For every function group bound in the sys crate, verify there is a corresponding safe method. Flag sys-level functions that have no safe wrapper yet. Prioritize by usefulness.
- Are all callback-based APIs wrapped safely with `catch_unwind`?
- Are all MeshGL/MeshGL64 accessors exposed through the safe types?
- Are the quality globals exposed and documented as affecting global state?

**Feature flag coverage:**
- Does the `nalgebra` feature cover all methods that take/return geometric types?
- Are there other popular geometry crates that should have optional integration?

### 6. API Ergonomics

Review the safe API from a user's perspective:
- Are method signatures intuitive? Would a first-time user understand the parameter order?
- Are there missing convenience methods?
- Should any methods accept `impl Into<T>` for flexibility?
- Are builder patterns appropriate anywhere?
- Error types — are they specific enough to be actionable?
- Does the re-export structure in `lib.rs` give users a clean import experience?
- Are operator overloads discoverable and documented?

**C/C++ API parity (many users will transition from the C/C++ library):**
- Compare parameter order and types against the C header. Flag reordering, renamed parameters, or hidden defaults that would surprise a C/C++ user.
- Check that optional/defaulted parameters match C API defaults. If a wrapper omits a C parameter, verify there's a sensible default or `_with_options` variant.
- Check consistency: do similar functions handle the same parameter the same way?
- Where Rust packs multiple C params into an array (e.g., `normal: [f64; 3]` instead of `nx, ny, nz`), verify this is documented

### 7. Test Coverage & Quality

Assess the test suite:
- Untested public functions — every public method should have at least one test
- Edge cases — empty inputs, zero-size primitives, very large/small values, degenerate geometry
- Negative testing — do error paths get exercised?
- Thread safety — is Send tested with actual thread spawning? Is Sync tested with concurrent reads?
- Round-trip fidelity — are mesh export→import round-trips tested for volume/vertex preservation?
- Test isolation — do tests depend on execution order or shared mutable state?
- Assertion quality — are tests checking meaningful properties or just "doesn't panic"?

### 8. Examples & Documentation Artifacts

**Examples:**
- Do all examples compile and run? (`cargo run -p manifold-csg --example <name>`)
- Do examples cover the main entry points?
- Are examples free of unexplained `unwrap()`?

**API_COVERAGE.md:**
- Does it account for every function in the sys crate?
- Are safe wrapper links accurate?
- Does the summary count match the detailed tables?

**README:**
- Are feature descriptions accurate? (e.g., Send/Sync, f64 default, test count, upstream version)
- Do quick-start examples compile?
- Are links valid?
- MSRV, platform support, and build requirements documented?
- Badges present and pointing to the right crate/repo?

**Docstrings:**
- Do all main types (`Manifold`, `CrossSection`, `MeshGL`, `MeshGL64`) link to the upstream manifold3d API docs so users can understand parameter semantics?
- Does the crate-level doc (`lib.rs`) link to upstream?
- Run `cargo doc --no-deps` — any warnings?
- Are methods with non-obvious parameters (e.g., `normal_idx`, `min_sharp_angle`, column-major matrices) documented well enough that a user doesn't have to read C++ headers?

### 9. Packaging & Publishing Correctness

**Versioning (see CLAUDE.md for the scheme):**
- Verify sys crate version matches the upstream pin
- Verify safe crate dependency pins the correct sys version
- Sys patch bumps must be semver-compatible (additions only). Flag any violations.

**Cargo.toml correctness:**
- `description`, `readme`, `keywords`, `categories` — present and accurate
- `package.exclude` / `package.include` — no test fixtures or build artifacts in published crate
- `links` key in sys crate — correctly set

**Publishing readiness:**
- `cargo publish --dry-run` for both crates — does it succeed?
- Crate size — reasonably small? (no vendored C++ source)
- License files present and referenced

**API stability audit (pre-publish):**
- Flag any public API that feels provisional or likely to change — hard to undo after publishing
- Are there methods that should be `pub(crate)` instead of `pub`?
- Are return types locked in appropriately?

**Dependency hygiene:**
- `cargo update --dry-run` — anything to bump?
- Dev-dependencies correctly scoped?
- Feature flags complete?

**Documentation:**
- Crate-level `//!` docs present with examples
- Doc-tests — can any `rust,ignore` tests be made runnable?

### 10. Upstream Compatibility & Carry-Patches

This crate tracks manifold3d upstream, pinning to a specific commit SHA.

**Pinned commit:**
- Is the pinned SHA still on upstream's master branch (not reverted)?
- What's the latest upstream release tag? How far ahead/behind are we?
- Have any upstream changes since our pin affected the C API?

**Carry-patches (`crates/manifold-csg-sys/patches/`):**
- List all current patches. For each:
  - Has the upstream PR been merged? If so, is it included in our pinned commit? (Can be removed if yes.)
  - Does the patch still apply cleanly?
  - Is any safety justification in our code (e.g., `unsafe impl Sync`) dependent on this patch?
- Are there upstream fixes we need that aren't in our pin or patches?
- Patch scope: restricted to `src/` (and `bindings/` if relevant) — no `test/` since we build with `MANIFOLD_TEST=OFF`, no docs/JS/python.
- Patch size roughly matches the upstream PR's stated diff. A patch that's much larger than the linked PR is a red flag — it usually means whoever generated it used `git diff master..pr-branch` instead of `git diff $(git merge-base master pr-branch)..pr-branch`, and silently picked up the reverse of master's intervening commits.
- Patch filename has a numeric prefix (e.g., `0001-`) that encodes apply order, and references the upstream PR number.

**Release PR descriptions and commit messages:**
- Cross-repo PR refs use `elalish/manifold#NNNN` (no backticks) — bare `#NNNN` resolves to our own repo, and backticks suppress GitHub's auto-link entirely.
- Same-repo PR refs (`#NNNN`) are correct and auto-link as-is.
- When the release window includes a contributor PR (e.g., from a non-maintainer), credit them by `@username` in the release PR body.

**Known upstream bugs:**
- Check manifold3d issues for bugs affecting functions we bind
- Note any upstream error status propagation issues that affect our safe wrappers

### 11. Dependency Audit

- Cargo dependencies at latest? (`cargo update --dry-run`)
- C++ dependencies — check upstream releases for newer versions. Manifold pulls Clipper2 and TBB via CMake FetchContent.
- License concerns — warn on any copyleft/viral license
- Unnecessary or redundant dependencies

### 12. Cross-Platform & CI

- Does the build work on all platforms? Check CI results.
- Are there platform-specific code paths in `build.rs`?
- Does CI test with and without the `parallel` feature?
- Does CI test the declared MSRV?
- Are there CI jobs that should exist but don't?

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
