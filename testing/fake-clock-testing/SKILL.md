---
name: fake-clock-testing
description: "Fake clocks / freeze time in tests across every mainstream runtime: freezegun (Python), Jest fake timers + Sinon @sinonjs/fake-timers (JS/TS), timecop (Ruby), java.time.Clock / InstantSource injection (JVM), .NET TimeProvider / FakeTimeProvider, and libfaketime (LD_PRELOAD for any native binary). Covers the language-agnostic discipline - inject or patch the clock, freeze vs tick vs advance vs set-system-time semantics, teardown so fake clocks never leak between tests - plus the shared anti-pattern table (real sleep under a frozen clock, leaked clock state, timezone-dependent assertions). Per-library setup, API, and CI recipes live in references/{python,js,ruby,jvm,dotnet,libfaketime}.md. Use when tests need deterministic control of now(), timers, or timeouts in any language, or when choosing the right fake-clock tool for a stack."
---

# fake-clock-testing

## Overview

Tests that read the real clock flake at midnight, on DST transitions, and on
slow CI runners. The fix is always the same discipline, whatever the
language: replace the clock the code under test reads, drive it explicitly,
and restore it afterwards. Two mechanism families exist:

| Family | How it works | Libraries |
|---|---|---|
| **Injection** | Production code takes a clock dependency; tests pass a fake | `java.time.Clock` / `InstantSource` (JVM), `TimeProvider` / `FakeTimeProvider` (.NET) |
| **Patching** | The library rewrites the runtime's time APIs in test scope | freezegun (Python), Jest fake timers + Sinon `@sinonjs/fake-timers` (JS), timecop (Ruby), libfaketime (libc interception, any binary) |

Injection needs source control of the code under test but has no global
state; patching works on unmodified code but must be scoped and torn down
per test.

## Choosing the tool

| Stack | Tool | Reference |
|---|---|---|
| Python (pytest / unittest) | freezegun | [references/python.md](references/python.md) |
| JS/TS in Jest | `jest.useFakeTimers()` (wraps Sinon's engine) | [references/js.md](references/js.md) |
| JS/TS in Mocha / Vitest / AVA / node:test / browser | `@sinonjs/fake-timers` directly | [references/js.md](references/js.md) |
| Ruby / Rails | timecop | [references/ruby.md](references/ruby.md) |
| Java / Kotlin / Scala | `Clock.fixed` / `MutableClock` / `InstantSource` injection | [references/jvm.md](references/jvm.md) |
| C# / F# (.NET 8+) | `TimeProvider` + `FakeTimeProvider` | [references/dotnet.md](references/dotnet.md) |
| C/C++, closed-source or multi-process binaries | libfaketime (`LD_PRELOAD` escape hatch) | [references/libfaketime.md](references/libfaketime.md) |

libfaketime is the fallback when language-native fakes cannot reach the
code: it intercepts libc `time()` / `gettimeofday()` / `clock_gettime()`,
so it covers any dynamically linked binary regardless of language.

## The four clock operations

Every library exposes some subset of the same four operations; tests should
name which one they rely on:

1. **Freeze** - pin now() to a fixed instant; successive reads are equal
   (`freeze_time`, `Timecop.freeze`, `Clock.fixed`, `jest.setSystemTime`
   after `useFakeTimers`).
2. **Advance** - move the frozen clock forward by a duration, firing any
   timers that come due (`jest.advanceTimersByTime`, `clock.tick`,
   `FakeTimeProvider.Advance`, `freezer.tick`).
3. **Set / jump** - reposition the clock to an absolute instant without
   firing intermediate timers (`setSystemTime`, `freezer.move_to`,
   `Timecop.travel`). Use for large jumps; advancing through a year fires
   every intermediate timer one-by-one and crawls.
4. **Restore** - put the real clock back (`useRealTimers`,
   `clock.uninstall`, `Timecop.return`, decorator/context-manager exit).
   Always in an after-each hook, never at the end of the test body - a
   failed assertion would skip it and leak the fake clock into the next
   test.

## Worked example - a boundary test on an expiring token

The canonical shape, here with .NET's `FakeTimeProvider` (the same
freeze-then-advance pattern maps 1:1 onto every library in references/):

