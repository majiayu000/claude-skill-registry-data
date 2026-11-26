---
name: nasqret-playbook
description: "Build a fresh route slate when a frontier move changes the shape of the search. Diff adjacent public winners, name their visible mechanisms (qubit shelf, lifetime move, Toffoli move, nonce dependence), run equal-size pilots, sort each route into tail-sensitive, structurally dirty, score-dead or validation-ready, and send compute only to the last group. Named for nasqret, whose broad sweeps it follows."
license: MIT
---

# Rundumschlag (nasqret-playbook)

*Nasqret-style route factory*

Use when a frontier move changes the shape of the search.

## Goal

Avoid chasing stale single knobs. Build a route slate, test small, then scale
only the routes that have landability and a validator.

## Steps

1. Refresh the current target.
2. Diff adjacent public winners, not old endpoints.
3. Extract visible mechanisms: qubit shelf, memory/lifetime move, Toffoli move,
   nonce/island dependence, validation note.
4. Generate multiple route candidates.
5. Run equal-size pilot checks.
6. Classify each route:
   - tail-sensitive,
   - structurally dirty,
   - score-dead,
   - validation-ready.
7. Dispatch compute only for validation-ready routes.
8. Write negative evidence back to memory so dead lanes stay dead.

## Output

Return a route slate with:

- route ID,
- expected edge,
- validator,
- kill gate,
- owner,
- credit note.

## Credit

Inspired by nasqret / Bartosz Naskrecki's public frontier behavior and
group-discussion process notes. Do not imply copied code.
