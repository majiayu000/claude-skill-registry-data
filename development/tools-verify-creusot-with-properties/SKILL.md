---
name: tools-verify-creusot-with-properties
description: Create a Creusot verification for a Certus component from BOTH its spec and its Rust code — at function granularity with spec-derived contracts — prove it, and record exactly what was proved (with evidence) by writing each property's status/symbol/fidelity/evidence into the shared `unified_properties.yaml` under its `creusot:` block. Attempt every property you can express as a contract — do not pre-filter by lane, effort, or difficulty. Use for the normal verify-and-document workflow (not the blind property-extraction experiment).
argument-hint: "<component-name-or-path>"
---

## Goal
Verify a component with Creusot **and** record exactly what was proved.
Inputs are the component's **spec** (the intended behavior) and its **Rust code** (the functions to
prove). Outputs are (1) the Creusot `verif/` artifacts and (2) the per-property status/symbol/
fidelity/evidence written back into the shared `unified_properties.yaml` under each property's
`creusot:` block.

This skill = **`tools-verify-creusot` + explicit spec pairing + a status-write-back step.** Use
`tools-verify-creusot` for the create/proof mechanics (pure-core extraction, `verif/` crate,
`#[requires]`/`#[ensures]`, drift/equality check, fault-injection validation). This skill adds the
spec-derived-contract sourcing and the structured write-back into `unified_properties.yaml`.

## Steps
0. **Environment — make the toolchain reachable FIRST (mandatory).** The agent/tool shell does **not**
   source `~/.bashrc`, so the bundled Creusot toolchain (`why3` + the SMT provers) is off `PATH` by
   default. Before any `cargo creusot`, self-establish it and confirm the provers are registered — a
   "why3 not found" / "no prover" error is an **environment fault to fix here**, never a `tool-boundary`
   and never a reason to leave a property unattempted:
   ```bash
   export PATH="$HOME/.local/share/creusot/bin:$PATH"   # why3 + alt-ergo/cvc4/cvc5/z3 (absolute paths in ~/.why3.conf)
   command -v why3 >/dev/null || { echo "FATAL: why3 unreachable — creusot bundle missing, escalate to user"; exit 1; }
   why3 config detect >/dev/null 2>&1 || true           # re-register provers if ~/.why3.conf lost them
   why3 config list-provers | grep -qiE "alt-ergo|z3|cvc" || { echo "FATAL: no SMT prover registered"; exit 1; }
   ```
   Prepend the same `PATH` export to every heredoc/`cargo creusot` invocation in this run (a fresh tool
   shell starts without it). If the bundle itself is genuinely absent, that is a **blocker to escalate to
   the user**, not a per-property verdict — it does not license leaving any property unattempted.
1. **Resolve inputs — consume the inventory, do NOT re-extract.** Resolve to `components/<name>/` and
   load the **property inventory** `verif/unified_properties.yaml` (Role 1,
   `build-property-inventory`): the agreed, id-keyed, tool-independent property set. Also open the Rust
   functions to prove (`src/**`); use the spec only to read the wording of an obligation, never to mint a
   new one. **Do not build a private per-tool property list.** If the inventory is missing, stop and run
   `build-property-inventory` first. If you spot a real obligation the inventory lacks, **flag it back**
   to the inventory so it gets an `id` there — never keep a private property.
2. **Prove the shared/global invariants FIRST, once — then reuse.** Before any per-method work, take the
   inventory properties whose bundle spans multiple methods (the inventory marks these as global /
   maintained invariants and gives each an attachment count). **Order them by attachment count, highest
   first** — the one in the most bundles has the most leverage. Prove each as a **single maintained
   invariant** (a type `#[invariant]` or a `logic` predicate): establish it at construction/`initialize`,
   and prove each mutator **preserves** it (`#[requires] inv(self)` → `#[ensures] inv(result)`). Record it
   under its **one** inventory `id` — its `proved` status then propagates to every bundle it belongs to
   automatically (Role 3 attaches by id; you do NOT re-prove it per method). A cheap invariant in many
   bundles (e.g. an init-gate or an accounting invariant) unblocks all those methods in one proof — never
   skip it because "no single method owns it," and never re-assert it vacuously in each method.
