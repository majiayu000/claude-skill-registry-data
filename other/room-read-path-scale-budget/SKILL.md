---
name: room-read-path-scale-budget
description: "Measure Room/SQLite read paths at realistic data volume (years of user data) and set a regression budget from the measurements rather than a round number — covers bulk-seeding an isolated database, timing only the queries that load on a UI thread, and proving the budget can actually fail. Use when a data layer has only ever been tested with a handful of rows, or before claiming a screen stays responsive as data grows."
---

# Scale budget for Room read paths

Most data tests use three rows. That proves correctness and says nothing about
the size a real user reaches. An accidental N+1 or a scan-per-row is invisible
at three rows and a freeze at three thousand.

## 1. Pick the volume from the product, not a round number

Derive it: "four sessions a week for five years" → 1,000 sessions × 5 sets.
State the derivation in the test, so the next reader can argue with the premise
rather than the number.

## 2. Seed in bulk, on an isolated database

Insert through the DAO, **not** through the domain flow — going through
`completeSession()` a thousand times measures writes and buries the read you
care about. Use a test-only database name; never the app's live file.

```kotlin
db = MonarchDatabase.create(context, TEST_DB)   // isolated
repeat(SESSIONS) { i ->
    val id = db.sessionDao().insertSession(...)
    db.sessionDao().insertSets( (0 until SETS).map { ... } )   // one batch call
}
```

## 3. Time only what loads on a UI thread

Journal/history, any aggregate a screen header shows, and export. Collect into a
map so one failure reports every number:

```kotlin
val timings = LinkedHashMap<String, Long>()
suspend fun time(label: String, block: suspend () -> Int) {
    val t0 = System.nanoTime()
    val size = block()
    timings[label] = (System.nanoTime() - t0) / 1_000_000
    assertTrue("$label returned nothing", size > 0)   // guards a vacuous zero
}
```

The `size > 0` check matters: a query that returns an empty list is fast and
proves nothing.

## 4. Get the numbers BEFORE choosing the budget

Set the budget to `1L`, run, read the assertion message. That single step does
two jobs — it reports the real timings and it proves the check can fail.

```
read paths slower than 1ms at 1000 sessions:
  {journal=76, titles ledger=122, export=131, completed count=0}
```

Then set the budget about an order of magnitude above the slowest measurement
and record the measurements in a KDoc beside it.

**A budget with 30x headroom is decoration.** If the slowest path is 131ms, a
4,000ms budget can never fail; 1,500ms still tolerates slower hardware while
catching a regression that lands in seconds.

## 5. What this is and is not

It is a guard against an order-of-magnitude regression. It is not a benchmark:
an emulator on a software renderer is far slower than a phone, and the numbers
move with the host. Say so in the test, or someone will later "fix" it by
tightening the budget until it flakes.

## Traps

- An instrumented gate run **uninstalls the app**; a device sweep straight after
  one drives an empty launcher.
- `runTest` makes `delay` virtual — use `runBlocking` when anything must wait in
  real time.
- Assert the fixture size first (`assertEquals(SESSIONS, completedCount())`),
  otherwise a seeding failure reads as excellent performance.
