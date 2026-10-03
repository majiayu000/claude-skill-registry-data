---
name: hermes-crashes
description: Decoding Hermes crashes and minified production stack traces. Use for "address at index.android.bundle" frames, unsymbolicated or badly grouped Sentry events, SIGSEGV in libhermes, ANRs, source maps.
user-invocable: false
---

# Making production crashes readable

## First, classify the crash

Three families, three completely different investigations:

1. **JS error**: a thrown Error, a rejected promise, a render error. Stack frames point into the JS bundle (`index.android.bundle`, `main.jsbundle`). Fix in JS.
2. **Native crash**: SIGSEGV, SIGABRT, EXC_BAD_ACCESS, frames in `libhermes.so` or platform frameworks. The JS code may be the trigger but the defect is in a native module or in JSI usage.
3. **ANR / watchdog kill**: no crash at all, the main thread was blocked. Investigate what ran long, not what threw.

Misclassifying wastes days. A SIGSEGV cannot be fixed by editing JavaScript, and an unhandled rejection will never appear in a tombstone.

## Decoding "address at index.android.bundle:1:589926"

That address is an offset into Hermes bytecode, not a line and column in your source. The decoder is metro-symbolicate plus the source map that was generated for that exact build:

```bash
# paste the raw stack into a file, then:
npx metro-symbolicate path/to/index.android.bundle.map < stack.txt
```

Rules that make this work:

- The map must come from the same build as the crashing bundle. A map from a rebuild of "the same commit" often still matches, but treat any nonsense output as a map mismatch.
- Expo/EAS builds can emit source maps during the build; keep them as build artifacts. If you have no map for a release, that release's crashes stay unreadable forever, so archiving maps per release is part of the release process, not an optimization.

## Sentry (or any crash reporter) symbolication checklist

When events show minified frames instead of source:

1. Current tooling matches bundle and map through Debug IDs injected into both at build time; the usual failure is that the upload step ran locally but not in the release lane. Confirm the CI job actually uploaded artifacts for the build that is crashing.
2. On older release-plus-dist setups, maps must be uploaded per release AND distribution. A dist mismatch fails silently and looks exactly like "sourcemaps don't work".
3. Same for the release name: what the app reports at runtime must equal what the maps were uploaded under. Log both once and compare character by character.

## The "Object captured as exception" disease

Error monitoring full of events titled `Object captured as exception with keys: code, details, hint, message` means non-Error objects are being thrown or captured. Consequences: useless titles, and worse, wrong grouping, because grouping falls back to the capture callsite instead of the error identity.

Fix it at the boundary: normalize everything to a real Error before capture. Give the Error a meaningful `name` (include an error code when one exists) and keep the original object on `cause`. One small `normalizeError(err)` helper applied at every `captureException` callsite turns a swamp of identical events into distinct, countable issues. Copy-ready implementations of `normalizeError` and the abort filter are in [reference.md](reference.md).

Related hygiene that pays off immediately:

- Network timeouts and aborts (`AbortError`) are connectivity weather, not bugs. Capture them at warning level with a fixed fingerprint so they group into one issue instead of flooding the error feed.
- Tag events with a small set of stable dimensions (flow, action) at capture time. Filtering by tag later is how you find the real signal.

## Native crashes

- Android: get the tombstone (`adb bugreport`, or Play Console's crash section). Frames in a library's `.so` file name the culprit directly. Frames in `libhermes.so` with no library frames usually mean a JSI misuse: some native module touched JS values off the JS thread or kept a reference across invalidation. Look at recently added or recently upgraded native modules first.
- iOS: crash logs from the device or from the store's crash organizer, plus the dSYMs for that build. Upload dSYMs to your crash reporter in the release lane; with bitcode long gone there is no excuse for missing them.
- Both platforms: a native crash that appeared after exactly one dependency changed is that dependency until proven otherwise. `git log -p package.json` is a legitimate debugging tool.

## ANRs

The report shows where the main thread was stuck, which is often innocent framework code waiting on your work. Usual causes worth hunting in JS land: synchronous storage on startup, megabyte JSON.parse on interaction, unbatched bridge/JSI traffic in a hot loop, and dev-only logging left on in release. Reproduce with a release build; debug builds have completely different performance characteristics and will mislead you.
