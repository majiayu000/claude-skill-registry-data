---
name: tools-creusot-annotate-interfaces
description: Formally verify a component's properties with Creusot and annotate its interface definitions
argument-hint: "[component-name]"
---

Given a target component, this skill:
1. Creates a verification branch and `verif/` subdirectory
2. Writes a Creusot verification model for the component's key properties
3. Runs the prover to discharge all verification conditions
4. Returns to the original branch and annotates the interface definition files with verified and unchecked property comments

## Interactive Configuration

If no component name is provided as an argument, list the available components and ask the user to select one:

```bash
ls components/*/Cargo.toml | sed 's|components/||;s|/Cargo.toml||' | sort
```

Present the list and ask the user to choose.

## Workflow

### 1. Pre-flight

- Record the current branch: `ORIGINAL_BRANCH=$(git branch --show-current)`
- Check for uncommitted changes; if any, stash them: `git stash push -m "pre-creusot-annotate"`
- Verify Creusot is installed: `cargo creusot version` (if not, tell the user to run `/tools-creusot-install`)
- Identify the component's interface file(s) by reading its `define_component!` block to find which interfaces it `provides` (e.g., `IDispatcher`, `IDispatchMap`)
- Locate the corresponding interface definition file(s) in `components/interfaces/src/`

### 2. Create Verification Branch

```bash
git checkout -b creusot/<component-name>
```

### 3. Create the `verif/` Subdirectory

Create `components/<component-name>/verif/` with:

**`Cargo.toml`:**
```toml
[package]
name = "<component-name>-verif"
version = "0.1.0"
edition = "2021"
publish = false

[workspace]

[dependencies]
creusot-std = { path = "../../../tools/creusot/creusot/creusot-std" }

[lints.rust]
unexpected_cfgs = { level = "warn", check-cfg = ['cfg(creusot)'] }
```

**`why3find.json`:**
```json
{
  "fast": 0.2,
  "time": 2.0,
  "depth": 6,
  "packages": ["creusot"],
  "provers": ["alt-ergo", "z3", "cvc5"],
  "tactics": ["compute_specified", "split_vc"],
  "drivers": [],
  "warnoff": ["unused_variable", "axiom_abstract"]
}
```

**`src/lib.rs`:** The verification model (see step 4).

### 4. Write the Verification Model

Read the component's implementation source (`src/lib.rs`) to understand its internal logic. Extract the key correctness properties into a pure-functional Creusot model.

**Guidelines for writing the model:**

- Use `creusot_std::prelude::*` for annotations
- Model internal state as simple structs (no Mutex, HashMap, Arc — Creusot cannot handle those)
- Each operation becomes a pure function with `#[requires]` and `#[ensures]`
- Use `@` for logical integer projection (e.g., `value@ == 0`)
- Use `*state` for pre-state and `^state` for post-state on `&mut` params
- Use `proof_assert!()` for intermediate proof hints
- Composite lifecycle functions prove end-to-end scenarios
- Target: all VCs dischargeable by SMT solvers within 2 seconds

**Property categories to look for:**

- **Arithmetic safety**: No overflow/underflow on counters or indices
- **State machine validity**: Only valid transitions between states
- **Conservation laws**: Quantities preserved across operations (e.g., total refs)
- **Exclusivity/locking**: At most one writer, write blocks readers
- **Precondition enforcement**: Functions reject invalid inputs (return Err)
- **Lifecycle correctness**: Create→use→destroy paths leave no leaked resources
- **Idempotency**: Operations that should be safe to repeat

### 5. Run Verification

```bash
cd components/<component-name>/verif
export PATH="$HOME/.local/share/creusot/bin:$PATH"
cargo creusot
why3find prove
```

- If verification fails, analyze the unproved VCs, strengthen preconditions or add `proof_assert!` hints, and retry
- Iterate until all VCs are discharged (target: 0 unproved goals)
- Record the number of VCs proved per function

### 6. Commit on local Verification Branch (do not push remotely).

```bash
git add components/<component-name>/verif/
git commit -m "feat: add Creusot verification for <component-name>

Proved N properties with M total verification conditions discharged."
```

### 7. Return to Original Branch

```bash
git checkout $ORIGINAL_BRANCH
```

If changes were stashed in step 1, pop them: `git stash pop`

### 8. Annotate Interface Definitions

Edit the interface definition file(s) in `components/interfaces/src/` (e.g., `idispatch_map.rs`, `idispatcher.rs`).

**Scope rule:** Only include properties that are directly about the interface being annotated. For example:
- Properties about dispatch-map reference counting (take_read, release_write, etc.) belong in `idispatch_map.rs`, NOT in `idispatcher.rs`.
- Properties about dispatcher logic (drive index, eviction termination, size validation) belong in `idispatcher.rs`.
- If a dispatcher property depends on a dispatch-map guarantee (e.g., "populate calls downgrade_reference"), reference it briefly but do NOT reproduce the full dispatch-map property list in the dispatcher file.

**Add a header comment block** above the `define_interface!` macro listing verified properties for THIS interface only:

```rust
// # Verified Properties (see `components/<component-name>/verif/`)
//
// The following invariants are formally proved with Creusot:
//
// - P1 (<name>): <one-line description>
// - P2 (<name>): <one-line description>
// ...
```

