---
name: mac-defaults
description: Read and change Mac app and system preferences from the shell with `defaults` — and find the hidden key behind any setting by diffing before and after you flip it. Use when you say "change this setting from the terminal", "what's the defaults command for X", "script my Mac setup", "show hidden files", "make the Dock autohide", "my defaults write didn't do anything", "back up my app preferences". Covers read/write/types, domains, the diff method, applying changes, sandboxed app containers and the cfprefsd cache.
compatibility: >-
  macOS (tested on macOS 26, Apple silicon). Built-in tools only: defaults, plutil, killall. No network.
metadata:
  grounded: "2026-11-03 — read/write/delete run live against a throwaway domain on macOS 26.6"
---

# `defaults`: preferences as data

Every app's settings are a plist keyed by a **domain** (usually the bundle id). `defaults`
talks to `cfprefsd`, the daemon that owns them. **Always go through `defaults`; never edit
the `.plist` file directly.** cfprefsd caches, and a file edit is overwritten or ignored.

## Read

```bash
defaults read com.apple.dock autohide          # one key  -> 1
defaults read-type com.apple.dock autohide     # -> Type is boolean
defaults read -g AppleInterfaceStyle           # -g = global domain (NSGlobalDomain) -> Dark
defaults read com.apple.finder                 # whole domain
defaults domains | tr ',' '\n'                 # every domain you have
defaults find ShowPathbar                      # search all domains for a key or value
defaults export com.apple.dock - | plutil -p - # whole domain as a plist, readable
```

`The domain/default pair of (X, Y) does not exist` is **not an error about your command**:
it means the key was never set and the app is using its built-in default. Writing the key
creates it.

## Write — always state the type

```bash
defaults write com.apple.finder AppleShowAllFiles -bool true
defaults write com.apple.dock tilesize -int 48
defaults write com.apple.screencapture location -string "$HOME/Pictures/Screenshots"
defaults write local.example list -array a b c
defaults write local.example map -dict-add key value
defaults delete com.apple.dock tilesize        # back to the app's default
```

Without `-bool`/`-int`/`-float`, the value is written as a **string**. Some APIs coerce `"true"`, many don't, and you can't tell which from outside;
write the real type. Check with `read-type` after writing.

## Make it take effect

Most apps read preferences at launch. After a write:

```bash
killall Dock          # Dock, Mission Control, Launchpad
killall Finder        # Finder
killall SystemUIServer # menu bar extras
```

For any other app: quit and reopen it. Some system settings only apply at next login.
Killing an app the user has open loses their unsaved state in it; say so before you do it.

## Find the key behind a setting (the diff method)

There is no index of `defaults` keys. Find one by watching it change:

```bash
defaults read > /tmp/before.txt            # every domain, ~700 KB
# flip the setting once in System Settings or the app's Settings window
defaults read > /tmp/after.txt
diff /tmp/before.txt /tmp/after.txt
```

Narrow it once you know the domain: `defaults read com.apple.finder > before`. Also diff
`defaults -currentHost read` for per-machine settings (stored under `ByHost/`), which a
plain `read` does not show.

## Traps

- **Sandboxed apps keep preferences in a container.** For many App Store and Apple apps
  the file lives at
  `~/Library/Containers/<bundle-id>/Data/Library/Preferences/<bundle-id>.plist`, and
  reading it may need Full Disk Access for your terminal (`mac-permissions` skill).
  `defaults read <bundle-id>` resolves the container for you when access allows.
- **`defaults delete <domain>` leaves the file behind.** Verified: after deleting a
  whole domain, `defaults read` says it doesn't exist but the `.plist` file is still in
  `~/Library/Preferences/`. Harmless; remove the file only if you created it.
- **Managed (MDM) preferences win.** On a work Mac a profile can force a value; your
  write succeeds and is ignored. `defaults read` shows the forced value.
- **Some settings are not in `defaults` at all**: anything gated by TCC, most of
  System Settings' privacy panes, and per-user settings stored in databases. Those are
  `mac-permissions` and `mac-automation` territory.

## Script a whole setup

Put the writes in one script, then one `killall` per affected app at the end. Back up
first: `defaults export com.apple.dock ~/dock-backup.plist`, and restore with
`defaults import com.apple.dock ~/dock-backup.plist`.
