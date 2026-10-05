---
name: update-upstream
description: Bump the manifold3d pin, add FFI + safe wrappers for new upstream C API functions, bump versions, open a PR
user-invocable: true
---

# Update upstream

Guided workflow for picking up upstream manifold3d changes: bump the pin,
audit carry-patches, bind new C API, add safe wrappers, bump versions,
open a PR. The user still makes API shape decisions for new wrappers;
this skill handles the mechanical parts.

## Arguments

- No arguments: bump to current upstream master HEAD
- A commit SHA, tag, or branch name: bump to that ref instead (e.g., `v3.5.0`, `abc123def`)

## Steps

Work through these in order. Stop and surface any decision to the user.

### 1. Clean working tree, new branch

```
git status               # must be clean on main
git checkout main && git pull
git checkout -b update-upstream-<ref>
```

### 2. Determine the target ref

- If the user gave a ref, use it directly.
- Otherwise, query upstream master HEAD: `gh api repos/elalish/manifold/git/refs/heads/master --jq '.object.sha'`
- Show the user: current pin (from `MANIFOLD_VERSION` in `crates/manifold-csg-sys/build.rs`), the target, and a one-line commit summary of what's between them: `gh api repos/elalish/manifold/compare/<current>...<target> --jq '{ahead_by: .ahead_by, commits: [.commits[] | {sha: .sha[0:8], message: (.commit.message | split("\n")[0])}]}'`
- Confirm before proceeding.
- **Check shim coverage.** Before committing to the target, verify `wasm-cxx-shim` supports it. Look at the latest shim release's `MANIFOLD_GIT_TAG` default (in the helper at `cmake/WasmCxxShimManifold.cmake`, or in the release notes). If the target SHA is past the shim's tested pin, flag it: either pick a target the shim already supports, or be ready to cfg-gate any new C API on `not(all(target_arch = "wasm32", target_os = "unknown"))` (the wasm-uu lane will fall back to the shim's tested pin via `wasm_cxx_shim_add_manifold()`'s default). Mismatch without gating produces wasm-uu link failures — see CLAUDE.md "Versioning" section.

### 3. Update the pin

Edit `MANIFOLD_VERSION` in `crates/manifold-csg-sys/build.rs`. The constant accepts tags, branches, or commit SHAs — prefer SHAs for reproducibility (commit on master) or tags for tagged releases.

Then update the Nix offline lane to match: run `nix flake update` and commit the new `flake.lock`. The `nix-offline` CI lane links nixpkgs' prebuilt `manifold` via `MANIFOLD_CSG_LIB_DIR`, so the locked nixpkgs must resolve to a `manifold` matching the new pin (or the lane links an ABI-mismatched library). If nixpkgs hasn't caught up to the new upstream version yet, note it for the user - the lane may fail until nixpkgs ships it.

### 4. Carry-patch audit

For each patch in `crates/manifold-csg-sys/patches/`:
- Check if the referenced upstream PR has been merged (`gh api repos/elalish/manifold/pulls/<N>`).
- If merged AND included in the new pin, the patch can be removed — propose deletion to the user and remove if they agree.
- Run `cargo clean -p manifold-csg-sys && cargo build -p manifold-csg-sys`. If any patch fails to apply, stop and surface the conflict — the user needs to either update the patch or drop it.

### 5. Clean build and test

```
cargo clean -p manifold-csg-sys
cargo test --features nalgebra
```

Any test failure stops the flow. Common causes: upstream changed behavior (e.g., numerical differences from deterministic math changes), signature changes (will show as compile errors), or carry-patch conflicts.

### 6. Diff the C header against our FFI bindings

The built C header is at `target/debug/build/manifold-csg-sys-*/out/manifold-src/bindings/c/include/manifold/manifoldc.h`. Find it and extract every `manifold_*` function declaration, compare against `pub fn manifold_*` in `crates/manifold-csg-sys/src/lib.rs`.

