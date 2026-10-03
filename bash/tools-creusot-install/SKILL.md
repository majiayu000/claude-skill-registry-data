---
name: tools-creusot-install
description: Install the Creusot Rust verification tool
---

This skill should not need sudo privileges.

## Prerequisites (must already be installed)
- curl
- Rust toolchain (rustup/cargo)
- opam (initialized with `opam init`)
- pip

If any prerequisite is missing, inform the user and stop.

## Installation Steps

1. Install z3-solver via pip if not already present:
   ```
   pip install z3-solver
   ```

2. Clone the Creusot repo into `tools/creusot/creusot` (if not already cloned):
   ```
   git clone https://github.com/creusot-rs/creusot tools/creusot/creusot
   ```

3. Run the install script with `--external z3` (uses the pip-installed z3):
   ```
   cd tools/creusot/creusot && ./INSTALL --external z3
   ```
   This installs cargo-creusot, creusot-rustc, Why3, why3find, Alt-Ergo, CVC4, and CVC5.

4. Fix why3find package resolution (required for proof discharge):
   ```
   mkdir -p ~/.local/share/creusot/_opam/lib/why3find/packages
   ln -sf ~/.local/share/creusot/share/why3find/packages/creusot \
          ~/.local/share/creusot/_opam/lib/why3find/packages/creusot
   ```

5. Add Creusot bin path to `~/.bash_profile`:
   ```
   export PATH="$HOME/.local/share/creusot/bin:$PATH"
   ```

6. Verify installation using the bundled test example:
   - Run `cargo creusot version` — should show version info for all components
   - Build and prove the test example:
     ```
     cd tools/creusot/creusot-test-example
     cargo clean
     cargo creusot
     ```
   - Confirm output shows `Proved (4 files) ✔`
   - Note: `cargo clean` is required before the first `cargo creusot` run if `cargo build`
     was previously executed (stale artifacts block the Creusot translation pass)

## Notes
- Z3 4.16.0 (from pip) is newer than the recommended 4.15 — produces a warning but works fine.
- The `--external z3` flag tells Creusot to use the system z3 rather than downloading its own.
- For proofs that SMT solvers cannot discharge (e.g. modular arithmetic with variable
  divisors), Coq can be added as an additional prover — see `tools-creusot-coq-install`.
