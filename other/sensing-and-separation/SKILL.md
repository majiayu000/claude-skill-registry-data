---
name: sensing-and-separation
kind: skill
status: ready
provenance:
  principles:
  - P081
  - P051
  - P123
  - P137
  - P139
  - P057
  - P083
  claims:
  - C00053
  - C00054
  - C00055
  - C00056
  - C00058
  - C00060
  - C00061
  - C00062
  - C00063
  - C00057
  source_anchors:
  - 1d83dc6f489c-c0003
  authored_from_digest: 7254266886288f25886ec43c11a26e265a36178a0777249ea8f5d2a4d6c23a7c
---

# Sensing and separation

## Purpose

Classify *why* a dependency is blocking a test and choose the breaking move accordingly.
There are two reasons to break a dependency to get code under test: **sensing** — you
cannot access values the code computes — and **separation** — you cannot get the code into
a test harness to run at all (P081). The distinction matters because faking a collaborator
is the dominant technique for sensing (P051), while there are many techniques for
separation, and the incisions made before tests exist must stay conservative.

## When to use

- A class cannot be instantiated in a harness, or its computed effects cannot be observed in
  a test (P083 — the four common obstacles: hard construction, harness will not build, bad
  constructor side effects, undetectable side effects).

Do **not** apply when the code is already isolable and its effects are directly observable —
no dependency needs breaking.

## Procedure

1. **State what you are trying to test** at the change point.
2. **Classify the blocker (P081):**
   - **Sensing** — the code runs but you cannot observe the value/effect it produces
     (e.g. it writes to a collaborator instead of returning).
   - **Separation** — the code cannot even be instantiated or run in the harness (e.g. the
     constructor needs a live database or network; globals and singletons are among the
     hardest such dependencies, P057).
   A single dependency can block both; name each reason.
3. **For sensing → use a fake object (P051).** Substitute a fake that impersonates the
   collaborator so the test can sense effects *through* it (record the calls/values the code
   under test sends). Prefer a plain hand-written fake; reach for a mock (a fake that asserts
   internally) only when you must write many fakes and the language makes hand-writing them
   costly (P123).
4. **For separation → make the collaborator fakeable (P137).** Introduce a seam at the
   blocking collaborator — typically **Extract Interface** — so the class under test can hold
   either the real collaborator or a fake (see `dependency-breaking-techniques`,
   `seam-model`). For an irritating parameter that is slow, unreliable, or has side effects,
   extract an interface on it and pass a fake supplying only what the test needs (P139).
5. **Make the incision conservatively.** Before any tests exist, make minimal,
   signature-preserving changes only — even if the code temporarily looks worse. Accept the
   "scar"; heal it once tests cover the area. Do not bundle cleanup with the break.
6. **Verify** the code now instantiates and its effects are observable, then proceed to
   characterization tests.

## Inputs

- The code unit, the change point, and the blocking collaborator(s)/dependencies.
- The language in use (affects which seam/break techniques apply).

## Output

For each blocking dependency: its reason class (sensing / separation / both), the breaking
technique to apply (fake object, Extract Interface, …), and a note that the pre-test
incision must stay conservative and signature-preserving.

## References

- `dependency-breaking-techniques` — the Extract Interface and fake-object technique detail.
- `seam-model` — where and how to insert the substitution point.
- `characterization-testing` — what to do once the code is in the harness.

## Provenance

Derived from principles P081 (sensing vs separation), P051 (fake objects), P123 (fake vs
mock), P137 (make a collaborator fakeable), P139 (irritating parameter), P057 (globals /
singletons), and P083 (harness obstacles). Source is distillation-only; paraphrased, not
quoted.
