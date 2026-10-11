---
name: android-main-thread-io-triage
description: "Find and judge main-thread disk/network work in an Android app using debug-only StrictMode, then decide by measurement instead of refactoring on reflex — covers reading the violation stack for your own frames, the startup work that legitimately cannot move off the main thread (a pre-Room database snapshot), and setting a regression budget from the measured number rather than a round one. Use when checking ANR risk, after adding work to Application.onCreate, or before claiming a cold start is clean."
---

# Triaging main-thread I/O on Android

`Application.onCreate` accumulates work nobody measures: a crash-handler
install, a backup copy, a preference read. Each is invisible until a user with
years of data cold-starts on a slow morning. StrictMode makes it visible in one
launch; the mistake afterwards is refactoring everything it prints.

## 1. Install StrictMode in debug only, log never crash

```kotlin
if (BuildConfig.DEBUG) {
    StrictMode.setThreadPolicy(
        StrictMode.ThreadPolicy.Builder()
            .detectDiskReads().detectDiskWrites().detectNetwork()
            .detectCustomSlowCalls().penaltyLog().build(),
    )
}
```

`penaltyDeath` looks rigorous and is wrong here: the framework itself violates
the policy during startup, so death turns every launch into a crash.

## 2. Read only your own frames

A launch typically logs 100+ violations, nearly all framework
(`ActivityThread`, preference loading, profile installer). Filter to your
package:

```bash
adb shell logcat -c
adb shell am start -W -n <pkg>/.MainActivity && sleep 8
adb shell logcat -d -s StrictMode:* | grep "<pkg>"
```

The `~duration=NNms` on the violation header is the only number that matters;
a bare count of violations says nothing.

## 3. Measure before moving anything

For each of your frames, ask **how big does this get** and **how often does it
run**, then measure at realistic size in an instrumented test:

```kotlin
val started = System.nanoTime()
val snapshot = DbSnapshot.capture(context, TEST_DB)
val tookMs = (System.nanoTime() - started) / 1_000_000
```

Real example: a database byte-copy on the main thread looked alarming, measured
**11 ms for 0.3 MB at 1,000 sessions**, and was already throttled to one copy
per day — bounded, not an ANR.

## 4. Some startup work genuinely cannot move

A snapshot taken *before the first Room open* exists precisely because a failed
migration leaves data on disk but unreachable. Pushing it to a background
coroutine races the first database access and silently defeats it. When work
must stay on the main thread, the defence is a **budget test**, not a thread
switch — and say so in the comment so the next reader does not "fix" it.

## 5. Set the budget from the number you measured

A budget with 30x headroom can never fail, which is the same vacuous-green trap
as an unvalidated detector. Measure, then leave roughly an order of magnitude
for slower hardware:

- measured 11 ms → budget 150 ms (catches a real regression)
- measured 11 ms → budget 4000 ms (catches nothing; delete it or tighten it)

Prove the budget fires by setting it to `1L` once and reading the assertion —
that same run also prints the measurement you need for the comment.

## What this does not cover

StrictMode's thread policy sees disk and network, not CPU. A slow pure
computation on the main thread passes cleanly; for that, time the call directly
or use a frame-timing trace.
