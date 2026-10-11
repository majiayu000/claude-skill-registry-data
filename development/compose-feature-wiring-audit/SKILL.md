---
name: compose-feature-wiring-audit
description: "Use when parallel agents added Compose screens, entities or DB columns: a new screen never appears, a feature silently does nothing, or launch crashes with No enum constant or a missing migration. Also after new enum values reach a UI filter row."
---

# Compose feature wiring audit

Parallel agents produce code that compiles, passes tests, and is **unreachable or crashes on launch**. Compile-green is not feature-complete. Run these four checks after any fan-out that adds screens or schema.

## 1. Orphaned screens

Agents build `FooScreen` but nobody routes it. The compiler never complains — an unused public composable is legal.

A screen is reachable only if something other than its own declaration calls it — the nav graph (Ironvellum: `ui/IronvellumNav.kt`) or a host screen. Search all of `app/src/main`: Ironvellum's `SocialScreen` hosts Feed, Leaderboard and Account as tabs, so a nav-only grep calls them unreachable. Lead with a known-routed screen as a positive control:

```bash
for s in SettingsScreen FeedScreen LeaderboardScreen AccountScreen WorkoutLogScreen; do   # first = known-routed control
  c=$(grep -rn --include='*.kt' "$s(" app/src/main | grep -v "fun $s(" | cut -d: -f1 | sed 's#.*/##' | sort -u | tr '\n' ' ')
  printf "%-24s %s\n" "$s" "${c:-NOT REACHABLE}"
done
```

Each line names the calling files. A `@Preview` caller doesn't count, nor does a host that is itself unreachable — follow the chain up to the nav graph. A control that prints NOT REACHABLE means the check is broken, not the app: git-bash has globstar off, so a `**` path like `app/src/main/kotlin/**/ui/*Nav.kt` never matches a package three directories deep, grep exits 2, and every screen reads NOT REACHABLE (verified 2026-09-24).

Real result from one session: **5 of 5 screens NOT REACHABLE** — feed, leaderboard, account (the sign-in gate!), workout log and detail. The user found out by looking for them.

Add every new screen to this check before claiming a feature is done.

## 2. Defaulted callbacks hide missing wiring

```kotlin
fun StatsScreen(onOpenMeasurement: (Site) -> Unit = {})   // forgotten wiring compiles clean
fun StatsScreen(onOpenMeasurement: (Site) -> Unit)        // compiler enforces the call site
```

Same class of bug as a defaulted data parameter:

```kotlin
fun ledgerOf(..., exercises: Map<Long, Exercise> = emptyMap())  // zeroes every activity deed, silently
```

Removing that default exposed **four** call sites relying on it. Rule: **a default that means "feature silently does nothing" is a bug**. Defaults are for values with a correct fallback, not for wiring.

## 3. `valueOf` on stored data crashes the app

Seeds wrote `muscleGroup = "CARDIO"` while the enum held only `PULL/PUSH/LEGS/CORE`. `MuscleGroup.valueOf` threw while mapping the catalogue → **every screen dead on launch**, on a build that compiled and passed 109 tests.

```kotlin
// crashes on any unknown string from the DB or an imported archive
muscleGroup = MuscleGroup.valueOf(stored)

// survives it
muscleGroup = MuscleGroup.entries.firstOrNull { it.name == stored } ?: MuscleGroup.CORE
```

Fix **both** sides: harden the mapper *and* correct the seeds. Defaulting alone leaves the data quietly wrong (all activities filed under one group) instead of loudly broken.

Audit: `grep -rn "\.valueOf(" --include=*.kt` over any path that reads persisted values.

## 4. New column without a migration = launch crash

Once `fallbackToDestructiveMigration()` is removed (and it should be — it silently deletes user data), every schema change needs an explicit `Migration(n, n+1)` registered via `addMigrations(...)`. Missing one throws at open.

Give agents the current version number in their brief and require the migration SQL back in their report.

## Verify on hardware

```bash
ADB="$LOCALAPPDATA/Android/Sdk/platform-tools/adb.exe"
"$ADB" logcat -c -b crash                      # clear FIRST or you re-read an old crash
"$ADB" install -r app/build/outputs/apk/debug/app-debug.apk
"$ADB" shell am start -W -n <pkg>/.MainActivity; sleep 7
"$ADB" logcat -d -b crash | rtk grep -c "FATAL EXCEPTION"   # must be 0
"$ADB" shell pidof <pkg>                       # must return a pid
```

`install ... Success` means the APK parsed, nothing more. Check the crash buffer and that the process is still alive, then screenshot.

## Layout regressions from enum growth

Adding enum constants grows any UI that iterates `entries` — a fixed `Row` of filter chips pushed labels off-screen, rendering `CLIMBING` one letter per line. When a list feeds a horizontal row: `Modifier.horizontalScroll(rememberScrollState())` plus `maxLines = 1, softWrap = false` on the label. Also check whether the new values duplicate an existing filter axis.