3. **Then, for each remaining per-method obligation, express it as a Creusot contract bound to the CODE.**
   Take the obligation verbatim from its inventory row (`id`, `statement`, `kind`, `object_fn`) and render
   it as `#[requires]`/`#[ensures]` on the real function, **citing the already-proved invariants as known
   facts** rather than re-proving them. Where the crate can't build under Creusot, use a **faithful
   whole-function mirror** in `verif/` with the **same** contract, guarded by a drift/equality check.
   Function granularity — never a lifted statement.
4. **Prove.** `cargo creusot` to green; iterate. Record every `#[trusted]` boundary and assumption.
5. **Validate (anti-vacuity).** Fault-inject each function (a contract-violating change) and confirm the
   proof goes **red**; if it stays green, the contract is vacuous — strengthen it. Then revert. For a
   maintained invariant, also fault-inject a mutator that *breaks* it and confirm the preservation VC fails.
6. **Produce artifacts the scorer can reproduce — you do NOT write your own status.** The verdict is
   assigned in Step 7 by the shipped scorer, which *re-runs `cargo creusot` from source* (it `touch`es
   every `src/**.rs` first, so a hand-edited `.coma` cannot fake a `Proved`). Your job in Step 6 is to
   leave, for every property, a proof unit the scorer can name and run:
   - **One why3 module per property `id`** — a function or lemma named `verify_<id>` (id lowercased,
     `-`→`_`) carrying the contract, so it compiles to `verif/<crate>_rlib/verify_<id>.coma`. If the
     obligation is discharged inside a differently-named module, point the scorer at it with
     `creusot.evidence.module: <name>` (or `modules: [<a>, <b>]` when several must all prove) — but each
     named module must exist and prove.
   - **For any property you cannot prove on the first clean attempt, build the lever-battery variants**
     that `gate/lever_battery_creusot.yaml` requires for the failure class you hit, as *named modules*:
     `verify_<id>__inv` (strengthened invariant), `lemma_<id>` (inductive `#[logic]` lemma),
     `verify_<id>__fmap` (FMap/Seq ghost mirror of a std container), `verify_<id>__trusted` (opaque type
     behind a contract-carrying `#[trusted]` u64-handle boundary). The scorer runs the *scorer-applied*
     levers itself (prover portfolio `-P alt-ergo,z3,cvc5,cvc4`, `--time`/`--depth` budget,
     `-T split_vc,compute_specified`); the *code* levers above it demands as artifacts. A tool-boundary
     is **inadmissible** until every required code-lever module exists — a missing one scores UNRESOLVED,
     not tool-boundary.
   - **An anti-vacuity twin** `verify_<id>__mutant` (a contract-violating copy) wherever the property
     could pass vacuously — the scorer requires it to go RED.
   - In `unified_properties.yaml` under the `creusot:` block you may fill **only the advisory fields the
     scorer does not own**: `fidelity` (`real-type | ghost-mirror | trusted-boundary`), a human `note`
     (name every `#[trusted]` boundary and what it therefore does *not* prove), the `evidence.module(s)`
     pointer above, and for a genuine cross-*component* delegation a resolvable `delegate_to:`. **Do NOT
     write `status`, `symbol`, or the run-measured `evidence` (vcs/coma/wall/rss)** — the scorer
     overwrites them from the live run and stamps `_scored_by: scorer_creusot`. The only way to move a
     property's status is to make its module reproduce.
   `fidelity` meanings: `real-type` = proved against the real product code; `ghost-mirror` = proved
   against a logic FMap/Seq model of the real container (`★`); `trusted-boundary` = the effect sits behind
   a contract-carrying `#[trusted]` boundary (block-device I/O, crc32fast, UTF-16, Mutex, raw ptr/FFI)
   (`★`). Report evidence in prose as **VCs/goals discharged + `.coma` count — never bare "files"**.
