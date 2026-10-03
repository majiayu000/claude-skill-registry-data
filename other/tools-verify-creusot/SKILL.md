---
name: tools-verify-creusot
description: Identify what to verify in real-world Rust code, extract the pure core, and drive it to a full Creusot proof
argument-hint: <target>  (e.g. "entry ref-counting in dispatch-map" or "segment_io in io_segmenter.rs")
---

This skill guides you from a real codebase function to a Creusot proof.
The key shift from naive Creusot use: **don't ask "is this function pure?" — ask "what invariant must always hold, and can I prove it?"**

**Two things that keep the proof honest** (this skill extracts a *copy* of shipped code):

- **Function granularity + a spec-derived contract is the unit.** Extract a *whole
  function* and prove a spec property with `#[requires]`/`#[ensures]`, never a lifted
  statement. That is what makes the proof both *meaningful* and *fault-injection-testable*.
- **Mind the drift.** Because the dispatcher and friends can't be built under Creusot,
  this skill proves a standalone **mirror**, not the shipped function. Keep the body
  byte-faithful to the source, add a drift/equality check against it, and **validate by
  fault injection**: inject a contract-violating change into the mirror and confirm a VC
  goes red (`✘`). If it stays `Proved ✔`, the contract is vacuous — strengthen it. (Injecting
  into the *shipped* function will NOT fail this proof — that residual gap is the drift the
  equality check guards.)

---

## The two levels where Creusot adds value

Most production Rust mixes two kinds of logic:

| Level | What it is | Example in this codebase |
|---|---|---|
| **Arithmetic** | Numeric calculations — bounds, overflow, coverage | `segment_io()`: every byte covered, no LBA overflow |
| **Protocol / state machine** | Rules about data structure state — what transitions are legal, what must always be true | `dispatch-map`: `write_ref` is always 0 or 1; refs never underflow |

Creusot can prove both. The arithmetic level is found in pure functions. The protocol level is hidden inside impure functions — wrapped in Mutex, HashMap, async — but the core logic is still provable once extracted.

---

## Step 0 — Find what to verify: the invariant-first approach

### For arithmetic targets (easier)

Look for functions that are already pure or nearly pure:
- Offset/size calculations, segmentation, alignment math
- No Mutex, no HashMap, no async, no FFI in the function body
- `segment_io()` is the canonical example: given total_bytes, produce a Vec of segments

Good signals: `-> Vec<T>`, arithmetic on `usize`/`u64`, loops with counters.

### For protocol targets (richer)

Look for data structures with **reference counts, state flags, or lifecycle enums**, then ask:

> *"What must always be true about this struct's fields, regardless of which operation ran?"*

That question gives you the **invariant**. Once you have the invariant, you can prove it holds:
- Before and after each individual operation
- Across entire sequences of operations (lifecycle proofs)

**Signals that a protocol target exists:**
- `checked_add` / `checked_sub` on ref-count fields — overflow protection hiding a safety property
- `match entry.location { Staging | BlockDevice | MemoryTier }` — a state machine
- Guards like `if entry.write_ref > 0 { return Err(...) }` — preconditions in disguise
- Multiple functions that all touch the same struct fields

**The dispatch-map example:**
- Invariant discovered: `write_ref` is always 0 or 1 (`inv_write_binary`)
- Secondary invariant: removability requires zero refs (`no_active_refs`)
- Functions proved: `take_read`, `take_write`, `release_read`, `release_write`, `downgrade_reference`, `check_removable`, `convert_to_storage`, `convert_memory_tier_to_block`, `is_evictable`
- Lifecycle sequences proved: staging→read path, downgrade path, staging→block path

---

## Step 1 — Extract the pure core

Production functions that maintain invariants usually look like:

```rust
pub async fn take_read(&self, key: ...) -> Result<(), Error> {
    let map = self.map.lock().unwrap();          // ← Mutex
    let entry = map.get_mut(&key).unwrap();      // ← HashMap
    self.wait_for(|e| e.write_ref == 0).await;  // ← condvar / async
    entry.read_ref = entry.read_ref              // ← THE ACTUAL LOGIC
        .checked_add(1)
        .ok_or(Error::RefCountOverflow)?;
    Ok(())
}
```

The verifiable core is only the last four lines. Extract it like this:

**Three substitutions:**

| Production code | Verification crate |
|---|---|
| `self.map.lock().get_mut(&key)` | `entry: &mut DispatchEntry` (passed directly) |
| `wait_for(guard)` | `#[requires(guard_condition)]` precondition |
| `Arc<DmaBuffer>` / `*mut u8` | `u64` opaque handle |

**What the substitutions mean logically:**
- Passing `&mut Entry` directly means: "we already have the lock and the entry — prove what happens next"
- `#[requires(write_ref == 0)]` means: "the condvar wait already guaranteed this — now prove the body is correct under that assumption"
- Opaque `u64` handles mean: "we don't care what the buffer contains — we only care about the state machine transitions"

---

## Step 2 — Create the standalone verification crate

Structure:
```
components/<name>/verif/          ← co-locate with the component
├── Cargo.toml
├── why3find.json
└── src/lib.rs
```

`Cargo.toml`:
```toml
[package]
name = "<name>-verif"
version = "0.1.0"
edition = "2021"
publish = false

[dependencies]
creusot-std = { path = "../../tools/creusot/creusot/creusot-std" }

[workspace]
```

`why3find.json`:
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

`src/lib.rs` — start with the types, then logical predicates, then functions:

