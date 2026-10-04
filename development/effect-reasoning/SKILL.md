---
name: effect-reasoning
kind: skill
status: ready
provenance:
  principles:
  - P004
  - P041
  - P061
  - P043
  - P062
  - P091
  claims:
  - C00264
  - C00265
  - C00266
  - C00267
  - C00269
  - C00270
  - C00271
  - C00272
  - C00282
  - C00260
  source_anchors:
  - 1d83dc6f489c-c0012
  - 1d83dc6f489c-c0011
  authored_from_digest: 6fde9d1f34e20ea6fafe16da228fabf29740f7aa3e5c14472770fc246f4ba6b3
---

# Effect reasoning

## Purpose

Decide *where* to put tests by reasoning about the **effects** of a change rather than
guessing. Use effect sketches — a bubble per affected variable or return value with arrows
to what it can change — to find where to test (P004), then place characterization tests where
they will actually sense the change, ideally at **pinch points**, narrowings where tests on
one or two methods detect changes across many (P043).

## When to use

- You must choose the smallest set of test points that will sense a change rippling across
  several methods or classes.

Do **not** apply when the change is local and its single test point is obvious — just test
there.

## Procedure

1. **Mark the change point(s).** Identify what the change will modify.
2. **Sketch the effects (P004).** From each change point, draw a bubble per affected variable
   or return value with arrows to what it can change, building an effect sketch of everything
   the change can affect.
3. **Trace the three ways effects propagate (P061):** used return values, mutated objects
   passed as parameters, and mutated static or global data. Reason forward about the effect
   chain, which propagates to callers up to a system boundary while unrelated code keeps its
   behaviour (P041).
4. **Find interception points (P062).** Trace effects outward from the change points and
   prefer interception points close to the change — fewer steps make a stronger safety
   assurance.
5. **Look for a pinch point (P043).** Find a narrowing where one or two methods sit on the
   path of changes that fan out across many; tests there detect a wide set of changes with
   few tests. A pinch point is also a natural encapsulation boundary and can reveal hidden
   classes worth extracting later (P091).
6. **Place characterization tests** at the chosen interception/pinch points (see
   `characterization-testing`).

## Inputs

- The change point(s) and enough of the call/data structure to trace effects.

## Output

An effect sketch for the change, the identified interception/pinch point(s), and the
recommended test points — the minimal set that senses the change — plus any pinch point
flagged as a natural encapsulation boundary.

## References

- `characterization-testing` — how to write the tests placed at the chosen points.
- `legacy-code-change-algorithm` — this supports step 2 (find test points).

## Provenance

Derived from principles P004 (effect sketches), P041 (forward effect-chain reasoning), P061
(three propagation mechanisms), P043 (pinch points), P062 (interception points close to the
change), and P091 (feature sketches reveal hidden classes / encapsulation boundaries). Source
is distillation-only; paraphrased, not quoted.
