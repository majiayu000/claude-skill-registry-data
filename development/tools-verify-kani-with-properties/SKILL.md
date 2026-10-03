---
name: tools-verify-kani-with-properties
description: Create Kani harnesses for a Certus component from BOTH its spec and its Rust code — at function granularity, calling the real function under spec-derived pre/postconditions — run them, and record what was verified (with evidence) by writing each property's status/symbol/fidelity/evidence into the shared `unified_properties.yaml` under its `kani:` block. Attempt every property you can express as a harness — do not pre-filter by lane, effort, or difficulty. Use for the normal verify-and-document workflow (not the blind property-extraction experiment).
argument-hint: "[component-path] [interface-path]"
---

## Goal
Verify a component with Kani **and** record exactly what was verified.
Inputs are the component's **spec** (the intended behavior) and its **Rust code** (functions +
interface). Outputs are (1) the `#[cfg(kani)] mod verification` harnesses and (2) the per-property
status/symbol/fidelity/evidence written back into the shared `unified_properties.yaml` under each
property's `kani:` block.

This skill = **`tools-verify-kani` + explicit spec pairing + a status-write-back step.** Use
`tools-verify-kani` for the create mechanics (stub unsafe/FFI, `kani::assume` mirroring production
guards, run/fix, its "core rule"). This skill adds spec-derived contracts and the structured
write-back into `unified_properties.yaml`.

## Steps
0. **Environment — confirm the toolchain FIRST (mandatory).** Confirm `cargo kani` is reachable and run
   from the **component directory**, not the workspace root — the root triggers a spurious `gpu-services`
   feature error that is an environment artifact, never a property verdict. A missing/erroring toolchain is
   a **blocker to fix or escalate here**, never a `tool-boundary` and never a reason to leave a property unattempted:
   ```bash
   command -v cargo-kani >/dev/null || { echo "FATAL: cargo-kani unreachable — escalate to user"; exit 1; }
   cargo kani --version    # expect a version line, not an error
   cd components/<name>    # run all `cargo kani` from HERE, not the workspace root
   ```
1. **Resolve inputs — consume the inventory, do NOT re-extract.** Load the **property inventory**
   `verif/unified_properties.yaml` (Role 1, `build-property-inventory`): the agreed, id-keyed,
   tool-independent property set. Also open the Rust functions + interface (`src/**`, `interfaces/`); use
   the spec only for an obligation's wording, never to mint a new one. **Do not build a private per-tool
   property list.** If the inventory is missing, stop and run `build-property-inventory` first. If you
   spot a real obligation the inventory lacks, **flag it back** to the inventory so it gets an `id`.
