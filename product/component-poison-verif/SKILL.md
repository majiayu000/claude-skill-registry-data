---
name: component-poison-verif
description: Deliberately introduce a controlled number of concrete-code/abstract-code misalignments ("verif poisons") into a single Certus component on a throwaway branch, in order to test formal-verification drift tooling (Creusot mirror/equality checks, Kani assume-audits, and `tools-spin-sync`). Each poison intentionally desynchronizes the component's verification artifacts (a `verif/` Creusot mirror, a `#[cfg(kani)] mod verification`, or a Spin `.pml` model) from the shipped implementation while keeping the code compiling. Use only for red-team / evaluation of the verification skills, never on a branch intended to merge.
argument-hint: "[component-name] [poison-count]"
---

# Poison a Component's Verification (concrete ↔ abstract)

The purpose of this skill is to **test the formal-verification drift mechanisms** by
deliberately introducing known, controlled mismatches between a component's *concrete*
(shipped) code and its *abstract* verification artifacts. Where `component-poison` attacks
the `spec.md` ↔ code link, this skill attacks the code ↔ **verif** link:

- **Creusot** — a `verif/` mirror crate that copies a shipped function and proves a
  spec-derived contract with `#[requires]`/`#[ensures]`, kept honest by a *drift/equality
  check* and *fault injection* (see `tools-verify-creusot`).
- **Kani** — a `#[cfg(kani)] mod verification` whose harnesses call the real function under
  `kani::assume` preconditions that must mirror production guards (see `tools-verify-kani`).
- **Spin** — a Promela `.pml` model under `modelling/spin/<name>/` whose README maps model
  locations to source lines (see `tools-spin-sync`).

The verification skills then should detect these seeded mismatches — either by a
verification condition (VC) going red / a counterexample, or (the harder, more important
case) by the drift/equality check, the assume-audit, or the sync divergence report catching
a *silently vacuous* proof.

This is a destructive, adversarial skill. It only ever operates on a dedicated
`poison-verif-<component-name>` branch that is **not** meant to be merged. Do not run it on
`unstable`, a feature branch you intend to ship, or any branch with uncommitted work you
care about.

The component name is `$0` and the number of poisons to introduce is `$1`.

## 1. Resolve parameters and find the verification artifacts

1. If `$0` (component name) was not supplied, interactively ask the user which component to
   poison and stop until provided.
2. Resolve `$0` to exactly one component directory under `components/` (the lower-case,
   hyphen-ized form of the name, or the directory whose `define_component!` block declares
   it). If it does not exist or is ambiguous, return an error and stop.
3. Discover the component's **verification artifacts** — at least one must exist, or there is
   nothing to desynchronize:
   - **Creusot mirror**: a co-located `verif/` crate (e.g. `components/<name>/verif/`), a
     `*-verif` crate, or any `src/**` file that uses `creusot_std::prelude` /
     `#[requires]` / `#[ensures]` / `pearlite!`. Look for a `why3find.json`.
   - **Kani harnesses**: a `#[cfg(kani)] mod verification` block (`rg 'cfg\(kani\)|kani::proof'
     <component-dir>`), plus any `#[cfg(kani)]` stubs.
   - **Spin model**: a directory `modelling/spin/<name>/` with a `.pml` file and a `README.md`
     containing a "Correspondence to Source Code" table.
   If **none** of these exist, stop and report the searched paths — this skill needs abstract
   code to misalign against. (If the user wants spec↔code poisons instead, point them at
   `component-poison`.)
4. Record which artifact form(s) are present; the poison categories in §3 are keyed to them.
5. If `$1` (poison-count) was not supplied, interactively ask the user how many poisons to
   introduce and stop until provided. Require a positive integer; reject `0` or negatives. If
   `$1` exceeds the number of distinct, independently-detectable claims the artifacts expose,
   warn and offer to cap it.

## 2. Create and check out the poison branch

1. Confirm the working tree is clean enough to proceed. If there are uncommitted changes
   that would be swept onto the new branch, warn the user and ask whether to continue.
2. Record the current branch as the base branch.
3. Create a **new local branch derived from the current branch**, named
   `poison-verif-<component-name>` (using the lower-case, hyphen-ized component name), and
   check it out — e.g. `git checkout -b poison-verif-dispatch-map`. If a branch with that
   name already exists, ask the user whether to delete and recreate it, or to append a
   numeric suffix. Do not push this branch to any remote.

## 3. Introduce `$1` verif poisons

Build a short inventory of what each verification artifact *claims* about the concrete code:
the mirrored function(s) and their bodies, each `#[requires]`/`#[ensures]`/loop
`#[invariant]`, each `kani::assume`/`assert`, each Promela property (`P1`, `P2`, …) and its
correspondence rows. Each poison must target a *specific, testable* claim. Spread the poisons
across different claims and, where possible, across different categories below so the test
exercises several detection paths.

