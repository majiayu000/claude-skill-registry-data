---
name: android-action-idempotence-verify
description: "Prove an Android/Compose action that mints or spends (complete session, claim reward, collect currency, roll gacha, submit payment) cannot double-pay or crash when tapped twice — covers the invariant-by-throw trap where the repository refuses correctly but the ViewModel launches it uncaught, the concurrent-callers test that a sequential test misses, and why one lucky device tap proves nothing. Use when auditing economy/mutating actions, or before claiming a button is safe to press twice."
---

# Verifying action idempotence on Android

A button that mints XP, spends currency, claims a reward or submits an order must
act **exactly once** however hard it is pressed. Two independent things can be
wrong, and fixing one does not fix the other:

1. **The ledger** — does a second invocation pay twice?
2. **The failure mode** — *how* does the second invocation get refused?

The second is the one that gets missed, because the first is usually already
correct.

## The invariant-by-throw trap

The common (good) pattern is a guard inside the transaction:

```kotlin
suspend fun completeSession(id: Long) = db.withTransaction {
    val session = sessionDao.byId(id) ?: error("not found")
    check(session.completedAtMs == null) { "Session already completed" }
    ...
}
```

This is correct for the ledger and **refuses by throwing**. Now look at the caller:

```kotlin
fun complete(onResult: (Result) -> Unit) {
    viewModelScope.launch { onResult(repo.completeSession(sessionId)) }   // no catch
}
```

A second tap landing before the UI replaces the button takes that exception
straight into `viewModelScope` — a crash, on the app's primary action. The data
is safe and the app dies anyway.

Fix at the caller, keeping the repository invariant as-is:

```kotlin
private var inFlight = false

fun complete(onResult: (Result) -> Unit) {
    if (inFlight) return
    inFlight = true
    viewModelScope.launch {
        runCatching { repo.completeSession(sessionId) }
            .onSuccess(onResult)
            .onFailure { inFlight = false }   // a real failure must be retryable
    }
}
```

Reset the flag on failure only. Resetting it on success re-opens the race.

## Step 1 — find the actions worth checking

Anything that writes a currency, an award, a streak, a purchase or a remote
mutation. Grep the ViewModels for launches with no guard:

```bash
rg -n "viewModelScope.launch" app/src/main/kotlin | wc -l
rg -n -B3 "viewModelScope.launch" app/src/main/kotlin | rg -n "if \(.*\) return|_loading|inFlight"
```

Compare against actions that already guard (exports and imports usually do —
that is the idiom to copy). The unguarded economy actions are the findings.

## Step 2 — prove the ledger with a CONCURRENT test

A sequential test (`complete(); complete()`) only proves the second caller sees
committed state. The real double-tap has **both callers in flight before either
commits**, which is a different code path through the transaction:

```kotlin
@Test
fun twoConcurrentCompletionsStillPayOnce() = runBlocking {
    val id = seedSessionWithOneDoneSet()
    val results = coroutineScope {
        val a = async { runCatching { repo.completeSession(id) } }
        val b = async { runCatching { repo.completeSession(id) } }
        listOf(a.await(), b.await())
    }
    assertEquals(1, results.count { it.isSuccess })
    val paid = results.first { it.isSuccess }.getOrThrow().xpAwarded.toLong()
    assertEquals(paid, db.profileDao().get()!!.totalXp)   // the LEDGER, not the exception
    assertEquals(1, db.sessionDao().completedCount())
}
```

**Assert the ledger, not the exception.** `assertTrue(second.isFailure)` passes
for a build that throws *after* paying. Assert the stored total and the row count.

Write both tests: sequential and concurrent. They fail differently.

## Step 3 — device check, with the right expectations

Drive a real action and fire taps with no gap **in one shell invocation**, so
the gap is adb's, not Python's:

```bash
adb -s $SERIAL shell "input tap $X $Y; input tap $X $Y; input tap $X $Y; input tap $X $Y"
sleep 5
adb -s $SERIAL logcat -d -b crash    # must be empty
```

Then read the award line from a `uiautomator dump` and confirm it paid once.

**A clean device run proves little on its own.** If the UI replaces the button
fast enough, the taps never race and the check passes on a build that is
genuinely broken. The device run confirms no crash and a single payment; the
*concurrent instrumented test* is what establishes the behaviour. Do not skip
step 2 because step 3 looked fine.

## Traps

- **Reading the wrong node** when checking whether the button became disabled:
  `enabled` sits on the clickable ancestor; the label's own node reports `true`
  regardless. Walk parents until `clickable="true"`.
- **A guard flag that never resets** turns a transient failure into a dead
  button for the rest of the screen's life. Reset on failure.
- **`pm clear` between attempts** — a completed session cannot be completed
  again, so each device attempt needs fresh state.
- **Rest days / schedule-dependent entry points**: the primary CTA may be absent
  today. Find a schedule-independent route into the same action (a quick/free
  session) rather than waiting for the calendar.
