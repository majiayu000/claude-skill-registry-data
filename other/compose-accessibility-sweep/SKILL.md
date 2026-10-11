---
name: compose-accessibility-sweep
description: "Use when adding TalkBack/accessibility coverage to a Compose UI, or a screen reader cannot tell which tab, segmented control or filter chip is selected, lands on nothing, or reads a bare symbol. Also after adding tabs or chips, when a tap target may be under 24dp or 48dp, or when an accessibility sweep passes suspiciously: a surface never reached, or a half-scrolled control measuring too small."
---

# Compose accessibility sweep

Drive every surface through the semantics tree and assert three things per
control: an accessibility service can **announce** it, it is big enough to
**hit**, and a selection control says **which one is active**. All three are
measured, never eyeballed, and belong in one instrumented class (Ironvellum:
`app/src/androidTest/kotlin/com/ironvellum/app/ui/AccessibilityChecksTest.kt`).

## 1. Announce: every control must say something

**A `BasicTextField` whose placeholder is a sibling `Text`.** The field looks
labelled on screen and announces *nothing* — a screen reader lands on an
unlabelled input. Label the field; leave the decorative icon `null`, because
naming both makes TalkBack read it twice.

```kotlin
BasicTextField(
    modifier = Modifier
        .fillMaxWidth()
        .heightIn(min = 24.dp)              // one line of text measures ~20dp
        .semantics { contentDescription = "Search movements" },
)
if (query.isEmpty()) Text("search movements")   // sibling placeholder
```

**A symbol is not a label.** A naive unlabelled check tests for non-blank text.
`"−"`, `"→"`, `"—"` are all non-blank and all announce as punctuation
characters — the control is legible on screen and useless to TalkBack. Sharpen
the predicate:

```kotlin
private fun String.saysSomething(): Boolean = any { it.isLetterOrDigit() }
```

This found seven defects in one pass, including a 44dp stepper that passed every
size check. Labels must also *disambiguate*: two `"+"` glyphs on one screen
become "More" and "More added load", not two identical announcements.

Expect a **cascade** — failure lists truncate, so fixing six surfaces exposes a
seventh. Re-run until green rather than assuming the first list was complete.

## 2. Hit: a two-tier size floor

Use a two-tier policy and say so in the test, or reviewers will argue about it
forever:

- **WCAG 2.5.8 AA = 24dp** for *every* tappable control.
- **Material 48dp** for the nav bar only — the one control on every screen.
- The 24–48 band on dense in-panel chips is a **layout decision, not a defect**.
  Compose clips touch delivery to the parent's bounds, so widening a child
  inside a padded panel changes nothing measurable.

Typical fix for chips: `.heightIn(min = 32.dp)` — Material chip height, costs a
few density pixels, no relayout.

**Clipped bounds ≠ target size.** `boundsInRoot` is clipped to the *visible*
region, so a half-scrolled 40dp button measures 23dp and reads as a defect. Use
`node.size` — the laid-out size. A test that fails on scroll position gets
deleted within a week.

## 3. State: say which control is active

Selection drawn with a gradient fill and a brighter border never leaves Kotlin:
a screen reader reads every tab identically, so the user has no sense of place.
On an icon-forward app whose nav is the only chrome on every screen, that
removes navigation entirely.

List every place a `selected`/`isOn` boolean may drive only colour, then check
each for a semantics block:

```bash
grep -rn "selected\|isOn" app/src/main/kotlin --include=*.kt | grep "/ui/" | grep -v "semantics"
```

| family | example | role |
|---|---|---|
| nav destinations | bottom bar slots | `Role.Tab` |
| in-screen tab rows | tab pills, segmented controls | `Role.Tab` |
| filter chips | status/rarity/group filters | `Role.Checkbox` |

Chips are **not** tabs: they narrow a list while you stay put, so they read as
checkboxes. Getting this wrong announces "tab" for something that never moves.

```kotlin
.semantics {
    role = Role.Tab
    this.selected = selected
}
```