The essential axis is **which side you poison** and **whether the mismatch is loud or
silent**:

- **Loud** — the mismatch makes a VC go red (Creusot `✘`), a Kani harness fail, or Spin
  produce a counterexample. Easy to detect; confirms the tool runs.
- **Silent** — the mismatch leaves every proof green but the proof no longer means what it
  claims (vacuous contract, drifted mirror, unmatched assume, stale correspondence). Only the
  *drift/equality check*, the *assume-audit*, or the *sync divergence report* catches it.
  **These are the high-value poisons** — they test whether the harness is actually bound to
  the shipped code. Include at least one silent poison when `$1 >= 2`.

Choose from these categories (mix them; do not use the same category for every poison):

### Creusot (mirror crate)

- **Mirror-body drift** — change the mirror function body in `verif/` so it no longer matches
  the shipped function (or change the shipped function so it no longer matches the mirror),
  *without* touching the contract. The proof stays green; the drift/equality check should flag
  that shipped ≠ mirror. (→ *Drift / Contradiction*, silent.)
- **Vacuous contract** — weaken an `#[ensures]` to something trivially true (e.g.
  `result@ >= 0`, `true`, or dropping the tie to `*entry`/`^entry`) so the VC passes without
  constraining behavior. Fault injection should reveal the VC stays `Proved ✔` when it must go
  red. (→ *Vacuous / Unverifiable*, silent.)
- **Precondition mismatch** — strengthen a `#[requires]` beyond what the production guard
  ensures (assumes a condition the caller never establishes), or drop a `#[requires]` the body
  actually depends on (proof now fails). (→ *Contradiction* loud, or *Unsound precondition*
  silent.)
- **Postcondition contradiction** — flip an `#[ensures]` to state the opposite of what the
  body computes (e.g. `^entry.read_ref == *entry.read_ref - 1u32` where the body adds). The
  VC should go red. (→ *Contradiction*, loud.)
- **Type/structure drift in the mirror** — change a mirrored field/return type so it diverges
  from the real struct (`u32` where the shipped field is `u64`, `Option<T>` vs `T`, a dropped
  enum variant of `Location`). (→ *Contradiction*, may be loud or silent.)

### Kani (`#[cfg(kani)] mod verification`)

- **Unmatched assume** — add or keep a `kani::assume(X)` for which **no** production guard
  enforces `X` (e.g. `assume(read_ref < u32::MAX)` while the shipped increment is a bare
  `+= 1`). The harness passes in a restricted universe; the Phase-4 assume-audit should flag
  it as hiding a bug. (→ *Unsound assumption*, silent.)
- **Harness detached from code** — rewrite the harness to assert against a local copy /
  reimplementation instead of calling the real function, so injecting a fault into the shipped
  function no longer fails the harness. (→ *Drift*, silent.)
- **Stub divergence** — change a `#[cfg(kani)]` stub so its behavior/API subtly differs from
  the `#[cfg(not(kani))]` production type (different default, different bound), verifying a
  type the shipped build never uses. (→ *Drift / Contradiction*.)
- **Wrong postcondition** — change an `assert!` to encode a property the concrete code does
  not actually satisfy (loud: counterexample) or a trivially-true one (silent: vacuous).
- **Coverage gap** — delete a harness for a still-present function whose invariant matters, or
  add an unverified new arithmetic site to the shipped code that no harness covers. (→
  *Missing coverage*, silent unless a completeness check runs.)

### Spin (`modelling/spin/<name>/`)

- **Protocol drift** — change the concrete code's protocol (lock ordering, a new error branch,
  a new transition, a changed channel semantic) **without** updating the `.pml`, so the model
  no longer reflects source. `tools-spin-sync` should report MODEL UPDATE REQUIRED. (→ *Model
  drift*, silent until sync runs.)
- **Model weakening** — remove or weaken a Promela property (`P_n`) or an `assert` in the
  `.pml` so a genuinely-reachable violation is no longer checked. (→ *Vacuous property*.)
- **Correspondence rot** — edit the shipped logic so the README "Correspondence to Source
  Code" line ranges/function names are wrong (LINE DRIFT or worse). (→ *Stale correspondence*.)

Guidance for each poison:

- Make it a *semantic* mismatch between concrete and abstract, not a cosmetic one. Renaming a
  private local or reflowing comments will not exercise the drift tooling. Target something the
  verification artifact states as an observable contract, invariant, or property.
- Keep each poison small and self-contained, and note the exact `path:line` on **both** the
  concrete side and the abstract side.
- Prefer targeting distinct functions / contracts / properties so the poisons are
  independently detectable.
- For each poison, decide up front whether it is **loud** or **silent** and record the
  mechanism you expect to catch it (VC red, counterexample, drift/equality check, assume-audit,
  or sync divergence). A poison whose detection path you cannot name is a weak test — replace it.

