---
name: compose-unbounded-list-audit
description: "Find and fix Jetpack Compose screens that render an unbounded, growing list eagerly (forEach inside a scrolling Column instead of LazyColumn), and prove the LazyColumn conversion by content rather than by compiling. Use after measuring a data layer at scale, or when a history/journal/feed screen will grow for years."
---

# Auditing Compose screens for eager unbounded lists

A fast data layer proves nothing about the UI. `observeHistory()` returning in
76ms at 1,000 sessions still freezes the screen if the composable does
`history.forEach { Row(...) }` inside a `verticalScroll(...)` Column: every row
is composed whether or not it is on screen.

## 1. Find the eager lists

Lazy containers are the safe ones; the risk is `forEach` over data that grows
without bound (history, sessions, entries, attempts, measurements, feed rows).

```python
for p in pathlib.Path("app/src/main/kotlin/.../ui").rglob("*.kt"):
    src = p.read_text(encoding="utf-8")
    lazy = len(re.findall(r"LazyColumn|LazyVerticalGrid|LazyRow", src))
    eager = [m.group(1) for m in re.finditer(r"(\w+)\.forEach(?:Indexed)?\s*\{", src)]
    growing = [e for e in eager if any(k in e.lower() for k in
              ("history","sessions","entries","attempts","measurements","feed","rows","stats"))]
```

Then confirm per hit whether the data is capped upstream (`observeRecent(limit)`,
`.take(n)`) — many are, and those need no change. Only an uncapped source inside
a non-lazy container is a defect.

## 2. Pick the right fix per screen

- **Screen must show everything** (a full log) → convert to `LazyColumn` with
  stable keys. Group headers become their own `item(key = ...)`; rows become
  `items(list, key = { it.id })`.
- **Screen is a summary** (a dashboard's recent activity) → cap it with
  `.take(n)` and rely on the "see all" entry point already beside it. Cheaper
  and keeps the screen a simple Column.

## 3. Prove the conversion by CONTENT

A `LazyColumn` refactor compiles happily while emitting nothing — the failure
mode is silent, so the mutation must be too:

```kotlin
// seed through the app's own live repository, then drive the real screen
val label = db.sessionDao().byId(sessionId)!!.label
assertTrue("the log did not render the session labelled \"$label\"",
    compose.onAllNodesWithText(label, substring = true).fetchSemanticsNodes().isNotEmpty())
```

Mutate by replacing the collection in `items(...)` with `emptyList()` and confirm
the test names the missing row. Asserting a generic marker is weaker AND
error-prone: a row showing XP via a pill renders `"+120"` and `"XP"` as separate
text nodes, so a `" XP"` substring never matches. Assert the seeded row's own
label — it is both stronger and unambiguous.

## Traps

- The instrumented gate uninstalls the app, so a device sweep run straight after
  one drives an empty launcher. Reinstall first.
- Driving the UI to create fixture data fights whatever state the device is in
  (a rest day, a half-finished session). Seeding through the repository in the
  test is deterministic; driving taps is not.
