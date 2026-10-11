---
name: compose-layout-device-traps
description: "Use when Compose renders wrong on device but builds green: Row labels one letter per line, zero-width steppers, stacking in PullToRefreshBox, keyboard over inputs, LazyColumn in verticalScroll. Also on 'measured with an infinity maximum height constraints', Scaffold content drawn over itself, adb taps landing on the IME, uiautomator bounds that disagree with the screenshot, Text printing a data class toString, or before trusting an agent's 'my file compiles' claim about UI."
---

# Compose layout defects the compiler cannot see

Scope: **layout/measure/gesture defects that only appear on a device.** Green build + green tests + an agent reporting "zero errors in my file" says nothing about whether the screen is correct.

Sibling skills — do not duplicate them:
- **Wiring** defects (screens built but never routed, defaults that hide missing wiring, `valueOf` crashes from seed data, missing Room migrations) → `compose-feature-wiring-audit`.
- **adb mechanics** (device auth, wake, uiautomator driving, screenshots, gradle quirks) → `android-usb-verify`.
- Defects that appear only at a large or small **system font scale** → `android-font-scale-verification`.

## The rule that catches all of these

A screenshot is the only proof. Run the flow, capture, and *read the image*. A `uiautomator dump` misleads in both directions: it lists nodes that are stacked, clipped, or behind the keyboard as though they render fine, and it can report nonsense bounds for a text node (a title 6px tall, hit-rects overlapping in Y) on a screen that renders correctly. Confirmed: such bounds persisted unchanged after a fix whose screenshot was visibly correct. Treat odd bounds as a reporting artifact and adjudicate with `exec-out screencap`, not the XML.

```bash
ADB="$LOCALAPPDATA/Android/Sdk/platform-tools/adb.exe"
"$ADB" logcat -c -b crash                      # clear FIRST or you re-read an old crash
"$ADB" install -r app/build/outputs/apk/debug/app-debug.apk
"$ADB" shell am force-stop <pkg>; "$ADB" shell am start -W -n <pkg>/.MainActivity
sleep 6
echo "FATAL: $("$ADB" logcat -d -b crash | grep -c 'FATAL EXCEPTION')  pid: $("$ADB" shell pidof <pkg>)"
"$ADB" exec-out screencap -p > shot.png
```
`FATAL: 0` **and** a live pid **and** a screenshot you looked at. Any one alone is insufficient.

## Trap 1 — Box-slot containers stack their children

`PullToRefreshBox`, `Scaffold`'s content, `Box` — their content slot is a **`BoxScope`**, not a column. Children emitted directly into it all draw at the same origin.

Symptom: only the last-drawn element is visible; earlier elements look "missing" or "empty" (a podium renders its plinths but the names appear blank because a later card is painted over them). Dumps still list every node, so automation reports success.

```kotlin
PullToRefreshBox(isRefreshing = …, onRefresh = …) {
    Column(Modifier.fillMaxWidth()) {   // REQUIRED: the slot is a Box
        Header(); Rows()
    }
}
```

Stacking overlays whole elements at one origin; width starvation (Trap 3a) squeezes widths inside a `Row`. Different bugs, different fixes.

## Trap 2 — LazyColumn inside a verticalScroll parent

Crashes at measure time:
`IllegalStateException: Vertically scrollable component was measured with an infinity maximum height constraints`

Fix structurally; do **not** drop laziness (that defeats the point for a growing list). The lazy list owns the scrolling, and the caller passes a bounded modifier:

```kotlin
// parent: no verticalScroll on this branch
Column(Modifier.fillMaxSize()) {
    Header()
    MyList(modifier = Modifier.fillMaxWidth().weight(1f))   // bounded height
}
// child
@Composable fun MyList(modifier: Modifier = Modifier.fillMaxSize()) { LazyColumn(modifier) { … } }
```
When one tab of a screen needs a lazy list and the others scroll, branch the modifier:
`.then(if (lazyTab) Modifier else Modifier.verticalScroll(rememberScrollState()))`.

## Trap 3 — Row labels one letter per line: find the cause before the fix

Signature: labels wrap **one character per line** (`L` / `O` / `A` / `D`, or `CLIMBING` → `C/L/I/M…`), steppers, fields or icon pairs collapse to slivers or vanish, the build is green, and the `Row` body reads as correct. Two causes with opposite fixes, so read the Row's **whole child list** before touching any size.

### 3a. A greedy sibling starves the weighted children

