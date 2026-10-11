---
name: slice-check
description: Verify a multi-phase plan is composed of vertical slices (each phase touches data + behavior + test, end-to-end) rather than horizontal layers (whole DB layer first, then whole API, then whole UI). Use before exiting plan mode on any plan with 3+ phases, or when the user asks to "decompose this", "break this into phases / steps / issues".
---

# Slice-check

Agents tend to over-build horizontally — whole DB layer, then whole API layer, then whole UI — because each layer "looks coherent" individually. The cost: nothing works end-to-end until the last phase, and context windows cannot hold a finished feature. The discipline is vertical slices (tracer bullets): each phase delivers a thin path through *all* layers, end-to-end.

## The test for each phase

A phase is a valid vertical slice if and only if it touches **all three**:

1. **Data** — schema, types, state shape, persistence, or input shape.
2. **Behavior** — the logic, transport, computation, or rendering that uses the data.
3. **Test** — at least one assertion (unit, integration, or manual repro script) that fails before this phase and passes after.

If a phase touches only one or two, it is a horizontal layer disguised as a slice. Reject it and re-decompose.

## What to do when slicing fails

If you cannot decompose into vertical slices, the request is one of:

- **A spike** — too uncertain to plan; prototype it first (use the `prototype` skill, then come back to slicing).
- **A refactor** — restructuring, no new behavior. Slicing doesn't apply; use checkpoint verification instead ("after step N, the test suite is still green; nothing user-visible changed").
- **Too small for phasing** — one slice, just code it.

State which case applies and exit plan mode accordingly.

## Output format (this exact structure)

```
Phase 1 — <short name>
  Data:     <files / types / schema touched>
  Behavior: <logic / transport added>
  Test:     <assertion that proves this phase works end-to-end>
  Exit:     <observable criterion: what a reviewer can run to see it works>

Phase 2 — <short name>
  Data:     ...
  Behavior: ...
  Test:     ...
  Exit:     ...
```

Reject — out loud — any phase that cannot fill all four lines.

## Anti-patterns

- ❌ "Phase 1: schema. Phase 2: API. Phase 3: UI." — pure horizontal, no slice runs end-to-end until phase 3.
- ❌ "Phase 1: data + behavior. Phase 2: tests." — tests are not a separate phase; they belong inside the phase that introduced the behavior.
- ❌ Slicing a refactor — refactors don't add behavior; vertical slicing doesn't apply.
- ❌ "Phase 1: setup tooling. Phase 2: build the feature." — setup is one step inside the feature's first slice, not its own phase.
- ❌ A 6+ phase plan where none of the first 5 are usable on their own — that is one giant slice; re-think.

## Integration with other skills

- After `slice-check` accepts the plan → use `premortem-bind` on the high-risk slices.
- If `slice-check` rejects the plan → drop to `prototype` for the uncertain part, then re-plan.
- `to-issues` will consume vertical-slice phases directly as independent issues.

$ARGUMENTS
