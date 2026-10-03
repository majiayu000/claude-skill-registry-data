---
name: tools-verify-kani
description: Verify a Rust component using Kani model checking — stub unsafe/FFI dependencies, write harnesses targeting arithmetic and state invariants, audit kani::assume calls against production guards, fix gaps, and re-verify.
argument-hint: "[component-path] [interface-path]"
---

## Goal

Formally verify a Rust component using Kani. Kani proves absence of panics,
arithmetic overflows, and invariant violations for **all possible inputs** —
not just sampled ones. The output is either a passing proof or a concrete
counterexample pointing to a real bug.

Work on a dedicated branch (e.g. `kani_harnesses`) so harnesses and fixes can
be reviewed separately from feature work.

---

## The core rule — verify at function granularity, against a spec-derived contract

Before anything else: **the unit of verification is a whole function plus a property
from the spec — never a cherry-picked statement.** Lifting a suspect line and checking
it for overflow/out-of-bounds is *bug-hunting*: it proves a fragment that has no
contract, so a green result only says "this one line does not panic." Instead, for each
target produce three things and label the global `Pn`:

1. **precondition** — `kani::assume(...)` the spec's precondition (mirror the production guard);
2. **function** — **call the real function** (preferred: the proof then tracks shipped
   code). A faithful *whole-function* copy carrying the same contract is acceptable only
   where the crate cannot be built under Kani, and must carry a drift/equality check;
3. **postcondition** — `assert!(...)` the spec's postcondition.

Then **validate the harness by fault injection**: make a change to the function that
violates the contract and confirm the harness *fails*. If it still passes, the harness is
not bound to the real code — fix it. (`--harness` substring-matches; use `--exact` with the
fully-qualified `module::name` to run one harness in isolation.)

The statement scan in Phase 1 is only for *finding candidate functions and their
properties* — not for lifting statements into harnesses.

---

## Phase 1 — Reconnaissance

Before writing a single line of Kani code, read:

1. All source files: `src/lib.rs`, `src/state.rs`, `src/entry.rs`, and any
   submodules.
2. The component's interface file (`components/interfaces/src/ixxx.rs`).
3. `Cargo.toml` — note feature flags, optional deps, and workspace deps.

**Build a target list** — scan for every arithmetic expression that can panic
or wrap:

| Pattern | Risk | Example |
|---|---|---|
| `x += 1` on integer field | Overflow if field reaches MAX | `read_ref += 1` |
| `x -= 1` on integer field | Underflow if field is 0 | `read_ref -= 1` |
| `a * b` before a bounds check | Overflow before guard runs | `block_id * BLOCK_SIZE` |
| `a + b` | Overflow | `offset + BLOCK_SIZE` |
| `x as usize` widening cast | Safe on 64-bit, not on 32-bit | `size as usize * 4096` |
| `buf[i]` inside a loop | Out-of-bounds if bound is wrong | `buf[i] = 1` |

Also note:
- Types with raw pointers or FFI calls → need stubs (Phase 2)
- Component framework macros (`define_component!`) → bypass in harnesses (Phase 3)
- `Mutex` / `Condvar` / `Arc` → test the inner state directly, not through locks

---

## Phase 2 — Stub Unsafe / FFI Dependencies

Kani cannot model raw pointers or calls into C/SPDK FFI. Any type that
contains these must be replaced with a safe equivalent under `#[cfg(kani)]`.

**Rule:** Gate the real implementation with `#[cfg(not(kani))]` and provide a
`#[cfg(kani)]` stub with the **identical public API** but backed by safe Rust.

```rust
// Production struct — raw pointer, FFI deallocator
#[cfg(not(kani))]
pub struct DmaBuffer {
    ptr: *mut std::ffi::c_void,
    len: usize,
    free_fn: unsafe extern "C" fn(*mut std::ffi::c_void),
}

// Kani stub — Vec<u8>, no raw pointers, Drop is a no-op
#[cfg(kani)]
pub struct DmaBuffer {
    data: Vec<u8>,
}
```

