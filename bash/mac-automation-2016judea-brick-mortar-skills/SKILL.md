---
name: mac-automation
description: Drive Mac apps and the desktop from the shell — AppleScript and JavaScript (JXA) via osascript, UI scripting through System Events, notifications, dialogs, the clipboard, `open` tricks and the Shortcuts CLI. Use when you say "automate this app", "click that button for me", "send me a notification when it's done", "copy this to my clipboard", "run my shortcut", "open this file in X", "what's the frontmost app", "get the bundle id". Covers the exact one-liners, how to discover a UI element's name, how not to hang on a consent prompt, and how not to clobber the user's clipboard.
compatibility: >-
  macOS (tested on macOS 26, Apple silicon). Built-in tools only: osascript, pbcopy/pbpaste, open, shortcuts, mdfind. No network. Controlling another app needs the Automation permission; UI scripting needs Accessibility.
metadata:
  grounded: "2026-11-03 — every one-liner run live on macOS 26.6"
---

# Mac automation from the shell

Order of preference, cheapest and sturdiest first:

1. **A CLI or file the app already exposes** (`defaults`, a sqlite db, the app's own CLI).
2. **The app's scripting dictionary** (`tell application "Finder" to ...`). Stable across
   versions. See what an app supports: open Script Editor > File > Open Dictionary.
3. **The Shortcuts CLI**, if the user already built a shortcut.
4. **UI scripting** through System Events (clicking buttons by name). Brittle, needs
   Accessibility, breaks on every redesign. Last resort.

## One-liners that work

```bash
osascript -e 'tell application "System Events" to get name of first process whose frontmost is true'
osascript -e 'id of app "Safari"'                          # bundle id -> com.apple.Safari
osascript -e 'POSIX path of (path to application "Safari")'
osascript -e 'display notification "Build finished" with title "Done" sound name "Glass"'
osascript -e 'tell application "Finder" to get name of startup disk'
osascript -e 'tell application "TextEdit" to quit'          # polite quit (saves prompt)
```

JXA is the same bridge in JavaScript, and can reach Objective-C frameworks:

```bash
osascript -l JavaScript -e 'Application("System Events").processes.whose({frontmost:true})[0].name()'
osascript -l JavaScript -e 'var a=Application.currentApplication(); a.includeStandardAdditions=true; a.doShellScript("sw_vers -productVersion")'
```

Dialogs (`display dialog`, `choose file`) **block until a human clicks**. Never put one in
an unattended script; use a notification instead.

## Clipboard

```bash
printf '%s' "text" | pbcopy
pbpaste
osascript -e 'the clipboard as text'
```

**Save and restore the user's clipboard if you only need it as a pipe.** It is their
working memory, and overwriting it destroys whatever they copied last:

```bash
saved=$(pbpaste); printf '%s' "$payload" | pbcopy; ...; printf '%s' "$saved" | pbcopy
```

This only restores text; an image or file on the clipboard is lost. If the clipboard
holds non-text, don't touch it.

## `open`

```bash
open file.pdf                       # default app
open -a "Preview" file.png          # a named app
open -b com.apple.TextEdit file.txt # by bundle id (survives app renames)
open -g -a "Mail"                   # launch in the background, don't steal focus
open -j -a "Notes"                  # launch hidden
open -R file.txt                    # reveal in Finder
open -W -a "TextEdit" f.txt         # wait until the app quits
open "x-apple.systempreferences:"   # System Settings
```

Find where an app lives: `mdfind "kMDItemCFBundleIdentifier == 'com.apple.TextEdit'"`.

Every `open` puts a window or focus change on the user's screen. If they are working,
prefer `-g`, and never open things they didn't ask for.

## Shortcuts

```bash
shortcuts list                         # empty output = the user has no shortcuts
shortcuts run "Shortcut Name"
shortcuts run "Resize Image" -i in.png -o out.png
```

A shortcut can do things that have no CLI (Focus modes, HomeKit, some app intents). If
the user has one, run it rather than rebuilding it.

## UI scripting (System Events)

```bash
osascript -e 'tell application "System Events" to tell process "Finder" to get name of every menu bar item of menu bar 1'
osascript -e 'tell application "System Events" to tell process "Finder" to click menu item "New Finder Window" of menu "File" of menu bar 1'
osascript -e 'tell application "System Events" to keystroke "n" using command down'
```

- **Discover names by walking the tree**: `get entire contents of window 1 of process "X"`
  (slow) or `get UI elements of window 1 of process "X"`, one level at a time.
- `get name of menu bars` returns `missing value`; ask for the *items* of `menu bar 1`.
- `keystroke` goes to whatever is frontmost **right now**. Activate the target app first,
  and never send keystrokes while the user is typing.
- Apps with custom-drawn controls (many SwiftUI and Electron apps) expose no titles to
  Accessibility; UI scripting can't see them. A screenshot (`mac-screenshots`) plus
  coordinates is the fallback, and it is fragile.

## Don't hang

macOS ships **no `timeout` command**. The first `tell application "X"` from a new
responsible app opens an Automation consent dialog and blocks forever if nobody answers.
Wrap anything unattended:

```bash
perl -e 'alarm 10; exec @ARGV' osascript -e 'tell application "Notes" to count notes'
echo $?    # 142 = timed out
```

Errors decoded and how to check grants first: `mac-permissions` skill.
