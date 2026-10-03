---
name: component-check-verif-translation
description: Cross-check a Certus component's abstract verification artifacts (a `verif/` Creusot mirror, a `#[cfg(kani)] mod verification`, or a Spin `.pml` model) against its concrete shipped implementation, then summarize concrete-code/abstract-code drift with source evidence. Use when auditing whether a formal-verification harness still faithfully mirrors the code it claims to prove, when checking for vacuous contracts or unmatched assumptions after code changes, or when validating what `component-poison-verif` seeded. This is a read-only audit and does not reconcile, repair, or edit either side; it does not run spec/model sync or repair skills.
---

# Check Component Verif Translation

Compare *abstract* verification intent (Creusot contracts and mirrors, Kani harnesses and
assumes, Spin models and their correspondence tables) with the *concrete* shipped code they
claim to cover. Look for meaning that drifted, went vacuous, was contradicted, was assumed
without a guard, or was never covered. **A green proof is not evidence of alignment** — a
contract can pass while mirroring nothing. Reason about what each artifact actually constrains,
not about whether the solver returned `Proved ✔`.

This is the companion audit to `component-poison-verif`: the categories below are the same
ones that skill seeds, so this skill's findings double as the scoring key for a poison run.

## Resolve the Scope

1. Resolve the requested component name or path to one component directory. Prefer
   `components/<name>/`; accept an explicit component path elsewhere in the repository.
2. If no component is named, infer it only when the working directory is inside one component
   or the request identifies exactly one. Otherwise ask for the component.
3. Discover the **verification artifacts** present (at least one must exist):
   - **Creusot mirror** — a co-located `verif/` crate, a `*-verif` crate, or any `src/**`
     using `creusot_std::prelude` / `#[requires]` / `#[ensures]` / `#[logic]` / `pearlite!`.
     Note the `why3find.json` if present.
   - **Kani harnesses** — a `#[cfg(kani)] mod verification` block (`rg 'cfg\(kani\)|kani::proof'
     <component>`) plus any `#[cfg(kani)]` stubs.
   - **Spin model** — `modelling/spin/<name>/` with a `.pml` file and a `README.md` carrying a
     "Correspondence to Source Code" table.
4. Treat the component's checked-in source as the concrete implementation. Include
   `Cargo.toml`, `src/`, `tests/`, `build.rs`. Follow references into shared interfaces
   (`components/interfaces/`), macros, or app wiring when needed to determine behavior.
5. Exclude build output, vendored code, logs, transcripts, and prior drift/poison reports as
   *evidence of alignment*. A `POISON-VERIF.md` may help locate seeded changes but must never
   be read to pre-decide a finding — reach each verdict from the code and the artifact.

If none of the three artifact forms exist, stop and report the searched paths (there is no
abstract code to audit; `component-check-spec-translation` covers the spec↔code link instead).
If the component path is ambiguous, do not combine candidates.

## Build the Verification Inventory

Read every discovered artifact completely and extract each independently checkable claim:

- **Creusot**: each mirrored function and its body; each `#[requires]`, `#[ensures]`, loop
  `#[invariant]`, `#[variant]`, and `#[logic]` predicate; the shipped function each mirror
  claims to copy.
- **Kani**: each `#[kani::proof]` harness and the function it exercises; every `kani::assume`
  and `assert`/`kani::assert`; each `#[cfg(kani)]` stub and its `#[cfg(not(kani))]` twin.
- **Spin**: each property (`P1`, `P2`, …) and `assert` in the `.pml`; each row of the
  Correspondence, Properties Verified, System Abstraction, and Assumptions/Stubs tables.

For each claim, identify the concrete counterpart it is meant to mirror or constrain, with an
exact `path:line` on **both** the abstract and the concrete side. Split compound contracts when
their clauses can align differently.

## Trace Claims into Code — the four checks

For every inventory item, run whichever of these apply. Cite `path:line` on both sides; never
call something faithful because names resemble each other or because a proof is green.

### 1. Drift check (does the abstract still match the concrete?)

- **Creusot**: compare the mirror function body against the shipped function it copies,
  statement by statement. Any divergence in operations, operators (`checked_add` vs
  `wrapping_add`), constants, branch conditions, or control flow is **Drift**, even if the VC
  still discharges — the proof is now about code that no longer ships.
- **Kani**: confirm each harness *calls the real function*. A harness that asserts against a
  local reimplementation or copy is detached — injecting a fault into the shipped function
  would not fail it → **Drift**.
- **Kani stubs**: compare each `#[cfg(kani)]` stub to its `#[cfg(not(kani))]` twin for
  behavioral/API divergence (different default, bound, or signature) → **Drift**.
- **Spin**: read the source at each Correspondence row and confirm the model still reflects it
  (control flow, transitions, lock ordering, channel semantics). Materially diverged →
  **Drift**; correct logic but wrong line ranges/function names → **Stale correspondence**.

### 2. Vacuity check (does the contract actually constrain anything?)

For each `#[ensures]` / `assert` / Spin property, ask: *would a plausible contract-violating
change to the code make this go red?* If the postcondition is trivially true (`true`,
`result@ >= 0` on an unsigned, dropped ties to `*x`/`^x`), tautological, or too weak to
distinguish correct from incorrect behavior, it is **Vacuous** — it passes without proving the
property it names. Reason by mental fault injection; run the tool (below) only to confirm.

### 3. Assumption/precondition audit (is every hypothesis backed by a guard?)

