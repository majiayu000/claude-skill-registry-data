---
name: agent-device
description: >-
  Drive the Apex Factory app on a leased iOS simulator or Android emulator
  with agent-device through .agents/scripts/device-lane.sh — open the app,
  read the accessibility snapshot, tap, type, scroll, verify with wait/is/get,
  take screenshots, record evidence, and write or replay agent-device .ad
  scripts (the e2e tests under apps/mobile/e2e/). Use for any interaction with
  a device, when writing an e2e: test, or when someone says "check it on the
  simulator", "tap through the app" or "dogfood the app".
---

# agent-device in this repo

Vendored from `callstack/agent-device` (see `SOURCE.md`) and adapted. agent-device is the
workspace's pinned devDependency. Every agent interaction with a device goes through it, and
every agent-device call that touches a device goes through the lane script:

```bash
.agents/scripts/device-lane.sh ad <agent-device command and args>
```

The script adds the leased device (`--udid` or `--serial`), simlock's device set
(`--ios-simulator-device-set`), the platform and the lane's session (`--session
apex-<branch>`), renews the lease when it is due, and refuses flags that would pick another
device. Never pass those flags yourself, never run `npx agent-device` or a global
`agent-device`, and never call `xcrun simctl`, `adb` or `emulator` to boot, erase, install or
screenshot. `pnpm exec agent-device help <topic>` is fine: help touches no device.

## The lane around it

```bash
.agents/scripts/device-lane.sh lease ios                 # 0 leased, 2 still queued (run again), 75 busy, 69 unavailable
.agents/scripts/device-lane.sh build ios release         # detached; prints <log>; wait for <log>.exit
.agents/scripts/device-lane.sh install                   # the last successful build, on the leased device
.agents/scripts/device-lane.sh ad open com.callstack.apexfactory --foreground
# ... the loop below ...
.agents/scripts/device-lane.sh ad close
.agents/scripts/device-lane.sh release                   # always, on every path out
```

simlock erases a simulator when its lease ends, so install the app on every new lease. A build
holds no lease; lease after the build has started, not before, so the device is not idle while
Xcode runs.

## Recommended agent rule (upstream, adapted)

Use agent-device only for app and device automation. For a normal app-driving task, start
immediately. Do not probe first with `--help`, `--version`, `devices`, `appstate`, `snapshot`,
or `screenshot`; open the requested app in the foreground and continue from its initial
interactive snapshot. For exploratory QA read `references/dogfood.md`. For logs, network,
traces, or runtime failures, read `pnpm exec agent-device help debugging`. For React Native
apps, overlays and Metro blockers, read `pnpm exec agent-device help react-native`. Prefer
`open -> snapshot -i -> act -> re-snapshot -> verify -> close`. Use current refs such as `@e3`
for exploration and selectors for durable replay. Keep mutating commands against one session
serial. Capture screenshots, logs, network, traces, recordings and `.ad` replay scripts only
when they add evidence.

## The loop

```bash
.agents/scripts/device-lane.sh ad open com.callstack.apexfactory --foreground   # initial snapshot with @refs
.agents/scripts/device-lane.sh ad press @e7 --settle                            # prints the UI diff
.agents/scripts/device-lane.sh ad fill @e3 "hello" --settle
.agents/scripts/device-lane.sh ad scroll down --settle
.agents/scripts/device-lane.sh ad wait text "Shipped at the booth"
.agents/scripts/device-lane.sh ad is visible 'id="status-api"'
.agents/scripts/device-lane.sh ad get text 'id="shipped-count"'
.agents/scripts/device-lane.sh ad open com.callstack.apexfactory "apexfactory:///features/12"   # deep link
.agents/scripts/device-lane.sh screenshot pr12-1                                # <main>/.worktrees/sim-shots/pr12-1.png
.agents/scripts/device-lane.sh ad close
```

- Copy refs byte for byte: `@e12`, `@e12~s4`. Prefer current refs, then `id`/`label`/`role`
  selectors; coordinates are a last resort, after a screenshot.
- `--settle` only on press/click/fill/longpress/scroll/back, never on open, snapshot or close.
- Verify a named expectation with `wait text`, `wait <selector>`, `wait absent <selector>`,
  `is` or `get`. A bare screenshot is not verification; a screenshot is evidence for a person.
- Error output carries corrective hints; follow them instead of re-planning.
- The app's selectors are its `testID`s and accessibility labels (`id="home-headline"`,
  `id="status-api"`, `id="shipped-feature-<id>"`, `id="update-banner"`; the full rule is in
  `apps/mobile/AGENTS.md`). When the selector a check needs does not exist, that is a finding
  for the implementer, not a reason to tap coordinates.

## Replay scripts (`.ad`) — the `e2e:` tests

A spec's `e2e:` test is an agent-device replay script in `apps/mobile/e2e/<name>.ad`, run on
a leased device. `apps/mobile/e2e/home.ad` is the model:

```
context platform=ios timeout=120000
env APP_ID=com.callstack.apexfactory
open ${APP_ID} --relaunch
wait id="home-headline" 60000
is visible "id=\"home-headline\" label=\"This app is empty. On purpose.\""
is exists id="shipped-empty"
close
```

```bash
.agents/scripts/device-lane.sh ad replay apps/mobile/e2e/home.ad  # one script; exit 0 is pass
.agents/scripts/device-lane.sh ad test 'apps/mobile/e2e/*.ad'     # the suite, one replay per script
```

The lane runs a script inside its own agent-device session, which knows simlock's device set
(agent-device 0.21.20 loses the set in `replay`'s private daemon and in `test`'s per-script
sessions, so the lane opens the app first and replays each script itself). Do not `close`
before a replay, and do not call `agent-device test` directly.

- A script names selectors, never refs or coordinates, so it survives layout changes.
- Write the expectation the spec states (`is visible`, `wait text`), with explicit timeouts on
  waits that cross the network.
- Known gaps in 0.21.20: `label~=` and `scroll --until` did not work inside `.ad` scripts; use
  exact `label=`/`id=` and `scroll bottom`.
- A script that ends with `close` ends the lane's session too: `ad open` again before more
  commands. `open --relaunch` kills the app, which also ends an appduct session (pair again).
- On a failure, `replay` prints the step that diverged with ranked selector suggestions; it
  never edits the `.ad` file. Report the step, do not rewrite the test to pass.

## Evidence

```bash
.agents/scripts/device-lane.sh ad logs start          # then reproduce, then:
.agents/scripts/device-lane.sh ad logs stop
.agents/scripts/device-lane.sh ad network dump 20     # HTTP seen in the app's logs
.agents/scripts/device-lane.sh record start <name>    # ... record stop: sim-shots/<name>.mp4
```

Screenshots and recordings are never committed: describe them in a report. The
`verify-mobile` skill uploads its own as PR attachments (`attach.sh`, ADR 0023).

## Not allowed here

`agent-device install-from-source`, `react-devtools` (fetches from npm), `daemon`, `connect`,
`prepare` and `close --shutdown` are refused by the lane script; a host-level step such as
pre-warming the iOS runner is the maintainer's (see `docs/internal/DEVICES.md`). If two lanes
run at once, keep to your own session: never close or kill another session's runner.

## References

- `references/ios-simulator.md`, `references/android-emulator.md` — platform notes.
- `references/dogfood.md` — exploratory QA.
- `pnpm exec agent-device help workflow` — refs, selectors, waits, recovery.
