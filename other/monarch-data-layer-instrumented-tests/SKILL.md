---
name: monarch-data-layer-instrumented-tests
description: "Write and mutation-prove instrumented Room tests for Monarch's (D:\\Monarch) data layer — export/import archives, exercise-name resolution, and destructive operations — avoiding the two-seed-source trap, the live-database trap, and misreading equivalent mutations as weak tests. Use when testing Repository/DAO behaviour on device or emulator, or when an instrumented data test fails for a reason you can't explain."
---

# Monarch data-layer instrumented tests

For `app/src/androidTest/.../data/` tests exercising `Repository`, DAOs, and
archive import/export. These are the traps that cost real time, each measured.

## Never touch the live database

Open an isolated file, delete it either side:

```kotlin
context.deleteDatabase(TEST_DB)
db = MonarchDatabase.create(context, TEST_DB)   // the `name` param exists for this
repo = Repository(db)
repo.ensureSeeded()
```

Deleting `monarch.db` while `MonarchApp` holds it open produces
`SQLiteException: no such table: gacha_state` in unrelated tests — the app's
Room instance keeps writing into the unlinked inode. See `DbSnapshot`'s KDoc.

## The catalogue has TWO seed sources

`data/Seed.kt` **and** `domain/Skills.kt` (skill-tree movements are inserted as
exercises). Grepping only `Seed.kt` to decide a movement name is absent gives
false negatives — `Ring Muscle-up` lives in `Skills.kt`.

Never hardcode a "surely absent" name. Assert the premise against the database,
so it cannot rot as the catalogue grows:

```kotlin
val foreign = "Sandbag Zercher Carry"
assertEquals("the fixture name must be unknown here", null, db.exerciseDao().byName(foreign))
```

Name matching is **case-insensitive** (`exerciseIdByName[name.lowercase()]` plus
`byName` NOCASE), so an archive differing only in case reuses the row. A probe
showing archive text `Ring Muscle-Up` but stored row `Ring Muscle-up` means the
row pre-existed and was matched — not that anything rewrote the case. There is
no name normalizer anywhere in the import path.

## Real API surface (frequently mis-remembered)

| want | use |
|---|---|
| log a set | `repo.updateSet(setId, reps, weightKg, done)` |
| body stat | `repo.addStat(weightKg, bodyFatPct)` |
| completed session + sets | `repo.startSessionFromPreset(id)` → `repo.completeSession(id)` |
| read sets | `db.sessionDao().setsFor(id)` / `observeCompletedWithSets()` |
| exercise name | `db.exerciseDao().byId(set.exerciseId)?.name` — **not** on `SetLogEntity` |

`toggleSet`, `logStat`, `withTransactionForTest`, `SessionDao.observeAll` do not
exist.

## Mutation proof without vacuous greens

Delete stale results first, and print the file count — otherwise a build that
never ran echoes the previous green:

```bash
rm -rf app/build/outputs/androidTest-results
# ...run...
python -c "import glob;xs=glob.glob('app/build/outputs/androidTest-results/connected/**/*.xml',recursive=True);print('result xml files:',len(xs),'(0 = never ran)')"
```

Mutate by **line anchors**, asserting the anchors before editing; regex excision
decapitates enclosing functions. In `ExportWriter.appendSessions` the sets loop
closes with `append("]}")`, so searching forward for `append("]")` grabs the
*sessions*-array closer and breaks the file.

## Equivalent mutations are a result, not a weak test

`importArchive` is protected twice over: validation runs before the destructive
clears, **and** the clears run inside `db.withTransaction`. Mutating either alone
leaves behaviour identical — a rejected file still costs nothing. Only removing
both loses training.

Report those survivals as equivalent and say so in the test's comment with
"(measured)". Do not rework the test to detect ordering the user can't observe.

## Mutations known to bite

| mutation | assertion that fires |
|---|---|
| archive writes `done: false` for every set | *the archive must remember which sets were logged* |
| sets array emitted empty (replace lines of the loop incl. `append("]}")`) | *restored set rows expected:<N> but was:<0>* |
| clear before read, no transaction | *a refused import must not touch the completed sessions* |
| name matching made case-sensitive | *a case variant … must not create a second row* (measured: +7 rows) |
| `resolveExercise` returns null instead of inserting | *the foreign movement must be created, exactly once* |

An empty `sets` array is **restored as empty, not rejected at parse** — the
import reports success with every session, stat and XP intact and no training.