**`this.` is load-bearing.** If the enclosing composable has its own `selected`
parameter (common: `InkSegmented(selected: T, …)`), the bare name resolves to
the parameter and you get `'val' cannot be reassigned` — or, when the types
happen to agree, a silent assignment to the wrong target.

**Assert the property, not the plumbing.** Check *exactly one* is selected and
that it follows the tap. Asserting only "something reports selected" passes on a
component hardcoded to `true`.

```kotlin
val selected = DESTINATIONS.filter { candidate ->
    compose.onNodeWithContentDescription(candidate).fetchSemanticsNode()
        .config.valueOrNull(SemanticsProperties.Selected) == true
}
assertEquals("after opening $destination", listOf(destination), selected)
```

For chips, assert both directions — default on, others **off**, then tap and
watch the state move. The `false` assertions are what catch a blanket `true`.

Substring matchers are safe here without extra guarding: the assertion keys on
`Selected == true`, so a match against body prose contributes nothing and cannot
produce a false pass. Compose's `onAllNodesWithText(substring = true)` is
case-sensitive, so an uppercase pill label will not collide with lowercase prose.

## 4. Sweep behind each tab, and prove you arrived

Top-level destinations are the least likely place to find anything. The dense
screens — a live session, an editor, a picker — are where unlabelled glyphs
hide. Drive `destination -> sub-surface` pairs.

**Vacuous skips.** Skipping a surface whose label doesn't match is right for a
missing feature and fatal as a silent default: every assertion then passes on an
empty node set. Assert the surfaces were actually *reached*, and name the
missing ones:

```kotlin
assertEquals(
    "surfaces the sweep could not reach: ${ALL.map { "${it.first}/${it.second}" } - visited.toSet()}",
    ALL.size, visited.size,
)
```

This is what exposes a settings screen that was never opened at all.

**Icon-only entry points.** A settings gear has a *content description*, not
text. Match text first, then description, or the surface is silently skipped:

```kotlin
private fun openSurface(label: String): Boolean {
    val byText = compose.onAllNodesWithText(label, substring = true)
    if (byText.fetchSemanticsNodes().isNotEmpty()) { byText.onFirst().performClick(); return true }
    val byDesc = compose.onAllNodesWithContentDescription(label, substring = true)
    if (byDesc.fetchSemanticsNodes().isNotEmpty()) { byDesc.onFirst().performClick(); return true }
    return false
}
```

**Ordering and navigation.**

- Some surfaces **replace the nav bar**; walk back until it returns rather than
  assuming it is there: press `onBackPressedDispatcher` until a known nav
  content description resolves (cap the retries). Behind an app-wide first-run
  gate, advance the clock until the bar appears before the first press, or it
  exits the app — see `first-run-gate-breaks-instrumented-suite`.
- Put **destructive surfaces last** — starting a session leaves a live trial
  whose abandon prompt sits between the sweep and the nav bar.

## 5. Name the control in failures

`178x23 dp` sends the next reader hunting across every screen. Build an
identifier from `node.config`: `SemanticsProperties.Text`, then
`ContentDescription`, else `"unnamed"` → `"CONNECT & SYNC" 178x23 dp`.

## 6. Prove it bites

Revert each fix and confirm the matching assertion fails — label removed →
`role=null at Rect(...)`; height floor removed → `"PULL" 45x23 dp`. An
accessibility test that has never failed has never been tested.

Each selection family needs its own mutation; one shared assertion can hide two
broken components. Strip the `semantics` block, confirm the failure *names* the
control, restore, re-run green:

```
after opening Train the nav should report exactly it as selected expected:<[Train]> but was:<[]>
in Codex, opening DEEDS should leave exactly it selected expected:<[DEEDS]> but was:<[]>
the default deed filter must report itself on expected:<true> but was:<false>
```

## Environment notes

- The clock is often held (`mainClock.advanceTimeBy`) because ink/gradient
  animations never idle; `ComposeNotIdleException` otherwise.
- Instrumented runs **uninstall the app**; reinstall before driving the device
  by hand afterwards.
- `uiautomator` dumps do **not** expose Compose's merged click nodes — measure
  from the semantics tree, not the flat XML dump.