**Add per-method `# Verified:` comments** on each method that participates in a proven property:

```rust
/// <existing doc comment>
///
/// # Verified: P1 (<name>), P3 (<name>)
/// <brief explanation of what is proved for this method>
fn method_name(...) -> ...;
```

**Add `# Unchecked:` comments** for properties that are NOT yet verified but represent important correctness claims:

```rust
/// <existing doc comment>
///
/// # Unchecked: <property description>
/// <why this matters and what could go wrong if violated>
fn method_name(...) -> ...;
```

**Updating existing annotations:**

If the interface file already has `# Verified:`, `# Unchecked:`, or `# Verified Properties` comment blocks from a prior run:
- **Replace** the header property summary block with the updated list (add new properties, remove properties that no longer apply, update descriptions).
- **Update** per-method `# Verified:` sections — add newly proved properties, remove any that were invalidated by code changes.
- **Promote** `# Unchecked:` to `# Verified:` if the property is now proved.
- **Preserve** `# Unchecked:` entries that are still not covered.
- Do NOT duplicate property annotations — each method should have at most one `# Verified:` section and one `# Unchecked:` section.

**Identifying unchecked properties:**

After annotating verified properties, scan each method for claims that are:
- Stated in doc comments but not formally proved (e.g., "blocks until...", "never returns stale data")
- Concurrency guarantees that the sequential Creusot model cannot capture (e.g., "atomic with respect to...")
- Ordering guarantees (e.g., "entries are returned oldest-first")
- Timeout behavior (e.g., "blocks for at most 100ms")
- Memory safety claims beyond what Rust's type system guarantees (e.g., pointer validity across `unsafe`)

Mark these as `# Unchecked` with a brief note on what verification technique could address them (Spin model, runtime assertion, fuzzing, etc.).

### 9. Commit Annotations on Original Branch

```bash
git add components/interfaces/src/<interface-file>.rs
git commit -m "docs: annotate <interface> with verified and unchecked properties

References Creusot proofs on branch creusot/<component-name>.
N properties verified, M properties identified as unchecked."
```

### 10. Cross-check with Spec Kit Specifications

Read the component's spec kit specifications from `components/<component-name>/.specify/` (look for `specs/*/spec.md`, `spec.md`, or any `.md` files under `.specify/`). Extract requirements, invariants, or behavioral contracts stated in the specifications.

Compare them against the verified (P1–PN) and unchecked (U1–UM) properties:

- **Spec requirements covered by formal proofs** — the requirement is verified.
- **Spec requirements matching an unchecked annotation** — identified but not yet proved.
- **Spec requirements with no corresponding property** — gaps in verification coverage.
- **Verified properties with no corresponding spec requirement** — proofs beyond what was specified.

Present the results as a table to the user:

```
Spec Kit Cross-Check: <component-name>
══════════════════════════════════════

| Spec Requirement                        | Status     | Property  | Notes                          |
|-----------------------------------------|------------|-----------|--------------------------------|
| "release_read fails on zero refs"       | ✔ Verified | P1        |                                |
| "write_ref is binary exclusive"         | ✔ Verified | P4        |                                |
| "shutdown drains background writes"     | ⚠ Unchecked| U2        | Needs Spin model               |
| "entries evicted LRU-first"             | ⚠ Unchecked| —         | Not modeled in Creusot         |
| "max 100ms timeout on blocking ops"     | ✗ No match | —         | Runtime property only           |
| (no spec requirement)                   | + Extra    | P10       | Alignment proof beyond spec    |
```

If the `.specify/` directory does not exist for the component, note this in the report and skip the cross-check.

### 11. Report

```
Creusot Verification Complete: <component-name>
═══════════════════════════════════════════════

Verification branch: creusot/<component-name>
Interface file(s):   components/interfaces/src/<file>.rs

Verified Properties:
  P1: <name> — <description> (N VCs)
  P2: <name> — <description> (N VCs)
  ...

Unchecked Properties (identified for future work):
  U1: <name> — <description> [suggested technique: Spin/fuzzing/etc.]
  U2: <name> — <description>
  ...

Spec Kit Cross-Check:
  [table as above, or "No .specify/ directory found — skipped."]

Total: N properties verified, M unchecked identified
       K verification conditions discharged by SMT solvers
```

### 12. Return to Starting Branch

As the final action, ensure you are back on the branch recorded in step 1:

```bash
git checkout $ORIGINAL_BRANCH
```

Do not commit annotation changes to interface .rs files.

If changes were stashed in step 1, pop them: `git stash pop`

This guarantees the user's working state is restored regardless of which branches were visited during the skill execution.

## Important Notes

- The verification model is a PURE ABSTRACTION of the component logic — it does not import or depend on the actual component crate.
- Creusot proves sequential correctness (no concurrency). Concurrency properties should be marked as `# Unchecked` with a note pointing to Spin models if they exist.
- Always return to the original branch at the end, even if verification fails.
- Use regular `//` comments (not `///` doc comments) for the property summary block above `define_interface!` to avoid the `unused_doc_comments` warning on macro invocations.
- Do not remove existing doc comments — add the `# Verified:` / `# Unchecked:` sections within them.
- The `verif/` directory uses `[workspace]` in its Cargo.toml to be independent of the parent workspace.
