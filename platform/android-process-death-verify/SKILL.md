---
name: android-process-death-verify
description: "Verify an Android app survives process death and restores its work — backgrounding before killing (am kill spares foreground apps), proving the kill actually happened, distinguishing persisted state from in-memory state, and the two harness traps that make the check pass vacuously (an uninstalled app after an instrumented run, and stale uiautomator tap coordinates). Use when checking state restoration, \"does my app lose data when Android kills it\", or before claiming a screen survives backgrounding."
---

# Verifying process death on Android

Android kills backgrounded apps under memory pressure. The question is never
"does it crash" alone — it is **what does the hunter lose**. Data in Room
survives; data in a ViewModel does not.

## The procedure

```python
sh("shell","logcat","-c","-b","crash")          # clear the crash buffer FIRST
# 1. get into the deep, state-heavy screen and record its markers
# 2. background it — this step is not optional (see trap 1)
sh("shell","input","keyevent","KEYCODE_HOME"); time.sleep(2)
sh("shell","am","kill","<pkg>"); time.sleep(3)
assert not sh("shell","pidof","<pkg>").strip()   # PROVE the kill happened
# 3. relaunch the way the launcher would, not with an explicit component
sh("shell","monkey","-p","<pkg>","-c","android.intent.category.LAUNCHER","1")
# 4. crash buffer empty? is the WORK still offered back?
```

Judge two things separately:

| question | verdict |
|---|---|
| crash buffer empty after relaunch | must pass |
| the work itself is offered back | must pass — e.g. a CTA reading `RESUME · …` |
| navigation position restored | usually a legitimate non-goal; say so explicitly |

A live session that reappears as `RESUME` proves it was **persisted**, not held
in memory. That is the distinction worth reporting; "no crash" alone is weak.

## Trap 1: `am kill` silently spares foreground apps

`am kill` only targets **background** processes. Run it on the foreground app
and it returns success while the process keeps running, so the app never died
and "state restored!" is measuring nothing. Always `KEYCODE_HOME` first, then
assert `pidof` is empty. If `pidof` still prints a pid, the test is void.

`am force-stop` kills regardless, but it also clears state Android would have
kept, so it models a user swiping the app away rather than a system kill. Use
`am kill` for the memory-pressure case.

## Trap 2: an instrumented run leaves the app uninstalled

`connectedAndroidTest` uninstalls the APK when it finishes. A device sweep run
straight after a gate drives an **empty launcher** and every marker reads
absent, which looks exactly like catastrophic state loss. Symptom: the dump
contains `Calendar, Camera, Chrome, Clock …`.

Reinstall before any device sweep, and never silence the install output — a
silenced failure produces a stale-build verdict that wastes the whole run.

## Trap 3: stale tap coordinates

Dumping the tree, then scrolling to find a label, then tapping bounds from the
**first** dump taps whatever moved into that spot. The screen you wanted never
opens, and subsequent searches scroll the screen behind it while reporting
"unreachable".

Take the bounds and the tap in the same breath:

```python
def tap_fresh(label, by="text"):
    x = dump()                                   # dump and tap together
    m = re.search(rf'{by}="{re.escape(label)}"[^>]*bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"', x)
    if not m: return False
    a,b,c,d = map(int, m.groups())
    sh("shell","input","tap",str((a+c)//2),str((b+d)//2)); time.sleep(3.5); return True
```

Then **confirm the screen actually changed** before searching it — assert a
marker unique to the new screen. A search run against the old screen is the
vacuous-pass shape.

## Reporting

State which of the three traps were hit; each one produces a confident false
result, and a reader who does not know them will repeat the run and disagree
with you. Note explicitly whether navigation position is restored, so nobody
later reads "survives process death" as a promise it returns you to the screen.
