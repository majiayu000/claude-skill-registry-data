---
name: sprout-and-wrap
kind: skill
status: ready
provenance:
  principles:
  - P031
  - P032
  - P012
  - P009
  - P144
  - P084
  claims:
  - C00109
  - C00110
  - C00111
  - C00112
  - C00116
  - C00115
  - C00117
  - C00118
  - C00119
  - C00120
  source_anchors:
  - 1d83dc6f489c-c0005
  authored_from_digest: e45ff16a065cb53c9ebff106b5a31546111a1f40af79c1143271560d5e957085
---

# Sprout and wrap

## Purpose

Add new functionality to code you cannot yet get under test by writing the new code
**test-first and kept separate** from the old, untested code — rather than editing new logic
inline into an untested method. Four techniques cover the cases; all keep new and old
behaviour independent and avoid temporal coupling.

## When to use

- You must add a feature but cannot cheaply get the surrounding code under test.

Do **not** apply when the surrounding code can be brought under test quickly — then cover it
and make the change directly (see `cover-before-change`).

## Procedure

1. **Confirm the precondition:** the surrounding code cannot cheaply be brought under test.
   (If it can, stop and cover-then-change instead.)
2. **Choose the technique** by intent and whether the class is instantiable (P144 — Sprout
   Method when the existing method already communicates a clear algorithm; move to Wrap when
   the new behaviour should not interleave with the existing logic):

   | Situation | Technique | Move |
   |-----------|-----------|------|
   | Change is a distinct piece of new code, host method exists & is editable | **Sprout Method** (P031) | Write the new behaviour as a new, test-driven method (write the call first, commented out); call it from the existing code. Do not add the logic inline to the untested method. |
   | Class can't be instantiated in a harness within reasonable effort | **Sprout Class** (P032) | Put the new change in a separate new class, developed test-first; the source class uses it. |
   | New behaviour runs entirely before or after existing logic, without enlarging the method | **Wrap Method** (P012) | Rename the original; create a same-signature method with the original's name that calls the new behaviour and the renamed original. Keeps the two independent (no temporal coupling). |
   | Wrapping at class granularity | **Wrap Class** (P009) | A new class (decorator-style, same interface) holds the added behaviour and delegates to the original. |

3. **Write the new code test-first (TDD).** The sprouted/wrapped unit is new, so it can be
   driven by tests from the start.
4. **Keep new code independent of old code** to avoid temporal coupling.
5. **Know the hazards (P084).** Sprouting and wrapping without tests do not improve the
   existing code, can duplicate untested code, and leave fear in place; treat them as a way
   to add tested code now, and return to cover and improve the old code when feasible.

## Inputs

- The feature to add, the host method/class, and whether that class is instantiable in a
  harness.

## Output

A named technique (Sprout Method/Class, Wrap Method/Class), the new test-first unit to
create, the call/delegation wiring to the existing code, and a note on the hazards to revisit.

## References

- `cover-before-change` — the preferred path when the area *can* be covered cheaply.
- `dependency-breaking-techniques` — Extract Interface / Extract Implementer for Wrap Class.
- `characterization-testing` — covering the old code later, once feasible.

## Provenance

Derived from principles P031 (Sprout Method), P032 (Sprout Class), P012 (Wrap Method), P009
(Wrap Class), P144 (choosing sprout vs wrap by intent), and P084 (hazards of sprout/wrap
without tests). Source is distillation-only; paraphrased, not quoted.