2. **Harness the shared/global invariants FIRST, once — then reuse.** Before per-method work, take the
   inventory properties whose bundle spans multiple methods (the inventory marks these as global /
   maintained invariants with an attachment count). **Order by attachment count, highest first.** Prove
   each as a **single inductive harness**: build a symbolic valid state, `kani::assume(inv(state))`, call
   the mutator, `assert!(inv(state'))` — plus one establishment harness (`initialize` from scratch →
   `assert!(inv)`). Record it under its **one** inventory `id`; its status then propagates to every bundle
   automatically (Role 3 attaches by id — do NOT re-harness it per method, and do NOT skip it because "no
   single method owns it"). One cheap invariant harness unblocks every method in its bundle at once.
3. **Then, for each remaining per-method obligation, harness the CODE against it.** Function granularity,
   using the obligation from its inventory row (`id`, `statement`, `kind`):
   `kani::assume(<precondition — mirror the production guard>)` → **call the real function** →
   `assert!(<postcondition>)`, taking the already-proved invariants as assumed pre-state. Never lift a
   statement into the harness.
4. **Run.** `cargo kani` to green; fix gaps; **audit** that each `assume` matches a real production
   guard (no over-assuming that would make the proof vacuous).
5. **Validate (anti-vacuity).** Fault-inject (a contract-violating change) and confirm the harness
   **FAILS**; if it still passes, it isn't bound to the real code — fix it. Then revert. For a maintained
   invariant, also fault-inject a mutator that breaks it and confirm the inductive harness FAILS.
   (`--harness` substring-matches; use `--exact` with `module::name` to run one in isolation.)
6. **Produce artifacts the scorer can reproduce — you do NOT write your own status.** The verdict is
   assigned in Step 7 by the shipped scorer, which *runs* your harnesses. Your job in Step 6 is to leave,
   for every property, a runnable artifact named so the scorer finds it:
   - **One harness per property `id`**, named `verify_<id>` (id lowercased, `-`→`_`). If a single
     descriptive harness covers a property, point the scorer at it with `kani.evidence.harness: <name>`
     instead — but it must exist and pass on its own.
   - **For any property you cannot prove on the first clean attempt, build the lever-battery variants**
     that `gate/lever_battery_kani.yaml` requires for the failure class you hit — as *named runnable
     harnesses*: `verify_<id>__nounwindcheck`, `verify_<id>__concrete`, `verify_<id>__split_*`,
     `verify_<id>__stub`. A tool-boundary is **inadmissible** until every required variant exists and the
     scorer has run each — a missing variant scores UNRESOLVED (gate fails), not tool-boundary.
   - **An anti-vacuity twin** `verify_<id>__mutant` wherever the property could pass vacuously — a
     deliberately contract-violating copy that the scorer requires to FAIL.
   - In `unified_properties.yaml` under the `kani:` block you may fill **only the advisory fields the
     scorer does not own**: `fidelity` (`real-type-bounded | representative | arithmetic-core |
     bounded-shallow`) and a human `note`; and for a genuine cross-*component* delegation, a resolvable
     `delegate_to:` (named component + concrete obligation). **Do NOT write `status`, `symbol`, or
     `evidence`** — the scorer overwrites them from the live run and stamps `_scored_by: scorer_kani`.
     Anything you type there is discarded; the only way to move a property's status is to make its
     artifact reproduce.
   `fidelity` meanings: `real-type-bounded` = real product type/code under a stated `#[kani::unwind(N)]`
   (a bounded proof is a real proof); `representative` = the ∀ shrunk to one symbolic representative;
   `arithmetic-core` = an extracted arithmetic core behind a stub (`★`); `bounded-shallow` = a pass under
   `--no-unwinding-checks` at low unwind — every loop *cut* at N, sound only for executions where each
   loop runs ≤N (disclose the cut in `note`; route a fully-sound proof of the same obligation to Creusot).
7. **Gate — the shipped scorer decides, by reproduction (mandatory; you cannot grade yourself).** The
   reproduction gate is `scorer_kani.py`, which the `component-verify` orchestrator runs in its Step 2.5.
   If you are running this skill standalone, invoke it yourself before returning and paste its output into
   your report:
   ```bash
   python3 "$(git rev-parse --show-toplevel)/.claude/skills/component-verify/gate/scorer_kani.py" \
       components/<name>/verif --component-dir components/<name> --cap-seconds <cap>
   ```
   The scorer *executes* each `verify_<id>` harness (rebuilding from source, so a hand-edited artifact
   cannot fake a pass), captures wall-clock + peak RSS **from the run**, checks the anti-vacuity mutant,
   and writes the scorer-owned `status`/`evidence`/`note`/`_scored_by`. It assigns `proved` /
   `tool-boundary` (only after the full lever battery ran and the residual signature is not a known defeat)
   / `delegated` (resolvable referent) / **UNRESOLVED** (no harness, an unreproducible pass, a missing
   required lever variant, a known-defeat signature, or a broken harness) — and **exits non-zero if any
   verifiable property is UNRESOLVED.** If it exits non-zero you are **not done**: for each UNRESOLVED
   `id`, produce the missing harness / the demanded lever variant / fix the broken harness, and re-run the
   scorer. Iterate until it exits 0. You may not hand back the run, write a "partial run" summary, or ask
   the user to accept the remainder while the scorer fails — no matter how many properties are proved.
   Editing the YAML to say `proved` does nothing: the scorer reproduces from source and overwrites it.

## Coverage discipline (mandatory)
**Attempt every property in the inventory that you can express as a harness. You do not get to pick
lanes here** — routing properties across tools is a separate step, not this one. Your job is to verify or
fail *trying*, and to record the outcome **keyed to the inventory `id`** so Role 3 can aggregate it.
- **No pre-filtering by lane, effort, or budget.** "Better suited to Creusot", "intractable", "requires
  induction", "to stay within budget" are **not** acceptable reasons to omit a property. If you can write
  the harness, run it.
- **Attack the highest-leverage properties first.** A property in many bundles is *higher* priority, not
  lower, because one inductive harness discharges it everywhere. Harness the shared/global invariants
  (ordered by attachment count) before method-specific obligations; a cheap invariant left at `not_yet`
  silently keeps every method in its bundle unproved.
- **Attempt at a tractable bounded geometry.** Kani proves exhaustively *at the chosen size*: pick a small
  `#[kani::unwind(N)]` and a small structure that still exercises the property, and use `kani::stub` to
  replace unsupported/FFI dependencies rather than dropping the harness. A bounded proof is a real proof —
  report its geometry.
- **Bounded effort, not infinite grind.** Give each harness a real attempt against a stated cap (per-harness
  CBMC timeout). Exceeding the cap converts the property to a **`tool-boundary` with the timeout signature**
  (`miss_class: TOOL`, `note:` the exact `>N min at unwind=K` string) — it does **not** license leaving the
  property unattempted. The cap decides *when the captured signature is ready for the scorer*, never *whether you may skip*.
- **Every non-success carries a reproducible signature**, never a subjective verdict: `VERIFICATION FAILED`,
  an unwinding-assertion failure (N too small), `unsupported_construct: <name>` (e.g. `_xgetbv` from
  `crc32fast`), or a SAT/solver timeout (`>N min at unwind=K`). Ban bare "intractable"/"out of scope".
- **Only two legitimate non-proofs**, each needing a one-line technical reason and a suggested route:
  (a) **Not expressible for a bounded checker** — concurrency interleavings, liveness/timing, or a property
  that only holds at unbounded scale and no finite geometry witnesses it;
  (b) **Depends on effects Kani cannot model** — real I/O, hardware, FFI (and no stub is faithful).
  Everything else must be attempted at a bounded geometry and reported with its signature under bucket (a).
- **Concrete string/char CONTENT is EXPRESSIBLE here — prove it, do not claim a boundary.** A property
  Creusot cannot state because its string view is opaque (contains a tag, equals `"ERROR"`, ends in `'\n'`,
  excludes an ESC byte, or is built by `format!`) is exactly what a bounded checker CAN witness on the
  concrete bytes. When `unified_properties.yaml` shows such a property with `creusot.claims_inexpressible`
  and `covered_by: kani`, that is **your obligation to discharge bounded** (small symbolic representative,
  real type), not to punt. There is **no inexpressibility hatch for Kani** in this pipeline — bounded byte
  reasoning is Kani's home turf, so a Kani inexpressibility claim on strings is illegitimate.

## Coverage-extending levers — exhaust these BEFORE recording ⊘ (mandatory)
A "tool boundary" is only legitimate after the applicable levers below have been *tried and shown to
fail with a captured signature*. A wall that a documented lever clears is a **recipe gap, not a tool
boundary** — recording ⊘ without trying the lever is a false negative (this is exactly how a
HashMap-backed component was once mis-recorded as whole-component ⊘ when a one-line stub proved it in
3.5 s). Enable unstable levers with the matching `-Z` flag: `cargo kani -Z stubbing`,
`-Z function-contracts`, `-Z loop-contracts`.

- **HashMap / HashSet construction wall (`RandomState::new` → `getrandom` → `syscall`).** This is
  DEFEATABLE, not a boundary. Stub `RandomState::new` with a deterministic seed and construct the real
  type in situ:
  ```rust
  use std::collections::hash_map::RandomState;
  use std::mem::{size_of, size_of_val, transmute};
  fn concrete_state() -> RandomState {
      let keys: [u64; 2] = [0, 0];
      assert_eq!(size_of_val(&keys), size_of::<RandomState>());
      unsafe { transmute(keys) }              // fixed [0,0] seed, no syscall
  }
  #[kani::proof]
  #[kani::stub(RandomState::new, concrete_state)]   // also covers the Default path
  #[kani::unwind(5)] #[kani::solver(minisat)]
  fn harness() { /* build + drive the real HashMap-backed struct */ }
  ```
  Fidelity `real-type-bounded` (the real product type, in situ; symbol `✓`). Two measured caveats:
  (a) **use concrete representative keys** — symbolic keys (`kani::any()`) drive SipHash over symbolic
  bytes and blow up hashbrown's probe loop (record such a harness as `representative` fidelity, not a
  boundary); (b) the seed stub is sound only for map *semantics* (insert/get/remove/len/containment) —
  never assert anything depending on hasher randomness (iteration order, DoS-resistance) under it.
