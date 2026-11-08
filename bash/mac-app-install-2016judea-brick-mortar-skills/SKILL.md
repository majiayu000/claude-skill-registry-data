---
name: mac-app-install
description: Install, inspect and unblock software on a Mac from a session — Homebrew formulae and casks, Mac App Store apps with mas (and the GUI fallback when mas needs root), plus quarantine and Gatekeeper ("app is damaged", "can't be opened because Apple cannot check it"). Use when you say "install X", "is X installed", "what version do I have", "brew says...", "mas install fails", "install from the App Store", "the app is damaged and can't be opened", "remove the quarantine flag", "is this app signed". Covers read-only checks first, which installs need a human, and the traps that make a read write.
compatibility: >-
  macOS (tested on macOS 26, Apple silicon). Uses Homebrew (formulae.brew.sh, github.com, ghcr.io) and mas (Apple's App Store) when installed; xattr, spctl, codesign are built in.
metadata:
  grounded: "2026-11-03 — every read and the quarantine round-trip run live on macOS 26.6; nothing installed"
  network-hosts: "formulae.brew.sh, github.com, ghcr.io, apps.apple.com"
  network-purpose: "package metadata and downloads for Homebrew and the App Store"
---

# Installing software on a Mac

Check before installing. Most "install X" requests are already satisfied, and a lot of
tools ship with macOS now (`jq` is at `/usr/bin/jq` on recent macOS, for example).

## Is it already here?

```bash
command -v jq; which -a python3                 # every copy on PATH, first one wins
brew list --versions jq                         # installed by brew? (empty = no)
mdfind "kMDItemCFBundleIdentifier == 'com.example.App'" 2>/dev/null   # an app, anywhere
ls /Applications ~/Applications
mas list                                        # App Store apps: id, name, version
```

`which jq` finding `/usr/bin/jq` while `brew list` says not installed is normal: the
system copy, not brew's. Know which one a script will run.

## Homebrew: read without writing

**Many brew commands auto-update brew first**, downloading and rewriting its taps (verified:
`brew outdated` pulled a new portable Ruby and updated three taps). For read-only queries:

```bash
export HOMEBREW_NO_AUTO_UPDATE=1
brew info --json=v2 jq | jq -r '.formulae[0] | "\(.name) \(.versions.stable) installed=\(.installed|length)"'
brew outdated --quiet
brew uses --installed jq                       # what depends on it
brew info --cask --json=v2 visual-studio-code | jq '.casks[0].artifacts'
curl -s https://formulae.brew.sh/api/formula/jq.json | jq -r '.versions.stable, .license'
```

The JSON API at `formulae.brew.sh/api/formula/<name>.json` (and `/api/cask/<name>.json`)
answers "what version, what licence, what does it depend on" without touching the local
install.

## Homebrew: install (the user asked for it)

```bash
brew install jq                  # CLI tool (formula), no sudo on Apple silicon
brew install --cask firefox      # GUI app into /Applications
brew upgrade jq
brew uninstall jq
```

- Prefix is `/opt/homebrew` on Apple silicon, `/usr/local` on Intel. A LaunchAgent won't
  find either without a PATH (`mac-launchd`).
- A cask that installs a `.pkg` or a system extension asks for an admin password; a
  non-interactive session cannot answer. Stop and hand it to the user.
- `Untrusted tap` warnings mean a third-party tap was added at some point; installing from
  it runs that tap author's code.

## Mac App Store

```bash
mas search "Xcode"            # id + name + version
mas list
mas install 497799835         # by id
```

`mas` v7 **needs root to install** (`requires root privileges`), which a non-interactive
shell can't give. The fallback that works for a **free** app under the signed-in account:
open its page and GUI-script the buttons through System Events (`mac-automation`):

```bash
open "macappstore://apps.apple.com/app/id497799835"
# then walk `UI elements of window 1 of process "App Store"` to find the buttons:
# first launch shows a welcome sheet (Continue), then Get, then Install on a confirm sheet
```

Screenshot between steps (`mac-screenshots`), because button names aren't discoverable
without walking the tree. Never do this while the user is working at the keyboard (it takes
focus), and **never for a paid app**: that is spending the user's money.

## "Damaged", "can't be opened": quarantine and Gatekeeper

Files downloaded by a browser or mail client get a `com.apple.quarantine` xattr, and
Gatekeeper checks the first launch. `curl` and `brew` downloads do **not** get it (verified:
a `curl` download carried only `com.apple.provenance`).

```bash
xattr file.dmg                                   # list attributes
xattr -p com.apple.quarantine App.app            # 0081;<hex time>;<agent>;<uuid>
spctl --status                                   # assessments enabled = Gatekeeper on
spctl -a -vv -t exec /Applications/App.app       # accepted / rejected, and why
codesign -dv /Applications/App.app 2>&1 | grep -E "Identifier|TeamIdentifier"
```

To open an app the user trusts and chose to download:

```bash
xattr -d com.apple.quarantine /Applications/App.app        # one file
xattr -dr com.apple.quarantine /Applications/App.app       # recursively, for a bundle
```

This turns off a security check **for that app**. Only do it for software the user
deliberately downloaded from a source they trust, and say what you did. Never disable
Gatekeeper globally (`spctl --master-disable`).

## Uninstall

`brew uninstall`, `brew uninstall --cask`, or drag from `/Applications`. Leftovers live in
`~/Library/Application Support/<app>`, `~/Library/Preferences/<bundle-id>.plist`,
`~/Library/Caches/<bundle-id>`, `~/Library/Containers/<bundle-id>`. Removing those
deletes the user's data for that app; list them, let the user decide.
