---
name: kotlin-test-file-overwrite-guard
description: "Add test coverage to a Kotlin/Gradle repo without silently overwriting existing tests, and keep fixtures from asserting premises a grep got wrong. Use before creating a test file, or when a new test fails in a way that looks like a production bug but isn't."
---

# Adding tests without destroying tests

Two failure modes that both produce confident, wrong work. Observed in a
Kotlin/Gradle Android repo; neither is repo-specific.

## 1. Never write to a path you have not confirmed is new

Symptom: a commit whose message says *add coverage* shows deletions in the
diffstat, and the suite total rises by fewer tests than were written.

    1 file changed, 76 insertions(+), 44 deletions(-)   # a "new" file cannot delete
    unit: 174 -> 177                                    # but 7 tests were added

Rules:

- Before writing, answer *does this exist?* with `git log --oneline -3 -- <path>`
  , not with a heuristic or a coverage script written minutes earlier.
- Path exists: read it, then edit. Write is only for genuinely new files.
- A detector with known false positives (it called an obviously-tested file
  untested) also has false negatives. Distrust it in both directions.

Recovery if it already happened:

    git show <commit>^:<path> > .tmp/prev.kt   # the overwritten version
    grep -c "@Test" .tmp/prev.kt               # what was destroyed

Merge rather than choose: old tests often assert something a rewrite misses
(e.g. *only measured sites appear in the map* - a `latest.size` assertion).
Verify each recovered test name is back, then sweep the session:

    for c in <commits>; do git show --numstat --format="" $c | awk '$2>0 {print $3}'; done

## 2. Make the fixture prove its own premise

A test assuming "this name is not in the catalogue/seed/enum" will one day fail
for an unrelated reason, and the failure looks exactly like a production bug.

- A case-sensitive grep of one file is not proof of absence. Catalogues are
  often seeded from more than one place (a static list *and* a feature module).
- Assert the premise against the real source of truth:

      assertEquals("the fixture name must be unknown here", null, dao.byName(foreign))

- Prefer that over a "surely absent" literal: the literal works today and rots
  when the catalogue grows; the assertion cannot.
- Name enum members explicitly (`MeasurementSite.WAIST`) rather than
  positionally (`entries.first()`), which silently re-targets on reorder.

## Diagnose in the assertion, not in the source

When a new test fails, put the facts in the assertion message and run once
instead of reading production code for theories:

    assertTrue("restored=$restoredNames stored=\"${row?.name}\"", restored.contains(foreign))

The mismatch between what the fixture wrote and what the database stored is
usually the whole answer. In the observed case the archive said `Ring Muscle-Up`
while the stored row read `Ring Muscle-up`, proving case-insensitive matching
had found a pre-existing row and the production code was correct all along.
