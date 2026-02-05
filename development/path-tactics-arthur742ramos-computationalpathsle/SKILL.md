---
name: path-tactics
description: Use ComputationalPaths path tactics to automate common RwEq goals (path_simp/path_auto/path_normalize), and structure calc-based proofs cleanly.
---

# Path Tactics (RwEq automation)

This skill focuses on reducing boilerplate in `RwEq` proofs by using the project’s path tactics and a few repeatable proof shapes.

## Import

Most automation lives in:

```lean
import ComputationalPaths.Path.Rewrite.PathTactic
```

## What to try first

### 1) `path_auto`

Use for “standalone” goals that are mostly groupoid laws, cancellation, associativity reshaping, etc.

```lean
theorem t : RwEq (trans (symm p) p) refl := by
  path_auto
```

### 2) `path_simp`

Use inside longer proofs to close the last “cleanup” step (unit laws, trivial cancellations).

```lean
-- ... after rewriting/congruence steps
path_simp
```

### 3) `path_normalize`

Use when the goal is blocked because both sides are definitionally different parenthesizations.

```lean
path_normalize
```

## Proof structuring patterns

### Prefer `calc` chains for readability

This project commonly uses a `calc` chain with the `÷` notation for `RwEq`:

```lean
theorem my_rweq : RwEq p q := by
  calc p
    _ ÷ p' := h1
    _ ÷ p'' := h2
    _ ÷ q := by
      path_simp
```

### Combine tactics with targeted lemmas

When you need one key lemma application (e.g. associativity or congruence) and the rest is routine:
1. apply the key lemma(s) with `apply` / `exact`
2. finish with `path_simp` / `path_auto`

## Troubleshooting

- If `path_auto` fails, normalize both sides (`path_normalize`) and retry.
- If the goal is “almost solved” but has extra `trans refl _` / `trans _ refl`, use `path_simp`.
- For congruence-heavy goals, apply the project lemmas (e.g. `rweq_trans_congr_left/right`) to reduce the goal, then finish with tactics.