A `Row` where one child is **inflexible and greedy** (typically `Modifier.fillMaxWidth()`, or a fixed `width()` larger than the slack) measures that child first. Every `weight(1f)` sibling divides what is left, which can be **zero**. The culprit is the sibling nobody suspects, often appended later by a feature that was meant to sit *below* the row:

```kotlin
Row(Modifier.fillMaxWidth()) {
    Column(Modifier.weight(1f)) { /* starved */ }
    Column(Modifier.weight(1f)) { /* starved */ }
    SomeBadge()            // <- internally Row(Modifier.fillMaxWidth()), takes everything
}
```

Grep the suspect child's own composable for `fillMaxWidth()` / `width(`:

```
grep pattern: "private fun <ChildName>|fillMaxWidth\(|width\("
```

A comment on the offending call site saying the element belongs "under" / "below" the row is strong confirmation the structure, not the sizing, is wrong.

Fix structurally: wrap in a `Column` and move the greedy child out of the `Row`. Carry the outer modifiers (`fillMaxWidth`, `alpha`, `padding`) up to the `Column` so behaviour is unchanged:

```kotlin
Column(Modifier.fillMaxWidth().alpha(..).padding(..)) {
    Row(Modifier.fillMaxWidth(), ...) { /* controls only */ }
    SomeBadge()
}
```

Do **not** "fix" it by shrinking the badge, adding `weight` to the greedy child, or setting `maxLines` on the starved labels. Those hide the measurement bug and it returns with the next label change.

Verify by comparing **child widths** before/after via uiautomator:

```python
# widths of the row's children; starved children report w≈0 or a 6px-tall text node
for b, txt in nodes(xml, r'text="[^"]{1,60}"'):
    print(repr(txt), "w=", b[2]-b[0], b)
```

Expect starved children to go from absent/slivers to real widths (e.g. a stepper's `−` `value` `+` each reporting ~100px+).

### 3b. A fixed chip rail outgrew the row

With no greedy sibling, a fixed `Row` of filter chips silently wraps each label to one letter per line off the right edge once the set grows. Scroll the rail and keep each chip's text on one line:

```kotlin
Row(Modifier.fillMaxWidth().horizontalScroll(rememberScrollState()), …) { … }
Text(label, maxLines = 1, softWrap = false)   // on the chip's own Text
```

`maxLines` is part of this fix only, paired with the scroll; on a starved Row (3a) it hides the bug. Also check for **duplicated filter axes**: if two rails end up offering the same values (e.g. a muscle-group enum that grew to include activity groups already present in a category rail), the fix is to narrow one rail, not to scroll both.

## Trap 4 — keyboard covers the input, and eats your taps

With `enableEdgeToEdge()` the IME overlays content even with `windowSoftInputMode="adjustResize"`.

```kotlin
Column(
    Modifier.fillMaxSize()
        .imePadding()                               // BEFORE the scroll modifier
        .verticalScroll(rememberScrollState())
)
```
Sweep **every** screen with a text field, not just the reported one — grep for `BasicTextField|OutlinedTextField|TextField(` and compare against files containing `imePadding`.

A submit button below the field can still sit under the keyboard. Wire the IME action so the entry is never stranded:

```kotlin
keyboardOptions = KeyboardOptions(keyboardType = …, imeAction = ImeAction.Done),
keyboardActions = KeyboardActions(onDone = { submit() }),
```

**Automation corollary:** `uiautomator dump` reports app-window coordinates, but the IME floats above them. A scripted tap at a button's dumped `y` lands on a *keypad key* instead — symptom: a typed `84.5` mysteriously becomes `84.52` (it hit `2`). Dismiss the IME or use the Done action before tapping anything low on screen.

## Trap 5 — never interpolate an object into Text

`"$row.lifetimeStrength"` interpolates the whole data class `toString()` then appends the literal text `.lifetimeStrength`. It compiles, and prints `LeaderboardRow(userId=0ce6…, …).lifetimeStrength` on screen. Always `"${row.lifetimeStrength}"`, and grep for `"\$[a-z]+\.` after any UI agent's work.

## Verification checklist before believing a UI is done

1. Screenshot read by eye — not a dump, not a compile.
2. `FATAL: 0` from a **cleared** crash buffer, plus a live pid.
3. Count what should render vs what does (header says "5 lifters ranked" → count five).
4. Grep the diff for `"\$[a-z]+\.`, new `LazyColumn`, new `Row(` chip rails, children appended to an existing `Row`, new text fields.
5. Child widths are real for every `Row` you touched (Trap 3a).
