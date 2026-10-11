---
name: subagent-damage-repair
description: "Use before running a subagent edit wave on D:/Monarch, or after parallel-agent edits to a Kotlin/Android repo: KSP fails with the opaque [ksp] [MissingType]: Element '...Database' references a type that is not present, imports, parameters or helpers vanish, declarations get clobbered, or a wave reports green but the build fails."
---

# Subagent damage repair (Kotlin/Android)

Parallel `task` subagents repeatedly rewrite import blocks, overwrite neighbouring declarations, delete parameters and helpers, and still report success — sometimes the build fails, sometimes it compiles with silent visual/behavioural loss instead. In Monarch this happened on three consecutive dispatches. Self-reports are never sufficient; the gate plus a HEAD-diff is the enforcement that counts.

## Recognize the damage

The signature symptom is one opaque KSP line that hides the real error:

```
e: [ksp] [MissingType]: Element '<DbClass>' references a type that is not present
> Task :app:kspDebugKotlin FAILED
KSP failed with exit code: PROCESSING_ERROR
```

**KSP aborts before the Kotlin compiler reports anything**, so the real cause — an unresolved symbol *anywhere in the module* — never gets named. It doesn't mean the `@Database` class is broken, and the damage may not be in that file; fixing the true cascade source makes the line vanish. Never patch Room-graph suspects one at a time (entities, DAO return types, migration bodies) — those checks pass while the real damage sits elsewhere. The same damage can surface as a plain `e: Unresolved reference 'X'` on an obviously-existing symbol.

**Failure modes actually seen:**
- **Dropped imports** — a rewritten import block loses dozens of lines. Measured: 34 lost from `Repository.kt` in one wave, 44 in a later one.
- **Dropped parameters** — a new parameter is appended and an existing one silently vanishes; it compiles clean when the new one has a default, so a feature disappears behind a green build. Verified: `trailing` from `IdentityRow`, `name` from `Achievement`, `gold = true` from a button.
- **Overwritten/duplicated declarations** — an inserted member replaces its neighbour instead of landing beside it. Verified: `gachaDao()` appeared twice while `profileDao()` vanished entirely.
- **Deleted scaffolding** — the most destructive variant: `fun create(context) = Room.databaseBuilder(...)` disappears outright, leaving the file dangling into a stray `.addMigrations(`.
- **Unclosed blocks** — an auto-repaired edit leaves a `try`/`while` unclosed, nesting later functions at depth > 1 (seen twice) — they effectively become members of another function, so callers report "Unresolved reference" on something that plainly exists.
- **Contract mismatches between sibling agents** — two agents implement the same interface and disagree (one declares `Flow<Int?>`, the other calls `.rolls` on it), or one references a shared helper the other never created.
- **Wrong mechanism, right area** — the edit lands in the right place but the logic is inverted, e.g. a duplicate-cleanup SQL whose sort deleted the *oldest* row when the comment said oldest should win.

## Find it — probe sequence

Every check takes seconds, so run all that apply on every touched file rather than stopping at the first hit — one wave can cause several kinds of damage at once. The import diff comes first because it has the highest yield.

1. **Import diff against HEAD**, per touched file — the check that found the 34/44 drops above:
   ```bash
   git show HEAD:<file> | grep "^import" | sort > head.txt
   grep "^import" <file> | sort > now.txt
   comm -23 head.txt now.txt        # dropped imports
   ```

2. **Brace balance**, every touched file:
   ```bash
   python -c "t=open(f,encoding='utf-8').read(); print(t.count('{')-t.count('}'))"
   ```
   Must be 0. Non-zero means an unclosed block — locate it with a depth-walk that prints nesting depth at each `fun` line.

3. **Declaration/symbol diff against HEAD** — the check everyone skips: an agent adding a member can overwrite the line already there, failing the build for an untouched symbol.
   ```python
   import re, collections, pathlib
   t = pathlib.Path(DB_FILE).read_text(encoding="utf-8")
   daos = re.findall(r"abstract fun (\w+)\(\)", t)
   ents = re.findall(r"(\w+)::class", t)
   print("dup daos:", [k for k,v in collections.Counter(daos).items() if v>1])
   print("dup entities:", [k for k,v in collections.Counter(ents).items() if v>1])
   ```
   A duplicate is the tell. Diff the full declaration list too (`git show HEAD:$DB_FILE | sed -n '/abstract fun /p'` vs current, `diff`), then broaden to whole-file `fun`/`data class`/`val` sets to catch a deleted helper or property — once a `healthDays` ViewModel property was deleted while its `by collectAsStateWithLifecycle()` call site survived:
   ```bash
   git show HEAD:<file> | python -c "import sys,re; print(sorted(set(re.findall(r'fun (\w+)', sys.stdin.read()))))"
   ```
   run against HEAD and the current file.

