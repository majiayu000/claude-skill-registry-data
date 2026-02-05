---
name: reflex
description: Build and debug Reflex (rx) UIs in this repo. Use for editing ui/*.py, choosing rx components, fixing Var/conditional/foreach issues, and applying responsive/layout patterns from the Reflex docs.
---

# Reflex UI Skill

Use this skill whenever the task involves Reflex UI code (`ui/*.py`), rx components, state vars, event handlers, or front-end layout/styling issues.

## Quick rules

- **Never use Python `if/else` with state vars** in component trees. Use `rx.cond` or `rx.match`.
- **Never use Python `for` loops over state vars** in component trees. Use `rx.foreach`.
- **Var operations** use bitwise operators: `&`, `|`, `~` for logic.
- **Selects**: use `rx.select(["a", "b"])` or the `rx.select.root` family (no `rx.option`).
- **Responsive**: prefer `rx.breakpoints(...)` on props (e.g., `columns=rx.breakpoints(...)`).
- **Layout**: use `rx.grid` for grids, `rx.flex` for rows/columns.

## When debugging compile errors

1. Look for `VarTypeError` or "Cannot convert Var to bool" and replace `if`/`or`/`and` with `rx.cond` / `&` / `|` / `~`.
2. If a list/iterable is a state var, render it with `rx.foreach` (do not `join()` or list‑comprehend in Python).
3. For responsive direction/columns, use `rx.breakpoints` instead of lists.

## Reference files

- Library component patterns: [references/library.md](references/library.md)
- Conditional + foreach rules: [references/components.md](references/components.md)
- Responsive rules + breakpoints: [references/styling.md](references/styling.md)
- State vars + setters guidance: [references/state.md](references/state.md)
- Examples & patterns from `/Users/eric/git/reflex-examples`: [references/examples.md](references/examples.md)
