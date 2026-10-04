---
name: characterization-testing
kind: skill
status: ready
provenance:
  principles:
  - P093
  - P063
  - P092
  - P140
  - P074
  - P005
  claims:
  - C00305
  - C00306
  - C00307
  - C00308
  - C00309
  - C00310
  - C00311
  - C00299
  - C00300
  - C00301
  source_anchors:
  - 1d83dc6f489c-c0013
  authored_from_digest: c8239051fcbf383cd409d7fa8a7c04be24e4ccf2ad19546064430688c9076fc9
---

# Characterization testing

## Purpose

Write tests that document what legacy code **actually does**, not what it was supposed to
do, so that future changes can be sensed against real current behaviour (P093). Deployed
callers depend on the actual behaviour, so these tests pin behaviour — they do not bless it.
The goal is to write correct code consistently, not to hunt for bugs, which is usually
misdirected effort (P074).

## When to use

- You need tests around legacy code whose intended behaviour is unknown or undocumented.
- You are about to modify a path and must confirm your tests actually cover it (P005).

Do **not** apply when a clear specification already exists and specification-based tests are
appropriate — write to the spec instead.

## Procedure

**Writing a characterization test (the assert-fail-observe-expect loop, P093):**

1. Get the code into a test harness so it can be exercised (break dependencies first if
   needed — see `sensing-and-separation`, `seam-model`).
2. Write an assertion you expect to **fail** (assert a value you know is probably wrong).
3. Run it; let the failure message tell you the **actual** behaviour the code produces.
4. Change the test to **expect that actual behaviour**.
5. Repeat for the next behaviour. Stop when the behaviours relevant to the planned change
   are pinned.

**Characterize by reading (P063):** get curious and write tests until you understand the
code, then add tests until confident they cover the behaviour you must preserve — rather than
treating it purely as a black box.

**Do targeted testing (P005):** verify the tests cover the exact code you will change — test
the branch that will change and confirm it is actually hit — so a "sunny day" test cannot
pass while a changed method silently truncates or mis-converts a value.

**Pinch-point tests are scaffolding (P092):** tests written at a pinch point to characterize
a cluster are temporary. Once behaviour is pinned, write narrower per-class unit tests and
then delete the pinch-point tests.

**When you find a bug while characterizing (P140):** fix it directly only if the system was
never deployed. If it is deployed, **keep the test**, and analyse how to fix the behaviour
without ripple effects rather than correcting it on the spot — deployed callers may depend on
it. Do **not** silently "fix" it.

## Inputs

- The code unit and the specific path/conversions the planned change will affect.
- Whether the code is deployed (governs the bug-found escalation).

## Output

A set of characterization tests pinning current behaviour along the relevant path, plus a
list of any behaviours flagged suspicious and escalated rather than changed.

## References

- `sensing-and-separation`, `seam-model` — getting the code into the harness first.
- `effect-reasoning` — choosing where the tests should sit.
- `legacy-code-change-algorithm` — this is step 4 of the algorithm.

## Provenance

Derived from principles P093 (characterization / assert-fail-observe-expect), P063
(characterize by reading), P092 (pinch-point scaffolding), P140 (bug found while
characterizing), P074 (write correct code, do not hunt bugs), and P005 (targeted testing).
Source is distillation-only; paraphrased, not quoted.