```rust
use creusot_std::prelude::*;

// --- Types (strip hardware pointers, keep structure) ---

pub enum Location {
    Staging    { buffer_handle: u64 },  // Arc<DmaBuffer> → u64
    BlockDevice { offset: u64 },
    MemoryTier { mem_handle: u64, size: u32, ssd_offset: Option<u64> },
}

pub struct DispatchEntry {
    pub location:    Location,
    pub size_blocks: u32,
    pub read_ref:    u32,
    pub write_ref:   u32,
    pub tsc:         u64,
}

// --- Logical predicates (the invariants you want to maintain) ---

#[logic]
pub fn inv_write_binary(e: &DispatchEntry) -> bool {
    pearlite! { e.write_ref == 0u32 || e.write_ref == 1u32 }
}

#[logic]
pub fn no_active_refs(e: &DispatchEntry) -> bool {
    pearlite! { e.read_ref == 0u32 && e.write_ref == 0u32 }
}

// --- Functions: requires = what the guard ensured, ensures = what we prove ---

#[requires((*entry).write_ref == 0u32)]          // condvar wait ensured this
#[requires((*entry).read_ref@ < u32::MAX@)]      // overflow precondition
#[requires(inv_write_binary(entry))]
#[ensures((^entry).read_ref == (*entry).read_ref + 1u32)]
#[ensures(inv_write_binary(&^entry))]
pub fn take_read(entry: &mut DispatchEntry) -> Result<(), DispatchMapError> {
    entry.read_ref = match entry.read_ref.checked_add(1) {
        Some(v) => v,
        None    => return Err(DispatchMapError::RefCountOverflow),
    };
    Ok(())
}
```

---

## Step 3 — Write lifecycle proofs

After proving individual operations, prove that **sequences** maintain invariants.
A lifecycle proof is a plain function that calls operations in order and has postconditions on the final state.

```rust
/// Proves: create → release_write → take_read → release_read ends removable.
#[ensures(no_active_refs(&result))]
#[ensures(inv_write_binary(&result))]
pub fn lifecycle_staging_read() -> DispatchEntry {
    let mut e = DispatchEntry { ..., write_ref: 1, ... };
    let _ = release_write(&mut e);
    let _ = take_read(&mut e);
    let _ = release_read(&mut e);
    e
}
```

Write one lifecycle proof per valid path through the state machine.
These are the highest-value proofs: they show the whole protocol is correct, not just individual steps.

---

## Step 4 — Syntax check and full proof

Fast syntax check (no SMT solvers):
```bash
cargo creusot --only coma
```

Full proof:
```bash
cargo creusot
```

Expected output when all VCs discharge:
```
Proved (verif/<crate>_rlib/<function>.coma) ✔
```

---

## Step 5 — Arithmetic annotation patterns

For arithmetic targets (loops with counters, segmentation math):

```rust
#[requires(max_size@ > 0)]
#[requires(start_lba@ + total_bytes@ / sector_size@ <= u64::MAX@)]  // overflow pre
#[ensures(total_bytes@ == 0 ==> result@.len() == 0)]
#[ensures(total_bytes@ > 0  ==> result@.len() > 0)]
pub fn segment_io(total_bytes: usize, ...) -> Vec<Segment> {
    #[invariant(offset@ + remaining@ == total_bytes@)]  // coverage
    #[invariant(offset@ > 0 ==> segments@.len() > 0)]  // growth
    #[invariant(lba@ <= start_lba@ + offset@ / ss@)]   // LBA bound
    #[variant(remaining)]                                // termination
    while remaining > 0 { ... }
}
```

### When the prover gets stuck — `proof_assert!`

Creusot does NOT carry preconditions through `as` casts automatically:
```rust
let mts = max_size as usize;
proof_assert!(mts@ > 0);   // bridge: tells prover mts > 0 is still true after cast
```

Use `proof_assert!` whenever a fact the prover "should know" isn't reaching a later goal.

---

## Quick reference: annotation cheatsheet

```rust
use creusot_std::prelude::*;

// Logical predicate (specification helper, not runtime code)
#[logic]
fn my_invariant(e: &MyStruct) -> bool { pearlite! { e.field > 0u32 } }

// Function-level
#[requires(x@ > 0)]                              // precondition
#[requires(a@ + b@ <= usize::MAX@)]              // overflow-safe precondition
#[ensures(result@ == x@ * 2)]                   // postcondition on return
#[ensures(inv_write_binary(&^entry))]            // invariant preserved on &mut
#[ensures(no_active_refs(&result))]              // state postcondition

// Loop-level (place just before the while)
#[invariant(offset@ + remaining@ == total@)]     // coverage
#[invariant(remaining@ <= total@)]               // monotone bound
#[invariant(ptr@ > 0 ==> vec@.len() > 0)]       // growth
#[variant(remaining)]                             // termination

// Mid-proof bridge
proof_assert!(x@ > 0);                           // assert a fact for subsequent goals
```

**The `@` operator:** maps Rust values to mathematical integers. Always use `@` in spec
expressions. Casts (`as usize`) do NOT propagate `@` facts — bridge with `proof_assert!`.

**`*entry` vs `^entry`:** in postconditions on `&mut T`, `*entry` is the value on entry
(old), `^entry` is the value on exit (new).

---

## Common mistakes

| Mistake | Fix |
|---|---|
| Copying an impure function as-is | Extract the pure core; replace Mutex/HashMap/async with parameters and `#[requires]` |
| Writing `#[requires]` but forgetting what the guard ensured | Ask: "what condition did the caller's wait/check guarantee?" — that's your precondition |
| Forgetting `proof_assert!` after `as` casts | Add immediately after every `let x = y as T` that matters |
| Lifecycle proof fails while individual ops pass | The ops' postconditions don't chain — add intermediate `proof_assert!` calls |
| `Clone` ambiguous | Remove `#[derive(Clone)]` from structs in the verif crate |
| `[workspace]` missing | Add empty `[workspace]` to standalone `Cargo.toml` |
