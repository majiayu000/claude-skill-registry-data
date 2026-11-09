---
name: timeline-browser-transport
description: Use when relaunching the CDP browser or its extension goes silent.
version: 1.0.0
author: Timeline
license: MIT
platforms: [macos]
metadata:
    hermes:
        tags: [cdp, brave, extension, relaunch, transport]
---

# Timeline Browser Transport

The bookmark pipeline drives the person's own browser over CDP, and Hermes Control reaches that same
browser through an unpacked extension. Both are transport, not application logic: when they break,
every downstream symptom looks like a data bug.

No handle, list id or session id belongs in this file. Tab identity comes from the gitignored
identifier map (`Documentation/Reference/Configure.md`); a command takes a slug, never an id.

## A command reaches the browser through `Transport`, never `Browser/`

`Source/Transport/Transport.ts` is the seam. A command declares what it needs
(`transport: "read" | "write" | "browser"`), receives a `CommandContext`, and calls
`context.transport`. `Source/Browser/` is the CDP implementation detail: the client, the selectors
and the session, reachable only from `Source/Transport/CDP/`.

A new browser command therefore adds nothing to `Browser/` and imports nothing from it. If the
interface has no member for what the command needs, that is the interface's gap, not a reason to
reach past it. A command that names `Transport/CDP` or `Transport/View` is a defect; nothing in the
tree tests for it, so the rule is held by review.

`--transport view` answers read commands from the shadow store with the same JSON shapes and refuses
everything else (`read-only-transport` for a write, `unsupported-transport` for a tab, a page or a
scrape). It is never a fallback: with the debug port closed, `tab list` fails `cdp-unreachable`
instead of answering from the archive.

## When to Use

- Relaunching the browser instances.
- `curl -s http://127.0.0.1:9222/json/version` answers nothing.
- `tab_*` tools report that no browser is connected.
- A relaunch "succeeded" but the extension is missing afterwards.

## Two instances, two profiles

A second debug instance needs its own `--user-data-dir`. Chromium locks each profile directory, so
relaunching on a directory already in use starts no second process and silently drops the flags.
Launch both explicitly, so each is identifiable by its own command line rather than by assumption:

```sh
# the person's normal browser
"/Applications/Brave Browser.app/Contents/MacOS/Brave Browser" \
	--user-data-dir="$HOME/Library/Application Support/BraveSoftware/Brave-Browser" \
	--no-first-run --no-default-browser-check

# the CDP instance
"/Applications/Brave Browser.app/Contents/MacOS/Brave Browser" \
	--remote-debugging-port=9222 \
	--user-data-dir="$HOME/.hermes/cache/scratch/brave-cdp-profile" \
	--load-extension="$HOME/<path-to-extension>/dist" \
	--disable-features=DisableLoadExtensionCommandLineSwitch \
	--no-first-run --no-default-browser-check
```

Quit gracefully (`kill -TERM <main-pid>`) rather than force-killing: the profile writes its session
on a clean exit. Confirm the port is free before relaunching with
`lsof -nP -iTCP:9222 -sTCP:LISTEN`.

## Chromium 156+ ignores `--load-extension`

Without `--disable-features=DisableLoadExtensionCommandLineSwitch` the launch succeeds with **no
extension loaded and no error**. The profile keeps a ghost registration: the id sits in
`Secure Preferences` → `extensions.settings` with `location: 4` (unpacked) and neither `path` nor
`manifest`, and every `chrome-extension://<id>/…` tab renders as a dead page whose title is the raw
URL and whose `chrome.storage` is `undefined` - the limited `window.chrome` object, not an extension
context.

An extension that a previous session was using can therefore disappear purely because a relaunch
omitted the flag. Always re-probe after a relaunch instead of assuming the old targets survived.

## Prove the extension loaded

The background worker is the only positive signal; the launch exit code is not:

```sh
curl -s --max-time 5 http://127.0.0.1:9222/json/list \
	| grep -o 'chrome-extension://[a-z]*/background.js'
```

Poll more than once. An MV3 background worker is absent while idle, so a single empty result is not
a verdict.

## A command-line extension never starts its own heartbeat

`--load-extension` does not fire `onInstalled`, so an extension whose periodic work is a
`chrome.alarms` job never creates that alarm. It loads, its worker sleeps, and it stays silent
indefinitely.

```sh
grep 'browser-control/register' $HERMES_HOME/logs/gateway.log | tail -1
```

Observed on a `--load-extension` relaunch: the background worker was present, yet no
`browser-control/register` request arrived for 12+ minutes. Opening the extension's `sidepanel.html`
with `PUT /json/new` did not change that - it renders as a plain tab with no extension APIs. The
reliable trigger is the person clicking the toolbar icon, which opens the real side panel and starts
the heartbeat. Report that as the remaining step; do not call the extension healthy because its
target exists.

## Restoring the tab set

A profile with `session.restore_on_startup` unset opens a new tab page, not the previous session, so
a relaunch loses the person's tabs even though the session files exist. Reopen the known set and let
the titles prove the session:

```sh
curl -s -X PUT "http://127.0.0.1:9222/json/new?<URL-encoded-URL>" > /dev/null
```

A logged-in title (the person's handle, not `@undefined`) is the evidence that the profile still
carries the session. Titles that stay as raw URLs mean the page has not finished loading, not that
the session is gone - re-read the list after a few seconds.

## Claim → test

| Claim                              | Test                                                                                                |
| ---------------------------------- | --------------------------------------------------------------------------------------------------- |
| A browser is exposing CDP          | `curl -s http://127.0.0.1:9222/json/version` returns a `Protocol-Version`                           |
| Which profile owns the port        | `PID=$(lsof -nP -iTCP:9222 -sTCP:LISTEN -t \| head -1); ps -o command= -p "$PID"`                   |
| Both instances are up              | `ps -eo command \| grep '[B]rave Browser' \| grep -o -- '--user-data-dir=[^ ]*' \| sort \| uniq -c` |
| The extension actually loaded      | `curl -s http://127.0.0.1:9222/json/list \| grep -o 'chrome-extension://[a-z]*/background.js'`      |
| The extension is talking to Hermes | `grep 'browser-control/register' $HERMES_HOME/logs/gateway.log \| tail -1` shows a recent timestamp |
| Tabs came back and are logged in   | `curl -s http://127.0.0.1:9222/json/list` shows resolved titles, not `@undefined`                   |