7. **Gate — the shipped scorer decides, by reproduction (mandatory; you cannot grade yourself).** The
   reproduction gate is `scorer_creusot.py`, which the `component-verify` orchestrator runs in its Step
   2.5. If you are running this skill standalone, invoke it yourself before returning and paste its output
   into your report:
   ```bash
   python3 "$(git rev-parse --show-toplevel)/.claude/skills/component-verify/gate/scorer_creusot.py" \
       components/<name>/verif --crate-dir components/<name>/verif --cap-seconds <cap>
   ```
   The scorer touches all sources (anti-tamper), runs scoped `cargo creusot <module>` for each property's
   module(s) (a `Proved (…) ✔` with no `✘`/`unproved` and exit 0 is a pass), captures VCs/`.coma`/wall/RSS
   **from the run**, checks the anti-vacuity mutant, applies the scorer-owned levers on failure, and writes
   the scorer-owned `status`/`evidence`/`note`/`_scored_by`. It assigns `proved` / `tool-boundary` (only
   after the scorer-applied levers ran, every required code-lever module was present and re-run, and the
   residual signature is not a known defeat) / `delegated` (resolvable referent) / **UNRESOLVED** (no
   module, an unreproducible pass, a missing required code-lever module, a known-defeat signature, or a
   broken/untranslatable crate) — and **exits non-zero if any verifiable property is UNRESOLVED.** If it
   exits non-zero you are **not done**: for each UNRESOLVED `id`, produce the missing module / the demanded
   lever module / fix the crate, and re-run the scorer. Iterate until it exits 0. A translate error in the *real* verif crate is a
   broken crate (UNRESOLVED), never a tool-boundary. "Better suited to Kani" is not an exit — a
   within-component obligation Creusot genuinely cannot express earns a `tool-boundary` **only** by mapping
   to an active construct in `gate/inexpressible_creusot.yaml` (add `claims_inexpressible: <IX-ID>`; the
   scorer confirms it via an isolated canonical probe and records the covering tool from the entry's
   `covered_by`). It is not a delegation (delegation crosses a *component* boundary). You may not
   hand back the run or write a "partial run" summary while the scorer fails, no matter how many properties
   are proved; editing the YAML to say `proved` does nothing, since the scorer regenerates from source and
   overwrites it.

## Coverage discipline (mandatory)
**Attempt every property in the inventory that you can express as a contract. You do not get to pick
lanes here** — routing properties across tools is a separate step, not this one. Your job is to prove or
fail *trying*, and to record the outcome **keyed to the inventory `id`** so Role 3 can aggregate it.
- **No pre-filtering by lane, effort, or budget.** "Better suited to Kani", "intractable", "needs
  induction", "to stay within budget" are **not** acceptable reasons to omit a property. If you can state
  the contract, you must attempt the proof.
- **Attack the highest-leverage properties first.** A property in many bundles is not lower priority for
  being "shared infrastructure" — it is *higher* priority, because one proof discharges it everywhere. Prove
  the shared/global invariants (ordered by attachment count) before spending effort on method-specific
  obligations; a cheap invariant left at `not_yet` silently keeps every method in its bundle unproved.
- **Exhaust Creusot's capabilities before declaring a limit.** Bit-level properties → `#[bitwise_proof]`
  (reasons over `&`/`|`/`<<`/`>>` and `Vec<u64>` words — a bitmap round-trip is *in scope*, prove it).
  Maps/collections → logic-level `FMap`/`Seq` models. Nonlinear/division facts → `proof_assert!` bridges.
  Do not defer a bit-vector or container obligation as "out of reach" without first trying these.
- **Bounded effort, not infinite grind.** Give each proof a real attempt against a stated cap (e.g. one
  full portfolio pass, or a per-VC solver timeout). Exceeding the cap converts the property to a
  **`tool-boundary` with the solver-timeout signature** (`miss_class: TOOL`, `note:` the exact
  `>N min, portfolio alt-ergo/z3/cvc5` string) — it does **not** license leaving the property unattempted.
  The cap decides *when the captured signature is ready for the scorer*, never *whether you may skip*.