4. **Factory function check** — cheap, specific to the deleted-scaffolding mode:
   ```bash
   grep -c "Room.databaseBuilder" $DB_FILE   # must be 1
   ```

5. **Parameter-drop grep** — after any signature change, grep all call sites for the old parameter name and for now-unused locals left behind (a dead `val accent` nothing reads is a tell).

6. **Cross-check the Room graph**, once 1-4 are clean:
   ```python
   imports = set(re.findall(r"^import com\.x\.app\.data\.db\.(\w+)", t, re.M))   # your package; Monarch: com\.ironvellum\.app
   used    = set(re.findall(r"(\w+)::class", t)) | set(re.findall(r"abstract fun \w+\(\): (\w+)", t))
   print("referenced but NOT imported:", sorted(used - imports))
   ```
   Genuine Room-side causes, in rough order of frequency — each fails the *whole* `@Database` with the *same* opaque MissingType:
   - a DAO typed `Flow<Int?>` against `SELECT *` — Room can't map a row to a scalar. Select the column (`SELECT rolls FROM …`) or return the entity; match what the repository calls (mirror a sibling DAO's row-style — `IdleDao` returns the row, `Repository` maps it).
   - a `@Database` entity list naming a class that no longer exists.
   - a DAO returning a type Room can't convert (`Set<T>` and friends).

7. **Last resort — bisect**, two techniques:
   - `git stash push <files>` a subset and rebuild; verify the stash emptied the working tree (`git status --porcelain`) before trusting the result — a no-op stash proves nothing.
   - Comment out the `@Database` annotation and run `:app:compileDebugKotlin` alone; the first plain-Kotlin `e:` line names the unresolved symbol. Restore immediately.

## Repair it

- Restore imports as the **sorted union** of HEAD + current, replacing the whole block between the first and last import line, then add back any import the *new* code needs that HEAD lacked too:
  ```python
  merged = sorted(set(head_imports) | set(current_imports))
  out = lines[:first_import] + merged + lines[last_import + 1:]
  ```
- If a file is badly mangled, **reconstruct the damaged region from `git show HEAD:<file>`, never from memory**, then re-apply only the intended change — incremental patching of a scrambled region takes longer and leaves leftovers. A from-memory reconstruction once shipped `shapes.extraSmall`/`padding(10,8)` where HEAD said `shapes.small`/`padding(12)`; separately, a repair spliced a stray function inside `ArmyStat`'s modifier chain.
- Fix a Room mapping mismatch by declaring the real row type (or selecting the single column) instead of forcing a scalar.
- Resolve a cross-agent contract mismatch by aligning to whichever side the tests or most callers already assume, then grep every call site of the changed signature.
- After repairing, run `git diff --stat` and read every hunk: the diff must contain ONLY the intended changes — stray deletions are how the next bug gets in.
- Read raw hunks at collision regions, not the rendered diff — compact renderers have twice hidden real damage here (`background(...)` reconstructed wrong; a duplicated migration registration sitting next to a deleted `Room.databaseBuilder`). Full acceptance checklist: `fixer-wave-orchestration` / `verify-delegated-edits`.
- Gate once, after every agent settles, never mid-flight (`fixer-wave-orchestration`) — a forbidden-to-build agent self-reports green regardless (it happened on every wave of one session). Re-gate after each repair until green, and report agent defects honestly; they're findings, not shame.

## Prevent it

- Tell edit agents explicitly: never rewrite an import block, add only the lines you need.
- Require a closing report per agent: list any deleted symbol and confirm nothing else references it; separately, report — don't apply — any change needing a signature/test/other-file edit outside your files.
- State shared-API signatures verbatim in a contract block at the top of the shared context — exact signature, who owns it, explicit "no signature change" clauses, who passes what. This has prevented drift once and must always be stated for any shared component.
- Split the wave by exclusive file ownership; full dispatch/brief mechanics: `fixer-wave-orchestration`.
- Forbid build/test/lint/formatter/commit during the batch; the parent runs the one gate afterward.
- After any wave that touches Room files, run the import and declaration diffs (steps 1 and 3) *before* the build — they name the damage precisely, while the build names nothing.
- Brief wording is cheaper than repair but does not prevent the damage — agents told not to break imports still break them. The gate plus the probes above is the control.

## Monarch specifics

