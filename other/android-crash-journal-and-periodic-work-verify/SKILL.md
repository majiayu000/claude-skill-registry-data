---
name: android-crash-journal-and-periodic-work-verify
description: "Prove an Android app's own crash journal records a real crash and that its periodic WorkManager job is actually registered with the OS — covers the am crash routing, the below-the-fold Settings trap that reads as \"no crashes\", identifying the job as yours via its constraints, and what dumpsys does not tell you. Use when an app substitutes a local crash log for a crash-reporting SDK, or when a \"syncs daily\" claim rests only on schedule() being called."
---

# Verifying a crash journal and a periodic job on device

Two claims that are usually only checked at the call site: "crashes are
recorded" and "it syncs on a schedule". Both are verifiable in minutes, and
both have a trap that makes a working feature look broken.

## 1. Force a real crash through the app's handler

`am crash` delivers a `RemoteServiceException` **through the app process**, so
a `Thread.setDefaultUncaughtExceptionHandler` installed at startup does run:

```bash
adb shell am crash <pkg>
sleep 4
adb shell pidof <pkg>          # empty: the process died, as it should
```

Then relaunch and read the record off disk (debuggable builds only):

```bash
adb shell run-as <pkg> ls -l /data/data/<pkg>/files/crash/
adb shell run-as <pkg> cat /data/data/<pkg>/files/crash/<file>
```

A record worth having names app version, API level, device, thread and the
stack. If the directory exists but is empty, the handler was installed *after*
the crash path or was replaced — check it is installed unconditionally in
`Application.onCreate`, not behind a debug flag.

**Clean up afterwards.** A synthetic crash left in the journal is a fake defect
for whoever reads it next:

```bash
adb shell run-as <pkg> rm -f /data/data/<pkg>/files/crash/<file>
```

## 2. The trap: the UI section is below the fold

A crash-count row usually sits near the bottom of a settings screen. A single
`uiautomator dump` right after opening Settings reports **no crash text at
all**, which reads exactly like "the journal did not record". Scroll before
concluding:

```python
for i in range(10):
    x = dump()
    if "crash record" in x or "No crashes recorded" in x: break
    sh("shell","input","swipe","540","1500","540","700","300")
```

Same class as tapping stale coordinates: settle the screen, then read.

## 3. Prove the periodic job exists at the OS

`schedule()` being called proves nothing — WorkManager may have rejected,
replaced, or never persisted it. Ask the system:

```bash
adb shell dumpsys jobscheduler | grep -n -i <pkg>
```

Look for a job whose **Service** is the app's own:

```
JOB androidx.work.systemjobscheduler:uXXX/0
  Service: <pkg>/androidx.work.impl.background.systemjob.SystemJobService
  Requires: charging=false batteryNotLow=true deviceIdle=false
  Unsatisfied constraints: TIMING_DELAY
```

**Identify it as yours by its constraints.** `batteryNotLow=true` and nothing
else matches a request built with
`Constraints.Builder().setRequiresBatteryNotLow(true)`. That correspondence is
what turns "a job exists" into "our job was accepted".

`TIMING_DELAY` unsatisfied is the healthy state for a periodic job between
runs — not a fault.

## 4. What this does NOT tell you

The **interval is not printed** in that dumpsys output. A job scheduled with
the wrong period looks identical. Say so rather than implying it was observed:
source the interval from the code (`PeriodicWorkRequestBuilder(Duration.ofDays(1))`)
and mark it as unverified-on-device.

Splitting `dumpsys jobscheduler` on `JOB #` also mis-attributes blocks to other
packages — grep for the package and read the surrounding lines instead.
