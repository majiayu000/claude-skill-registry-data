---
name: gradle-mutation-proof-regression-test
description: "Use when proving a new Gradle/Android test (unit/instrumented) catches its bug, or a mutation passes suspiciously fast, a failed compile reads as green, or a mutation edit breaks untouched helpers."
---

# Mutation-proving a Gradle/Android regression test

A new test that has never failed proves nothing. Break the code it defends,
watch it fail with a legible message, restore, confirm green. Two environment
traps make this go wrong silently.

## Trap 1 — stale results XML reads as a pass

`connectedFossDebugAndroidTest` / `testFossDebugUnitTest` leave their XML behind. If the
mutated build **fails to compile**, the task never runs and the previous run's
XML is still on disk — so a parse of it reports the old `failures="0"` and the
mutation looks survived-by-a-green-test.

Always delete results first and print the file count:

```bash
rm -rf app/build/outputs/androidTest-results
# ...run the mutated build...
python -c "
import glob,re,pathlib
xs=glob.glob('app/build/outputs/androidTest-results/connected/**/*.xml', recursive=True)
print('result xml files:', len(xs), '(0 = the run never happened)')
for f in xs:
    t=pathlib.Path(f).read_text(encoding='utf-8')
    print('result:', dict(re.findall(r'(tests|failures)=\"(\d+)\"', t)[:2]))
    for m in re.findall(r'<failure[^>]*>(.{0,260})', t, re.S): print('  CAUGHT:', m.strip().splitlines()[0][:260])
"
```

Unit tests write `app/build/test-results/testFossDebugUnitTest/TEST-<class>.xml`; run
the same check there. A filtered run (`--tests '*XTest*'`) leaves every earlier XML in
place, so unlink the matching result files first. The trap is live on D:/Monarch:
pre-flavour `connected/debug/TEST-*.xml` and `test-results/testDebugUnitTest/` still
sit beside the flavoured results (seen 2026-09-24), and a recursive glob reads them.

Instrumented suites are destructive, so run them on the emulator only:
`ANDROID_SERIAL=emulator-5554 ./gradlew :app:connectedFossDebugAndroidTest`
(see `android-physical-phone-safe-verify`).

Also scan build output for `^e:` (Kotlin errors) alongside `FAILED`/`BUILD SUCCESS`.
A compile error in the *mutation* is a no-op run, not evidence.

## Trap 2 — regex excision decapitates the enclosing function

Excising a loop by searching for its closing `append("]")` (or any generic
closer) routinely matches the **enclosing** construct's closer, deleting the
function's tail and cascading into unrelated "Unresolved reference" errors for
neighbouring private helpers. Symptom: errors point at helpers you never touched.

Read the real region first, then edit by line number with asserted anchors:

```python
lines = p.read_text(encoding="utf-8").splitlines(keepends=True)
assert 'append(",\\"sets\\":[")' in lines[99] and 'append("]}")' in lines[113], "anchors moved"
lines[99:114] = ['            append(",\\"sets\\":[]")\n']
```

Nested closers are often fused (`append("]}")` closes both the inner array and
the object), so deleting "just the loop lines" leaves unbalanced braces. Replace
the whole anchored span with the mutated equivalent.

## Prefer a mutation that compiles

A mutation the type system rejects proves only that the compiler works. Pick one
that type-checks and changes *behaviour*:

- flag inversion (`append(set.done)` -> `append(false)`) over deleting a block
- emptying a collection that is still the right type
- disconnecting a callback (`onClick = { }`)

If the compiler refuses the mutation, say so — "the type system already blocks
that one" is a real result, but it is not evidence about the test.

## Make the failure legible

`.single { ... }` / `.first { ... }` fail as `NoSuchElementException`, which
states nothing. Assert the count with a message first, then destructure:

```kotlin
val logged = restored.filter { it.done }
assertEquals("the archive must remember which sets were logged", 1, logged.size)
```

Re-run the mutation after tightening, to confirm the new message is what fires.

## Sequence

1. `rm -rf` results -> run baseline -> green
2. Commit the fix and the test, then apply one compiling, line-anchored mutation
3. Run; confirm XML count is 1 and the **expected** assertion fired
4. Revert with `git checkout -- <file>` (lossless against the commit; a `.bak` copy can be
   deleted by a cleanup `rm` mid-run), assert the source is byte-identical, re-run, confirm
   green and `git status` clean
5. Report which mutations were compiler-refused vs behaviourally caught

## Ground the test in the real API first

Write instrumented tests against symbols confirmed by reading the repository /
DAO interfaces, not recalled ones; the first `assembleFossDebugAndroidTest` will
list every invented name. Instrumented tests must open an **isolated database
file** (`IronvellumDatabase.create(context, TEST_DB)`), never the live one. For the
live-database `no such table` trap and Ironvellum's real Repository/DAO surface, see
`monarch-data-layer-instrumented-tests`.
