---
name: room-migration-data-survival-test
description: "Prove a Room upgrade keeps the user's DATA, not just that the schema validates — covers the passing migration test that only seeds one settings/profile row, which any migration that drops user tables would also pass, and the mutation that proves the new assertions bite. Use when a repo has MigrationTestHelper coverage, before shipping any update over existing installs, or when a migration test's name promises more than it asserts."
---

# Room migration data-survival test

`runMigrationsAndValidate` proves the **schema** matches. It says nothing about
whether rows survived. A migration test that seeds one settings row and checks
it back is the classic false comfort: a migration that drops `sessions`,
`set_logs`, or any other user table passes it unchanged.

Losing logged user data on an app update is usually the worst bug a local-first
app can ship, and it is invisible until a real install upgrades.

## Procedure

1. **Read what the existing test asserts**, not its name. If it seeds only a
   profile/settings row, the data axis is uncovered however thorough it looks.

2. **Find the exported baseline schema** (`app/schemas/<db>/<N>.json`) and read
   the real column names/nullability of the user tables from it — not from
   today's entity classes, which have moved on.

   ```python
   s = json.loads(pathlib.Path("app/schemas/<db>/21.json").read_text())
   for e in s["database"]["entities"]:
       print(e["tableName"], [f["columnName"] for f in e["fields"]])
   ```

3. **Seed real training/user rows at the shipped baseline** with
   `helper.createDatabase(name, BASELINE).use { it.execSQL(...) }`. Cover:
   - a parent row and **two** child rows (so a count assertion can distinguish
     "some" from "all"),
   - at least one field that is device-only/private — its silent loss is the
     one a user notices last,
   - one row per additional user table (unlocks, measurements, …).

4. **Walk the whole registered chain** to `VERSION`, then read each row back
   and assert **values**, not just `moveToFirst()`. Counts plus a `SUM`/`MAX`
   catch partial loss that a row-exists check misses.

5. **Mutation-prove it.** Insert one destructive line into a real migration and
   confirm the named assertion fails:

   ```kotlin
   db.execSQL("DELETE FROM set_logs")   // inside MIGRATION_N_N+1
   ```

   Expect `both logged sets must survive expected:<2> but was:<0>`. Restore the
   file and confirm byte-identical (`read == orig`) before moving on.

## Traps

- **Stale results XML.** Delete `app/build/outputs/androidTest-results` before
  each run; a failed compile otherwise re-reports the previous green.
- **Asserting only the current version.** A test that creates the DB at
  `VERSION` and migrates to `VERSION` is a no-op walk; start at the oldest
  schema you actually shipped.
- **Row-exists assertions.** `assertTrue(c.moveToFirst())` passes when half the
  rows are gone. Assert counts and aggregates.
- **Schema drift in the seed SQL.** If `execSQL` fails at the baseline, the
  column list came from the entity class, not the exported JSON.
