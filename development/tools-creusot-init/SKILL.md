---
name: tools-creusot-init
description: Prepare an existing Cargo project to use Creusot formal verification
argument-hint: <project-directory>  (e.g. components/extent-manager)
---

This skill takes a cargo project directory and configures it for Creusot verification.

## Input

The user must provide the target project directory as an argument (e.g. `/tools-init-creusot components/dispatch-map`).

If no argument is provided, show the hint and stop.

## Prerequisites

- Creusot must already be installed (`cargo creusot version` should succeed)
- If not installed, inform the user to run the `tools-install-creusot` skill first, then stop

## Steps

1. Verify the target directory contains a `Cargo.toml`. If not, inform the user and stop.

2. Check that Creusot is installed by running `cargo creusot version`. If it fails, tell the user to run `/tools-install-creusot` first and stop.

3. Modify `Cargo.toml`:
   - Add `creusot-std = "0.12.0-dev"` under `[dependencies]` (if not already present)
   - Add a `[patch.crates-io]` section pointing to the local creusot-std (use a relative path from the project to the certus repo's `tools/creusot/creusot/creusot-std`, or use `~` notation for shell expansion):
     ```toml
     [patch.crates-io]
     creusot-std = { path = "<relative-path-to>/tools/creusot/creusot/creusot-std" }
     ```
     Compute the correct relative path from the target project directory to `certus/tools/creusot/creusot/creusot-std`.
   - Add the `cfg(creusot)` lint configuration under `[lints.rust]`:
     ```toml
     [lints.rust]
     unexpected_cfgs = { level = "warn", check-cfg = ['cfg(creusot)'] }
     ```
   - If the project is inside another workspace but should be standalone, add an empty `[workspace]` table

4. Create `why3find.json` in the project root (if not already present):
   ```json
   {
     "fast": 0.2,
     "time": 1,
     "depth": 6,
     "packages": [ "creusot" ],
     "provers": [ "alt-ergo", "z3", "cvc5", "cvc4" ],
     "tactics": [ "compute_specified", "split_vc" ],
     "drivers": [],
     "warnoff": [ "unused_variable", "axiom_abstract" ]
   }
   ```

5. Add `use creusot_std::prelude::*;` to `src/lib.rs` or `src/main.rs` (if not already present). If the file has existing functions, add a commented example showing how to annotate:
   ```rust
   // Example Creusot annotations:
   // #[requires(precondition)]
   // #[ensures(postcondition)]
   // pub fn verified_function(...) { ... }
   ```

6. Run `cargo clean` to remove any stale build artifacts that would block Creusot's translation pass.

7. Verify the setup works by running:
   ```
   export PATH="$HOME/.local/share/creusot/bin:$PATH"
   cargo creusot --only coma
   ```
   This should compile without errors. If there are no annotated functions yet, it will produce no `.coma` files — that's expected.

8. Report success and tell the user:
   - Add `#[requires(...)]` and `#[ensures(...)]` annotations to functions they want to verify
   - Run `cargo creusot` to build and prove
   - Run `why3find prove verif/<crate_name>_rlib/*.coma` to prove individual files
   - Reference `certus/tools/creusot/creusot-test-example/src/lib.rs` for annotation examples

## Notes
- Always run `cargo clean` before the first `cargo creusot` if the project was previously built with plain `cargo build`
- The `[patch.crates-io]` section assumes Creusot was cloned to `certus/tools/creusot/creusot` per the install skill
- If the project uses `edition = "2024"`, it works with Creusot's required nightly toolchain
