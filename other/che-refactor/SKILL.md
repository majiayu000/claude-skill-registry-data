---
name: "che-refactor"
description: "Behaviour-preserving refactoring in the Fowler sense. Takes existing code and applies established refactorings (extract function, inline, extract variable, replace conditional with polymorphism, split phase, ...) to improve readability, maintainability, scalability and testability WITHOUT changing observable behaviour. PRECONDITION: a green test safety net; if coverage is missing the first step is characterization tests, not refactoring. Each step is small, tests green after it, atomic commit. Invocable standalone and recommendable by che-pair. NEVER run inside che-ship."
---

# Che — Refactor (behaviour-preserving)

> **SHARED REFERENCES (CANONICAL — do NOT duplicate the body here):**
> - Simplicity Bias + blast radius: `engineering-contracts` §1
> - Diff review + architecture boundaries: `che-code-review` skill
> - LEAN scanner (L1-L13): `che-scope-checker` skill
> - Increment checkpoint loop: `che-pair` skill

---

## §0 THE DEFINING PROPERTY

Refactoring is **behaviour-preserving**. A change that alters observable behaviour is NOT a refactor —
it is a feature or a fix. This skill refuses to mix the two.

---

## §1 PRECONDITION (fail-fast)

1. **A green test safety net exists** for the code being refactored. Run the tests BEFORE starting.
2. If coverage is missing → the FIRST commit is **characterization tests** that pin the current
   behaviour, not a refactoring. Refactoring without a net is just editing.

---

## §2 PROCESS (small steps, verify each)

1. **Identify the smell** and name it from the catalogue (long function, duplicated code, feature envy,
   primitive obsession, conditional complexity, …).
2. **Name the refactoring** that removes it (extract function, inline, extract variable, replace
   conditional with polymorphism, split phase, …).
3. **Apply ONE small step.**
4. **Run the tests — they must be green.** Red → revert the step; do not "fix forward".
5. **Atomic commit** per coherent step.
6. Repeat until the smell is gone. **Stop when it is gone** — no gold-plating.

---

## §3 HARD RULES

- **Behaviour preserved** — tests green before and after; no new observable behaviour.
- **No feature, no fix, no new dependency** in a refactor commit. Found a bug? Stop, log it, handle it
  separately.
- **Tests are not modified** except to ADD characterization tests — never to make a refactor pass.
- **Blast radius bounded** — a repo-wide refactor is a red flag → split into increments / `gh-stack`.
- **Measurable target** — each refactoring declares which signal it improves (cyclomatic complexity,
  duplication, coupling/fan-out, coverage). "Looks cleaner" is not a target.

---

## §4 INTEGRATION

- **Standalone**: `/che-refactor` on a worktree + a scope.
- **Recommended by `che-pair`**: a pair finding may say "extract this"; the refactor itself is a
  separate step with its own tests.
- **NEVER inside `che-ship`**: ship is commit + push + PR; refactoring there inflates the diff at merge
  time.

---

## §5 OUTPUT

- Refactored code (behaviour-preserving) — inside the worktree, as usual.
- A **refactor log** written as a worktree artifact (never inside the worktree, never the fallback):
  1. `eval "$(che compute_paths "$WORKTREE_ROOT" "$SESSION_ID" --cwd "$PWD")"`
  2. `REFACTOR_LOG="$(che output_path report refactor-log "$RELATED_ID" workspace md)"`
     → `$CHE_WORKSPACE_SHARED/reports/<related_id>/<YYYYMMDD-HHMMSS>-refactor-log.md`
  3. Write it with the content on **stdin**: `che write_file_atomic "$REFACTOR_LOG" <<'LOG_EOF' … LOG_EOF`
     — smell → refactoring → files → signal improved.
- `decisions.log` entries via `che decision_append`: `REFACTOR_STEP` per step, `REFACTOR_DONE`
  (smells, signals, coverage, path).

---

## §6 WHAT IT IS NOT

- **Not a rewrite** · **not a feature** · **not a performance optimisation** (unless the smell IS the
  performance issue) · **not a licence to change tests**.
