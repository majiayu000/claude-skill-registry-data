---
name: android-health-connect-sync-debug
description: "Diagnose Android Health Connect reads that return zeros, \"unavailable\", or step counts that trail the phone's own tally — covers the LocalDateTime aggregation trap, one-denied-permission-kills-all-metrics, the missing VIEW_PERMISSION_USAGE activity, and proving whether missing data is upstream. Use when a Health Connect sync writes empty rows, reports permanent unavailability, or disagrees with Samsung Health/Fitbit numbers."
---

# Health Connect sync debugging

Failure mode: the sync "succeeds", writes N rows, and every metric is zero — or
the card says "unavailable" forever. The cause is almost never the code path you
are staring at. Work the checklist in order; each step is a one-command check.

## 0. Make the sync report why, before fixing anything

Never let a read collapse into a bare count or `null`. A result type that carries
diagnostics turns a week of guessing into one screenshot:

```kotlin
data class HistoryRead(
    val days: List<HealthDay> = emptyList(),
    val coverage: Map<String, Int> = emptyMap(),   // days each metric filled
    val problems: List<String> = emptyList(),      // "$metric: ${e.javaClass.simpleName} ${e.message}"
)
```

Surface `problems` verbatim in the UI. Every later step below was found this way,
not by reasoning.

## 1. Period aggregation rejects Instant ranges

`aggregateGroupByPeriod` with an `Instant`-based `TimeRangeFilter` throws:

> IllegalArgumentException: Either use TimeRangeFilter with LocalDateTime or
> AggregateGroupByDurationRequest

Silently caught, this zeroes **every** day while a plain `aggregate()` (snapshot
totals) still works — so "today's steps" looks fine and history is empty.

```kotlin
val fromLocal = start.atStartOfDay()            // LocalDateTime for grouped aggregation
val toLocal = end.plusDays(1).atStartOfDay()
timeRangeFilter = TimeRangeFilter.between(fromLocal, toLocal)
```

Keep `Instant` ranges for `readRecords` (sleep sessions, HR samples) — those are fine.

## 2. One denied permission kills every metric in the request

Metrics batched into a single `AggregateGroupByPeriodRequest` fail as a unit. A
missing calories grant therefore reports as a *steps* failure. Issue one request
per metric so a denial degrades only itself:

```kotlin
suspend fun <T : Any> daily(label: String, metric: AggregateMetric<T>): Map<LocalDate, T> =
    runCatching { /* aggregateGroupByPeriod(setOf(metric), ...) */ }
        .onFailure { note(label, it) }
        .getOrDefault(emptyMap())
```

## 3. Manifest and request-set parity

Every record type needs BOTH, or reads return empty with no error:

1. `<uses-permission android:name="android.permission.health.READ_X" />` in the manifest
2. `HealthPermission.getReadPermission(XRecord::class)` in the set passed to the
   permission launcher

Easy to add one and forget the other. Check parity directly:

```bash
rtk grep -n "permission.health" app/src/main/AndroidManifest.xml
rtk grep -n "getReadPermission" <the screen that launches the request>
```

Grant them for testing without touching the UI:

```bash
adb shell pm grant <pkg> android.permission.health.READ_DISTANCE
adb shell dumpsys package <pkg> | rtk grep "permission.health"   # granted=true?
```

## 4. Two manifest entries that masquerade as "not installed"

- **`<queries>` for the provider** — without it `getSdkStatus()` cannot see Health
  Connect and always returns unavailable:

```xml
<queries>
  <package android:name="com.google.android.apps.healthdata" />
  <intent><action android:name="androidx.health.ACTION_SHOW_PERMISSIONS_RATIONALE" /></intent>
</queries>
```

- **`VIEW_PERMISSION_USAGE` rationale activity** — Android 14+ rejects *every*
  read with `IllegalStateException: Incorrect health permission state` without it,
  even when permissions are granted:

```xml
<activity-alias android:name="ViewPermissionUsageActivity" android:targetActivity=".MainActivity"
    android:exported="true" android:permission="android.permission.START_VIEW_PERMISSION_USAGE">
  <intent-filter>
    <action android:name="android.intent.action.VIEW_PERMISSION_USAGE" />
    <category android:name="android.intent.category.HEALTH_PERMISSIONS" />
  </intent-filter>
</activity-alias>
```

Also distinguish `SDK_UNAVAILABLE` from `SDK_UNAVAILABLE_PROVIDER_UPDATE_REQUIRED`
— collapsing both into "unavailable" hides a fixable state.

## 5. Never fabricate rows for empty days

Writing a row per requested day makes the sync claim "90 days synced" while every
screen shows nothing. Keep only days with real signal, and purge legacy junk:

```sql
DELETE FROM health_days WHERE steps = 0 AND distanceKm = 0
  AND activeKcal = 0 AND sleepMinutes = 0 AND restingHr IS NULL
```

## 6. Counts that trail the phone's own tally

Providers (Samsung Health especially) push in batches — a total an hour behind is
upstream lag, not a bug. Prove it instead of arguing: read the raw records and
report provenance.

```kotlin
val raw = client.readRecords(ReadRecordsRequest(StepsRecord::class, ...)).records
val newest = raw.maxOfOrNull { it.endTime }          // e.g. 10:48 when it is 12:20
val sources = raw.map { it.metadata.dataOrigin.packageName }.distinct()
```

Then label the UI "as of HH:mm" so the number never claims to be live.

## 7. Missing metric = check the source before writing code

Widening a lookback window cannot invent data. If distance/calories/sleep/weight
read zero while steps work, the provider is not sharing those types. Confirm in
the Health Connect app (Data and access → the type), or ship the per-metric
`coverage` map and read it on-device. Direct the user to the provider's own sync
toggles; no app-side change fixes an empty source.

## Device verification loop

UI dumps beat vision guesses for coordinates; navigate before driving:

```bash
adb shell uiautomator dump /sdcard/ui.xml && adb shell cat /sdcard/ui.xml > .tmp/ui.xml
# find a control by text, tap its bounds centre, re-dump, read the result text
```

Confirm in this order: the metric coverage line → days written → the screens that
consume the data (charts, achievements). Force-stop and relaunch between installs;
a tap sent during app restart is swallowed silently.