Apply `#[cfg(not(kani))]` / `#[cfg(kani)]` to **every** `impl` block for the
type (`Drop`, `Deref`, `DerefMut`, `Debug`, `Send`, `Sync`, method impls).

Stub rules:
- `new(size, ...)` → `vec![0u8; size]`, no FFI calls
- `from_raw(ptr, len, ...)` → `vec![0u8; len]`, ignore the raw pointer
- `as_ptr()` → `self.data.as_ptr() as *mut _` (safe to return, just not deref'd)
- `Drop` → empty body; `Vec` handles deallocation
- Keep `unsafe impl Send` / `unsafe impl Sync` — still needed for `Arc<T>`

**Suppress the lint** in every affected `Cargo.toml`:

```toml
[lints.rust]
unexpected_cfgs = { level = "warn", check-cfg = ['cfg(kani)'] }
```

---

## Phase 3 — Write Harnesses

Place all harnesses in a single `#[cfg(kani)] mod verification` block inside
`src/lib.rs`. This keeps them invisible to `cargo build` and `cargo test`.

```rust
#[cfg(kani)]
mod verification {
    use super::*;
    // access pub(crate) state types directly from here

    #[kani::proof]
    #[kani::unwind(N)]   // N = deepest loop bound + 1
    fn verify_something() { ... }
}
```

### Harness rules

**Use `kani::any()` for every input** — this tells Kani to consider all
possible values, not just a sample.

```rust
let count: u32 = kani::any();
let key: u64 = kani::any();
```

**Use `kani::assume()` only for pre-conditions that production code enforces.**
Every `assume` is a hypothesis — it must be audited in Phase 4.

```rust
kani::assume(count > 0); // only if production code checks count > 0 first
```

**Bypass the component framework.** Do not try to drive `IFoo` through
`define_component!`. Construct the inner state structs (`Inner`, `State`,
`Entry`) directly — they are `pub(crate)` and visible inside `mod verification`.

```rust
let entry = DispatchEntry { read_ref: kani::any(), write_ref: 0, ... };
```

**Avoid heap allocation in harnesses.** `HashMap::new()`, `Vec::new()`,
`String::new()` pull in `__rust_alloc_error_handler` which Kani does not
support. Instead, test invariants directly on struct fields.

```rust
// Bad — HashMap triggers unsupported alloc error handler
let mut map = HashMap::new();
map.insert(key, entry);

// Good — test the guard logic on the struct directly
let active = entry.read_ref > 0 || entry.write_ref > 0;
kani::assert(!active || ..., "...");
```

**Set `#[kani::unwind(N)]` correctly.**
- For a loop with bound `B`: use `N = B + 1`
- For harnesses with no loops: use `N = 1`
- Kani will fail with an unwind error if N is too small

### Standard harnesses to write for any component

| Harness | What to verify |
|---|---|
| `verify_increment_no_overflow` | Every `field += 1` site: `checked_add` returns correct value below MAX, `None` at MAX |
| `verify_decrement_underflow_guarded` | Every `field -= 1` site: safe because production guard `field > 0` exists |
| `verify_multiplication_no_overflow` | Every `a * b` before a bounds check |
| `verify_cast_no_overflow` | Every `x as usize * N` on a 32/64-bit sensitive target |
| `verify_state_invariant` | After a state transition, assert the resulting field values are consistent |
| `verify_removal_requires_zero_refs` | Entry is only removed when all reference counts are zero |
| `verify_symmetric_operation` | e.g. acquire then release leaves state identical to before |

---

## Phase 4 — The Assume Audit (Critical Step)

**After all harnesses pass**, audit every `kani::assume` against the
production code. This is the most important step — a passing harness with
an unmatched assume only proves safety in a restricted universe.

For each `kani::assume(X)` in a harness:

1. Find the corresponding guard in the production code.
2. If the guard exists → the assume is justified. Leave it.
3. If **no guard exists** → the assume is hiding a bug. The production code
   depends on X being true but never checks it. **This is a defect.**

Example of a matched assume (safe):
```rust
// Harness
kani::assume(entry.read_ref > 0);
// Production code — guard IS present
if entry.read_ref == 0 {
    return Err(DispatchMapError::RefCountUnderflow(key));
}
entry.read_ref -= 1;
```

Example of an unmatched assume (bug):
```rust
// Harness
kani::assume(read_ref < u32::MAX);  // assumed, but...
// Production code — NO guard
entry.read_ref += 1;                // bare increment, can overflow at u32::MAX
```

**Symmetric pairs are a strong signal.** If an error enum has `Underflow` but
no `Overflow`, look for increment sites that lack the matching guard.

---

## Phase 5 — Fix and Re-Verify

### Fix pattern for arithmetic overflow

Replace bare arithmetic with `checked_*` operations and propagate via `?`:

```rust
// Before
entry.read_ref += 1;

// After
entry.read_ref = entry
    .read_ref
    .checked_add(1)
    .ok_or(ComponentError::RefCountOverflow(key))?;
```

Apply the same pattern for:
- `checked_mul` — for multiplications before bounds checks
- `checked_add` — for additions (offset + size, etc.)
- `checked_sub` — only if the existing guard can be removed

### Add symmetric error variants

When adding an overflow error, add it to the interface error enum
(e.g. `components/interfaces/src/ixxx.rs`) with a symmetric name:

```rust
/// Reference count underflow (release when already zero).
RefCountUnderflow(CacheKey),
/// Reference count overflow (acquire when already at u32::MAX).
RefCountOverflow(CacheKey),   // ← add this
```

Add the matching `Display` arm.

### Tighten the harnesses after fixing

Remove `kani::assume` calls that were masking the bug. The harness should
now verify the full range including the previously-hidden edge case:

```rust
// Before fix — assume hid the overflow
kani::assume(read_ref < u32::MAX);
entry.read_ref += 1;

// After fix — no assume needed; checked_add handles all u32 values
let result = entry.read_ref.checked_add(1);
if let Some(r) = result {
    kani::assert(r == entry.read_ref + 1, "...");
} else {
    kani::assert(entry.read_ref == u32::MAX, "overflow only at MAX");
}
```

### Re-run and confirm

```sh
cargo kani --manifest-path components/<name>/vN/Cargo.toml
```

Target: `0 of N failed`, all harnesses in `Manual Harness Summary` show success.

---

## Phase 6 — Document and Commit

Create `VERIFICATION.md` in the component directory covering:
- Component overview and what was verified
- The stub approach (if FFI types were involved)
- Each harness and what it proves
- Bugs found (file, line, expression)
- Fixes applied
- Final verification output

Commit on the `kani_harnesses` branch:

```
git add components/<name>/... components/interfaces/...
git commit -m "Add Kani harnesses for <component>; fix <N> arithmetic gaps"
```

---

## Common Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| `HashMap` / `Vec` in harness | `__rust_alloc_error_handler not supported` | Test struct fields directly |
| `define_component!` wrapper | Complex macro expansion confuses Kani | Construct inner state structs directly |
| `#[cfg(feature = "X")]` gate | Kani sees wrong version of a type | Check `Cargo.toml` features; pass `--features X` to `cargo kani` |
| Unwind too low | `unwinding assertion failure` | Increase `#[kani::unwind(N)]` by 1 and retry |
| `kani::assume` not audited | Harness passes but bug still present | Do Phase 4 audit before declaring success |
| Stub missing an `impl` block | Compile error under `cargo kani` | Add `#[cfg(kani)]` version of every `impl` for the stubbed type |
| `write_ref` vs `read_ref` risk | `write_ref` is assign (0/1), not increment — lower risk | Focus overflow checks on fields that are genuinely incremented |

---

## Quick Reference

```sh
# Run all harnesses in a component
cargo kani --manifest-path components/<name>/vN/Cargo.toml

# Run a single harness
cargo kani --manifest-path components/<name>/vN/Cargo.toml \
  --harness verification::<harness_name>

# Run with a specific feature enabled
cargo kani --manifest-path components/<name>/vN/Cargo.toml \
  --features spdk
```