## 4. Keep the concrete code compiling and the artifacts runnable

Two things must hold after all poison changes:

1. **The shipped code must still compile.** Build the component with its default configuration:

   ```bash
   cargo build -p <crate-name>
   ```

2. **The verification artifacts must still parse/typecheck**, so the detection tool actually
   *runs* and reports a mismatch rather than dying on a syntax/compile error (a build failure is
   not a drift finding). Sanity-check whichever forms are present, without "helpfully"
   reconciling the mismatch:
   - Creusot: `cargo creusot --only coma` (syntax check, no SMT) in the `verif/` crate.
   - Kani: `cargo build --features kani`-equivalent or `cargo kani --only-codegen` if available,
     otherwise confirm the `#[cfg(kani)]` module compiles under `cfg(kani)`.
   - Spin: confirm the `.pml` still compiles with `spin -a` (or `make` up to codegen) — but do
     **not** run the full model check here (that is the detection step, run later by the user).

If a component is SPDK-gated and cannot be built in this environment, build with its default
configuration and clearly note in the report that a full `--workspace`/hardware build was not
verified. If a poison cannot be made to compile/parse without also removing the misalignment,
back it out and choose a different poison so the final count of applied poisons still equals
`$1` (or, if impossible, stop and report how many were successfully applied).

Do **not** run formatters or linters that would reconcile the mismatch, and do **not** run
`tools-verify-creusot`, `tools-verify-kani`, `tools-spin-sync`, `component-sync-specs`, or any
sync/repair skill — running those *is the test*, and doing so here would defeat the purpose.

## 5. Summarize the poisons

Write a `POISON-VERIF.md` file in the component directory summarizing every applied change in a
table, so the poisons can later be compared against whatever the verification tooling detects
(the ground-truth key). Use this shape:

```markdown
# Verif Poison Report

Component: <component-dir>
Verification forms present: <Creusot verif/ | Kani mod verification | Spin model>
Base branch: <base branch>
Poison branch: poison-verif-<component-name>
Poisons requested: <$1>   Poisons applied: <N>   (loud: <x>, silent: <y>)
Concrete build verified: <cargo build -p <crate> result / caveat>
Artifacts parse-checked: <creusot --only coma / kani codegen / spin -a result / caveat>

> Generated by the `component-poison-verif` skill to test formal-verification drift tooling.
> This branch is intentionally broken and must not be merged.

| # | Form | Category | Side poisoned | Abstract claim (path:line) | Concrete location (path:line) | What was changed | Loud/Silent | Detection mechanism | Expected result |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Creusot | Vacuous contract | abstract | verif/src/lib.rs:182 | src/lib.rs:184 | `#[ensures(^e.read_ref == *e.read_ref+1)]` → `#[ensures(true)]` | Silent | fault injection keeps VC green | Vacuous (must go red) |
| 2 | Kani | Unmatched assume | abstract | src/lib.rs:220 (harness) | src/lib.rs:96 (bare `+= 1`) | added `assume(read_ref < MAX)` with no guard | Silent | assume-audit | Unsound assumption |
| 3 | Creusot | Mirror-body drift | concrete | verif/src/lib.rs:188 | src/dispatch.rs:142 | shipped `checked_add` → `wrapping_add` | Silent | drift/equality check | Drift (shipped ≠ mirror) |
| 4 | Spin | Model weakening | abstract | modelling/spin/…/m.pml:57 (P2) | src/state.rs:70 | removed `assert(write_ref<=1)` | Loud on real bug / Silent | tools-spin-sync | Vacuous property |
```

Map the "Expected result" column to the vocabulary the relevant detection path uses (VC
`Proved ✔`/`✘`, Kani `failed`/assume-audit *defect*, Spin PASS/FAIL/MODEL UPDATE REQUIRED, or
the drift/equality-check verdict) so the poison report doubles as an answer key.

## 6. Report

Print a concise summary to the user: the poison branch name, the base branch, which
verification form(s) were poisoned, how many poisons were applied (vs requested) and the
loud/silent split, whether the concrete build passed, whether the artifacts still parse, and
the path to `POISON-VERIF.md`. Remind the user this branch is intentionally broken, must not be
merged, and that they can now run the matching verification skill against the component to see
how many poisons it catches:

- Creusot poisons → `tools-verify-creusot` (watch for VCs that *should* go red but stay green —
  the drift/equality check and fault-injection step are what catch the silent ones).
- Kani poisons → `tools-verify-kani` (the Phase-4 assume-audit is what catches unmatched
  assumes and detached harnesses).
- Spin poisons → `tools-spin-sync` (the divergence report is what catches protocol drift and
  stale correspondence).

Do not commit or push unless the user explicitly asks.