```csharp
var fakeTime = new FakeTimeProvider(
    new DateTimeOffset(2026, 5, 20, 12, 0, 0, TimeSpan.Zero));
var svc = new TokenService(fakeTime);              // clock injected
var expiresAt = fakeTime.GetUtcNow().AddHours(1);

Assert.False(svc.IsExpired(expiresAt));            // frozen: still valid

fakeTime.Advance(TimeSpan.FromHours(1));           // advance to the boundary
Assert.False(svc.IsExpired(expiresAt));            // boundary is inclusive

fakeTime.Advance(TimeSpan.FromTicks(1));           // one tick past
Assert.True(svc.IsExpired(expiresAt));
```

The test asserts on both sides of the boundary and never sleeps; it passes
in microseconds on any runner at any wall-clock time. In freezegun the same
test is `freeze_time(...)` + `freezer.tick(...)`; in Jest,
`setSystemTime` + `advanceTimersByTime`; in Ruby, `Timecop.freeze` + a
second freeze at the boundary.

## Anti-patterns

| Anti-pattern | Why it fails | Fix |
|---|---|---|
| Real `sleep()` inside a frozen-clock test | Sleep is wall-clock; the frozen clock never advances - the test just gets slower | Advance the fake clock instead (`tick` / `Advance` / `advanceTimersByTime`) |
| Fake clock leaking between tests | Restore skipped on assertion failure; later tests inherit frozen time and fail mysteriously | Restore in `afterEach` / fixture teardown, not the test body |
| Timezone-dependent assertions | `new Date().toString()` / `datetime.now()` render in host-local zone; green locally, red in CI | Assert on UTC instants or set the zone explicitly (`TZ` env, `tz=`, `SetLocalTimeZone`) |
| Mixing real and fake time in one test | Real `fetch` / `Thread.Sleep` / C-extension resolves on the real clock; races with faked timers | Fake everything time-related in the test, or fake nothing |
| Date-only freeze (`freeze_time("2026-05-20")`) | Interpreted as midnight local; off-by-one around zone boundaries | Freeze a full ISO-8601 instant with offset |
| Hardcoded timestamps that age (`assert year == 2026`) | Test rots on the next New Year | Derive expectations from the frozen instant |
| Advancing years via timer ticks | Every intermediate timer fires; test crawls | Set / jump to the target instant instead |
| Asserting durations from the wall clock | Frozen wall clock breaks elapsed-time math | Use the monotonic clock for durations; fake it only when the library supports it |

## Limitations

- **Patching libraries stop at the language boundary.** C extensions,
  native gems, and statically linked binaries read the real
  `clock_gettime()`; use libfaketime for those
  ([references/libfaketime.md](references/libfaketime.md)).
- **Injection requires owning the code.** Third-party libraries that call
  `Instant.now()` / `DateTime.UtcNow` internally cannot be reached by
  injected clocks.
- **Monotonic clocks are usually not faked by default**
  (`performance.now`, `process.hrtime`, `GetTimestamp`); check each
  library's selective-faking option before asserting on them.
- **DST resolution depends on the runtime's tz database** (ICU in Node,
  system tzdata in Python, JDK tzdata on the JVM). Pin the zone per test
  and assert against `dst-transition-reference`'s documented behaviours.
- **No library simulates leap seconds** - see
  `dst-transition-reference` references/leap-seconds.md.

## References

- Per-library recipes:
  [references/python.md](references/python.md) (freezegun),
  [references/js.md](references/js.md) (Jest + Sinon fake timers),
  [references/ruby.md](references/ruby.md) (timecop),
  [references/jvm.md](references/jvm.md) (Clock / InstantSource),
  [references/dotnet.md](references/dotnet.md) (TimeProvider / FakeTimeProvider),
  [references/libfaketime.md](references/libfaketime.md) (LD_PRELOAD).
- Companion catalog: `dst-transition-reference` (DST bug classes +
  leap-second reference).
- Test-matrix builder: `timezone-test-matrix-builder` wires these fakes
  into a per-touchpoint timezone/DST matrix.
