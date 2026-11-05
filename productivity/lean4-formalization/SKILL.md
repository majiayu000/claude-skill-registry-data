---
name: lean4-formalization
description: Formalize mathematical definitions, theorem statements, and proofs in Lean 4 with Mathlib. Use when converting LaTeX results to Lean, checking Lean files, designing inspectable formal definitions, running Lake/Lean on the remote worker, interpreting Lean errors, or validating that a formal proof has no sorry/admit/axiom gaps.
---

# Lean4 Formalization

Formalization is part of the mathematical audit, not just a translation task.
First make the statement inspectable, then make the proof check.

## Execution Policy

- Use the project-configured remote worker (`LEAN_REMOTE_HOST`) for substantial Lean/Lake work.
  Keep host names and project paths in the project configuration.
- Do not run nontrivial Lean/Lake builds locally unless the local `MemAvailable` permits a useful
  `prlimit --as` at no more than 75% of free RAM.
- Always run heavy Lean/Lake commands with `nice` and `prlimit`; do not count swap as usable memory.
- Use the sync-and-run wrapper when working from a research repo:

```bash
scripts/lean_worker_sync_run.sh --sync-mode archive --sync-path formalization \
  --commit "Formalize theorem X" --stage formalization --workdir formalization -- lake build
scripts/lean_worker_sync_run.sh --workdir formalization -- lake env lean Formalization/Main.lean
```

This wrapper can commit/push local changes, clone or pull the repo on the worker, and run the Lean
command under `nice` and `prlimit`. Prefer `--sync-mode archive --sync-path formalization` for
ordinary research repos: it does not require GitHub credentials on the worker, avoids copying large
PDF/build artifacts, and makes the local machine the Git authority. The wrapper automatically runs
`lake exe cache get` before `lake build` unless `--no-cache-get` is passed.

- Use the lower-level helper for direct commands in an existing worker project:

```bash
.claude/skills/lean4-formalization/scripts/remote_lean.sh lake build
.claude/skills/lean4-formalization/scripts/remote_lean.sh lean Formalization/MyFile.lean
```

Set `LEAN_REMOTE_WORKDIR` to the target project directory on the worker.

## Workflow

1. **Choose the scope.** Start with one definition, lemma, or theorem. Avoid formalizing a whole paper
   before the foundational vocabulary is stable.
2. **Create a translation ledger.** For each LaTeX object, record the informal name, Lean name, type,
   hypotheses, theorem source, and any deliberate mismatch.
3. **Formalize definitions first.** Prefer definitions whose printed types are understandable to a
   human mathematician. Use `#check`, `#print`, and small examples before writing theorems.
4. **State the theorem before proving it.** Make the theorem statement human-reviewable: inspect the
   full elaborated type and compare every quantifier, hypothesis, coercion, finiteness condition, and
   nonemptiness assumption with the LaTeX source.
5. **Prove incrementally.** Replace `by sorry` with structured proof blocks, run Lean after each
   meaningful step, and use the error messages to refine terms, imports, typeclass assumptions, and
   statement shape.
6. **Validate the artifact.** A theorem is valid only after the target file or Lake package checks with
   no `sorry`, `admit`, `axiom`, or placeholder theorem used to close the proof.

## Statement Discipline

- Keep Lean theorem names close to the LaTeX labels when possible.
- Prefer explicit theorem variants over hidden coercion-heavy statements. A slightly longer statement
  that a human can inspect is better than a compact one whose meaning depends on typeclass inference.
- Separate reusable definitions from proof-local abbreviations.
- If the Lean statement is stronger, weaker, or differently parameterized than the LaTeX statement,
  record that explicitly in the ledger and do not present it as the same theorem.
- Use existing Mathlib definitions whenever they match the mathematical object. If a custom definition
  is introduced, add small lemmas or examples that confirm it behaves as intended.

## Lean Feedback Loop

- Use `#check` to inspect constants and theorem types.
- Use `#print` for local definitions and important imported facts.
- Use `set_option pp.all true` sparingly when coercions or implicit arguments are suspicious.
- Use `lake env lean <file>` or `lake build` from the project root; prefer `lake build` before declaring
  a repo-level result valid.
- Before `lake build`, run `lake exe cache get` or use `scripts/lean_worker_sync_run.sh`, which does
  this automatically. This prevents needless Mathlib recompilation when cache artifacts are available.
- Treat parser/type errors as statement feedback first. Many proof failures are actually bad
  definitions, missing hypotheses, or theorem statements that do not match the intended mathematics.

## Forbidden Validation Shortcuts

- Do not accept a file that contains `sorry`, `admit`, `axiom`, `unsafe`, or a theorem whose proof is
  delegated to a newly introduced unproved placeholder.
- Do not hide a hard mathematical gap inside a definition or typeclass instance.
- Do not replace a theorem by a weaker statement without recording the mismatch.
- Do not trust a proof term unless Lean has checked the file in the intended Lake project.

## References

- Read `references/project-workflow.md` when creating or maintaining a Lean project.
- Use `scripts/lean_worker_sync_run.sh` for repo sync + remote checking.
- Use `scripts/remote_lean.sh` for low-level remote guarded execution.