For each `kani::assume(X)` and each `#[requires(X)]`, find the production guard that establishes
`X` before the function runs (a caller check, a condvar wait, a validation branch).
- Guard exists → the assumption is justified.
- **No guard exists** → **Unsound assumption**: the proof holds only in a universe the shipped
  code never enforces (the classic `assume(read_ref < u32::MAX)` over a bare `+= 1`). This is
  the highest-value silent defect — surface it even when every harness passes.
- A `#[requires]` *stronger* than any guard is likewise unsound; one *weaker* than what the
  body needs will usually show up as a red VC (**Contradiction**).

### 4. Coverage check (is what matters actually verified?)

Enumerate the risky sites the verification *should* cover — arithmetic that can overflow/wrap,
ref-count/state transitions, the invariants named in the component's own docs — and confirm
each has a live contract, harness, or property. A still-present function or reachable path with
no coverage is **Missing coverage**. Note added-but-unverified code paths explicitly.

### Optional: run the tools for confirming evidence (read-only w.r.t. source)

To settle a material claim you may run the verifier in a way that does not edit source:
`cargo creusot --only coma` (syntax) or `cargo creusot` (full VCs) in the mirror crate;
`cargo kani --manifest-path …` (optionally `--harness`); `spin -a`/`make` then the model
check in `modelling/spin/<name>/`. Separate this runtime evidence from static reasoning, state
exactly what you ran, and remember a **green result never upgrades a Drift/Vacuous/Unsound
finding to faithful** — those are precisely the failures the solver cannot see. If a tool is
unavailable (no solver, no Spin, SPDK/hardware gate), mark affected claims **Unverifiable** and
say so. Do **not** run `tools-verify-*`, `tools-spin-sync`, `component-sync-specs`, or any
repair/sync skill — those reconcile the mismatch and would destroy the evidence.

## Classify Translation Results

Assign exactly one primary result to each claim:

- **Faithful**: the abstract artifact mirrors the concrete code and the contract/property is
  non-vacuous and covers the claim.
- **Drift**: the mirror body, harness target, stub, or model no longer matches the shipped code
  (abstract ≠ concrete), regardless of whether the proof still passes.
- **Vacuous**: the contract/assert/property is trivially true or too weak to constrain the
  behavior it names; a plausible fault would not be caught.
- **Contradiction**: the contract/assertion/model states something the concrete code does not
  satisfy — a red VC, a Kani counterexample, or a Spin assertion violation on reachable code.
- **Unsound assumption**: a `kani::assume` or `#[requires]` not established by any production
  guard (or stronger than one).
- **Missing coverage**: a still-present function, arithmetic site, invariant, or reachable path
  that has no contract, harness, or property.
- **Stale correspondence**: Spin/README correspondence rows (or contract doc-comments) point at
  the wrong file, function, or line range though the logic is otherwise mirrored.
- **Unverifiable**: settling the claim needs a solver, hardware, or environment unavailable to
  this audit. Do not count as a mismatch.

Severities for non-faithful findings:

- **Critical**: a proof relied upon for a safety/data-integrity contract is unsound or vacuous,
  so the guarantee is illusory.
- **High**: mirror drift or a contradiction on a core invariant; an unmatched assume over a
  genuinely reachable overflow/underflow.
- **Medium**: vacuous edge-case contract, missing coverage of a real risk site, stub
  divergence with behavioral impact.
- **Low**: stale correspondence or line-range drift with the logic otherwise intact.

State confidence as high, medium, or low. Prefer `Unverifiable` or lower confidence over
speculation. Do not turn harmless naming, formatting, or refactoring differences into drift.

## Summarize the Audit

Return the report in this shape:

```markdown
# Component Verif Translation Audit

Component: <path>
Verification forms: <Creusot verif/ | Kani mod verification | Spin model>
Evidence: static inspection; <tools run, or "no tools run">

## Summary

| Result | Count |
|---|---:|
| Faithful | N |
| Drift | N |
| Vacuous | N |
| Contradiction | N |
| Unsound assumption | N |
| Missing coverage | N |
| Stale correspondence | N |
| Unverifiable | N |

Verdict: <one-sentence assessment of how much the passing proofs can be trusted, and the highest risk>

## Concrete ↔ Abstract Mismatches

| ID | Form | Severity | Result | Abstract evidence | Concrete evidence | Mismatch and impact |
|---|---|---|---|---|---|---|
| V-1 | Creusot | Critical | Vacuous | `verif/src/lib.rs:182` | `src/lib.rs:184` | `#[ensures(true)]` proves nothing; increment property unguarded. |
| V-2 | Kani | High | Unsound assumption | `src/lib.rs:220` | `src/lib.rs:96` | `assume(read_ref<MAX)` has no production guard; bare `+= 1` can overflow. |
| V-3 | Creusot | High | Drift | `verif/src/lib.rs:188` | `src/dispatch.rs:142` | Mirror uses `checked_add`; shipped uses `wrapping_add`. Proof is about dead code. |

## Unverifiable Claims

- <claim and why it could not be established (tool/hardware/environment)>

## Coverage by Artifact

| Artifact | Claims | Faithful | Mismatched | Unverifiable |
|---|---:|---:|---:|---:|

## Recommended Next Actions

1. <highest-value fix; name which side (concrete or abstract) needs review, without editing it>
```

List findings by severity, then artifact order. Include every non-`Faithful`, non-`Unverifiable`
result in the mismatched total. Omit empty detail sections. End with the total number of claims
checked and mismatches found.

If this run is scoring a `component-poison-verif` branch, report only what the code and
artifacts show; do not consult `POISON-VERIF.md` before forming verdicts. The user can compare
your findings against that answer key afterward.

Remain read-only. Do not update the mirror, harnesses, model, implementation, specs, or any
sync report unless the user separately asks for remediation.