- **Every non-success carries a reproducible signature**, never a subjective verdict: the failing VC, a
  solver timeout (`>N min, portfolio alt-ergo/z3/cvc5`), or a specific SMT model gap (e.g. `leading_zeros`
  modelled only relationally, so `leading_zeros ↔ log2` won't discharge). Ban bare "intractable"/"out of scope".
- **Only two legitimate non-proofs**, each needing a one-line technical reason and a suggested route:
  (a) **Not expressible** in Creusot's logic at all — and *inexpressibility is not yours to assert from a
  hunch*: it holds only when the property maps to an **active construct in `gate/inexpressible_creusot.yaml`**
  (a documented tool-model fact), which you claim with `claims_inexpressible: <IX-ID>` for the scorer to
  confirm (see the record-format section). Concurrency/interleaving and liveness/timing are **delegated to a
  concurrency model (Loom/Spin)**, not claimed here;
  (b) **Depends on effects Creusot cannot model** — real I/O, hardware, FFI byte layout.
  Everything else must be attempted and reported with its signature under the tool-boundary shape.

## Coverage-extending levers — exhaust these BEFORE recording ⊘ (mandatory)
A "tool boundary" is only legitimate after the applicable levers below have been *tried and shown to
fail with a captured signature*. A wall that a documented lever clears is a **recipe gap, not a tool
boundary** — recording ⊘ without trying the lever is a false negative. In particular a
`HashMap`/`HashSet`-backed field is **not** an automatic boundary: `creusot-std` already gives it a
`View` (`ViewTy = FMap<K::DeepModelTy, V>`) and you supply the mutation specs yourself.

- **`HashMap` / `HashSet` field (`insert`/`get`/`remove`/`contains`/`len`).** DEFEATABLE. The `@`
  model exists but `creusot-std` ships specs for *iteration only* — write your own `extern_spec!`
  against the `FMap` API to give the mutators semantics:
  ```rust
  use creusot_std::{logic::FMap, prelude::*};
  use std::collections::HashMap; use std::hash::{BuildHasher, Hash};
  extern_spec! {
      impl<K: DeepModel + Eq + Hash, V, S: BuildHasher> HashMap<K, V, S> {
          #[check(ghost)]
          #[ensures((^self)@ == (*self)@.insert(key.deep_model(), value))]
          #[ensures(result == (*self)@.get(key.deep_model()))]
          fn insert(&mut self, key: K, value: V) -> Option<V>;
          // ...get / remove: see catalog §5 for the full Borrow/DeepModel-bounded block
      }
  }
  ```
  Fidelity `ghost-mirror` (symbol `★`): you assert `DeepModel` equality coincides with `Eq`/`Hash`.
  Ship this `extern_spec!` block once as shared project infrastructure, not per-component.
- **`extern "C"` / raw-pointer / FFI in the path.** `#[trusted]` program fn with the real `unsafe`
  body + a contract that models the C effect logically + a ghost `Ghost<Perm<*const T>>` permission
  token the caller threads through (`creusot-std/src/std/ptr.rs:555-660`). Fidelity
  `trusted-boundary` (`★`). Only ⊘ if no faithful effect model exists.
- **Foreign/std fn with no spec.** `extern_spec! { impl … { #[ensures(...)] fn … ; } }` attaches a
  contract to a fn you don't own (the `Vec`→`Seq` pattern). `#[trusted]` for a whole opaque body.
- **Trusted modules to widen coverage (contract-carrying `#[trusted]` boundaries — the coverage-over-a-hard-leaf
  lever).** When a leaf fn/module is genuinely hard for Creusot (Creusot can't build it, a solver times out on
  its body, or it wraps an effect Creusot can't model), do **not** let it sink the whole call graph. Mark that
  leaf `#[trusted]` **and give it a full `#[ensures]`/`#[requires]` contract** stating what it guarantees; the
  callers above it then verify *natively* against that contract instead of inlining the unprovable body. One
  trusted leaf with a good contract can unblock many callers — this is the primary lever for raising the
  *percentage* of code Creusot covers. Discipline that keeps it honest, not a rug:
  - **A `#[trusted]` contract is a promise, not a proof.** It is an obligation you have *shifted*, not
    discharged. Every trusted item must be recorded per-property as `fidelity: trusted-boundary` (`★`), with the
    `note` naming *why* it is trusted and *what it therefore does not prove*. Never mark a leaf trusted merely
    because proving it is tedious — only when a lever above genuinely failed (capture that signature).
  - **Make the contract as tight as the real behavior** — an over-strong trusted `#[ensures]` silently makes
    every caller's proof vacuous. Anti-vacuity still applies: fault-inject a *caller* to confirm the caller
    proof depends on the trusted contract (goes red), and where feasible discharge the trusted contract by other
    means (a Kani harness over the leaf, a runtime witness test, or a later native Creusot proof) and cite that
    route in the `note`. Untrusted-by-another-tool > trusted-and-unchecked.
  - **Keep the trusted surface small and explicit.** Prefer trusting one narrow leaf over a broad module; the
    coverage you claim is "callers proved *given* these N trusted contracts", and Role 3 must be able to list
    those N. Shrink the trusted set over time as real proofs replace the promises.
- **Complex / unbounded body.** Decompose via sub-fn contracts + loop `#[invariant]`/`#[variant]`
  (termination measure) + `#[maintains(inv)]` to thread the data-structure invariant; call sites use
  only the contract.
- **Bit-level property.** `#[bitwise_proof]` reasons over `&`/`|`/`<<`/`>>` and `Vec<u64>` words — a
  bitmap round-trip is *in scope*.
- **Reference:** `verif/skills_research/CREUSOT_capability_catalog.md` in the
  eviction-policy-session-lists component carries the full catalog (0.12 renames, `extern_spec!`
  HashMap→FMap recipe with copy-paste `get`/`remove`, the `Ghost<Perm>` FFI pattern, soundness costs).

## Crate hygiene and proof engineering — measured, not theoretical (mandatory)

### 🔴 NEVER put `[patch.crates-io]` in `components/<component>/.cargo/config.toml`
Put the `creusot-std` patch in **`verif-creusot/Cargo.toml`**, as a manifest-level patch, with a
checkout-relative path (`creusot-std = { path = "../creusot/creusot-std" }` via the gitignored
`components/<component>/creusot` symlink).

A cargo **config** at component scope applies to EVERY cargo invocation whose cwd is anywhere inside
the component — including `cargo kani` and the Kani scorer's `cargo metadata` preflight, which then
die in dependency resolution on a crate they have no reason to load. This has now happened TWICE
(block-device-filesys, then eviction-policy-session-lists). The second time it would have aborted the
entire Kani gate before it scored a single property; it was caught only because the Kani agent
reported it. A manifest-level `[patch]` is scoped to the one crate and is always the right home.
Note `cargo metadata --no-deps` does NOT reveal this fault (measured: it returns 0 while full
resolution fails), which is why the Kani doctor deliberately omits that flag.

### Splitting a multi-conjunct invariant is NECESSARY BUT NOT SUFFICIENT
`split_vc` splits goal **structure**, not a predicate body. So N conjuncts hidden behind a single
`#[ensures(pool_inv(&^p))]` collapse into ONE goal and fail, while each conjunct closes on its own.
Therefore: give each mutator one `#[ensures]` per clause, and **define every composite predicate as
the conjunction of its named halves**, so re-deriving the composite is a definitional unfolding.
Measured: this took `pool_touch` from failing to proved, and `pool_register` from 3 open goals to 2.

**But separating them does not, by itself, close them** — and the reason is NOT what an earlier
version of this section claimed. It said the residue was budget starvation ("many goals in one why3
file degrade the harder ones"). **That was never measured, and it is wrong.** When `pool_unlink`'s 22
remaining goals were finally closed, the causes were identified by decoding `proof.json` and were
**four missing facts plus three collateral positions** — not starvation:
- the two levers the starvation theory recommends were both tried and both **failed**. Raising the
  budget (`-t 90 -d 20 -j 16`) on `pool_unlink` alone **ran 35 minutes without finishing** and had to
  be killed; the gate's cap is 120-600 s, so that route is disqualified on cost. Dropping the composite
  clauses would have removed only the 3 collateral positions (9 of 22) and left all 4 root causes
  untouched, at the price of making ~40 driver modules unfold the invariant themselves.
- what actually worked was **shape**, covered in the next section: positional provenance clauses on the
  four container primitives (19 goals), plus putting the model's one existential behind a named
  `#[logic]` predicate and supplying the witness term no prover invents (3 goals).

So when goals survive the split, **decode which ones and why before reaching for a bigger budget.**
The recipe: the first `split_vc` under `vc_<fn>` yields exactly one child per `#[ensures]` in source
order, so `proof.json` tells you precisely which clause fails. Distinguish a root cause from a
composite that merely contains one. Chasing budget first cost 35 minutes for nothing.

One genuine budget caveat, separate from the above: a clause proving at 29.0 s against a 20 s budget
passes only intermittently and will flip under load — which is why one helper read "2 open" rather
than "1". If a goal's time is near the budget, treat it as failing.

### State a preservation postcondition in the SAME SHAPE as the invariant that consumes it
A logically equivalent phrasing is **not** an equivalent hypothesis, and this is the lever that
actually closes invariant-preservation goals. **The rule, measured:**
- an invariant that quantifies over a **POSITION** needs a **positional** preservation clause;
- one that quantifies over a **VALUE** needs a **membership** clause;
- a container primitive is used by both, so it needs **both**;
- any `exists` belongs behind a **named `#[logic]` predicate**, with a wrapper that supplies the
  witness term explicitly — a prover will not invent it.

Measured on eviction-policy-session-lists: the existing clauses were all membership-shaped
(`map_has_i`/`leaves_mem_i`), which is right for `leaf_in_set` and useless to `idx_ok`,
`by_key_entries_live` and `session_entries_ok`, which quantify over a position — so the solver had to
invent the position first. `map_insert` had no whole-range clause at all. Adding positional provenance
to `map_insert`/`map_remove`/`leaves_insert`/`leaves_remove` took `pool_unlink` **22 → 8**; putting the
one existential behind `free_covers` with a `free_push` wrapper supplying `free@.len()` closed the rest
and took all three helpers to **0 open**. Side effect worth noting: one driver's proof went from 61
recorded prover calls to 8 — the right shape is also far cheaper.

The same principle unblocked three stale-handle refutations, which needed **frame** facts (slot reuse,
key-index frame) rather than stronger ones.

### `cargo check` is necessary but NOT sufficient
It does not reproduce pearlite-side errors: `Int as u32`, `Clone` ambiguous against the prelude glob,
`old()` in a loop invariant, or `recursion_limit = 1024` overflowing at ~31 `#[ensures]`. Only
`cargo creusot` does. **A verif crate that compiles can still be a broken verif crate**, so "it
builds" is never evidence. Still run `cargo check` — it caught two real Rust errors here (`use of
moved value`, `cannot move out of index`). Derive-ambiguity fix: fully-qualified paths
(`#[derive(::core::clone::Clone, ::core::marker::Copy)]`) **and** drop `PartialEq`/`Eq`, since
deriving `PartialEq` additionally demands `DeepModel` while pearlite `==` is logical equality.

### Driver goals that are NOT in the `#[ensures]` block — check here before blaming the helper
A driver whose own `verify_<id>` module fails may not be failing on its postcondition at all. The
top-level split children **before** the exit VC are the `#[requires]` obligations of the calls the
driver makes. Measured on eviction-policy-session-lists: ~22 properties fail exactly there, on the
arithmetic side conditions every state-layer operation requires and none re-establishes
(`reads < u32::MAX-15`, `clock + n < u64::MAX-615`, `nodes.len() < u32::MAX-15`, log capacity). A driver
chaining two operations therefore cannot discharge the second call's precondition.

**The fix is contract exposure, not prover tuning:** have each state-layer operation ensure how much it
consumed ("the arena grew by at most one", "the clock advanced by at most n", "reads grew by at most
one"), so a chained caller can carry the bound forward. Recognise this class by reading WHICH split
child failed — a missing precondition looks nothing like an unproved postcondition, but both surface as
"module failed".

### Two measurement traps that produce WRONG NUMBERS you will be tempted to report
- **`proof.json` is written incrementally.** A mid-run read is unreliable — `pool_register` read 0
  unproved mid-run and 2 when finished. Gate every census on the printed `Proved ✔` /
  `Goal … ✘ (x/y)` line, never on a mid-run `proof.json`. (This trap cost a wrong number in a
  hand-off report on the very run that discovered it.)
- **`why3find` REPLAYS CACHED RESULTS.** After changing a source, delete the module directory or pass
  `--why3find-arg=-f`, or you are measuring the previous run.

### Dead end — do not retry
`proof_assert!` is unusable inside `macro_rules!` mutator bodies ("Use of borrowed or uninitialized
variable p"), with or without explicit `&mut *p` reborrows. Bridging facts must live on callee
contracts.

## Definition of done — "not attempted" is not an outcome (mandatory)
Every inventory property must reach **exactly one** of three end states. There is no fourth box.
1. **Proved** — a green proof (native), or a disclosed faithful whole-function mirror / `#[trusted]` boundary, named.
2. **Delegated** — the obligation is owned by a **different component** across a real interface boundary; name it and route it. "Belongs to another *tool*" is **not** delegation — that is still your property to attempt here.
3. **Tool boundary hit** — you **exhausted the applicable coverage-extending levers, wrote the contract, ran the proof, and captured a reproducible failure signature** (failing VC / solver timeout `>N min portfolio` / specific SMT model gap). Evidence is mandatory; a limit asserted *without a proof attempt*, or before trying the lever that clears it (e.g. the `extern_spec!` `FMap` recipe for a HashMap field), is **not** a legitimate boundary — it is a recipe gap.

**"Contract not written" / "authorable but not done" is NOT an end state.** A property with no contract is *unfinished work*, never a rating. Do not report it, do not park it, do not hand back the run with it open. The only exit from the not-done set is an actual attempt, which forces the property to (1) or (3). On uncertainty the default is **attempt**, never "tool limitation." A run returned with unattempted properties has not met the bar, no matter how many were proved.

**An unattempted property — no runnable proof unit produced — is a transient working state, never returnable.** It means the work is *unfinished*, not that a boundary was found. You do **not** write `status` at all (Step 6); enforcement is by **reproduction**, not by reading a field you set. The **gate (Step 7) is the shipped `scorer_creusot.py`**, which `touch`es every source and re-runs `cargo creusot` from scratch: for any property lacking a proof unit it can re-run to `Proved`, a completed run lever-battery, or a resolvable delegation, it returns **UNRESOLVED and exits non-zero** — the hand-back fails. (An advisory `miss_class: AGENT` you leave behind is your own admission the item is unfinished, never a verdict.) There is no "partial run" hand-back and no asking the user to accept the remainder — you either finish (every property the scorer re-runs to proved / delegated to a named component / tool-boundary with a captured signature that survives the lever battery) or you keep working. The highest-leverage unfinished items are the shared/global invariants (Step 2, ordered by attachment count); the scorer flags them first because one left unattempted keeps every method in its bundle unproved.

## Clean-slate re-run protocol (mandatory for re-runs)
A re-run must not inherit credit from a prior run's artifacts.
- **Start from a stripped, isolated tree.** New worktree; **reduce every contract to a bare signature** (drop `#[ensures]`, `#[requires(true)]`) / empty the `verif/` mirror, so every contract is re-authored from the inventory. You may not point at pre-existing contracts to claim coverage.
- **Do NOT delete the previous verified run.** It stays on its committed `verif/creusot/<component>` branch as the baseline and as evidence — deletion destroys expensive proofs (`.coma`/VCs) and the ability to catch regressions.
- **Provenance rule:** a property counts as proved **only** if its contract was authored and its VCs are discharged **in this run's tree**. A prior-run pass does not count until reproduced here.
- **Diff against the baseline** and report three sets: re-proved, regressed, and prior-"proved" that did **not** reproduce (phantom coverage). That diff is the audit.
- Capture **wall-clock + peak RSS** for every proof in the fresh run; report proofs as VCs/goals discharged + `.coma` count, never bare "files".

## What each `creusot:` block must record (per `id`)
Write these into `unified_properties.yaml`; there is **no `.md`** — the YAML is the record and the HTML
(Role 3) is the human-readable form.
- **Proved rows:** `status: proved`, `symbol: ✓` (native) or `★` (faithful ghost mirror / `#[trusted]`
  boundary), the `fidelity`, and `evidence` as **VCs/goals discharged + `.coma` count** (never "files") with
  wall-clock + peak RSS. If the proof is against a mirror, say what it therefore does **not** cover in `note`.
- **Trusted boundaries:** name each `#[trusted]` item / mirror / environment assumption in the `note` of the
  property it guards — why trusted, and what it therefore does NOT prove (`fidelity: trusted-boundary`, `★`).
- **Not proved — attempted, tool boundary hit:** `status: tool-boundary`, `symbol: ⊘`, `miss_class: TOOL`,
  and a `note` giving the capability tried (`#[bitwise_proof]` / `FMap` / `proof_assert!`) and the concrete
  signature that blocked it (failing VC / solver timeout `>N min` / SMT model gap).
- **Not proved — genuinely NOT EXPRESSIBLE in Creusot:** you do **not** write `status` or a prose excuse.
  A property is inexpressible **only** if it maps to an **active construct** in
  `gate/inexpressible_creusot.yaml` — a curated, documented tool-model fact (e.g.
  `IX-CREUSOT-STRING-CONTENT`: concrete string/char CONTENT sits behind an opaque `Seq<char>` view). If it
  does, add **`claims_inexpressible: <IX-ID>`** to the property's `creusot:` block (an advisory *claim*, not
  a verdict) and stop — the scorer confirms it by building that construct's canonical probe in isolation and
  observing the model-predicted signature; only then does it award `tool-boundary` (`fidelity:
  not-expressible`, `covered_by` recorded). **You may only reference an existing active construct — never
  invent one, and never use this for "hard to prove."** A goal you can *state* but the solver won't discharge
  is bucket (a) above (battery + captured signature), not this. If no construct fits, the property is either
  provable (attempt it) or a concurrency/interleaving obligation that is **delegated** to Loom/Spin (a
  different model), not an inexpressibility claim here.
- **Delegated:** `status: delegated`, `symbol: ⤴`, `note` naming the owning component/test.

## Notes
- Construction + documentation skill — **distinct** from the read-only audits
  `component-check-spec-translation` / `component-check-verif-translation`, from the source-agnostic
  extraction primitive `extract-verifiable-properties`, and from the inventory builder
  `build-property-inventory` (Role 1) whose output this skill **consumes** by `id`.
- Every outcome is written to `unified_properties.yaml`'s `creusot:` block by `id`, so
  `tools-aggregate-coverage-by-interface` (Role 3) renders from structured data without re-reconciling.
- Routing: Creusot proof code (the `verif/` crate + `.coma` + the `unified_properties.yaml` write-back)
  → the per-component **`verif/creusot/<name>`** branch, overwrite-in-place, committed only under
  `components/<name>/`. Under the `component-verify` orchestrator, the orchestrator performs the
  branch/commit/push and enforces the component-folder-only contamination gate — this skill just leaves
  the artifacts in the working tree.