Also look for new types (structs, enums, opaque handles) in `bindings/c/include/manifold/types.h`.

Report:
- **New functions** (present in header, missing from sys crate) — grouped by category (memory management, allocation, ray casting, etc.)
- **Changed signatures** (present in both but different) — these are breaking upstream changes that need attention
- **Removed functions** (in sys crate, missing from header) — should be deleted from our FFI

### 7. Decide what to bind (user choice)

Show the list of new functions to the user. Ask which to bind in this PR. Some guidelines:
- Standalone features (e.g., ray casting) — usually yes
- Allocation/destruct helpers for new types — bind along with the feature they support
- Deeply specialized accessors — may defer if no clear safe API maps to them
- Internal size queries — bind but mark as internal

If the user says "bind everything new," proceed without individual approval.

### 8. Add FFI declarations

In `crates/manifold-csg-sys/src/lib.rs`:
- Add any new opaque handle types (e.g., `pub struct ManifoldXyzVec { _private: [u8; 0] }`).
- Add any new value types with `#[repr(C)]`.
- Add new size/alloc/destruct/delete functions in their respective sections.
- Add new operational functions in a logical section (or create a new section with a `// ── <Name> ──` header).

Match the upstream C header signature exactly. Use `*const` for read-only pointers where the C uses non-const but we can tell the function is read-only.

### 9. Add safe wrappers

For each new function, write a safe wrapper method or free function in the appropriate `crates/manifold-csg/src/` file. If the new functionality deserves its own module (like ray casting did), create it and register in `lib.rs`.

Follow existing patterns:
- Allocate with `manifold_alloc_*`, call the FFI, delete the allocation, return a new wrapper.
- For methods returning multiple values, define a value-type struct in the safe crate with `[f64; 3]` arrays for 3D vectors.
- Safety comments: every `unsafe` block gets a `// SAFETY: ...` explaining the invariant.
- `#[must_use]` on pure transforms returning `Self`.
- Link to upstream docs in the doc comment if the semantics are non-obvious.

### 10. Add tests

New tests go in `crates/manifold-csg/tests/integration.rs`. Cover:
- Happy path (does the feature work?)
- Edge case (empty input, miss, degenerate geometry)
- Any invariants (e.g., unit-length normals, non-negative distances)

Run `cargo test --features nalgebra` and `cargo clippy --all-targets --features nalgebra -- -D warnings`.

### 11. Update API_COVERAGE.md

Add rows for new wrappers. Update the summary if present (but prefer prose over hardcoded counts — see CLAUDE.md).

### 12. Bump versions

Per CLAUDE.md versioning policy:
- `manifold-csg-sys`: patch bump (e.g., `3.4.103` → `3.4.104`) since upstream contents changed. If the upstream major.minor changed (new manifold3d release), update major.minor accordingly.
- `manifold-csg` (workspace version): patch bump for additive changes, minor for breaking.
- `manifold-csg`'s `manifold-csg-sys` dep: update to new sys version.
- `manifold3d-sys` and `manifold3d` share their canonical counterparts' versions via `=` pins; update those pins.

### 13. Commit and open PR

One commit. Commit message explains:
- New pin SHA or tag
- Any carry-patches added or removed
- New bindings added
- Version bumps

Use `/pr` skill or `gh pr create` directly. Show the user the draft before posting — the `feedback_no_public_posts` rule applies.

### 14. (Optional) publish

If the user wants to publish after the PR merges, invoke `/publish`.

## Rules

- Do NOT invoke this skill on a dirty working tree.
- Do NOT skip the clean rebuild — it's what confirms the new pin actually works.
- Do NOT bind functions blindly — judgment about what deserves a safe wrapper is part of the job.
- Surface any upstream API breakage loudly — it's easy to miss and expensive to ship.
- All rules from CLAUDE.md apply (no hard-wrap in PR descriptions, no Claude session links in commits, show PR drafts before posting, etc.).