- **`extern "C"` / FFI in the path.** `#[kani::stub(the_extern_fn, rust_model)]` replaces the foreign fn
  with a Rust model (symbol `★`, disclosed in `note`). Or give it a contract and `#[kani::stub_verified]`
  (`-Z function-contracts`). Only ⊘ if no faithful model exists.
- **Unbounded loop.** Prefer `#[kani::loop_invariant(..)]` (+ `#[kani::loop_decreases(..)]`,
  `-Z loop-contracts`) over an ever-growing `#[kani::unwind]` — an inductive invariant removes the bound.
  (Not `while let` loops; decreases is integer-only.)
- **Large / slow formula.** Switch `#[kani::solver(minisat|kissat|cadical|z3)]` (minisat cleared the
  hashbrown `swap_nonoverlapping` loop here); bound symbolic state with `kani::assume`; decompose a huge
  function via `#[kani::proof_for_contract]` + `#[kani::stub_verified]` so callers assume the verified
  contract instead of inlining the body.
- **Sweep the unwind number — and use `--no-unwinding-checks` for shallow coverage (the coverage-over-depth
  lever).** A single fixed unwind is a trap: too low raises a spurious `unwinding assertion loop N` FAILED
  (not a real defect — just "the bound is below the loop"), too high explodes the SAT formula into a
  timeout. **Iterate the bound** — try `--unwind 2,3,4,5,…` (cheapest first) and take the smallest that
  reaches the property without an unwinding failure; record the winning `N` in `evidence.unwind`. When the
  loop genuinely needs many iterations to *terminate* (e.g. hashbrown's probe loop) and the sound geometry
  times out, add **`--no-unwinding-checks`**: Kani then *cuts* every loop at the unwind bound and verifies
  the bounded prefix, turning a >500 s timeout into a ~7 s pass (measured ~70× on the ≥2-`HashMap`-mutation
  harnesses here — unwind 5 timed out >500 s under minisat **and** cadical; unwind 2 + `--no-unwinding-checks`
  passed in ~7 s / ~355 MB). **Soundness cost — record it honestly:** this is `bounded-shallow` fidelity
  (symbol `✓`, but the `note` must state "loops cut at N; sound only for executions where every loop runs
  ≤N times; deeper iterations out of scope"). It is *coverage over depth*: it lets you sweep many functions
  cheaply and confirm the shallow slice, but it is **not** a full proof — route a fully-sound proof of the
  same obligation to Creusot (FMap induction removes the bound entirely). Prefer real levers (loop
  contracts, solver switch, smaller symbolic state) when they fit in budget; reach for `--no-unwinding-checks`
  to *widen* coverage across source, not to *replace* a sound proof where one is affordable.
- **Reference:** `verif/skills_research/KANI_capability_catalog.md` in the eviction-policy-session-lists
  component carries the full catalog with flags, examples, and soundness costs.

## Harness hygiene the GATE depends on — measured, not theoretical (mandatory)

### 🔴 Do NOT generate harnesses with `macro_rules!` — the gate cannot see them
`find_harness_names` discovers harnesses by **regex over source text**. A harness emitted from a
macro is invisible to it, so the property scores "no runnable harness" while the harness sits in the
file — blaming you for a discovery limitation. Measured: 13 global-invariant harnesses written via
`macro_rules!` would all have scored that way. Write explicit `#[kani::proof] fn verify_<id>()`
functions, however repetitive.

### 🥇 LOOP CONTRACTS FIRST — the correct answer to a loop that will not fit a bound
`-Z loop-contracts` replaces unrolling with a Floyd–Hoare invariant, so **the loop body executes
exactly twice** and verification cost is decoupled from the iteration count. This is available in
cargo-kani 0.67.0 (checked: `-Z` accepts `loop-contracts`, `function-contracts`, `quantifiers`,
`ghost-state`, `mem-predicates`, `uninit-checks`, `valid-value-checks`).

**Measured, on a 1024-iteration loop that mirrors a real component's `halve()`:**

| approach | base harness | its mutant (MUST fail) | time | sound? |
|---|---|---|---|---|
| `--unwind 4 --no-unwinding-checks` | SUCCESSFUL | **SUCCESSFUL** | 0.034 s | **NO — vacuous** |
| `-Z loop-contracts`, no bound at all | SUCCESSFUL | **FAILED** ✓ | 0.20 s | **YES** |

Read that table before reaching for `--no-unwinding-checks` again. The bounded version "verified" in
34 ms **and so did a harness asserting the exact opposite**, because a 4-iteration bound over a
4096-iteration loop prunes away every path the obligation is about. The loop-contract version costs
6× more and is worth infinitely more: it holds for all iteration counts, and its mutant correctly
fails. Kani's own tool paper puts the same contrast at 0.2 s with a contract versus 91.8 s unrolling
19 iterations.

```rust
#![cfg_attr(kani, feature(stmt_expr_attributes, proc_macro_hygiene))]
let mut i = 0usize;
#[kani::loop_invariant(i <= COLS && (i == 0 || c[0] <= 127))]
while i < COLS { c[i] >>= 1; i += 1; }
```
Run with `-Z loop-contracts`. Companions: `#[kani::loop_modifies(...)]` when the inferred write set is
wrong, and `#[kani::loop_decreases(expr)]` for termination.

**Limitations you WILL hit, so design around them:**
- **An invariant that is not INDUCTIVE fails even though it is true.** This is the trap, and it looks
  exactly like a tool bug. CBMC havocs the loop's write set, so the invariant must be re-establishable
  from itself plus the body — not merely true of the final state. Measured: `a[0] <= 127` after
  `a[i] >>= 1` is inductive for `u8` (halving can never exceed 127) but NOT for `u64`, and the `u64`
  version fails while being perfectly true.
  An earlier version of this section blamed **kani #3168** (struct field projections) for that failure.
  **That was a misdiagnosis and #3168 does NOT reproduce on 0.67.0** — invariants over a struct field
  (`s.a[0]`), a `&mut` array parameter, a by-value array parameter and a harness-body local all prove.
  So do **not** hoist state out of structs to appease the tool; check inductiveness first. When an
  invariant fails, ask "could the body break this from a state satisfying it?" before suspecting Kani.
- Loop contracts do **not** havoc state the loop only reads, so a read-only scan over an
  assumed-well-formed structure needs no `loop_modifies`.
- `while let` loops are unsupported. `while` and `loop` work; `for` works over ranges, slices, Vec,
  Iter and the common adaptors.
- **Without `loop_decreases` you get PARTIAL correctness** — "if the loop terminates, the result is
  correct". Kani's docs show an infinite `while true` whose post-loop assertion is reported *proved*.
  So an invariant alone does not rule out non-termination; add a decreases measure when that matters,
  and record fidelity accordingly.
- `loop_decreases` takes **integer** expressions only, no lexicographic tuples, no field projections,
  and it conflicts with `loop_modifies` in this version.
- The invariant and the decreases expression must be **pure**; side effects there are unchecked and
  "could lead to an unsound proof result".
- Diagnosing: establishment fails → invariant too strong for the initial state; preservation fails →
  too weak to prove itself, or too strong for the body; post-loop assertion fails → invariant plus
  `!guard` is not enough.

### 🔴🔴 `kani::forall!` SILENTLY DROPS a body containing `&&` — the worst trap found so far
Under `-Z quantifiers`, measured shape by shape on 0.67.0:

| body | binds? |
|---|---|
| `a[i] == 42` · `b[i]` · `b[i] == c[i]` · `a[i] <= d[i]` · `a[i] != s` | ✓ |
| `(b[i]==false) \|\| (a[i]==42)` · 3-way `\|\|` over struct fields | ✓ |
| **`(b[i]==true) && (a[i]==42)`** | **SILENTLY IGNORED** |

The assume compiles, runs, and **constrains nothing**. Also silently ignored: a **symbolic** upper
bound (only constant bounds bind). Related: `\|i: T in ..\|` is a parse error, and a body indexing
through a reference can fail type inference — wrap it in `fn pred(p: &Pool, i: usize) -> bool`.

**Know which direction is dangerous.** A dropped `forall!` inside an **assume** only weakens the
precondition, so the proof gets harder and never vacuous. A dropped conjunct inside an **assertion**
or a **loop invariant** is straight vacuity, and **no tool flags it** — not Kani, not our mutant twins
necessarily, because the mutant may be dropped the same way.

**Rules, mandatory wherever `-Z quantifiers` is used:**
1. **Never put `&&` inside `forall!`.** One `forall!` per conjunct.
2. Only constant upper bounds.
3. **Carry a `check_assumes_actually_bind` harness** that re-asserts every assumed predicate at a
   symbolic index. If an assume silently dropped, that harness fails and tells you so. This is cheap
   (measured 5.08 s) and it is the only mechanism that catches the failure at all.

### 🔴 A STUB CAN BLIND THE CODE — a vacuity source no mutant twin catches
Stubbing a container to make a harness affordable can silently remove the behaviour under test, and
then **the property AND its mutant both pass.** Proved, not theorised: with `BTreeSet` stubbed on
`eviction-policy-session-lists`, a diagnostic harness asserting
`p.leaves.len() == 2 && p.evict_oldest().is_none()` **PASSES** — the model holds two leaves while the
operation that selects a victim returns `None`, because the read path (`leaves.iter().next()`) was
never intercepted.

Every obligation phrased as an **implication over a returned value** ("if a victim is returned it is a
leaf", "a protected block is never chosen") is then vacuously true, and its mutant is vacuous for the
same reason, so anti-vacuity cannot see it. **Applied carelessly, stubbing is worse than the bounded
harnesses it replaces.**

**Required whenever you stub:** a diagnostic harness asserting the stubbed path is still REACHED and
still returns something — the analogue of `check_assumes_actually_bind`. If the operation can return
"nothing" while the state says otherwise, every downstream implication is worthless.

Also know what Kani will and will not let you stub, measured on 0.67.0:
- A stub must repeat the target's generics **exactly**; a monomorphised stub is rejected
  ("mismatch in the number of generic parameters"). So a stub **cannot own typed state**, which forces
  a type-erased side table if you need per-instance state.
- **External-crate trait impls cannot be stubbed at all**: `btree_set::Iter::next` → "unable to find
  `next` inside struct"; `<Iter<'_,T> as Iterator>::next` → "unable to find implementation of
  associated function". So any obligation whose only read path is an iterator is out by construction.
- Per-instance stub state keyed on the receiver address works, but **a Rust move relocates the struct
  and orphans the table** — so the object must be built in place and never moved. A
  `Vec<Mutex<Pool>>` therefore cannot use the technique at all.

### The CAPACITY-SCALING check — a second, independent test that a proof is real
The mutant twin catches a proof with no content. It does **not** catch a proof whose bound merely
happened to be generous enough for the states the harness explores. So for any harness over a
fixed-capacity structure, **re-run it at a larger capacity and require every verdict to hold.**

Measured on a 474-line Pool model, 7 harnesses, capacity 8 → 32 (a 4× arena), same source, same flags:

| | CAP=8 | CAP=32 |
|---|---|---|
| 3 base proofs | 19.1 / 25.6 / 23.9 s, all SUCCESSFUL | 139.7 / 130.9 / 74.0 s, **all still SUCCESSFUL** |
| 3 mutant twins | all FAILED (correct) | **all still FAILED** |
| assume-binding guard | 5.1 s | 20.9 s |
| undetermined checks | 0 | **0** |

No verdict flipped and nothing became undetermined at 4× the state space. That is the signature of a
real proof. A harness leaning on a lucky bound behaves the opposite way: checks start coming back
undetermined as the space grows, because the solver can no longer reach them.

Cost grew ~CAP^1.5–2.6 — with the **data size**, not with loop trip count, which is exactly the
property loop contracts are supposed to buy and is the cleanest evidence that they delivered it.

**Use it as a gate-time discipline:** prove at the working capacity, then re-run the property and its
mutant at 2–4× and require both verdicts unchanged. It costs one extra run per property and it closes
a hole the mutant twin cannot see.

### Skolemise instead of quantifying — measured 400× cheaper
For a scan loop, replace a universally-quantified invariant with a **witness index chosen symbolically
BEFORE the loop** and referenced only inside the invariant. The proof then holds for an arbitrary
witness, hence for all of them, and stays quantifier-free. Measured on the same obligation: **1120 s
with a real `forall!` vs 2.81 s Skolemised.**
It does **not** work for permutation loops (a shift-insert moves values between cells, so a single
witness is not inductive). Those need a real `forall!` at ~1120 s per harness — not viable at scale, so
prefer a model that avoids permutation loops entirely.

### The escalation order for a loop-bound failure — strongest claim first
1. **`#[kani::unwind(n)]` / `--unwind n` sweep with unwinding checks ON.** Anything that proves here is
   full strength. Note Kani needs the bound **one more than** the iteration count, and `break`/
   `continue` can need two or three more.
2. **`-Z loop-contracts`.** Unbounded and full strength. Prefer this over any bounded fallback.
3. **Shrink the problem** — a smaller `const` bound in the harness, honestly recorded, so the claim is
   about the smaller structure rather than silently about nothing.
4. **`--no-unwinding-checks` LAST, and never without its mutant twin.** See below.

### 🔴 `--no-unwinding-checks` PRUNES paths — and it destroys Kani's own completeness claim
Kani's guarantee is stated as "**practically complete when all unwinding assertions pass**". The
unwinding assertion is the check that your bound was big enough. `--no-unwinding-checks` deletes
exactly that check, so it does not merely narrow the claim — it removes the evidence that the claim
covers anything. Kani's documentation never recommends the flag; the tutorial's remedy for a
too-small bound is to raise the bound or shrink the problem.

### 🔴 `--no-unwinding-checks` PRUNES paths — it does not merely truncate them
So a harness can pass **with no content**. Measured on eviction-policy-session-lists: in the first
full run every `verify_*` passed AND **36 `__mutant` twins passed too**, and a passing mutant is the
definition of a vacuous proof. Two consequences you must design for:

1. **`bounded-shallow` is the fidelity where vacuity is most likely, not least.** Write the harness so
   that no reachable loop needs more than the bound, and say so in the `note`. The scorer now re-runs
   the mutant under the same flags as the proof, so a contentless bounded pass is caught — but a
   harness written to be honest is better than one caught being dishonest.
2. **For a refutation, bind the outcome instead of trusting a bare assert.** A pruned pass would score
   a real defect as `proved`. The idiom that survives pruning: bind the outcome, `kani::cover!` the
   violating case, then assert. An unsatisfiable cover is a FAILED check, so the harness fails whether
   the violation is unreachable OR the path was pruned away — it can never pass silently.

### Why every proof here carries a mutant twin — Kani has no vacuity detection
Kani's own tool paper is explicit that a bad assumption "makes the proof vacuously true, so
assumptions must be reviewed as carefully as the code itself", and it describes **no** vacuity
detection, no reachability or coverage metric, and no assumption-consistency check. Mutation testing
of proofs appears nowhere in it. So the `verify_<id>__mutant` twin is not ceremony and not
duplication: it is the only mechanism in this pipeline that can tell a proof from an empty one, and
the tool cannot do it for you.

Measured worth: on `eviction-policy-session-lists` the gate found **52 of 90** harnesses vacuous, and
on `eviction-policy-optimized` one published proof was empty. Every one of those passed Kani cleanly.

### Trusted stubs make a proof CONDITIONAL — prefer `stub_verified`
A plain `#[kani::stub(f, g)]` is **not** checked against the real `f`. Any result that depends on it is
sound only if the stub over-approximates faithfully, which nothing verifies. With `-Z function-contracts`
you can instead give `f` a contract, prove it once with `#[kani::proof_for_contract]`, and use
`stub_verified` — then the abstraction is checked rather than trusted. Where you must use a plain stub
(the `RandomState::new` seed stub is the standing example), record `fidelity: representative` and name
the stub in the note, so the page shows a conditional claim as conditional.

### Solver choice is a real lever, and wider than two options
Backends available: SAT — **MiniSat (default)**, Kissat, CaDiCaL; SMT — Z3, cvc5, Bitwuzla. Their
timeout profiles differ sharply, so a sat-timeout is worth retrying across several, not just one swap.
Quantifiers are bounded: SAT backends expand eagerly and warn above ~1000 values, while SMT backends
accept runtime-valued bounds — so a quantified invariant over a large array wants an SMT backend.

### `--harness NAME` matches SUBSTRINGS
One flag can run several harnesses and interleave their verdicts. Never infer a verdict for one
harness from a run that matched others, and avoid names that are prefixes of other names. This
produced a false `proved` on a property that both tools had in fact refuted — the worst bug this
pipeline has had.

### Write a discriminator wherever you suspect a missing check
A variant that PASSES once the suspected check is added isolates the cause to that check alone. On
eviction-policy-optimized that was the single strongest piece of evidence in the whole report, and it
is what turns "this assertion failed" into "this specific missing bounds check is the defect".

## Definition of done — "not attempted" is not an outcome (mandatory)
Every inventory property must reach **exactly one** of three end states. There is no fourth box.
1. **Proved** — a passing harness (bounded scope stated), or a disclosed faithful stub/mirror with the boundary named.
2. **Delegated** — the obligation is owned by a **different component** across a real interface boundary; name it and route it. "Belongs to another *tool*" is **not** delegation — that is still your property to attempt here.
3. **Tool boundary hit** — you **exhausted the applicable coverage-extending levers, wrote the harness, ran it, and captured a reproducible failure signature** (unwinding-assertion / `unsupported_construct: <name>` / SAT-timeout `>N min at unwind=K`). Evidence is mandatory; a limit asserted *without a run*, or before trying the lever that clears it (e.g. the `RandomState` stub for a HashMap wall), is **not** a legitimate boundary — it is a recipe gap.

**"Harness not written" / "authorable but not done" is NOT an end state.** A property with no harness is *unfinished work*, never a rating. Do not report it, do not park it, do not hand back the run with it open. The only exit from the not-done set is an actual attempt, which forces the property to (1) or (3). On uncertainty the default is **attempt**, never "tool limitation." A run returned with unattempted properties has not met the bar, no matter how many were proved.

**An unattempted property — no runnable harness produced — is a transient working state, never returnable.** It means the work is *unfinished*, not that a boundary was found. You do **not** write `status` at all (Step 6); enforcement is by **reproduction**, not by reading a field you set. The **gate (Step 7) is the shipped `scorer_kani.py`**: for any property lacking a harness it can re-run to `VERIFICATION SUCCESSFUL`, a completed run lever-battery, or a resolvable delegation, it returns **UNRESOLVED and exits non-zero** — the hand-back fails. (An advisory `miss_class: AGENT` you leave behind is your own admission the item is unfinished, never a verdict.) There is no "partial run" hand-back and no asking the user to accept the remainder — you either finish (every property the scorer re-runs to proved / delegated to a named component / tool-boundary with a captured signature that survives the lever battery) or you keep working. The highest-leverage unfinished items are the shared/global invariants (Step 2, ordered by attachment count); the scorer flags them first because one left unattempted keeps every method in its bundle unproved.

## Clean-slate re-run protocol (mandatory for re-runs)
A re-run must not inherit credit from a prior run's artifacts.
- **Start from a stripped, isolated tree.** New worktree; **remove all existing `#[cfg(kani)] mod verification` harnesses** so every one is re-authored from the inventory. You may not point at pre-existing harnesses to claim coverage.
- **Do NOT delete the previous verified run.** It stays on its committed `verif/kani/<component>` branch as the baseline and as evidence — deletion destroys expensive proofs and the ability to catch regressions.
- **Provenance rule:** a property counts as proved **only** if its harness was authored and is passing **in this run's tree**. A prior-run pass does not count until reproduced here.
- **Diff against the baseline** and report three sets: re-proved, regressed, and prior-"proved" that did **not** reproduce (phantom coverage). That diff is the audit.
- Capture **wall-clock + peak RSS** for every harness in the fresh run.

## What each `kani:` block must record (per `id`)
Write these into `unified_properties.yaml`; there is **no `.md`** — the YAML is the record and the HTML
(Role 3) is the human-readable form.
- **Proved rows:** `status: proved`, `symbol: ✓` (native) or `★` (disclosed faithful stub/mirror), the
  `fidelity` (`real-type-bounded` / `representative` / `arithmetic-core` / `bounded-shallow`), and
  `evidence` with the harness name, Kani result, `unwind: N`, any `flags` (e.g. `--no-unwinding-checks`),
  wall-clock + peak RSS. State the bounded geometry in `note` — and for `bounded-shallow`, the loop-cut
  caveat (sound only when every loop runs ≤N) plus the Creusot route for a fully-sound proof.
- **Assumptions / bounds:** record each `kani::assume(...)` (the production guard it mirrors) and each
  stubbed FFI / `#[kani::unwind(N)]` bound — and what it leaves unproven — in the `note` of the property it
  affects.
- **Not verified — attempted, tool boundary hit:** `status: tool-boundary`, `symbol: ⊘`, `miss_class: TOOL`,
  and a `note` giving the geometry tried (unwind=K, structure size / stub used) and the concrete signature
  (unwinding-assertion at unwind=K / `unsupported_construct: _xgetbv` / SAT timeout `>N min`).
- **Not verified — not expressible for a bounded checker:** `status: tool-boundary`, `symbol: ⊘`, `note`
  with the one-line reason (concurrency/liveness, unbounded-only, or I/O/hardware/FFI) and the route
  (Creusot / Loom / Spin / fault-injection test). **Note:** string/char CONTENT is *not* in this bucket — it
  is expressible bounded (prove it); this bucket is for concurrency, unbounded-only, and I/O/hardware/FFI.
- **Delegated:** `status: delegated`, `symbol: ⤴`, `note` naming the owning component/test.

## Notes
- Construction + documentation skill — **distinct** from the read-only audits
  `component-check-spec-translation` / `component-check-verif-translation`, from the source-agnostic
  extraction primitive `extract-verifiable-properties`, and from the inventory builder
  `build-property-inventory` (Role 1) whose output this skill **consumes** by `id`.
- Every outcome is written to `unified_properties.yaml`'s `kani:` block by `id`, so
  `tools-aggregate-coverage-by-interface` (Role 3) renders from structured data without re-reconciling.
- Routing: Kani proof code (the `#[cfg(kani)] mod verification` harnesses + the `unified_properties.yaml`
  write-back) → the per-component **`verif/kani/<name>`** branch, overwrite-in-place, committed only under
  `components/<name>/`. Under the `component-verify` orchestrator, the orchestrator performs the
  branch/commit/push and enforces the component-folder-only contamination gate — this skill just leaves the
  artifacts in the working tree.
