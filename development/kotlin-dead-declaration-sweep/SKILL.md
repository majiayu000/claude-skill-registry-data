---
name: kotlin-dead-declaration-sweep
description: "Find and safely remove unused declarations in a Kotlin/Android repo without deleting live code — filtering runner-invoked test functions that look dead to a reference count, checking imports orphaned by the removal, and avoiding the false-negative search that \"proves\" a feature is missing when it is only named differently. Use when pruning dead code, after a feature is superseded, or when a reference count is about to justify a deletion."
---

# Dead declaration sweep (Kotlin / Android)

Goal: delete code nothing calls, without deleting code that *is* called through a
path a reference count cannot see.

## 1. Sweep by exact declaration name

```python
import pathlib, re, collections
roots = ["app/src/main/kotlin", "app/src/test/kotlin", "app/src/androidTest/kotlin"]
files = [p for r in roots for p in pathlib.Path(r).rglob("*.kt")]
src = {p: p.read_text(encoding="utf-8") for p in files}
decl = re.compile(r"^\s*(?:public |internal )?(?:suspend )?fun (?:<[^>]+> )?(\w+)\s*\(", re.M)
where = {}
for p, s in src.items():
    for m in decl.finditer(s):
        where.setdefault(m.group(1), []).append((p.name, s[:m.start()].count("\n") + 1))
allsrc = "\n".join(src.values())
for name, sites in where.items():
    if len(sites) > 1:                       # overloads: skip, judge by hand
        continue
    if len(re.findall(rf"\b{re.escape(name)}\b", allsrc)) <= 1:
        print(name, sites[0])                # referenced only at its declaration
```

Search **all** source sets in one corpus. A production function used only by a
test is not dead — it is covered.

## 2. Filter what a reference count cannot see

Before deleting anything, drop these from the candidate list:

- **`@Test` / `@Before` / `@After` functions** — invoked by the runner by
  annotation, never by name. In a real sweep these are usually the large
  majority of "dead" hits (50 of 54 in one run).
- **Anything reached by a framework**: `@Composable` previews, `Application` /
  `Activity` lifecycle overrides, WorkManager `doWork`, Room `@Dao` methods used
  only by generated code paths you have not grepped, serializer hooks.
- **Reflection / dynamic names**: check the string form too
  (`grep -rn "someName"` across `app/src` *and* non-Kotlin assets, SQL, config).

What remains is safe to inspect individually. Read each one; do not bulk-delete.

## 3. Remove, then chase orphaned imports

Deleting the last user of a type leaves an unused import that the compiler may
only warn about. Check by counting the symbol **after** the removal:

```python
symbol = imp.rsplit(".", 1)[1]
body = text.split("\n", 1)[1].replace(imp, "")
if len(re.findall(rf"\b{symbol}\b", body)) == 0:
    drop(imp)
```

Then rebuild and confirm the warning count in the touched files is zero — a
removal that trades dead code for a new warning is not finished.

## 4. Verify

Full gate (assemble + unit + instrumented + lint). A dead-code removal that
changes behaviour means the code was not dead.

## The false-negative trap (this is the important part)

**A negative grep is evidence of nothing until the positive case is located.**

Failure seen in practice: searching a UI tree for `setTrainingMode` and
`HYPERTROPHY`, finding neither, and concluding the feature was unreachable. The
control existed — it called `viewModel.setMode(...)` and built labels from
`TrainingMode.entries`, so it spelled neither literal. A duplicate feature was
built and installed before an accessibility dump showed the control twice on one
screen.

Rules that prevent it:

- Search for the **setter the UI actually calls** (`setMode`), not the
  repository function it wraps (`setTrainingMode`).
- Never search for an **enum's literal values** — labels are routinely derived
  (`Enum.entries.map { it to it.name }`).
- Before claiming something is absent, **find where the positive case would
  live** and read it. For a settings toggle: open the settings screen source and
  count the controls.
- Prefer LSP `references` over grep for symbol questions when a language server
  is available; it follows shadowing and re-exports that text search misses.
