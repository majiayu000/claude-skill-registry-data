---
name: mub6-manager
description: "Use for MUB6 repo work. Review and repair MUB6 code and Lean evidence, maintain lessons, prioritize derivations."
operad_source_colours: ["Code", "Proof"]
operad_target_colour: "Receipt"
operad_arity: 2
operad_residual: "unknown"
families: [governance, verification, math, techne]
---

# mub6_manager

Manage the MUB6 research repository from its actual definitions, computations,
and theorem dependencies. The invocation name is `$mub6-manager`; the display
name preserves the requested `mub6_manager` spelling.

AuthorityEffect: None.

## Start with current evidence

Locate the repository with `git rev-parse --show-toplevel`, record HEAD and
`git status --short`, and read its `agents.md` / `AGENTS.md`. Read the relevant
entries in [references/lessons.md](references/lessons.md), then verify facts that
the current checkout can have changed. The lesson log is a dated aid, not a
certificate or a source of permission.

Useful entry points, relative to the repository root:

- Python: `code/mub_verify/` (research verifiers); the retired tests are in `tests/mub_verify_python_tests_2026-09-25.zip`.
- Rust: `engine/crates_rs/core_mub/` in the larger Cargo workspace.
- Abstract interfaces: `lean4/gluing/`.
- Concrete complex Hilbert definitions and reflection:
  `lean4/012_mutually_unbiased_bases/MUB/`.
- Latest spot-check evidence: `research/spotcheck_2026_09_18.md`.
- Initial prioritized research targets: `research/next_derivations_2026_09_18.md`.

Preserve unrelated changes. For a requested random review, record the candidate
population, seed, algorithm, baseline SHA, and selected paths before reading the
sample. Distinguish sampled files from supporting dependency reads.

## Check the meaning as well as the execution

Use exact rational or exact cyclotomic arithmetic for certifiers, with rigorous
rational enclosures for continuum parameters. Do not introduce floating-point
acceptance gates. General complex phase parameters are not automatically
restricted to the finite roots represented by a cyclotomic fixture.

Read the type and body behind a mathematical name. A remainder inequality is
not a root-of-unity theorem; a predicate named `FiniteCornerWitness` may not
contain finiteness data. An explicit hypothesis, Boolean declaration, or theorem
name is not a discharged result. Inspect caller-supplied hypotheses and actual
axiom dependencies before reporting a theorem's scope.

For covers, check dimensions, containment, coverage, and overlap in the domain's
non-fixed coordinates, as well as each leaf's analytic bound or off-domain
witness. Reject missing regions, duplicate leaves, empty successful audits,
and silently omitted failed samples. Finite sampling and a local replay of
generated boxes do not validate an entire persisted receipt.

For Lean, require no `sorryAx` and only `[propext, Classical.choice, Quot.sound]`
for published results. A successful build does not establish that condition.
Retain `by rfl` checks for concrete cover receipts in `KernelReflection*.lean`;
also check the bridge from those data to actual matrices, residuals, and domains.
Do not replace a missing mathematical derivation with a custom axiom.

## Repair and verify proportionately

Reproduce a substantive defect with a small counterexample, fix the responsible
boundary, and run the affected checks. Keep transcripts, build output, and
temporary probes under ignored `scratch/`.

Use an available Python 3.11+ interpreter. The Python test suite was retired on 2026-09-25 and archived in `tests/mub_verify_python_tests_2026-09-25.zip`; the exact algebra is exercised by the Rust `core_mub` tests (`cargo test -j 1 -p core_mub` from `engine/crates_rs`).
The former command was
`python -m pytest tests/mub_verify -n 8 --basetemp=scratch/pytest_tmp`.
If that directory is occupied or inaccessible, use a fresh path under
`scratch/<run>/pytest_tmp` and record the reason; pytest can delete an existing
basetemp. Keep pytest's cache in that run directory if the shared cache is locked.

Run `lake build` from each affected package using its pinned `lean-toolchain`,
and inspect `#print axioms` for the changed results. Target Rust tests narrowly,
for example `cargo test -p core_mub --lib <module>::tests --offline`; a short
substring can unintentionally select a long `deep_run` test. Do not describe
unrun tests, cached builds, or metadata declarations as fresh proof replay.

## Choose derivations and retain lessons

Prioritize missing semantic or coverage links that block an existing conditional
theorem. Give each proposed derivation an explicit statement, hypotheses, current
theorem/receipt pointers, a bounded deliverable, and a falsification or completion
check. Separate a feasible first lemma today from completion of the larger
research problem. Verify cited primary literature before adopting its scope;
single-matrix classification does not supply simultaneous triple compatibility.

When the user requests lesson retention, append a compact dated entry to
`references/lessons.md`: evidence path/SHA, what worked, what failed, current
scope, and a condition for revisiting it. Keep conjectures and unresolved gaps
separate from verified outcomes. Do not copy transcripts or update Codex's
central memory store through this skill.

Keep the repository copy of this skill as the maintained source when available;
after an authorized lesson update, synchronize the installed copy and verify
their hashes. Do not overwrite divergent installed lessons without reconciling
their content. End with actual changes, checks, and remaining limits.