D:/Monarch is the Ironvellum app (formerly Monarch): Kotlin + Compose + Room + Supabase in package `com.ironvellum.app`, with `MonarchDatabase` renamed to `IronvellumDatabase` and builds split into `foss`/`play` flavours (so `:app:compileFossDebugKotlin`, not `:app:compileDebugKotlin`). Standing repo facts — flavoured task names, `ANDROID_SERIAL`, Supabase state — live in `monarch-session-context`. The error reads:
```
e: [ksp] [MissingType]: Element 'com.ironvellum.app.data.IronvellumDatabase' references a type that is not present
> Task :app:kspFossDebugKotlin FAILED
```

Scan all four data-layer files at once when probing a wave:
```bash
for f in data/IronvellumDatabase.kt data/Repository.kt data/db/Entities.kt data/db/Daos.kt; do
  git show HEAD:app/src/main/kotlin/com/ironvellum/app/$f | grep "^import" | sort > /tmp/h.txt
  grep "^import" app/src/main/kotlin/com/ironvellum/app/$f | sort > /tmp/n.txt
  d=$(comm -23 /tmp/h.txt /tmp/n.txt); [ -n "$d" ] && echo "=== $f dropped:" && echo "$d"
done
```

**Dispatch mechanics** (brief basics — ownership, verified mechanism, intended fix: `fixer-wave-orchestration`): when two changes need one file, give it to one agent and state the other's contract ("X owns it, you pass-through"). Monarch briefs add read-only data-layer rules where applicable, ready-made greps, a budget rule (grep first, read ±30 lines — files run 20-40KB), and an output contract (findings/changes one per line, `path:line`, no preamble).

**Gate**: first, `git status --porcelain=v1 --untracked-files=all` must equal the union of assigned rosters — extra files are stray edits, missing files are undeclared work (full inventory checklist: `fixer-wave-orchestration` / `verify-delegated-edits`). Then run the repo's gate (~2 min; run it in the background):
```
python tools/gate.py --no-device --backend     # or --serial emulator-5554 to include instrumented tests
```
or call `./gradlew.bat :app:assembleFossDebug :app:testFossDebugUnitTest --console=plain` directly and filter for `^e:|FAILED|BUILD`.

**Room migration discipline**: migration objects are named `MIGRATION_<from>_<to>` as `private val` declarations:
```python
registered = re.findall(r"MIGRATION_\d+_\d+", t.split("addMigrations")[1])
defined    = sorted(set(re.findall(r"private val (MIGRATION_\d+_\d+)", t)))
print("defined but NOT registered:", [m for m in defined if m not in registered])
```
`fallbackToDestructiveMigration` was removed on purpose (it wipes user data on an unknown schema, and an upgrade once wiped everything) — so a migration defined but never registered is now a guaranteed launch **crash**, not a silent wipe or a warning to suppress. The same migration registered twice signals the overwrite pattern above. None of this proves the migration preserves existing *data*, only the schema — for that, see `room-migration-data-survival-test`.

**Live-Supabase gate (user-mandated, no exceptions)**: migrations go to `supabase/migrations/`, staged only. Applying via dockerized `psql` to the live pooler needs an explicit per-run yes — "fix everything" isn't consent, and a batch approval doesn't cover a later, new DDL statement. Name destructive steps explicitly when asking (row deletes/updates, `ALTER` on live tables) and verify row effects after (`DELETE 0`, `UPDATE 0` counts). Prove an RLS exploit dead by replaying it as `set local role authenticated` with the relevant JWT claims inside `begin ... rollback`, alongside the legitimate path.

**Device verification (S25 Ultra via adb)**: device choreography and UI driving live in `android-usb-verify`. For a wave's migrations: `run-as` + `sqlite3` doesn't work there (no `sqlite3` binary), so prove them behaviorally — open the screen reading the new tables, confirm `FATAL: 0` from `logcat -d -b crash`, zero "migration didn't properly handle" lines, and real data rendering. Locate tap targets by `text=`/`content-desc=`, never raw coordinates (they drift onto identity rows and navigate away), and read the `clickable` flag — icons are often `clickable=false` inside a clickable parent. `rtk grep` silently returns empty on some multi-alternation/paren patterns — never treat emptiness as evidence, re-run with the built-in Grep tool without any `$` anchor (it keeps the carriage return of CRLF files, so `foo$` never matches in D:/Monarch; verified 2026-09-24).

**Post-wave**: commit thematically, push, and report local == remote hashes plus what was verified on hardware vs build-verified only — users here draw that distinction explicitly.
