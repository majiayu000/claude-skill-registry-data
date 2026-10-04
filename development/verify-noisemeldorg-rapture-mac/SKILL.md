---
name: verify
description: Build, launch, and drive a Debug build of Rapture for Mac to verify changes end-to-end against its real surfaces (destination folder, relay folder, menu bar). Use when verifying capture/triage/relay changes by observing the running app rather than the test suite.
---

# Verifying Rapture for Mac live

The app's surfaces are filesystem side effects (the notes destination, the iCloud relay folder) plus the menu bar. Drive them by dropping files and observing what the running app produces.

## Build + launch

```sh
xcodebuild -derivedDataPath /tmp/RaptureMacDerived \
  -project RaptureMac/RaptureMac.xcodeproj -scheme RaptureMac \
  -configuration Debug build            # test runs also produce the app

pkill -x Rapture                        # quit the installed app (watermark catch-up recovers anything missed)
open -n /tmp/RaptureMacDerived/Build/Products/Debug/Rapture.app   # -n + the full path launches THIS bundle
ps -ax -o pid,comm | grep "Rapture.app/Contents/MacOS"          # confirm the /tmp binary is the one running
```

**Never move or rename `/Applications/Rapture.app`** to get the Debug build to launch. Moving the installed app aside and back made macOS drop its Full Disk Access grant (2026-09-29): the user had to re-grant it and Quit & Reopen. `open -n <full path>` launches the Debug bundle without touching the installed one.

**Always restore when done** (and relaunch — the user's capture pipeline was running):

```sh
pkill -x Rapture
open /Applications/Rapture.app
ps -ax -o pid,comm | grep "Rapture.app/Contents/MacOS"          # confirm /Applications is running again
```

## Debug isolation (what to drive)

- Notes destination: `~/Documents/Rapture Notes (Debug)/`
- Relay folder: `~/Library/Mobile Documents/iCloud~noisemeld~Rapture/Relay (Debug)/`
- Settings/state: `~/Library/Application Support/Rapture for Mac (Debug)/{settings.json,state.json}`

Drop `.txt` files at the destination root (or a `.txt`+`.m4a` pair in the relay folder) and watch the outputs. `state.json` is the best oracle: `triagedRecords` / `relayFiledRecords` / `lastError` record exactly what the app did and when.

## Gotchas (all bitten before)

- **A freshly built debug binary re-triggers Full Disk Access onboarding, and granting it quits the app.** Each rebuild is a new bundle at a new/changed signature, so TCC treats it as a new app: the FDA sheet opens on launch, and after the user grants FDA the app must quit and relaunch to see it (a running process never picks up a new grant). To the verifying agent this looks like the app **silently vanished mid-test** — no crash report, drops stop being processed. What to do: (a) if the surfaces under test don't need FDA (relay, triage, enrichment — most of them), tell the user up front they can ignore/dismiss the FDA sheet for this run; (b) poll process liveness (`kill -0 <pid>`) between steps rather than assuming the pid survives; (c) if it exited, just `open` it again — settings/state are on disk and the test continues where it left off; (d) if the user *does* grant FDA mid-run, expect exactly one quit-and-relaunch cycle and re-`open` afterwards.

- **App Nap stalls the poll loops.** A debug build launched via `open` from a shell has no window and no user input, so macOS naps it — 5s polls stretched to ~18 minutes in one session. Wake it deterministically after each file drop: `sample <pid> 1 >/dev/null 2>&1` (attaching wakes the process), then wait ~10s (two poll ticks; the triage settle rule needs two same-size sightings ≥5s apart). The user-launched production app has not shown this in dogfooding, but keep it in mind if "nothing happens."
- **The debug build has no Full Disk Access**, so iMessage capture won't run (FDA poll loops harmlessly; a permissions window may open). Relay + triage surfaces need no FDA and are fully drivable.
- **`log show`/`log stream` return nothing from the sandboxed shell.** Use `state.json`, output files, and `sample <pid>` stacks as evidence instead.
- Don't pre-create files you expect the app to create; don't clean the debug notes folder — it's isolated scratch and prior artifacts are useful realism.
- **Exec'ing the binary directly never starts the pipeline.** `pipeline.start()` fires from the menu-bar label's `.task`, which needs a proper LaunchServices launch — a directly-exec'd binary sits idle forever (looks like "nothing happens", no errors). To pass an env var (e.g. `RAPTURE_AI_FORCE_ENGINE=anthropic`), use `launchctl setenv KEY value` then `open …/Rapture.app`, and `launchctl unsetenv KEY` when done.
- **Planting a keychain item with the `security` CLI blocks the app on an ACL dialog** (invisible in a headless session — the process hangs inside `SecItemCopyMatching`). Add `-A` (any-app access) when planting a test key for the debug service `noisemeld.RaptureMac.debug`. App-created items (Settings → Triage → Save) never prompt.
- **Don't relaunch the installed app while a test run is in flight** — the shared bundle ID can abort the hosted test session partway ("TEST FAILED" with a fraction of the suite executed, zero failures). Re-run after the launch settles.
