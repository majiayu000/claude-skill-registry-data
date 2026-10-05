---
name: ios-debugger-agent
description: Build, run, and debug iOS apps on a simulator. Use when asked to run an iOS app, interact with the simulator UI, capture logs, or diagnose runtime behavior.
---

# iOS Debugger Agent

Build and run iOS projects on a booted simulator, interact with the UI, and capture logs for debugging — via the `flowdeck` skill, which is this lacquer's canonical source of truth for exact FlowDeck syntax. This skill is a thin, scenario-specific wrapper around it, not a competing source of commands. If a command below errors or you're unsure of a flag, consult `flowdeck`'s `resources/` docs or run `flowdeck <command> --help` rather than guessing — never fall back to `xcrun`/`simctl`/`xcodebuild`.

## Overview

FlowDeck ties build, install, and launch together (`flowdeck run`), and streams logs from the running app rather than querying the OS unified log. There is no need to discover DerivedData paths, hand-construct `xcodebuild` destinations, or spawn `log stream` predicates — FlowDeck's config-first workflow and app-tracking model replace all of that.

## Prerequisites

- FlowDeck CLI installed (`flowdeck --version`)
- Project with `.xcodeproj` or `.xcworkspace`
- A saved FlowDeck config, or enough context to create one (`flowdeck context --json`)

## Core Workflow

### 1) Check for a saved config first

```bash
flowdeck config get --json
```

If a config exists, use bare commands (`flowdeck build`, `flowdeck run`, etc.) for the rest of this workflow. If not, discover and create one:

```bash
flowdeck context --json
flowdeck config set -w <workspace> -s <scheme> -S "<simulator>"
```

### 2) Discover the booted simulator (if you need a specific one)

```bash
flowdeck simulator list --json
```

Check each entry's `state` field for `"Booted"`. If none are booted and you need a specific device, boot one by UDID (boot takes a UDID, not a name):

```bash
flowdeck simulator boot <udid>
```

### 3) Build the project

```bash
flowdeck build
```

Add `-w <workspace> -s <scheme> -S "<simulator>"` only if no config is saved and you're not overriding it.

### 4) Install and launch the app

```bash
flowdeck run
```

This builds, installs, and launches in one step, returning an **App ID**. To launch an existing build without rebuilding:

```bash
flowdeck run --no-build
```

There is no standalone "install only" verb for simulators — FlowDeck ties install to launch by design. (Physical devices are the exception: `flowdeck device install <udid> <path-to-app>` installs without launching — see `resources/device.md` in the `flowdeck` skill.)

### 5) Capture logs

Either launch with logs streaming immediately:

```bash
flowdeck run --log     # run with run_in_background: true
```

Or attach to an already-running app:

```bash
flowdeck apps                 # find the App ID
flowdeck logs <app-id>        # run with run_in_background: true — this is a continuous stream
```

Never use `xcrun simctl spawn … log`, `log show`, or `log stream` — FlowDeck captures all `print()` and `OSLog` output in this one stream.

## UI Interaction

### Read and act on the UI

Verify what's on screen and drive the UI by reading the accessibility tree as
text, not by capturing and reading an image — it is orders of magnitude
cheaper and more precise for the same question ("what's on screen", "did that
tap land", "what can I tap next"):

```bash
rocketsim elements --agent-mode nav             # or --agent-mode act for values/enabled-state
# or, if RocketSim isn't available:
flowdeck ui simulator screen -S "<sim>" --tree --json
```

Act on the result by element id or label — `rocketsim interact tap --id <id>`,
or `flowdeck ui simulator tap "<label>"` / `tap --point x,y`. Re-snapshot the
tree after any action that changes the screen rather than reusing stale ids.

### Take a screenshot

Reach for an actual screenshot only when the question is genuinely visual —
layout and spacing, contrast, comparing against a design mockup, or anything
else the tree can't express. Screenshots are primarily session-based, not
one-off:

```bash
flowdeck ui simulator session start -S "<sim>" --json
# Read the `latest_screenshot` path from the JSON response with the Read tool
```

For a single one-off capture when no session is running:

```bash
flowdeck ui simulator screen -S "<sim>" --output /tmp/screenshot.png
```

To let a human watch the simulator live instead of relaying screenshots,
surface `rocketsim preview` — it streams the simulator to a local browser page
and costs the agent no tokens.

### Record video

```bash
flowdeck simulator record -S "<sim>"                      # record until Ctrl+C, or add --duration 10s
```

For frame-by-frame capture (e.g. validating an animation) instead of a video file, use `flowdeck simulator frames -S "<sim>"` (contact sheet by default, `--images` for full-res PNGs per frame).

### Open a URL in the simulator

```bash
flowdeck ui simulator open-url "myapp://deeplink" -S "<sim>"
```

### Send a push notification

```bash
flowdeck simulator push notification.apns -b com.example.MyApp -S "<sim>"
```

`notification.apns` must contain an `aps` key. `-b/--bundle-id` is optional if the payload includes a `Simulator Target Bundle` key.

## Troubleshooting

- **Build fails**: Run `flowdeck context --json` or `flowdeck project schemes` to confirm the scheme name. On failure, `flowdeck build` prints the extracted reason and a `Full log: <path>` line — read that file rather than rerunning with `-v/--verbose`.
- **App won't launch**: Check `flowdeck simulator app info <bundle-id> -S "<sim>"` for bundle metadata, or `flowdeck apps` to see what FlowDeck currently has tracked.
- **Simulator not found**: `flowdeck simulator list --available-only`; create one with `flowdeck simulator create -n "<name>" --device-type "<type>" --runtime "<runtime>"` if needed.
- **Clean build**: `flowdeck clean`, or `flowdeck clean --all` to clear all caches.

## Common Commands Reference

| Task | FlowDeck Command | Notes |
|------|-------------------|-------|
| List simulators | `flowdeck simulator list --json` | Check `state` field for `"Booted"`/`"Shutdown"` |
| Boot simulator | `flowdeck simulator boot <udid>` | Positional UDID only, not a name — resolve via `simulator list --json` first |
| Shutdown simulator | `flowdeck simulator shutdown <udid>` | |
| Erase simulator | `flowdeck simulator erase <udid>` | Simulator must be shut down first |
| Install app | `flowdeck run` (build+install+launch), or `flowdeck run --no-build` (install+launch an existing build) | No standalone simulator-only "install" verb exists in FlowDeck |
| Uninstall app | `flowdeck uninstall <app-id-or-bundle-id>` | Destructive — requires explicit user consent; not part of FlowDeck's automatic validation loop |
| Launch app | `flowdeck run` for apps FlowDeck built; `flowdeck simulator launch <bundle-id> -S <udid>` for apps FlowDeck did not build (system apps, pre-installed builds) | |
| Terminate app | `flowdeck stop <app-id-or-bundle-id>` | Targets an app FlowDeck is tracking (launched via `run` or `simulator launch`) — see `flowdeck apps` for identifiers. `--force` sends `SIGKILL` for a stuck app. |
| Get app container | `flowdeck simulator app container <bundle-id> [-c app\|data\|groups\|<group-id>] -S <udid>` | `-c/--container` defaults to `app` |

For anything not covered above — hardware buttons, appearance, Dynamic Type, privacy grants, keychain, pasteboard, watch/phone pairing — see `resources/simulator.md` and `resources/ui.md` in the `flowdeck` skill.
